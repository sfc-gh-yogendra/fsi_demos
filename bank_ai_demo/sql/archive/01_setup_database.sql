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
-- DATA TABLES NOTE
-- =============================================================================

-- All data tables are created during data generation using Snowpark save_as_table()
-- This eliminates duplicate table creation and ensures schema consistency

-- =============================================================================
-- COMPLETION MESSAGE
-- =============================================================================

SELECT 'Database infrastructure setup completed successfully!' AS STATUS;