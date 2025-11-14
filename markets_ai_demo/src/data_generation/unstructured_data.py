# src/data_generation/unstructured_data.py
# Unstructured data generation using Cortex complete() for Frost Markets Intelligence Demo

import random
import sys
import os
from datetime import datetime, timedelta
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit
from snowflake.cortex import complete

# Add the src directory to the path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DemoConfig
from utils.date_utils import get_historical_quarters, get_dynamic_date_range, get_quarter_date_range


def get_current_and_previous_quarters():
    """Calculate current and previous quarters based on execution date"""
    quarters = get_historical_quarters(2)  # Get current and previous quarter
    current_quarter_raw = quarters[0]  # Most recent
    previous_quarter_raw = quarters[1]  # Previous
    
    # Convert YYYY-QN format to "QN YYYY" format for backward compatibility
    def format_quarter(q_str):
        year, quarter = q_str.split('-')
        return f"{quarter} {year}"
    
    # Extract years from the quarter strings
    current_year = int(current_quarter_raw.split('-')[0])
    previous_year = int(previous_quarter_raw.split('-')[0])
    
    return {
        'current_quarter': format_quarter(current_quarter_raw),
        'previous_quarter': format_quarter(previous_quarter_raw),
        'current_year': current_year,
        'previous_year': previous_year
    }


def generate_all_unstructured_data(session: Session) -> None:
    """Generate all unstructured documents using Cortex complete()"""
    
    print("   📄 Generating SEC filings...")
    generate_sec_filings(session)
    
    print("   🎤 Generating earnings call transcripts...")
    generate_earnings_transcripts(session)
    
    print("   📰 Generating news articles...")
    generate_news_articles(session)
    
    print("   📰 Generating carbon capture thematic news...")
    generate_carbon_capture_news(session)
    
    print("   📊 Generating research reports...")
    generate_research_reports(session)
    
    print("   ✅ All unstructured data generated")


def generate_sec_filings(session: Session) -> None:
    """Generate SEC 10-Q filings using event-driven prompts"""
    
    # Create table for SEC filings corpus
    create_table_sql = """
    CREATE OR REPLACE TABLE CURATED.SEC_FILINGS_CORPUS (
        FILING_ID STRING,
        TICKER VARCHAR(10),
        FISCAL_QUARTER VARCHAR(7),
        FILING_TYPE VARCHAR(4),
        TITLE VARCHAR(500),
        PROMPT VARCHAR(8000),
        FULL_TEXT VARCHAR(16777216)
    )
    """
    session.sql(create_table_sql).collect()
    
    # Get company and event data for context
    companies = session.table(f"{DemoConfig.SCHEMAS['CURATED']}.DIM_COMPANY").collect()
    events = session.table(f"{DemoConfig.SCHEMAS['RAW']}.MASTER_EVENT_LOG").collect()
    
    # Create events lookup
    events_by_ticker = {}
    for event in events:
        ticker = event['AFFECTED_TICKER']
        if ticker not in events_by_ticker:
            events_by_ticker[ticker] = []
        events_by_ticker[ticker].append(event)
    
    # Generate prompts for SEC filings
    filing_prompts = []
    # Use dynamic quarters for SEC filings (last 4 quarters)
    all_quarters = get_historical_quarters()
    quarters = all_quarters[:4]  # Most recent 4 quarters for SEC filings
    
    for company in companies[:8]:  # Generate for first 8 companies
        ticker = company['TICKER']
        company_name = company['COMPANY_NAME']
        sector = company['SECTOR']
        
        for quarter in quarters:
            # Find relevant events for this company/quarter
            relevant_events = []
            if ticker in events_by_ticker:
                # Use proper quarter date range calculation
                quarter_start, quarter_end = get_quarter_date_range(quarter)
                
                for event in events_by_ticker[ticker]:
                    event_date = datetime.strptime(str(event['EVENT_DATE']), "%Y-%m-%d")
                    if quarter_start <= event_date <= quarter_end:
                        relevant_events.append(event)
            
            # Generate financial metrics
            revenue = random.randint(8000, 25000)  # Revenue in millions
            revenue_growth = random.uniform(-5, 15)  # Revenue growth %
            net_income = revenue * random.uniform(0.05, 0.25)  # Net income
            
            # Create event context for the filing
            event_context = ""
            if relevant_events:
                event = relevant_events[0]  # Use first relevant event
                event_context = f"""
    
    Significant events that occurred this quarter which MUST be discussed:
    1. Event Type: {event['EVENT_TYPE']}
    2. Description: {event['EVENT_DESCRIPTION']}
    3. Impact: This event had a {'positive' if event['EXPECTED_SENTIMENT'] > 0 else 'negative'} impact on our operations and financials.
    """
            
            prompt = f"""You are an expert financial writer for a public company's legal and finance team.
Generate the "Item 2. Management's Discussion and Analysis of Financial Condition and Results of Operations" (MD&A) section for a Form 10-Q filing.

Company: {company_name} ({ticker})
Sector: {sector}
Fiscal Quarter: {quarter}

Key Financials to discuss:
- Revenue: ${revenue}M (a {revenue_growth:.1f}% {'increase' if revenue_growth > 0 else 'decrease'} year-over-year)
- Net Income: ${net_income:.0f}M
{event_context}

Instructions:
- Write in a formal, cautious, and legally compliant tone typical of SEC filings
- Include a "Forward-Looking Statements" disclaimer
- Compare results to the same quarter in the prior year
- Explain the drivers of revenue performance and operational changes
- If events occurred, discuss their material impact on the business
- Structure with clear headers: Overview, Results of Operations, Liquidity and Capital Resources
- Length should be 500-800 words
- Do not generate any other sections of the 10-Q
- Use financial terminology and be specific about operational metrics"""
            
            # Generate TITLE in format: "Q2 2024 10-Q Filing - Apple Inc."
            quarter_year = quarter.split('-')[0]  # e.g., "2024"
            quarter_num = quarter.split('-')[1]   # e.g., "Q2"
            filing_title = f"{quarter_num} {quarter_year} 10-Q Filing - {company_name}"
            
            filing_prompts.append({
                "FILING_ID": f"10Q_{ticker}_{quarter}",
                "TICKER": ticker,
                "FISCAL_QUARTER": quarter,
                "FILING_TYPE": "10-Q",
                "TITLE": filing_title,
                "PROMPT": prompt
            })
    
    # Generate content using Cortex complete()
    _generate_content_with_cortex(session, filing_prompts, "CURATED.SEC_FILINGS_CORPUS")


def generate_earnings_transcripts(session: Session) -> None:
    """Generate earnings call transcripts"""
    
    create_table_sql = """
    CREATE OR REPLACE TABLE CURATED.EARNINGS_TRANSCRIPTS_CORPUS (
        TRANSCRIPT_ID STRING,
        TICKER VARCHAR(10),
        FISCAL_QUARTER VARCHAR(7),
        TITLE VARCHAR(500),
        PROMPT VARCHAR(8000),
        FULL_TEXT VARCHAR(16777216)
    )
    """
    session.sql(create_table_sql).collect()
    
    # Get data for context
    companies = session.table(f"{DemoConfig.SCHEMAS['CURATED']}.DIM_COMPANY").collect()
    events = session.table(f"{DemoConfig.SCHEMAS['RAW']}.MASTER_EVENT_LOG").collect()
    
    events_by_ticker = {}
    for event in events:
        ticker = event['AFFECTED_TICKER']
        if ticker not in events_by_ticker:
            events_by_ticker[ticker] = []
        events_by_ticker[ticker].append(event)
    
    transcript_prompts = []
    # Use dynamic quarters based on current date - limit to last 3 quarters for transcripts
    all_quarters = get_historical_quarters()
    quarters = all_quarters[:3]  # Most recent 3 quarters for transcripts
    
    # Strategic: Ensure Netflix is always included for earnings scenario
    selected_companies = []
    
    # Always include Netflix if it exists
    netflix_company = [c for c in companies if c['TICKER'] == 'NFLX']
    if netflix_company:
        selected_companies.extend(netflix_company)
    
    # Add other companies to reach 6 total
    other_companies = [c for c in companies if c['TICKER'] != 'NFLX']
    selected_companies.extend(other_companies[:6-len(selected_companies)])
    
    for company in selected_companies:
        ticker = company['TICKER']
        company_name = company['COMPANY_NAME']
        sector = company['SECTOR']
        
        for quarter in quarters:
            # Find relevant events
            relevant_events = []
            if ticker in events_by_ticker:
                # Use proper quarter date range calculation
                quarter_start, quarter_end = get_quarter_date_range(quarter)
                
                for event in events_by_ticker[ticker]:
                    event_date = datetime.strptime(str(event['EVENT_DATE']), "%Y-%m-%d")
                    if quarter_start <= event_date <= quarter_end:
                        relevant_events.append(event)
            
            # Generate metrics for the call
            revenue = random.randint(8000, 25000)
            eps = random.uniform(1.5, 6.0)
            guidance_change = random.choice(["raising", "maintaining", "lowering"])
            
            event_questions = ""
            if relevant_events:
                event = relevant_events[0]
                event_questions = f"""
    
In the Q&A section, one analyst MUST ask a specific question about: "{event['EVENT_DESCRIPTION']}"
The CEO should provide a {"confident and optimistic" if event['EXPECTED_SENTIMENT'] > 0 else "cautious but reassuring"} response addressing the situation.
"""
            
            prompt = f"""Generate a realistic earnings call transcript for {company_name} ({ticker}) for their {quarter} results.

The transcript must have two distinct sections:
1. "Prepared Remarks" (CEO and CFO presentations)
2. "Question-and-Answer Session" (analyst questions and management responses)

Key Results to Discuss:
- Revenue: ${revenue}M 
- EPS: ${eps:.2f}
- Guidance: Management is {guidance_change} full-year guidance
- Sector: {sector} industry trends

Prepared Remarks Structure:
- CEO: Opens with quarter highlights, strategic initiatives, market conditions
- CFO: Reviews financial details, margins, cash flow, provides guidance

Q&A Section Requirements:
- Include questions from 3 fictional analysts from major banks (Goldman Sachs, Morgan Stanley, JPMorgan)
- Cover topics: financial performance, guidance, industry trends, strategic priorities
- Management should give detailed, realistic responses{event_questions}

Style Guidelines:
- Use realistic financial terminology and metrics
- Include typical earnings call language and phrases
- Make responses sound authentic to executive communication style
- Length: 1200-1500 words total
- Include realistic analyst firm names and analyst names"""
            
            # Generate TITLE in format: "Q2 2024 Earnings Call - Apple Inc."
            quarter_year = quarter.split('-')[0]  # e.g., "2024"
            quarter_num = quarter.split('-')[1]   # e.g., "Q2"
            transcript_title = f"{quarter_num} {quarter_year} Earnings Call - {company_name}"
            
            transcript_prompts.append({
                "TRANSCRIPT_ID": f"CALL_{ticker}_{quarter}",
                "TICKER": ticker,
                "FISCAL_QUARTER": quarter,
                "TITLE": transcript_title,
                "PROMPT": prompt
            })
    
    _generate_content_with_cortex(session, transcript_prompts, "CURATED.EARNINGS_TRANSCRIPTS_CORPUS")


def generate_news_articles(session: Session) -> None:
    """Generate news articles corpus based on events"""
    
    create_table_sql = """
    CREATE OR REPLACE TABLE CURATED.NEWS_ARTICLES_CORPUS (
        ARTICLE_ID STRING,
        AFFECTED_TICKER VARCHAR(10),
        PUBLISHED_AT TIMESTAMP_NTZ,
        SOURCE VARCHAR(50),
        HEADLINE VARCHAR(500),
        PROMPT VARCHAR(8000),
        BODY VARCHAR(16777216)
    )
    """
    session.sql(create_table_sql).collect()
    
    # Get events to generate news articles
    events = session.table(f"{DemoConfig.SCHEMAS['RAW']}.MASTER_EVENT_LOG").collect()
    companies = {row['TICKER']: row['COMPANY_NAME'] for row in session.table(f"{DemoConfig.SCHEMAS['CURATED']}.DIM_COMPANY").collect()}
    
    news_prompts = []
    sources = ["Reuters", "Bloomberg", "Wall Street Journal", "Financial Times", "MarketWatch"]
    
    for i, event in enumerate(events):
        ticker = event['AFFECTED_TICKER']
        company_name = companies.get(ticker, f"Company {ticker}")
        event_description = event['EVENT_DESCRIPTION']
        event_type = event['EVENT_TYPE']
        sentiment = event['EXPECTED_SENTIMENT']
        event_date = event['EVENT_DATE']
        
        # Generate headline based on event
        if sentiment > 0.5:
            headline_template = f"{company_name} ({ticker}) Shares Surge After {event_type}"
        elif sentiment < -0.5:
            headline_template = f"{company_name} ({ticker}) Faces Challenges Following {event_type}"
        else:
            headline_template = f"{company_name} ({ticker}) Announces {event_type}"
        
        # Create publication timestamp (same day as event, business hours)
        # Convert event_date to date object if it's a string
        if isinstance(event_date, str):
            event_date_obj = datetime.strptime(event_date, "%Y-%m-%d").date()
        else:
            event_date_obj = event_date
        
        pub_time = datetime.combine(event_date_obj, datetime.min.time().replace(hour=random.randint(9, 16), minute=random.randint(0, 59)))
        
        prompt = f"""You are a financial journalist writing for {random.choice(sources)}. Write a news article with the following headline: "{headline_template}"

The article must report on the following event:
- Company: {company_name} ({ticker})
- Event: {event_description}
- Event Type: {event_type}

Article Requirements:
- Professional, objective financial journalism tone
- Approximately 400-500 words
- Include a realistic quote from the company's CEO or spokesperson
- Include a realistic quote from a market analyst at a major investment bank
- Mention the immediate impact on the company's stock price
- Provide relevant background context about the company and industry
- Include specific details that make the story credible
- Use proper financial journalism style and terminology

Structure:
1. Lead paragraph with key facts
2. Company statement/reaction
3. Market/analyst reaction
4. Background and context
5. Industry implications

Make the article feel authentic and well-researched."""
        
        news_prompts.append({
            "ARTICLE_ID": f"NEWS_{i+1:03d}",
            "AFFECTED_TICKER": ticker,
            "PUBLISHED_AT": pub_time.strftime("%Y-%m-%d %H:%M:%S"),
            "SOURCE": random.choice(sources),
            "HEADLINE": headline_template,
            "PROMPT": prompt
        })
    
    _generate_content_with_cortex(session, news_prompts, "CURATED.NEWS_ARTICLES_CORPUS")


def generate_research_reports(session: Session) -> None:
    """Generate internal research reports corpus for search capabilities"""
    
    create_table_sql = """
    CREATE OR REPLACE TABLE CURATED.RESEARCH_REPORTS_CORPUS (
        REPORT_ID STRING,
        TITLE VARCHAR(500),
        REPORT_TYPE VARCHAR(50),
        PUBLISHED_DATE DATE,
        AUTHOR VARCHAR(100),
        THEMATIC_TAGS VARCHAR(500),
        PROMPT VARCHAR(8000),
        FULL_TEXT VARCHAR(16777216)
    )
    """
    session.sql(create_table_sql).collect()
    
    research_prompts = []
    
    # Get dynamic quarter information
    quarter_info = get_current_and_previous_quarters()
    prev_quarter = quarter_info['previous_quarter']
    current_quarter = quarter_info['current_quarter']
    
    # Generate thematic research reports with dynamic quarters
    thematic_reports = [
        {
            "title": f"{prev_quarter} FICC Market Structure Review: EMIR 3.0 and EMEA Regulatory Landscape",
            "type": "Market Structure",
            "tags": f"FICC, EMEA, EMIR 3.0, Derivatives Clearing, Regulatory Change, Bond Markets, {prev_quarter}",
            "focus": f"Comprehensive review of FICC market structure developments in EMEA during {prev_quarter}, focusing on EMIR 3.0 implementation, bond market transparency initiatives, and algorithmic trading adoption in European fixed income markets"
        },
        {
            "title": f"EMEA Bond Market Transparency {current_quarter}: MiFID II Evolution and Electronic Trading Impact",
            "type": "Market Structure",
            "tags": f"FICC, EMEA, Bond Markets, MiFID II, Electronic Trading, Market Transparency, European Fixed Income, {current_quarter}",
            "focus": f"Analysis of bond market transparency improvements in EMEA during {current_quarter} under evolving MiFID II framework and growth of electronic trading platforms in European fixed income markets"
        },
        {
            "title": f"Global Macro Outlook {current_quarter}: Navigating the Shifting Liquidity Landscape",
            "type": "Global Macro Strategy",
            "tags": f"Global Macro, Central Bank Policy, Liquidity, Economic Outlook, Investment Strategy, {current_quarter}",
            "focus": f"Comprehensive analysis of global macroeconomic conditions in {current_quarter}, examining central bank policy shifts, liquidity conditions, and their implications for cross-asset portfolio positioning"
        },
        {
            "title": "Trade Activity Indicators and Growth Forecasts: A Data-Driven Approach",
            "type": "Global Macro Strategy",
            "tags": "Global Trade, Shipping Volumes, Economic Growth, Leading Indicators, Manufacturing",
            "focus": "Analysis of global trade activity and shipping volume data as leading indicators for economic growth, with investment implications across sectors"
        },
        {
            "title": "Sector Rotation Strategy: Positioning for the Next Macro Regime",
            "type": "Global Macro Strategy",
            "tags": "Sector Rotation, Macro Strategy, Asset Allocation, Economic Cycle, Investment Strategy",
            "focus": "Strategic sector positioning recommendations based on macroeconomic signal analysis and correlation patterns with proprietary indicators"
        },
        {
            "title": "Carbon Capture Technologies: Investment Opportunities in Climate Solutions",
            "type": "Thematic Research",
            "tags": "Carbon Capture, Direct Air Capture, Climate Technology",
            "focus": "Direct air capture technology trends and investment opportunities"
        },
        {
            "title": "Johnson Matthey: Competitive Position in Carbon Capture Catalysts",
            "type": "Company Analysis",
            "tags": "Johnson Matthey, JMPLY, Carbon Capture, Catalysts, Materials Science, Competitive Analysis",
            "focus": "Deep dive analysis of Johnson Matthey's catalyst technology for carbon capture, market share dynamics, competitive pressures from emerging players, and balanced assessment of growth opportunities versus execution challenges"
        },
        {
            "title": "Linde's Carbon Capture Infrastructure Leadership: Scale Advantages in Industrial Gases",
            "type": "Company Analysis",
            "tags": "Linde, LIN, Carbon Capture, Industrial Gases, Infrastructure, Market Leadership",
            "focus": "Analysis of Linde's dominant position in carbon capture infrastructure through industrial gases expertise, operational scale advantages, global facility network, and strategic partnerships with energy companies"
        },
        {
            "title": "Industrial Automation in Carbon Capture: Siemens' Strategic Opportunity",
            "type": "Company Analysis",
            "tags": "Siemens, SIEGY, Carbon Capture, Industrial Automation, Process Control, Growth Markets",
            "focus": "Assessment of Siemens' role in carbon capture facility automation and process control systems, technology integration capabilities, and addressable market opportunity in the growing carbon capture sector"
        },
        {
            "title": "Semiconductor Supply Chain Resilience: Navigating Geopolitical Risks",
            "type": "Sector Analysis",
            "tags": "Semiconductors, Supply Chain, Geopolitical Risk",
            "focus": "Semiconductor industry supply chain vulnerabilities and risk mitigation"
        },
        {
            "title": "ESG Integration in Portfolio Management: Beyond Compliance",
            "type": "Strategy Report",
            "tags": "ESG, Portfolio Management, Sustainability",
            "focus": "Advanced ESG integration strategies for institutional investors"
        }
    ]
    
    for i, report in enumerate(thematic_reports):
        # Use dynamic date range for publication dates
        start_date, end_date = get_dynamic_date_range()
        random_days = random.randint(30, (end_date - start_date).days - 30)  # Leave some buffer
        pub_date = start_date + timedelta(days=random_days)
        
        # Customize prompt based on report type
        if report['type'] == "Global Macro Strategy":
            prompt = f"""You are a senior global macro strategist at Frost Markets Intelligence writing an authoritative research report.

Report Title: {report['title']}
Report Type: {report['type']}
Focus Area: {report['focus']}

Write a comprehensive global macro strategy report that includes:

1. Executive Summary (2-3 paragraphs)
   - Key macroeconomic findings and cross-asset investment implications
   - Main strategic recommendations for portfolio positioning

2. Global Macro Analysis (4-5 paragraphs)
   - Analysis of our proprietary macroeconomic signals including:
     * Frost Global Shipping Volume Index (trade activity indicator)
     * Frost Central Bank Liquidity Indicator (monetary policy stance)
     * Frost Manufacturing PMI Composite (economic activity gauge)
     * Frost Consumer Sentiment Index (consumer outlook)
     * Frost Credit Conditions Indicator (financial conditions)
     * Frost Commodity Price Momentum (commodity trends)
   - Central bank policy trends and implications (Fed, ECB, BOJ, PBOC)
   - Global growth outlook and regional divergences
   - Key macro risks and opportunities

3. Sector Implications (3-4 paragraphs)
   - Sector rotation recommendations based on macro signals
   - Analysis of sector correlations with our proprietary indicators
   - Technology sector outlook given capex trends
   - Energy sector positioning given commodity dynamics
   - Financial services outlook given credit conditions and liquidity
   - Consumer sector views given sentiment and spending indicators

4. Strategic Recommendations (2-3 paragraphs)
   - Specific cross-asset allocation recommendations
   - Geographic positioning (US, Europe, Emerging Markets, Asia)
   - Hedging strategies for macro risks
   - Tactical opportunities in current environment

5. Conclusion (1-2 paragraphs)
   - Summary of key macro themes
   - Forward-looking perspective and key indicators to watch

Style Requirements:
- Professional, authoritative tone suitable for institutional investors
- Reference our proprietary Frost indicators by name (e.g., "The Frost Global Shipping Volume Index declined 3.2% this quarter...")
- Include specific data points, index levels, and trend analysis
- Discuss macro regime shifts and investment implications
- Use sophisticated macro and investment terminology
- Length: 1200-1500 words
- Make recommendations specific, actionable, and cross-asset focused

This report will guide institutional clients' strategic asset allocation and macro positioning decisions."""
        
        elif report['type'] == "Thematic Research":
            prompt = f"""You are a senior thematic research analyst at Frost Markets Intelligence writing an authoritative research report that synthesizes external research, expert interviews, and industry analysis.

Report Title: {report['title']}
Report Type: {report['type']}
Focus Area: {report['focus']}

Write a comprehensive thematic research report that includes:

1. Executive Summary (2-3 paragraphs)
   - Key technology trends and investment thesis
   - Main investment opportunities and target companies
   - Summary of research methodology (external sources analyzed)

2. Technology Landscape and Innovation Trends (4-5 paragraphs)
   - Overview of Direct Air Capture (DAC) technology evolution
   - Key technological breakthroughs in solid sorbent materials and modular designs
   - Reference specific external research sources, for example:
     * "According to a recent Nature Climate Change study by researchers at ETH Zurich..."
     * "Patent filings analysis reveals a 340% increase in solid sorbent applications (USPTO database, 2023-2024)"
     * "Dr. Jennifer Klaus at the Carbon Capture Innovation Institute notes in a recent interview..."
   - Comparison of DAC vs. traditional point-source capture
   - Cost trajectory analysis and commercialization timeline

3. Industry Expert Perspectives (3-4 paragraphs)
   - Include 2-3 fictional expert interview quotes, such as:
     * Quote from a CTO at a carbon capture technology company
     * Quote from an academic researcher at a leading university
     * Quote from an industry analyst or consultant
   - Expert views on technological barriers and breakthroughs
   - Insights on policy support and regulatory landscape
   - Discussion of capital requirements and scaling challenges

4. Company Ecosystem and Investment Opportunities (4-5 paragraphs)
   - Publicly traded companies with significant exposure:
     * Johnson Matthey - catalyst and materials supplier
     * Linde - industrial gases and carbon capture infrastructure
     * Siemens - industrial equipment and automation systems
   - Specific roles each company plays in the DAC value chain
   - Mention frequency of company names in patent filings and research papers
   - Analysis of competitive positioning and technology partnerships
   - Discussion of private market players (Climeworks, Carbon Engineering) and IPO potential

5. Investment Thesis and Recommendations (2-3 paragraphs)
   - Specific stock recommendations from the three public companies mentioned
   - Positioning within broader climate technology portfolio
   - Risk factors and key milestones to monitor
   - Valuation considerations and timeline expectations

6. Conclusion (1-2 paragraphs)
   - Summary of investment opportunity
   - Key catalysts and signposts to watch

Style Requirements:
- Professional, authoritative tone suitable for institutional investors
- Include specific citations to external sources (academic papers, patents, expert interviews)
- Use realistic but fictional reference examples like:
  * "Nature Climate Change (2024), 'Advances in Solid Sorbent Materials for DAC'"
  * "US Patent US2024-1234567, filed by Climeworks AG"
  * "Interview with Dr. Michael Chen, Director of Carbon Capture Research, Stanford University"
- Include specific data points, percentages, and market figures
- Reference the three public companies (Johnson Matthey, Linde, Siemens) prominently
- Use technical terminology appropriately (solid sorbents, temperature swing adsorption, modular DAC units)
- Length: 1200-1500 words
- Make recommendations specific, actionable, and backed by research synthesis

This report demonstrates our research team's ability to synthesize external academic research, patent analysis, and expert interviews into actionable investment insights."""
        
        elif report['type'] == "Company Analysis":
            prompt = f"""You are a senior equity research analyst at Frost Markets Intelligence writing a detailed company analysis report focused on carbon capture opportunities.

Report Title: {report['title']}
Report Type: {report['type']}
Focus Area: {report['focus']}

Write a comprehensive company analysis that includes:

1. Executive Summary (2-3 paragraphs)
   - Company's strategic position in carbon capture market
   - Key investment thesis (both opportunities and risks)
   - Overall assessment and recommendation

2. Company Overview and Carbon Capture Strategy (3-4 paragraphs)
   - Core business model and carbon capture segment
   - Technology platform and competitive advantages
   - Strategic initiatives and capital allocation
   - Management's carbon capture vision and execution track record

3. Competitive Position and Market Dynamics (4-5 paragraphs)
   - Market share analysis in carbon capture subsegment
   - Competitive landscape (name 2-3 specific competitors)
   - Barriers to entry and sustainable advantages
   - Pricing power and margin dynamics
   - Recent competitive developments and market share shifts

4. Financial Performance and Outlook (3-4 paragraphs)
   - Revenue contribution from carbon capture activities
   - Profitability and margin trends
   - R&D investment levels and innovation pipeline
   - Capital requirements for growth
   - Financial projections and key assumptions

5. Risk Factors and Challenges (2-3 paragraphs)
   - Technology risks and execution challenges
   - Competitive threats and market share pressure
   - Regulatory and policy dependencies
   - Customer concentration or supply chain risks
   - Include specific concerns relevant to the company

6. Investment Recommendation (2-3 paragraphs)
   - Valuation assessment and target price considerations
   - Relative positioning vs. peers
   - Key catalysts and milestones to monitor
   - Risk/reward balance

7. Conclusion (1-2 paragraphs)
   - Summary of balanced investment view
   - Key monitoring points for thesis evolution

Style Requirements:
- Professional, balanced equity research tone
- Include BOTH bullish and bearish perspectives
- Use specific financial metrics, percentages, and market data
- Reference industry reports, management commentary, and competitive intelligence
- For Johnson Matthey specifically: discuss competitive pressures and execution challenges alongside technology strengths
- For Linde specifically: emphasize scale advantages and infrastructure network
- For Siemens specifically: focus on automation opportunity and technology integration
- Include realistic but fictional financial projections
- Length: 1200-1500 words
- Provide nuanced, actionable investment analysis

This report should demonstrate deep fundamental analysis of the company's carbon capture positioning with balanced assessment of opportunities and risks."""
        
        else:
            # Original prompt for non-macro reports
            prompt = f"""You are a senior research analyst at Frost Markets Intelligence writing an authoritative research report.

Report Title: {report['title']}
Report Type: {report['type']}
Focus Area: {report['focus']}

Write a comprehensive research report that includes:

1. Executive Summary (2-3 paragraphs)
   - Key findings and investment implications
   - Main recommendations for clients

2. Market Overview (3-4 paragraphs)
   - Current market conditions and trends in FICC markets (Fixed Income, Currency, Commodities)
   - Regulatory environment and recent changes (EMIR 3.0, MiFID II, bond transparency)
   - Key drivers and challenges affecting EMEA derivatives and bond markets

3. Strategic Recommendations (2-3 paragraphs)
   - Specific actionable advice for institutional clients, especially asset managers
   - Risk management considerations for FICC trading and derivatives clearing
   - Implementation strategies for regulatory compliance (EMIR 3.0, bond transparency)

4. Conclusion (1-2 paragraphs)
   - Summary of key points
   - Forward-looking perspective

Style Requirements:
- Professional, authoritative tone suitable for institutional clients
- Include specific data points, percentages, and market figures (realistic but fictional)
- Reference regulatory bodies, industry associations, and market trends
- Use sophisticated financial terminology
- Length: 1000-1200 words
- Make recommendations specific and actionable

This report will be used by relationship managers for client discussions and should demonstrate deep market expertise.

Special Instructions for Market Structure Reports:
- Prominently mention 'FICC market structure developments in EMEA'
- Reference specific quarters ({prev_quarter} for completed analysis, {current_quarter} for current developments) and timeframes
- Discuss bond market transparency, derivatives clearing, and algorithmic trading
- Focus on regulatory changes affecting European fixed income and derivatives markets
- Include impact analysis for different client types, especially asset managers"""
        
        research_prompts.append({
            "REPORT_ID": f"RPT_{i+1:03d}",
            "TITLE": report['title'],
            "REPORT_TYPE": report['type'],
            "PUBLISHED_DATE": pub_date.strftime("%Y-%m-%d"),
            "AUTHOR": f"Frost Markets Intelligence {report['type']} Team",
            "THEMATIC_TAGS": report['tags'],
            "PROMPT": prompt
        })
    
    _generate_content_with_cortex(session, research_prompts, "CURATED.RESEARCH_REPORTS_CORPUS")


def generate_carbon_capture_news(session: Session) -> None:
    """Generate thematic news articles specifically about carbon capture companies"""
    
    # Get dynamic date range
    start_date, end_date = get_dynamic_date_range()
    
    # Define carbon capture themed news articles
    carbon_news = [
        {
            "ticker": "JMPLY",
            "company": "Johnson Matthey",
            "headline": "Johnson Matthey Unveils Next-Generation Carbon Capture Catalyst Platform",
            "source": "Reuters",
            "focus": "New catalyst technology launch with improved efficiency and cost reduction claims"
        },
        {
            "ticker": "LIN",
            "company": "Linde",
            "headline": "Linde Expands Carbon Capture Operations with New North American Facilities",
            "source": "Bloomberg",
            "focus": "Facility expansion announcement and capacity increase for carbon capture services"
        },
        {
            "ticker": "SIEGY",
            "company": "Siemens",
            "headline": "Siemens Wins $300M Carbon Capture Facility Automation Contract",
            "source": "Wall Street Journal",
            "focus": "Major contract win for automation and control systems at carbon capture facility"
        },
        {
            "ticker": "JMPLY",
            "company": "Johnson Matthey",
            "headline": "Johnson Matthey Faces Increased Competition in Carbon Capture Materials Market",
            "source": "Financial Times",
            "focus": "Analysis of competitive pressures and market share challenges from new entrants"
        },
        {
            "ticker": "LIN",
            "company": "Linde",
            "headline": "Linde Partners with Major Oil Company on Carbon Capture Infrastructure Project",
            "source": "MarketWatch",
            "focus": "Strategic partnership announcement for large-scale carbon capture deployment"
        }
    ]
    
    news_prompts = []
    
    for i, article in enumerate(carbon_news):
        # Generate random publication date within the date range
        days_diff = (end_date - start_date).days
        random_days = random.randint(30, days_diff - 30)
        pub_date = start_date + timedelta(days=random_days)
        pub_time = datetime.combine(pub_date, datetime.min.time().replace(hour=random.randint(9, 16), minute=random.randint(0, 59)))
        
        prompt = f"""You are a financial journalist writing for {article['source']}. Write a news article with the following headline: "{article['headline']}"

The article must cover:
- Company: {article['company']} ({article['ticker']})
- Focus: {article['focus']}
- Context: Carbon capture technology and climate solutions market

Article Requirements:
- Professional, objective financial journalism tone
- Approximately 400-500 words
- Include a realistic quote from the company's spokesperson or executive
- Include a realistic quote from an industry analyst or market expert
- Discuss the implications for the carbon capture industry
- Provide background on the company's carbon capture strategy
- Include specific technical or financial details that make the story credible
- Use proper financial journalism style and terminology

Structure:
1. Lead paragraph with key facts
2. Company statement and details
3. Industry expert analysis
4. Background and market context
5. Competitive landscape implications
6. Forward-looking perspective

Make the article feel authentic, well-researched, and provide balanced coverage."""
        
        news_prompts.append({
            "ARTICLE_ID": f"CARBON_NEWS_{i+1:03d}",
            "AFFECTED_TICKER": article['ticker'],
            "PUBLISHED_AT": pub_time.strftime("%Y-%m-%d %H:%M:%S"),
            "SOURCE": article['source'],
            "HEADLINE": article['headline'],
            "PROMPT": prompt
        })
    
    # Append to existing news articles table
    _generate_content_with_cortex(session, news_prompts, "CURATED.NEWS_ARTICLES_CORPUS", append=True)


def _generate_content_with_cortex(session: Session, prompts_data: list, target_table: str, append: bool = False) -> None:
    """
    Generic function to generate content using Cortex complete()
    Follows the 5-step process: prompts -> table -> DataFrame -> with_column -> save
    """
    
    if not prompts_data:
        print(f"     ⚠️  No prompts to generate for {target_table}")
        return
    
    # Step 1 & 2: Prompts already generated, store in temporary table
    # Extract just the table name without schema for temp table
    table_name_only = target_table.split('.')[-1]  # Gets "SEC_FILINGS_CORPUS" from "RAW.SEC_FILINGS_CORPUS"
    temp_table = f"{DemoConfig.SCHEMAS['RAW']}.TEMP_PROMPTS_{table_name_only}"
    prompts_df = session.create_dataframe(prompts_data)
    prompts_df.write.mode("overwrite").save_as_table(temp_table)
    
    print(f"     📝 Generated {len(prompts_data)} prompts for {target_table}")
    
    # Step 3: Create Snowpark DataFrame from prompt table
    temp_df = session.table(temp_table)
    
    # Step 4: Use with_column to create generated content
    print(f"     🤖 Generating content with Cortex (model: {DemoConfig.CORTEX_MODEL_NAME})...")
    
    try:
        # Add content column based on table type (check against table name only)
        if table_name_only == "SEC_FILINGS_CORPUS":
            content_df = temp_df.with_column(
                "FULL_TEXT",
                complete(lit(DemoConfig.CORTEX_MODEL_NAME), col("PROMPT"))
            )
        elif table_name_only == "EARNINGS_TRANSCRIPTS_CORPUS":
            content_df = temp_df.with_column(
                "FULL_TEXT", 
                complete(lit(DemoConfig.CORTEX_MODEL_NAME), col("PROMPT"))
            )
        elif table_name_only == "NEWS_ARTICLES_CORPUS":
            content_df = temp_df.with_column(
                "BODY",
                complete(lit(DemoConfig.CORTEX_MODEL_NAME), col("PROMPT"))
            )
        elif table_name_only == "RESEARCH_REPORTS_CORPUS":
            content_df = temp_df.with_column(
                "FULL_TEXT",
                complete(lit(DemoConfig.CORTEX_MODEL_NAME), col("PROMPT"))
            )
        else:
            raise ValueError(f"Unknown target table: {target_table}")
        
        # Step 5: Save to final destination table
        write_mode = "append" if append else "overwrite"
        content_df.write.mode(write_mode).save_as_table(target_table)
        
        action = "appended to" if append else "saved to"
        print(f"     ✅ Generated content {action} {target_table}")
        
        # Clean up temporary table
        session.sql(f"DROP TABLE IF EXISTS {temp_table}").collect()
        
    except Exception as e:
        print(f"     ❌ Error generating content for {target_table}: {str(e)}")
        print(f"     💡 Prompts saved in {temp_table} for debugging")
        raise
