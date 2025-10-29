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

def build_all(session: Session, scenarios: List[str], build_semantic: bool = True, build_search: bool = True, build_agents: bool = True):
    """
    Build AI components for the specified scenarios.
    
    Args:
        session: Active Snowpark session
        scenarios: List of scenario names
        build_semantic: Whether to build semantic views
        build_search: Whether to build search services
        build_agents: Whether to create Snowflake Intelligence agents
    """
    # print(" Starting AI components build...")
    # print(f"   Scenarios: {', '.join(scenarios)}")
    
    if build_semantic:
        # print("🧠 Building semantic views...")
        try:
            create_semantic_views(session, scenarios)
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Semantic view creation failed: {e}")
            # print("🛑 STOPPING BUILD - Cannot continue without semantic views")
            raise
    
    if build_search:
        # print(" Building Cortex Search services...")
        try:
            create_search_services(session, scenarios)
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Search service creation failed: {e}")
            # print("🛑 STOPPING BUILD - Cannot continue without required search services")
            raise
    
    # Create custom tools (PDF generation)
    # print("📄 Creating custom tools...")
    try:
        create_pdf_report_stage(session)
        create_simple_pdf_tool(session)
    except Exception as e:
        print(f"ERROR: Warning: Custom tool creation failed: {e}")
        # print("   Continuing build - custom tools are optional for basic functionality")
    
    # Create Snowflake Intelligence agents
    if build_agents:
        # print("🤖 Creating Snowflake Intelligence agents...")
        try:
            import create_agents
            created, failed = create_agents.create_all_agents(session, scenarios)
            if failed > 0:
                print(f"   ⚠️  WARNING: {failed} agents failed to create")
        except Exception as e:
            print(f"ERROR: Warning: Agent creation failed: {e}")
            # print("   Continuing build - agents can be created manually if needed")
    
    # Validate components
    # print(" Validating AI components...")
    try:
        validate_components(session, build_semantic, build_search)
    except Exception as e:
        print(f"ERROR: CRITICAL FAILURE: AI component validation failed: {e}")
        # print("🛑 STOPPING BUILD - AI components not working properly")
        raise
    
    # print(" AI components build complete")

def create_semantic_views(session: Session, scenarios: List[str] = None):
    """Create semantic views required for the specified scenarios."""
    
    try:
        # Create proper semantic view with correct syntax patterns
        session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE['name']}.AI.SAM_ANALYST_VIEW
	TABLES (
		HOLDINGS AS {config.DATABASE['name']}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HOLDINGDATE, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('positions','investments','allocations','holdings') 
			COMMENT='Daily portfolio holdings and positions. Each portfolio holding has multiple rows. When no time period is provided always get the latest value by date.',
		PORTFOLIOS AS {config.DATABASE['name']}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('funds','strategies','mandates','portfolios') 
			COMMENT='Investment portfolios and fund information',
		SECURITIES AS {config.DATABASE['name']}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','bonds','instruments','securities') 
			COMMENT='Master security reference data',
		ISSUERS AS {config.DATABASE['name']}.CURATED.DIM_ISSUER
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
		ISSUERS.LegalName AS LEGALNAME WITH SYNONYMS=('issuer_name','legal_name','company_name') COMMENT='Legal issuer name',
		ISSUERS.Industry AS SIC_DESCRIPTION WITH SYNONYMS=('industry','sector','industry_type','sic_industry','business_type','industry_description','industry_classification') COMMENT='SIC industry classification with granular descriptions (e.g., Semiconductors and related devices, Computer programming services, Motor vehicles and car bodies). Use this for industry-level filtering and analysis.',
		ISSUERS.CountryOfIncorporation AS COUNTRYOFINCORPORATION WITH SYNONYMS=('domicile','country_of_risk','country') COMMENT='Country of incorporation using 2-letter ISO codes (e.g., TW for Taiwan, US for United States, GB for United Kingdom)',
		
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
		HOLDINGS.MAX_POSITION_WEIGHT AS MAX(PortfolioWeight) WITH SYNONYMS=('largest_position','max_weight','concentration') COMMENT='Largest single position weight',
		
		-- Mandate compliance metrics (for Scenario 3.2)
		HOLDINGS.AI_GROWTH_SCORE AS AVG(CASE 
			WHEN SECURITIES.Ticker IN ('NVDA', 'MSFT', 'GOOGL', 'META', 'AMZN', 'AAPL') THEN 
				CASE SECURITIES.Ticker
					WHEN 'NVDA' THEN 92
					WHEN 'MSFT' THEN 89
					WHEN 'GOOGL' THEN 85
					WHEN 'META' THEN 82
					WHEN 'AMZN' THEN 88
					WHEN 'AAPL' THEN 87
					ELSE 75
				END
			ELSE 75
		END) WITH SYNONYMS=('ai_score','innovation_score','ai_growth','ai_potential','technology_score') COMMENT='Proprietary AI Growth Score (0-100) measuring AI/ML innovation potential and market positioning. Higher scores indicate stronger AI capabilities, patent portfolios, and growth potential in artificial intelligence.'
	)
	COMMENT='Multi-asset semantic view for portfolio analytics with issuer hierarchy support and mandate compliance metrics'
	WITH EXTENSION (CA='{{"tables":[{{"name":"HOLDINGS","metrics":[{{"name":"AI_GROWTH_SCORE"}},{{"name":"HOLDING_COUNT"}},{{"name":"ISSUER_EXPOSURE"}},{{"name":"MAX_POSITION_WEIGHT"}},{{"name":"PORTFOLIO_WEIGHT"}},{{"name":"PORTFOLIO_WEIGHT_PCT"}},{{"name":"TOTAL_MARKET_VALUE"}}],"time_dimensions":[{{"name":"HoldingDate","expr":"HOLDINGDATE","data_type":"DATE","synonyms":["position_date","as_of_date","portfolio_date","valuation_date"],"description":"The date when portfolio holdings were valued and recorded. Use this for historical analysis and period comparisons."}},{{"name":"holding_month","expr":"DATE_TRUNC(\\'MONTH\\', HOLDINGDATE)","data_type":"DATE","synonyms":["month","monthly","month_end"],"description":"Monthly aggregation of holding dates for trend analysis and month-over-month comparisons."}},{{"name":"holding_quarter","expr":"DATE_TRUNC(\\'QUARTER\\', HOLDINGDATE)","data_type":"DATE","synonyms":["quarter","quarterly","quarter_end"],"description":"Quarterly aggregation for quarterly reporting and period-over-period analysis."}}]}},{{"name":"ISSUERS","dimensions":[{{"name":"COUNTRYOFINCORPORATION"}},{{"name":"SIC_DESCRIPTION"}},{{"name":"LEGALNAME"}}]}},{{"name":"PORTFOLIOS","dimensions":[{{"name":"PortfolioName"}},{{"name":"Strategy"}}]}},{{"name":"SECURITIES","dimensions":[{{"name":"AssetClass"}},{{"name":"Description"}},{{"name":"Ticker"}}]}}],"relationships":[{{"name":"HOLDINGS_TO_PORTFOLIOS"}},{{"name":"HOLDINGS_TO_SECURITIES"}},{{"name":"SECURITIES_TO_ISSUERS"}}],"verified_queries":[{{"name":"top_holdings_by_portfolio","question":"What are the top 10 holdings by market value in the SAM Technology & Infrastructure portfolio?","sql":"SELECT __SECURITIES.DESCRIPTION, __SECURITIES.TICKER, __HOLDINGS.MARKETVALUE_BASE, (__HOLDINGS.MARKETVALUE_BASE / SUM(__HOLDINGS.MARKETVALUE_BASE) OVER (PARTITION BY __HOLDINGS.PORTFOLIOID)) * 100 AS WEIGHT_PCT FROM __HOLDINGS JOIN __SECURITIES ON __HOLDINGS.SECURITYID = __SECURITIES.SECURITYID JOIN __PORTFOLIOS ON __HOLDINGS.PORTFOLIOID = __PORTFOLIOS.PORTFOLIOID WHERE __PORTFOLIOS.PORTFOLIONAME = \\'SAM Technology & Infrastructure\\' AND __HOLDINGS.HOLDINGDATE = (SELECT MAX(HOLDINGDATE) FROM __HOLDINGS) ORDER BY __HOLDINGS.MARKETVALUE_BASE DESC LIMIT 10","use_as_onboarding_question":true}},{{"name":"sector_allocation_by_portfolio","question":"What is the sector allocation for the SAM Technology & Infrastructure portfolio?","sql":"SELECT __ISSUERS.Industry, SUM(__HOLDINGS.MARKETVALUE_BASE) AS SECTOR_VALUE, (SUM(__HOLDINGS.MARKETVALUE_BASE) / SUM(SUM(__HOLDINGS.MARKETVALUE_BASE)) OVER ()) * 100 AS SECTOR_WEIGHT_PCT FROM __HOLDINGS JOIN __SECURITIES ON __HOLDINGS.SECURITYID = __SECURITIES.SECURITYID JOIN __ISSUERS ON __SECURITIES.ISSUERID = __ISSUERS.ISSUERID JOIN __PORTFOLIOS ON __HOLDINGS.PORTFOLIOID = __PORTFOLIOS.PORTFOLIOID WHERE __PORTFOLIOS.PORTFOLIONAME = \\'SAM Technology & Infrastructure\\' AND __HOLDINGS.HOLDINGDATE = (SELECT MAX(HOLDINGDATE) FROM __HOLDINGS) GROUP BY __ISSUERS.Industry ORDER BY SECTOR_VALUE DESC","use_as_onboarding_question":true}},{{"name":"concentration_warnings","question":"Which portfolios have positions above the 6.5% concentration warning threshold?","sql":"WITH position_weights AS (SELECT __HOLDINGS.PORTFOLIOID, __HOLDINGS.SECURITYID, __HOLDINGS.MARKETVALUE_BASE, (__HOLDINGS.MARKETVALUE_BASE / SUM(__HOLDINGS.MARKETVALUE_BASE) OVER (PARTITION BY __HOLDINGS.PORTFOLIOID)) * 100 AS POSITION_WEIGHT_PCT FROM __HOLDINGS WHERE __HOLDINGS.HOLDINGDATE = (SELECT MAX(HOLDINGDATE) FROM __HOLDINGS)) SELECT __PORTFOLIOS.PORTFOLIONAME, __SECURITIES.DESCRIPTION, __SECURITIES.TICKER, pw.POSITION_WEIGHT_PCT FROM position_weights pw JOIN __SECURITIES ON pw.SECURITYID = __SECURITIES.SECURITYID JOIN __PORTFOLIOS ON pw.PORTFOLIOID = __PORTFOLIOS.PORTFOLIOID WHERE pw.POSITION_WEIGHT_PCT > 6.5 ORDER BY pw.POSITION_WEIGHT_PCT DESC","use_as_onboarding_question":false}},{{"name":"issuer_exposure_analysis","question":"What is the total exposure to Apple and Microsoft across all portfolios?","sql":"SELECT __ISSUERS.LegalName, __ISSUERS.Industry, SUM(__HOLDINGS.MARKETVALUE_BASE) AS TOTAL_ISSUER_EXPOSURE, COUNT(DISTINCT __PORTFOLIOS.PORTFOLIOID) AS PORTFOLIOS_EXPOSED FROM __HOLDINGS JOIN __SECURITIES ON __HOLDINGS.SECURITYID = __SECURITIES.SECURITYID JOIN __ISSUERS ON __SECURITIES.ISSUERID = __ISSUERS.ISSUERID JOIN __PORTFOLIOS ON __HOLDINGS.PORTFOLIOID = __PORTFOLIOS.PORTFOLIOID WHERE __HOLDINGS.HOLDINGDATE = (SELECT MAX(HOLDINGDATE) FROM __HOLDINGS) AND __SECURITIES.TICKER IN (\\'AAPL\\', \\'MSFT\\') GROUP BY __ISSUERS.ISSUERID, __ISSUERS.LegalName, __ISSUERS.Industry ORDER BY TOTAL_ISSUER_EXPOSURE DESC","use_as_onboarding_question":false}}],"module_custom_instructions":{{"sql_generation":"For portfolio weight calculations, always multiply by 100 to show percentages. For current holdings queries, automatically filter to the most recent holding date using WHERE HOLDINGDATE = (SELECT MAX(HOLDINGDATE) FROM HOLDINGS). When calculating issuer exposure, aggregate MARKETVALUE_BASE across all securities of the same issuer. Always round market values to 2 decimal places and portfolio weights to 1 decimal place.","question_categorization":"If users ask about \\'funds\\' or \\'portfolios\\', treat these as the same concept referring to investment portfolios. If users ask about current holdings without specifying a date, assume they want the most recent data."}}}}');
        """).collect()
        
        # print("   ✅ Created semantic view: SAM_ANALYST_VIEW")
        
    except Exception as e:
        print(f"ERROR: Failed to create semantic view: {e}")
        raise
    
    # Create scenario-specific semantic views
    if scenarios and 'research_copilot' in scenarios:
        try:
            # print(" Creating research semantic view with fundamentals...")
            create_research_semantic_view(session)
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Could not create research semantic view: {e}")
            # print("   This is required for research_copilot scenario")
            raise Exception(f"Failed to create research semantic view: {e}")
    
    # Create quantitative semantic view for factor analysis
    if scenarios and 'quant_analyst' in scenarios:
        try:
            # print(" Creating quantitative semantic view for factor analysis...")
            create_quantitative_semantic_view(session)
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Could not create quantitative semantic view: {e}")
            # print("   This is required for quant_analyst scenarios")
            raise Exception(f"Failed to create quantitative semantic view: {e}")
    
    # Create implementation semantic view for portfolio management
    if scenarios and ('portfolio_copilot' in scenarios or 'sales_advisor' in scenarios):
        try:
            # print("🎯 Creating implementation semantic view for portfolio management...")
            create_implementation_semantic_view(session)
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Could not create implementation semantic view: {e}")
            # print("   This is required for portfolio_copilot and sales_advisor scenarios")
            raise Exception(f"Failed to create implementation semantic view: {e}")
    
    # Create SEC filings semantic view for financial analysis
    try:
        # print("💰 Creating SEC filings semantic view for financial analysis...")
        create_sec_filings_semantic_view(session)
    except Exception as e:
        print(f"ERROR: CRITICAL FAILURE: Could not create SEC filings semantic view: {e}")
        # print("   This is required for comprehensive financial analysis")
        raise Exception(f"Failed to create SEC filings semantic view: {e}")
    
    # Create supply chain semantic view for risk verification
    if scenarios and 'portfolio_copilot' in scenarios:
        try:
            # print("🔗 Creating supply chain semantic view for risk verification...")
            create_supply_chain_semantic_view(session)
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Could not create supply chain semantic view: {e}")
            # print("   This is required for risk verification scenario")
            raise Exception(f"Failed to create supply chain semantic view: {e}")

def create_research_semantic_view(session: Session):
    """Create semantic view for research with fundamentals and estimates data."""
    
    # First check if the fundamentals tables exist
    try:
        session.sql(f"SELECT 1 FROM {config.DATABASE['name']}.CURATED.FACT_FUNDAMENTALS LIMIT 1").collect()
        session.sql(f"SELECT 1 FROM {config.DATABASE['name']}.CURATED.FACT_ESTIMATES LIMIT 1").collect()
    except:
        print("WARNING:  Fundamentals tables not found, skipping research view creation")
        return
    
    # Create the research-focused semantic view
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE['name']}.AI.SAM_RESEARCH_VIEW
	TABLES (
		SECURITIES AS {config.DATABASE['name']}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','equities','securities') 
			COMMENT='Security master data',
		ISSUERS AS {config.DATABASE['name']}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate data',
		FUNDAMENTALS AS {config.DATABASE['name']}.CURATED.FACT_FUNDAMENTALS
			PRIMARY KEY (SECURITY_ID, REPORTING_DATE, METRIC_NAME)
			WITH SYNONYMS=('financials','earnings','results','fundamentals')
			COMMENT='Company financial fundamentals',
		ESTIMATES AS {config.DATABASE['name']}.CURATED.FACT_ESTIMATES
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
		ISSUERS.LegalName AS LEGALNAME WITH SYNONYMS=('issuer','legal_name','entity_name') COMMENT='Legal entity name',
		ISSUERS.Industry AS SIC_DESCRIPTION WITH SYNONYMS=('industry','sector','industry_type','sic_industry','business_type','industry_description') COMMENT='SIC industry classification with granular descriptions (e.g., Semiconductors and related devices, Computer programming services). Use for industry-level filtering.',
		ISSUERS.CountryOfIncorporation AS COUNTRYOFINCORPORATION WITH SYNONYMS=('domicile','country','headquarters') COMMENT='Country of incorporation using 2-letter ISO codes (e.g., TW for Taiwan, US for United States, GB for United Kingdom)',
		
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
    
    # print("   ✅ Created semantic view: SAM_RESEARCH_VIEW")

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
            session.sql(f"SELECT 1 FROM {config.DATABASE['name']}.CURATED.{table} LIMIT 1").collect()
        except:
            missing_tables.append(table)
    
    if missing_tables:
        print(f"WARNING:  Quantitative tables not found, skipping quant view creation: {missing_tables}")
        return
    
    # Create the quantitative analysis semantic view
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE['name']}.AI.SAM_QUANT_VIEW
	TABLES (
		HOLDINGS AS {config.DATABASE['name']}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HoldingDate, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('quant_positions','factor_holdings','quantitative_holdings','quant_allocations') 
			COMMENT='Portfolio holdings for factor analysis',
		PORTFOLIOS AS {config.DATABASE['name']}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('quant_funds','factor_strategies','quantitative_mandates','quant_portfolios') 
			COMMENT='Portfolio information',
		SECURITIES AS {config.DATABASE['name']}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('factor_companies','quant_stocks','quantitative_instruments','factor_securities') 
			COMMENT='Security reference data',
		ISSUERS AS {config.DATABASE['name']}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('factor_issuers','quantitative_entities','quant_corporates') 
			COMMENT='Issuer data',
		FACTOR_EXPOSURES AS {config.DATABASE['name']}.CURATED.FACT_FACTOR_EXPOSURES
			PRIMARY KEY (SECURITYID, EXPOSURE_DATE, FACTOR_NAME)
			WITH SYNONYMS=('factors','loadings','exposures','factor_data')
			COMMENT='Factor exposures and loadings',
		FUNDAMENTALS AS {config.DATABASE['name']}.CURATED.FACT_FUNDAMENTALS
			PRIMARY KEY (SECURITY_ID, REPORTING_DATE, METRIC_NAME)
			WITH SYNONYMS=('financials','earnings','fundamentals','metrics')
			COMMENT='Financial fundamentals data',
		ESTIMATES AS {config.DATABASE['name']}.CURATED.FACT_ESTIMATES
			PRIMARY KEY (SECURITY_ID, ESTIMATE_DATE, FISCAL_PERIOD, METRIC_NAME)
			WITH SYNONYMS=('forecasts','estimates','consensus','guidance')
			COMMENT='Analyst estimates and guidance',
		MARKET_DATA AS {config.DATABASE['name']}.CURATED.FACT_MARKETDATA_TIMESERIES
			PRIMARY KEY (PriceDate, SECURITYID)
			WITH SYNONYMS=('prices','returns','market_data','performance')
			COMMENT='Market data and returns',
		BENCHMARK_HOLDINGS AS {config.DATABASE['name']}.CURATED.FACT_BENCHMARK_HOLDINGS
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
		ISSUERS.LegalName AS LEGALNAME WITH SYNONYMS=('factor_issuer','quant_legal_name','quantitative_entity_name') COMMENT='Legal entity name',
		ISSUERS.Industry AS SIC_DESCRIPTION WITH SYNONYMS=('industry','sector','factor_sector','quant_industry','business_type','industry_classification') COMMENT='SIC industry classification with granular descriptions. Use for industry-level factor analysis and screening.',
		ISSUERS.CountryOfIncorporation AS COUNTRYOFINCORPORATION WITH SYNONYMS=('factor_domicile','quant_country','quantitative_headquarters') COMMENT='Country of incorporation using 2-letter ISO codes (e.g., TW for Taiwan, US for United States, GB for United Kingdom)',
		
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
	COMMENT='Quantitative analysis semantic view with factor exposures, performance attribution, and systematic analysis capabilities'
	WITH EXTENSION (CA='{{"tables":[{{"name":"HOLDINGS","metrics":[{{"name":"PORTFOLIO_WEIGHT"}},{{"name":"PORTFOLIO_WEIGHT_PCT"}},{{"name":"TOTAL_MARKET_VALUE"}}],"time_dimensions":[{{"name":"exposure_date","expr":"FactorDate","data_type":"DATE","synonyms":["factor_date","exposure_date","measurement_date"],"description":"The date when factor exposures were calculated. Use for factor evolution analysis."}},{{"name":"exposure_month","expr":"DATE_TRUNC(\\'MONTH\\', FactorDate)","data_type":"DATE","synonyms":["month","monthly","factor_month"],"description":"Monthly aggregation for factor trend analysis."}}]}},{{"name":"FACTOR_EXPOSURES","metrics":[{{"name":"FACTOR_EXPOSURE"}},{{"name":"FACTOR_R_SQUARED"}},{{"name":"GROWTH_SCORE"}},{{"name":"MOMENTUM_SCORE"}},{{"name":"QUALITY_SCORE"}},{{"name":"VALUE_SCORE"}}]}},{{"name":"ISSUERS","dimensions":[{{"name":"COUNTRYOFINCORPORATION"}},{{"name":"LEGALNAME"}},{{"name":"SIC_DESCRIPTION"}}]}},{{"name":"PORTFOLIOS","dimensions":[{{"name":"PortfolioName"}},{{"name":"Strategy"}}]}},{{"name":"SECURITIES","dimensions":[{{"name":"AssetClass"}},{{"name":"Description"}},{{"name":"Ticker"}}]}},{{"name":"MARKET_DATA","metrics":[{{"name":"PRICE_RETURN"}},{{"name":"TOTAL_RETURN"}},{{"name":"VOLUME_TRADED"}}]}},{{"name":"FUNDAMENTALS","metrics":[{{"name":"FUNDAMENTAL_VALUE"}}]}},{{"name":"ESTIMATES","metrics":[{{"name":"ESTIMATE_VALUE"}}]}},{{"name":"BENCHMARK_HOLDINGS","metrics":[{{"name":"BenchmarkWeight"}}]}}],"relationships":[{{"name":"HOLDINGS_TO_PORTFOLIOS"}},{{"name":"HOLDINGS_TO_SECURITIES"}},{{"name":"SECURITIES_TO_ISSUERS"}},{{"name":"FACTORS_TO_SECURITIES"}},{{"name":"FUNDAMENTALS_TO_SECURITIES"}},{{"name":"ESTIMATES_TO_SECURITIES"}},{{"name":"MARKET_DATA_TO_SECURITIES"}},{{"name":"BENCHMARK_TO_SECURITIES"}}],"module_custom_instructions":{{"sql_generation":"For factor analysis queries, always show factor exposures with 2 decimal places. When comparing factors across time, use monthly intervals. For trend analysis, calculate the difference between the most recent and previous period factor exposures."}}}}');
    """).collect()
    
    # print("   ✅ Created semantic view: SAM_QUANT_VIEW")

def create_search_services(session: Session, scenarios: List[str]):
    """Create Cortex Search services for required document types."""
    
    # Determine required document types from scenarios
    required_doc_types = set()
    for scenario in scenarios:
        if scenario in config.SCENARIO_DATA_REQUIREMENTS:
            required_doc_types.update(config.SCENARIO_DATA_REQUIREMENTS[scenario])
    
    # print(f"   📑 Document types: {', '.join(required_doc_types)}")
    
    # Group document types by search service (some services combine multiple corpus tables)
    service_to_corpus_tables = {}
    for doc_type in required_doc_types:
        if doc_type in config.DOCUMENT_TYPES:
            service_name = config.DOCUMENT_TYPES[doc_type]['search_service']
            corpus_table = f"{config.DATABASE['name']}.CURATED.{config.DOCUMENT_TYPES[doc_type]['corpus_name']}"
            
            if service_name not in service_to_corpus_tables:
                service_to_corpus_tables[service_name] = []
            service_to_corpus_tables[service_name].append(corpus_table)
    
    # Create search service for each unique service (combining multiple corpus tables if needed)
    for service_name, corpus_tables in service_to_corpus_tables.items():
        try:
            # Use dedicated Cortex Search warehouse from structured config
            search_warehouse = config.WAREHOUSES['cortex_search']['name']
            target_lag = config.WAREHOUSES['cortex_search']['target_lag']
            
            # Build UNION ALL query if multiple corpus tables
            if len(corpus_tables) == 1:
                from_clause = f"FROM {corpus_tables[0]}"
            else:
                union_parts = [f"""
                    SELECT 
                        DOCUMENT_ID,
                        DOCUMENT_TITLE,
                        DOCUMENT_TEXT,
                        SecurityID,
                        IssuerID,
                        DOCUMENT_TYPE,
                        PUBLISH_DATE,
                        LANGUAGE
                    FROM {table}""" for table in corpus_tables]
                from_clause = " UNION ALL ".join(union_parts)
                from_clause = f"FROM ({from_clause})"
            
            # Create enhanced Cortex Search service with SecurityID and IssuerID attributes
            # Using configurable TARGET_LAG for demo environments to see changes quickly
            session.sql(f"""
                CREATE OR REPLACE CORTEX SEARCH SERVICE {config.DATABASE['name']}.AI.{service_name}
                    ON DOCUMENT_TEXT
                    ATTRIBUTES DOCUMENT_TITLE, SecurityID, IssuerID, DOCUMENT_TYPE, PUBLISH_DATE, LANGUAGE
                    WAREHOUSE = {search_warehouse}
                    TARGET_LAG = '{target_lag}'
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
                    {from_clause}
            """).collect()
            
            # print(f"   ✅ Created search service: {service_name} from {len(corpus_tables)} corpus table(s)")
            
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Failed to create search service {service_name}: {e}")
            # print(f"   This search service is required for document types using {service_name}")
            raise Exception(f"Failed to create required search service {service_name}: {e}")

# =============================================================================
# CUSTOM TOOLS (PDF Generation)
# =============================================================================

def create_pdf_report_stage(session: Session):
    """Create Snowflake stage for storing generated PDF reports."""
    database_name = config.DATABASE['name']
    
    session.sql(f"""
        CREATE STAGE IF NOT EXISTS {database_name}.CURATED.SAM_REPORTS_STAGE
            ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
            DIRECTORY = (ENABLE = TRUE)
            COMMENT = 'Stage for storing generated investment committee and compliance PDF reports'
    """).collect()
    
    # print(" Created stage: SAM_REPORTS_STAGE for PDF document storage")

def create_simple_pdf_tool(session: Session):
    """Create simplified PDF generation tool that accepts markdown content."""
    database_name = config.DATABASE['name']
    
    pdf_generator_sql = f"""
CREATE OR REPLACE PROCEDURE {database_name}.AI.GENERATE_INVESTMENT_COMMITTEE_PDF(
    markdown_content VARCHAR,
    portfolio_name VARCHAR,
    security_ticker VARCHAR
)
RETURNS VARCHAR
LANGUAGE PYTHON
RUNTIME_VERSION = '3.11'
PACKAGES = ('snowflake-snowpark-python','markdown','weasyprint')
HANDLER = 'generate_pdf'
AS
$$
from snowflake.snowpark import Session
from datetime import datetime
import re
import markdown
import tempfile
import os

def generate_pdf(session: Session, markdown_content: str, portfolio_name: str, security_ticker: str):
    \"\"\"
    Generate PDF report from markdown content provided by the agent.
    
    Args:
        session: Snowpark session
        markdown_content: Complete markdown document from agent analysis
        portfolio_name: Portfolio name for filename
        security_ticker: Security ticker for filename
        
    Returns:
        String with download link to generated PDF
    \"\"\"
    # Generate filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    safe_portfolio = re.sub(r'[^a-zA-Z0-9_]', '_', portfolio_name)[:20]
    safe_ticker = re.sub(r'[^a-zA-Z0-9_]', '_', security_ticker)[:10]
    pdf_filename = f'mandate_compliance_{{safe_portfolio}}_{{safe_ticker}}_{{timestamp}}.pdf'
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Convert markdown to HTML
        html_body = markdown.markdown(markdown_content, extensions=['tables', 'fenced_code'])
        
        # Professional CSS styling for investment reports
        css_style = \"\"\"
            @page {{ size: A4; margin: 2cm; }}
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #2C3E50; }}
            h1 {{ color: #1F4E79; border-bottom: 3px solid #1F4E79; padding-bottom: 10px; }}
            h2 {{ color: #2E75B6; border-left: 4px solid #2E75B6; padding-left: 15px; }}
            h3 {{ color: #3F7CAC; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th {{ background-color: #1F4E79; color: white; padding: 12px; font-weight: bold; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            tr:nth-child(even) {{ background-color: #F8F9FA; }}
            .alert-box {{ background-color: #F8D7DA; border: 1px solid #F5C6CB; padding: 15px; margin: 20px 0; }}
            .recommendation {{ background-color: #D4EDDA; border: 1px solid #C3E6CB; padding: 15px; margin: 20px 0; }}
        \"\"\"
        
        # Snowcrest Asset Management header
        sam_header = \"\"\"
        <div style="text-align: center; background: linear-gradient(135deg, #1F4E79, #2E75B6); color: white; padding: 20px; margin-bottom: 30px; border-radius: 10px;">
            <h1 style="margin: 0; font-size: 28px; color: white; border: none;">🏔️ SNOWCREST ASSET MANAGEMENT</h1>
            <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Investment Committee Decision Documentation</p>
        </div>
        \"\"\"
        
        # Professional footer
        footer = f\"\"\"
        <div class="footer" style="margin-top: 30px; padding-top: 15px; border-top: 2px solid #1F4E79; font-size: 12px; color: #666;">
            <p><strong>Report Generated:</strong> {{datetime.now().strftime('%B %d, %Y at %I:%M %p UTC')}}</p>
            <p><strong>Generated By:</strong> Snowflake Intelligence - Portfolio Co-Pilot</p>
            <p><em>This report demonstrates AI-powered investment decision making with Snowflake Intelligence</em></p>
        </div>
        \"\"\"
        
        # Complete HTML document
        html_content = f\"\"\"
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Snowcrest Asset Management - Investment Committee Report</title>
            <style>{{css_style}}</style>
        </head>
        <body>
            {{sam_header}}
            {{html_body}}
            {{footer}}
        </body>
        </html>
        \"\"\"
        
        # Create HTML file
        html_path = os.path.join(tmpdir, 'report.html')
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Convert HTML to PDF
        import weasyprint
        pdf_path = os.path.join(tmpdir, pdf_filename)
        weasyprint.HTML(filename=html_path).write_pdf(pdf_path)
        
        # Upload to stage
        stage_path = '@SAM_DEMO.CURATED.SAM_REPORTS_STAGE'
        session.file.put(pdf_path, stage_path, overwrite=True, auto_compress=False)
        
        # Generate presigned URL for download
        presigned_url = session.sql(
            f"SELECT GET_PRESIGNED_URL('{{stage_path}}', '{{pdf_filename}}') AS url"
        ).collect()[0]['URL']
        
        # Format response with clickable link
        report_display_name = f"Investment Committee Decision - {{portfolio_name}} - {{security_ticker}}"
        return f"[{{report_display_name}}]({{presigned_url}}) - Professional mandate compliance report generated successfully. The document includes full analysis, data sources, and conversational audit trail for investment committee review."
$$;
    """
    
    session.sql(pdf_generator_sql).collect()
    # print(" Created custom tool: GENERATE_INVESTMENT_COMMITTEE_PDF (simplified markdown input)")

def validate_components(session: Session, semantic_built: bool, search_built: bool):
    """Validate that AI components are working correctly."""
    
    if semantic_built:
        # print(" Testing semantic view...")
        try:
            # Test semantic view using proper SEMANTIC_VIEW() function with correct semantic names
            test_query = f"""
                SELECT * FROM SEMANTIC_VIEW(
                    {config.DATABASE['name']}.AI.SAM_ANALYST_VIEW
                    METRICS TOTAL_MARKET_VALUE
                    DIMENSIONS PORTFOLIONAME
                )
                LIMIT 5
            """
            result = session.sql(test_query).collect()
            # print(f" Semantic view query test passed: {len(result)} results")
            
            # Test DESCRIBE SEMANTIC VIEW
            describe_result = session.sql(f"DESCRIBE SEMANTIC VIEW {config.DATABASE['name']}.AI.SAM_ANALYST_VIEW").collect()
            # print(f" Semantic view structure validated: {len(describe_result)} components")
            
            # Test with multiple metrics and dimensions (using semantic names BEFORE AS)
            advanced_test = f"""
                SELECT * FROM SEMANTIC_VIEW(
                    {config.DATABASE['name']}.AI.SAM_ANALYST_VIEW
                    METRICS TOTAL_MARKET_VALUE, HOLDING_COUNT
                    DIMENSIONS DESCRIPTION, Industry
                )
                LIMIT 10
            """
            advanced_result = session.sql(advanced_test).collect()
            # print(f" Advanced semantic view test passed: {len(advanced_result)} records")
            
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Semantic view validation failed: {e}")
            # print("   The main semantic view is essential for all agents")
            raise Exception(f"Main semantic view validation failed: {e}")
    
    if search_built:
        # print(" Testing search services...")
        try:
            # Get list of search services using correct SHOW command
            database_name = config.DATABASE['name']
            ai_objects = session.sql(f'SHOW CORTEX SEARCH SERVICES IN {database_name}.AI').collect()
            
            # print(f"Found {len(ai_objects)} search services to test")
            
            # Test each search service using your example syntax (without schema prefix in OVER clause)
            for service in ai_objects:
                service_name = service['name']
                try:
                    test_result = session.sql(f"""
                        SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                            '{config.DATABASE['name']}.AI.{service_name}',
                            '{{"query": "technology investment", "limit": 2}}'
                        ) 
                    """).collect()
                    # print(f" Search service test passed: {service_name}")
                except Exception as e:
                    print(f"ERROR: CRITICAL FAILURE: Search service test failed for {service_name}: {e}")
                    # print(f"   This search service is required for document search functionality")
                    raise Exception(f"Search service validation failed for {service_name}: {e}")
                    
        except Exception as e:
            print(f"ERROR: CRITICAL FAILURE: Search services validation failed: {e}")
            # print("   Search services are required for document-based scenarios")
            raise Exception(f"Search services validation failed: {e}")
    
    # print(" AI component validation complete")

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
            session.sql(f"SELECT 1 FROM {config.DATABASE['name']}.CURATED.{table} LIMIT 1").collect()
        except:
            print(f"WARNING:  Implementation table {table} not found, skipping implementation view creation")
            return
    
    # Create the implementation-focused semantic view
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE['name']}.AI.SAM_IMPLEMENTATION_VIEW
	TABLES (
		HOLDINGS AS {config.DATABASE['name']}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HOLDINGDATE, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('positions','investments','allocations','holdings') 
			COMMENT='Current portfolio holdings for implementation planning',
		PORTFOLIOS AS {config.DATABASE['name']}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('funds','strategies','mandates','portfolios') 
			COMMENT='Portfolio information',
		SECURITIES AS {config.DATABASE['name']}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','instruments','securities') 
			COMMENT='Security reference data',
		TRANSACTION_COSTS AS {config.DATABASE['name']}.CURATED.FACT_TRANSACTION_COSTS
			PRIMARY KEY (SECURITYID, COST_DATE)
			WITH SYNONYMS=('trading_costs','execution_costs','cost_data','transaction_costs')
			COMMENT='Transaction costs and market microstructure data',
		PORTFOLIO_LIQUIDITY AS {config.DATABASE['name']}.CURATED.FACT_PORTFOLIO_LIQUIDITY
			PRIMARY KEY (PORTFOLIOID, LIQUIDITY_DATE)
			WITH SYNONYMS=('liquidity_info','liquidity','cash_position','liquidity_data')
			COMMENT='Portfolio cash and liquidity information',
		RISK_LIMITS AS {config.DATABASE['name']}.CURATED.FACT_RISK_LIMITS
			PRIMARY KEY (PORTFOLIOID, LIMITS_DATE)
			WITH SYNONYMS=('risk_budget','limits','constraints','risk_limits')
			COMMENT='Risk limits and budget utilization',
		TRADING_CALENDAR AS {config.DATABASE['name']}.CURATED.FACT_TRADING_CALENDAR
			PRIMARY KEY (SECURITYID, EVENT_DATE)
			WITH SYNONYMS=('calendar','events','blackouts','earnings_dates','trading_calendar')
			COMMENT='Trading calendar with blackout periods and events',
		CLIENT_MANDATES AS {config.DATABASE['name']}.CURATED.DIM_CLIENT_MANDATES
			PRIMARY KEY (PORTFOLIOID)
			WITH SYNONYMS=('client_constraints','approvals','client_rules','client_mandates')
			COMMENT='Client mandate requirements and approval thresholds',
		TAX_IMPLICATIONS AS {config.DATABASE['name']}.CURATED.FACT_TAX_IMPLICATIONS
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
    
    # print(" Created semantic view: SAM_IMPLEMENTATION_VIEW")

def create_sec_filings_semantic_view(session: Session):
    """Create semantic view for SEC filings financial analysis."""
    
    # Check if SEC filings table exists
    try:
        session.sql(f"SELECT COUNT(*) FROM {config.DATABASE['name']}.CURATED.FACT_SEC_FILINGS LIMIT 1").collect()
    except Exception as e:
        print(f"WARNING:  FACT_SEC_FILINGS table not found: {e}")
        # print("   SEC filings semantic view creation skipped")
        return
    
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE['name']}.AI.SAM_SEC_FILINGS_VIEW
	TABLES (
		SEC_FILINGS AS {config.DATABASE['name']}.CURATED.FACT_SEC_FILINGS
			PRIMARY KEY (FILINGID) 
			WITH SYNONYMS=('sec_filings','filings','financial_statements','sec_data') 
			COMMENT='SEC filing financial data with comprehensive metrics across Income Statement, Balance Sheet, and Cash Flow',
		SECURITIES AS {config.DATABASE['name']}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('companies','stocks','bonds','instruments','securities') 
			COMMENT='Master security reference data',
		ISSUERS AS {config.DATABASE['name']}.CURATED.DIM_ISSUER
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
		ISSUERS.CompanyName AS LEGALNAME WITH SYNONYMS=('company','issuer_name','legal_name','company_name') COMMENT='Company legal name',
		ISSUERS.Ticker AS PRIMARYTICKER WITH SYNONYMS=('symbol','ticker_symbol','ticker','primary_ticker') COMMENT='Primary stock ticker symbol for the company',
		ISSUERS.Industry AS SIC_DESCRIPTION WITH SYNONYMS=('industry','sector','industry_type','business_type','industry_classification') COMMENT='SIC industry classification with granular descriptions. Use for industry-level financial analysis.',
		
		-- SEC Filing specific dimensions
		SEC_FILINGS.CIK AS CIK WITH SYNONYMS=('cik','sec_cik','company_cik') COMMENT='SEC Central Index Key',
		SEC_FILINGS.FORMTYPE AS FormType WITH SYNONYMS=('form_type','sec_form','filing_form') COMMENT='SEC form type (10-K, 10-Q, etc.)',
		SEC_FILINGS.TAG AS TAG WITH SYNONYMS=('tag','measure','metric_name','sec_measure') COMMENT='SEC financial measure tag name',
		SEC_FILINGS.MEASUREDESCRIPTION AS MeasureDescription WITH SYNONYMS=('measure_description','description','label') COMMENT='Human-readable description of the measure',
		SEC_FILINGS.UNITOFMEASURE AS UnitOfMeasure WITH SYNONYMS=('unit','measure_unit','unit_of_measure') COMMENT='Unit of measurement',
		SEC_FILINGS.STATEMENT AS Statement WITH SYNONYMS=('statement','financial_statement','fs_type') COMMENT='Financial statement type (Income Statement, Balance Sheet, Cash Flow)',
		
		-- Time dimensions
		SEC_FILINGS.FilingDate AS FILINGDATE WITH SYNONYMS=('filing_date','report_date','date','submission_date') COMMENT='SEC filing submission date (when the filing was submitted to SEC)',
		SEC_FILINGS.FiscalPeriod AS FISCALPERIOD WITH SYNONYMS=('period','quarter','fiscal_period') COMMENT='Fiscal reporting period (Q1, Q2, Q3, Q4, FY)',
		SEC_FILINGS.FiscalYear AS FISCALYEAR WITH SYNONYMS=('year','fiscal_year') COMMENT='Fiscal year',
		SEC_FILINGS.MeasurePeriodStart AS PERIODSTARTDATE WITH SYNONYMS=('measure_start','value_start_date','metric_start_date') COMMENT='Start date of the period that the measure value covers (varies by measure type)',
		SEC_FILINGS.MeasurePeriodEnd AS PERIODENDDATE WITH SYNONYMS=('measure_end','value_end_date','metric_end_date') COMMENT='End date of the period that the measure value covers (varies by measure type)'
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
	COMMENT='SEC filing data semantic view for financial analysis using authentic EDGAR data'
	WITH EXTENSION (CA='{{"tables":[{{"name":"SEC_FILINGS","metrics":[{{"name":"CASH_AND_EQUIVALENTS"}},{{"name":"CURRENT_ASSETS"}},{{"name":"CURRENT_LIABILITIES"}},{{"name":"DEPRECIATION"}},{{"name":"EPS_BASIC"}},{{"name":"EPS_DILUTED"}},{{"name":"FILING_COUNT"}},{{"name":"FINANCING_CASH_FLOW"}},{{"name":"GOODWILL"}},{{"name":"GROSS_PROFIT"}},{{"name":"INTEREST_EXPENSE"}},{{"name":"INVESTING_CASH_FLOW"}},{{"name":"MEASURE_VALUE"}},{{"name":"NET_INCOME"}},{{"name":"OPERATING_CASH_FLOW"}},{{"name":"OPERATING_EXPENSES"}},{{"name":"OPERATING_INCOME"}},{{"name":"RETAINED_EARNINGS"}},{{"name":"STOCK_BASED_COMPENSATION"}},{{"name":"TOTAL_ASSETS"}},{{"name":"TOTAL_EQUITY"}},{{"name":"TOTAL_LIABILITIES"}},{{"name":"TOTAL_REVENUE"}}],"time_dimensions":[{{"name":"filing_date","expr":"FILINGDATE","data_type":"DATE","synonyms":["report_date","filing_date","quarter_end_date"],"description":"The date when the SEC filing was submitted. Use for time-based financial analysis."}},{{"name":"filing_quarter","expr":"DATE_TRUNC(\\'QUARTER\\', FILINGDATE)","data_type":"DATE","synonyms":["quarter","quarterly","fiscal_quarter"],"description":"Quarterly aggregation for quarter-over-quarter financial comparisons."}}]}},{{"name":"ISSUERS","dimensions":[{{"name":"SIC_DESCRIPTION"}},{{"name":"LEGALNAME"}},{{"name":"PRIMARYTICKER"}}]}},{{"name":"SECURITIES"}}],"relationships":[{{"name":"SEC_FILINGS_TO_SECURITIES"}},{{"name":"SECURITIES_TO_ISSUERS"}}],"module_custom_instructions":{{"sql_generation":"For financial metrics, always use the most recent fiscal period when not specified. When showing quarterly progression, order by FILINGDATE DESC to show most recent first. Round revenue and income metrics to 2 decimal places. Use PRIMARYTICKER dimension (from ISSUERS table) for company filtering."}}}}');
    """).collect()
    
    # print(" Created semantic view: SAM_SEC_FILINGS_VIEW")

def create_supply_chain_semantic_view(session: Session):
    """Create semantic view for supply chain risk analysis."""
    
    # Check if supply chain relationships table exists
    try:
        session.sql(f"SELECT COUNT(*) FROM {config.DATABASE['name']}.CURATED.DIM_SUPPLY_CHAIN_RELATIONSHIPS LIMIT 1").collect()
    except Exception as e:
        print(f"WARNING:  DIM_SUPPLY_CHAIN_RELATIONSHIPS table not found: {e}")
        # print("   Supply chain semantic view creation skipped")
        return
    
    session.sql(f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE['name']}.AI.SAM_SUPPLY_CHAIN_VIEW
	TABLES (
		SUPPLY_CHAIN AS {config.DATABASE['name']}.CURATED.DIM_SUPPLY_CHAIN_RELATIONSHIPS
			PRIMARY KEY (RELATIONSHIPID) 
			WITH SYNONYMS=('supply_chain','dependencies','relationships','supplier_customer') 
			COMMENT='Supply chain relationships between issuers for risk analysis',
		COMPANY_ISSUERS AS {config.DATABASE['name']}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('companies','company_issuers','primary_entities') 
			COMMENT='Company issuer information',
		COUNTERPARTY_ISSUERS AS {config.DATABASE['name']}.CURATED.DIM_ISSUER
			PRIMARY KEY (ISSUERID) 
			WITH SYNONYMS=('counterparties','suppliers','customers','trading_partners') 
			COMMENT='Counterparty issuer information',
		SECURITIES AS {config.DATABASE['name']}.CURATED.DIM_SECURITY
			PRIMARY KEY (SECURITYID) 
			WITH SYNONYMS=('securities','stocks') 
			COMMENT='Security master data',
		HOLDINGS AS {config.DATABASE['name']}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HOLDINGDATE, PORTFOLIOID, SECURITYID) 
			WITH SYNONYMS=('positions','holdings','portfolio_holdings') 
			COMMENT='Portfolio holdings for exposure calculation',
		PORTFOLIOS AS {config.DATABASE['name']}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PORTFOLIOID) 
			WITH SYNONYMS=('portfolios','funds') 
			COMMENT='Portfolio information'
	)
	RELATIONSHIPS (
		SUPPLY_CHAIN_TO_COMPANY AS SUPPLY_CHAIN(COMPANY_ISSUERID) REFERENCES COMPANY_ISSUERS(ISSUERID),
		SUPPLY_CHAIN_TO_COUNTERPARTY AS SUPPLY_CHAIN(COUNTERPARTY_ISSUERID) REFERENCES COUNTERPARTY_ISSUERS(ISSUERID),
		SECURITIES_TO_COMPANY AS SECURITIES(ISSUERID) REFERENCES COMPANY_ISSUERS(ISSUERID),
		HOLDINGS_TO_SECURITIES AS HOLDINGS(SECURITYID) REFERENCES SECURITIES(SECURITYID),
		HOLDINGS_TO_PORTFOLIOS AS HOLDINGS(PORTFOLIOID) REFERENCES PORTFOLIOS(PORTFOLIOID)
	)
	DIMENSIONS (
		-- Company dimensions (US companies in portfolio)
		COMPANY_ISSUERS.CompanyName AS LEGALNAME WITH SYNONYMS=('company','company_name','us_company','portfolio_company','customer_company') COMMENT='US company legal name (the company with portfolio holdings)',
		COMPANY_ISSUERS.CompanyIndustry AS SIC_DESCRIPTION WITH SYNONYMS=('company_industry','customer_industry','us_industry') COMMENT='US company SIC industry classification',
		COMPANY_ISSUERS.CompanyCountry AS COUNTRYOFINCORPORATION WITH SYNONYMS=('company_country','customer_country') COMMENT='US company country of incorporation using 2-letter ISO codes (e.g., US for United States)',
		
		-- Counterparty dimensions (Taiwan suppliers)
		COUNTERPARTY_ISSUERS.CounterpartyName AS LEGALNAME WITH SYNONYMS=('counterparty','supplier','supplier_name','taiwan_supplier','supplier_company') COMMENT='Supplier/counterparty legal name (e.g., Taiwan semiconductor suppliers like TSMC)',
		COUNTERPARTY_ISSUERS.CounterpartyIndustry AS SIC_DESCRIPTION WITH SYNONYMS=('counterparty_industry','supplier_industry','taiwan_industry','semiconductor_industry') COMMENT='Supplier SIC industry classification (e.g., Semiconductors and related devices)',
		COUNTERPARTY_ISSUERS.CounterpartyCountry AS COUNTRYOFINCORPORATION WITH SYNONYMS=('counterparty_country','supplier_country','taiwan') COMMENT='Supplier country of incorporation using 2-letter ISO codes (use TW for Taiwan, not Taiwan)',
		
		-- Relationship dimensions
		SUPPLY_CHAIN.RelationshipType AS RELATIONSHIPTYPE WITH SYNONYMS=('relationship','relationship_type','supplier_or_customer','dependency_type') COMMENT='Relationship type: Supplier (for upstream dependencies) or Customer (for downstream)',
		SUPPLY_CHAIN.CriticalityTier AS CRITICALITYTIER WITH SYNONYMS=('criticality','importance','tier','priority') COMMENT='Criticality tier indicating importance: Low, Medium, High, Critical',
		
		-- Portfolio dimensions
		PORTFOLIOS.PortfolioName AS PORTFOLIONAME WITH SYNONYMS=('portfolio','fund','portfolio_name') COMMENT='Portfolio name for exposure calculation',
		
		-- Time dimensions
		HOLDINGS.HoldingDate AS HOLDINGDATE WITH SYNONYMS=('date','position_date','as_of_date') COMMENT='Holdings date for current positions'
	)
	METRICS (
		-- Relationship strength metrics (CostShare and RevenueShare are decimal values 0.0-1.0)
		SUPPLY_CHAIN.UPSTREAM_EXPOSURE AS SUM(COSTSHARE) WITH SYNONYMS=('upstream','cost_share','supplier_dependency','supplier_exposure') COMMENT='Upstream exposure as cost share from suppliers (0.0-1.0, represents percentage of costs from this supplier)',
		SUPPLY_CHAIN.DOWNSTREAM_EXPOSURE AS SUM(REVENUESHARE) WITH SYNONYMS=('downstream','revenue_share','customer_dependency','customer_exposure') COMMENT='Downstream exposure as revenue share to customers (0.0-1.0, represents percentage of revenue to this customer)',
		SUPPLY_CHAIN.MAX_DEPENDENCY AS MAX(GREATEST(COALESCE(COSTSHARE, 0), COALESCE(REVENUESHARE, 0))) WITH SYNONYMS=('max_dependency','largest_dependency','peak_exposure','max_share') COMMENT='Maximum single dependency (largest of cost or revenue share)',
		SUPPLY_CHAIN.AVG_DEPENDENCY AS AVG(GREATEST(COALESCE(COSTSHARE, 0), COALESCE(REVENUESHARE, 0))) WITH SYNONYMS=('avg_dependency','average_dependency','typical_exposure') COMMENT='Average dependency strength across relationships',
		
		-- Portfolio exposure metrics (for second-order risk calculation)
		HOLDINGS.DIRECT_EXPOSURE AS SUM(MARKETVALUE_BASE) WITH SYNONYMS=('direct_exposure','direct_position','position_value','market_value') COMMENT='Direct portfolio exposure to US companies in base currency (USD)',
		HOLDINGS.PORTFOLIO_WEIGHT_PCT AS SUM(PORTFOLIOWEIGHT) * 100 WITH SYNONYMS=('weight','portfolio_weight','allocation_percent','weight_percent') COMMENT='Portfolio weight as percentage (0-100)',
		
		-- Relationship counts (for analysis)
		SUPPLY_CHAIN.RELATIONSHIP_COUNT AS COUNT(RELATIONSHIPID) WITH SYNONYMS=('relationship_count','dependency_count','connection_count','supplier_count','customer_count') COMMENT='Count of supply chain relationships (can filter by RelationshipType for suppliers vs customers)',
		SUPPLY_CHAIN.DISTINCT_COMPANIES AS COUNT(DISTINCT COMPANY_ISSUERID) WITH SYNONYMS=('company_count','us_company_count','affected_companies') COMMENT='Count of distinct US companies with dependencies',
		SUPPLY_CHAIN.DISTINCT_SUPPLIERS AS COUNT(DISTINCT COUNTERPARTY_ISSUERID) WITH SYNONYMS=('supplier_count','unique_suppliers','taiwan_supplier_count') COMMENT='Count of distinct suppliers/counterparties',
		
		-- Source confidence and data quality
		SUPPLY_CHAIN.AVG_CONFIDENCE AS AVG(SOURCECONFIDENCE) WITH SYNONYMS=('confidence','average_confidence','data_quality','reliability') COMMENT='Average source confidence score (0-100, higher is better)'
	)
	COMMENT='Supply chain semantic view for multi-hop dependency and second-order risk analysis';
    """).collect()
    
    # print(" Created semantic view: SAM_SUPPLY_CHAIN_VIEW")