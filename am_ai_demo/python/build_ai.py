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
    
    if build_semantic:
        print("🧠 Building semantic views...")
        create_semantic_views(session)
    
    if build_search:
        print("🔍 Building Cortex Search services...")
        create_search_services(session, scenarios)
    
    # Validate components
    print("✅ Validating AI components...")
    validate_components(session, build_semantic, build_search)
    
    print("✅ AI components build complete")

def create_semantic_views(session: Session):
    """Create the master semantic view for Cortex Analyst using correct Snowflake syntax."""
    
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
		PORTFOLIOS.STRATEGY AS Strategy WITH SYNONYMS=('investment_strategy','portfolio_strategy') COMMENT='Investment strategy type',
		
		-- Security dimensions  
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('company','security_name','description') COMMENT='Security description or company name',
		SECURITIES.PRIMARYTICKER AS Ticker WITH SYNONYMS=('ticker_symbol','symbol','primary_ticker') COMMENT='Primary trading symbol',
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
        
        print("✅ Created semantic view: SAM_ANALYST_VIEW")
        
    except Exception as e:
        print(f"❌ Failed to create semantic view: {e}")
        raise
    
    # Create additional semantic view for research with fundamentals data
    try:
        print("📊 Creating research semantic view with fundamentals...")
        create_research_semantic_view(session)
    except Exception as e:
        print(f"⚠️  Warning: Could not create research semantic view: {e}")
        # Don't raise - this is optional enhancement
    
    # Create implementation semantic view for portfolio management
    try:
        print("🎯 Creating implementation semantic view for portfolio management...")
        create_implementation_semantic_view(session)
    except Exception as e:
        print(f"⚠️  Warning: Could not create implementation semantic view: {e}")
        # Don't raise - this is optional enhancement

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
		SECURITIES.PRIMARYTICKER AS Ticker WITH SYNONYMS=('ticker','symbol','ticker_symbol') COMMENT='Trading ticker symbol',
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
    
    print("✅ Created semantic view: SAM_RESEARCH_VIEW")

def create_search_services(session: Session, scenarios: List[str]):
    """Create Cortex Search services for required document types."""
    
    # Determine required document types from scenarios
    required_doc_types = set()
    for scenario in scenarios:
        if scenario in config.SCENARIO_DATA_REQUIREMENTS:
            required_doc_types.update(config.SCENARIO_DATA_REQUIREMENTS[scenario])
    
    print(f"Creating search services for: {list(required_doc_types)}")
    
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
                
                print(f"✅ Created search service: {service_name}")
                
            except Exception as e:
                print(f"❌ Failed to create search service {service_name}: {e}")
                continue

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
            print(f"❌ Semantic view validation failed: {e}")
            # Don't raise - continue with search services
    
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
                    print(f"❌ Search service test failed for {service_name}: {e}")
                    
        except Exception as e:
            print(f"❌ Search services validation failed: {e}")
    
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
			WITH SYNONYMS=('trading_costs','execution_costs','market_impact','transaction_costs')
			COMMENT='Transaction costs and market microstructure data',
		PORTFOLIO_LIQUIDITY AS {config.DATABASE_NAME}.CURATED.FACT_PORTFOLIO_LIQUIDITY
			PRIMARY KEY (PORTFOLIOID, LIQUIDITY_DATE)
			WITH SYNONYMS=('cash_flow','liquidity','cash_position','portfolio_liquidity')
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
			WITH SYNONYMS=('mandates','approvals','client_rules','client_mandates')
			COMMENT='Client mandate requirements and approval thresholds',
		TAX_IMPLICATIONS AS {config.DATABASE_NAME}.CURATED.FACT_TAX_IMPLICATIONS
			PRIMARY KEY (PORTFOLIOID, SECURITYID, TAX_DATE)
			WITH SYNONYMS=('tax_data','cost_basis','gains_losses','tax_implications')
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
		TAX_IMPLICATIONS_TO_HOLDINGS AS TAX_IMPLICATIONS(PORTFOLIOID, SECURITYID) REFERENCES HOLDINGS(PORTFOLIOID, SECURITYID)
	)
	DIMENSIONS (
		-- Portfolio dimensions
		PORTFOLIOS.PortfolioName AS PORTFOLIONAME WITH SYNONYMS=('fund_name','strategy_name','portfolio_name') COMMENT='Portfolio name',
		PORTFOLIOS.Strategy AS STRATEGY WITH SYNONYMS=('investment_strategy','portfolio_strategy') COMMENT='Investment strategy',
		
		-- Security dimensions  
		SECURITIES.Description AS DESCRIPTION WITH SYNONYMS=('security_name','security_description','name') COMMENT='Security description',
		SECURITIES.Ticker AS PRIMARYTICKER WITH SYNONYMS=('ticker_symbol','symbol','primary_ticker') COMMENT='Trading ticker symbol',
		
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