"""
WAM AI Demo - Semantic Views Creation
Creates CLIENT_FINANCIALS_SV and CLIENT_INTERACTIONS_SV following the enhanced rules
"""

from snowflake.snowpark import Session
import config

def create_semantic_views(session: Session):
    """Create all semantic views for Cortex Analyst"""
    
    print("  → Creating semantic views...")
    
    # Set the warehouse for AI operations
    session.sql(f"USE WAREHOUSE {config.CORTEX_WAREHOUSE}").collect()
    
    # Create CLIENT_FINANCIALS_SV
    create_client_financials_sv(session)
    
    # Create CLIENT_INTERACTIONS_SV
    create_client_interactions_sv(session)
    
    # Create ADVISOR_PERFORMANCE_SV for benchmarking
    create_advisor_performance_sv(session)
    
    # Create watchlist semantic view
    create_watchlist_analytics_sv(session)
    
    # Validate semantic views
    validate_semantic_views(session)
    
    print("  ✅ Semantic views created and validated")

def create_client_financials_sv(session: Session):
    """Create CLIENT_FINANCIALS_SV following the exact pattern from rules"""
    
    print("    → Creating CLIENT_FINANCIALS_SV...")
    
    # Drop any existing views first
    try:
        session.sql(f"DROP SEMANTIC VIEW IF EXISTS {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV").collect()
    except:
        pass  # Ignore if doesn't exist
    
    semantic_view_sql = f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
	TABLES (
		CLIENTS AS {config.DATABASE_NAME}.CURATED.DIM_CLIENT
			PRIMARY KEY (ClientID) 
			WITH SYNONYMS=('customers','investors','clients') 
			COMMENT='Client profile information',
		ACCOUNTS AS {config.DATABASE_NAME}.CURATED.DIM_ACCOUNT
			PRIMARY KEY (AccountID) 
			WITH SYNONYMS=('accounts','client_accounts') 
			COMMENT='Client account information',
		PORTFOLIOS AS {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO
			PRIMARY KEY (PortfolioID) 
			WITH SYNONYMS=('funds','strategies','mandates','portfolios') 
			COMMENT='Investment portfolios linked to accounts',
		HOLDINGS AS {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HoldingDate, PortfolioID, SecurityID) 
			WITH SYNONYMS=('positions','investments','allocations','holdings') 
			COMMENT='Daily portfolio holdings and positions',
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SecurityID) 
			WITH SYNONYMS=('companies','stocks','bonds','instruments','securities') 
			COMMENT='Master security reference data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (IssuerID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate hierarchy data'
	)
	RELATIONSHIPS (
		ACCOUNTS_TO_CLIENTS AS ACCOUNTS(ClientID) REFERENCES CLIENTS(ClientID),
		PORTFOLIOS_TO_ACCOUNTS AS PORTFOLIOS(AccountID) REFERENCES ACCOUNTS(AccountID),
		HOLDINGS_TO_PORTFOLIOS AS HOLDINGS(PortfolioID) REFERENCES PORTFOLIOS(PortfolioID),
		HOLDINGS_TO_SECURITIES AS HOLDINGS(SecurityID) REFERENCES SECURITIES(SecurityID),
		SECURITIES_TO_ISSUERS AS SECURITIES(IssuerID) REFERENCES ISSUERS(IssuerID)
	)
	DIMENSIONS (
		-- Client dimensions (for advisor scenarios)
		CLIENTS.FIRSTNAME AS FirstName WITH SYNONYMS=('client_first_name','first_name','sarah','michael','jennifer') COMMENT='Client first name',
		CLIENTS.LASTNAME AS LastName WITH SYNONYMS=('client_last_name','last_name','surname','johnson','williams','brown') COMMENT='Client last name',
		CLIENTS.RISKTOLERANCE AS RiskTolerance WITH SYNONYMS=('risk_profile','risk_level','conservative','moderate','aggressive') COMMENT='Client risk tolerance level',
		
		-- Account dimensions
		ACCOUNTS.ACCOUNTID AS AccountID WITH SYNONYMS=('account_id','account_number') COMMENT='Account identifier',
		ACCOUNTS.ACCOUNTTYPE AS AccountType WITH SYNONYMS=('account_type','account_category') COMMENT='Type of account (Brokerage, IRA, etc.)',
		
		-- Portfolio dimensions
		PORTFOLIOS.PORTFOLIONAME AS PortfolioName WITH SYNONYMS=('fund_name','strategy_name','portfolio_name') COMMENT='Portfolio or fund name',
		PORTFOLIOS.STRATEGY AS Strategy WITH SYNONYMS=('investment_strategy','portfolio_strategy') COMMENT='Investment strategy type',
		
		-- Security dimensions (with natural language support)
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('company','security_name','description','apple','microsoft','nvidia','jpmorgan','visa') COMMENT='Security description or company name',
		SECURITIES.PRIMARYTICKER AS PrimaryTicker WITH SYNONYMS=('ticker_symbol','symbol','primary_ticker','aapl','msft','nvda','jpm') COMMENT='Primary trading symbol',
		SECURITIES.ASSETCLASS AS AssetClass WITH SYNONYMS=('instrument_type','security_type','asset_class') COMMENT='Asset class: Equity, Corporate Bond, ETF',
		
		-- Issuer dimensions (for enhanced analysis)
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('issuer_name','legal_name','company_name','apple_inc','microsoft_corp','nvidia_corp','jpmorgan_chase','visa_inc','sap_se') COMMENT='Legal issuer name',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('sector','industry_sector','gics_sector','technology','financials','information_technology') COMMENT='GICS Level 1 sector classification',
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
	COMMENT='Multi-asset semantic view for portfolio analytics with issuer hierarchy support'
"""
    
    try:
        session.sql(semantic_view_sql).collect()
        print("    ✅ CLIENT_FINANCIALS_SV created successfully")
    except Exception as e:
        print(f"    ❌ Failed to create CLIENT_FINANCIALS_SV: {e}")
        # Provide diagnostic information
        print("    🔍 Checking table structures...")
        check_table_structure(session, f"{config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR")
        check_table_structure(session, f"{config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO")
        check_table_structure(session, f"{config.DATABASE_NAME}.CURATED.DIM_SECURITY")
        check_table_structure(session, f"{config.DATABASE_NAME}.CURATED.DIM_ISSUER")
        raise

def create_client_interactions_sv(session: Session):
    """Create CLIENT_INTERACTIONS_SV for communication analytics"""
    
    print("    → Creating CLIENT_INTERACTIONS_SV...")
    
    # Drop any existing views first
    try:
        session.sql(f"DROP SEMANTIC VIEW IF EXISTS {config.DATABASE_NAME}.AI.CLIENT_INTERACTIONS_SV").collect()
    except:
        pass  # Ignore if doesn't exist
    
    semantic_view_sql = f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.CLIENT_INTERACTIONS_SV
	TABLES (
		COMMUNICATIONS AS {config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS
			PRIMARY KEY (COMMUNICATION_ID) 
			WITH SYNONYMS=('communications','contacts','interactions') 
			COMMENT='Client communications and interaction data'
	)
	DIMENSIONS (
		-- Communication dimensions
		COMMUNICATIONS.CHANNEL AS CHANNEL WITH SYNONYMS=('communication_type','contact_method') COMMENT='Communication channel type',
		COMMUNICATIONS.CLIENT_ID AS CLIENT_ID WITH SYNONYMS=('client_id','customer_id') COMMENT='Client identifier',
		COMMUNICATIONS.ADVISOR_ID AS ADVISOR_ID WITH SYNONYMS=('advisor_id','manager_id') COMMENT='Advisor identifier'
	)
	METRICS (
		-- Communication frequency metrics
		COMMUNICATIONS.TOTAL_COMMUNICATIONS AS COUNT(*) WITH SYNONYMS=('total_communications','contact_count','interaction_count') COMMENT='Total number of communications'
	)
	COMMENT='Simplified client interaction analytics'
"""
    
    try:
        session.sql(semantic_view_sql).collect()
        print("    ✅ CLIENT_INTERACTIONS_SV created successfully")
    except Exception as e:
        print(f"    ❌ Failed to create CLIENT_INTERACTIONS_SV: {e}")
        # Provide diagnostic information
        print("    🔍 Checking view structure...")
        check_table_structure(session, f"{config.DATABASE_NAME}.CURATED.VW_CLIENT_INTERACTIONS")
        check_table_structure(session, f"{config.DATABASE_NAME}.CURATED.DIM_CLIENT")
        check_table_structure(session, f"{config.DATABASE_NAME}.CURATED.DIM_ADVISOR")
        raise

def check_table_structure(session: Session, table_name: str):
    """Check table structure for debugging"""
    try:
        columns = session.sql(f"DESCRIBE TABLE {table_name}").collect()
        print(f"    📋 Table {table_name} columns:")
        for row in columns:
            print(f"       - {row['name']} ({row['type']})")
    except Exception as e:
        print(f"    ❌ Cannot access table {table_name}: {e}")

def validate_semantic_views(session: Session):
    """Validate semantic views with test queries"""
    
    print("    → Validating semantic views...")
    
    # Validate CLIENT_FINANCIALS_SV
    try:
        # Basic functionality test - Client-specific query
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS TOTAL_MARKET_VALUE
                DIMENSIONS FIRSTNAME, LASTNAME
            ) 
            WHERE FIRSTNAME = 'Sarah'
            LIMIT 5
        """).collect()
        print(f"    ✅ CLIENT_FINANCIALS_SV client test: {len(result)} results")
        
        # Complex query test - Portfolio analysis
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS TOTAL_MARKET_VALUE, HOLDING_COUNT
                DIMENSIONS FIRSTNAME, LASTNAME, PRIMARYTICKER
            ) 
            WHERE FIRSTNAME = 'Sarah'
            LIMIT 10
        """).collect()
        print(f"    ✅ CLIENT_FINANCIALS_SV client holdings test: {len(result)} results")
        
        # Issuer-level aggregation test
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS ISSUER_EXPOSURE
                DIMENSIONS LEGALNAME
            ) LIMIT 5
        """).collect()
        print(f"    ✅ CLIENT_FINANCIALS_SV issuer test: {len(result)} results")
        
    except Exception as e:
        print(f"    ❌ CLIENT_FINANCIALS_SV validation failed: {e}")
        raise
    
    # Validate CLIENT_INTERACTIONS_SV
    try:
        # Basic functionality test
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_INTERACTIONS_SV
                METRICS TOTAL_COMMUNICATIONS
                DIMENSIONS CHANNEL
            ) LIMIT 5
        """).collect()
        print(f"    ✅ CLIENT_INTERACTIONS_SV basic test: {len(result)} results")
        
    except Exception as e:
        print(f"    ❌ CLIENT_INTERACTIONS_SV validation failed: {e}")
        raise
    
    # Validate watchlist semantic view
    validate_watchlist_analytics_sv(session)
    
    # Show created semantic views
    views = session.sql(f"SHOW SEMANTIC VIEWS IN {config.DATABASE_NAME}.AI").collect()
    print(f"    📋 Created semantic views: {len(views)}")
    for view in views:
        print(f"       - {view['name']}")

def create_advisor_performance_sv(session: Session):
    """Create ADVISOR_PERFORMANCE_SV for advisor benchmarking"""
    
    print("    → Creating ADVISOR_PERFORMANCE_SV...")
    
    # Drop any existing views first
    try:
        session.sql(f"DROP SEMANTIC VIEW IF EXISTS {config.DATABASE_NAME}.AI.ADVISOR_PERFORMANCE_SV").collect()
    except:
        pass  # Ignore if doesn't exist
    
    semantic_view_sql = f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.ADVISOR_PERFORMANCE_SV
TABLES (
	ADVISORS AS {config.DATABASE_NAME}.CURATED.ADVISOR_ROSTER
		PRIMARY KEY (AdvisorID)
		WITH SYNONYMS=('advisor_roster')
		COMMENT='Advisor roster with manager/team and peer group'
	,
	SUMMARY AS {config.DATABASE_NAME}.CURATED.ADVISOR_SUMMARY_TTM
		PRIMARY KEY (AdvisorID, PeriodEndDate)
		WITH SYNONYMS=('advisor_summary_ttm')
		COMMENT='TTM advisor performance summary'
)
RELATIONSHIPS (
	ADVISOR_TO_SUMMARY AS SUMMARY(AdvisorID) REFERENCES ADVISORS(AdvisorID)
)
DIMENSIONS (
	ADVISORS.ADVISORID AS AdvisorID WITH SYNONYMS=('advisor_id') COMMENT='Advisor identifier',
	ADVISORS.ADVISORNAME AS AdvisorName WITH SYNONYMS=('advisor_name') COMMENT='Advisor name',
	ADVISORS.MANAGERID AS ManagerID WITH SYNONYMS=('manager_id') COMMENT='Manager identifier',
	ADVISORS.MANAGERNAME AS ManagerName WITH SYNONYMS=('manager_name') COMMENT='Manager name',
	ADVISORS.TEAMNAME AS TeamName WITH SYNONYMS=('team') COMMENT='Team name',
	ADVISORS.PEERGROUP AS PeerGroup WITH SYNONYMS=('peer_group') COMMENT='Peer group by book size',
	SUMMARY.PERIODENDDATE AS PeriodEndDate WITH SYNONYMS=('period_end') COMMENT='TTM period end date'
)
METRICS (
	SUMMARY.AUM_GROWTH AS AVG((EndingAUM - StartingAUM - NetFlows) / NULLIF(StartingAUM,0)) WITH SYNONYMS=('aum_growth') COMMENT='TTM AUM growth %',
	SUMMARY.NET_NEW_ASSETS AS SUM(NetFlows) WITH SYNONYMS=('nna') COMMENT='TTM net new assets',
	SUMMARY.CLIENT_RETENTION AS AVG(1 - (ClientsLost / NULLIF(ClientsStart,0))) WITH SYNONYMS=('client_retention') COMMENT='TTM client retention',
	SUMMARY.AUM_RETENTION AS AVG(1 - (AUMLostFromDepartures / NULLIF(StartingAUM,0))) WITH SYNONYMS=('aum_retention') COMMENT='TTM AUM retention',
	SUMMARY.ENGAGEMENT_PER_CLIENT_QTR AS AVG(InteractionsCount / NULLIF(TotalHouseholds,0) / 4) WITH SYNONYMS=('engagement_qtr') COMMENT='Interactions per client per quarter',
	SUMMARY.AVG_DAYS_BETWEEN_CONTACTS AS AVG(AvgDaysBetweenContacts) WITH SYNONYMS=('days_between_contacts') COMMENT='Average days between contacts',
	SUMMARY.POSITIVE_PCT AS AVG(PositivePct) WITH SYNONYMS=('sent_pos') COMMENT='Share positive sentiment',
	SUMMARY.NEUTRAL_PCT AS AVG(NeutralPct) WITH SYNONYMS=('sent_neu') COMMENT='Share neutral sentiment',
	SUMMARY.NEGATIVE_PCT AS AVG(NegativePct) WITH SYNONYMS=('sent_neg') COMMENT='Share negative sentiment',
	SUMMARY.PLANNING_COVERAGE AS AVG(PlanningCoveragePct) WITH SYNONYMS=('plan_coverage') COMMENT='Households with current plan+IPS',
	SUMMARY.REVENUE_TTM AS SUM(Revenue_TTM) WITH SYNONYMS=('revenue_ttm') COMMENT='TTM revenue (assumed schedule)',
	SUMMARY.RISK_FLAGS_PER_100 AS AVG(RiskFlagsPer100) WITH SYNONYMS=('risk_rate') COMMENT='Risk flags per 100 comms'
)
"""
    
    session.sql(semantic_view_sql).collect()
    print(f"    ✅ ADVISOR_PERFORMANCE_SV created successfully")

def create_watchlist_analytics_sv(session: Session):
    """Create WATCHLIST_ANALYTICS_SV for thematic analysis"""
    
    print("    → Creating WATCHLIST_ANALYTICS_SV...")
    
    # Drop any existing views first
    try:
        session.sql(f"DROP SEMANTIC VIEW IF EXISTS {config.DATABASE_NAME}.AI.WATCHLIST_ANALYTICS_SV").collect()
    except:
        pass  # Ignore if doesn't exist
    
    semantic_view_sql = f"""
CREATE OR REPLACE SEMANTIC VIEW {config.DATABASE_NAME}.AI.WATCHLIST_ANALYTICS_SV
	TABLES (
		WATCHLISTS AS {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST
			PRIMARY KEY (WatchlistID) 
			WITH SYNONYMS=('watchlists','themes','lists') 
			COMMENT='Thematic investment watchlists',
		WATCHLIST_SECURITIES AS {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES
			PRIMARY KEY (WatchlistSecurityID) 
			WITH SYNONYMS=('watchlist_holdings','thematic_securities') 
			COMMENT='Securities included in watchlists',
		SECURITIES AS {config.DATABASE_NAME}.CURATED.DIM_SECURITY
			PRIMARY KEY (SecurityID) 
			WITH SYNONYMS=('companies','stocks','bonds','instruments','securities') 
			COMMENT='Master security reference data',
		ISSUERS AS {config.DATABASE_NAME}.CURATED.DIM_ISSUER
			PRIMARY KEY (IssuerID) 
			WITH SYNONYMS=('issuers','entities','corporates') 
			COMMENT='Issuer and corporate hierarchy data',
		HOLDINGS AS {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
			PRIMARY KEY (HoldingDate, PortfolioID, SecurityID) 
			WITH SYNONYMS=('positions','investments','allocations','holdings') 
			COMMENT='Portfolio holdings for performance analysis'
	)
	RELATIONSHIPS (
		WATCHLIST_SECURITIES_TO_WATCHLISTS AS WATCHLIST_SECURITIES(WatchlistID) REFERENCES WATCHLISTS(WatchlistID),
		WATCHLIST_SECURITIES_TO_SECURITIES AS WATCHLIST_SECURITIES(SecurityID) REFERENCES SECURITIES(SecurityID),
		SECURITIES_TO_ISSUERS AS SECURITIES(IssuerID) REFERENCES ISSUERS(IssuerID),
		HOLDINGS_TO_SECURITIES AS HOLDINGS(SecurityID) REFERENCES SECURITIES(SecurityID)
	)
	DIMENSIONS (
		-- Watchlist dimensions
		WATCHLISTS.WATCHLISTNAME AS WatchlistName WITH SYNONYMS=('watchlist_name','theme_name','list_name','carbon_negative_leaders','ai_innovation_leaders','esg_leaders') COMMENT='Watchlist or theme name',
		WATCHLISTS.WATCHLISTTYPE AS WatchlistType WITH SYNONYMS=('watchlist_type','theme_type','esg','technology','thematic') COMMENT='Type of watchlist theme',
		WATCHLISTS.WATCHLIST_DESCRIPTION AS Description WITH SYNONYMS=('watchlist_description','theme_description') COMMENT='Watchlist description and criteria',
		
		-- Security dimensions
		SECURITIES.PRIMARYTICKER AS PrimaryTicker WITH SYNONYMS=('ticker_symbol','symbol','primary_ticker','aapl','msft','nvda','jpm','sap') COMMENT='Primary trading symbol',
		SECURITIES.DESCRIPTION AS Description WITH SYNONYMS=('company','security_name','security_description','apple','microsoft','nvidia','jpmorgan','visa','sap') COMMENT='Security description',
		SECURITIES.ASSETCLASS AS AssetClass WITH SYNONYMS=('instrument_type','security_type','asset_class') COMMENT='Asset class: Equity, Corporate Bond, ETF',
		
		-- Issuer dimensions
		ISSUERS.LEGALNAME AS LegalName WITH SYNONYMS=('issuer_name','legal_name','company_name','apple_inc','microsoft_corp','nvidia_corp','sap_se') COMMENT='Legal issuer name',
		ISSUERS.GICS_SECTOR AS GICS_Sector WITH SYNONYMS=('sector','industry_sector','gics_sector','technology','information_technology') COMMENT='GICS Level 1 sector classification',
		
		-- ESG dimensions
		WATCHLIST_SECURITIES.ESG_SCORE AS ESG_Score WITH SYNONYMS=('esg_rating','sustainability_score','environmental_score') COMMENT='ESG score for watchlist inclusion',
		WATCHLIST_SECURITIES.RATIONALE AS Rationale WITH SYNONYMS=('rationale','reason','criteria') COMMENT='Rationale for watchlist inclusion'
	)
	METRICS (
		-- Watchlist metrics
		WATCHLIST_SECURITIES.SECURITY_COUNT AS COUNT(SecurityID) WITH SYNONYMS=('security_count','watchlist_size','theme_count') COMMENT='Number of securities in watchlist',
		WATCHLIST_SECURITIES.AVG_ESG_SCORE AS AVG(ESG_Score) WITH SYNONYMS=('average_esg','avg_sustainability','mean_esg_score') COMMENT='Average ESG score for watchlist',
		
		-- Portfolio performance metrics (for watchlist holdings)
		HOLDINGS.WATCHLIST_MARKET_VALUE AS SUM(MarketValue_Base) WITH SYNONYMS=('watchlist_exposure','theme_exposure','total_value') COMMENT='Total market value of watchlist securities in portfolios',
		HOLDINGS.WATCHLIST_WEIGHT AS SUM(PortfolioWeight) WITH SYNONYMS=('watchlist_weight','theme_allocation','watchlist_percentage') COMMENT='Portfolio weight of watchlist securities'
	)
	COMMENT='Watchlist analytics for thematic investment analysis including ESG and AI themes'
"""
    
    try:
        session.sql(semantic_view_sql).collect()
        print("    ✅ WATCHLIST_ANALYTICS_SV created successfully")
    except Exception as e:
        print(f"    ❌ Failed to create WATCHLIST_ANALYTICS_SV: {e}")
        raise

def validate_watchlist_analytics_sv(session: Session):
    """Validate the watchlist semantic view"""
    
    print("    → Validating WATCHLIST_ANALYTICS_SV...")
    
    try:
        # Test watchlist analysis
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.WATCHLIST_ANALYTICS_SV
                METRICS SECURITY_COUNT, AVG_ESG_SCORE
                DIMENSIONS WATCHLISTNAME
            )
            ORDER BY AVG_ESG_SCORE DESC
        """).collect()
        print(f"    ✅ Watchlist analysis test: {len(result)} watchlists")
        
        # Test Carbon Negative Leaders specific query
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.WATCHLIST_ANALYTICS_SV
                METRICS SECURITY_COUNT
                DIMENSIONS WATCHLISTNAME, PRIMARYTICKER, LEGALNAME
            )
            WHERE WATCHLISTNAME = 'Carbon Negative Leaders'
        """).collect()
        print(f"    ✅ Carbon Negative Leaders test: {len(result)} securities")
        
    except Exception as e:
        print(f"    ❌ Watchlist semantic view validation failed: {e}")