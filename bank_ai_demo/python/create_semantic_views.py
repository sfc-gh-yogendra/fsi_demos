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
    
    if 'transaction_monitoring' in scenarios:
        required_tables.update([
            'ALERTS',
            'ALERT_DISPOSITION_HISTORY',
            'TRANSACTIONS'
        ])
    
    if 'periodic_kyc_review' in scenarios:
        required_tables.update([
            'TRANSACTIONS'
        ])
    
    if 'network_analysis' in scenarios:
        required_tables.update([
            'ENTITY_RELATIONSHIPS',
            'TRANSACTIONS'
        ])
    
    # Phase 2 scenarios
    if 'corp_relationship_manager' in scenarios:
        required_tables.update([
            'CLIENT_CRM',
            'CLIENT_OPPORTUNITIES',
            'ENTITY_RELATIONSHIPS',
            'TRANSACTIONS'
        ])
    
    if 'wealth_advisor' in scenarios:
        required_tables.update([
            'WEALTH_CLIENT_PROFILES',
            'HOLDINGS',
            'MODEL_PORTFOLIOS'
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
    if any(scenario in scenarios for scenario in ['aml_kyc_edd', 'credit_analysis', 'network_analysis']):
        create_cross_domain_intelligence_semantic_view(session)
    
    # Create transaction monitoring semantic view
    if 'transaction_monitoring' in scenarios:
        create_alert_summary_view(session)
        create_transaction_monitoring_semantic_view(session)
    
    # Create network analysis semantic view
    if 'network_analysis' in scenarios:
        create_entity_network_analysis_view(session)
        create_network_analysis_semantic_view(session)
    
    # Phase 2: Create corporate client 360 semantic view
    if 'corp_relationship_manager' in scenarios:
        create_corporate_client_360_view(session)
        create_corporate_client_360_semantic_view(session)
    
    # Phase 2: Create wealth client semantic view
    if 'wealth_advisor' in scenarios:
        create_wealth_client_sv(session)
    
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
            c.REVIEW_FREQUENCY_MONTHS,
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
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.aml_kyc_risk_sv
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
            customer_risk.AmlFlags AS AML_FLAGS
                WITH SYNONYMS=('aml flag count', 'risk flags', 'suspicious flags')
                COMMENT='Number of AML risk flags raised (0-5 scale)',
            
            transaction_summary.TotalTransactions AS total_transactions
                WITH SYNONYMS=('transaction count', 'number of transactions')
                COMMENT='Total number of transactions for the customer',
            
            transaction_summary.SuspiciousTransactions AS suspicious_transactions
                WITH SYNONYMS=('flagged transactions', 'suspicious activity count')
                COMMENT='Number of transactions flagged for suspicious activity',
            
            transaction_summary.LargestTransactionAmount AS largest_transaction_amount
                WITH SYNONYMS=('biggest transaction', 'maximum amount', 'largest deposit')
                COMMENT='Largest single transaction amount in {config.CURRENCY}',
            
            transaction_summary.LargestSuspiciousAmount AS largest_suspicious_amount
                WITH SYNONYMS=('biggest suspicious transaction', 'largest flagged amount')
                COMMENT='Largest suspicious transaction amount in {config.CURRENCY}',
            
            transaction_summary.LargeTransactionsCount AS large_transactions_count
                WITH SYNONYMS=('large transaction count', 'high value transactions')
                COMMENT='Number of transactions over €1M threshold',
            
            transaction_summary.RecentTransactionsCount AS recent_transactions_count
                WITH SYNONYMS=('recent activity count', 'current month transactions')
                COMMENT='Number of transactions in the last 30 days',
            
            transaction_summary.RecentDepositsTotal AS recent_deposits_total
                WITH SYNONYMS=('recent deposit amount', 'current deposits', 'latest funding')
                COMMENT='Total amount of deposits received in the last 30 days in {config.CURRENCY}',
            
            transaction_summary.AvgRiskScore AS avg_risk_score
                WITH SYNONYMS=('average risk', 'transaction risk level')
                COMMENT='Average risk score across all transactions (0-1 scale)'
        )
        DIMENSIONS (
            customer_risk.CustomerId AS CUSTOMER_ID
                WITH SYNONYMS=('client id', 'customer identifier')
                COMMENT='Unique customer identifier',
            
            customer_risk.EntityName AS ENTITY_NAME
                WITH SYNONYMS=('company name', 'organization name', 'client name')
                COMMENT='Legal entity name for customer identification',
            
            customer_risk.EntityId AS ENTITY_ID
                WITH SYNONYMS=('entity identifier', 'company id')
                COMMENT='Associated entity identifier',
            
            customer_risk.RiskRating AS RISK_RATING
                WITH SYNONYMS=('risk level', 'customer risk', 'aml rating')
                COMMENT='Customer risk rating (LOW, MEDIUM, HIGH)',
            
            customer_risk.KycStatus AS KYC_STATUS
                WITH SYNONYMS=('kyc state', 'due diligence status')
                COMMENT='KYC completion status: COMPLETE (standard DD completed), PENDING (documentation in progress), REQUIRES_EDD (Enhanced Due Diligence needed)',
            
            customer_risk.CustomerType AS CUSTOMER_TYPE
                WITH SYNONYMS=('client type', 'customer classification')
                COMMENT='Type of customer relationship',
            
            customer_risk.LastReviewDate AS LAST_REVIEW_DATE
                WITH SYNONYMS=('previous review date', 'last KYC review')
                COMMENT='Date of the most recent KYC review',
            
            customer_risk.NextReviewDate AS NEXT_REVIEW_DATE
                WITH SYNONYMS=('upcoming review date', 'scheduled review')
                COMMENT='Date when next periodic KYC review is due',
            
            customer_risk.ReviewFrequencyMonths AS REVIEW_FREQUENCY_MONTHS
                WITH SYNONYMS=('review cycle', 'review interval')
                COMMENT='Review frequency in months based on risk rating (HIGH=6, MEDIUM=12, LOW=24)',
            
            transaction_summary.LatestLargeTransactionDate AS latest_large_transaction_date
                WITH SYNONYMS=('recent large transaction date', 'latest high value transaction')
                COMMENT='Date of the most recent transaction over €1M',
            
            transaction_summary.LatestSuspiciousTransactionDate AS latest_suspicious_transaction_date
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
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.credit_risk_sv
        TABLES (
            loan_apps AS {config.SNOWFLAKE['database']}.RAW_DATA.LOAN_APPLICATIONS
                PRIMARY KEY (APPLICATION_ID)
                COMMENT='Current loan applications under review'
        )
        FACTS (
            loan_apps.RequestedAmount AS REQUESTED_AMOUNT 
                WITH SYNONYMS=('loan amount', 'credit amount', 'funding request')
                COMMENT='Amount of credit requested in {config.CURRENCY}',
            
            loan_apps.DSCR AS DSCR
                WITH SYNONYMS=('debt service coverage ratio', 'debt coverage ratio', 'cash flow coverage')
                COMMENT='Debt Service Coverage Ratio (cash flow / debt service)',
            
            loan_apps.DebtToEquity AS DEBT_TO_EQUITY
                WITH SYNONYMS=('D/E ratio', 'leverage ratio', 'debt equity ratio')
                COMMENT='Debt-to-Equity ratio (total debt / equity)',
            
            loan_apps.CurrentRatio AS CURRENT_RATIO
                WITH SYNONYMS=('liquidity ratio', 'working capital ratio')
                COMMENT='Current ratio for liquidity assessment (current assets / current liabilities)',
                
            loan_apps.ClientConcentration AS CLIENT_CONCENTRATION
                WITH SYNONYMS=('client concentration', 'customer concentration percentage', 'revenue concentration')
                COMMENT='Percentage of revenue from largest client (concentration risk)'
        )
        DIMENSIONS (
            loan_apps.ApplicationId AS APPLICATION_ID
                WITH SYNONYMS=('app id', 'application number', 'loan application id')
                COMMENT='Unique loan application identifier',
                
            loan_apps.CustomerId AS CUSTOMER_ID
                WITH SYNONYMS=('borrower id', 'applicant id')
                COMMENT='Customer identifier for the applicant',
            
            loan_apps.EntityId AS ENTITY_ID
                WITH SYNONYMS=('borrower entity', 'applicant entity', 'entity identifier')
                COMMENT='Entity ID of the loan applicant',
            
            loan_apps.Industry AS INDUSTRY
                WITH SYNONYMS=('industry sector', 'business sector', 'sector classification')
                COMMENT='Industry classification of the applicant',
                
            loan_apps.ApplicationStatus AS APPLICATION_STATUS
                WITH SYNONYMS=('loan status', 'application state', 'review status')
                COMMENT='Current status of the loan application',
                
            loan_apps.ApplicationDate AS APPLICATION_DATE
                WITH SYNONYMS=('submission date', 'application submission date')
                COMMENT='Date when the loan application was submitted',
            
            loan_apps.RiskRating AS RISK_RATING
                WITH SYNONYMS=('credit risk level', 'applicant risk rating')
                COMMENT='Overall risk rating of the application (LOW, MEDIUM, HIGH)'
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
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.cross_domain_intelligence_sv
        TABLES (
            entities AS {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES
                PRIMARY KEY (ENTITY_ID)
                COMMENT='Core entity information for cross-domain analysis',
            
            relationships AS {config.SNOWFLAKE['database']}.RAW_DATA.ENTITY_RELATIONSHIPS
                PRIMARY KEY (RELATIONSHIP_ID)
                COMMENT='Entity relationships for ecosystem analysis'
        )
        RELATIONSHIPS (
            relationships_to_entities AS relationships(PRIMARY_ENTITY_ID) REFERENCES entities(ENTITY_ID)
        )
        FACTS (
            relationships.RiskImpactScore AS RISK_IMPACT_SCORE
                WITH SYNONYMS=('risk impact', 'relationship risk', 'contagion risk')
                COMMENT='Risk impact score of the relationship (0-1 scale)'
        )
        DIMENSIONS (
            entities.EntityId AS ENTITY_ID
                WITH SYNONYMS=('company id', 'entity identifier')
                COMMENT='Unique entity identifier',
            
            entities.EntityName AS ENTITY_NAME
                WITH SYNONYMS=('company name', 'organization name')
                COMMENT='Legal entity name',
            
            entities.IndustrySector AS INDUSTRY_SECTOR
                WITH SYNONYMS=('industry', 'business sector', 'sector')
                COMMENT='Industry classification of the entity',
            
            entities.CountryCode AS COUNTRY_CODE
                WITH SYNONYMS=('country', 'jurisdiction', 'location')
                COMMENT='Country code where entity is incorporated',
            
            relationships.RelationshipType AS RELATIONSHIP_TYPE
                WITH SYNONYMS=('connection type', 'business relationship')
                COMMENT='Type of business relationship (SUPPLIER, CUSTOMER, VENDOR, etc.)',
            
            relationships.RelatedEntityId AS RELATED_ENTITY_ID
                WITH SYNONYMS=('connected entity', 'relationship target')
                COMMENT='Entity ID of the related entity in the relationship'
        )
        COMMENT='Cross-domain intelligence view for ecosystem analysis and risk contagion modeling'
    """).collect()
    
    logger.info("Cross-domain intelligence semantic view created successfully")


def create_alert_summary_view(session: Session) -> None:
    """Create alert summary view for transaction monitoring semantic view."""
    logger.info("Creating alert summary view...")
    
    # Validate required tables exist
    validate_required_tables(session, ['ALERTS', 'CUSTOMERS'])
    
    session.sql(f"""
        CREATE OR REPLACE VIEW {config.SNOWFLAKE['database']}.CURATED_DATA.alert_summary_view AS
        SELECT 
            a.ALERT_ID,
            a.CUSTOMER_ID,
            c.ENTITY_NAME,
            c.RISK_RATING as customer_risk_rating,
            a.ALERT_TYPE,
            a.ALERT_DATE,
            a.ALERT_STATUS,
            a.PRIORITY_SCORE,
            a.ASSIGNED_TO,
            a.RESOLUTION_DATE,
            a.DISPOSITION,
            a.ALERT_DESCRIPTION,
            a.FLAGGED_TRANSACTION_COUNT,
            a.TOTAL_FLAGGED_AMOUNT,
            DATEDIFF(day, a.ALERT_DATE, COALESCE(a.RESOLUTION_DATE, CURRENT_DATE())) as days_open,
            CASE 
                WHEN a.RESOLUTION_DATE IS NOT NULL THEN DATEDIFF(hour, a.ALERT_DATE, a.RESOLUTION_DATE)
                ELSE NULL 
            END as investigation_hours,
            a.CREATED_DATE
        FROM {config.SNOWFLAKE['database']}.RAW_DATA.ALERTS a
        JOIN {config.SNOWFLAKE['database']}.CURATED_DATA.customer_risk_view c ON a.CUSTOMER_ID = c.CUSTOMER_ID
    """).collect()
    
    logger.info("Alert summary view created successfully")


def create_transaction_monitoring_semantic_view(session: Session) -> None:
    """Create transaction monitoring semantic view for alert triage and investigation."""
    logger.info("Creating transaction monitoring semantic view...")
    
    session.sql(f"""
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.transaction_monitoring_sv
        TABLES (
            alerts AS {config.SNOWFLAKE['database']}.CURATED_DATA.alert_summary_view
                PRIMARY KEY (ALERT_ID)
                COMMENT='Transaction monitoring alerts with customer risk context'
        )
        FACTS (
            alerts.PriorityScore AS PRIORITY_SCORE
                WITH SYNONYMS=('alert priority', 'suspicion score', 'risk score')
                COMMENT='ML-based priority score for alert triage (0-1 scale)',
            
            alerts.FlaggedTransactionCount AS FLAGGED_TRANSACTION_COUNT
                WITH SYNONYMS=('transaction count', 'number of transactions')
                COMMENT='Number of transactions flagged in this alert',
            
            alerts.TotalFlaggedAmount AS TOTAL_FLAGGED_AMOUNT
                WITH SYNONYMS=('flagged amount', 'suspicious amount')
                COMMENT='Total amount of flagged transactions in {config.CURRENCY}',
            
            alerts.DaysOpen AS days_open
                WITH SYNONYMS=('alert age', 'days pending', 'open duration')
                COMMENT='Number of days alert has been open',
            
            alerts.InvestigationHours AS investigation_hours
                WITH SYNONYMS=('time spent', 'investigation time')
                COMMENT='Hours spent investigating the alert'
        )
        DIMENSIONS (
            alerts.AlertId AS ALERT_ID
                WITH SYNONYMS=('alert number', 'alert identifier')
                COMMENT='Unique alert identifier',
            
            alerts.CustomerId AS CUSTOMER_ID
                WITH SYNONYMS=('alert client id', 'customer identifier')
                COMMENT='Customer identifier associated with alert',
            
            alerts.EntityName AS ENTITY_NAME
                WITH SYNONYMS=('alert entity name', 'customer name')
                COMMENT='Legal entity name of the customer',
            
            alerts.CustomerRiskRating AS customer_risk_rating
                WITH SYNONYMS=('alert risk level', 'alert customer risk')
                COMMENT='Customer risk rating (LOW, MEDIUM, HIGH)',
            
            alerts.AlertType AS ALERT_TYPE
                WITH SYNONYMS=('alert category', 'scenario type')
                COMMENT='Type of alert: Structuring, Large Cash, Rapid Movement, High Risk Country, Unusual Pattern',
            
            alerts.AlertStatus AS ALERT_STATUS
                WITH SYNONYMS=('status', 'alert state')
                COMMENT='Current status: OPEN, UNDER_INVESTIGATION, CLOSED',
            
            alerts.AssignedTo AS ASSIGNED_TO
                WITH SYNONYMS=('analyst', 'investigator', 'assigned analyst')
                COMMENT='Name of analyst assigned to the alert',
            
            alerts.Disposition AS DISPOSITION
                WITH SYNONYMS=('outcome', 'final disposition', 'resolution')
                COMMENT='Final disposition: SAR_FILED, FALSE_POSITIVE, CLEARED',
            
            alerts.AlertDate AS ALERT_DATE
                WITH SYNONYMS=('alert generated date', 'trigger date')
                COMMENT='Date when alert was generated',
            
            alerts.ResolutionDate AS RESOLUTION_DATE
                WITH SYNONYMS=('closed date', 'completion date')
                COMMENT='Date when alert was resolved'
        )
        COMMENT='Transaction monitoring view for alert triage with ML-based priority scoring'
    """).collect()
    
    logger.info("Transaction monitoring semantic view created successfully")


def create_entity_network_analysis_view(session: Session) -> None:
    """Create entity network analysis view for network analysis semantic view."""
    logger.info("Creating entity network analysis view...")
    
    # Validate required tables exist
    validate_required_tables(session, ['ENTITIES', 'ENTITY_RELATIONSHIPS'])
    
    session.sql(f"""
        CREATE OR REPLACE VIEW {config.SNOWFLAKE['database']}.CURATED_DATA.entity_network_analysis_view AS
        SELECT 
            e.ENTITY_ID,
            e.ENTITY_NAME,
            e.COUNTRY_CODE,
            e.INDUSTRY_SECTOR,
            e.INCORPORATION_DATE,
            COUNT(DISTINCT r.RELATIONSHIP_ID) as total_relationships,
            COUNT(DISTINCT CASE WHEN r.RELATIONSHIP_TYPE = 'VENDOR' THEN r.RELATIONSHIP_ID END) as vendor_relationships,
            COUNT(DISTINCT CASE WHEN r.SHARED_DIRECTOR_NAME IS NOT NULL THEN r.RELATIONSHIP_ID END) as shared_director_relationships,
            COUNT(DISTINCT CASE WHEN r.SHARED_ADDRESS_FLAG = TRUE THEN r.RELATIONSHIP_ID END) as shared_address_relationships,
            MAX(r.SHARED_DIRECTOR_NAME) as primary_shared_director,
            MAX(r.SHARED_ADDRESS) as primary_shared_address,
            AVG(r.RISK_IMPACT_SCORE) as avg_relationship_risk_score,
            MAX(r.RISK_IMPACT_SCORE) as max_relationship_risk_score
        FROM {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES e
        LEFT JOIN {config.SNOWFLAKE['database']}.RAW_DATA.ENTITY_RELATIONSHIPS r 
            ON e.ENTITY_ID = r.PRIMARY_ENTITY_ID OR e.ENTITY_ID = r.RELATED_ENTITY_ID
        GROUP BY 
            e.ENTITY_ID, e.ENTITY_NAME, e.COUNTRY_CODE, 
            e.INDUSTRY_SECTOR, e.INCORPORATION_DATE
    """).collect()
    
    logger.info("Entity network analysis view created successfully")


def create_network_analysis_semantic_view(session: Session) -> None:
    """Create network analysis semantic view for shell company and TBML detection."""
    logger.info("Creating network analysis semantic view...")
    
    session.sql(f"""
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.network_analysis_sv
        TABLES (
            entities AS {config.SNOWFLAKE['database']}.CURATED_DATA.entity_network_analysis_view
                PRIMARY KEY (ENTITY_ID)
                COMMENT='Entity profiles with network relationship metrics',
            
            relationships AS {config.SNOWFLAKE['database']}.RAW_DATA.ENTITY_RELATIONSHIPS
                PRIMARY KEY (RELATIONSHIP_ID)
                COMMENT='Entity relationships with shared characteristic indicators'
        )
        RELATIONSHIPS (
            relationships_to_entities AS relationships(PRIMARY_ENTITY_ID) REFERENCES entities(ENTITY_ID)
        )
        FACTS (
            entities.TotalRelationships AS total_relationships
                WITH SYNONYMS=('relationship count', 'connection count')
                COMMENT='Total number of relationships for the entity',
            
            entities.VendorRelationships AS vendor_relationships
                WITH SYNONYMS=('supplier count', 'vendor count')
                COMMENT='Number of vendor relationships',
            
            entities.SharedDirectorRelationships AS shared_director_relationships
                WITH SYNONYMS=('common director count', 'shared director count')
                COMMENT='Number of relationships with shared directors',
            
            entities.SharedAddressRelationships AS shared_address_relationships
                WITH SYNONYMS=('common address count', 'shared address count')
                COMMENT='Number of relationships with shared addresses',
            
            entities.AvgRelationshipRiskScore AS avg_relationship_risk_score
                WITH SYNONYMS=('average risk', 'mean risk score')
                COMMENT='Average risk score across all relationships (0-1 scale)',
            
            entities.MaxRelationshipRiskScore AS max_relationship_risk_score
                WITH SYNONYMS=('highest risk', 'peak risk score')
                COMMENT='Maximum risk score among relationships (0-1 scale)',
            
            relationships.RiskImpactScore AS RISK_IMPACT_SCORE
                WITH SYNONYMS=('relationship risk', 'connection risk')
                COMMENT='Risk impact score of individual relationship (0-1 scale)',
            
            relationships.IncorporationProximityDays AS INCORPORATION_PROXIMITY_DAYS
                WITH SYNONYMS=('incorporation timing', 'formation proximity')
                COMMENT='Days between entity incorporations (shell company indicator)'
        )
        DIMENSIONS (
            entities.EntityId AS ENTITY_ID
                WITH SYNONYMS=('company id', 'entity identifier')
                COMMENT='Unique entity identifier',
            
            entities.EntityName AS ENTITY_NAME
                WITH SYNONYMS=('company name', 'organization name')
                COMMENT='Legal entity name',
            
            entities.CountryCode AS COUNTRY_CODE
                WITH SYNONYMS=('country', 'jurisdiction', 'location')
                COMMENT='Country code where entity is incorporated',
            
            entities.IndustrySector AS INDUSTRY_SECTOR
                WITH SYNONYMS=('industry', 'business sector')
                COMMENT='Industry classification of the entity',
            
            entities.PrimarySharedDirector AS primary_shared_director
                WITH SYNONYMS=('common director', 'shared director name')
                COMMENT='Name of primary shared director across relationships',
            
            entities.PrimarySharedAddress AS primary_shared_address
                WITH SYNONYMS=('common address', 'shared address')
                COMMENT='Primary shared address across relationships',
            
            relationships.RelationshipType AS RELATIONSHIP_TYPE
                WITH SYNONYMS=('connection type', 'business relationship')
                COMMENT='Type of relationship: VENDOR, CUSTOMER, SUBSIDIARY, etc.',
            
            relationships.RelatedEntityId AS RELATED_ENTITY_ID
                WITH SYNONYMS=('connected entity', 'relationship target')
                COMMENT='Entity ID of the related entity',
            
            relationships.SharedDirectorName AS SHARED_DIRECTOR_NAME
                WITH SYNONYMS=('common director name', 'director overlap')
                COMMENT='Name of shared director between entities',
            
            relationships.SharedAddressFlag AS SHARED_ADDRESS_FLAG
                WITH SYNONYMS=('common address indicator', 'address overlap flag')
                COMMENT='Indicator that entities share the same address',
            
            relationships.SharedAddress AS SHARED_ADDRESS
                WITH SYNONYMS=('common address', 'shared location')
                COMMENT='The actual shared address between entities'
        )
        COMMENT='Network analysis view for shell company detection and TBML typology identification with shared characteristic tracking'
    """).collect()
    
    logger.info("Network analysis semantic view created successfully")


# =============================================================================
# PHASE 2 SEMANTIC VIEWS
# =============================================================================

def create_corporate_client_360_view(session: Session) -> None:
    """Create curated view aggregating client CRM, opportunities, and relationships for Corporate RM."""
    logger.info("Creating corporate client 360 curated view...")
    
    session.sql(f"""
        CREATE OR REPLACE VIEW {config.SNOWFLAKE['database']}.CURATED_DATA.corporate_client_360_view AS
        SELECT 
            c.CUSTOMER_ID,
            e.ENTITY_NAME as client_name,
            e.COUNTRY_CODE as country,
            e.INDUSTRY_SECTOR as industry,
            c.RISK_RATING as risk_rating,
            crm.RELATIONSHIP_MANAGER,
            crm.LAST_CONTACT_DATE,
            crm.ACCOUNT_STATUS,
            crm.ACCOUNT_TIER,
            crm.RISK_OPPORTUNITIES_COUNT,
            -- Opportunity metrics
            COUNT(DISTINCT opp.OPPORTUNITY_ID) as total_opportunities,
            COUNT(DISTINCT CASE WHEN opp.STATUS = 'OPEN' THEN opp.OPPORTUNITY_ID END) as open_opportunities,
            SUM(CASE WHEN opp.STATUS IN ('OPEN', 'IN_PROGRESS') THEN opp.POTENTIAL_VALUE ELSE 0 END) as pipeline_value,
            -- Relationship metrics
            COUNT(DISTINCT r.RELATIONSHIP_ID) as vendor_relationship_count,
            AVG(r.RISK_IMPACT_SCORE) as avg_vendor_risk_score,
            -- Transaction metrics
            COUNT(DISTINCT t.TRANSACTION_ID) as transaction_count_90d,
            SUM(t.AMOUNT) as transaction_volume_90d
        FROM {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS c
        LEFT JOIN {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES e ON c.ENTITY_ID = e.ENTITY_ID
        LEFT JOIN {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM crm ON c.CUSTOMER_ID = crm.CUSTOMER_ID
        LEFT JOIN {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_OPPORTUNITIES opp ON c.CUSTOMER_ID = opp.CUSTOMER_ID
        LEFT JOIN {config.SNOWFLAKE['database']}.RAW_DATA.ENTITY_RELATIONSHIPS r ON c.ENTITY_ID = r.PRIMARY_ENTITY_ID
        LEFT JOIN {config.SNOWFLAKE['database']}.RAW_DATA.TRANSACTIONS t 
            ON c.CUSTOMER_ID = t.CUSTOMER_ID 
            AND t.TRANSACTION_DATE >= DATEADD(day, -90, CURRENT_DATE())
        GROUP BY 
            c.CUSTOMER_ID, e.ENTITY_NAME, e.COUNTRY_CODE, e.INDUSTRY_SECTOR, c.RISK_RATING,
            crm.RELATIONSHIP_MANAGER, crm.LAST_CONTACT_DATE, crm.ACCOUNT_STATUS, 
            crm.ACCOUNT_TIER, crm.RISK_OPPORTUNITIES_COUNT
    """).collect()
    
    logger.info("Corporate client 360 curated view created successfully")


def create_corporate_client_360_semantic_view(session: Session) -> None:
    """Create corporate_client_360_sv for relationship manager scenario."""
    logger.info("Creating corporate_client_360_sv semantic view...")
    
    session.sql(f"""
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.corporate_client_360_sv
        TABLES (
            clients AS {config.SNOWFLAKE['database']}.CURATED_DATA.corporate_client_360_view
                PRIMARY KEY (CUSTOMER_ID)
                COMMENT='Corporate client 360-degree view with CRM, opportunities, and relationships',
            
            opportunities AS {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_OPPORTUNITIES
                PRIMARY KEY (OPPORTUNITY_ID)
                COMMENT='Client opportunities with potential revenue impact'
        )
        FACTS (
            clients.TotalOpportunities AS total_opportunities
                WITH SYNONYMS=('opportunity count', 'number of opportunities')
                COMMENT='Total number of opportunities identified for this client',
            
            clients.OpenOpportunities AS open_opportunities
                WITH SYNONYMS=('active opportunities', 'in progress opportunities')
                COMMENT='Number of opportunities currently open or in progress',
            
            clients.PipelineValue AS pipeline_value
                WITH SYNONYMS=('pipeline amount', 'opportunity value', 'potential revenue')
                COMMENT='Total potential value of open and in-progress opportunities',
            
            clients.VendorRelationshipCount AS vendor_relationship_count
                WITH SYNONYMS=('supplier count', 'vendor count')
                COMMENT='Number of vendor relationships this client has',
            
            clients.AvgVendorRiskScore AS avg_vendor_risk_score
                WITH SYNONYMS=('average vendor risk', 'mean supplier risk')
                COMMENT='Average risk impact score of vendor relationships',
            
            clients.TransactionCount90d AS transaction_count_90d
                WITH SYNONYMS=('recent transaction count', 'quarterly transactions')
                COMMENT='Number of transactions in last 90 days',
            
            clients.TransactionVolume90d AS transaction_volume_90d
                WITH SYNONYMS=('transaction volume', 'quarterly volume', 'recent volume')
                COMMENT='Total transaction volume in EUR over last 90 days',
            
            opportunities.OpportunityPotentialValue AS POTENTIAL_VALUE
                WITH SYNONYMS=('opportunity value', 'estimated revenue', 'potential value')
                COMMENT='Estimated revenue impact of this opportunity'
        )
        DIMENSIONS (
            clients.CustomerId AS CUSTOMER_ID
                COMMENT='Unique customer identifier',
            
            clients.ClientName AS client_name
                WITH SYNONYMS=('customer name', 'entity name', 'company name')
                COMMENT='Legal name of the client entity',
            
            clients.Country AS country
                WITH SYNONYMS=('country code', 'jurisdiction', 'domicile')
                COMMENT='Country where client is domiciled',
            
            clients.Industry AS industry
                WITH SYNONYMS=('sector', 'industry sector', 'business sector')
                COMMENT='Industry classification of the client',
            
            clients.RiskRating AS risk_rating
                WITH SYNONYMS=('risk level', 'client risk')
                COMMENT='Overall risk rating (LOW, MEDIUM, HIGH)',
            
            clients.RelationshipManager AS RELATIONSHIP_MANAGER
                WITH SYNONYMS=('RM', 'account manager', 'relationship banker')
                COMMENT='Name of the relationship manager assigned to this client',
            
            clients.LastContactDate AS LAST_CONTACT_DATE
                WITH SYNONYMS=('last call date', 'last interaction')
                COMMENT='Date of most recent client contact',
            
            clients.AccountStatus AS ACCOUNT_STATUS
                WITH SYNONYMS=('client status', 'relationship status')
                COMMENT='Status of the account (ACTIVE, PROSPECT, INACTIVE)',
            
            clients.AccountTier AS ACCOUNT_TIER
                WITH SYNONYMS=('tier', 'service level', 'client tier')
                COMMENT='Account tier classification (PREMIUM, STANDARD, BASIC)',
            
            opportunities.OpportunityId AS OPPORTUNITY_ID
                COMMENT='Unique opportunity identifier',
            
            opportunities.OpportunityType AS OPPORTUNITY_TYPE
                WITH SYNONYMS=('opp type', 'product type')
                COMMENT='Type of opportunity (CROSS_SELL, UPSELL, RISK_MITIGATION, etc.)',
            
            opportunities.OpportunityDescription AS OPPORTUNITY_DESCRIPTION
                WITH SYNONYMS=('opportunity details', 'product description')
                COMMENT='Detailed description of the opportunity',
            
            opportunities.OpportunitySource AS SOURCE_TYPE
                WITH SYNONYMS=('source', 'origin', 'how identified')
                COMMENT='How opportunity was identified (call_note, internal_email, news, etc.)',
            
            opportunities.OpportunityPriority AS PRIORITY
                WITH SYNONYMS=('urgency', 'importance')
                COMMENT='Priority level (HIGH, MEDIUM, LOW)',
            
            opportunities.OpportunityStatus AS STATUS
                WITH SYNONYMS=('opp status', 'stage')
                COMMENT='Current status (OPEN, IN_PROGRESS, CLOSED_WON, CLOSED_LOST)',
            
            opportunities.OpportunityCreatedDate AS CREATED_DATE
                WITH SYNONYMS=('opportunity date', 'identified date')
                COMMENT='Date when opportunity was first identified'
        )
        COMMENT='Corporate client 360 view for relationship manager with opportunities and cross-entity intelligence'
    """).collect()
    
    logger.info("Corporate client 360 semantic view created successfully")


def create_wealth_client_sv(session: Session) -> None:
    """Create wealth_client_sv for wealth advisor scenario."""
    logger.info("Creating wealth_client_sv semantic view...")
    
    session.sql(f"""
        CREATE OR REPLACE SEMANTIC VIEW {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.wealth_client_sv
        TABLES (
            profiles AS {config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_CLIENT_PROFILES
                PRIMARY KEY (PROFILE_ID)
                COMMENT='Wealth client profiles with model portfolio assignments',
            
            holdings AS {config.SNOWFLAKE['database']}.RAW_DATA.HOLDINGS
                PRIMARY KEY (HOLDING_ID)
                COMMENT='Individual investment holdings',
            
            models AS {config.SNOWFLAKE['database']}.RAW_DATA.MODEL_PORTFOLIOS
                PRIMARY KEY (MODEL_ID)
                COMMENT='Model portfolio definitions with target allocations'
        )
        FACTS (
            profiles.TotalAUM AS TOTAL_AUM
                WITH SYNONYMS=('assets under management', 'portfolio value', 'total assets')
                COMMENT='Total assets under management for this client',
            
            profiles.ConcentrationThreshold AS CONCENTRATION_THRESHOLD_PCT
                WITH SYNONYMS=('concentration limit', 'position limit')
                COMMENT='Alert threshold if any single holding exceeds this percentage',
            
            profiles.RebalanceTrigger AS REBALANCE_TRIGGER_PCT
                WITH SYNONYMS=('rebalance threshold', 'drift threshold')
                COMMENT='Trigger rebalance if allocation deviates by this percentage',
            
            holdings.HoldingValue AS CURRENT_VALUE
                WITH SYNONYMS=('market value', 'position value', 'holding amount')
                COMMENT='Current market value of this holding',
            
            holdings.HoldingCostBasis AS COST_BASIS
                WITH SYNONYMS=('original cost', 'purchase price', 'tax basis')
                COMMENT='Original cost basis for tax calculations',
            
            holdings.UnrealizedGainLoss AS UNREALIZED_GAIN_LOSS
                WITH SYNONYMS=('paper gain', 'unrealized profit', 'mark to market gain')
                COMMENT='Unrealized gain or loss on this holding',
            
            holdings.CurrentAllocation AS ALLOCATION_PCT
                WITH SYNONYMS=('portfolio percentage', 'weight', 'allocation weight')
                COMMENT='Percentage of total portfolio this holding represents',
            
            holdings.HoldingQuantity AS QUANTITY
                WITH SYNONYMS=('shares', 'units', 'position size')
                COMMENT='Number of shares or units held',
            
            models.TargetEquityAllocation AS TARGET_EQUITY_PCT
                WITH SYNONYMS=('equity target', 'stock allocation target')
                COMMENT='Target equity allocation for this model portfolio',
            
            models.TargetBondAllocation AS TARGET_BOND_PCT
                WITH SYNONYMS=('bond target', 'fixed income target')
                COMMENT='Target bond allocation for this model portfolio',
            
            models.TargetAlternativeAllocation AS TARGET_ALTERNATIVE_PCT
                WITH SYNONYMS=('alternative target', 'alts target')
                COMMENT='Target alternative investment allocation',
            
            models.TargetCashAllocation AS TARGET_CASH_PCT
                WITH SYNONYMS=('cash target', 'liquidity target')
                COMMENT='Target cash allocation',
            
            models.ExpectedReturn AS EXPECTED_ANNUAL_RETURN_PCT
                WITH SYNONYMS=('expected return', 'target return', 'projected return')
                COMMENT='Expected annual return for this model portfolio',
            
            models.ExpectedVolatility AS EXPECTED_VOLATILITY_PCT
                WITH SYNONYMS=('risk level', 'standard deviation', 'volatility')
                COMMENT='Expected volatility (standard deviation) for this model'
        )
        DIMENSIONS (
            profiles.ProfileId AS PROFILE_ID
                COMMENT='Unique wealth client profile identifier',
            
            profiles.CustomerId AS CUSTOMER_ID
                WITH SYNONYMS=('client id', 'account id')
                COMMENT='Link to customer master data',
            
            profiles.WealthAdvisor AS WEALTH_ADVISOR
                WITH SYNONYMS=('advisor', 'advisor name', 'portfolio manager')
                COMMENT='Name of the wealth advisor managing this client',
            
            profiles.RiskTolerance AS RISK_TOLERANCE
                WITH SYNONYMS=('risk appetite', 'risk profile')
                COMMENT='Client risk tolerance (CONSERVATIVE, MODERATE, AGGRESSIVE)',
            
            profiles.TaxStatus AS TAX_STATUS
                WITH SYNONYMS=('tax treatment', 'account type')
                COMMENT='Tax status of the account (STANDARD, TAX_DEFERRED, TAX_EXEMPT)',
            
            profiles.InvestmentObjectives AS INVESTMENT_OBJECTIVES
                WITH SYNONYMS=('investment goals', 'objectives', 'financial goals')
                COMMENT='Primary investment objectives (GROWTH, INCOME, PRESERVATION, BALANCED)',
            
            profiles.LastRebalanceDate AS LAST_REBALANCE_DATE
                WITH SYNONYMS=('previous rebalance', 'last portfolio adjustment')
                COMMENT='Date of most recent portfolio rebalancing',
            
            profiles.NextReviewDate AS NEXT_REVIEW_DATE
                WITH SYNONYMS=('upcoming review', 'scheduled review date')
                COMMENT='Date when next portfolio review is scheduled',
            
            holdings.AssetType AS ASSET_TYPE
                WITH SYNONYMS=('asset category', 'investment type')
                COMMENT='Broad asset type (EQUITY, BOND, ALTERNATIVE, CASH)',
            
            holdings.AssetClass AS ASSET_CLASS
                WITH SYNONYMS=('sub-asset class', 'specific asset type')
                COMMENT='Specific asset class (DOMESTIC_EQUITY, INTL_EQUITY, GOVT_BOND, etc.)',
            
            holdings.AssetName AS ASSET_NAME
                WITH SYNONYMS=('holding name', 'security name', 'investment name')
                COMMENT='Full name of the asset or security',
            
            holdings.Ticker AS TICKER_SYMBOL
                WITH SYNONYMS=('ticker symbol', 'symbol', 'stock symbol')
                COMMENT='Trading symbol for this asset',
            
            holdings.HoldingsAsOfDate AS AS_OF_DATE
                WITH SYNONYMS=('valuation date', 'pricing date')
                COMMENT='Date of current valuation',
            
            models.ModelPortfolioId AS MODEL_ID
                COMMENT='Unique model portfolio identifier',
            
            models.ModelName AS MODEL_NAME
                WITH SYNONYMS=('model portfolio name', 'portfolio model')
                COMMENT='Name of the model portfolio',
            
            models.ModelRiskProfile AS RISK_PROFILE
                WITH SYNONYMS=('model risk level')
                COMMENT='Risk profile of this model (LOW, MODERATE, HIGH)',
            
            models.ModelDescription AS DESCRIPTION
                WITH SYNONYMS=('model summary', 'portfolio description')
                COMMENT='Detailed description of the model portfolio strategy'
        )
        COMMENT='Wealth client view for portfolio analysis with model alignment and concentration monitoring'
    """).collect()
    
    logger.info("Wealth client semantic view created successfully")


def main():
    """Main function for testing semantic views creation."""
    print("Semantic views creator module loaded successfully")
    print("Use create_all_semantic_views() method to create semantic views")


if __name__ == "__main__":
    main()
