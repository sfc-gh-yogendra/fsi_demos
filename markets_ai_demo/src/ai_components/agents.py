# src/ai_components/agents.py
# Agent configuration templates for Frost Markets Intelligence Demo

"""
Agent Configuration for Snowflake Intelligence

This module contains SQL-based agent creation for all demo agents.
Agents are automatically created during the build process.

Phase 1 Agents (Build First):
1. Earnings Analysis Agent - Equity Research Analyst scenario
2. Thematic Research Agent - Equity Research Analyst scenario

Phase 2 Agents (Future):
3. Global Macro Strategy Agent - Global Research & Market Insights scenario
4. Market Reports Agent - Global Research & Market Insights scenario  
5. Client Strategy Agent - Global Research & Market Insights scenario
"""

from snowflake.snowpark import Session
from config import DemoConfig
from typing import List


def check_snowflake_intelligence(session: Session) -> bool:
    """
    Check if Snowflake Intelligence object exists.
    User must create this manually in Snowsight before agents can be registered.
    
    Returns:
        True if exists, False if not
    """
    try:
        result = session.sql("SHOW SNOWFLAKE INTELLIGENCES").collect()
        if len(result) > 0:
            print("✅ Snowflake Intelligence object found")
            return True
        else:
            print("⚠️  No Snowflake Intelligence object found")
            print("   Please create one in Snowsight before proceeding:")
            print("   AI & ML → Snowflake Intelligence → Create New Intelligence")
            return False
    except Exception as e:
        print(f"⚠️  Could not check for Snowflake Intelligence: {str(e)}")
        return False


def format_instructions_for_yaml(text: str) -> str:
    """
    Format multi-line instructions for YAML specification within SQL.
    - Replace actual line breaks with \\n
    - Escape double quotes with \\"
    - Escape single quotes with '' (SQL standard)
    
    Args:
        text: Multi-line instruction text
        
    Returns:
        YAML-safe formatted string
    """
    formatted = text.replace('\n', '\\n')
    formatted = formatted.replace('"', '\\"')
    formatted = formatted.replace("'", "''")
    return formatted


def get_agent_configs():
    """Return all agent configurations"""
    
    return {
        "earnings_analysis_agent": {
            "agent_name": "MR_EARNINGS_ANALYSIS_AGENT",
            "display_name": "Earnings Analysis Assistant (Market Research)", 
            "description": "Specialized assistant for analyzing quarterly earnings results, consensus estimates, and management commentary",
            "orchestration_model": "Claude 4",
            "tools": [
                "earnings_data_analyzer (Cortex Analyst)",
                "search_earnings_transcripts (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help equity research analysts understand quarterly earnings performance and management commentary.

Tool Selection Logic:
1. For questions about SPECIFIC FINANCIAL RESULTS, headline numbers, consensus beats/misses, or historical performance comparisons:
   → Use the earnings_data_analyzer (Cortex Analyst) tool on AI.EARNINGS_ANALYSIS_VIEW
   
2. For questions about MANAGEMENT COMMENTARY, tone, sentiment, analyst questions, or specific quotes from earnings calls:
   → Use the search_earnings_transcripts (Cortex Search) tool on AI.EARNINGS_TRANSCRIPTS_SEARCH
   
3. For generating SUMMARIES, REPORTS, or FIRST TAKE notes:
   → Gather data from appropriate tools first, then synthesize the information

Examples:
- "Revenue for Netflix Q3" → Use earnings_data_analyzer
- "What did management say about subscriber growth?" → Use search_earnings_transcripts  
- "Compare revenue vs estimates for last 4 quarters" → Use earnings_data_analyzer
- "Management tone on guidance" → Use search_earnings_transcripts""",
            
            "response_instructions": """You are a world-class equity research assistant specializing in earnings analysis.

IMPORTANT DISCLAIMER:
- At the end of EVERY response, include this disclaimer: "⚠️ Note: This analysis is based on synthetic demo data for demonstration purposes only."

Response Guidelines:
- Be concise, accurate, and data-driven in all responses
- Present numerical data clearly in sentences or markdown tables
- When providing charts/visualizations, include the underlying data in table format
- Always cite your sources (e.g., "According to the Q3 10-Q filing...", "Based on the earnings call transcript...")
- Use professional financial terminology appropriate for research analysts
- For beat/miss analysis, clearly state both dollar amounts and percentages
- When quoting management, use exact quotes and provide context

Format for Financial Results:
- Lead with the headline: "[Company] reported [Metric] of $X vs consensus of $Y, a Z% beat/miss"
- Follow with context and drivers
- Include relevant management commentary if available

Tone: Professional, analytical, and confident while remaining objective."""
        },
        
        "thematic_research_agent": {
            "agent_name": "MR_THEMATIC_RESEARCH_AGENT",
            "display_name": "Thematic Investment Research Assistant (Market Research)",
            "description": "Advanced assistant for discovering emerging investment themes and cross-sector trends from alternative data sources",
            "orchestration_model": "Claude 4", 
            "tools": [
                "thematic_data_analyzer (Cortex Analyst)",
                "search_research_reports (Cortex Search)",
                "search_news_articles (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help equity research analysts discover and analyze emerging investment themes and trends.

Tool Selection Logic:
1. For questions about THEMATIC TRENDS, investment themes, or cross-sector analysis:
   → Use the thematic_data_analyzer (Cortex Analyst) tool on AI.THEMATIC_RESEARCH_VIEW
   
2. For questions about INTERNAL RESEARCH, official firm analysis, or regulatory topics:
   → Use the search_research_reports (Cortex Search) tool on AI.RESEARCH_REPORTS_SEARCH
   
3. For questions about MARKET EVENTS, news analysis, or current developments:
   → Use the search_news_articles (Cortex Search) tool on AI.NEWS_ARTICLES_SEARCH

4. For STOCK PERFORMANCE related to themes:
   → Use thematic_data_analyzer to get price data and correlations

Strategy for Complex Queries:
- Start with thematic_data_analyzer for quantitative analysis
- Use search tools to provide supporting qualitative context
- Synthesize findings from multiple sources

Examples:
- "Carbon capture technology trends" → search_research_reports + search_news_articles
- "Companies exposed to semiconductor risk" → thematic_data_analyzer
- "Stock performance of climate tech companies" → thematic_data_analyzer""",
            
            "response_instructions": """You are an expert thematic investment research assistant focused on identifying emerging trends and cross-sector opportunities.

IMPORTANT DISCLAIMER:
- At the end of EVERY response, include this disclaimer: "⚠️ Note: This analysis is based on synthetic demo data for demonstration purposes only."

Response Guidelines:
- Think like a senior research analyst looking for alpha-generating insights
- Combine quantitative analysis with qualitative context
- Identify unexpected connections between sectors, themes, and market events
- Provide actionable investment implications, not just academic analysis
- When discussing themes, always connect to specific investable companies
- Use data to support qualitative observations

Format for Thematic Analysis:
- Start with the key finding or trend identification
- Provide supporting data (company exposure, performance metrics)
- Include market context and news developments
- End with investment implications or questions for further research

Investment Focus:
- Look for early-stage themes before they become consensus
- Identify companies with unexpected exposure to emerging trends
- Flag both opportunities and risks within themes
- Consider regulatory, technological, and market drivers

Tone: Insightful, forward-looking, and commercially minded while remaining analytically rigorous."""
        },
        
        "global_macro_strategy_agent": {
            "agent_name": "MR_GLOBAL_MACRO_STRATEGY_AGENT",
            "display_name": "Global Macro Strategy Assistant (Market Research)",
            "description": "Expert assistant for analyzing proprietary macroeconomic signals and developing cross-asset investment strategies",
            "orchestration_model": "Claude 4",
            "tools": [
                "macro_signals_analyzer (Cortex Analyst)",
                "search_research_reports (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help global macro strategists analyze macroeconomic signals and develop investment recommendations.

Tool Selection Logic:
1. For questions about PROPRIETARY MACRO SIGNALS, signal trends, sector correlations, or quantitative macro analysis:
   → Use the macro_signals_analyzer (Cortex Analyst) tool on AI.GLOBAL_MACRO_SIGNALS_VIEW
   
2. For questions about MACRO RESEARCH, investment themes, or strategic recommendations:
   → Use the search_research_reports (Cortex Search) tool on AI.RESEARCH_REPORTS_SEARCH
   
3. For CROSS-ASSET STRATEGY questions:
   → Combine both tools: start with macro_signals_analyzer for quantitative signal analysis, then use search_research_reports for strategic context

Strategy for Complex Queries:
- Start with macro_signals_analyzer to get current signal levels and trends
- Use sector correlation data to identify investment implications
- Reference research reports for strategic recommendations and market context
- Synthesize quantitative signals with qualitative research insights

Examples:
- "What's the current level of the Frost Global Shipping Volume Index?" → macro_signals_analyzer
- "Which sectors benefit most from rising commodity prices?" → macro_signals_analyzer (sector correlations)
- "Find our latest macro outlook report" → search_research_reports
- "Build a sector rotation strategy based on current macro signals" → Both tools""",
            
            "response_instructions": """You are an expert global macro strategist and cross-asset investment advisor at Frost Markets Intelligence.

IMPORTANT DISCLAIMER:
- At the end of EVERY response, include this disclaimer: "⚠️ Note: This analysis is based on synthetic demo data for demonstration purposes only."

Response Guidelines:
- Think like a senior macro strategist developing actionable investment strategies
- Always reference our proprietary Frost indicators by their full names (e.g., "Frost Global Shipping Volume Index")
- Translate macro signals into specific sector and asset class recommendations
- Provide quantitative analysis (signal levels, trends, correlations) combined with qualitative context
- Consider cross-asset implications and regional dynamics
- Be forward-looking and focus on investment positioning

Format for Macro Analysis:
- Lead with the key macro theme or signal change
- Provide current signal levels and recent trends with specific numbers
- Connect signals to sector/asset class implications using correlation data
- Reference relevant research reports for strategic context
- End with actionable investment recommendations

Investment Focus:
- Emphasize our proprietary signal insights as competitive advantage
- Link macro developments to tactical portfolio positioning
- Consider both opportunities and risks in recommendations
- Address sector rotation, geographic allocation, and asset class positioning
- Discuss hedging strategies when appropriate

Tone: Strategic, authoritative, and investment-focused while remaining analytically rigorous and data-driven."""
        },
        
        "market_reports_agent": {
            "agent_name": "MR_MARKET_REPORTS_AGENT", 
            "display_name": "Market Structure Research Assistant (Market Research)",
            "description": "Specialist in market structure analysis, regulatory changes, and institutional client insights",
            "orchestration_model": "Claude 4",
            "tools": [
                "client_engagement_analyzer (Cortex Analyst)",
                "search_research_reports (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help market structure analysts understand client engagement patterns and identify opportunities for targeted outreach on regulatory and market structure topics.

Tool Selection Logic:
1. For questions about CLIENT ENGAGEMENT PATTERNS, content downloads, trading activity, or client segmentation:
   → Use the client_engagement_analyzer (Cortex Analyst) tool on AI.CLIENT_MARKET_IMPACT_VIEW
   
2. For questions about REGULATORY TOPICS, market structure research, FICC developments, or EMIR 3.0:
   → Use the search_research_reports (Cortex Search) tool on AI.RESEARCH_REPORTS_SEARCH
   
3. For IDENTIFYING OUTREACH OPPORTUNITIES:
   → Combine both tools: start with search_research_reports to identify key themes, then use client_engagement_analyzer to find clients engaging with those topics

Strategy for Complex Queries:
- Use client_engagement_analyzer to quantify which topics drive most engagement
- Use search_research_reports to understand the regulatory/market structure context
- Synthesize to identify high-value clients for strategic outreach

Examples:
- "Which regulatory topics generated most client engagement?" → client_engagement_analyzer
- "What are the key implications of EMIR 3.0?" → search_research_reports
- "Which asset managers are engaging with EMIR content but haven't met with us?" → Both tools""",
            
            "response_instructions": """You are an expert market structure analyst focused on institutional client insights and regulatory change implications.

IMPORTANT DISCLAIMER:
- At the end of EVERY response, include this disclaimer: "⚠️ Note: This analysis is based on synthetic demo data for demonstration purposes only."

Response Guidelines:
- Think like a market structure specialist helping relationship managers identify strategic opportunities
- Combine quantitative engagement data with qualitative regulatory context
- Focus on actionable insights for client outreach and content strategy
- When discussing regulatory changes, always connect to specific client impacts and opportunities
- Use data to identify which clients care most about specific topics
- Provide clear, specific recommendations for targeted engagements

Format for Market Structure Analysis:
- Start with the key regulatory or market structure theme
- Provide engagement metrics showing client interest levels
- Identify specific client segments or names for outreach
- Include relevant research context from internal reports
- End with actionable recommendations for relationship managers

Client Focus:
- Emphasize data-driven client segmentation
- Identify clients with high engagement but low direct interaction
- Connect regulatory changes to trading patterns and client needs
- Provide talking points for strategic discussions
- Consider regional and client-type differences

Tone: Strategic, client-centric, and data-driven while remaining analytically rigorous and commercially focused."""
        },
        
        "client_strategy_agent": {
            "agent_name": "MR_CLIENT_STRATEGY_AGENT",
            "display_name": "Client Strategy Assistant (Market Research)", 
            "description": "Strategic assistant for preparing data-driven client meetings and personalized recommendations",
            "orchestration_model": "Claude 4",
            "tools": [
                "client_impact_analyzer (Cortex Analyst)",
                "search_research_reports (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help relationship managers prepare for strategic client meetings by analyzing specific client activity and synthesizing personalized recommendations.

Tool Selection Logic:
1. For questions about SPECIFIC CLIENT ACTIVITY, trading patterns, FX hedging, clearing relationships, or exposure to market events:
   → Use the client_impact_analyzer (Cortex Analyst) tool on AI.CLIENT_MARKET_IMPACT_VIEW
   
2. For questions about STRATEGIC RECOMMENDATIONS, firm research positions, or regulatory guidance (like EMIR 3.0):
   → Use the search_research_reports (Cortex Search) tool on AI.RESEARCH_REPORTS_SEARCH
   
3. For PREPARING CLIENT BRIEFINGS:
   → Start with client_impact_analyzer to understand the client's specific situation
   → Use search_research_reports to find relevant firm research and recommendations
   → Synthesize into personalized, actionable talking points

Strategy for Meeting Preparation:
- First understand the client's trading patterns and exposure
- Identify their specific risks or opportunities based on activity
- Find relevant internal research to provide strategic context
- Create personalized briefing that connects their situation to our recommendations

Examples:
- "What is [Client Corp]'s FX hedging activity?" → client_impact_analyzer
- "Find our EMIR 3.0 guidance for corporates" → search_research_reports
- "Prepare briefing for [Client] on upcoming regulatory changes" → Both tools""",
            
            "response_instructions": """You are an expert client strategy advisor helping relationship managers prepare for high-value strategic discussions.

IMPORTANT DISCLAIMER:
- At the end of EVERY response, include this disclaimer: "⚠️ Note: This analysis is based on synthetic demo data for demonstration purposes only."

Response Guidelines:
- Think like a senior relationship manager preparing for a strategic client meeting
- Always connect data-driven insights about the client's specific situation to actionable recommendations
- Frame regulatory changes and market developments as opportunities to provide strategic value
- Provide clear, specific talking points that demonstrate understanding of the client's business
- Focus on being proactive and consultative, not reactive
- Use client-specific data to show you understand their unique situation

Format for Client Briefing Notes:
- Start with a clear subject line and purpose for the meeting
- Summarize the client's relevant activity or exposure in 2-3 sentences
- Explain the specific market/regulatory development and its impact on this client
- Provide our firm's strategic recommendations, citing internal research
- End with clear next steps and value proposition

Strategic Approach:
- Position the firm as a proactive strategic partner, not just a service provider
- Show how our insights help the client navigate change successfully
- Use data to demonstrate understanding, not just to show you have data
- Frame challenges as opportunities to strengthen the relationship
- Always include specific, actionable recommendations

Tone: Consultative, strategic, and client-centric while being data-driven and professionally authoritative."""
        },
        
        "market_risk_agent": {
            "agent_name": "MR_MARKET_RISK_AGENT",
            "display_name": "Market Risk Analysis Assistant (Market Research)",
            "description": "Expert assistant for real-time market risk assessment, portfolio stress testing, and firm-wide exposure analysis",
            "orchestration_model": "Claude 4",
            "tools": [
                "firm_exposure_analyzer (Cortex Analyst)",
                "calculate_portfolio_var (Custom Tool)",
                "search_news_articles (Cortex Search)"
            ],
            "planning_instructions": """Your goal is to help market risk analysts assess firm-wide exposure, perform stress tests, and monitor real-time market events.

Tool Selection Logic:
1. For questions about FIRM EXPOSURE, portfolio holdings, sector concentration, or geographic exposure:
   → Use the firm_exposure_analyzer (Cortex Analyst) tool on AI.FIRM_EXPOSURE_VIEW
   
2. For questions about STRESS TESTING, Value-at-Risk calculations, or scenario analysis with price shocks:
   → Use the calculate_portfolio_var (Custom Tool) which performs historical simulation VaR calculations
   
3. For questions about MARKET EVENTS, breaking news, or real-time developments:
   → Use the search_news_articles (Cortex Search) tool on AI.NEWS_ARTICLES_SEARCH

Strategy for Risk Assessment:
- Start with firm_exposure_analyzer to understand current positions and concentrations
- Use search_news_articles to understand market context and events
- Apply calculate_portfolio_var for quantitative stress testing
- Synthesize exposure data, market context, and stress test results into risk assessment

Examples:
- "What is our exposure to Taiwan equities?" → firm_exposure_analyzer
- "Stress test semiconductor portfolio with 15% drop" → calculate_portfolio_var
- "Recent news about Taiwan earthquake" → search_news_articles
- "Taiwan earthquake - assess our semiconductor exposure and stress test it" → All three tools""",
            
            "response_instructions": """You are an expert market risk analyst focused on real-time risk assessment and portfolio stress testing.

IMPORTANT DISCLAIMER:
- At the end of EVERY response, include this disclaimer: "⚠️ Note: This analysis is based on synthetic demo data for demonstration purposes only."

Response Guidelines:
- Think like a senior market risk analyst providing urgent, actionable risk intelligence
- Always quantify exposure in dollar terms and as percentage of total portfolio
- When discussing market events, immediately connect to firm's specific exposure
- Provide both current exposure and stressed scenarios for context
- Be clear about methodology and assumptions in stress tests
- Focus on actionable intelligence that risk managers can use immediately
- Present risk metrics clearly: VaR, exposure by sector/geography, concentration risk

Format for Risk Assessments:
- Start with headline exposure figure (e.g., "$250M exposure to Taiwan equities")
- Break down by relevant dimensions (sector, portfolio, top holdings)
- Connect to market context or event if relevant
- Provide stress test results showing potential losses under adverse scenarios
- End with clear risk assessment and monitoring recommendations

Risk Communication:
- Lead with the most critical risk metric
- Use tables to show top exposures and concentrations
- Always provide context: absolute amounts AND percentages
- Explain implications of VaR numbers in business terms
- Distinguish between current exposure and potential losses under stress
- Be direct about risk levels without unnecessary hedging

Tone: Urgent, quantitative, and actionable while remaining analytically rigorous and clear."""
        }
    }


def get_tool_configurations():
    """Return tool configurations for agents"""
    
    return {
        "earnings_data_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "AI.EARNINGS_ANALYSIS_VIEW",
            "description": "Analyzes quarterly earnings results, consensus estimates, and beat/miss calculations. Use for financial metrics, performance comparisons, and quantitative earnings analysis."
        },
        
        "search_earnings_transcripts": {
            "type": "Cortex Search",
            "search_service": "AI.EARNINGS_TRANSCRIPTS_SEARCH", 
            "description": "Searches earnings call transcripts for management commentary, analyst questions, and qualitative insights. Use for tone analysis, guidance discussions, and specific quotes."
        },
        
        "thematic_data_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "AI.THEMATIC_RESEARCH_VIEW",
            "description": "Analyzes thematic investment trends, company exposures, and cross-sector patterns. Use for identifying emerging themes and quantifying company relationships to trends."
        },
        
        "macro_signals_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "AI.GLOBAL_MACRO_SIGNALS_VIEW",
            "description": "Analyzes proprietary macroeconomic signals including Frost indicators, sector correlations, and economic regional data. Use for macro trend analysis, signal levels, sector positioning, and cross-asset strategy development."
        },
        
        "search_research_reports": {
            "type": "Cortex Search", 
            "search_service": "AI.RESEARCH_REPORTS_SEARCH",
            "description": "Searches internal research reports and official firm analysis. Use for regulatory topics, market structure insights, macro outlook reports, and established firm positions on themes."
        },
        
        "search_news_articles": {
            "type": "Cortex Search",
            "search_service": "AI.NEWS_ARTICLES_SEARCH", 
            "description": "Searches news articles and market event coverage. Use for current developments, market reaction analysis, and real-time event context."
        },
        
        "client_engagement_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "AI.CLIENT_MARKET_IMPACT_VIEW",
            "description": "Analyzes client engagement patterns, trading activity, and discussion topics. Use for understanding which clients care about specific topics, engagement metrics, and identifying outreach opportunities."
        },
        
        "client_impact_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "AI.CLIENT_MARKET_IMPACT_VIEW",
            "description": "Analyzes specific client trading patterns and exposure to market events. Use for preparing personalized client briefings and strategic recommendations."
        },
        
        "firm_exposure_analyzer": {
            "type": "Cortex Analyst",
            "semantic_view": "AI.FIRM_EXPOSURE_VIEW",
            "description": "Analyzes firm-wide portfolio exposure by sector, geography, and credit quality. Use for understanding firm risk concentrations, portfolio holdings, and exposure to market events."
        }
    }


def get_demo_test_queries():
    """Return test queries for validating agent setups"""
    
    return {
        "earnings_analysis_agent": [
            "Give me a summary of Netflix's latest quarter results",
            "How did Netflix perform against consensus estimates?", 
            "What was management's tone about subscriber growth in the earnings call?",
            "Generate a chart comparing Netflix revenue vs estimates for the last 4 quarters"
        ],
        
        "thematic_research_agent": [
            "What are the emerging trends in carbon capture technology?",
            "Which companies have the highest exposure to semiconductor supply chain risks?",
            "Show me the stock performance of companies involved in climate technology",
            "Find recent news about direct air capture developments"
        ],
        
        "global_macro_strategy_agent": [
            "What is the current level of the Frost Global Shipping Volume Index and what does it signal?",
            "Which sectors have the strongest positive correlation with our Frost Central Bank Liquidity Indicator?",
            "Based on current macro signals, which sectors should we overweight in portfolios?",
            "Find our latest global macro outlook report and summarize the key themes"
        ]
    }


def create_earnings_analysis_agent(session: Session) -> None:
    """Create Earnings Analysis Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    ai_schema = DemoConfig.SCHEMAS['AI']
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['earnings_analysis_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {database_name}.{ai_schema}.MR_EARNINGS_ANALYSIS_AGENT
  COMMENT = 'Specialized assistant for analyzing quarterly earnings results, consensus estimates, and management commentary'
  PROFILE = '{{"display_name": "{display_name}"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: {DemoConfig.AGENT_ORCHESTRATION_MODEL}
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "earnings_data_analyzer"
        description: "Analyzes quarterly earnings results, consensus estimates, and beat/miss calculations. Data Coverage: 8 quarters of historical earnings data, daily refresh. Use for financial metrics, performance comparisons, and quantitative earnings analysis. When to Use: Questions about actual results, consensus beats/misses, historical comparisons. When NOT to Use: Management commentary (use search_earnings_transcripts), future guidance discussions (use search tool)."
    - tool_spec:
        type: "cortex_search"
        name: "search_earnings_transcripts"
        description: "Searches earnings call transcripts for management commentary, analyst questions, and qualitative insights. Data Coverage: Earnings call transcripts from last 8 quarters with full text search. Use for tone analysis, guidance discussions, and specific quotes from management and analysts. When to Use: Questions about what management said, analyst Q&A, sentiment analysis. When NOT to Use: Financial numbers and metrics (use earnings_data_analyzer)."
  tool_resources:
    earnings_data_analyzer:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "{warehouse_name}"
      semantic_view: "{database_name}.AI.EARNINGS_ANALYSIS_VIEW"
    search_earnings_transcripts:
      search_service: "{database_name}.AI.EARNINGS_TRANSCRIPTS_SEARCH"
      id_column: "TRANSCRIPT_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    try:
        session.sql(sql).collect()
        print("✅ Created agent: earnings_analysis_agent")
        
        # Register with Snowflake Intelligence
        register_sql = f"""
        ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT 
        ADD AGENT {database_name}.{ai_schema}.MR_EARNINGS_ANALYSIS_AGENT
        """
        session.sql(register_sql).collect()
        print("✅ Registered agent with Snowflake Intelligence")
        
    except Exception as e:
        print(f"❌ Failed to create/register earnings_analysis_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_thematic_research_agent(session: Session) -> None:
    """Create Thematic Investment Research Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    ai_schema = DemoConfig.SCHEMAS['AI']
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['thematic_research_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {database_name}.{ai_schema}.MR_THEMATIC_RESEARCH_AGENT
  COMMENT = 'Advanced assistant for discovering emerging investment themes and cross-sector trends from alternative data sources'
  PROFILE = '{{"display_name": "{display_name}"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: {DemoConfig.AGENT_ORCHESTRATION_MODEL}
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "thematic_data_analyzer"
        description: "Analyzes thematic investment trends, company exposures, and cross-sector patterns. Data Coverage: Historical stock prices, company master data, and thematic tags across 15 companies. Use for identifying emerging themes, quantifying company relationships to trends, and stock performance analysis. When to Use: Questions about theme exposure, sector trends, price performance. When NOT to Use: Qualitative research synthesis (use search tools), specific company news (use search_news_articles)."
    - tool_spec:
        type: "cortex_search"
        name: "search_research_reports"
        description: "Searches internal research reports and official Frost Markets Intelligence analysis. Data Coverage: Internal research reports with thematic tags, regulatory topics, and market structure insights. Use for established firm positions on themes, regulatory analysis, and strategic research. When to Use: Questions about Frost research views, regulatory topics, official analysis. When NOT to Use: Breaking news (use search_news_articles), quantitative data (use thematic_data_analyzer)."
    - tool_spec:
        type: "cortex_search"
        name: "search_news_articles"
        description: "Searches news articles and market event coverage. Data Coverage: News articles with affected tickers, sources, and market events. Use for current developments, market reaction analysis, and real-time event context. When to Use: Questions about recent news, market events, current developments. When NOT to Use: Historical performance data (use thematic_data_analyzer), official research (use search_research_reports)."
  tool_resources:
    thematic_data_analyzer:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "{warehouse_name}"
      semantic_view: "{database_name}.AI.THEMATIC_RESEARCH_VIEW"
    search_research_reports:
      search_service: "{database_name}.AI.RESEARCH_REPORTS_SEARCH"
      id_column: "REPORT_ID"
      title_column: "TITLE"
      max_results: 4
    search_news_articles:
      search_service: "{database_name}.AI.NEWS_ARTICLES_SEARCH"
      id_column: "ARTICLE_ID"
      title_column: "HEADLINE"
      max_results: 4
  $$;
"""
    
    try:
        session.sql(sql).collect()
        print("✅ Created agent: thematic_research_agent")
        
        # Register with Snowflake Intelligence
        register_sql = f"""
        ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT 
        ADD AGENT {database_name}.{ai_schema}.MR_THEMATIC_RESEARCH_AGENT
        """
        session.sql(register_sql).collect()
        print("✅ Registered agent with Snowflake Intelligence")
        
    except Exception as e:
        print(f"❌ Failed to create/register thematic_research_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_global_macro_strategy_agent(session: Session) -> None:
    """Create Global Macro Strategy Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    ai_schema = DemoConfig.SCHEMAS['AI']
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['global_macro_strategy_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {database_name}.{ai_schema}.MR_GLOBAL_MACRO_STRATEGY_AGENT
  COMMENT = 'Expert assistant for analyzing proprietary macroeconomic signals and developing cross-asset investment strategies'
  PROFILE = '{{"display_name": "{display_name}"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: {DemoConfig.AGENT_ORCHESTRATION_MODEL}
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "macro_signals_analyzer"
        description: "Analyzes proprietary macroeconomic signals including Frost indicators, sector correlations, and economic regional data. Data Coverage: Weekly proprietary signals (Frost Global Shipping Volume Index, Central Bank Liquidity Indicator, etc.), sector-macro correlation coefficients, regional GDP data. Use for macro trend analysis, signal levels and changes, sector positioning based on correlations, and cross-asset strategy development. When to Use: Questions about current signal levels, sector correlations, regional macro data, quantitative macro analysis. When NOT to Use: Qualitative macro research and strategy recommendations (use search_research_reports)."
    - tool_spec:
        type: "cortex_search"
        name: "search_research_reports"
        description: "Searches internal research reports including macro outlook reports, thematic analysis, and strategic recommendations. Data Coverage: Frost Markets Intelligence research reports with macro themes, investment strategies, and market outlook. Use for strategic context, macro research synthesis, and investment recommendations. When to Use: Questions about Frost macro outlook, strategic recommendations, qualitative analysis. When NOT to Use: Quantitative signal data (use macro_signals_analyzer)."
  tool_resources:
    macro_signals_analyzer:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "{warehouse_name}"
      semantic_view: "{database_name}.AI.GLOBAL_MACRO_SIGNALS_VIEW"
    search_research_reports:
      search_service: "{database_name}.AI.RESEARCH_REPORTS_SEARCH"
      id_column: "REPORT_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    try:
        session.sql(sql).collect()
        print("✅ Created agent: global_macro_strategy_agent")
        
        # Register with Snowflake Intelligence
        register_sql = f"""
        ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT 
        ADD AGENT {database_name}.{ai_schema}.MR_GLOBAL_MACRO_STRATEGY_AGENT
        """
        session.sql(register_sql).collect()
        print("✅ Registered agent with Snowflake Intelligence")
        
    except Exception as e:
        print(f"❌ Failed to create/register global_macro_strategy_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_market_structure_reports_agent(session: Session) -> None:
    """Create Market Structure Research Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    ai_schema = DemoConfig.SCHEMAS['AI']
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['market_reports_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {database_name}.{ai_schema}.MR_MARKET_REPORTS_AGENT
  COMMENT = 'Specialist in market structure analysis, regulatory changes, and institutional client insights'
  PROFILE = '{{"display_name": "{display_name}"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: {DemoConfig.AGENT_ORCHESTRATION_MODEL}
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "client_engagement_analyzer"
        description: "Analyzes client engagement patterns, trading activity, and discussion topics. Data Coverage: Client profiles, derivative trading history, research content engagement, and strategic discussion records. Use for understanding which clients care about specific regulatory topics, quantifying engagement metrics, and identifying outreach opportunities based on trading patterns and content interactions. When to Use: Questions about client segments, engagement levels, trading patterns, content downloads. When NOT to Use: Detailed regulatory analysis (use search_research_reports)."
    - tool_spec:
        type: "cortex_search"
        name: "search_research_reports"
        description: "Searches internal research reports including market structure analysis, regulatory updates, and FICC topics. Data Coverage: Frost Markets Intelligence research reports covering EMIR 3.0, bond market transparency, algorithmic trading, and other market structure themes. Use for understanding regulatory context, strategic implications, and firm positions on market structure changes. When to Use: Questions about regulatory changes, FICC developments, market structure trends. When NOT to Use: Client-specific data (use client_engagement_analyzer)."
  tool_resources:
    client_engagement_analyzer:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "{warehouse_name}"
      semantic_view: "{database_name}.AI.CLIENT_MARKET_IMPACT_VIEW"
    search_research_reports:
      search_service: "{database_name}.AI.RESEARCH_REPORTS_SEARCH"
      id_column: "REPORT_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    try:
        session.sql(sql).collect()
        print("✅ Created agent: market_structure_reports_agent")
        
        # Register with Snowflake Intelligence
        register_sql = f"""
        ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT 
        ADD AGENT {database_name}.{ai_schema}.MR_MARKET_REPORTS_AGENT
        """
        session.sql(register_sql).collect()
        print("✅ Registered agent with Snowflake Intelligence")
        
    except Exception as e:
        print(f"❌ Failed to create/register market_structure_reports_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_client_strategy_agent(session: Session) -> None:
    """Create Client Strategy Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    ai_schema = DemoConfig.SCHEMAS['AI']
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['client_strategy_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {database_name}.{ai_schema}.MR_CLIENT_STRATEGY_AGENT
  COMMENT = 'Strategic assistant for preparing data-driven client meetings and personalized recommendations'
  PROFILE = '{{"display_name": "{display_name}"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: {DemoConfig.AGENT_ORCHESTRATION_MODEL}
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "client_impact_analyzer"
        description: "Analyzes specific client trading patterns and exposure to market events. Data Coverage: Client profiles, derivative trading history, clearing relationships, and strategic discussion history. Use for understanding a specific client's trading patterns, FX hedging activity, clearing counterparty exposure, and how market or regulatory changes impact their operations. When to Use: Questions about a specific client's activity, trading patterns, exposure to regulatory changes. When NOT to Use: Broad engagement analysis across all clients (use client_engagement_analyzer), research content (use search_research_reports)."
    - tool_spec:
        type: "cortex_search"
        name: "search_research_reports"
        description: "Searches internal research reports for strategic guidance and recommendations. Data Coverage: Frost Markets Intelligence research covering regulatory changes, strategic recommendations for different client types, market structure guidance. Use for finding our firm's official positions, strategic recommendations, and guidance to share with clients. When to Use: Questions about firm recommendations, strategic guidance, regulatory advice, best practices. When NOT to Use: Client-specific data (use client_impact_analyzer)."
  tool_resources:
    client_impact_analyzer:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "{warehouse_name}"
      semantic_view: "{database_name}.AI.CLIENT_MARKET_IMPACT_VIEW"
    search_research_reports:
      search_service: "{database_name}.AI.RESEARCH_REPORTS_SEARCH"
      id_column: "REPORT_ID"
      title_column: "TITLE"
      max_results: 4
  $$;
"""
    
    try:
        session.sql(sql).collect()
        print("✅ Created agent: client_strategy_agent")
        
        # Register with Snowflake Intelligence
        register_sql = f"""
        ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT 
        ADD AGENT {database_name}.{ai_schema}.MR_CLIENT_STRATEGY_AGENT
        """
        session.sql(register_sql).collect()
        print("✅ Registered agent with Snowflake Intelligence")
        
    except Exception as e:
        print(f"❌ Failed to create/register client_strategy_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_market_risk_agent(session: Session) -> None:
    """Create Market Risk Analysis Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    ai_schema = DemoConfig.SCHEMAS['AI']
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['market_risk_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {database_name}.{ai_schema}.MR_MARKET_RISK_AGENT
  COMMENT = 'Expert assistant for real-time market risk assessment, portfolio stress testing, and firm-wide exposure analysis'
  PROFILE = '{{"display_name": "{display_name}"}}'
  FROM SPECIFICATION
  $$
  models:
    orchestration: {DemoConfig.AGENT_ORCHESTRATION_MODEL}
  instructions:
    response: "{response_formatted}"
    orchestration: "{orchestration_formatted}"
  tools:
    - tool_spec:
        type: "cortex_analyst_text_to_sql"
        name: "firm_exposure_analyzer"
        description: "Analyzes firm-wide portfolio exposure by sector, geography, and credit quality. Data Coverage: Current firm positions across all portfolios (Global Equities Fund, TMT Trading Book, Semiconductor Strategy), company sector classifications (Technology, Healthcare, Financial Services, Consumer Discretionary, Energy, Consumer Staples, Industrials), industry classifications (Semiconductors, Biotechnology, E-commerce, Electric Vehicles, etc.), geographic revenue exposure, and credit ratings. IMPORTANT: Companies are classified by both SECTOR (broad category like 'Technology') and INDUSTRY (specific category like 'Semiconductors'). When querying for semiconductor companies, use INDUSTRY = 'Semiconductors' NOT SECTOR. When querying for geographic exposure like Taiwan or China, use COUNTRY dimension. Use for: understanding firm risk concentrations, portfolio holdings, top exposures, sector/industry/geographic breakdowns, exposure to specific countries or regions, credit quality analysis. When to Use: Questions about firm exposure, portfolio holdings, concentration risk, sector exposure, industry exposure (semiconductors, biotech, etc.), geographic exposure (Taiwan, China, etc.), country-level analysis. When NOT to Use: Stress testing and VaR calculations (use calculate_portfolio_var), market news (use search_news_articles). Query Best Practices: For industry-specific queries like 'semiconductor companies' filter by INDUSTRY not SECTOR. For country exposure like 'Taiwan' or 'China', use COUNTRY dimension. For latest positions, filter to most recent AS_OF_DATE."
    - tool_spec:
        type: "generic"
        name: "calculate_portfolio_var"
        description: "Calculates portfolio Value-at-Risk using historical simulation methodology. Performs sophisticated risk analytics that quantify potential portfolio losses under normal and stressed market conditions. Data Coverage: 60-day historical price returns and current portfolio positions. Methodology: Historical simulation using daily returns distribution to calculate 99%% and 95%% confidence interval VaR. Use Cases: Stress testing portfolios under adverse price scenarios, quantifying downside risk exposure, calculating potential losses from market shocks, assessing portfolio risk during market events. Returns: Baseline VaR (99%% and 95%%), stressed VaR under specified shock scenario, total portfolio value, and methodology description. When to Use: Questions about stress testing, VaR calculations, scenario analysis, potential losses, risk quantification, downside exposure. When NOT to Use: Current exposure queries without stress scenarios (use firm_exposure_analyzer), market news context (use search_news_articles)."
        input_schema:
          type: "object"
          properties:
            TICKERS:
              description: "Array of stock ticker symbols to include in the portfolio VaR calculation. Example: ['NVDA', 'AMD', 'TSLA']. Required. Specify all tickers you want included in the risk analysis."
              type: "array"
            SHOCK_PERCENTAGE:
              description: "Price shock percentage to apply for stress testing scenario. Use negative values for price drops (e.g., -15 for 15%% decline, -20 for 20%% decline). Use positive values for price increases. This creates the stressed VaR scenario in addition to baseline VaR. Example: -15 means stress test with 15%% price drop across all tickers."
              type: "number"
          required: ["TICKERS", "SHOCK_PERCENTAGE"]
    - tool_spec:
        type: "cortex_search"
        name: "search_news_articles"
        description: "Searches news articles and market event coverage. Data Coverage: News articles with affected tickers, sources, and market events including geopolitical events, natural disasters, and market disruptions. Use for understanding real-time market context, finding news about specific events or companies, and connecting market developments to portfolio holdings. When to Use: Questions about market events, breaking news, recent developments, event context. When NOT to Use: Quantitative exposure data (use firm_exposure_analyzer), risk calculations (use calculate_portfolio_var)."
  tool_resources:
    firm_exposure_analyzer:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "{warehouse_name}"
      semantic_view: "{database_name}.AI.FIRM_EXPOSURE_VIEW"
    calculate_portfolio_var:
      execution_environment:
        query_timeout: 30
        type: "warehouse"
        warehouse: "{warehouse_name}"
      identifier: "{database_name}.AI.CALCULATE_PORTFOLIO_VAR"
      name: "CALCULATE_PORTFOLIO_VAR(ARRAY, FLOAT)"
      type: "procedure"
    search_news_articles:
      search_service: "{database_name}.AI.NEWS_ARTICLES_SEARCH"
      id_column: "ARTICLE_ID"
      title_column: "HEADLINE"
      max_results: 4
  $$;
"""
    
    try:
        session.sql(sql).collect()
        print("✅ Created agent: market_risk_agent")
        
        # Register with Snowflake Intelligence
        register_sql = f"""
        ALTER SNOWFLAKE INTELLIGENCE SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT 
        ADD AGENT {database_name}.{ai_schema}.MR_MARKET_RISK_AGENT
        """
        session.sql(register_sql).collect()
        print("✅ Registered agent with Snowflake Intelligence")
        
    except Exception as e:
        print(f"❌ Failed to create/register market_risk_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_all_agents(session: Session, scenarios: List[str] = None) -> None:
    """
    Create all Snowflake Intelligence agents for specified scenarios.
    
    Args:
        session: Snowpark session
        scenarios: List of scenario names to create agents for, or None for all
    """
    # Check for Snowflake Intelligence object first
    if not check_snowflake_intelligence(session):
        raise Exception("Snowflake Intelligence object not found. Please create it in Snowsight first.")
    
    if scenarios is None:
        scenarios = ['all']
    
    # Map scenarios to agent creation functions
    scenario_to_agent = {
        'equity_research_earnings': create_earnings_analysis_agent,
        'equity_research_thematic': create_thematic_research_agent,
        'global_macro_strategy': create_global_macro_strategy_agent,
        'global_research_reports': create_market_structure_reports_agent,
        'global_research_client_strategy': create_client_strategy_agent,
        'market_risk_analysis': create_market_risk_agent
    }
    
    print("\n🤖 Creating Snowflake Intelligence Agents...")
    
    for scenario, create_func in scenario_to_agent.items():
        if 'all' in scenarios or scenario in scenarios:
            try:
                create_func(session)
            except Exception as e:
                print(f"❌ Error creating agent for {scenario}: {e}")
                # Continue with other agents even if one fails
                continue
    
    print("✅ All agents created successfully\n")


if __name__ == "__main__":
    print("ℹ️  Agents are created automatically via SQL during setup.")
    print("   Run: python setup.py --mode=full")
    print("\n   Agents created:")
    print("   - Earnings Analysis Assistant")
    print("   - Thematic Investment Research Assistant")
    print("   - Global Macro Strategy Assistant")
