-- Glacier First Bank AI Intelligence Demo - Cortex Search Services
-- Creates search services for unstructured document analysis
-- IMPORTANT: Only run after document tables exist and are populated

USE DATABASE BANK_AI_DEMO;
USE WAREHOUSE BANK_AI_DEMO_SEARCH_WH;

-- =============================================================================
-- COMPLIANCE DOCUMENTS SEARCH SERVICE
-- =============================================================================

-- Create Cortex Search service for compliance documents (AML/KYC)
CREATE OR REPLACE CORTEX SEARCH SERVICE BANK_AI_DEMO.AGENT_FRAMEWORK.compliance_docs_search_svc
    ON CONTENT
    ATTRIBUTES ID, TITLE, ENTITY_NAME, DOC_TYPE, PUBLISH_DATE, RISK_SIGNAL
    WAREHOUSE = BANK_AI_DEMO_SEARCH_WH
    TARGET_LAG = '5 minutes'
    AS 
    SELECT 
        ID,
        TITLE,
        CONTENT,
        ENTITY_NAME,
        DOC_TYPE,
        PUBLISH_DATE,
        RISK_SIGNAL
    FROM BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENTS;

-- =============================================================================
-- CREDIT POLICY SEARCH SERVICE
-- =============================================================================

-- Create Cortex Search service for credit policy documents
CREATE OR REPLACE CORTEX SEARCH SERVICE BANK_AI_DEMO.AGENT_FRAMEWORK.credit_policy_search_svc
    ON CONTENT
    ATTRIBUTES ID, TITLE, POLICY_SECTION, EFFECTIVE_DATE
    WAREHOUSE = BANK_AI_DEMO_SEARCH_WH
    TARGET_LAG = '5 minutes'
    AS 
    SELECT 
        ID,
        TITLE,
        CONTENT,
        POLICY_SECTION,
        EFFECTIVE_DATE
    FROM BANK_AI_DEMO.RAW_DATA.CREDIT_POLICY_DOCUMENTS;

-- =============================================================================
-- LOAN DOCUMENTS SEARCH SERVICE
-- =============================================================================

-- Create Cortex Search service for loan application documents
CREATE OR REPLACE CORTEX SEARCH SERVICE BANK_AI_DEMO.AGENT_FRAMEWORK.loan_documents_search_svc
    ON CONTENT
    ATTRIBUTES ID, TITLE, APPLICANT_NAME, DOC_TYPE, DOCUMENT_SECTION
    WAREHOUSE = BANK_AI_DEMO_SEARCH_WH
    TARGET_LAG = '5 minutes'
    AS 
    SELECT 
        ID,
        TITLE,
        CONTENT,
        APPLICANT_NAME,
        DOC_TYPE,
        DOCUMENT_SECTION
    FROM BANK_AI_DEMO.RAW_DATA.LOAN_DOCUMENTS;

-- =============================================================================
-- NEWS AND RESEARCH SEARCH SERVICE
-- =============================================================================

-- Create Cortex Search service for news and research documents
CREATE OR REPLACE CORTEX SEARCH SERVICE BANK_AI_DEMO.AGENT_FRAMEWORK.news_research_search_svc
    ON CONTENT
    ATTRIBUTES ID, TITLE, ENTITY_NAME, ARTICLE_TYPE, PUBLISH_DATE
    WAREHOUSE = BANK_AI_DEMO_SEARCH_WH
    TARGET_LAG = '5 minutes'
    AS 
    SELECT 
        ID,
        TITLE,
        CONTENT,
        ENTITY_NAME,
        ARTICLE_TYPE,
        PUBLISH_DATE
    FROM BANK_AI_DEMO.RAW_DATA.NEWS_AND_RESEARCH;

-- =============================================================================
-- DOCUMENT TEMPLATES SEARCH SERVICE
-- =============================================================================

-- Create Cortex Search service for document templates (RFIs, credit memos, etc.)
CREATE OR REPLACE CORTEX SEARCH SERVICE BANK_AI_DEMO.AGENT_FRAMEWORK.document_templates_search_svc
    ON TEMPLATE_CONTENT
    ATTRIBUTES TEMPLATE_ID, TEMPLATE_NAME, TEMPLATE_TYPE, SCENARIO, USE_CASE, REGULATORY_FRAMEWORK, REQUIRED_VARIABLES
    WAREHOUSE = BANK_AI_DEMO_SEARCH_WH
    TARGET_LAG = '5 minutes'
    AS 
    SELECT 
        TEMPLATE_ID,
        TEMPLATE_NAME,
        TEMPLATE_CONTENT,
        TEMPLATE_TYPE,
        SCENARIO,
        USE_CASE,
        REGULATORY_FRAMEWORK,
        REQUIRED_VARIABLES
    FROM BANK_AI_DEMO.RAW_DATA.DOCUMENT_TEMPLATES;

COMMIT;