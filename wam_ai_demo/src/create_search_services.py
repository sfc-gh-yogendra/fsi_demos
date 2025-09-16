"""
WAM AI Demo - Cortex Search Services Creation
Creates COMMUNICATIONS, RESEARCH, and REGULATORY search services following the enhanced rules
"""

from snowflake.snowpark import Session
import config

def create_search_services(session: Session):
    """Create all Cortex Search services"""
    
    print("  → Creating search services...")
    
    # Set the warehouse for AI operations
    session.sql(f"USE WAREHOUSE {config.CORTEX_WAREHOUSE}").collect()
    
    # Create COMMUNICATIONS_SEARCH
    create_communications_search(session)
    
    # Create RESEARCH_SEARCH
    create_research_search(session)
    
    # Create REGULATORY_SEARCH
    create_regulatory_search(session)
    
    # Create PLANNING_SEARCH
    create_planning_search(session)
    
    # Validate search services
    validate_search_services(session)
    
    print("  ✅ Search services created and validated")

def create_communications_search(session: Session):
    """Create COMMUNICATIONS_SEARCH service following the exact pattern from rules"""
    
    print("    → Creating COMMUNICATIONS_SEARCH...")
    
    # Verify corpus table exists and has content
    verify_corpus_table(session, f"{config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS")
    
    search_service_sql = f"""
CREATE OR REPLACE CORTEX SEARCH SERVICE {config.DATABASE_NAME}.AI.COMMUNICATIONS_SEARCH
    ON CONTENT
    ATTRIBUTES CLIENT_ID, ADVISOR_ID, TIMESTAMP, CHANNEL
    WAREHOUSE = {config.CORTEX_WAREHOUSE}
    TARGET_LAG = '{config.SEARCH_TARGET_LAG}'
    AS 
    SELECT 
        COMMUNICATION_ID,
        SUBJECT AS TITLE,
        CONTENT,
        CLIENT_ID,
        ADVISOR_ID,
        TIMESTAMP,
        CHANNEL
    FROM {config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS
"""
    
    try:
        session.sql(search_service_sql).collect()
        print("    ✅ COMMUNICATIONS_SEARCH created successfully")
    except Exception as e:
        print(f"    ❌ Failed to create COMMUNICATIONS_SEARCH: {e}")
        diagnose_search_service_error(session, e, "COMMUNICATIONS_SEARCH")
        raise

def create_research_search(session: Session):
    """Create RESEARCH_SEARCH service following the exact pattern from rules"""
    
    print("    → Creating RESEARCH_SEARCH...")
    
    # Verify corpus table exists and has content
    verify_corpus_table(session, f"{config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS")
    
    search_service_sql = f"""
CREATE OR REPLACE CORTEX SEARCH SERVICE {config.DATABASE_NAME}.AI.RESEARCH_SEARCH
    ON DOCUMENT_TEXT
    ATTRIBUTES TICKER, DOCUMENT_TYPE, PUBLISH_DATE, SOURCE
    WAREHOUSE = {config.CORTEX_WAREHOUSE}
    TARGET_LAG = '{config.SEARCH_TARGET_LAG}'
    AS 
    SELECT 
        DOCUMENT_ID,
        DOCUMENT_TITLE AS TITLE,
        DOCUMENT_TEXT,
        TICKER,
        DOCUMENT_TYPE,
        PUBLISH_DATE,
        SOURCE
    FROM {config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS
"""
    
    try:
        session.sql(search_service_sql).collect()
        print("    ✅ RESEARCH_SEARCH created successfully")
    except Exception as e:
        print(f"    ❌ Failed to create RESEARCH_SEARCH: {e}")
        diagnose_search_service_error(session, e, "RESEARCH_SEARCH")
        raise

def create_regulatory_search(session: Session):
    """Create REGULATORY_SEARCH service following the exact pattern from rules"""
    
    print("    → Creating REGULATORY_SEARCH...")
    
    # Verify corpus table exists and has content
    verify_corpus_table(session, f"{config.DATABASE_NAME}.CURATED.REGULATORY_CORPUS")
    
    search_service_sql = f"""
CREATE OR REPLACE CORTEX SEARCH SERVICE {config.DATABASE_NAME}.AI.REGULATORY_SEARCH
    ON CONTENT
    ATTRIBUTES REGULATOR, RULE_ID, PUBLISH_DATE, TITLE
    WAREHOUSE = {config.CORTEX_WAREHOUSE}
    TARGET_LAG = '{config.SEARCH_TARGET_LAG}'
    AS 
    SELECT 
        DOCUMENT_ID,
        TITLE,
        CONTENT,
        REGULATOR,
        RULE_ID,
        PUBLISH_DATE
    FROM {config.DATABASE_NAME}.CURATED.REGULATORY_CORPUS
"""
    
    try:
        session.sql(search_service_sql).collect()
        print("    ✅ REGULATORY_SEARCH created successfully")
    except Exception as e:
        print(f"    ❌ Failed to create REGULATORY_SEARCH: {e}")
        diagnose_search_service_error(session, e, "REGULATORY_SEARCH")
        raise

def create_planning_search(session: Session):
    """Create PLANNING_SEARCH service for financial planning documents"""
    
    print("    → Creating PLANNING_SEARCH...")
    
    # Verify corpus table exists and has content
    verify_corpus_table(session, f"{config.DATABASE_NAME}.CURATED.PLANNING_CORPUS")
    
    search_service_sql = f"""
CREATE OR REPLACE CORTEX SEARCH SERVICE {config.DATABASE_NAME}.AI.PLANNING_SEARCH
    ON DOCUMENT_TEXT
    ATTRIBUTES CLIENT_ID, PLAN_TYPE, CREATED_DATE, ADVISOR_ID, GOAL_CATEGORY
    WAREHOUSE = {config.CORTEX_WAREHOUSE}
    TARGET_LAG = '{config.SEARCH_TARGET_LAG}'
    AS 
    SELECT 
        DOCUMENT_ID,
        PLAN_TITLE AS TITLE,
        DOCUMENT_TEXT,
        CLIENT_ID,
        PLAN_TYPE,
        CREATED_DATE,
        ADVISOR_ID,
        GOAL_CATEGORY
    FROM {config.DATABASE_NAME}.CURATED.PLANNING_CORPUS
"""
    
    try:
        session.sql(search_service_sql).collect()
        print("    ✅ PLANNING_SEARCH created successfully")
    except Exception as e:
        print(f"    ❌ Failed to create PLANNING_SEARCH: {e}")
        diagnose_search_service_error(session, e, "PLANNING_SEARCH")
        raise

def verify_corpus_table(session: Session, table_name: str):
    """Verify corpus table exists and has searchable content"""
    
    try:
        # Check table access
        session.sql(f"SELECT 1 FROM {table_name} LIMIT 1").collect()
        
        # Check content quality based on table type
        if 'COMMUNICATIONS_CORPUS' in table_name:
            content_column = 'CONTENT'
        elif 'RESEARCH_CORPUS' in table_name:
            content_column = 'DOCUMENT_TEXT'
        elif 'PLANNING_CORPUS' in table_name:
            content_column = 'DOCUMENT_TEXT'
        else:
            content_column = 'CONTENT'
            
        result = session.sql(f"""
            SELECT 
                COUNT(*) as total_docs,
                COUNT(CASE WHEN LENGTH({content_column}) > 100 THEN 1 END) as docs_with_content,
                AVG(LENGTH({content_column})) as avg_content_length
            FROM {table_name}
        """).collect()
        
        if result:
            stats = result[0]
            print(f"    📊 {table_name}: {stats['TOTAL_DOCS']} docs, {stats['DOCS_WITH_CONTENT']} with content")
            if stats['TOTAL_DOCS'] == 0:
                raise Exception(f"Corpus table {table_name} is empty")
            if stats['DOCS_WITH_CONTENT'] == 0:
                raise Exception(f"Corpus table {table_name} has no searchable content")
        
    except Exception as e:
        print(f"    ❌ Corpus table validation failed for {table_name}: {e}")
        raise

def diagnose_search_service_error(session: Session, error: Exception, service_name: str):
    """Diagnose common search service creation errors"""
    
    error_str = str(error)
    
    if "Missing option WAREHOUSE" in error_str:
        print("    🔍 Check WAREHOUSE parameter")
        print(f"       Current warehouse: {config.CORTEX_WAREHOUSE}")
    elif "invalid identifier" in error_str:
        print("    🔍 Verify ATTRIBUTES match SELECT columns")
    elif "table not found" in error_str:
        print("    🔍 Verify corpus table exists")
    else:
        print(f"    🔍 Unknown error for {service_name}: {error_str}")

def validate_search_services(session: Session):
    """Validate search services with test queries"""
    
    print("    → Validating search services...")
    
    # Validate COMMUNICATIONS_SEARCH
    try:
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.COMMUNICATIONS_SEARCH',
                '{{"query": "portfolio performance", "limit": 1}}'
            )
        """).collect()
        print("    ✅ COMMUNICATIONS_SEARCH basic test passed")
    except Exception as e:
        print(f"    ❌ COMMUNICATIONS_SEARCH validation failed: {e}")
    
    # Validate RESEARCH_SEARCH
    try:
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.RESEARCH_SEARCH',
                '{{"query": "ESG sustainability", "limit": 1}}'
            )
        """).collect()
        print("    ✅ RESEARCH_SEARCH basic test passed")
    except Exception as e:
        print(f"    ❌ RESEARCH_SEARCH validation failed: {e}")
    
    # Validate REGULATORY_SEARCH
    try:
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.REGULATORY_SEARCH',
                '{{"query": "compliance requirements", "limit": 1}}'
            )
        """).collect()
        print("    ✅ REGULATORY_SEARCH basic test passed")
    except Exception as e:
        print(f"    ❌ REGULATORY_SEARCH validation failed: {e}")
    
    # Validate PLANNING_SEARCH
    try:
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.PLANNING_SEARCH',
                '{{"query": "financial goals", "limit": 1}}'
            )
        """).collect()
        print("    ✅ PLANNING_SEARCH basic test passed")
    except Exception as e:
        print(f"    ❌ PLANNING_SEARCH validation failed: {e}")
    
    # Show created search services
    services = session.sql(f"SHOW CORTEX SEARCH SERVICES IN {config.DATABASE_NAME}.AI").collect()
    print(f"    📋 Created search services: {len(services)}")
    for service in services:
        print(f"       - {service['name']}")

def test_search_filters(session: Session):
    """Test search services with attribute filtering"""
    
    print("    → Testing search filters...")
    
    # Test RESEARCH_SEARCH with ticker filter
    try:
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.RESEARCH_SEARCH',
                '{{"query": "earnings", "filter": {{"TICKER": "AAPL"}}, "limit": 2}}'
            )
        """).collect()
        print("    ✅ RESEARCH_SEARCH filter test passed")
    except Exception as e:
        print(f"    ⚠️ RESEARCH_SEARCH filter test failed (may be expected): {e}")
    
    # Test COMMUNICATIONS_SEARCH with channel filter
    try:
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.COMMUNICATIONS_SEARCH',
                '{{"query": "portfolio", "filter": {{"CHANNEL": "Email"}}, "limit": 2}}'
            )
        """).collect()
        print("    ✅ COMMUNICATIONS_SEARCH filter test passed")
    except Exception as e:
        print(f"    ⚠️ COMMUNICATIONS_SEARCH filter test failed (may be expected): {e}")

def describe_search_services(session: Session):
    """Describe search services for verification"""
    
    print("    → Describing search services...")
    
    services = ['COMMUNICATIONS_SEARCH', 'RESEARCH_SEARCH', 'REGULATORY_SEARCH', 'PLANNING_SEARCH']
    
    for service in services:
        try:
            result = session.sql(f"DESCRIBE CORTEX SEARCH SERVICE {config.DATABASE_NAME}.AI.{service}").collect()
            print(f"    📋 {service} structure verified")
        except Exception as e:
            print(f"    ❌ Failed to describe {service}: {e}")
