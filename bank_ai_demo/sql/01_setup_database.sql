-- Glacier First Bank AI Intelligence Demo - Database Setup
-- Creates database, schemas, warehouses, and core infrastructure
-- Note: Tables are created automatically by Snowpark data generation

-- =============================================================================
-- DATABASE AND SCHEMA SETUP
-- =============================================================================

-- Create main database
CREATE OR REPLACE DATABASE BANK_AI_DEMO
    COMMENT = 'Glacier First Bank AI Intelligence Demo - Phase 1 Foundation';

-- Create schemas
CREATE OR REPLACE SCHEMA BANK_AI_DEMO.RAW_DATA
    COMMENT = 'Raw data tables for entities, transactions, documents';

CREATE OR REPLACE SCHEMA BANK_AI_DEMO.CURATED_DATA
    COMMENT = 'Curated and processed data for analytics';

CREATE OR REPLACE SCHEMA BANK_AI_DEMO.SEMANTIC_LAYER
    COMMENT = 'Semantic views for Cortex Analyst';

CREATE OR REPLACE SCHEMA BANK_AI_DEMO.AGENT_FRAMEWORK
    COMMENT = 'Cortex Search services and agent configurations';

-- =============================================================================
-- WAREHOUSE SETUP
-- =============================================================================

-- Create compute warehouse for general processing
CREATE OR REPLACE WAREHOUSE BANK_AI_DEMO_COMPUTE_WH
    WITH WAREHOUSE_SIZE = 'MEDIUM'
    AUTO_SUSPEND = 300
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'General compute warehouse for Glacier First Bank demo';

-- Create search warehouse for Cortex Search services
CREATE OR REPLACE WAREHOUSE BANK_AI_DEMO_SEARCH_WH
    WITH WAREHOUSE_SIZE = 'SMALL'
    AUTO_SUSPEND = 180
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Dedicated warehouse for Cortex Search services';

-- Set default warehouse
USE WAREHOUSE BANK_AI_DEMO_COMPUTE_WH;
USE DATABASE BANK_AI_DEMO;

-- =============================================================================
-- EXTERNAL DATA SIMULATION TABLES (Marketplace Attribution)
-- =============================================================================

-- S&P Global Market Intelligence simulation
CREATE OR REPLACE TABLE BANK_AI_DEMO.RAW_DATA.SP_GLOBAL_COMPANY_FINANCIALS (
    COMPANY_ID VARCHAR(50) PRIMARY KEY,
    COMPANY_NAME VARCHAR(200) NOT NULL,
    TICKER_SYMBOL VARCHAR(20),
    COUNTRY_CODE VARCHAR(3) NOT NULL,
    INDUSTRY_CODE INTEGER,
    FISCAL_YEAR INTEGER NOT NULL,
    FISCAL_PERIOD VARCHAR(10) NOT NULL, -- 'Q1', 'Q2', 'Q3', 'Q4', 'FY'
    REVENUE DECIMAL(18,2),
    EBITDA DECIMAL(18,2),
    NET_INCOME DECIMAL(18,2),
    TOTAL_ASSETS DECIMAL(18,2),
    TOTAL_DEBT DECIMAL(18,2),
    SHAREHOLDERS_EQUITY DECIMAL(18,2),
    OPERATING_CASH_FLOW DECIMAL(18,2),
    CAPEX DECIMAL(18,2),
    CURRENCY VARCHAR(3) DEFAULT 'EUR',
    REPORT_DATE DATE,
    DATA_SOURCE VARCHAR(100) DEFAULT 'S&P Global Market Intelligence via Snowflake Marketplace',
    LAST_UPDATED TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
COMMENT = 'S&P Global Market Intelligence financial data simulation';

-- Reuters News Feed simulation
CREATE OR REPLACE TABLE BANK_AI_DEMO.RAW_DATA.REUTERS_NEWS_FEED (
    ARTICLE_ID VARCHAR(50) PRIMARY KEY,
    HEADLINE VARCHAR(500) NOT NULL,
    BODY_TEXT TEXT,
    PUBLISH_DATETIME TIMESTAMP_NTZ NOT NULL,
    AUTHOR VARCHAR(200),
    CATEGORY VARCHAR(100),
    REGION VARCHAR(100),
    LANGUAGE VARCHAR(10) DEFAULT 'en',
    SENTIMENT_SCORE DECIMAL(3,2), -- -1.00 to 1.00
    RELEVANCE_ENTITIES TEXT, -- JSON array of entity names
    TAGS TEXT, -- JSON array of tags
    SOURCE_URL VARCHAR(500),
    DATA_SOURCE VARCHAR(100) DEFAULT 'Reuters News Feed via Snowflake Marketplace',
    INGESTION_TIME TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
COMMENT = 'Reuters news feed simulation for adverse media screening';

-- Dow Jones Risk & Compliance PEP database simulation
CREATE OR REPLACE TABLE BANK_AI_DEMO.RAW_DATA.DJ_RISK_PEP_DATABASE (
    PEP_ID VARCHAR(50) PRIMARY KEY,
    FULL_NAME VARCHAR(200) NOT NULL,
    ALIASES TEXT, -- JSON array of alternative names
    DATE_OF_BIRTH DATE,
    PLACE_OF_BIRTH VARCHAR(200),
    NATIONALITY VARCHAR(100),
    POSITION_TITLE VARCHAR(200),
    ORGANIZATION VARCHAR(200),
    COUNTRY_OF_POSITION VARCHAR(100),
    POSITION_START_DATE DATE,
    POSITION_END_DATE DATE,
    PEP_CATEGORY VARCHAR(50), -- 'Government Official', 'Family Member', 'Close Associate'
    RISK_LEVEL VARCHAR(20), -- 'Low', 'Medium', 'High'
    FAMILY_MEMBERS TEXT, -- JSON array of family member objects
    ASSOCIATES TEXT, -- JSON array of associate objects
    DATA_SOURCE VARCHAR(100) DEFAULT 'Dow Jones Risk & Compliance via Snowflake Marketplace',
    LAST_UPDATED TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
)
COMMENT = 'Dow Jones PEP database simulation for enhanced due diligence';

-- =============================================================================
-- PERFORMANCE OPTIMIZATION
-- =============================================================================

-- Note: Tables created by Snowpark will have clustering keys added after creation
-- This is handled in the data generation process

-- =============================================================================
-- COMPLETION MESSAGE
-- =============================================================================

SELECT 'Database infrastructure setup completed successfully!' AS STATUS;