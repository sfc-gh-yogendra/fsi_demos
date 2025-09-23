"""
Glacier First Bank Demo - Semantic Views Creator

Creates semantic views for Cortex Analyst supporting Phase 1 scenarios.
Each semantic view is defined in its own function for better modularity.
"""

import logging
from typing import List, Set
from snowflake.snowpark import Session

import config

logger = logging.getLogger(__name__)


def validate_table_exists(session: Session, table_name: str, schema: str = "RAW_DATA") -> bool:
    """Check if a specific table exists in the database."""
    try:
        result = session.sql(f"""
            SELECT COUNT(*) as cnt 
            FROM INFORMATION_SCHEMA.TABLES 
            WHERE TABLE_SCHEMA = '{schema}' 
            AND TABLE_NAME = '{table_name}'
            AND TABLE_CATALOG = '{config.SNOWFLAKE['database']}'
        """).collect()
        
        return result[0]['CNT'] > 0
        
    except Exception as e:
        logger.error(f"Error checking table existence for {schema}.{table_name}: {e}")
        return False


def validate_required_tables(session: Session, required_tables: List[str], schema: str = "RAW_DATA") -> None:
    """Validate that all required tables exist, raise error if any are missing."""
    missing_tables = []
    
    for table_name in required_tables:
        if not validate_table_exists(session, table_name, schema):
            missing_tables.append(f"{schema}.{table_name}")
    
    if missing_tables:
        missing_str = ", ".join(missing_tables)
        raise RuntimeError(f"Required tables do not exist: {missing_str}. "
                         f"Please run data generation first with --scope data or --scope all")


def get_required_tables_for_scenarios(scenarios: List[str]) -> Set[str]:
    """Get the set of required tables for the given scenarios."""
    required_tables = set()
    
    # Base tables needed for all scenarios
    required_tables.update(['ENTITIES', 'CUSTOMERS'])
    
    if 'aml_kyc_edd' in scenarios:
        required_tables.update([
            'TRANSACTIONS',
            'COMPLIANCE_DOCUMENTS'
        ])
    
    if 'credit_analysis' in scenarios:
        required_tables.update([
            'LOAN_APPLICATIONS',
            'HISTORICAL_LOANS',
            'CREDIT_POLICY_DOCUMENTS'
        ])
    
    return required_tables


def create_all_semantic_views(session: Session, scenarios: List[str] = None) -> None:
    """Create all semantic views for the specified scenarios."""
    logger.info("Creating semantic views...")
    
    # Set database and warehouse context
    session.sql(f"USE DATABASE {config.SNOWFLAKE['database']}").collect()
    session.sql(f"USE WAREHOUSE {config.SNOWFLAKE['compute_warehouse']}").collect()
    
    # Validate required tables exist before creating semantic views
    scenarios = scenarios or config.get_all_scenarios()
    required_tables = list(get_required_tables_for_scenarios(scenarios))
    
    logger.info(f"Validating required tables: {required_tables}")
    validate_required_tables(session, required_tables)
    logger.info("Table validation completed successfully")
    
    # Create supporting views first
    create_customer_risk_view(session)
    create_customer_transaction_summary_view(session)
    
    # Create semantic views based on scenarios
    if 'aml_kyc_edd' in scenarios:
        create_aml_kyc_risk_semantic_view(session)
    
    if 'credit_analysis' in scenarios:
        create_credit_risk_semantic_view(session)
    
    # Create cross-domain intelligence semantic view for ecosystem analysis
    # This supports both AML and credit scenarios
    if any(scenario in scenarios for scenario in ['aml_kyc_edd', 'credit_analysis']):
        create_cross_domain_intelligence_semantic_view(session)
    
    logger.info("All semantic views created successfully")


def create_customer_risk_view(session: Session) -> None:
    """Create customer risk view for AML/KYC semantic view."""
    logger.info("Creating customer risk view...")
    
    # Validate required tables exist
    validate_required_tables(session, ['CUSTOMERS', 'ENTITIES'])
    
    session.sql(f"""
        CREATE OR REPLACE VIEW {config.SNOWFLAKE['database']}.CURATED_DATA.customer_risk_view AS
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
        FROM {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS c
        JOIN {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES e ON c.ENTITY_ID = e.ENTITY_ID
    """).collect()
    
    logger.info("Customer risk view created successfully")


def create_customer_transaction_summary_view(session: Session) -> None:
    """Create customer transaction summary view for AML/KYC semantic view."""
    logger.info("Creating customer transaction summary view...")
    
    # Validate required tables exist
    validate_required_tables(session, ['TRANSACTIONS'])
    
    session.sql(f"""
        CREATE OR REPLACE VIEW {config.SNOWFLAKE['database']}.CURATED_DATA.customer_transaction_summary_view AS
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
        FROM {config.SNOWFLAKE['database']}.RAW_DATA.TRANSACTIONS t
        GROUP BY t.CUSTOMER_ID
    """).collect()
    
    logger.info("Customer transaction summary view created successfully")


def create_aml_kyc_risk_semantic_view(session: Session) -> None:
    """Create AML/KYC risk semantic view for enhanced due diligence monitoring."""
    logger.info("Creating AML/KYC risk semantic view...")
    
    session.sql(f"""
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.SEMANTIC_LAYER.aml_kyc_risk_sv
        TABLES (
            customer_risk AS {config.SNOWFLAKE['database']}.CURATED_DATA.customer_risk_view
                PRIMARY KEY (CUSTOMER_ID)
                COMMENT='Customer AML risk profiles with entity names',
            
            transaction_summary AS {config.SNOWFLAKE['database']}.CURATED_DATA.customer_transaction_summary_view
                PRIMARY KEY (CUSTOMER_ID)
                COMMENT='Customer transaction activity summary for AML monitoring'
        )
        RELATIONSHIPS (
            customer_to_transactions AS customer_risk(CUSTOMER_ID) REFERENCES transaction_summary(CUSTOMER_ID)
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
                COMMENT='Largest single transaction amount in {config.CURRENCY}',
            
            transaction_summary.largest_suspicious_amount AS largest_suspicious_amount
                WITH SYNONYMS=('biggest suspicious transaction', 'largest flagged amount')
                COMMENT='Largest suspicious transaction amount in {config.CURRENCY}',
            
            transaction_summary.large_transactions_count AS large_transactions_count
                WITH SYNONYMS=('large transaction count', 'high value transactions')
                COMMENT='Number of transactions over €1M threshold',
            
            transaction_summary.recent_transactions_count AS recent_transactions_count
                WITH SYNONYMS=('recent activity count', 'current month transactions')
                COMMENT='Number of transactions in the last 30 days',
            
            transaction_summary.recent_deposits_total AS recent_deposits_total
                WITH SYNONYMS=('recent deposit amount', 'current deposits', 'latest funding')
                COMMENT='Total amount of deposits received in the last 30 days in {config.CURRENCY}',
            
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
        COMMENT='AML/KYC risk analysis view for enhanced due diligence monitoring with entity names and transaction activity'
    """).collect()
    
    logger.info("AML/KYC risk semantic view created successfully")


def create_credit_risk_semantic_view(session: Session) -> None:
    """Create credit risk semantic view for loan applications analysis."""
    logger.info("Creating credit risk semantic view...")
    
    # Validate required tables exist
    validate_required_tables(session, ['LOAN_APPLICATIONS'])
    
    session.sql(f"""
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.SEMANTIC_LAYER.credit_risk_sv
        TABLES (
            loan_apps AS {config.SNOWFLAKE['database']}.RAW_DATA.LOAN_APPLICATIONS
                PRIMARY KEY (APPLICATION_ID)
                COMMENT='Current loan applications under review'
        )
        FACTS (
            loan_apps.REQUESTED_AMOUNT AS requested_amount 
                WITH SYNONYMS=('loan amount', 'credit amount', 'funding request')
                COMMENT='Amount of credit requested in {config.CURRENCY}',
            
            loan_apps.ANNUAL_REVENUE AS annual_revenue
                WITH SYNONYMS=('yearly revenue', 'company revenue', 'turnover')
                COMMENT='Applicant annual revenue in {config.CURRENCY}',
                
            loan_apps.TOTAL_ASSETS AS total_assets
                WITH SYNONYMS=('company assets', 'total balance sheet assets')
                COMMENT='Total assets of the applicant in {config.CURRENCY}',
                
            loan_apps.TOTAL_LIABILITIES AS total_liabilities
                WITH SYNONYMS=('company debt', 'total debt', 'liabilities')
                COMMENT='Total liabilities of the applicant in {config.CURRENCY}',
                
            loan_apps.EBITDA AS ebitda
                WITH SYNONYMS=('earnings before interest tax depreciation amortization', 'operating income')
                COMMENT='EBITDA of the applicant in {config.CURRENCY}',
                
            loan_apps.DEBT_SERVICE_COVERAGE_RATIO AS debt_service_coverage_ratio
                WITH SYNONYMS=('DSCR', 'debt coverage ratio', 'cash flow coverage')
                COMMENT='Debt Service Coverage Ratio (cash flow / debt service)',
            
            loan_apps.DEBT_TO_EQUITY_RATIO AS debt_to_equity_ratio
                WITH SYNONYMS=('D/E ratio', 'leverage ratio', 'debt equity ratio')
                COMMENT='Debt-to-Equity ratio (total debt / equity)',
            
            loan_apps.CURRENT_RATIO AS current_ratio
                WITH SYNONYMS=('liquidity ratio', 'working capital ratio')
                COMMENT='Current ratio for liquidity assessment (current assets / current liabilities)',
                
            loan_apps.SINGLE_CLIENT_CONCENTRATION_PCT AS single_client_concentration_pct
                WITH SYNONYMS=('client concentration', 'customer concentration percentage', 'revenue concentration')
                COMMENT='Percentage of revenue from largest client (concentration risk)',
                
            loan_apps.TERM_MONTHS AS term_months
                WITH SYNONYMS=('loan term', 'maturity period', 'repayment period')
                COMMENT='Loan term in months'
        )
        DIMENSIONS (
            loan_apps.APPLICATION_ID AS application_id
                WITH SYNONYMS=('app id', 'application number', 'loan application id')
                COMMENT='Unique loan application identifier',
                
            loan_apps.CUSTOMER_ID AS customer_id
                WITH SYNONYMS=('client id', 'borrower id')
                COMMENT='Customer identifier for the applicant',
            
            loan_apps.APPLICANT_NAME AS applicant_name
                WITH SYNONYMS=('borrower name', 'company name', 'client name')
                COMMENT='Name of the loan applicant',
            
            loan_apps.INDUSTRY_SECTOR AS industry_sector
                WITH SYNONYMS=('industry', 'business sector', 'sector classification')
                COMMENT='Industry classification of the applicant',
                
            loan_apps.APPLICATION_STATUS AS application_status
                WITH SYNONYMS=('loan status', 'application state', 'review status')
                COMMENT='Current status of the loan application',
                
            loan_apps.LOAN_PURPOSE AS loan_purpose
                WITH SYNONYMS=('use of funds', 'funding purpose', 'credit purpose')
                COMMENT='Intended use of the loan proceeds',
                
            loan_apps.APPLICATION_DATE AS application_date
                WITH SYNONYMS=('submission date', 'application submission date')
                COMMENT='Date when the loan application was submitted',
                
            loan_apps.CURRENCY AS currency
                WITH SYNONYMS=('loan currency', 'currency code')
                COMMENT='Currency of the loan request'
        )
        COMMENT='Credit risk analysis view for loan applications with financial ratios and risk metrics'
    """).collect()
    
    logger.info("Credit risk semantic view created successfully")


def create_cross_domain_intelligence_semantic_view(session: Session) -> None:
    """Create cross-domain intelligence semantic view for ecosystem analysis."""
    logger.info("Creating cross-domain intelligence semantic view...")
    
    # Validate required tables exist
    validate_required_tables(session, ['ENTITIES', 'ENTITY_RELATIONSHIPS'])
    
    session.sql(f"""
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.SEMANTIC_LAYER.cross_domain_intelligence_sv
        TABLES (
            entities AS {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES
                PRIMARY KEY (ENTITY_ID)
                COMMENT='Core entity information for cross-domain analysis',
            
            relationships AS {config.SNOWFLAKE['database']}.RAW_DATA.ENTITY_RELATIONSHIPS
                PRIMARY KEY (RELATIONSHIP_ID)
                COMMENT='Entity relationships for ecosystem analysis'
        )
        RELATIONSHIPS (
            entity_to_relationships AS entities(ENTITY_ID) REFERENCES relationships(PRIMARY_ENTITY_ID)
        )
        FACTS (
            relationships.RISK_IMPACT_SCORE AS risk_impact_score
                WITH SYNONYMS=('risk impact', 'relationship risk', 'contagion risk')
                COMMENT='Risk impact score of the relationship (0-1 scale)',
            
            entities.ANNUAL_REVENUE AS annual_revenue
                WITH SYNONYMS=('yearly revenue', 'company revenue', 'turnover')
                COMMENT='Annual revenue of the entity in {config.CURRENCY}'
        )
        DIMENSIONS (
            entities.ENTITY_ID AS entity_id
                WITH SYNONYMS=('company id', 'entity identifier')
                COMMENT='Unique entity identifier',
            
            entities.ENTITY_NAME AS entity_name
                WITH SYNONYMS=('company name', 'organization name')
                COMMENT='Legal entity name',
            
            entities.INDUSTRY_SECTOR AS industry_sector
                WITH SYNONYMS=('industry', 'business sector', 'sector')
                COMMENT='Industry classification of the entity',
            
            entities.COUNTRY_CODE AS country_code
                WITH SYNONYMS=('country', 'jurisdiction', 'location')
                COMMENT='Country code where entity is incorporated',
            
            relationships.RELATIONSHIP_TYPE AS relationship_type
                WITH SYNONYMS=('connection type', 'business relationship')
                COMMENT='Type of business relationship (SUPPLIER, CUSTOMER, VENDOR, etc.)',
            
            relationships.RELATED_ENTITY_ID AS related_entity_id
                WITH SYNONYMS=('connected entity', 'relationship target')
                COMMENT='Entity ID of the related entity in the relationship'
        )
        COMMENT='Cross-domain intelligence view for ecosystem analysis and risk contagion modeling'
    """).collect()
    
    logger.info("Cross-domain intelligence semantic view created successfully")


def main():
    """Main function for testing semantic views creation."""
    print("Semantic views creator module loaded successfully")
    print("Use create_all_semantic_views() method to create semantic views")


if __name__ == "__main__":
    main()
