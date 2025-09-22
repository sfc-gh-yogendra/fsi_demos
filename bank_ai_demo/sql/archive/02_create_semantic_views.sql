-- Glacier First Bank AI Intelligence Demo - Semantic Views
-- Creates semantic views for Cortex Analyst supporting Phase 1 scenarios
-- IMPORTANT: Only run after all referenced tables exist

USE DATABASE BANK_AI_DEMO;
USE WAREHOUSE BANK_AI_DEMO_COMPUTE_WH;

-- =============================================================================
-- CUSTOMER RISK VIEW (FOR AML/KYC SEMANTIC VIEW)
-- =============================================================================

CREATE OR REPLACE VIEW BANK_AI_DEMO.CURATED_DATA.customer_risk_view AS
SELECT 
    c.CUSTOMER_ID,
    c.ENTITY_ID,
    e.ENTITY_NAME,
    c.CUSTOMER_TYPE,
    c.ONBOARDING_DATE,
    c.RISK_RATING,
    c.KYC_STATUS,
    c.LAST_REVIEW_DATE,
    c.NEXT_REVIEW_DATE,
    c.RELATIONSHIP_MANAGER,
    c.AML_FLAGS,
    c.CREATED_DATE
FROM BANK_AI_DEMO.RAW_DATA.CUSTOMERS c
JOIN BANK_AI_DEMO.RAW_DATA.ENTITIES e ON c.ENTITY_ID = e.ENTITY_ID;

-- =============================================================================
-- CUSTOMER TRANSACTION SUMMARY VIEW (FOR AML/KYC SEMANTIC VIEW)
-- =============================================================================

CREATE OR REPLACE VIEW BANK_AI_DEMO.CURATED_DATA.customer_transaction_summary_view AS
SELECT 
    t.CUSTOMER_ID,
    COUNT(*) AS total_transactions,
    COUNT(CASE WHEN t.SUSPICIOUS_ACTIVITY_FLAG = TRUE THEN 1 END) AS suspicious_transactions,
    MAX(t.AMOUNT) AS largest_transaction_amount,
    MAX(CASE WHEN t.SUSPICIOUS_ACTIVITY_FLAG = TRUE THEN t.AMOUNT END) AS largest_suspicious_amount,
    MAX(CASE WHEN t.AMOUNT >= 1000000 THEN t.TRANSACTION_DATE END) AS latest_large_transaction_date,
    MAX(CASE WHEN t.SUSPICIOUS_ACTIVITY_FLAG = TRUE THEN t.TRANSACTION_DATE END) AS latest_suspicious_transaction_date,
    AVG(t.RISK_SCORE) AS avg_risk_score,
    COUNT(CASE WHEN t.AMOUNT >= 1000000 THEN 1 END) AS large_transactions_count,
    COUNT(CASE WHEN t.TRANSACTION_DATE >= DATEADD(day, -30, CURRENT_DATE()) THEN 1 END) AS recent_transactions_count,
    SUM(CASE WHEN t.TRANSACTION_TYPE = 'CREDIT' AND t.TRANSACTION_DATE >= DATEADD(day, -30, CURRENT_DATE()) THEN t.AMOUNT END) AS recent_deposits_total
FROM BANK_AI_DEMO.RAW_DATA.TRANSACTIONS t
GROUP BY t.CUSTOMER_ID;

-- =============================================================================
-- AML/KYC RISK SEMANTIC VIEW
-- =============================================================================

CREATE OR REPLACE SEMANTIC VIEW BANK_AI_DEMO.SEMANTIC_LAYER.aml_kyc_risk_sv
TABLES (
    customer_risk AS BANK_AI_DEMO.CURATED_DATA.customer_risk_view
        PRIMARY KEY (CUSTOMER_ID)
        COMMENT='Customer AML risk profiles with entity names',
    
    transaction_summary AS BANK_AI_DEMO.CURATED_DATA.customer_transaction_summary_view
        PRIMARY KEY (CUSTOMER_ID)
        COMMENT='Customer transaction activity summary for AML monitoring'
)
RELATIONSHIPS (
    customer_risk.CUSTOMER_ID = transaction_summary.CUSTOMER_ID
)
FACTS (
    customer_risk.AML_FLAGS AS aml_flags
        WITH SYNONYMS=('aml flag count', 'risk flags', 'suspicious flags')
        COMMENT='Number of AML risk flags raised (0-5 scale)',
    
    transaction_summary.total_transactions AS total_transactions
        WITH SYNONYMS=('transaction count', 'number of transactions')
        COMMENT='Total number of transactions for the customer',
    
    transaction_summary.suspicious_transactions AS suspicious_transactions
        WITH SYNONYMS=('flagged transactions', 'suspicious activity count')
        COMMENT='Number of transactions flagged for suspicious activity',
    
    transaction_summary.largest_transaction_amount AS largest_transaction_amount
        WITH SYNONYMS=('biggest transaction', 'maximum amount', 'largest deposit')
        COMMENT='Largest single transaction amount in EUR',
    
    transaction_summary.largest_suspicious_amount AS largest_suspicious_amount
        WITH SYNONYMS=('biggest suspicious transaction', 'largest flagged amount')
        COMMENT='Largest suspicious transaction amount in EUR',
    
    transaction_summary.large_transactions_count AS large_transactions_count
        WITH SYNONYMS=('large transaction count', 'high value transactions')
        COMMENT='Number of transactions over €1M threshold',
    
    transaction_summary.recent_transactions_count AS recent_transactions_count
        WITH SYNONYMS=('recent activity count', 'current month transactions')
        COMMENT='Number of transactions in the last 30 days',
    
    transaction_summary.recent_deposits_total AS recent_deposits_total
        WITH SYNONYMS=('recent deposit amount', 'current deposits', 'latest funding')
        COMMENT='Total amount of deposits received in the last 30 days in EUR',
    
    transaction_summary.avg_risk_score AS avg_risk_score
        WITH SYNONYMS=('average risk', 'transaction risk level')
        COMMENT='Average risk score across all transactions (0-1 scale)'
)
DIMENSIONS (
    customer_risk.CUSTOMER_ID AS customer_id
        WITH SYNONYMS=('client id', 'customer identifier')
        COMMENT='Unique customer identifier',
    
    customer_risk.ENTITY_NAME AS entity_name
        WITH SYNONYMS=('company name', 'organization name', 'client name')
        COMMENT='Legal entity name for customer identification',
    
    customer_risk.ENTITY_ID AS entity_id
        WITH SYNONYMS=('entity identifier', 'company id')
        COMMENT='Associated entity identifier',
    
    customer_risk.RISK_RATING AS risk_rating
        WITH SYNONYMS=('risk level', 'customer risk', 'aml rating')
        COMMENT='Customer risk rating (LOW, MEDIUM, HIGH)',
    
    customer_risk.KYC_STATUS AS kyc_status
        WITH SYNONYMS=('kyc state', 'due diligence status')
        COMMENT='KYC completion status: COMPLETE (standard DD completed), PENDING (documentation in progress), REQUIRES_EDD (Enhanced Due Diligence needed)',
    
    customer_risk.CUSTOMER_TYPE AS customer_type
        WITH SYNONYMS=('client type', 'customer classification')
        COMMENT='Type of customer relationship',
    
    transaction_summary.latest_large_transaction_date AS latest_large_transaction_date
        WITH SYNONYMS=('recent large transaction date', 'latest high value transaction')
        COMMENT='Date of the most recent transaction over €1M',
    
    transaction_summary.latest_suspicious_transaction_date AS latest_suspicious_transaction_date
        WITH SYNONYMS=('recent suspicious activity date', 'latest flagged transaction')
        COMMENT='Date of the most recent suspicious transaction'
)
COMMENT='AML/KYC risk analysis view for enhanced due diligence monitoring with entity names and transaction activity';

-- =============================================================================
-- CREDIT RISK SEMANTIC VIEW (SIMPLIFIED)
-- =============================================================================

CREATE OR REPLACE SEMANTIC VIEW BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
TABLES (
    loan_apps AS BANK_AI_DEMO.RAW_DATA.LOAN_APPLICATIONS
        PRIMARY KEY (APPLICATION_ID)
        COMMENT='Current loan applications under review'
)
FACTS (
    loan_apps.REQUESTED_AMOUNT AS requested_amount 
        COMMENT='Amount of credit requested in EUR',
    
    loan_apps.ANNUAL_REVENUE AS annual_revenue
        COMMENT='Applicant annual revenue in EUR',
        
    loan_apps.DEBT_SERVICE_COVERAGE_RATIO AS debt_service_coverage_ratio
        COMMENT='Debt Service Coverage Ratio',
    
    loan_apps.DEBT_TO_EQUITY_RATIO AS debt_to_equity_ratio
        COMMENT='Debt-to-Equity ratio',
    
    loan_apps.CURRENT_RATIO AS current_ratio
        COMMENT='Current ratio for liquidity assessment'
)
DIMENSIONS (
    loan_apps.APPLICANT_NAME AS applicant_name
        COMMENT='Name of the loan applicant',
    
    loan_apps.INDUSTRY_SECTOR AS industry_sector
        COMMENT='Industry classification of the applicant',
        
    loan_apps.APPLICATION_STATUS AS application_status
        COMMENT='Current status of the loan application'
)
COMMENT='Credit risk analysis view for loan applications';

COMMIT;