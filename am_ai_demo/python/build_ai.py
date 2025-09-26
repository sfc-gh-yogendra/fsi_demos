"""
AI Components Builder for SAM Demo

This module creates AI components including:
- Semantic views for Cortex Analyst
- Cortex Search services for document types
- Validation and testing of AI components
"""

from snowflake.snowpark import Session
from typing import List
import config

def build_all(session: Session, scenarios: List[str], build_semantic: bool = True, build_search: bool = True):
    """
    Build AI components for the specified scenarios.
    
    Args:
        session: Active Snowpark session
        scenarios: List of scenario names
        build_semantic: Whether to build semantic views
        build_search: Whether to build search services
    """
    print("🤖 Starting AI components build...")
    print(f"   Scenarios: {', '.join(scenarios)}")
    
    if build_semantic:
        print("🧠 Building semantic views...")
        try:
            create_semantic_views(session, scenarios)
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Semantic view creation failed: {e}")
            print("🛑 STOPPING BUILD - Cannot continue without semantic views")
            raise
    
    if build_search:
        print("🔍 Building Cortex Search services...")
        try:
            create_search_services(session, scenarios)
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Search service creation failed: {e}")
            print("🛑 STOPPING BUILD - Cannot continue without required search services")
            raise
    
    # Validate components
    print("✅ Validating AI components...")
    try:
        validate_components(session, build_semantic, build_search)
    except Exception as e:
        print(f"❌ CRITICAL FAILURE: AI component validation failed: {e}")
        print("🛑 STOPPING BUILD - AI components not working properly")
        raise
    
    print("✅ AI components build complete")

def create_semantic_views(session: Session, scenarios: List[str] = None):
    """Create semantic views required for the specified scenarios."""
    
    try:
        # Create proper semantic view with correct syntax patterns
        session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW
	TABLES (
		HOLDINGS AS {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HOLDINGDATE, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('positions','investments','allocations','holdings') 
			COMMENT='Daily portfolio holdings and positions. Each portfolio holding has multiple rows. When no time period is provided always get the latest value by date.',
		PORTFOLIOS AS {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('funds','strategies','mandates','portfolios') 
			COMMENT='Investment portfolios and fund information',
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','bonds','instruments','securities') 
			COMMENT='Master security reference data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate hierarchy data'
	)
	RELATIONSHIPS (
		HOLDINGS_TO_PORTFOLIOS AS HOLDINGS(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		HOLDINGS_TO_SECURITIES AS HOLDINGS(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		SECURITIES_TO_ISSUERS AS SECURITIES(ISSUERID) REFERENCES ISSUERS(ISSUERID)
	)
	DIMENSIONS (
		-- Portfolio dimensions
		PORTFOLIOS.PORTFOLIONAME AS PortfolioName WITH SYNONYMS=('fund_name','strategy_name','portfolio_name') COMMENT='Portfolio or fund name',
		PORTFOLIOS.STRATEGY AS Strategy WITH SYNONYMS=('investment_strategy','portfolio_strategy','strategy_type','value_strategy','growth_strategy') COMMENT='Investment strategy: Value, Growth, ESG, Core, Multi-Asset, Income',
		
		-- Security dimensions  
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('company','security_name','description') COMMENT='Security description or company name',
		SECURITIES.TICKER AS Ticker WITH SYNONYMS=('ticker_symbol','symbol','primary_ticker') COMMENT='Primary trading symbol',
		SECURITIES.ASSETCLASS AS AssetClass WITH SYNONYMS=('instrument_type','security_type','asset_class') COMMENT='Asset class: Equity, Corporate Bond, ETF',
		
		-- Issuer dimensions (for enhanced analysis)
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('issuer_name','legal_name','company_name') COMMENT='Legal issuer name',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('sector','industry_sector','gics_sector') COMMENT='GICS Level 1 sector classification',
		ISSUERS.COUNTRYOFINCORPORATION AS CountryOfIncorporation WITH SYNONYMS=('domicile','country_of_risk','country') COMMENT='Country of incorporation',
		
		-- Time dimensions
		HOLDINGS.HOLDINGDATE AS HoldingDate WITH SYNONYMS=('position_date','as_of_date','date') COMMENT='Holdings as-of date'
	)
	METRICS (
		-- Core position metrics
		HOLDINGS.TOTAL_MARKET_VALUE AS SUM(MarketValue_Base) WITH SYNONYMS=('exposure','total_exposure','aum','market_value','position_value') COMMENT='Total market value in base currency',
		HOLDINGS.HOLDING_COUNT AS COUNT(SecurityID) WITH SYNONYMS=('position_count','number_of_holdings','holding_count','count') COMMENT='Count of portfolio positions',
		
		-- Portfolio weight metrics  
		HOLDINGS.PORTFOLIO_WEIGHT AS SUM(PortfolioWeight) WITH SYNONYMS=('weight','allocation','portfolio_weight') COMMENT='Portfolio weight as decimal',
		HOLDINGS.PORTFOLIO_WEIGHT_PCT AS SUM(PortfolioWeight) * 100 WITH SYNONYMS=('weight_percent','allocation_percent','percentage_weight') COMMENT='Portfolio weight as percentage',
		
		-- Issuer-level metrics (enhanced capability)
		HOLDINGS.ISSUER_EXPOSURE AS SUM(MarketValue_Base) WITH SYNONYMS=('issuer_total','issuer_value','issuer_exposure') COMMENT='Total exposure to issuer across all securities',
		
		-- Concentration metrics
		HOLDINGS.MAX_POSITION_WEIGHT AS MAX(PortfolioWeight) WITH SYNONYMS=('largest_position','max_weight','concentration') COMMENT='Largest single position weight'
	)
	COMMENT='Multi-asset semantic view for portfolio analytics with issuer hierarchy support';
        """).collect()
        
        print("   ✅ Created semantic view: SAM_ANALYST_VIEW")
        
    except Exception as e:
        print(f"❌ Failed to create semantic view: {e}")
        raise
    
    # Create scenario-specific semantic views
    if scenarios and 'research_copilot' in scenarios:
        try:
            print("📊 Creating research semantic view with fundamentals...")
            create_research_semantic_view(session)
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Could not create research semantic view: {e}")
            print("   This is required for research_copilot scenario")
            raise Exception(f"Failed to create research semantic view: {e}")
    
    # Create quantitative semantic view for factor analysis
    if scenarios and 'quant_analyst' in scenarios:
        try:
            print("📊 Creating quantitative semantic view for factor analysis...")
            create_quantitative_semantic_view(session)
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Could not create quantitative semantic view: {e}")
            print("   This is required for quant_analyst scenarios")
            raise Exception(f"Failed to create quantitative semantic view: {e}")
    
    # Create implementation semantic view for portfolio management
    if scenarios and ('portfolio_copilot' in scenarios or 'sales_advisor' in scenarios):
        try:
            print("🎯 Creating implementation semantic view for portfolio management...")
            create_implementation_semantic_view(session)
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Could not create implementation semantic view: {e}")
            print("   This is required for portfolio_copilot and sales_advisor scenarios")
            raise Exception(f"Failed to create implementation semantic view: {e}")
    
    # Create SEC filings semantic view for financial analysis
    try:
        print("💰 Creating SEC filings semantic view for financial analysis...")
        create_sec_filings_semantic_view(session)
    except Exception as e:
        print(f"❌ CRITICAL FAILURE: Could not create SEC filings semantic view: {e}")
        print("   This is required for comprehensive financial analysis")
        raise Exception(f"Failed to create SEC filings semantic view: {e}")

def create_research_semantic_view(session: Session):
    """Create semantic view for research with fundamentals and estimates data."""
    
    # First check if the fundamentals tables exist
    try:
        session.sql(f"SELECT 1 FROM {config.DATABASE_NAME}.CURATED.FACT_FUNDAMENTALS LIMIT 1").collect()
        session.sql(f"SELECT 1 FROM {config.DATABASE_NAME}.CURATED.FACT_ESTIMATES LIMIT 1").collect()
    except:
        print("⚠️  Fundamentals tables not found, skipping research view creation")
        return
    
    # Create the research-focused semantic view
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_RESEARCH_VIEW
	TABLES (
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','equities','securities') 
			COMMENT='Security master data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate data',
		FUNDAMENTALS AS {config.DATABASE_NAME}.CURATED.FACT_FUNDAMENTALS
			PRIMARY KEY (SECURITY_ID, REPORTING_DATE, METRIC_NAME)
			WITH SYNONYMS=('financials','earnings','results','fundamentals')
			COMMENT='Company financial fundamentals',
		ESTIMATES AS {config.DATABASE_NAME}.CURATED.FACT_ESTIMATES
			PRIMARY KEY (SECURITY_ID, ESTIMATE_DATE, FISCAL_PERIOD, METRIC_NAME) 
			WITH SYNONYMS=('forecasts','estimates','guidance','consensus') 
			COMMENT='Analyst estimates and guidance'
	)
	RELATIONSHIPS (
		SECURITIES_TO_ISSUERS AS SECURITIES(ISSUERID) REFERENCES ISSUERS(ISSUERID),
		FUNDAMENTALS_TO_SECURITIES AS FUNDAMENTALS(SECURITY_ID) REFERENCES SECURITIES(SECURITYID),
		ESTIMATES_TO_SECURITIES AS ESTIMATES(SECURITY_ID) REFERENCES SECURITIES(SECURITYID)
	)
	DIMENSIONS (
		-- Security dimensions  
		SECURITIES.TICKER AS Ticker WITH SYNONYMS=('ticker','symbol','ticker_symbol') COMMENT='Trading ticker symbol',
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('company','name','security_name') COMMENT='Company name',
		SECURITIES.ASSETCLASS AS AssetClass WITH SYNONYMS=('type','security_type','asset_class') COMMENT='Asset class',
		
		-- Issuer dimensions
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('issuer','legal_name','entity_name') COMMENT='Legal entity name',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('sector','industry_sector','gics') COMMENT='GICS sector',
		ISSUERS.COUNTRYOFINCORPORATION AS CountryOfIncorporation WITH SYNONYMS=('domicile','country','headquarters') COMMENT='Country of incorporation',
		
		-- Fundamentals dimensions
		FUNDAMENTALS.REPORTING_DATE AS REPORTING_DATE WITH SYNONYMS=('report_date','earnings_date','date') COMMENT='Financial reporting date',
		FUNDAMENTALS.FISCAL_QUARTER AS FISCAL_QUARTER WITH SYNONYMS=('quarter','period','fiscal_period') COMMENT='Fiscal quarter',
		FUNDAMENTALS.METRIC_NAME AS METRIC_NAME WITH SYNONYMS=('metric','measure','financial_metric') COMMENT='Financial metric name',
		
		-- Estimates dimensions
		ESTIMATES.FISCAL_PERIOD AS FISCAL_PERIOD WITH SYNONYMS=('forecast_period','estimate_quarter') COMMENT='Estimate fiscal period'
	)
	METRICS (
		-- Actual financial metrics
		FUNDAMENTALS.ACTUAL_VALUE AS SUM(METRIC_VALUE) WITH SYNONYMS=('actual','reported','result') COMMENT='Actual reported value',
		
		-- Estimate metrics
		ESTIMATES.ESTIMATE_VALUE AS SUM(ESTIMATE_VALUE) WITH SYNONYMS=('estimate','forecast','consensus') COMMENT='Consensus estimate value',
		ESTIMATES.GUIDANCE_LOW AS MIN(GUIDANCE_LOW) WITH SYNONYMS=('guidance_low','low_guidance') COMMENT='Low end of guidance',
		ESTIMATES.GUIDANCE_HIGH AS MAX(GUIDANCE_HIGH) WITH SYNONYMS=('guidance_high','high_guidance') COMMENT='High end of guidance',
		
		-- Count metrics
		FUNDAMENTALS.METRIC_COUNT AS COUNT(DISTINCT FUNDAMENTALS.METRIC_NAME) WITH SYNONYMS=('metric_count','measures_count') COMMENT='Count of financial metrics',
		ESTIMATES.ESTIMATE_COUNT AS COUNT(DISTINCT ESTIMATES.METRIC_NAME) WITH SYNONYMS=('estimate_count','forecasts_count') COMMENT='Count of estimate metrics'
	)
	COMMENT='Research semantic view with fundamentals and estimates for earnings analysis';
    """).collect()
    
    print("   ✅ Created semantic view: SAM_RESEARCH_VIEW")

def create_quantitative_semantic_view(session: Session):
    """Create semantic view for quantitative analysis with factors and attribution."""
    
    # First check if the quantitative tables exist
    quant_tables = [
        'FACT_FACTOR_EXPOSURES',
        'FACT_FUNDAMENTALS',
        'FACT_ESTIMATES', 
        'FACT_MARKETDATA_TIMESERIES',
        'FACT_BENCHMARK_HOLDINGS'
    ]
    
    missing_tables = []
    for table in quant_tables:
        try:
            session.sql(f"SELECT 1 FROM {config.DATABASE_NAME}.CURATED.{table} LIMIT 1").collect()
        except:
            missing_tables.append(table)
    
    if missing_tables:
        print(f"⚠️  Quantitative tables not found, skipping quant view creation: {missing_tables}")
        return
    
    # Create the quantitative analysis semantic view
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_QUANT_VIEW
	TABLES (
		HOLDINGS AS {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HoldingDate, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('quant_positions','factor_holdings','quantitative_holdings','quant_allocations') 
			COMMENT='Portfolio holdings for factor analysis',
		PORTFOLIOS AS {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('quant_funds','factor_strategies','quantitative_mandates','quant_portfolios') 
			COMMENT='Portfolio information',
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('factor_companies','quant_stocks','quantitative_instruments','factor_securities') 
			COMMENT='Security reference data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('factor_issuers','quantitative_entities','quant_corporates') 
			COMMENT='Issuer data',
		FACTOR_EXPOSURES AS {config.DATABASE_NAME}.CURATED.FACT_FACTOR_EXPOSURES
			PRIMARY KEY (SECURITYID, EXPOSURE_DATE, FACTOR_NAME)
			WITH SYNONYMS=('factors','loadings','exposures','factor_data')
			COMMENT='Factor exposures and loadings',
		FUNDAMENTALS AS {config.DATABASE_NAME}.CURATED.FACT_FUNDAMENTALS
			PRIMARY KEY (SECURITY_ID, REPORTING_DATE, METRIC_NAME)
			WITH SYNONYMS=('financials','earnings','fundamentals','metrics')
			COMMENT='Financial fundamentals data',
		ESTIMATES AS {config.DATABASE_NAME}.CURATED.FACT_ESTIMATES
			PRIMARY KEY (SECURITY_ID, ESTIMATE_DATE, FISCAL_PERIOD, METRIC_NAME)
			WITH SYNONYMS=('forecasts','estimates','consensus','guidance')
			COMMENT='Analyst estimates and guidance',
		MARKET_DATA AS {config.DATABASE_NAME}.CURATED.FACT_MARKETDATA_TIMESERIES
			PRIMARY KEY (PriceDate, SECURITYID)
			WITH SYNONYMS=('prices','returns','market_data','performance')
			COMMENT='Market data and returns',
		BENCHMARK_HOLDINGS AS {config.DATABASE_NAME}.CURATED.FACT_BENCHMARK_HOLDINGS
			PRIMARY KEY (HOLDING_DATE, BENCHMARKID, SECURITYID)
			WITH SYNONYMS=('benchmark_positions','index_holdings','benchmark_weights')
			COMMENT='Benchmark constituent holdings and weights'
	)
	RELATIONSHIPS (
		HOLDINGS_TO_PORTFOLIOS AS HOLDINGS(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		HOLDINGS_TO_SECURITIES AS HOLDINGS(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		SECURITIES_TO_ISSUERS AS SECURITIES(ISSUERID) REFERENCES ISSUERS(ISSUERID),
		FACTORS_TO_SECURITIES AS FACTOR_EXPOSURES(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		FUNDAMENTALS_TO_SECURITIES AS FUNDAMENTALS(SECURITY_ID) REFERENCES SECURITIES(SECURITYID),
		ESTIMATES_TO_SECURITIES AS ESTIMATES(SECURITY_ID) REFERENCES SECURITIES(SECURITYID),
		MARKET_DATA_TO_SECURITIES AS MARKET_DATA(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		BENCHMARK_TO_SECURITIES AS BENCHMARK_HOLDINGS(SECURITYID) REFERENCES SECURITIES(SECURITYID)
	)
	DIMENSIONS (
		-- Portfolio dimensions
		PORTFOLIOS.PORTFOLIONAME AS PortfolioName WITH SYNONYMS=('quant_fund_name','factor_strategy_name','quantitative_portfolio_name') COMMENT='Portfolio or fund name',
		PORTFOLIOS.STRATEGY AS Strategy WITH SYNONYMS=('quant_investment_strategy','factor_portfolio_strategy','value_strategy','growth_strategy','strategy_type') COMMENT='Investment strategy: Value, Growth, ESG, Core, Multi-Asset, Income',
		
		-- Security dimensions  
		SECURITIES.TICKER AS Ticker WITH SYNONYMS=('quant_ticker','factor_symbol','quantitative_ticker_symbol') COMMENT='Trading ticker symbol',
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('factor_company','quant_name','quantitative_security_name') COMMENT='Company name',
		SECURITIES.ASSETCLASS AS AssetClass WITH SYNONYMS=('quant_type','factor_security_type','quantitative_asset_class') COMMENT='Asset class',
		
		-- Issuer dimensions
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('factor_issuer','quant_legal_name','quantitative_entity_name') COMMENT='Legal entity name',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('factor_sector','quant_industry_sector','quantitative_gics') COMMENT='GICS sector',
		ISSUERS.COUNTRYOFINCORPORATION AS CountryOfIncorporation WITH SYNONYMS=('factor_domicile','quant_country','quantitative_headquarters') COMMENT='Country of incorporation',
		
		-- Factor dimensions
		FACTOR_EXPOSURES.FactorName AS FACTOR_NAME WITH SYNONYMS=('factor','factor_type','loading_type') COMMENT='Factor name (Value, Growth, Quality, etc.)',
		FACTOR_EXPOSURES.ExposureDate AS EXPOSURE_DATE WITH SYNONYMS=('factor_date','loading_date','exposure_date') COMMENT='Factor exposure date',
		
		-- Fundamental dimensions
		FUNDAMENTALS.ReportingDate AS REPORTING_DATE WITH SYNONYMS=('quant_report_date','factor_earnings_date','quantitative_fiscal_date') COMMENT='Financial reporting date',
		FUNDAMENTALS.FiscalQuarter AS FISCAL_QUARTER WITH SYNONYMS=('quant_quarter','factor_period','quantitative_fiscal_period') COMMENT='Fiscal quarter',
		FUNDAMENTALS.MetricName AS METRIC_NAME WITH SYNONYMS=('quant_metric','factor_measure','quantitative_financial_metric') COMMENT='Financial metric name',
		
		-- Time dimensions
		HOLDINGS.HoldingDate AS HOLDINGDATE WITH SYNONYMS=('quant_position_date','factor_as_of_date','quantitative_holding_date') COMMENT='Holdings as-of date',
		MARKET_DATA.PriceDate AS PRICEDATE WITH SYNONYMS=('quant_market_date','factor_price_date','quantitative_trading_date') COMMENT='Market data date'
	)
	METRICS (
		-- Portfolio metrics
		HOLDINGS.TOTAL_MARKET_VALUE AS SUM(MarketValue_Base) WITH SYNONYMS=('quant_exposure','factor_total_exposure','quantitative_market_value','quant_position_value') COMMENT='Total market value in base currency',
		HOLDINGS.PORTFOLIO_WEIGHT AS SUM(PortfolioWeight) WITH SYNONYMS=('quant_weight','factor_allocation','quantitative_portfolio_weight') COMMENT='Portfolio weight as decimal',
		HOLDINGS.PORTFOLIO_WEIGHT_PCT AS SUM(PortfolioWeight) * 100 WITH SYNONYMS=('quant_weight_percent','factor_allocation_percent','quantitative_percentage_weight') COMMENT='Portfolio weight as percentage',
		
		-- Factor metrics (enhanced for trend analysis)
		FACTOR_EXPOSURES.FACTOR_EXPOSURE AS SUM(EXPOSURE_VALUE) WITH SYNONYMS=('factor_loading','loading','factor_score','exposure') COMMENT='Factor exposure value',
		FACTOR_EXPOSURES.FACTOR_R_SQUARED AS AVG(R_SQUARED) WITH SYNONYMS=('r_squared','model_fit','factor_rsq') COMMENT='Factor model R-squared',
		FACTOR_EXPOSURES.MOMENTUM_SCORE AS AVG(CASE WHEN FACTOR_NAME = 'Momentum' THEN EXPOSURE_VALUE ELSE NULL END) WITH SYNONYMS=('momentum','momentum_factor','momentum_loading') COMMENT='Momentum factor exposure',
		FACTOR_EXPOSURES.QUALITY_SCORE AS AVG(CASE WHEN FACTOR_NAME = 'Quality' THEN EXPOSURE_VALUE ELSE NULL END) WITH SYNONYMS=('quality','quality_factor','quality_loading') COMMENT='Quality factor exposure',
		FACTOR_EXPOSURES.VALUE_SCORE AS AVG(CASE WHEN FACTOR_NAME = 'Value' THEN EXPOSURE_VALUE ELSE NULL END) WITH SYNONYMS=('value','value_factor','value_loading') COMMENT='Value factor exposure',
		FACTOR_EXPOSURES.GROWTH_SCORE AS AVG(CASE WHEN FACTOR_NAME = 'Growth' THEN EXPOSURE_VALUE ELSE NULL END) WITH SYNONYMS=('growth','growth_factor','growth_loading') COMMENT='Growth factor exposure',
		
		-- Performance metrics
		MARKET_DATA.TOTAL_RETURN AS SUM(TotalReturnFactor_Daily) WITH SYNONYMS=('quant_return','factor_performance','quantitative_total_return') COMMENT='Total return factor',
		MARKET_DATA.PRICE_RETURN AS AVG(Price_Close) WITH SYNONYMS=('quant_price','factor_closing_price','quantitative_market_price') COMMENT='Closing price',
		MARKET_DATA.VOLUME_TRADED AS SUM(Volume) WITH SYNONYMS=('quant_volume','factor_trading_volume','quantitative_daily_volume') COMMENT='Trading volume',
		
		-- Fundamental metrics
		FUNDAMENTALS.FUNDAMENTAL_VALUE AS SUM(METRIC_VALUE) WITH SYNONYMS=('quant_fundamental','factor_financial_value','quantitative_metric_value') COMMENT='Fundamental metric value',
		ESTIMATES.ESTIMATE_VALUE AS AVG(ESTIMATE_VALUE) WITH SYNONYMS=('quant_estimate','factor_forecast','quantitative_consensus') COMMENT='Consensus estimate value',
		
		-- Benchmark metrics
		BENCHMARK_HOLDINGS.BenchmarkWeight AS SUM(BENCHMARK_WEIGHT) WITH SYNONYMS=('quant_benchmark_allocation','factor_index_weight','quantitative_benchmark_percentage') COMMENT='Benchmark constituent weight'
	)
	COMMENT='Quantitative analysis semantic view with factor exposures, performance attribution, and systematic analysis capabilities';
    """).collect()
    
    print("   ✅ Created semantic view: SAM_QUANT_VIEW")

def create_search_services(session: Session, scenarios: List[str]):
    """Create Cortex Search services for required document types."""
    
    # Determine required document types from scenarios
    required_doc_types = set()
    for scenario in scenarios:
        if scenario in config.SCENARIO_DATA_REQUIREMENTS:
            required_doc_types.update(config.SCENARIO_DATA_REQUIREMENTS[scenario])
    
    print(f"   📑 Document types: {', '.join(required_doc_types)}")
    
    # Create search service for each required document type
    for doc_type in required_doc_types:
        if doc_type in config.DOCUMENT_TYPES:
            corpus_table = f"{config.DATABASE_NAME}.CURATED.{config.DOCUMENT_TYPES[doc_type]['corpus_name']}"
            service_name = config.DOCUMENT_TYPES[doc_type]['search_service']
            
            try:
                # Use dedicated Cortex Search warehouse
                from config import CORTEX_SEARCH_WAREHOUSE, CORTEX_SEARCH_TARGET_LAG
                search_warehouse = CORTEX_SEARCH_WAREHOUSE
                
                # Create enhanced Cortex Search service with SecurityID and IssuerID attributes
                # Using configurable TARGET_LAG for demo environments to see changes quickly
                session.sql(f"""
                    CREATE OR REPLACE CORTEX SEARCH SERVICE {config.DATABASE_NAME}.AI.{service_name}
                        ON DOCUMENT_TEXT
                        ATTRIBUTES DOCUMENT_TITLE, SecurityID, IssuerID, DOCUMENT_TYPE, PUBLISH_DATE, LANGUAGE
                        WAREHOUSE = {search_warehouse}
                        TARGET_LAG = '{CORTEX_SEARCH_TARGET_LAG}'
                        AS 
                        SELECT 
                            DOCUMENT_ID,
                            DOCUMENT_TITLE,
                            DOCUMENT_TEXT,
                            SecurityID,
                            IssuerID,
                            DOCUMENT_TYPE,
                            PUBLISH_DATE,
                            LANGUAGE
                        FROM {corpus_table}
                """).collect()
                
                print(f"   ✅ Created search service: {service_name}")
                
            except Exception as e:
                print(f"❌ CRITICAL FAILURE: Failed to create search service {service_name}: {e}")
                print(f"   This search service is required for scenarios using {doc_type}")
                raise Exception(f"Failed to create required search service {service_name}: {e}")

def validate_components(session: Session, semantic_built: bool, search_built: bool):
    """Validate that AI components are working correctly."""
    
    if semantic_built:
        print("🔍 Testing semantic view...")
        try:
            # Test semantic view using proper SEMANTIC_VIEW() function with correct metric names
            test_query = f"""
                SELECT * FROM SEMANTIC_VIEW(
                    {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW
                    METRICS TOTAL_MARKET_VALUE
                    DIMENSIONS PORTFOLIONAME
                )
                LIMIT 5
            """
            result = session.sql(test_query).collect()
            print(f"✅ Semantic view query test passed: {len(result)} results")
            
            # Test DESCRIBE SEMANTIC VIEW
            describe_result = session.sql(f"DESCRIBE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW").collect()
            print(f"✅ Semantic view structure validated: {len(describe_result)} components")
            
            # Test with multiple metrics and dimensions
            advanced_test = f"""
                SELECT * FROM SEMANTIC_VIEW(
                    {config.DATABASE_NAME}.AI.SAM_ANALYST_VIEW
                    METRICS TOTAL_MARKET_VALUE, HOLDING_COUNT
                    DIMENSIONS DESCRIPTION, GICS_SECTOR
                )
                LIMIT 10
            """
            advanced_result = session.sql(advanced_test).collect()
            print(f"✅ Advanced semantic view test passed: {len(advanced_result)} records")
            
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Semantic view validation failed: {e}")
            print("   The main semantic view is essential for all agents")
            raise Exception(f"Main semantic view validation failed: {e}")
    
    if search_built:
        print("🔍 Testing search services...")
        try:
            # Get list of search services using correct SHOW command
            ai_objects = session.sql(f'SHOW CORTEX SEARCH SERVICES IN {config.DATABASE_NAME}.AI').collect()
            
            print(f"Found {len(ai_objects)} search services to test")
            
            # Test each search service using your example syntax (without schema prefix in OVER clause)
            for service in ai_objects:
                service_name = service['name']
                try:
                    test_result = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                            '{config.DATABASE_NAME}.AI.{service_name}',
                            '{{"query": "technology investment", "limit": 2}}'
                        ) 
                    """).collect()
                    print(f"✅ Search service test passed: {service_name}")
                except Exception as e:
                    print(f"❌ CRITICAL FAILURE: Search service test failed for {service_name}: {e}")
                    print(f"   This search service is required for document search functionality")
                    raise Exception(f"Search service validation failed for {service_name}: {e}")
                    
        except Exception as e:
            print(f"❌ CRITICAL FAILURE: Search services validation failed: {e}")
            print("   Search services are required for document-based scenarios")
            raise Exception(f"Search services validation failed: {e}")
    
    print("✅ AI component validation complete")

def create_implementation_semantic_view(session: Session):
    """Create semantic view for portfolio implementation with trading, risk, and execution data."""
    
    # Check if implementation tables exist
    required_tables = [
        'FACT_TRANSACTION_COSTS',
        'FACT_PORTFOLIO_LIQUIDITY', 
        'FACT_RISK_LIMITS',
        'FACT_TRADING_CALENDAR',
        'DIM_CLIENT_MANDATES',
        'FACT_TAX_IMPLICATIONS'
    ]
    
    for table in required_tables:
        try:
            session.sql(f"SELECT 1 FROM {config.DATABASE_NAME}.CURATED.{table} LIMIT 1").collect()
        except:
            print(f"⚠️  Implementation table {table} not found, skipping implementation view creation")
            return
    
    # Create the implementation-focused semantic view
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_IMPLEMENTATION_VIEW
	TABLES (
		HOLDINGS AS {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HOLDINGDATE, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('positions','investments','allocations','holdings') 
			COMMENT='Current portfolio holdings for implementation planning',
		PORTFOLIOS AS {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('funds','strategies','mandates','portfolios') 
			COMMENT='Portfolio information',
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','instruments','securities') 
			COMMENT='Security reference data',
		TRANSACTION_COSTS AS {config.DATABASE_NAME}.CURATED.FACT_TRANSACTION_COSTS
			PRIMARY KEY (SECURITYID, COST_DATE)
			WITH SYNONYMS=('trading_costs','execution_costs','cost_data','transaction_costs')
			COMMENT='Transaction costs and market microstructure data',
		PORTFOLIO_LIQUIDITY AS {config.DATABASE_NAME}.CURATED.FACT_PORTFOLIO_LIQUIDITY
			PRIMARY KEY (PORTFOLIOID, LIQUIDITY_DATE)
			WITH SYNONYMS=('liquidity_info','liquidity','cash_position','liquidity_data')
			COMMENT='Portfolio cash and liquidity information',
		RISK_LIMITS AS {config.DATABASE_NAME}.CURATED.FACT_RISK_LIMITS
			PRIMARY KEY (PORTFOLIOID, LIMITS_DATE)
			WITH SYNONYMS=('risk_budget','limits','constraints','risk_limits')
			COMMENT='Risk limits and budget utilization',
		TRADING_CALENDAR AS {config.DATABASE_NAME}.CURATED.FACT_TRADING_CALENDAR
			PRIMARY KEY (SECURITYID, EVENT_DATE)
			WITH SYNONYMS=('calendar','events','blackouts','earnings_dates','trading_calendar')
			COMMENT='Trading calendar with blackout periods and events',
		CLIENT_MANDATES AS {config.DATABASE_NAME}.CURATED.DIM_CLIENT_MANDATES
			PRIMARY KEY (PORTFOLIOID)
			WITH SYNONYMS=('client_constraints','approvals','client_rules','client_mandates')
			COMMENT='Client mandate requirements and approval thresholds',
		TAX_IMPLICATIONS AS {config.DATABASE_NAME}.CURATED.FACT_TAX_IMPLICATIONS
			PRIMARY KEY (PORTFOLIOID, SECURITYID, TAX_DATE)
			WITH SYNONYMS=('tax_data','tax_records','gains_losses','tax_implications')
			COMMENT='Tax implications and cost basis data'
	)
	RELATIONSHIPS (
		HOLDINGS_TO_PORTFOLIOS AS HOLDINGS(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		HOLDINGS_TO_SECURITIES AS HOLDINGS(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		TRANSACTION_COSTS_TO_SECURITIES AS TRANSACTION_COSTS(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		PORTFOLIO_LIQUIDITY_TO_PORTFOLIOS AS PORTFOLIO_LIQUIDITY(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		RISK_LIMITS_TO_PORTFOLIOS AS RISK_LIMITS(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		TRADING_CALENDAR_TO_SECURITIES AS TRADING_CALENDAR(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		CLIENT_MANDATES_TO_PORTFOLIOS AS CLIENT_MANDATES(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		TAX_IMPLICATIONS_TO_PORTFOLIOS AS TAX_IMPLICATIONS(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID),
		TAX_IMPLICATIONS_TO_SECURITIES AS TAX_IMPLICATIONS(SECURITYID) REFERENCES SECURITIES(SECURITYID)
	)
	DIMENSIONS (
		-- Portfolio dimensions
		PORTFOLIOS.PORTFOLIONAME AS PORTFOLIONAME WITH SYNONYMS=('fund_name','strategy_name','portfolio_name') COMMENT='Portfolio name',
		PORTFOLIOS.STRATEGY AS STRATEGY WITH SYNONYMS=('investment_strategy','portfolio_strategy') COMMENT='Investment strategy',
		
		-- Security dimensions  
		SECURITIES.DESCRIPTION AS DESCRIPTION WITH SYNONYMS=('security_name','security_description','name') COMMENT='Security description',
		SECURITIES.TICKER AS TICKER WITH SYNONYMS=('ticker_symbol','symbol','primary_ticker') COMMENT='Trading ticker symbol',
		
		-- Trading calendar dimensions
		TRADING_CALENDAR.EventType AS EVENT_TYPE WITH SYNONYMS=('event','calendar_event','trading_event') COMMENT='Trading calendar event type',
		TRADING_CALENDAR.IsBlackoutPeriod AS IS_BLACKOUT_PERIOD WITH SYNONYMS=('blackout','restricted','no_trading') COMMENT='Blackout period indicator',
		
		-- Tax dimensions
		TAX_IMPLICATIONS.TaxTreatment AS TAX_TREATMENT WITH SYNONYMS=('tax_type','treatment','tax_treatment') COMMENT='Tax treatment classification',
		TAX_IMPLICATIONS.TaxLossHarvestOpportunity AS TAX_LOSS_HARVEST_OPPORTUNITY WITH SYNONYMS=('tax_loss','harvest_opportunity','harvest_flag') COMMENT='Tax loss harvesting opportunity'
	)
	METRICS (
		-- Position metrics
		HOLDINGS.TOTAL_MARKET_VALUE AS SUM(MarketValue_Base) WITH SYNONYMS=('market_value','position_value','exposure') COMMENT='Total market value of positions',
		HOLDINGS.PORTFOLIO_WEIGHT_PCT AS SUM(PortfolioWeight) * 100 WITH SYNONYMS=('weight_percent','allocation_percent','percentage_weight') COMMENT='Portfolio weight as percentage',
		
		-- Transaction cost metrics
		TRANSACTION_COSTS.AVG_BID_ASK_SPREAD AS AVG(BID_ASK_SPREAD_BPS) WITH SYNONYMS=('bid_ask_spread','spread','trading_spread') COMMENT='Average bid-ask spread in basis points',
		TRANSACTION_COSTS.AVG_MARKET_IMPACT AS AVG(MARKET_IMPACT_BPS_PER_1M) WITH SYNONYMS=('market_impact','trading_impact','execution_cost') COMMENT='Average market impact per $1M traded',
		TRANSACTION_COSTS.AVG_DAILY_VOLUME AS AVG(AVG_DAILY_VOLUME_M) WITH SYNONYMS=('daily_volume','trading_volume','volume') COMMENT='Average daily trading volume in millions',
		
		-- Liquidity metrics
		PORTFOLIO_LIQUIDITY.TOTAL_CASH_POSITION AS SUM(CASH_POSITION_USD) WITH SYNONYMS=('cash_available','available_cash','total_cash') COMMENT='Total available cash position',
		PORTFOLIO_LIQUIDITY.NET_CASH_FLOW AS SUM(NET_CASHFLOW_30D_USD) WITH SYNONYMS=('cash_flow','net_flow','expected_flow') COMMENT='Expected net cash flow over 30 days',
		PORTFOLIO_LIQUIDITY.AVG_LIQUIDITY_SCORE AS AVG(PORTFOLIO_LIQUIDITY_SCORE) WITH SYNONYMS=('liquidity_score','liquidity_rating','portfolio_liquidity') COMMENT='Portfolio liquidity score (1-10)',
		
		-- Risk metrics
		RISK_LIMITS.TRACKING_ERROR_UTILIZATION AS AVG(CURRENT_TRACKING_ERROR_PCT / TRACKING_ERROR_LIMIT_PCT) * 100 WITH SYNONYMS=('risk_utilization','tracking_error_usage','risk_budget_used') COMMENT='Tracking error budget utilization percentage',
		RISK_LIMITS.MAX_POSITION_LIMIT AS MAX(MAX_SINGLE_POSITION_PCT) * 100 WITH SYNONYMS=('concentration_limit','position_limit','max_weight_limit') COMMENT='Maximum single position limit as percentage',
		RISK_LIMITS.CURRENT_TRACKING_ERROR AS AVG(CURRENT_TRACKING_ERROR_PCT) WITH SYNONYMS=('current_risk','tracking_error','portfolio_risk') COMMENT='Current tracking error percentage',
		
		-- Tax metrics
		TAX_IMPLICATIONS.TOTAL_UNREALIZED_GAINS AS SUM(UNREALIZED_GAIN_LOSS_USD) WITH SYNONYMS=('unrealized_gains','capital_gains','unrealized_pnl') COMMENT='Total unrealized gains/losses',
		TAX_IMPLICATIONS.TOTAL_COST_BASIS AS SUM(COST_BASIS_USD) WITH SYNONYMS=('cost_basis','original_cost','tax_basis') COMMENT='Total cost basis for tax calculations',
		TAX_IMPLICATIONS.TAX_LOSS_HARVEST_VALUE AS SUM(CASE WHEN TAX_LOSS_HARVEST_OPPORTUNITY THEN ABS(UNREALIZED_GAIN_LOSS_USD) ELSE 0 END) WITH SYNONYMS=('harvest_value','tax_loss_value','loss_harvest_amount') COMMENT='Total value available for tax loss harvesting',
		
		-- Calendar metrics  
		TRADING_CALENDAR.BLACKOUT_DAYS AS COUNT(CASE WHEN IS_BLACKOUT_PERIOD THEN 1 END) WITH SYNONYMS=('blackout_count','restricted_days','no_trading_days') COMMENT='Count of blackout period days',
		TRADING_CALENDAR.AVG_VIX_FORECAST AS AVG(EXPECTED_VIX_LEVEL) WITH SYNONYMS=('volatility_forecast','vix_forecast','market_volatility') COMMENT='Average expected VIX volatility level'
	)
	COMMENT='Implementation semantic view with trading costs, liquidity, risk limits, and execution planning data';
    """).collect()
    
    print("✅ Created semantic view: SAM_IMPLEMENTATION_VIEW")

def create_sec_filings_semantic_view(session: Session):
    """Create semantic view for SEC filings financial analysis."""
    
    # Check if SEC filings table exists
    try:
        session.sql(f"SELECT COUNT(*) FROM {config.DATABASE_NAME}.CURATED.FACT_SEC_FILINGS LIMIT 1").collect()
    except Exception as e:
        print(f"⚠️  FACT_SEC_FILINGS table not found: {e}")
        print("   SEC filings semantic view creation skipped")
        return
    
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.SAM_SEC_FILINGS_VIEW
	TABLES (
		SEC_FILINGS AS {config.DATABASE_NAME}.CURATED.FACT_SEC_FILINGS
			PRIMARY KEY (FILINGID) 
			WITH SYNONYMS=('sec_filings','filings','financial_statements','sec_data') 
			COMMENT='SEC filing financial data with comprehensive metrics across Income Statement, Balance Sheet, and Cash Flow',
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','bonds','instruments','securities') 
			COMMENT='Master security reference data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate hierarchy data'
	)
	RELATIONSHIPS (
		SEC_FILINGS_TO_SECURITIES AS SEC_FILINGS(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		SECURITIES_TO_ISSUERS AS SECURITIES(ISSUERID) REFERENCES ISSUERS(ISSUERID)
	)
	DIMENSIONS (
		-- Company dimensions
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('company','issuer_name','legal_name') COMMENT='Company legal name',
		SECURITIES.TICKER AS Ticker WITH SYNONYMS=('symbol','ticker_symbol') COMMENT='Stock ticker symbol',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('industry','sector','gics_sector') COMMENT='Industry sector',
		
		-- SEC Filing specific dimensions
		SEC_FILINGS.CIK AS CIK WITH SYNONYMS=('cik','sec_cik','company_cik') COMMENT='SEC Central Index Key',
		SEC_FILINGS.FORMTYPE AS FormType WITH SYNONYMS=('form_type','sec_form','filing_form') COMMENT='SEC form type (10-K, 10-Q, etc.)',
		SEC_FILINGS.TAG AS TAG WITH SYNONYMS=('tag','measure','metric_name','sec_measure') COMMENT='SEC financial measure tag name',
		SEC_FILINGS.MEASUREDESCRIPTION AS MeasureDescription WITH SYNONYMS=('measure_description','description','label') COMMENT='Human-readable description of the measure',
		SEC_FILINGS.UNITOFMEASURE AS UnitOfMeasure WITH SYNONYMS=('unit','measure_unit','unit_of_measure') COMMENT='Unit of measurement',
		SEC_FILINGS.STATEMENT AS Statement WITH SYNONYMS=('statement','financial_statement','fs_type') COMMENT='Financial statement type (Income Statement, Balance Sheet, Cash Flow)',
		
		-- Time dimensions
		SEC_FILINGS.REPORTINGDATE AS ReportingDate WITH SYNONYMS=('report_date','period_date','date') COMMENT='Standardized financial reporting date',
		SEC_FILINGS.FISCALPERIOD AS FiscalPeriod WITH SYNONYMS=('period','quarter','fiscal_period') COMMENT='Fiscal reporting period',
		SEC_FILINGS.FISCALYEAR AS FiscalYear WITH SYNONYMS=('year','fiscal_year') COMMENT='Fiscal year',
		SEC_FILINGS.PERIODSTARTDATE AS PeriodStartDate WITH SYNONYMS=('start_date','period_start') COMMENT='Financial period start date',
		SEC_FILINGS.PERIODENDDATE AS PeriodEndDate WITH SYNONYMS=('end_date','period_end') COMMENT='Financial period end date'
	)
	METRICS (
		-- SEC Filing data metrics
		SEC_FILINGS.MEASURE_VALUE AS SUM(MeasureValue) WITH SYNONYMS=('value','sec_value','filing_value','amount') COMMENT='SEC filing measure value',
		SEC_FILINGS.FILING_COUNT AS COUNT(FilingID) WITH SYNONYMS=('filing_count','number_of_filings','sec_filing_count','count') COMMENT='Count of SEC filings',
		
		-- Income Statement metrics
		SEC_FILINGS.TOTAL_REVENUE AS SUM(CASE WHEN TAG IN ('Revenues', 'RevenueFromContractWithCustomerExcludingAssessedTax') THEN MeasureValue END) WITH SYNONYMS=('revenue','sales','total_revenue','top_line') COMMENT='Total company revenue from SEC filings',
		SEC_FILINGS.NET_INCOME AS SUM(CASE WHEN TAG = 'NetIncomeLoss' THEN MeasureValue END) WITH SYNONYMS=('profit','net_income','earnings','bottom_line') COMMENT='Net income from SEC filings',
		SEC_FILINGS.GROSS_PROFIT AS SUM(CASE WHEN TAG = 'GrossProfit' THEN MeasureValue END) WITH SYNONYMS=('gross_profit','gross_income') COMMENT='Gross profit from SEC filings',
		SEC_FILINGS.OPERATING_INCOME AS SUM(CASE WHEN TAG = 'OperatingIncomeLoss' THEN MeasureValue END) WITH SYNONYMS=('operating_income','operating_profit') COMMENT='Operating income from SEC filings',
		SEC_FILINGS.INTEREST_EXPENSE AS SUM(CASE WHEN TAG = 'InterestExpense' THEN MeasureValue END) WITH SYNONYMS=('interest_expense','interest_cost') COMMENT='Interest expense from SEC filings',
		SEC_FILINGS.OPERATING_EXPENSES AS SUM(CASE WHEN TAG = 'OperatingExpenses' THEN MeasureValue END) WITH SYNONYMS=('operating_expenses','opex') COMMENT='Total operating expenses from SEC filings',
		SEC_FILINGS.EPS_BASIC AS AVG(CASE WHEN TAG = 'EarningsPerShareBasic' THEN MeasureValue END) WITH SYNONYMS=('eps','earnings_per_share','eps_basic') COMMENT='Basic earnings per share from SEC filings',
		SEC_FILINGS.EPS_DILUTED AS AVG(CASE WHEN TAG = 'EarningsPerShareDiluted' THEN MeasureValue END) WITH SYNONYMS=('eps_diluted','diluted_eps') COMMENT='Diluted earnings per share from SEC filings',
		
		-- Balance Sheet metrics
		SEC_FILINGS.TOTAL_ASSETS AS SUM(CASE WHEN TAG = 'Assets' THEN MeasureValue END) WITH SYNONYMS=('assets','total_assets') COMMENT='Total assets from SEC filings',
		SEC_FILINGS.CURRENT_ASSETS AS SUM(CASE WHEN TAG = 'AssetsCurrent' THEN MeasureValue END) WITH SYNONYMS=('current_assets','liquid_assets') COMMENT='Current assets from SEC filings',
		SEC_FILINGS.TOTAL_EQUITY AS SUM(CASE WHEN TAG = 'StockholdersEquity' THEN MeasureValue END) WITH SYNONYMS=('equity','shareholders_equity','total_equity') COMMENT='Total equity from SEC filings',
		SEC_FILINGS.TOTAL_LIABILITIES AS SUM(CASE WHEN TAG = 'Liabilities' THEN MeasureValue END) WITH SYNONYMS=('liabilities','total_debt','debt') COMMENT='Total liabilities from SEC filings',
		SEC_FILINGS.CURRENT_LIABILITIES AS SUM(CASE WHEN TAG = 'LiabilitiesCurrent' THEN MeasureValue END) WITH SYNONYMS=('current_liabilities','short_term_debt') COMMENT='Current liabilities from SEC filings',
		SEC_FILINGS.CASH_AND_EQUIVALENTS AS SUM(CASE WHEN TAG = 'CashAndCashEquivalentsAtCarryingValue' THEN MeasureValue END) WITH SYNONYMS=('cash','cash_equivalents') COMMENT='Cash and equivalents from SEC filings',
		SEC_FILINGS.GOODWILL AS SUM(CASE WHEN TAG = 'Goodwill' THEN MeasureValue END) WITH SYNONYMS=('goodwill','intangible_assets') COMMENT='Goodwill from SEC filings',
		SEC_FILINGS.RETAINED_EARNINGS AS SUM(CASE WHEN TAG = 'RetainedEarningsAccumulatedDeficit' THEN MeasureValue END) WITH SYNONYMS=('retained_earnings','accumulated_deficit') COMMENT='Retained earnings from SEC filings',
		
		-- Cash Flow metrics
		SEC_FILINGS.OPERATING_CASH_FLOW AS SUM(CASE WHEN TAG = 'NetCashProvidedByUsedInOperatingActivities' THEN MeasureValue END) WITH SYNONYMS=('operating_cash_flow','ocf','cash_from_operations') COMMENT='Operating cash flow from SEC filings',
		SEC_FILINGS.INVESTING_CASH_FLOW AS SUM(CASE WHEN TAG = 'NetCashProvidedByUsedInInvestingActivities' THEN MeasureValue END) WITH SYNONYMS=('investing_cash_flow','icf','capex_flow') COMMENT='Investing cash flow from SEC filings',
		SEC_FILINGS.FINANCING_CASH_FLOW AS SUM(CASE WHEN TAG = 'NetCashProvidedByUsedInFinancingActivities' THEN MeasureValue END) WITH SYNONYMS=('financing_cash_flow','fcf','debt_equity_flow') COMMENT='Financing cash flow from SEC filings',
		SEC_FILINGS.DEPRECIATION AS SUM(CASE WHEN TAG = 'DepreciationDepletionAndAmortization' THEN MeasureValue END) WITH SYNONYMS=('depreciation','amortization','d_and_a') COMMENT='Depreciation and amortization from SEC filings',
		SEC_FILINGS.STOCK_BASED_COMPENSATION AS SUM(CASE WHEN TAG = 'ShareBasedCompensation' THEN MeasureValue END) WITH SYNONYMS=('stock_compensation','share_based_comp') COMMENT='Stock-based compensation from SEC filings'
	)
	COMMENT='SEC filing data semantic view for financial analysis using authentic EDGAR data';
    """).collect()
    
    print("✅ Created semantic view: SAM_SEC_FILINGS_VIEW")