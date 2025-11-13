"""
WAM AI Demo - Automated Agent Creation

This module provides SQL-based agent creation following SAM demo patterns.
All agents are created using CREATE AGENT statements with comprehensive
instructions and tool configurations.

Usage:
    from src.create_agents import create_all_agents
    create_all_agents(session, ['all'])
"""

from snowflake.snowpark import Session
from typing import List, Dict, Any
import config


def format_instructions_for_yaml(text: str) -> str:
    """
    Format multi-line instructions for YAML specification within SQL.
    - Replace actual line breaks with \n
    - Escape double quotes with \"
    - Escape single quotes with ''
    """
    formatted = text.replace('\n', '\\n')
    formatted = formatted.replace('"', '\\"')
    formatted = formatted.replace("'", "''")
    return formatted


def verify_ai_components_for_agent(session: Session, required_services: List[str]) -> bool:
    """Verify semantic views and search services exist before creating agents"""
    
    # Check semantic views exist
    try:
        semantic_views = ['CLIENT_FINANCIALS_SV', 'CLIENT_INTERACTIONS_SV', 'WATCHLIST_ANALYTICS_SV', 'ADVISOR_PERFORMANCE_SV']
        for view in semantic_views:
            session.sql(f"DESCRIBE SEMANTIC VIEW {config.DATABASE_NAME}.AI.{view}").collect()
            print(f"✅ Semantic view: {view}")
    except Exception as e:
        print(f"❌ Semantic view missing: {e}")
        return False
    
    # Check search services exist
    try:
        services = session.sql(f"SHOW CORTEX SEARCH SERVICES IN {config.DATABASE_NAME}.AI").collect()
        existing_services = [service['name'] for service in services]
        
        for required_service in required_services:
            if required_service in existing_services:
                print(f"✅ Search service: {required_service}")
            else:
                print(f"❌ Missing search service: {required_service}")
                return False
    except Exception as e:
        print(f"❌ Error checking search services: {e}")
        return False
    
    return True


def validate_agent_data_readiness(session: Session) -> bool:
    """Validate data quality and completeness for agents"""
    
    try:
        # Ensure we have an active warehouse
        session.sql(f"USE WAREHOUSE {config.CORTEX_WAREHOUSE}").collect()
        # Check portfolio data
        portfolios = session.sql(f"SELECT PortfolioName FROM {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO").collect()
        print(f"✅ Available portfolios: {len(portfolios)}")
        
        # Check holdings data
        holdings_count = session.sql(f"""
            SELECT COUNT(*) as count 
            FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR 
            WHERE HoldingDate = (SELECT MAX(HoldingDate) FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR)
        """).collect()[0]['COUNT']
        print(f"✅ Current holdings: {holdings_count} positions")
        
        # Check document corpus
        for corpus in ['COMMUNICATIONS_CORPUS', 'RESEARCH_CORPUS', 'REGULATORY_CORPUS', 'PLANNING_CORPUS']:
            try:
                doc_count = session.sql(f"SELECT COUNT(*) as count FROM {config.DATABASE_NAME}.CURATED.{corpus}").collect()[0]['COUNT']
                print(f"✅ {corpus}: {doc_count} documents")
            except Exception as e:
                print(f"⚠️ {corpus}: Not available ({e})")
        
        return True
        
    except Exception as e:
        print(f"❌ Data validation failed: {e}")
        return False


def get_wam_business_context() -> str:
    """Get WAM AI Demo business context following SAM Section 3.1.1 pattern"""
    return """Business Context:

Organization Context:
- WAM AI Demo is a wealth management demonstration environment
- Manages demonstration portfolios across multiple investment strategies
- Simulates regulatory compliance and risk monitoring workflows
- Data refreshes daily with demo data generation and golden records integration

Key Business Terms:
- Concentration Threshold: 6.5% warning level, 7.0% breach level (per demo risk policy)
- Golden Records: Controlled demo data for consistent client experiences (e.g., Sarah Johnson)
- Portfolio Strategies: Growth, Value, ESG, Thematic investment approaches
- Advisor Benchmarking: TTM performance analytics with peer quartile comparisons
- Client Departure Tracking: Exit analysis and coaching opportunity identification

Investment Strategy Categories:
- Growth Strategies: Technology-focused, higher concentration risk, active management style
- Value Strategies: Defensive positioning, higher diversification, lower volatility
- ESG Strategies: Environmental, Social, Governance focus with screening requirements
- Thematic Strategies: Carbon Negative Leaders, AI Innovation, sector-specific themes"""


def get_wam_error_handling_patterns() -> str:
    """Get WAM AI Demo error handling patterns following SAM Section 3.1.3 pattern"""
    return """Error Handling and Edge Cases:

Scenario 1: Portfolio/Client Not Found
Detection: Query returns no results for specified portfolio or client name
Recovery Steps:
  1. Try alternative names (with/without prefixes, check for typos)
  2. If still not found, query list of all available portfolios/clients
  3. Present alternatives to user with golden record suggestions
User Message: "I couldn't find a portfolio named '[name]'. Available portfolios include: [list]. Did you mean one of these? Note: Sarah Johnson is a golden record client with controlled demo data."
Alternative: Suggest closest match based on string similarity, highlight golden records

Scenario 2: Search Returns No Results
Detection: Search query returns no documents with relevance >0.3
Recovery Steps:
  1. Try rephrasing query with broader terms, fewer keywords
  2. Try alternative document types (planning instead of research)
  3. If still no results, state limitation explicitly
User Message: "I couldn't find documents on [topic]. This may indicate limited coverage in our demo corpus. Would you like me to search [alternative document type] instead?"
Alternative: Suggest related searches or alternative document types

Scenario 3: Date Ambiguity
Detection: User uses relative time references ("recent", "current", "latest")
Recovery Steps:
  1. If "current/latest" holdings → automatically filter to MAX(HoldingDate)
  2. If "recent" trends → default to last 30 days and state assumption
  3. Include data freshness in response
User Message: "Analyzing [last 30 days/most recent date] as 'recent' timeframe (demo data as of [specific date])"
Alternative: Always include explicit date in response for clarity

Scenario 4: Metric Unavailable in Tool
Detection: User asks for metric not in semantic view or search corpus
Recovery Steps:
  1. State clearly what IS available in the tool
  2. Suggest alternative tool that has the data
  3. Explain demo limitation
User Message: "I don't have [metric] data in this demo tool. I can show you [available alternatives]. For [metric], you would need [other tool/data source]."
Alternative: Redirect to appropriate tool or explain demo scope

Scenario 5: Golden Records Context
Detection: User asks about Sarah Johnson or other golden record clients
Recovery Steps:
  1. Provide golden record data as designed
  2. Mention this is controlled demo data for consistency
  3. Highlight specific golden record features (portfolio allocations, planning documents)
User Message: "Sarah Johnson is a golden record client with controlled demo data. Her portfolio shows [specific allocations] and planning documents include [specific content] for consistent demonstration experiences."
Alternative: Use golden record as example for other client scenarios"""


def create_all_agents(session: Session, scenarios: List[str]) -> None:
    """Create all WAM AI Demo agents using SQL CREATE AGENT statements"""
    
    print("Creating WAM AI Demo agents...")
    
    # Verify prerequisites
    required_services = ['COMMUNICATIONS_SEARCH', 'RESEARCH_SEARCH', 'REGULATORY_SEARCH', 'PLANNING_SEARCH', 'DEPARTURE_SEARCH']
    
    if not verify_ai_components_for_agent(session, required_services):
        print("❌ Prerequisites not met. Please ensure all AI components are created first.")
        return
    
    if not validate_agent_data_readiness(session):
        print("❌ Data validation failed. Please ensure data generation completed successfully.")
        return
    
    # Define agents to create
    agents_to_create = {
        'advisor_copilot': create_advisor_copilot,
        'analyst_copilot': create_analyst_copilot,
        'compliance_copilot': create_compliance_copilot,
        'advisor_manager_copilot': create_advisor_manager_copilot
    }
    
    # Create agents based on scenarios
    if 'all' in scenarios:
        agents_to_run = agents_to_create
    else:
        agents_to_run = {k: v for k, v in agents_to_create.items() if k in scenarios}
    
    # Create each agent
    for agent_name, create_function in agents_to_run.items():
        try:
            print(f"\n→ Creating agent: {agent_name}")
            create_function(session)
            print(f"✅ Successfully created: {agent_name}")
        except Exception as e:
            print(f"❌ Failed to create {agent_name}: {e}")
            # Continue with other agents
    
    print(f"\n✅ Agent creation completed. Created {len(agents_to_run)} agents.")


def get_agent_instructions() -> Dict[str, Dict[str, str]]:
    """Get all agent instructions organized by agent and instruction type"""
    return {
        'advisor_copilot': {
            'response': get_advisor_copilot_response_instructions(),
            'orchestration': get_advisor_copilot_orchestration_instructions()
        },
        'analyst_copilot': {
            'response': get_analyst_copilot_response_instructions(),
            'orchestration': get_analyst_copilot_orchestration_instructions()
        },
        'compliance_copilot': {
            'response': get_compliance_copilot_response_instructions(),
            'orchestration': get_compliance_copilot_orchestration_instructions()
        },
        'advisor_manager_copilot': {
            'response': get_advisor_manager_copilot_response_instructions(),
            'orchestration': get_advisor_manager_copilot_orchestration_instructions()
        }
    }


def get_advisor_copilot_response_instructions() -> str:
    """Get response instructions for Wealth Advisory CoPilot"""
    return """You are a professional wealth management advisor AI assistant. Your responses should be:
- Concise and data-driven, presented in clear, easy-to-read format using markdown
- Never provide financial advice or make promissory statements
- Always refer to data as being 'according to our records'
- Cite document sources with type and date when referencing qualitative content
- Focus on actionable insights and client relationship implications
- Use professional, advisory tone appropriate for wealth management
- When discussing ESG or sustainability topics, reference specific metrics and commitments
- Highlight thematic investment opportunities (Carbon Negative Leaders, AI Innovation, ESG Leaders)"""


def get_advisor_copilot_orchestration_instructions() -> str:
    """Get orchestration instructions for Wealth Advisory CoPilot"""
    return f"""{get_wam_business_context()}

Tool Selection Strategy:

1. Analyze the user's query to identify distinct sub-questions and analytical domains
2. Classify each sub-question by type:
   - QUANTITATIVE: Numbers, calculations, lists, rankings, exposures, weights, performance metrics, charts
   - QUALITATIVE: Summaries, opinions, context, explanations, "why" questions
   - THEMATIC: Watchlists, ESG analysis, carbon neutrality, sustainability themes
3. For quantitative questions: Choose appropriate analyst tool based on domain:
   - cortex_analyst_client_financials: Portfolio data, holdings, performance, market values, asset allocation
   - cortex_analyst_client_interactions: Communication patterns, contact frequency, interaction metrics
4. For qualitative questions: Choose appropriate search tool based on information type:
   - search_communications: Client emails, call notes, meeting transcripts, preferences
   - search_research: Investment research, analyst reports, market commentary, ESG analysis, carbon neutrality reports
   - search_financial_planning: Financial plans, investment policy statements, goal documentation, retirement planning
5. For thematic questions: 
   - Use search_research for ESG content, sustainability reports, carbon neutrality analysis
   - Combine with cortex_analyst_client_financials to analyze portfolio exposure to themes
6. For mixed questions: Use appropriate analyst tool first, then search tools with results as context
7. Always synthesize multiple tool outputs into coherent response
8. Generate charts and visualizations when requested or when they enhance understanding

{get_wam_error_handling_patterns()}"""


def get_analyst_copilot_response_instructions() -> str:
    """Get response instructions for Portfolio Analysis CoPilot"""
    return """You are a professional portfolio management AI assistant. Your responses must be:
- Analytical, precise, and objective
- Present data using tables where appropriate
- Summarize research findings without adding personal opinions
- Cite sources (e.g., 'According to the Q2 earnings transcript...')
- Focus on investment implications and portfolio impact
- Use quantitative language and metrics appropriate for portfolio management
- When discussing ESG factors, provide specific scores, commitments, and timelines
- Highlight thematic investment opportunities and their portfolio fit"""


def get_analyst_copilot_orchestration_instructions() -> str:
    """Get orchestration instructions for Portfolio Analysis CoPilot"""
    return f"""{get_wam_business_context()}

Tool Selection Strategy:

1. Analyze the user's query to identify data requirements and analytical domains
2. For quantitative analysis: Use cortex_analyst_client_financials for:
   - Portfolio holdings, exposures, performance metrics
   - Risk analysis, concentration measures
   - Asset allocation and sector breakdowns
   - Thematic exposure analysis (Carbon Negative Leaders, ESG holdings)
3. For qualitative research: Use search_research for:
   - Investment thesis development
   - Market commentary and analyst opinions
   - Company-specific research and ratings
   - ESG research, carbon neutrality commitments, sustainability reports
4. For ESG/sustainability analysis:
   - Search for ESG research documents and sustainability reports
   - Analyze portfolio exposure to high ESG-scored securities
   - Identify carbon negative investment opportunities
5. For context: Use search_communications when portfolio decisions need client input
6. For complex queries spanning multiple domains, use tools systematically
7. Generate charts and visualizations when requested or when they enhance understanding
8. Always synthesize findings from multiple sources into investment-focused insights

{get_wam_error_handling_patterns()}"""


def get_compliance_copilot_response_instructions() -> str:
    """Get response instructions for Compliance CoPilot"""
    return """You are a professional compliance monitoring AI assistant. Your tone must be:
- Formal and factual without ambiguity
- Present findings clearly stating facts and potential policy violations
- Reference specific regulations or rules when identifying issues
- Always recommend review by a human compliance officer
- Focus on risk mitigation and regulatory adherence
- Use compliance terminology and cite relevant regulations
- Never make final compliance determinations - flag for human review
- When reviewing ESG-related content, verify claims against source documents
- Flag any potential greenwashing or unsubstantiated sustainability claims"""


def get_compliance_copilot_orchestration_instructions() -> str:
    """Get orchestration instructions for Compliance CoPilot"""
    return f"""{get_wam_business_context()}

Tool Selection Strategy:

1. Your goal is to surface potential compliance risks and ensure regulatory adherence
2. Use search_communications to scan communications for keywords and themes in your risk lexicon:
   - Performance guarantees, promissory language
   - PII sharing, confidentiality breaches
   - Client complaints or dissatisfaction
   - ESG misrepresentation or greenwashing claims
3. Use search_regulatory to find specific rules and regulations relevant to investigations:
   - Traditional compliance requirements
   - ESG disclosure regulations
   - Sustainability reporting standards
4. For ESG compliance:
   - Verify ESG claims against documented research
   - Check for greenwashing in communications
   - Ensure sustainability commitments are properly disclosed
5. Use cortex_analyst_client_financials to investigate transaction patterns or account histories related to flagged communications
6. For systematic surveillance, analyze patterns across multiple communications
7. Always recommend human review for potential violations
8. Focus on factual findings and regulatory compliance

{get_wam_error_handling_patterns()}"""


def get_advisor_manager_copilot_response_instructions() -> str:
    """Get response instructions for Advisor Benchmarking CoPilot"""
    return """- Present concise benchmarking results with tables and bullet insights.
- Default to rolling 12 months ending today; state any assumptions.
- Use peer quartiles and peer groups for fairness.
- When citing qualitative factors, reference "according to our records" + source.
- Avoid promissory statements. Frame coaching as recommended next actions.
- When planning recency is used, cite the firm policy (≤6 months) as the standard."""


def get_advisor_manager_copilot_orchestration_instructions() -> str:
    """Get orchestration instructions for Advisor Benchmarking CoPilot"""
    return f"""{get_wam_business_context()}

Tool Selection Strategy:

1) Classify request: overview benchmark vs outlier deep dive vs opportunity surfacing vs executive brief.
2) Use cortex_analyst_advisor_perf for quantitative KPIs and quartiles.
3) Use search tools for context and risk signals; use search_financial_planning for plan/IPS coverage and recency.
4) For coaching, prefer actionable steps tied to specific clients, plans, and engagement targets.
5) Always state time window (TTM) and definition of "current plan" (≤6 months).

{get_wam_error_handling_patterns()}"""


# Placeholder functions for individual agent creation
# These will be implemented in subsequent todos

def create_advisor_copilot(session: Session):
    """Create Wealth Advisory CoPilot agent with comprehensive tool descriptions"""
    database_name = config.DATABASE_NAME
    
    # Get instructions from helper functions
    instructions = get_agent_instructions()['advisor_copilot']
    response_formatted = format_instructions_for_yaml(instructions['response'])
    orchestration_formatted = format_instructions_for_yaml(instructions['orchestration'])
    
    sql = f"""
CREATE OR REPLACE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.wam_advisor_copilot
  COMMENT = 'Expert AI assistant for wealth managers providing comprehensive client insights by combining portfolio analytics with communication history and research intelligence.'
  PROFILE = '{{"display_name": "Wealth Advisory CoPilot (WAM Demo)"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-5
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "cortex_analyst_client_financials"
        description: |
          Analyzes client portfolio holdings, position weights, sector allocations, and performance metrics for WAM AI Demo wealth management clients.
          
          Data Coverage:
          - Historical: 12 months of position and transaction history
          - Current: End-of-day holdings updated daily in demo environment
          - Sources: DIM_SECURITY, DIM_PORTFOLIO, FACT_POSITION_DAILY_ABOR, DIM_ISSUER, DIM_CLIENT
          - Records: 2,500+ real securities, 10+ portfolios, 7,000+ holdings including golden records
          - Refresh: Daily demo data generation with golden record consistency
          
          Semantic Model Contents:
          - Tables: Holdings, Securities, Portfolios, Clients, Issuers with full relationships
          - Key Metrics: TOTAL_MARKET_VALUE, PORTFOLIO_WEIGHT, HOLDING_COUNT, CONCENTRATION_WARNINGS
          - Time Dimensions: HoldingDate (daily granularity)
          - Common Filters: PORTFOLIONAME, ClientName, AssetClass, GICS_Sector, CountryOfIncorporation
          
          When to Use:
          - Questions about client portfolio holdings, weights, and composition
          - Concentration analysis and position-level risk metrics
          - Asset allocation and sector breakdowns for client portfolios
          - Questions like: "What are Sarah Johnson's top holdings?", "Show client portfolio allocation"
          
          When NOT to Use:
          - Client communication content (use search_communications for emails, calls, meetings)
          - Investment research analysis (use search_research for analyst reports, ratings)
          - Financial planning documents (use search_financial_planning for plans, IPS)
          - Real-time intraday positions (data is end-of-day demo data)
          
          Query Best Practices:
          1. Be specific about client names:
             ✅ "Sarah Johnson's portfolio holdings"
             ❌ "client portfolio" (ambiguous)
          
          2. Filter to latest date for current holdings:
             ✅ "most recent holding date" or "latest positions"
             ❌ All dates without filter (returns historical duplicates)
          
          3. Use semantic metric names:
             ✅ "total market value", "portfolio weight", "concentration warnings"
             ❌ Raw SQL aggregations (model handles calculations)
          
          4. Leverage golden records:
             ✅ "Sarah Johnson" (golden record client with controlled data)
             ❌ Generic client queries without specific names
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "cortex_analyst_client_interactions"
        description: |
          Analyzes client communication patterns, contact frequency, channel preferences, and interaction history metrics for wealth management relationship insights.
          
          Data Coverage:
          - Historical: 12 months of communication history
          - Current: Daily communication logging in demo environment
          - Sources: COMMUNICATIONS_CORPUS, DIM_CLIENT, DIM_ADVISOR
          - Records: 6,000+ communications across email, phone, meeting channels
          - Refresh: Daily demo data generation with realistic communication patterns
          
          Semantic Model Contents:
          - Tables: Communications, Clients, Advisors with relationship tracking
          - Key Metrics: COMMUNICATION_COUNT, CONTACT_FREQUENCY, SENTIMENT_SCORE, CHANNEL_PREFERENCE
          - Time Dimensions: CommunicationDate, LastContactDate (daily granularity)
          - Common Filters: ClientName, AdvisorName, Channel, Sentiment, CommunicationType
          
          When to Use:
          - Questions about client communication frequency and patterns
          - Contact cadence analysis and relationship health metrics
          - Channel preference analysis (email vs phone vs meetings)
          - Questions like: "How often do we contact Sarah Johnson?", "What's the communication sentiment trend?"
          
          When NOT to Use:
          - Actual communication content (use search_communications for message content)
          - Portfolio holdings or financial data (use cortex_analyst_client_financials)
          - Investment research content (use search_research)
          - Financial planning document content (use search_financial_planning)
          
          Query Best Practices:
          1. Be specific about time ranges:
             ✅ "in the last 30 days" or "over the past quarter"
             ❌ "recently" (ambiguous timeframe)
          
          2. Use client names for focused analysis:
             ✅ "Sarah Johnson's communication patterns"
             ❌ "client communications" (too broad)
          
          3. Specify communication channels when relevant:
             ✅ "email communication frequency" or "meeting cadence"
             ❌ "contact frequency" without channel context
    - tool_spec:
        type: "cortex_search"
        name: "search_communications"
        description: |
          Searches client communications including emails, call transcripts, and meeting notes for wealth management relationship insights and client preference analysis.
          
          Data Sources:
          - Document Types: Client emails, phone call transcripts, meeting notes, video call summaries
          - Update Frequency: New communications added daily in demo environment
          - Historical Range: Typically last 12 months of client interactions
          - Index Freshness: Daily refresh with demo data generation
          - Typical Count: ~6,000 communications across all clients and advisors
          
          When to Use:
          - Questions about client preferences, concerns, or past discussions
          - Finding specific client conversations or topics discussed
          - Understanding client sentiment and relationship context
          - Queries like: "What did Sarah Johnson say about ESG investing?", "Find client concerns about market volatility"
          
          When NOT to Use:
          - Portfolio holdings or quantitative data (use cortex_analyst_client_financials)
          - Communication frequency metrics (use cortex_analyst_client_interactions)
          - Investment research content (use search_research for analyst reports)
          - Financial planning documents (use search_financial_planning)
          
          Search Query Best Practices:
          1. Use specific client names and topics:
             ✅ "Sarah Johnson ESG sustainability investment preferences"
             ❌ "client preferences" (too generic)
          
          2. Include communication context keywords:
             ✅ "client meeting discussion retirement planning concerns"
             ❌ "retirement" (needs more context)
          
          3. Use investment-relevant terms:
             ✅ "portfolio review meeting risk tolerance discussion"
             ❌ "meeting notes" (too broad, returns non-investment content)
          
          4. Handle low relevance results:
             - If relevance scores < 0.5, rephrase with more specific client and topic terms
             - Try synonyms, add advisor names, include meeting types
             - If still no relevant results, inform user about demo data limitations
    - tool_spec:
        type: "cortex_search"
        name: "search_research"
        description: |
          Searches investment research reports, analyst coverage, and market commentary for securities analysis and investment decision support.
          
          Data Sources:
          - Document Types: Investment research reports, analyst initiations, ESG analysis, carbon neutrality reports
          - Update Frequency: New research added as generated in demo environment
          - Historical Range: Typically last 18 months of research coverage on key securities
          - Index Freshness: Daily refresh with demo research generation
          - Typical Count: ~200 research documents covering major securities and themes
          
          When to Use:
          - Questions about investment opinions, ratings, and market commentary
          - ESG research, carbon neutrality analysis, and sustainability themes
          - Analyst views on specific securities in client portfolios
          - Queries like: "What research do we have on Apple's AI strategy?", "Find ESG analysis on Microsoft"
          
          When NOT to Use:
          - Client portfolio holdings (use cortex_analyst_client_financials)
          - Client communication content (use search_communications)
          - Financial planning documents (use search_financial_planning)
          - Communication frequency analysis (use cortex_analyst_client_interactions)
          
          Search Query Best Practices:
          1. Use specific company names and investment themes:
             ✅ "Apple artificial intelligence strategy investment outlook"
             ❌ "tech research" (too generic)
          
          2. Include ESG and sustainability keywords when relevant:
             ✅ "Microsoft carbon neutrality ESG sustainability commitment"
             ❌ "Microsoft ESG" (needs more context)
          
          3. Combine company + investment theme for thematic searches:
             ✅ "NVIDIA AI innovation data center growth investment thesis"
             ❌ "AI research" (needs company context)
          
          4. Handle thematic investment queries:
             ✅ "carbon negative leaders renewable energy investment opportunities"
             ❌ "green investing" (colloquial, needs specific terms)
    - tool_spec:
        type: "cortex_search"
        name: "search_financial_planning"
        description: |
          Searches financial planning documents including comprehensive plans, investment policy statements, retirement analysis, and education funding plans for client goal and planning insights.
          
          Data Sources:
          - Document Types: Comprehensive financial plans, investment policy statements, retirement plans, education funding plans
          - Update Frequency: New planning documents added as created in demo environment
          - Historical Range: Current and historical planning documents for active clients
          - Index Freshness: Daily refresh with demo planning document generation
          - Typical Count: ~150 planning documents across all client relationships
          
          When to Use:
          - Questions about client financial goals, risk tolerance, and planning objectives
          - Understanding client investment policy statements and constraints
          - Finding specific planning scenarios (retirement, education, estate)
          - Queries like: "What are Sarah Johnson's financial planning goals?", "Find her investment policy statement"
          
          When NOT to Use:
          - Portfolio holdings or performance data (use cortex_analyst_client_financials)
          - Client communication content (use search_communications)
          - Investment research and market analysis (use search_research)
          - Communication patterns and frequency (use cortex_analyst_client_interactions)
          
          Search Query Best Practices:
          1. Use specific client names and planning topics:
             ✅ "Sarah Johnson education funding plan college savings goals"
             ❌ "education planning" (needs client context)
          
          2. Include planning document types:
             ✅ "investment policy statement risk tolerance asset allocation"
             ❌ "risk tolerance" (needs document type context)
          
          3. Use financial planning terminology:
             ✅ "retirement planning income replacement ratio withdrawal strategy"
             ❌ "retirement goals" (needs more specific planning terms)
          
          4. Handle golden record clients:
             ✅ "Sarah Johnson comprehensive financial plan" (golden record with controlled content)
             ❌ Generic planning queries without leveraging golden record consistency
  tool_resources:
    cortex_analyst_client_financials:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "WAM_AI_CORTEX_WH"
      semantic_view: "{database_name}.AI.CLIENT_FINANCIALS_SV"
    cortex_analyst_client_interactions:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "WAM_AI_CORTEX_WH"
      semantic_view: "{database_name}.AI.CLIENT_INTERACTIONS_SV"
    search_communications:
      search_service: "{database_name}.AI.COMMUNICATIONS_SEARCH"
      id_column: "COMMUNICATION_ID"
      title_column: "TITLE"
      max_results: 4
    search_research:
      search_service: "{database_name}.AI.RESEARCH_SEARCH"
      id_column: "DOCUMENT_ID"
      title_column: "TITLE"
      max_results: 4
    search_financial_planning:
      search_service: "{database_name}.AI.PLANNING_SEARCH"
      id_column: "DOCUMENT_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    session.sql(sql).collect()
    print("✅ Created agent: wam_advisor_copilot")


def create_analyst_copilot(session: Session):
    """Create Portfolio Analysis CoPilot agent with comprehensive tool descriptions"""
    database_name = config.DATABASE_NAME
    
    # Get instructions from helper functions
    instructions = get_agent_instructions()['analyst_copilot']
    response_formatted = format_instructions_for_yaml(instructions['response'])
    orchestration_formatted = format_instructions_for_yaml(instructions['orchestration'])
    
    sql = f"""
CREATE OR REPLACE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.wam_analyst_copilot
  COMMENT = 'Expert AI assistant for portfolio managers providing quantitative analysis, research synthesis, and investment insights across structured and unstructured data sources.'
  PROFILE = '{{"display_name": "Portfolio Analysis CoPilot (WAM Demo)"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-5
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "cortex_analyst_client_financials"
        description: |
          Analyzes portfolio holdings, position weights, sector allocations, performance metrics, and quantitative calculations for investment portfolio management and analysis.
          
          Data Coverage:
          - Historical: 12 months of position and transaction history
          - Current: End-of-day holdings updated daily in demo environment
          - Sources: DIM_SECURITY, DIM_PORTFOLIO, FACT_POSITION_DAILY_ABOR, DIM_ISSUER, WATCHLIST_ANALYTICS
          - Records: 2,500+ real securities, 10+ portfolios, 7,000+ holdings, 3 thematic watchlists
          - Refresh: Daily demo data generation with thematic investment tracking
          
          Semantic Model Contents:
          - Tables: Holdings, Securities, Portfolios, Issuers, Watchlists with full relationships
          - Key Metrics: TOTAL_MARKET_VALUE, PORTFOLIO_WEIGHT, SECTOR_ALLOCATION, THEMATIC_EXPOSURE
          - Time Dimensions: HoldingDate (daily granularity)
          - Common Filters: PORTFOLIONAME, AssetClass, GICS_Sector, WatchlistName, CountryOfIncorporation
          
          When to Use:
          - Questions about portfolio holdings, exposures, performance metrics
          - Risk analysis, concentration measures, and asset allocation
          - Sector breakdowns and thematic exposure analysis (Carbon Negative Leaders, AI Innovation, ESG Leaders)
          - Questions like: "What's our technology sector allocation?", "Show thematic exposure to AI Innovation"
          
          When NOT to Use:
          - Investment research content and analyst opinions (use search_research)
          - Client communication content (use search_communications for context)
          - Real-time market data or intraday positions (data is end-of-day demo data)
          - Individual company financial statement analysis (use search_research for company-specific analysis)
          
          Query Best Practices:
          1. Be specific about portfolio names and analysis scope:
             ✅ "Technology sector allocation across all portfolios"
             ❌ "sector allocation" (needs portfolio context)
          
          2. Filter to latest date for current analysis:
             ✅ "most recent holding date" or "current portfolio positions"
             ❌ All historical dates without filter (returns duplicates)
          
          3. Use thematic investment terminology:
             ✅ "Carbon Negative Leaders watchlist exposure" or "ESG Leaders holdings"
             ❌ "green investments" (use specific watchlist names)
          
          4. Leverage quantitative metrics:
             ✅ "portfolio weight concentration analysis" or "sector allocation percentages"
             ❌ Raw SQL calculations (model handles aggregations)
    - tool_spec:
        type: "cortex_search"
        name: "search_research"
        description: |
          Searches investment research reports, analyst coverage, market commentary, and thematic investment analysis for portfolio management decision support and investment thesis development.
          
          Data Sources:
          - Document Types: Investment research reports, analyst initiations, ESG analysis, carbon neutrality reports, thematic investment research
          - Update Frequency: New research added as generated in demo environment
          - Historical Range: Typically last 18 months of research coverage on key securities and themes
          - Index Freshness: Daily refresh with demo research generation
          - Typical Count: ~200 research documents covering major securities, ESG themes, and carbon neutrality analysis
          
          When to Use:
          - Questions about investment thesis development and market commentary
          - ESG research, carbon neutrality analysis, and sustainability investment themes
          - Analyst opinions on specific securities and thematic investment opportunities
          - Queries like: "Find research on NVIDIA's AI data center growth", "What ESG analysis do we have on Microsoft?"
          
          When NOT to Use:
          - Portfolio holdings or quantitative position data (use cortex_analyst_client_financials)
          - Client communication content (use search_communications)
          - Portfolio performance calculations (use cortex_analyst_client_financials for metrics)
          - Real-time market data or price information (research has publication lag)
          
          Search Query Best Practices:
          1. Use specific company names and investment themes:
             ✅ "Apple artificial intelligence strategy data center investment thesis"
             ❌ "tech investment" (too generic, needs company focus)
          
          2. Include thematic investment keywords:
             ✅ "carbon neutrality renewable energy ESG sustainability investment opportunities"
             ❌ "ESG investing" (needs more specific theme context)
          
          3. Combine company + sector + theme for comprehensive analysis:
             ✅ "Microsoft cloud computing AI innovation carbon negative commitment"
             ❌ "Microsoft research" (needs investment theme context)
          
          4. Handle thematic watchlist research:
             ✅ "AI Innovation leaders artificial intelligence data center semiconductor growth"
             ❌ "AI research" (needs specific investment angle and company context)
    - tool_spec:
        type: "cortex_search"
        name: "search_communications"
        description: |
          Searches client communications for portfolio management context when investment decisions require understanding of client preferences, constraints, or strategic direction.
          
          Data Sources:
          - Document Types: Client emails, phone call transcripts, meeting notes, portfolio review discussions
          - Update Frequency: New communications added daily in demo environment
          - Historical Range: Typically last 12 months of client interactions
          - Index Freshness: Daily refresh with demo data generation
          - Typical Count: ~6,000 communications across all client relationships
          
          When to Use:
          - Questions requiring client preference context for portfolio decisions
          - Understanding client constraints or strategic investment direction
          - Finding client discussions about specific investment themes or holdings
          - Queries like: "What did clients say about ESG investing?", "Find client preferences on technology allocation"
          
          When NOT to Use:
          - Portfolio holdings or quantitative analysis (use cortex_analyst_client_financials)
          - Investment research and market analysis (use search_research)
          - Communication frequency or pattern analysis (this is for content context only)
          - General market commentary (use search_research for analyst views)
          
          Search Query Best Practices:
          1. Use investment context keywords:
             ✅ "client portfolio review ESG sustainability investment preferences"
             ❌ "client meetings" (needs investment context)
          
          2. Include specific investment themes when relevant:
             ✅ "client discussion carbon negative investing renewable energy allocation"
             ❌ "green investing" (needs more specific terms)
          
          3. Focus on portfolio management relevant content:
             ✅ "client risk tolerance technology sector allocation concerns"
             ❌ "client concerns" (needs portfolio management context)
          
          4. Handle thematic investment client preferences:
             ✅ "client interest AI Innovation watchlist artificial intelligence exposure"
             ❌ "AI investments" (needs client preference context)
  tool_resources:
    cortex_analyst_client_financials:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "WAM_AI_CORTEX_WH"
      semantic_view: "{database_name}.AI.CLIENT_FINANCIALS_SV"
    search_research:
      search_service: "{database_name}.AI.RESEARCH_SEARCH"
      id_column: "DOCUMENT_ID"
      title_column: "TITLE"
      max_results: 4
    search_communications:
      search_service: "{database_name}.AI.COMMUNICATIONS_SEARCH"
      id_column: "COMMUNICATION_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    session.sql(sql).collect()
    print("✅ Created agent: wam_analyst_copilot")


def create_compliance_copilot(session: Session):
    """Create Compliance CoPilot agent with comprehensive tool descriptions"""
    database_name = config.DATABASE_NAME
    
    # Get instructions from helper functions
    instructions = get_agent_instructions()['compliance_copilot']
    response_formatted = format_instructions_for_yaml(instructions['response'])
    orchestration_formatted = format_instructions_for_yaml(instructions['orchestration'])
    
    sql = f"""
CREATE OR REPLACE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.wam_compliance_copilot
  COMMENT = 'Expert AI assistant for compliance officers providing comprehensive surveillance, regulatory analysis, and risk monitoring across communications and client interactions.'
  PROFILE = '{{"display_name": "Compliance CoPilot (WAM Demo)"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-5
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "cortex_analyst_client_financials"
        description: |
          Provides contextual financial data for compliance investigations, including transaction histories and account details related to flagged communications or compliance concerns.
          
          Data Coverage:
          - Historical: 12 months of position and transaction history for compliance context
          - Current: End-of-day holdings updated daily in demo environment
          - Sources: DIM_SECURITY, DIM_PORTFOLIO, FACT_POSITION_DAILY_ABOR, DIM_CLIENT, DIM_ADVISOR
          - Records: 2,500+ real securities, 10+ portfolios, 7,000+ holdings for compliance analysis
          - Refresh: Daily demo data generation with compliance monitoring integration
          
          Semantic Model Contents:
          - Tables: Holdings, Securities, Portfolios, Clients, Advisors with compliance relationships
          - Key Metrics: TRANSACTION_VALUE, POSITION_SIZE, CLIENT_EXPOSURE, ADVISOR_ACTIVITY
          - Time Dimensions: HoldingDate, TransactionDate (daily granularity)
          - Common Filters: ClientName, AdvisorName, SecurityType, TransactionType
          
          When to Use:
          - Investigating transaction patterns related to flagged communications
          - Analyzing account histories for compliance investigations
          - Contextual financial data for regulatory inquiries
          - Questions like: "What transactions occurred around the flagged communication date?", "Show client account activity"
          
          When NOT to Use:
          - Primary compliance surveillance (use search_communications for monitoring)
          - Regulatory rule lookup (use search_regulatory for compliance requirements)
          - Communication content analysis (use search_communications for message content)
          - General portfolio analysis (this tool is for compliance context only)
          
          Query Best Practices:
          1. Be specific about compliance investigation context:
             ✅ "Transaction history for Sarah Johnson around March 15th communication"
             ❌ "client transactions" (needs compliance context)
          
          2. Filter to relevant time periods for investigations:
             ✅ "Account activity in the 30 days before flagged communication"
             ❌ All historical data without investigation focus
          
          3. Use client and advisor names for focused investigations:
             ✅ "Advisor John Smith's client transaction patterns"
             ❌ "advisor transactions" (needs specific investigation scope)
          
          4. Leverage compliance-relevant metrics:
             ✅ "Large transaction amounts above normal patterns"
             ❌ Generic portfolio metrics without compliance focus
    - tool_spec:
        type: "cortex_search"
        name: "search_communications"
        description: |
          Searches and analyzes all electronic communications for potential compliance violations, risk patterns, and regulatory adherence monitoring across client-advisor interactions.
          
          Data Sources:
          - Document Types: Client emails, phone call transcripts, meeting notes, video call summaries, advisor communications
          - Update Frequency: New communications added daily in demo environment for surveillance
          - Historical Range: Typically last 12 months of all client-advisor interactions
          - Index Freshness: Daily refresh with demo communication generation and compliance flagging
          - Typical Count: ~6,000 communications across all relationships for comprehensive surveillance
          
          When to Use:
          - Scanning communications for compliance violations and risk keywords
          - Analyzing communication patterns for regulatory adherence
          - Investigating specific compliance concerns or client complaints
          - Queries like: "Find communications with performance guarantees", "Search for PII sharing violations"
          
          When NOT to Use:
          - Portfolio holdings or financial data analysis (use cortex_analyst_client_financials for context)
          - Regulatory rule lookup (use search_regulatory for compliance requirements)
          - Communication frequency metrics (this is for content surveillance, not patterns)
          - General client relationship analysis (focus on compliance violations only)
          
          Search Query Best Practices:
          1. Use compliance risk lexicon keywords:
             ✅ "performance guarantee promise return investment assurance"
             ❌ "investment discussion" (needs compliance risk focus)
          
          2. Include regulatory violation terms:
             ✅ "PII personal information social security confidential data sharing"
             ❌ "client information" (needs specific violation context)
          
          3. Search for ESG compliance and greenwashing:
             ✅ "ESG sustainable green investment claim unsubstantiated greenwashing"
             ❌ "ESG investing" (needs compliance violation angle)
          
          4. Handle systematic surveillance patterns:
             ✅ "client complaint dissatisfaction concern problem issue"
             ❌ "client feedback" (needs compliance risk terminology)
          
          5. Focus on promissory language detection:
             ✅ "will guarantee ensure promise deliver return profit"
             ❌ "investment advice" (needs specific promissory language)
    - tool_spec:
        type: "cortex_search"
        name: "search_regulatory"
        description: |
          Searches regulatory documents, compliance rules, and policy guidance for specific regulations, compliance requirements, and regulatory framework reference during investigations.
          
          Data Sources:
          - Document Types: Regulatory rules, compliance policies, FINRA guidance, SEC regulations, ESG disclosure requirements
          - Update Frequency: New regulatory documents added as published in demo environment
          - Historical Range: Current and historical regulatory framework documents
          - Index Freshness: Daily refresh with demo regulatory content generation
          - Typical Count: ~100 regulatory documents covering traditional and ESG compliance requirements
          
          When to Use:
          - Finding specific regulations and compliance requirements during investigations
          - Looking up regulatory guidance for compliance determinations
          - Understanding ESG disclosure regulations and sustainability reporting standards
          - Queries like: "Find FINRA rules about performance guarantees", "What are ESG disclosure requirements?"
          
          When NOT to Use:
          - Communication content analysis (use search_communications for surveillance)
          - Financial data investigation (use cortex_analyst_client_financials for context)
          - General regulatory research (focus on specific compliance investigation needs)
          - Communication surveillance (use search_communications for violation detection)
          
          Search Query Best Practices:
          1. Use specific regulatory authority names:
             ✅ "FINRA rule 2210 communications advertising performance"
             ❌ "advertising rules" (needs specific regulatory authority)
          
          2. Include regulation numbers when known:
             ✅ "SEC rule 206(4)-1 advertising investment adviser performance"
             ❌ "SEC advertising" (needs specific rule reference)
          
          3. Search for ESG regulatory requirements:
             ✅ "ESG disclosure regulation sustainability reporting requirements"
             ❌ "ESG rules" (needs specific regulatory context)
          
          4. Handle compliance policy lookup:
             ✅ "personal information PII protection confidentiality policy requirements"
             ❌ "privacy policy" (needs regulatory compliance context)
          
          5. Focus on violation-specific regulations:
             ✅ "performance guarantee prohibition promissory statement regulation"
             ❌ "performance rules" (needs specific violation context)
  tool_resources:
    cortex_analyst_client_financials:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "WAM_AI_CORTEX_WH"
      semantic_view: "{database_name}.AI.CLIENT_FINANCIALS_SV"
    search_communications:
      search_service: "{database_name}.AI.COMMUNICATIONS_SEARCH"
      id_column: "COMMUNICATION_ID"
      title_column: "TITLE"
      max_results: 4
    search_regulatory:
      search_service: "{database_name}.AI.REGULATORY_SEARCH"
      id_column: "DOCUMENT_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    session.sql(sql).collect()
    print("✅ Created agent: wam_compliance_copilot")


def create_advisor_manager_copilot(session: Session):
    """Create Advisor Benchmarking CoPilot agent with comprehensive tool descriptions"""
    database_name = config.DATABASE_NAME
    
    # Get instructions from helper functions
    instructions = get_agent_instructions()['advisor_manager_copilot']
    response_formatted = format_instructions_for_yaml(instructions['response'])
    orchestration_formatted = format_instructions_for_yaml(instructions['orchestration'])
    
    sql = f"""
CREATE OR REPLACE AGENT SNOWFLAKE_INTELLIGENCE.AGENTS.wam_advisor_manager_copilot
  COMMENT = 'Executive benchmarking agent for leadership to assess advisor performance, client outcomes, planning completeness, engagement quality, revenue, and risk signals over rolling 12 months, with quartile benchmarks and actionable coaching insights.'
  PROFILE = '{{"display_name": "Advisor Benchmarking CoPilot (WAM Demo)"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: claude-sonnet-4-5
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "cortex_analyst_advisor_perf"
        description: |
          Analyzes advisor-level KPIs including AUM growth, net flows, client retention, engagement cadence, sentiment trends, planning coverage, revenue, and risk signal rates for TTM benchmarking and coaching insights.
          
          Data Coverage:
          - Historical: Rolling 12 months (TTM) of advisor performance metrics
          - Current: Daily updates with advisor activity and client outcome tracking
          - Sources: ADVISOR_SUMMARY_TTM, DIM_ADVISOR, DIM_CLIENT, FACT_ADVISOR_CLIENT_RELATIONSHIP
          - Records: 5 advisors with comprehensive TTM performance analytics and peer quartile benchmarking
          - Refresh: Daily demo data generation with advisor benchmarking calculations
          
          Semantic Model Contents:
          - Tables: Advisor Performance, Client Relationships, Manager Hierarchy with TTM calculations
          - Key Metrics: AUM_GROWTH_TTM, CLIENT_RETENTION_RATE, ENGAGEMENT_SCORE, PLANNING_COVERAGE_RATE, REVENUE_TTM
          - Time Dimensions: TTM periods, quarterly benchmarks, monthly trends
          - Common Filters: AdvisorName, ManagerName, PerformanceQuartile, ClientSegment
          
          When to Use:
          - Questions about advisor performance benchmarking and peer quartile analysis
          - TTM metrics analysis for coaching and performance management
          - Client retention, engagement, and planning coverage analysis
          - Questions like: "Show advisor performance quartiles", "Which advisors need coaching on client retention?"
          
          When NOT to Use:
          - Individual client communication content (use search_communications for specific interactions)
          - Detailed financial planning document content (use search_financial_planning for plan details)
          - Departure feedback analysis (use search_departures for exit questionnaire content)
          - Regulatory compliance analysis (use search_regulatory for compliance requirements)
          
          Query Best Practices:
          1. Be specific about TTM timeframe and metrics:
             ✅ "TTM client retention rates by advisor with peer quartiles"
             ❌ "advisor performance" (needs specific metrics and timeframe)
          
          2. Use benchmarking and quartile terminology:
             ✅ "Bottom quartile advisors for AUM growth with coaching opportunities"
             ❌ "poor performing advisors" (needs specific quartile and metric context)
          
          3. Focus on actionable coaching insights:
             ✅ "Advisors with low planning coverage rates and specific improvement targets"
             ❌ "planning problems" (needs specific metrics and actionable context)
          
          4. Leverage peer group comparisons:
             ✅ "Top quartile engagement scores compared to firm average"
             ❌ "good engagement" (needs quantitative benchmarking context)
    - tool_spec:
        type: "cortex_search"
        name: "search_communications"
        description: |
          Searches client communications for qualitative context on engagement quality, risk signal detection, and coaching opportunity identification in advisor benchmarking analysis.
          
          Data Sources:
          - Document Types: Client emails, phone call transcripts, meeting notes, advisor-client interactions
          - Update Frequency: New communications added daily in demo environment for benchmarking context
          - Historical Range: TTM communications for advisor performance context analysis
          - Index Freshness: Daily refresh with demo communication generation
          - Typical Count: ~6,000 communications for advisor benchmarking and coaching insights
          
          When to Use:
          - Finding qualitative context for advisor performance issues
          - Identifying risk signals and client concerns for coaching opportunities
          - Understanding engagement quality beyond quantitative metrics
          - Queries like: "Find client concerns for bottom quartile retention advisors", "Search for risk signals in advisor communications"
          
          When NOT to Use:
          - Quantitative advisor performance metrics (use cortex_analyst_advisor_perf for TTM analytics)
          - Financial planning document analysis (use search_financial_planning for plan content)
          - Departure analysis (use search_departures for exit feedback)
          - Regulatory compliance monitoring (use search_regulatory for compliance requirements)
          
          Search Query Best Practices:
          1. Use advisor benchmarking context:
             ✅ "client concerns complaints advisor John Smith engagement quality issues"
             ❌ "client feedback" (needs advisor benchmarking context)
          
          2. Include risk signal terminology:
             ✅ "client dissatisfaction risk signal advisor performance concern"
             ❌ "client problems" (needs risk signal and coaching context)
          
          3. Focus on coaching opportunity identification:
             ✅ "advisor communication style client relationship coaching opportunity"
             ❌ "advisor communications" (needs coaching and improvement context)
          
          4. Handle engagement quality analysis:
             ✅ "client meeting quality advisor engagement effectiveness coaching"
             ❌ "meeting notes" (needs engagement quality and benchmarking context)
    - tool_spec:
        type: "cortex_search"
        name: "search_financial_planning"
        description: |
          Searches financial planning documents for plan coverage analysis, recency assessment, and goal documentation completeness in advisor benchmarking and coaching evaluation.
          
          Data Sources:
          - Document Types: Comprehensive financial plans, investment policy statements, retirement plans, education funding plans
          - Update Frequency: New planning documents added as created for coverage analysis
          - Historical Range: Current and historical planning documents for completeness assessment
          - Index Freshness: Daily refresh with demo planning document generation
          - Typical Count: ~150 planning documents for advisor benchmarking and coverage analysis
          
          When to Use:
          - Analyzing planning coverage rates and document recency for advisor benchmarking
          - Understanding plan quality and completeness for coaching insights
          - Identifying planning gaps and improvement opportunities by advisor
          - Queries like: "Find outdated plans for advisor coaching", "Analyze planning coverage completeness by advisor"
          
          When NOT to Use:
          - Quantitative advisor performance metrics (use cortex_analyst_advisor_perf for TTM analytics)
          - Client communication analysis (use search_communications for engagement context)
          - Departure feedback analysis (use search_departures for exit questionnaires)
          - General financial planning advice (focus on advisor benchmarking context)
          
          Search Query Best Practices:
          1. Use planning coverage terminology:
             ✅ "investment policy statement coverage advisor planning completeness"
             ❌ "financial plans" (needs coverage and benchmarking context)
          
          2. Include recency and timeliness analysis:
             ✅ "outdated financial plans advisor coaching planning recency policy"
             ❌ "old plans" (needs advisor benchmarking and policy context)
          
          3. Focus on advisor-specific planning quality:
             ✅ "comprehensive financial plan quality advisor benchmarking coaching"
             ❌ "plan quality" (needs advisor-specific benchmarking context)
          
          4. Handle planning gap identification:
             ✅ "missing retirement planning advisor coverage gap coaching opportunity"
             ❌ "planning gaps" (needs advisor-specific coaching context)
    - tool_spec:
        type: "cortex_search"
        name: "search_departures"
        description: |
          Searches exit questionnaires and departure feedback for retention analysis, coaching insights, and advisor performance improvement opportunities in benchmarking evaluation.
          
          Data Sources:
          - Document Types: Exit questionnaires, departure feedback, client retention analysis, advisor transition notes
          - Update Frequency: New departure documents added as clients exit for retention analysis
          - Historical Range: TTM departure feedback for advisor benchmarking context
          - Index Freshness: Daily refresh with demo departure content generation
          - Typical Count: ~25 departure documents for advisor retention analysis and coaching
          
          When to Use:
          - Analyzing departure reasons for advisor coaching and retention improvement
          - Understanding client exit feedback for advisor performance insights
          - Identifying retention patterns and coaching opportunities by advisor
          - Queries like: "Find departure reasons for low retention advisors", "Analyze exit feedback for coaching insights"
          
          When NOT to Use:
          - Quantitative retention metrics (use cortex_analyst_advisor_perf for TTM retention rates)
          - Current client communication analysis (use search_communications for active relationships)
          - Financial planning analysis (use search_financial_planning for plan coverage)
          - General retention strategies (focus on advisor-specific departure feedback)
          
          Search Query Best Practices:
          1. Use departure and retention terminology:
             ✅ "client departure reason advisor retention coaching opportunity"
             ❌ "client feedback" (needs departure and retention context)
          
          2. Include advisor-specific retention analysis:
             ✅ "exit questionnaire advisor John Smith retention improvement coaching"
             ❌ "exit feedback" (needs advisor-specific benchmarking context)
          
          3. Focus on coaching and improvement insights:
             ✅ "departure feedback advisor performance coaching retention strategy"
             ❌ "why clients left" (needs coaching and benchmarking context)
          
          4. Handle retention pattern analysis:
             ✅ "client exit pattern advisor benchmarking retention coaching opportunity"
             ❌ "departure patterns" (needs advisor benchmarking context)
    - tool_spec:
        type: "cortex_search"
        name: "search_regulatory"
        description: |
          Searches regulatory documents and compliance rules for quick lookup of compliance requirements referenced in advisor benchmarking and coaching analysis.
          
          Data Sources:
          - Document Types: Regulatory rules, compliance policies, advisor conduct requirements, planning standards
          - Update Frequency: New regulatory documents added as published for benchmarking reference
          - Historical Range: Current regulatory framework for advisor performance standards
          - Index Freshness: Daily refresh with demo regulatory content generation
          - Typical Count: ~100 regulatory documents for advisor benchmarking compliance reference
          
          When to Use:
          - Quick lookup of compliance rules referenced in advisor benchmarking analysis
          - Understanding regulatory requirements for advisor performance standards
          - Finding compliance context for coaching and performance improvement
          - Queries like: "Find advisor conduct requirements for coaching", "What are planning documentation standards?"
          
          When NOT to Use:
          - Advisor performance metrics analysis (use cortex_analyst_advisor_perf for TTM analytics)
          - Client communication surveillance (use search_communications for engagement context)
          - Detailed compliance investigations (focus on benchmarking reference only)
          - General regulatory research (focus on advisor performance context)
          
          Search Query Best Practices:
          1. Use advisor performance regulatory context:
             ✅ "advisor conduct standards performance requirements coaching compliance"
             ❌ "advisor rules" (needs performance and coaching context)
          
          2. Include planning and documentation standards:
             ✅ "financial planning documentation requirements advisor standards"
             ❌ "planning rules" (needs advisor benchmarking context)
          
          3. Focus on performance and coaching compliance:
             ✅ "advisor performance standards coaching compliance requirements"
             ❌ "compliance rules" (needs advisor benchmarking context)
          
          4. Handle benchmarking regulatory reference:
             ✅ "advisor benchmarking standards regulatory requirements coaching"
             ❌ "benchmarking rules" (needs advisor performance context)
  tool_resources:
    cortex_analyst_advisor_perf:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "WAM_AI_CORTEX_WH"
      semantic_view: "{database_name}.AI.ADVISOR_PERFORMANCE_SV"
    search_communications:
      search_service: "{database_name}.AI.COMMUNICATIONS_SEARCH"
      id_column: "COMMUNICATION_ID"
      title_column: "TITLE"
      max_results: 4
    search_financial_planning:
      search_service: "{database_name}.AI.PLANNING_SEARCH"
      id_column: "DOCUMENT_ID"
      title_column: "TITLE"
      max_results: 4
    search_departures:
      search_service: "{database_name}.AI.DEPARTURE_SEARCH"
      id_column: "DOCUMENT_ID"
      title_column: "TITLE"
      max_results: 4
    search_regulatory:
      search_service: "{database_name}.AI.REGULATORY_SEARCH"
      id_column: "DOCUMENT_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    session.sql(sql).collect()
    print("✅ Created agent: wam_advisor_manager_copilot")


if __name__ == "__main__":
    # For testing - create session and run
    from src.utils import create_session
    session = create_session()
    create_all_agents(session, ['all'])
