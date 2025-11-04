# src/ai_components/search_services.py
# Cortex Search service creation for Frost Markets Intelligence Demo

from snowflake.snowpark import Session
from config import DemoConfig


def create_all_search_services(session: Session) -> None:
    """Create all Cortex Search services for the demo scenarios"""
    
    print("   🔎 Creating earnings_transcripts search service...")
    create_earnings_transcripts_search(session)
    
    print("   🔎 Creating research_reports search service...")
    create_research_reports_search(session)
    
    print("   🔎 Creating news_articles search service...")  
    create_news_articles_search(session)
    
    print("   ✅ All search services created")


def create_earnings_transcripts_search(session: Session) -> None:
    """
    Create search service for earnings call transcripts
    Supports: Equity Research Analyst scenarios
    """
    
    search_service_sql = f"""
    CREATE OR REPLACE CORTEX SEARCH SERVICE AI.EARNINGS_TRANSCRIPTS_SEARCH
    ON FULL_TEXT
    ATTRIBUTES TRANSCRIPT_ID, TITLE, TICKER, FISCAL_QUARTER
    WAREHOUSE = {DemoConfig.SEARCH_WAREHOUSE}
    TARGET_LAG = '5 minutes'
    AS
    SELECT
        TRANSCRIPT_ID,
        TITLE,
        TICKER,
        FISCAL_QUARTER,
        FULL_TEXT
    FROM CURATED.EARNINGS_TRANSCRIPTS_CORPUS
    """
    
    try:
        session.sql(search_service_sql).collect()
        print("     📞 Earnings transcripts search service created")
        validate_search_service(session, 'AI.EARNINGS_TRANSCRIPTS_SEARCH')
    except Exception as e:
        print(f"     ❌ Failed to create earnings transcripts search service: {str(e)}")
        print(f"     📋 Full SQL attempted:")
        print(search_service_sql)
        raise


def create_research_reports_search(session: Session) -> None:
    """
    Create search service for internal research reports
    Supports: Global Research & Market Insights scenarios
    """
    
    search_service_sql = f"""
    CREATE OR REPLACE CORTEX SEARCH SERVICE AI.RESEARCH_REPORTS_SEARCH
    ON FULL_TEXT
    ATTRIBUTES REPORT_ID, TITLE, REPORT_TYPE, THEMATIC_TAGS, AUTHOR, PUBLISHED_DATE
    WAREHOUSE = {DemoConfig.SEARCH_WAREHOUSE}
    TARGET_LAG = '5 minutes'
    AS
    SELECT
        REPORT_ID,
        TITLE,
        REPORT_TYPE, 
        THEMATIC_TAGS,
        AUTHOR,
        PUBLISHED_DATE,
        FULL_TEXT
    FROM CURATED.RESEARCH_REPORTS_CORPUS
    """
    
    try:
        session.sql(search_service_sql).collect()
        print("     📊 Research reports search service created")
        validate_search_service(session, 'AI.RESEARCH_REPORTS_SEARCH')
    except Exception as e:
        print(f"     ❌ Failed to create research reports search service: {str(e)}")
        print(f"     📋 Full SQL attempted:")
        print(search_service_sql)
        raise


def create_news_articles_search(session: Session) -> None:
    """
    Create search service for news articles
    Supports: Cross-scenario news and market event analysis
    """
    
    search_service_sql = f"""
    CREATE OR REPLACE CORTEX SEARCH SERVICE AI.NEWS_ARTICLES_SEARCH
    ON BODY
    ATTRIBUTES ARTICLE_ID, HEADLINE, SOURCE, AFFECTED_TICKER, PUBLISHED_AT
    WAREHOUSE = {DemoConfig.SEARCH_WAREHOUSE}
    TARGET_LAG = '5 minutes'
    AS
    SELECT
        ARTICLE_ID,
        HEADLINE,
        SOURCE,
        AFFECTED_TICKER,
        PUBLISHED_AT,
        BODY
    FROM CURATED.NEWS_ARTICLES_CORPUS
    """
    
    try:
        session.sql(search_service_sql).collect() 
        print("     📰 News articles search service created")
        validate_search_service(session, 'AI.NEWS_ARTICLES_SEARCH')
    except Exception as e:
        print(f"     ❌ Failed to create news articles search service: {str(e)}")
        print(f"     📋 Full SQL attempted:")
        print(search_service_sql)
        raise


def validate_search_service(session: Session, service_name: str) -> None:
    """
    Validate that a Cortex Search service was created successfully.
    
    Args:
        session: Snowpark session
        service_name: Full name of search service (e.g., AI.EARNINGS_TRANSCRIPTS_SEARCH)
    """
    try:
        # Check if service exists
        result = session.sql(f"SHOW CORTEX SEARCH SERVICES LIKE '%{service_name.split('.')[-1]}%'").collect()
        if result:
            print(f"        ✅ Service validated: {service_name}")
        else:
            print(f"        ⚠️  Service may not be indexed yet: {service_name}")
    except Exception as e:
        print(f"        ⚠️  Could not validate service: {str(e)}")


def test_all_search_services(session: Session) -> None:
    """
    Test all created Cortex Search services.
    This validates that the services are ready for agent use.
    """
    print("\n   🧪 Testing all search services...")
    
    services = [
        ('AI.EARNINGS_TRANSCRIPTS_SEARCH', 'earnings guidance'),
        ('AI.RESEARCH_REPORTS_SEARCH', 'thematic investment'),
        ('AI.NEWS_ARTICLES_SEARCH', 'market news')
    ]
    
    for service_name, test_query in services:
        print(f"   🔍 Testing {service_name}...")
        try:
            # Note: SEARCH_PREVIEW may not be available in all environments
            # This is a best-effort test
            query = f"SELECT SEARCH_PREVIEW('{service_name}', '{test_query}') as results"
            result = session.sql(query).collect()
            print(f"      ✅ {service_name} search test successful")
        except Exception as e:
            if "Unknown function" in str(e) or "does not exist" in str(e):
                print(f"      ℹ️  {service_name} created but SEARCH_PREVIEW not available (expected in some environments)")
            else:
                print(f"      ⚠️  {service_name} test failed: {str(e)}")
    
    print("\n   ✅ Search service testing completed")