# src/ai_components/semantic_views.py
# Semantic view creation for Cortex Analyst in Frost Markets Intelligence Demo

from snowflake.snowpark import Session
from config import DemoConfig


def create_all_semantic_views(session: Session) -> None:
    """Create REAL semantic views for Cortex Analyst"""
    
    print("   🔍 Creating REAL semantic views for Cortex Analyst...")
    
    # Create EARNINGS_ACTUALS fact table first
    create_actuals_sql = """
    CREATE OR REPLACE TABLE CURATED.FACT_EARNINGS_ACTUAL AS
    SELECT 
        TICKER,
        FISCAL_QUARTER,
        METRIC_NAME,
        ESTIMATE_VALUE * (1 + UNIFORM(-0.1, 0.1, RANDOM())) AS ACTUAL_VALUE
    FROM CURATED.FACT_CONSENSUS_ESTIMATE 
    WHERE PROVIDER = 'FactSet'
    """
    session.sql(create_actuals_sql).collect()
    print("   ✅ EARNINGS_ACTUALS table created")
    
    # First verify column names in our tables
    print("   🔍 Verifying column names in source tables...")
    verify_table_columns(session)
    
    # Now create the semantic views
    print("   🔍 Creating EARNINGS_ANALYSIS_VIEW semantic view...")
    create_earnings_analysis_semantic_view(session)
    
    print("   🔍 Creating THEMATIC_RESEARCH_VIEW semantic view...")
    create_thematic_research_semantic_view(session)
    
    print("   🔍 Creating CLIENT_MARKET_IMPACT_VIEW semantic view...")
    create_client_market_impact_semantic_view(session)
    
    print("   🔍 Creating GLOBAL_MACRO_SIGNALS_VIEW semantic view...")
    create_global_macro_signals_semantic_view(session)
    
    print("   🔍 Creating FIRM_EXPOSURE_VIEW semantic view...")
    create_firm_exposure_semantic_view(session)


def verify_table_columns(session: Session) -> None:
    """Verify actual column names in source tables before creating semantic view"""
    
    tables_to_check = [
        "CURATED.DIM_COMPANY",
        "CURATED.FACT_CONSENSUS_ESTIMATE", 
        "CURATED.FACT_EARNINGS_ACTUAL",
        "CURATED.FACT_STOCK_PRICE_DAILY",
        "CURATED.NEWS_ARTICLES_CORPUS",
        "CURATED.RESEARCH_REPORTS_CORPUS",
        "CURATED.DIM_CLIENT",
        "CURATED.FACT_MACRO_SIGNAL",
        "CURATED.DIM_ECONOMIC_REGION",
        "CURATED.DIM_SECTOR_MACRO_CORRELATION",
        "CURATED.DIM_SECTOR"
    ]
    
    for table in tables_to_check:
        try:
            print(f"   📊 Columns in {table}:")
            result = session.sql(f"DESCRIBE TABLE {table}").collect()
            for row in result[:5]:  # Show first 5 columns
                print(f"      - {row['name']} ({row['type']})")
        except Exception as e:
            print(f"      ❌ Error describing {table}: {str(e)}")


def validate_synonym_uniqueness(synonyms_dict: dict) -> bool:
    """
    Validate that all synonyms are unique across dimensions and metrics.
    
    Args:
        synonyms_dict: Dictionary mapping element names to their synonym lists
        
    Returns:
        True if all synonyms are unique, False otherwise
    """
    all_synonyms = {}
    duplicates_found = False
    
    for element_name, synonyms in synonyms_dict.items():
        for synonym in synonyms:
            if synonym in all_synonyms:
                print(f"   ⚠️  Duplicate synonym '{synonym}' found in:")
                print(f"      - {all_synonyms[synonym]}")
                print(f"      - {element_name}")
                duplicates_found = True
            else:
                all_synonyms[synonym] = element_name
    
    if not duplicates_found:
        print(f"   ✅ All {len(all_synonyms)} synonyms are unique")
        return True
    else:
        return False


def test_semantic_view(session: Session, view_name: str, test_queries: list) -> None:
    """
    Test semantic view with SEMANTIC_VIEW() queries.
    
    Args:
        session: Snowpark session
        view_name: Full name of semantic view (e.g., ANALYTICS.EARNINGS_ANALYSIS_VIEW)
        test_queries: List of test query dictionaries with 'description', 'metrics', 'dimensions', 'limit'
    """
    print(f"   🧪 Testing {view_name}...")
    
    for i, test_query in enumerate(test_queries, 1):
        description = test_query.get('description', f'Test {i}')
        metrics = test_query.get('metrics', [])
        dimensions = test_query.get('dimensions', [])
        limit = test_query.get('limit', 5)
        
        metrics_str = ', '.join(metrics) if metrics else ''
        dimensions_str = ', '.join(dimensions) if dimensions else ''
        
        query = f"""
        SELECT * FROM SEMANTIC_VIEW(
            {view_name}
            {f'METRICS {metrics_str}' if metrics_str else ''}
            {f'DIMENSIONS {dimensions_str}' if dimensions_str else ''}
        ) LIMIT {limit}
        """
        
        try:
            result = session.sql(query).collect()
            print(f"      ✅ {description}: {len(result)} rows returned")
        except Exception as e:
            print(f"      ❌ {description}: {str(e)}")
            print(f"         Query: {query.strip()}")


def create_earnings_analysis_semantic_view(session: Session) -> None:
    """
    Create SEMANTIC VIEW for earnings analysis - required for Cortex Analyst
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW AI.EARNINGS_ANALYSIS_VIEW
	TABLES (
		ACTUALS AS CURATED.FACT_EARNINGS_ACTUAL
			PRIMARY KEY (TICKER, FISCAL_QUARTER, METRIC_NAME)
			WITH SYNONYMS=('earnings_results','financial_results','quarterly_results')
			COMMENT='Actual quarterly earnings results for companies',
		ESTIMATES AS CURATED.FACT_CONSENSUS_ESTIMATE  
			PRIMARY KEY (TICKER, FISCAL_QUARTER, METRIC_NAME, PROVIDER)
			WITH SYNONYMS=('consensus_estimates','analyst_estimates','forecasts')
			COMMENT='Consensus estimates from financial data providers',
		COMPANIES AS CURATED.DIM_COMPANY
			PRIMARY KEY (TICKER)
			WITH SYNONYMS=('companies_master','company_info')
			COMMENT='Company master data including sector and industry'
	)
	RELATIONSHIPS (
		ACTUALS_TO_COMPANIES AS ACTUALS(TICKER) REFERENCES COMPANIES(TICKER),
		ESTIMATES_TO_COMPANIES AS ESTIMATES(TICKER) REFERENCES COMPANIES(TICKER)
	)
	DIMENSIONS (
		COMPANIES.TICKER AS TICKER WITH SYNONYMS=('symbol','stock_ticker','ticker_symbol') COMMENT='Company stock ticker symbol',
		COMPANIES.COMPANY_NAME AS COMPANY_NAME WITH SYNONYMS=('company','firm_name','corporation') COMMENT='Full company name',
		COMPANIES.SECTOR AS SECTOR WITH SYNONYMS=('industry_sector','business_sector') COMMENT='Business sector classification',
		COMPANIES.INDUSTRY AS INDUSTRY WITH SYNONYMS=('industry_group','business_line') COMMENT='Industry classification',
		ACTUALS.FISCAL_QUARTER AS FISCAL_QUARTER WITH SYNONYMS=('reporting_period','fiscal_period','period') COMMENT='Fiscal quarter (e.g., 2024-Q1)',
		ACTUALS.METRIC_NAME AS METRIC_NAME WITH SYNONYMS=('financial_metric','kpi','measure') COMMENT='Financial metric name (Revenue, EPS, Net Income)',
		ESTIMATES.PROVIDER AS PROVIDER WITH SYNONYMS=('data_provider','research_provider','source') COMMENT='Source of the estimate (FactSet, Bloomberg, etc.)'
	)
	METRICS (
		ACTUALS.TOTAL_ACTUAL AS SUM(ACTUAL_VALUE) WITH SYNONYMS=('total_actual','sum_actual','actual_total') COMMENT='Sum of actual reported financial results',
		ESTIMATES.AVG_ESTIMATE AS AVG(ESTIMATE_VALUE) WITH SYNONYMS=('avg_estimate','mean_consensus','consensus_avg') COMMENT='Average consensus analyst estimate'
	)
	COMMENT='Earnings analysis semantic view for comparing actual results vs consensus estimates';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ EARNINGS_ANALYSIS_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create semantic view: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise


def create_thematic_research_semantic_view(session: Session) -> None:
    """
    Create THEMATIC_RESEARCH_VIEW semantic view for thematic investment research
    Supports Global Research & Market Insights scenarios
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW AI.THEMATIC_RESEARCH_VIEW
	TABLES (
		COMPANIES AS CURATED.DIM_COMPANY
			PRIMARY KEY (TICKER)
			WITH SYNONYMS=('companies_master','company_info','firms')
			COMMENT='Company master data with sector and industry classification',
		PRICES AS CURATED.FACT_STOCK_PRICE_DAILY
			PRIMARY KEY (TICKER, PRICE_DATE)
			WITH SYNONYMS=('stock_prices','market_data','price_history')
			COMMENT='Historical stock price data for performance analysis'
	)
	RELATIONSHIPS (
		PRICES_TO_COMPANIES AS PRICES(TICKER) REFERENCES COMPANIES(TICKER)
	)
	DIMENSIONS (
		COMPANIES.TICKER AS TICKER WITH SYNONYMS=('symbol','stock_ticker','ticker_symbol') COMMENT='Company stock ticker symbol',
		COMPANIES.COMPANY_NAME AS COMPANY_NAME WITH SYNONYMS=('company','firm_name','corporation') COMMENT='Company name',
		COMPANIES.SECTOR AS SECTOR WITH SYNONYMS=('industry_sector','business_sector') COMMENT='Business sector classification',
		COMPANIES.INDUSTRY AS INDUSTRY WITH SYNONYMS=('industry_group','business_line') COMMENT='Industry classification',
		PRICES.PRICE_DATE AS PRICE_DATE WITH SYNONYMS=('trade_date','market_date','date') COMMENT='Stock price date'
	)
	METRICS (
		PRICES.AVG_PRICE AS AVG(CLOSE) WITH SYNONYMS=('average_price','mean_price','avg_close') COMMENT='Average stock closing price',
		PRICES.MAX_PRICE AS MAX(CLOSE) WITH SYNONYMS=('highest_price','peak_price','max_close') COMMENT='Maximum stock closing price',
		PRICES.MIN_PRICE AS MIN(CLOSE) WITH SYNONYMS=('lowest_price','bottom_price','min_close') COMMENT='Minimum stock closing price',
		PRICES.TOTAL_VOLUME AS SUM(VOLUME) WITH SYNONYMS=('total_trading_volume','sum_volume','cumulative_volume') COMMENT='Total trading volume',
		COMPANIES.TOTAL_MARKET_CAP AS SUM(MARKET_CAP_BILLIONS) WITH SYNONYMS=('total_market_cap','sum_market_cap','aggregate_cap') COMMENT='Total market capitalization'
	)
	COMMENT='Thematic investment research semantic view for analyzing company performance and market trends';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ THEMATIC_RESEARCH_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create THEMATIC_RESEARCH_VIEW: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise


def create_client_market_impact_semantic_view(session: Session) -> None:
    """
    Create CLIENT_MARKET_IMPACT_VIEW semantic view for client analytics
    Supports Market Structure Reports scenarios
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW AI.CLIENT_MARKET_IMPACT_VIEW
	TABLES (
		CLIENTS AS CURATED.DIM_CLIENT
			PRIMARY KEY (CLIENT_ID)
			WITH SYNONYMS=('client_info','customer_profiles','institutional_clients')
			COMMENT='Client profile information and assets under management',
		TRADING AS CURATED.FACT_CLIENT_TRADE
			PRIMARY KEY (TRADE_ID)
			WITH SYNONYMS=('client_trades','trading_activity','derivative_trades')
			COMMENT='Client derivative trading activity and clearing details',
		ENGAGEMENT AS CURATED.FACT_CLIENT_ENGAGEMENT
			PRIMARY KEY (CLIENT_ID, CONTENT_ID, ENGAGEMENT_TIMESTAMP)
			WITH SYNONYMS=('content_engagement','research_downloads','client_interactions')
			COMMENT='Client engagement with research content and reports',
		DISCUSSIONS AS CURATED.FACT_CLIENT_DISCUSSION
			PRIMARY KEY (CLIENT_ID, DISCUSSION_DATE)
			WITH SYNONYMS=('client_meetings','strategic_discussions','relationship_management')
			COMMENT='Client discussion and meeting tracking'
	)
	RELATIONSHIPS (
		TRADING_TO_CLIENTS AS TRADING(CLIENT_ID) REFERENCES CLIENTS(CLIENT_ID),
		ENGAGEMENT_TO_CLIENTS AS ENGAGEMENT(CLIENT_ID) REFERENCES CLIENTS(CLIENT_ID),
		DISCUSSIONS_TO_CLIENTS AS DISCUSSIONS(CLIENT_ID) REFERENCES CLIENTS(CLIENT_ID)
	)
	DIMENSIONS (
		CLIENTS.CLIENT_ID AS CLIENT_ID WITH SYNONYMS=('client','customer_id','account_id') COMMENT='Unique client identifier',
		CLIENTS.CLIENT_NAME AS CLIENT_NAME WITH SYNONYMS=('client','customer_name','institution_name') COMMENT='Client organization name',
		CLIENTS.CLIENT_TYPE AS CLIENT_TYPE WITH SYNONYMS=('customer_type','institution_type','client_segment') COMMENT='Type of institutional client',
		CLIENTS.REGION AS REGION WITH SYNONYMS=('geography','location','client_region') COMMENT='Client geographic region',
		TRADING.TRADE_DATE AS TRADE_DATE WITH SYNONYMS=('transaction_date','trading_date') COMMENT='Date of trading activity',
		TRADING.ASSET_CLASS AS ASSET_CLASS WITH SYNONYMS=('product_type','instrument_class') COMMENT='Asset class of derivative trade',
		TRADING.DERIVATIVE_TYPE AS DERIVATIVE_TYPE WITH SYNONYMS=('product','instrument_type','trade_type') COMMENT='Specific derivative instrument type',
		TRADING.CLEARING_CCP AS CLEARING_CCP WITH SYNONYMS=('ccp','clearing_house','central_counterparty') COMMENT='Central counterparty for clearing',
		ENGAGEMENT.ENGAGEMENT_TYPE AS ENGAGEMENT_TYPE WITH SYNONYMS=('interaction_type','content_action','content_type') COMMENT='Type of content engagement',
		ENGAGEMENT.CONTENT_ID AS CONTENT_ID WITH SYNONYMS=('report_id','research_id','document_id') COMMENT='Research content identifier for correlation with Cortex Search',
		ENGAGEMENT.ENGAGEMENT_TIMESTAMP AS ENGAGEMENT_TIMESTAMP WITH SYNONYMS=('engagement_date','interaction_date','content_date','engagement_time') COMMENT='Date and time of content engagement',
		DISCUSSIONS.DISCUSSION_TYPE AS DISCUSSION_TYPE WITH SYNONYMS=('meeting_type','interaction_type') COMMENT='Type of client discussion',
		DISCUSSIONS.RELATIONSHIP_MANAGER AS RELATIONSHIP_MANAGER WITH SYNONYMS=('account_manager','rm','contact') COMMENT='Relationship manager name',
		DISCUSSIONS.TOPICS_DISCUSSED AS TOPICS_DISCUSSED WITH SYNONYMS=('discussion_topics','meeting_topics','conversation_themes','emir_3_0','market_structure','regulatory_topics') COMMENT='Topics discussed in client meetings including EMIR 3.0 and market structure'
	)
	METRICS (
		CLIENTS.TOTAL_AUM AS SUM(AUM_BILLIONS) WITH SYNONYMS=('total_assets','sum_aum','aggregate_assets') COMMENT='Total assets under management',
		TRADING.TOTAL_NOTIONAL AS SUM(NOTIONAL_VALUE) WITH SYNONYMS=('total_trading_volume','sum_notional','aggregate_volume') COMMENT='Total notional trading volume',
		TRADING.TRADE_COUNT AS COUNT(TRADE_ID) WITH SYNONYMS=('number_of_trades','trading_frequency','transaction_count') COMMENT='Count of derivative trades',
		ENGAGEMENT.ENGAGEMENT_COUNT AS COUNT(ENGAGEMENT_TIMESTAMP) WITH SYNONYMS=('content_interactions','download_count','interaction_count') COMMENT='Count of research content engagements',
		ENGAGEMENT.ENGAGEMENT_DURATION AS SUM(ENGAGEMENT_DURATION_MINUTES) WITH SYNONYMS=('engagement_score','interaction_score','content_score','total_duration') COMMENT='Total engagement duration in minutes',
		DISCUSSIONS.DISCUSSION_COUNT AS COUNT(DISCUSSION_DATE) WITH SYNONYMS=('meeting_count','interaction_frequency') COMMENT='Count of client discussions and meetings'
	)
	COMMENT='Client market impact analysis for understanding trading patterns and engagement with research content';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ CLIENT_MARKET_IMPACT_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create CLIENT_MARKET_IMPACT_VIEW: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise


def create_global_macro_signals_semantic_view(session: Session) -> None:
    """
    Create GLOBAL_MACRO_SIGNALS_VIEW semantic view for macroeconomic analysis
    Supports Global Macro Strategy scenarios
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW AI.GLOBAL_MACRO_SIGNALS_VIEW
	TABLES (
		SIGNALS AS CURATED.FACT_MACRO_SIGNAL
			PRIMARY KEY (SIGNAL_DATE, SIGNAL_NAME)
			WITH SYNONYMS=('macro_signals','economic_indicators','frost_indicators')
			COMMENT='Proprietary macroeconomic signals and leading indicators',
		REGIONS AS CURATED.DIM_ECONOMIC_REGION
			PRIMARY KEY (REGION_CODE)
			WITH SYNONYMS=('geographic_regions','economic_zones','geographies')
			COMMENT='Economic regions with GDP and population data',
		CORRELATIONS AS CURATED.DIM_SECTOR_MACRO_CORRELATION
			PRIMARY KEY (SECTOR, SIGNAL_NAME)
			WITH SYNONYMS=('sector_correlations','macro_relationships','signal_correlations')
			COMMENT='Correlation patterns between sectors and macro signals',
		SECTORS AS CURATED.DIM_SECTOR
			PRIMARY KEY (SECTOR)
			WITH SYNONYMS=('sector_master','sector_dim','industry_sectors')
			COMMENT='Sector dimension table for proper relationships',
		COMPANIES AS CURATED.DIM_COMPANY
			PRIMARY KEY (TICKER)
			WITH SYNONYMS=('companies_master','company_info','firms')
			COMMENT='Company master data with sector classification',
		PRICES AS CURATED.FACT_STOCK_PRICE_DAILY
			PRIMARY KEY (TICKER, PRICE_DATE)
			WITH SYNONYMS=('stock_prices','market_data','price_history')
			COMMENT='Historical stock price data for performance analysis'
	)
	RELATIONSHIPS (
		CORRELATIONS_TO_SECTORS AS CORRELATIONS(SECTOR) REFERENCES SECTORS(SECTOR),
		COMPANIES_TO_SECTORS AS COMPANIES(SECTOR) REFERENCES SECTORS(SECTOR),
		PRICES_TO_COMPANIES AS PRICES(TICKER) REFERENCES COMPANIES(TICKER)
	)
	DIMENSIONS (
		SIGNALS.SIGNAL_DATE AS SIGNAL_DATE WITH SYNONYMS=('date','observation_date','macro_date','time_period') COMMENT='Date of signal observation',
		SIGNALS.SIGNAL_NAME AS SIGNAL_NAME WITH SYNONYMS=('indicator_name','signal','macro_indicator','economic_indicator') COMMENT='Name of macroeconomic signal',
		SIGNALS.SIGNAL_CATEGORY AS SIGNAL_CATEGORY WITH SYNONYMS=('indicator_category','signal_type','macro_category') COMMENT='Category of macroeconomic signal',
		SIGNALS.SIGNAL_REGION AS SIGNAL_REGION WITH SYNONYMS=('geography','region','economic_region') COMMENT='Geographic region for the signal',
		SIGNALS.SIGNAL_DESCRIPTION AS SIGNAL_DESCRIPTION WITH SYNONYMS=('description','indicator_description') COMMENT='Description of the macroeconomic signal',
		REGIONS.REGION_CODE AS REGION_CODE WITH SYNONYMS=('country_code','geo_code') COMMENT='Region code identifier',
		REGIONS.REGION_NAME AS REGION_NAME WITH SYNONYMS=('region','country','geographic_name') COMMENT='Full region name',
		REGIONS.REGION_TYPE AS REGION_TYPE WITH SYNONYMS=('economy_type','market_type') COMMENT='Type of economy (Developed, Emerging)',
		SECTORS.SECTOR AS SECTOR WITH SYNONYMS=('sector_name','industry_sector','business_sector') COMMENT='Sector name',
		SECTORS.SECTOR_DESCRIPTION AS SECTOR_DESCRIPTION WITH SYNONYMS=('sector_desc') COMMENT='Sector description',
		CORRELATIONS.CORRELATION_SECTOR AS SECTOR WITH SYNONYMS=('corr_sector','signal_sector','correlation_sector') COMMENT='Sector for correlation mapping',
		CORRELATIONS.INTERPRETATION AS INTERPRETATION WITH SYNONYMS=('correlation_interpretation','relationship_description') COMMENT='Interpretation of sector-signal correlation',
		COMPANIES.TICKER AS TICKER WITH SYNONYMS=('symbol','stock_ticker','ticker_symbol') COMMENT='Company stock ticker symbol',
		COMPANIES.COMPANY_NAME AS COMPANY_NAME WITH SYNONYMS=('company','firm_name','corporation') COMMENT='Company name',
		COMPANIES.INDUSTRY AS INDUSTRY WITH SYNONYMS=('industry_group','business_line') COMMENT='Industry classification',
		PRICES.PRICE_DATE AS PRICE_DATE WITH SYNONYMS=('trade_date','market_date','stock_date') COMMENT='Stock price date'
	)
	METRICS (
		SIGNALS.AVG_SIGNAL_VALUE AS AVG(SIGNAL_VALUE) WITH SYNONYMS=('average_signal','mean_indicator','avg_macro_value') COMMENT='Average value of macroeconomic signal',
		SIGNALS.MAX_SIGNAL_VALUE AS MAX(SIGNAL_VALUE) WITH SYNONYMS=('highest_signal','peak_indicator','max_macro_value') COMMENT='Maximum value of macroeconomic signal',
		SIGNALS.MIN_SIGNAL_VALUE AS MIN(SIGNAL_VALUE) WITH SYNONYMS=('lowest_signal','bottom_indicator','min_macro_value') COMMENT='Minimum value of macroeconomic signal',
		REGIONS.TOTAL_GDP AS SUM(GDP_TRILLIONS) WITH SYNONYMS=('sum_gdp','total_economic_output','aggregate_gdp') COMMENT='Total GDP across regions in trillions',
		REGIONS.TOTAL_POPULATION AS SUM(POPULATION_MILLIONS) WITH SYNONYMS=('sum_population','total_population','aggregate_population') COMMENT='Total population across regions in millions',
		CORRELATIONS.AVG_CORRELATION AS AVG(CORRELATION_COEFFICIENT) WITH SYNONYMS=('average_correlation','mean_correlation') COMMENT='Average correlation coefficient between sectors and signals',
		PRICES.AVG_PRICE AS AVG(CLOSE) WITH SYNONYMS=('average_price','mean_price','avg_close') COMMENT='Average stock closing price',
		PRICES.TOTAL_VOLUME AS SUM(VOLUME) WITH SYNONYMS=('total_trading_volume','sum_volume','cumulative_volume') COMMENT='Total trading volume'
	)
	COMMENT='Global macroeconomic signals semantic view for analyzing proprietary indicators and their correlations with sectors';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ GLOBAL_MACRO_SIGNALS_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create GLOBAL_MACRO_SIGNALS_VIEW: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise


def create_firm_exposure_semantic_view(session: Session) -> None:
    """
    Create FIRM_EXPOSURE_VIEW semantic view for market risk analysis
    Supports Market Risk Analyst scenarios
    """
    
    semantic_view_sql = """
CREATE OR REPLACE SEMANTIC VIEW AI.FIRM_EXPOSURE_VIEW
	TABLES (
		POSITIONS AS CURATED.FACT_FIRM_POSITION
			PRIMARY KEY (PORTFOLIO_ID, TICKER, AS_OF_DATE)
			WITH SYNONYMS=('firm_positions','portfolio_holdings','firm_holdings')
			COMMENT='Firm-wide portfolio positions and holdings',
		COMPANIES AS CURATED.DIM_COMPANY
			PRIMARY KEY (TICKER)
			WITH SYNONYMS=('companies_master','company_info','firms')
			COMMENT='Company master data with sector and industry classification',
		GEO_REVENUE AS CURATED.DIM_COMPANY_GEO_REVENUE
			PRIMARY KEY (TICKER, COUNTRY)
			WITH SYNONYMS=('geographic_revenue','revenue_exposure','country_exposure')
			COMMENT='Geographic revenue breakdown by country',
		CREDIT_RATINGS AS CURATED.DIM_COMPANY_CREDIT_RATING
			PRIMARY KEY (TICKER)
			WITH SYNONYMS=('credit_quality','sp_ratings','ratings')
			COMMENT='S&P credit ratings and outlook'
	)
	RELATIONSHIPS (
		POSITIONS_TO_COMPANIES AS POSITIONS(TICKER) REFERENCES COMPANIES(TICKER),
		GEO_REVENUE_TO_COMPANIES AS GEO_REVENUE(TICKER) REFERENCES COMPANIES(TICKER),
		CREDIT_RATINGS_TO_COMPANIES AS CREDIT_RATINGS(TICKER) REFERENCES COMPANIES(TICKER)
	)
	DIMENSIONS (
		POSITIONS.PORTFOLIO_ID AS PORTFOLIO_ID WITH SYNONYMS=('portfolio','fund_name','book','portfolio_name') COMMENT='Portfolio identifier',
		POSITIONS.TICKER AS TICKER WITH SYNONYMS=('symbol','stock_ticker','ticker_symbol','security') COMMENT='Company stock ticker symbol',
		POSITIONS.AS_OF_DATE AS AS_OF_DATE WITH SYNONYMS=('date','position_date','valuation_date','as_of') COMMENT='Position as-of date',
		COMPANIES.COMPANY_NAME AS COMPANY_NAME WITH SYNONYMS=('company','firm_name','corporation','name') COMMENT='Company name',
		COMPANIES.SECTOR AS SECTOR WITH SYNONYMS=('industry_sector','business_sector','sector_name') COMMENT='Business sector classification: Technology, Healthcare, Financial Services, Consumer Discretionary, Energy, Consumer Staples, Industrials',
		COMPANIES.INDUSTRY AS INDUSTRY WITH SYNONYMS=('industry_group','business_line','sub_sector','semiconductor','semiconductors','chip_manufacturer','biotech','ecommerce','ev','electric_vehicle') COMMENT='Industry classification within sector. Examples: Semiconductors (within Technology), Biotechnology (within Healthcare), E-commerce (within Consumer Discretionary), Electric Vehicles (within Consumer Discretionary)',
		GEO_REVENUE.COUNTRY AS COUNTRY WITH SYNONYMS=('geography','region','revenue_geography','geographic_exposure','taiwan','china','usa','europe') COMMENT='Country for geographic revenue exposure. Common values: United States, China, Taiwan, Germany, Japan, United Kingdom',
		CREDIT_RATINGS.RATING AS RATING WITH SYNONYMS=('credit_rating','sp_rating','rating_level') COMMENT='S&P credit rating',
		CREDIT_RATINGS.OUTLOOK AS OUTLOOK WITH SYNONYMS=('rating_outlook','credit_outlook','rating_direction') COMMENT='Credit rating outlook'
	)
	METRICS (
		POSITIONS.TOTAL_MARKET_VALUE AS SUM(MARKET_VALUE) WITH SYNONYMS=('total_exposure','sum_market_value','aggregate_value','total_value','net_exposure') COMMENT='Total market value of positions',
		POSITIONS.TOTAL_QUANTITY AS SUM(QUANTITY) WITH SYNONYMS=('total_shares','sum_quantity','aggregate_quantity') COMMENT='Total number of shares held',
		POSITIONS.POSITION_COUNT AS COUNT(TICKER) WITH SYNONYMS=('number_of_positions','holding_count','position_count') COMMENT='Count of distinct positions',
		GEO_REVENUE.AVG_REVENUE_PCT AS AVG(REVENUE_PERCENTAGE) WITH SYNONYMS=('average_revenue_exposure','mean_geographic_exposure') COMMENT='Average revenue percentage by geography',
		COMPANIES.TOTAL_MARKET_CAP AS SUM(MARKET_CAP_BILLIONS) WITH SYNONYMS=('sum_market_cap','aggregate_cap') COMMENT='Total market capitalization'
	)
	COMMENT='Firm exposure analysis semantic view for market risk assessment and portfolio stress testing';
    """
    
    try:
        result = session.sql(semantic_view_sql).collect()
        print("   ✅ FIRM_EXPOSURE_VIEW semantic view created successfully")
    except Exception as e:
        print(f"   ❌ Failed to create FIRM_EXPOSURE_VIEW: {str(e)}")
        print(f"   📋 Full SQL attempted:")
        print(semantic_view_sql)
        print("   ❓ Please help fix the SQL syntax error above")
        raise


def test_all_semantic_views(session: Session) -> None:
    """
    Test all created semantic views with SEMANTIC_VIEW() queries.
    This validates that the views work correctly with Cortex Analyst.
    """
    print("\n   🧪 Testing all semantic views...")
    
    # Test EARNINGS_ANALYSIS_VIEW
    earnings_tests = [
        {
            'description': 'Basic earnings test',
            'metrics': ['TOTAL_ACTUAL'],
            'dimensions': ['TICKER'],
            'limit': 5
        },
        {
            'description': 'Complex earnings test',
            'metrics': ['TOTAL_ACTUAL', 'AVG_ESTIMATE'],
            'dimensions': ['TICKER', 'FISCAL_QUARTER', 'METRIC_NAME'],
            'limit': 10
        }
    ]
    test_semantic_view(session, 'AI.EARNINGS_ANALYSIS_VIEW', earnings_tests)
    
    # Test THEMATIC_RESEARCH_VIEW
    thematic_tests = [
        {
            'description': 'Basic thematic test',
            'metrics': ['AVG_PRICE'],
            'dimensions': ['TICKER'],
            'limit': 5
        },
        {
            'description': 'Complex thematic test',
            'metrics': ['AVG_PRICE', 'TOTAL_VOLUME'],
            'dimensions': ['TICKER', 'SECTOR', 'PRICE_DATE'],
            'limit': 10
        }
    ]
    test_semantic_view(session, 'AI.THEMATIC_RESEARCH_VIEW', thematic_tests)
    
    # Test CLIENT_MARKET_IMPACT_VIEW
    client_tests = [
        {
            'description': 'Basic client test',
            'metrics': ['ENGAGEMENT_COUNT'],
            'dimensions': ['CLIENT_NAME'],
            'limit': 5
        },
        {
            'description': 'Complex client test',
            'metrics': ['ENGAGEMENT_COUNT', 'TOTAL_AUM'],
            'dimensions': ['CLIENT_NAME', 'CLIENT_TYPE', 'REGION'],
            'limit': 10
        }
    ]
    test_semantic_view(session, 'AI.CLIENT_MARKET_IMPACT_VIEW', client_tests)
    
    # Test GLOBAL_MACRO_SIGNALS_VIEW
    macro_tests = [
        {
            'description': 'Basic macro test',
            'metrics': ['AVG_SIGNAL_VALUE'],
            'dimensions': ['SIGNAL_NAME'],
            'limit': 5
        },
        {
            'description': 'Complex macro test',
            'metrics': ['AVG_SIGNAL_VALUE', 'AVG_CORRELATION'],
            'dimensions': ['SIGNAL_NAME', 'SECTOR', 'SIGNAL_REGION'],
            'limit': 10
        }
    ]
    test_semantic_view(session, 'AI.GLOBAL_MACRO_SIGNALS_VIEW', macro_tests)
    
    print("\n   ✅ Semantic view testing completed")