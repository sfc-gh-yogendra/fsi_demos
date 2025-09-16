"""
WAM AI Demo - Database and Schema Setup
Sets up the foundational database structure following the enhanced model
"""

from snowflake.snowpark import Session
import config

def setup_database_and_schemas(session: Session):
    """Set up database, schemas, and warehouses"""
    
    print("  → Creating database and schemas...")
    
    # Create database
    session.sql(f"CREATE DATABASE IF NOT EXISTS {config.DATABASE_NAME}").collect()
    session.sql(f"USE DATABASE {config.DATABASE_NAME}").collect()
    
    # Create schemas following the organization pattern
    schemas = ['RAW', 'CURATED', 'AI']
    for schema in schemas:
        session.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}").collect()
        print(f"    ✅ Schema: {schema}")
    
    # Create warehouses
    warehouses = [config.BUILD_WAREHOUSE, config.CORTEX_WAREHOUSE]
    for warehouse in warehouses:
        session.sql(f"""
            CREATE WAREHOUSE IF NOT EXISTS {warehouse}
            WITH WAREHOUSE_SIZE = 'MEDIUM'
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
            INITIALLY_SUSPENDED = TRUE
        """).collect()
        print(f"    ✅ Warehouse: {warehouse}")
    
    # Set active warehouse for build operations
    session.sql(f"USE WAREHOUSE {config.BUILD_WAREHOUSE}").collect()
    
    # Create stage for PDFs
    session.sql(f"""
        CREATE STAGE IF NOT EXISTS {config.CLIENT_DOCS_STAGE}
        COMMENT = 'Stage for AI-generated client onboarding documents'
    """).collect()
    print(f"    ✅ Stage: {config.CLIENT_DOCS_STAGE}")
    
    print("  ✅ Database setup complete")

def create_foundation_tables(session: Session):
    """Create all foundation tables in dependency order"""
    
    print("  → Creating foundation tables...")
    
    # Step 1: Create dimension tables (no dependencies)
    create_dim_manager(session)
    create_dim_advisor(session)
    create_dim_client(session)
    create_dim_issuer(session)
    create_dim_portfolio(session)
    create_dim_benchmark(session)
    
    # Step 2: Create security dimension with cross-reference (depends on issuers)
    create_dim_security(session)
    create_dim_security_identifier_xref(session)
    create_dim_account(session)
    
    # Step 3: Create fact tables (depend on dimensions)
    create_fact_transaction(session)
    create_fact_position_daily_abor(session)
    create_fact_marketdata_timeseries(session)
    create_fact_advisor_client_relationship(session)
    
    # Step 4: Create corpus tables
    create_corpus_tables(session)
    
    # Step 5: Create advisor benchmarking summary tables
    create_advisor_roster(session)
    create_advisor_summary_ttm(session)
    create_departure_corpus(session)
    
    print("  ✅ Foundation tables created")

def create_dim_manager(session: Session):
    """Create manager dimension table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_MANAGER (
            ManagerID BIGINT IDENTITY(1,1) PRIMARY KEY,
            ManagerName VARCHAR(100),
            ManagerTitle VARCHAR(100),
            StartDate DATE,
            ActiveFlag BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_dim_advisor(session: Session):
    """Create advisor dimension table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_ADVISOR (
            AdvisorID BIGINT IDENTITY(1,1) PRIMARY KEY,
            ManagerID BIGINT,
            FirstName VARCHAR(100),
            LastName VARCHAR(100),
            Email VARCHAR(255),
            Team VARCHAR(100),
            IsActive BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_dim_client(session: Session):
    """Create client dimension table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_CLIENT (
            ClientID BIGINT IDENTITY(1,1) PRIMARY KEY,
            AdvisorID BIGINT NOT NULL,
            FirstName VARCHAR(100),
            LastName VARCHAR(100),
            Email VARCHAR(255),
            Phone VARCHAR(50),
            DateOfBirth DATE,
            RiskTolerance VARCHAR(50),
            InvestmentHorizon VARCHAR(50),
            OnboardingDate DATE,
            EndDate DATE,
            DepartureReason VARCHAR(50),
            DepartureNotes TEXT,
            IsActive BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_dim_issuer(session: Session):
    """Create issuer dimension with corporate hierarchy"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_ISSUER (
            IssuerID BIGINT IDENTITY(1,1) PRIMARY KEY,
            UltimateParentIssuerID BIGINT,
            LegalName VARCHAR(255) NOT NULL,
            LEI VARCHAR(20),
            CountryOfIncorporation CHAR(2),
            GICS_Sector VARCHAR(100)
        )
    """).collect()

def create_dim_security(session: Session):
    """Create security master dimension with immutable SecurityID"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_SECURITY (
            SecurityID BIGINT IDENTITY(1,1) PRIMARY KEY,
            IssuerID BIGINT NOT NULL,
            PrimaryTicker VARCHAR(50),
            Description VARCHAR(255),
            AssetClass VARCHAR(50),
            SecurityType VARCHAR(100),
            CountryOfRisk CHAR(2),
            IssueDate DATE,
            MaturityDate DATE,
            CouponRate DECIMAL(18, 8),
            RecordStartDate TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
            RecordEndDate TIMESTAMP_NTZ DEFAULT '2099-12-31 23:59:59'::TIMESTAMP_NTZ,
            IsActive BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_dim_security_identifier_xref(session: Session):
    """Create security identifier cross-reference table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_SECURITY_IDENTIFIER_XREF (
            SecurityIdentifierID BIGINT IDENTITY(1,1) PRIMARY KEY,
            SecurityID BIGINT NOT NULL,
            IdentifierType VARCHAR(50) NOT NULL,
            IdentifierValue VARCHAR(100) NOT NULL,
            EffectiveStartDate DATE NOT NULL,
            EffectiveEndDate DATE NOT NULL,
            IsPrimaryForType BOOLEAN DEFAULT FALSE
        )
    """).collect()

def create_dim_portfolio(session: Session):
    """Create portfolio dimension table with AccountID foreign key"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO (
            PortfolioID BIGINT IDENTITY(1,1) PRIMARY KEY,
            AccountID VARCHAR(50) NOT NULL,
            PortfolioCode VARCHAR(100) UNIQUE NOT NULL,
            PortfolioName VARCHAR(255),
            Strategy VARCHAR(100),
            BaseCurrency CHAR(3) DEFAULT 'USD',
            InceptionDate DATE,
            IsActive BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_dim_benchmark(session: Session):
    """Create benchmark dimension table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_BENCHMARK (
            BenchmarkID BIGINT IDENTITY(1,1) PRIMARY KEY,
            BenchmarkName VARCHAR(255) UNIQUE NOT NULL,
            Provider VARCHAR(100)
        )
    """).collect()

def create_dim_account(session: Session):
    """Create account dimension table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_ACCOUNT (
            AccountID VARCHAR(50) PRIMARY KEY,
            ClientID BIGINT NOT NULL,
            AccountType VARCHAR(50),
            ModelPortfolioName VARCHAR(255),
            OpenDate DATE,
            IsActive BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_fact_transaction(session: Session):
    """Create transaction log fact table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_TRANSACTION (
            TransactionID BIGINT IDENTITY(1,1) PRIMARY KEY,
            TransactionDate DATE NOT NULL,
            PortfolioID BIGINT NOT NULL,
            SecurityID BIGINT NOT NULL,
            TransactionType VARCHAR(50) NOT NULL,
            TradeDate DATE NOT NULL,
            SettleDate DATE,
            Quantity DECIMAL(38, 10),
            Price DECIMAL(38, 10),
            GrossAmount_Local DECIMAL(38, 10),
            Commission_Local DECIMAL(38, 10),
            Currency CHAR(3) DEFAULT 'USD',
            SourceSystem VARCHAR(50) DEFAULT 'ABOR'
        )
    """).collect()

def create_fact_position_daily_abor(session: Session):
    """Create ABOR positions fact table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR (
            HoldingDate DATE NOT NULL,
            PortfolioID BIGINT NOT NULL,
            SecurityID BIGINT NOT NULL,
            Quantity DECIMAL(38, 10),
            MarketValue_Local DECIMAL(38, 10),
            MarketValue_Base DECIMAL(38, 10),
            CostBasis_Local DECIMAL(38, 10),
            CostBasis_Base DECIMAL(38, 10),
            AccruedInterest_Local DECIMAL(38, 10),
            PortfolioWeight DECIMAL(18, 12),
            PRIMARY KEY (HoldingDate, PortfolioID, SecurityID)
        )
    """).collect()

def create_fact_marketdata_timeseries(session: Session):
    """Create market data time series fact table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_MARKETDATA_TIMESERIES (
            PriceDate DATE NOT NULL,
            SecurityID BIGINT NOT NULL,
            Price_Close DECIMAL(38, 10),
            Price_Open DECIMAL(38, 10),
            Price_High DECIMAL(38, 10),
            Price_Low DECIMAL(38, 10),
            Volume BIGINT,
            TotalReturnFactor_Daily DECIMAL(38, 15) DEFAULT 1.0,
            PRIMARY KEY (PriceDate, SecurityID)
        )
    """).collect()

def create_corpus_tables(session: Session):
    """Create document corpus tables"""
    
    # Communications Corpus
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS (
            COMMUNICATION_ID VARCHAR(100) PRIMARY KEY,
            CLIENT_ID BIGINT,
            ADVISOR_ID BIGINT,
            TIMESTAMP TIMESTAMP_NTZ,
            CHANNEL VARCHAR(50),
            SUBJECT VARCHAR(500),
            CONTENT TEXT,
            SENTIMENT_SCORE DECIMAL(3,2),
            RiskCategory VARCHAR(50),
            RiskSeverity VARCHAR(20),
            RiskFlags INTEGER DEFAULT 0
        )
    """).collect()
    
    # Research Corpus
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS (
            DOCUMENT_ID VARCHAR(100) PRIMARY KEY,
            DOCUMENT_TITLE VARCHAR(500),
            DOCUMENT_TYPE VARCHAR(100),
            TICKER VARCHAR(50),
            PUBLISH_DATE DATE,
            SOURCE VARCHAR(100),
            LANGUAGE VARCHAR(10) DEFAULT 'en',
            DOCUMENT_TEXT TEXT
        )
    """).collect()
    
    # Regulatory Corpus
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.REGULATORY_CORPUS (
            DOCUMENT_ID VARCHAR(100) PRIMARY KEY,
            REGULATOR VARCHAR(100),
            RULE_ID VARCHAR(50),
            TITLE VARCHAR(500),
            PUBLISH_DATE DATE,
            CONTENT TEXT
        )
    """).collect()

def create_fact_advisor_client_relationship(session: Session):
    """Create advisor-client relationship fact table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_ADVISOR_CLIENT_RELATIONSHIP (
            RelationshipID BIGINT IDENTITY(1,1) PRIMARY KEY,
            AdvisorID BIGINT NOT NULL,
            ClientID BIGINT NOT NULL,
            StartDate DATE NOT NULL,
            EndDate DATE,
            RelationshipStatus VARCHAR(20) DEFAULT 'Active'
        )
    """).collect()

def create_advisor_roster(session: Session):
    """Create advisor roster summary table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.ADVISOR_ROSTER (
            AdvisorID BIGINT PRIMARY KEY,
            AdvisorName VARCHAR(100),
            ManagerID BIGINT,
            ManagerName VARCHAR(100),
            TeamName VARCHAR(50),
            PeerGroup VARCHAR(20),
            StartDate DATE,
            ActiveFlag BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_advisor_summary_ttm(session: Session):
    """Create advisor summary TTM table"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.ADVISOR_SUMMARY_TTM (
            AdvisorID BIGINT,
            PeriodEndDate DATE,
            -- AUM & Flows
            StartingAUM DECIMAL(18,2),
            EndingAUM DECIMAL(18,2),
            Inflows DECIMAL(18,2),
            Outflows DECIMAL(18,2),
            NetFlows DECIMAL(18,2),
            -- Clients
            ClientsStart INTEGER,
            ClientsLost INTEGER,
            ClientsEnd INTEGER,
            AUMLostFromDepartures DECIMAL(18,2),
            -- Engagement
            InteractionsCount INTEGER,
            UniqueClientsContacted INTEGER,
            AvgDaysBetweenContacts DECIMAL(10,2),
            -- Sentiment
            PositivePct DECIMAL(5,2),
            NeutralPct DECIMAL(5,2),
            NegativePct DECIMAL(5,2),
            -- Planning
            PlanningHouseholds INTEGER,
            TotalHouseholds INTEGER,
            PlanningCoveragePct DECIMAL(5,2),
            -- Revenue
            AvgAUM_TTM DECIMAL(18,2),
            Revenue_TTM DECIMAL(18,2),
            -- Risk
            RiskFlags INTEGER,
            RiskFlagsPer100 DECIMAL(5,2),
            -- Peer Group
            PeerGroup VARCHAR(20),
            PRIMARY KEY (AdvisorID, PeriodEndDate)
        )
    """).collect()

def create_departure_corpus(session: Session):
    """Create departure corpus table for exit documents"""
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DEPARTURE_CORPUS (
            DocumentID VARCHAR(50) PRIMARY KEY,
            ClientID BIGINT,
            ClientName VARCHAR(100),
            AdvisorID BIGINT,
            AdvisorName VARCHAR(100),
            DocumentType VARCHAR(50),
            DocumentDate DATE,
            Title VARCHAR(200),
            DocumentText TEXT,
            DepartureReason VARCHAR(50),
            CreatedDate TIMESTAMP DEFAULT CURRENT_TIMESTAMP()
        )
    """).collect()

def create_client_interactions_view(session: Session):
    """Create client interactions view for CLIENT_INTERACTIONS_SV"""
    session.sql(f"""
        CREATE OR REPLACE VIEW {config.DATABASE_NAME}.CURATED.VW_CLIENT_INTERACTIONS AS
        SELECT 
            CLIENT_ID,
            ADVISOR_ID,
            CHANNEL,
            DATE(TIMESTAMP) as INTERACTION_DATE,
            COUNT(*) as COUNT_COMMUNICATIONS,
            AVG(CASE 
                WHEN CHANNEL IN ('Phone', 'Meeting') THEN 30 
                ELSE 5 
            END) as AVG_LENGTH_MINUTES,
            MAX(TIMESTAMP) as LAST_CONTACT_DATE
        FROM {config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS
        GROUP BY CLIENT_ID, ADVISOR_ID, CHANNEL, DATE(TIMESTAMP)
    """).collect()
