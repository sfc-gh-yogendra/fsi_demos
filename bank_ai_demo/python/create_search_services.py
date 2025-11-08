"""
Glacier First Bank Demo - Search Services Creator

Creates Cortex Search services for unstructured document analysis.
Each search service is defined in its own function for better modularity.
"""

import logging
from typing import List, Set
from snowflake.snowpark import Session

import config

logger = logging.getLogger(__name__)


def validate_table_exists(session: Session, table_name: str, schema: str = "CURATED") -> bool:
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


def validate_required_tables(session: Session, required_tables: List[str], schema: str = "CURATED") -> None:
    """Validate that all required tables exist, raise error if any are missing."""
    missing_tables = []
    
    for table_name in required_tables:
        if not validate_table_exists(session, table_name, schema):
            missing_tables.append(f"{schema}.{table_name}")
    
    if missing_tables:
        missing_str = ", ".join(missing_tables)
        raise RuntimeError(f"Required tables do not exist: {missing_str}. "
                         f"Please run data generation first with --scope data or --scope all")


def get_required_tables_for_search_services(scenarios: List[str]) -> Set[str]:
    """Get the set of required tables for search services based on scenarios."""
    required_tables = set()
    
    if 'aml_kyc_edd' in scenarios:
        required_tables.add('COMPLIANCE_DOCUMENTS')
    
    if 'credit_analysis' in scenarios:
        required_tables.update([
            'CREDIT_POLICY_DOCUMENTS',
            'LOAN_DOCUMENTS'
        ])
    
    # Commercial & Wealth scenarios
    if 'corp_relationship_manager' in scenarios:
        required_tables.add('CLIENT_DOCUMENTS')
    
    if 'wealth_advisor' in scenarios:
        required_tables.add('WEALTH_MEETING_NOTES')
    
    # Always include news and research (used by multiple scenarios)
    required_tables.add('NEWS_AND_RESEARCH')
    
    # Always include document templates (used by agent framework)
    required_tables.add('DOCUMENT_TEMPLATES')
    
    return required_tables


def validate_table_has_data(session: Session, table_name: str, schema: str = "CURATED") -> bool:
    """Check if a table exists and has data."""
    if not validate_table_exists(session, table_name, schema):
        return False
    
    try:
        result = session.sql(f"""
            SELECT COUNT(*) as cnt 
            FROM {config.SNOWFLAKE['database']}.{schema}.{table_name}
        """).collect()
        
        return result[0]['CNT'] > 0
        
    except Exception as e:
        logger.warning(f"Error checking data in {schema}.{table_name}: {e}")
        return False


def create_all_search_services(session: Session, scenarios: List[str] = None) -> None:
    """Create all Cortex Search services for the specified scenarios."""
    logger.info("Creating Cortex Search services...")
    
    # Set database and warehouse context
    session.sql(f"USE DATABASE {config.SNOWFLAKE['database']}").collect()
    session.sql(f"USE WAREHOUSE {config.SNOWFLAKE['search_warehouse']}").collect()
    
    # Validate required tables exist before creating search services
    scenarios = scenarios or config.get_all_scenarios()
    required_tables = list(get_required_tables_for_search_services(scenarios))
    
    logger.info(f"Validating required document tables: {required_tables}")
    validate_required_tables(session, required_tables)
    logger.info("Table validation completed successfully")
    
    # Warn about tables with no data (search services will still be created but may be empty)
    empty_tables = []
    for table_name in required_tables:
        if not validate_table_has_data(session, table_name):
            empty_tables.append(table_name)
    
    if empty_tables:
        logger.warning(f"Tables exist but appear to be empty: {empty_tables}. "
                      f"Search services will be created but may not return results until data is generated.")
    
    # Create search services based on scenarios
    if 'aml_kyc_edd' in scenarios:
        create_compliance_documents_search_service(session)
    
    if 'credit_analysis' in scenarios:
        create_credit_policy_search_service(session)
        create_loan_documents_search_service(session)
    
    # Always create news and research search service as it's used by multiple scenarios
    create_news_research_search_service(session)
    
    # Create document templates search service for agent framework
    create_document_templates_search_service(session)
    
    # Commercial & Wealth: Create search services for relationship manager and wealth advisor scenarios
    if 'corp_relationship_manager' in scenarios:
        create_client_documents_search_service(session)
    
    if 'wealth_advisor' in scenarios:
        create_wealth_meeting_notes_search_service(session)
    
    # Validate all search services were created successfully
    validate_search_services(session)
    
    logger.info("All Cortex Search services created successfully")


def create_compliance_documents_search_service(session: Session) -> None:
    """Create Cortex Search service for compliance documents (AML/KYC)."""
    logger.info("Creating compliance documents search service...")
    
    # Validate required table exists
    validate_required_tables(session, ['COMPLIANCE_DOCUMENTS'])
    
    session.sql(f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.compliance_docs_search_svc
            ON CONTENT
            ATTRIBUTES ID, TITLE, ENTITY_NAME, DOC_TYPE, PUBLISH_DATE, RISK_SIGNAL
            WAREHOUSE = {config.SNOWFLAKE['search_warehouse']}
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
            FROM {config.SNOWFLAKE['database']}.CURATED.COMPLIANCE_DOCUMENTS
    """).collect()
    
    logger.info("Compliance documents search service created successfully")


def create_credit_policy_search_service(session: Session) -> None:
    """Create Cortex Search service for credit policy documents."""
    logger.info("Creating credit policy search service...")
    
    # Validate required table exists
    validate_required_tables(session, ['CREDIT_POLICY_DOCUMENTS'])
    
    session.sql(f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.credit_policy_search_svc
            ON CONTENT
            ATTRIBUTES ID, TITLE, POLICY_SECTION, EFFECTIVE_DATE, VERSION, REGULATORY_FRAMEWORK
            WAREHOUSE = {config.SNOWFLAKE['search_warehouse']}
            TARGET_LAG = '5 minutes'
            AS 
            SELECT 
                ID,
                TITLE,
                CONTENT,
                POLICY_SECTION,
                EFFECTIVE_DATE,
                VERSION,
                REGULATORY_FRAMEWORK
            FROM {config.SNOWFLAKE['database']}.CURATED.CREDIT_POLICY_DOCUMENTS
    """).collect()
    
    logger.info("Credit policy search service created successfully")


def create_loan_documents_search_service(session: Session) -> None:
    """Create Cortex Search service for loan application documents."""
    logger.info("Creating loan documents search service...")
    
    # Validate required table exists
    validate_required_tables(session, ['LOAN_DOCUMENTS'])
    
    session.sql(f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.loan_documents_search_svc
            ON CONTENT
            ATTRIBUTES ID, TITLE, ENTITY_ID, DOC_TYPE, DOCUMENT_SECTION, PROCESSING_STATUS
            WAREHOUSE = {config.SNOWFLAKE['search_warehouse']}
            TARGET_LAG = '5 minutes'
            AS 
            SELECT 
                ID,
                TITLE,
                CONTENT,
                ENTITY_ID,
                DOC_TYPE,
                DOCUMENT_SECTION,
                PROCESSING_STATUS
            FROM {config.SNOWFLAKE['database']}.CURATED.LOAN_DOCUMENTS
    """).collect()
    
    logger.info("Loan documents search service created successfully")


def create_news_research_search_service(session: Session) -> None:
    """Create Cortex Search service for news and research documents."""
    logger.info("Creating news and research search service...")
    
    # Validate required table exists
    validate_required_tables(session, ['NEWS_AND_RESEARCH'])
    
    session.sql(f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.news_research_search_svc
            ON CONTENT
            ATTRIBUTES ID, TITLE, ENTITY_NAME, ARTICLE_TYPE, PUBLISH_DATE, SOURCE, SENTIMENT_SCORE, ESG_RELEVANCE, SUPPLY_CHAIN_RELEVANCE, INFLATION_RELEVANCE
            WAREHOUSE = {config.SNOWFLAKE['search_warehouse']}
            TARGET_LAG = '5 minutes'
            AS 
            SELECT 
                ID,
                TITLE,
                CONTENT,
                ENTITY_NAME,
                ARTICLE_TYPE,
                PUBLISH_DATE,
                SOURCE,
                SENTIMENT_SCORE,
                CASE WHEN ESG_RELEVANCE = TRUE THEN 'YES' ELSE 'NO' END AS ESG_RELEVANCE,
                CASE WHEN SUPPLY_CHAIN_RELEVANCE = TRUE THEN 'YES' ELSE 'NO' END AS SUPPLY_CHAIN_RELEVANCE,
                CASE WHEN INFLATION_RELEVANCE = TRUE THEN 'YES' ELSE 'NO' END AS INFLATION_RELEVANCE
            FROM {config.SNOWFLAKE['database']}.CURATED.NEWS_AND_RESEARCH
    """).collect()
    
    logger.info("News and research search service created successfully")


def create_document_templates_search_service(session: Session) -> None:
    """Create Cortex Search service for document templates (RFIs, credit memos, etc.)."""
    logger.info("Creating document templates search service...")
    
    # Validate required table exists
    validate_required_tables(session, ['DOCUMENT_TEMPLATES'])
    
    session.sql(f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.document_templates_search_svc
            ON TEMPLATE_CONTENT
            ATTRIBUTES TEMPLATE_ID, TEMPLATE_NAME, TEMPLATE_TYPE, SCENARIO, USE_CASE, REGULATORY_FRAMEWORK, REQUIRED_VARIABLES
            WAREHOUSE = {config.SNOWFLAKE['search_warehouse']}
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
            FROM {config.SNOWFLAKE['database']}.CURATED.DOCUMENT_TEMPLATES
    """).collect()
    
    logger.info("Document templates search service created successfully")


def create_external_data_search_service(session: Session) -> None:
    """Create Cortex Search service for external data sources (if needed)."""
    logger.info("Creating external data search service...")
    
    # This could be used for external data like Reuters news feeds, S&P data, etc.
    # For now, we'll skip this as external data is typically structured
    logger.info("External data search service creation skipped (structured data)")


def validate_search_services(session: Session) -> None:
    """Validate that all search services were created successfully."""
    logger.info("Validating search services...")
    
    try:
        # List all search services
        services = session.sql(f"""
            SHOW CORTEX SEARCH SERVICES IN SCHEMA {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}
        """).collect()
        
        service_names = [row['name'] for row in services]
        logger.info(f"Created search services: {service_names}")
        
        # Check specific services (convert to lowercase for comparison)
        service_names_lower = [name.lower() for name in service_names]
        expected_services = [
            'compliance_docs_search_svc',
            'credit_policy_search_svc', 
            'loan_documents_search_svc',
            'news_research_search_svc',
            'document_templates_search_svc'
        ]
        
        missing_services = [svc for svc in expected_services if svc not in service_names_lower]
        if missing_services:
            logger.warning(f"Missing search services: {missing_services}")
        else:
            logger.info("All expected search services created successfully")
            
    except Exception as e:
        logger.warning(f"Could not validate search services: {e}")


def drop_search_service(session: Session, service_name: str) -> None:
    """Drop a specific search service (utility function)."""
    logger.info(f"Dropping search service: {service_name}")
    
    try:
        session.sql(f"""
            DROP CORTEX SEARCH SERVICE IF EXISTS {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.{service_name}
        """).collect()
        
        logger.info(f"Search service {service_name} dropped successfully")
        
    except Exception as e:
        logger.error(f"Failed to drop search service {service_name}: {e}")


def refresh_search_service(session: Session, service_name: str) -> None:
    """Refresh a specific search service (utility function)."""
    logger.info(f"Refreshing search service: {service_name}")
    
    try:
        session.sql(f"""
            ALTER CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.{service_name} REFRESH
        """).collect()
        
        logger.info(f"Search service {service_name} refreshed successfully")
        
    except Exception as e:
        logger.warning(f"Could not refresh search service {service_name}: {e}")


# =============================================================================
# COMMERCIAL & WEALTH SEARCH SERVICES
# =============================================================================

def create_client_documents_search_service(session: Session) -> None:
    """Create Cortex Search service for client documents (Corporate RM scenario)."""
    logger.info("Creating client documents search service...")
    
    # Validate required table exists
    validate_required_tables(session, ['CLIENT_DOCUMENTS'])
    
    session.sql(f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.client_documents_search_svc
            ON CONTENT
            ATTRIBUTES ID, TITLE, CLIENT_NAME, SOURCE_TYPE, PUBLISH_DATE
            WAREHOUSE = {config.SNOWFLAKE['search_warehouse']}
            TARGET_LAG = '5 minutes'
            AS 
            SELECT 
                ID,
                TITLE,
                CONTENT,
                CLIENT_NAME,
                SOURCE_TYPE,
                PUBLISH_DATE
            FROM {config.SNOWFLAKE['database']}.CURATED.CLIENT_DOCUMENTS
    """).collect()
    
    logger.info("Client documents search service created successfully")


def create_wealth_meeting_notes_search_service(session: Session) -> None:
    """Create Cortex Search service for wealth advisor meeting notes."""
    logger.info("Creating wealth meeting notes search service...")
    
    # Validate required table exists
    validate_required_tables(session, ['WEALTH_MEETING_NOTES'])
    
    session.sql(f"""
        CREATE OR REPLACE CORTEX SEARCH SERVICE {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.wealth_meeting_notes_search_svc
            ON CONTENT
            ATTRIBUTES ID, TITLE, CLIENT_NAME, ADVISOR_NAME, MEETING_DATE
            WAREHOUSE = {config.SNOWFLAKE['search_warehouse']}
            TARGET_LAG = '5 minutes'
            AS 
            SELECT 
                ID,
                TITLE,
                CONTENT,
                CLIENT_NAME,
                ADVISOR_NAME,
                MEETING_DATE
            FROM {config.SNOWFLAKE['database']}.CURATED.WEALTH_MEETING_NOTES
    """).collect()
    
    logger.info("Wealth meeting notes search service created successfully")


def main():
    """Main function for testing search services creation."""
    print("Search services creator module loaded successfully")
    print("Use create_all_search_services() method to create Cortex Search services")


if __name__ == "__main__":
    main()
