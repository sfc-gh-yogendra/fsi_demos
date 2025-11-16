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
            "planning_instructions": "TBD - Phase 2",
            "response_instructions": "TBD - Phase 2"
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
            "planning_instructions": "TBD - Phase 2", 
            "response_instructions": "TBD - Phase 2"
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
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['earnings_analysis_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {DemoConfig.AGENT_SCHEMA}.MR_EARNINGS_ANALYSIS_AGENT
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
    except Exception as e:
        print(f"❌ Failed to create earnings_analysis_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_thematic_research_agent(session: Session) -> None:
    """Create Thematic Investment Research Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['thematic_research_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {DemoConfig.AGENT_SCHEMA}.MR_THEMATIC_RESEARCH_AGENT
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
    except Exception as e:
        print(f"❌ Failed to create thematic_research_agent: {str(e)}")
        print(f"📋 Full SQL attempted:")
        print(sql)
        raise


def create_global_macro_strategy_agent(session: Session) -> None:
    """Create Global Macro Strategy Assistant agent via SQL"""
    database_name = DemoConfig.DATABASE_NAME
    warehouse_name = DemoConfig.COMPUTE_WAREHOUSE
    
    # Get instructions from existing configs
    config = get_agent_configs()['global_macro_strategy_agent']
    display_name = config['display_name']
    response_formatted = format_instructions_for_yaml(config['response_instructions'])
    orchestration_formatted = format_instructions_for_yaml(config['planning_instructions'])
    
    sql = f"""
CREATE OR REPLACE AGENT {DemoConfig.AGENT_SCHEMA}.MR_GLOBAL_MACRO_STRATEGY_AGENT
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
    except Exception as e:
        print(f"❌ Failed to create global_macro_strategy_agent: {str(e)}")
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
    if scenarios is None:
        scenarios = ['all']
    
    # Map scenarios to agent creation functions
    scenario_to_agent = {
        'equity_research_earnings': create_earnings_analysis_agent,
        'equity_research_thematic': create_thematic_research_agent,
        'global_macro_strategy': create_global_macro_strategy_agent,
        'global_research_reports': None,  # Phase 2 - not implemented yet
        'global_research_client_strategy': None  # Phase 2 - not implemented yet
    }
    
    print("\n🤖 Creating Snowflake Intelligence Agents...")
    
    for scenario, create_func in scenario_to_agent.items():
        if 'all' in scenarios or scenario in scenarios:
            if create_func is None:
                print(f"⏭️  Skipping {scenario} (not implemented yet)")
                continue
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
