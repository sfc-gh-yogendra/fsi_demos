# SAM Demo - Scenario Scripts

Reference: See `docs/implementation_plan.md` for the build order and implementation details referenced by these scenarios.

Complete demo scenarios organized by role and agent, with step-by-step conversations, expected responses, and data flows.

## Available Scenarios by Role

### Portfolio Manager
**Agent: Portfolio Copilot** ✅ **IMPLEMENTED**
- Portfolio Insights & Benchmarking ✅ **READY FOR DEMO**

**Agent: Thematic Macro Advisor** ✅ **IMPLEMENTED**  
- Investment Theme Analysis ✅ **READY FOR DEMO**

### Research Analyst
**Agent: Research Copilot** ✅ **IMPLEMENTED**
- Document Research & Analysis ✅ **READY FOR DEMO**
- Earnings Intelligence Extensions ✅ **READY FOR DEMO**

### Quantitative Analyst
**Agent: Quant Analyst** ✅ **IMPLEMENTED**
- Factor Analysis & Performance Attribution ✅ **READY FOR DEMO**

### Client Relations
**Agent: Sales Advisor** ✅ **IMPLEMENTED**
- Client Reporting & Template Formatting ✅ **READY FOR DEMO**

### Risk & Compliance Officer
**Agent: ESG Guardian** 🔄 **READY FOR IMPLEMENTATION**
- ESG Risk Monitoring & Policy Compliance 🔄 **REQUIRES ESG DOCUMENTS**

**Agent: Compliance Advisor** 🔄 **READY FOR IMPLEMENTATION**
- Mandate Monitoring & Breach Detection 🔄 **REQUIRES POLICY DOCUMENTS**

---

## Portfolio Manager

### Portfolio Copilot - Portfolio Insights & Benchmarking ✅ **READY FOR DEMO**

### Business Context Setup

**Persona**: Anna, Senior Portfolio Manager at Snowcrest Asset Management  
**Business Challenge**: Portfolio managers need instant access to portfolio analytics, holdings information, and supporting research to make informed investment decisions. Traditional systems require multiple tools, manual data gathering, and time-consuming analysis that delays critical investment decisions.  
**Value Proposition**: AI-powered portfolio analytics that combines quantitative holdings data with qualitative research insights in seconds, enabling faster decision-making and better risk management.

**Agent**: `portfolio_copilot`  
**Data Available**: 10 portfolios, 5,000 securities, 2,800 research documents

### Demo Flow

**Scene Setting**: Anna is preparing for her weekly portfolio review meeting and needs to quickly assess her Technology & Infrastructure portfolio performance, understand current holdings, and identify any emerging risks that require attention.

#### Step 1: Top Holdings Overview
**User Input**: 
```
"What are my top 10 holdings by market value in the SAM Technology & Infrastructure portfolio?"
```

**Expected Response**:
- Table showing: Ticker, Company Name, Weight %, Market Value USD
- Flag any positions >6.5% (concentration warning)
- Total exposure percentage of top 10

**Talking Points**:
- Instant portfolio analytics without SQL or complex queries
- Automatic concentration risk flagging based on business rules
- Real-time data from the data warehouse with no latency

**Key Features Highlighted**: 
- Cortex Analyst semantic understanding of portfolio data
- Business rule integration (6.5% concentration threshold)
- Natural language to SQL conversion

#### Step 2: Latest Research for Top Holdings  
**User Input**: 
```
"Based on those top holdings you just showed me, what is the latest broker research saying about our three largest positions?"
```

**Expected Response**:
- Bullet list: Company → Recent report titles with dates for the top 3 holdings from Step 1
  - [Top Holding 1]: Recent research reports with ratings and dates
  - [Top Holding 2]: Recent research reports with ratings and dates  
  - [Top Holding 3]: Recent research reports with ratings and dates
- Brief summaries of key investment themes
- Ratings distribution (Buy/Hold/Sell)
- Analysis of how research sentiment aligns with large position sizes

**Talking Points**:
- AI automatically identifies research for the specific holdings shown in Step 1
- Seamless transition from quantitative holdings data to qualitative research insights
- Risk assessment: Large positions supported by positive research sentiment

**Key Features Highlighted**: 
- Contextual follow-up that builds on previous query results
- SecurityID-based linkage between holdings and research
- Automatic citation and source attribution

#### Step 3: Sector Risk Assessment
**User Input**: 
```
"Looking at those top holdings and their research, what's our sector concentration risk in this portfolio, especially for the companies with the largest positions?"
```

**Expected Response**:
- Sector allocation breakdown highlighting the top holdings from Step 1
- Concentration analysis showing sector exposure through large positions
- Comparison to benchmark sector weights
- Risk assessment combining position size and sector concentration
- Specific flagging if top holdings create sector concentration >6.5%

**Talking Points**:
- Integrated risk analysis that combines individual position risk (Step 1) with sector risk
- Research sentiment (Step 2) now viewed through concentration lens
- Comprehensive risk picture that builds on previous analysis

**Key Features Highlighted**: 
- Multi-dimensional risk analysis building on previous queries
- Sector-level concentration assessment linked to specific holdings
- Integrated benchmark comparison with position-level context

#### Step 4: Integrated Risk & Action Plan
**User Input**: 
```
"Based on our concentration analysis and research findings, which of our largest positions need attention and what actions should we consider?"
```

**Expected Response**:
- Integrated risk assessment for the top holdings identified in Steps 1-3
- Combination of concentration risk (Step 3) and research sentiment (Step 2)
- Specific concerns for positions that are both large AND have sector concentration risk
- Prioritized action plan: positions requiring immediate attention vs monitoring
- Recommended actions with specific rationale (reduce for concentration, hold for strong research, etc.)

**Talking Points**:
- Complete investment decision framework combining all previous analysis
- Prioritized action plan based on integrated quantitative and qualitative risk assessment
- Professional portfolio management workflow from analysis to action

**Key Features Highlighted**: 
- Comprehensive decision support building on multi-step analysis
- Integration of position size, sector risk, and research sentiment
- Actionable recommendations with clear prioritization and rationale

#### Step 5: Portfolio Management Decision
**User Input**: 
```
"Based on our complete analysis from Steps 1-4, provide me with a specific implementation plan including exact position sizes, timelines, and dollar amounts for the portfolio actions we should take."
```

**Expected Response**:
- **IMMEDIATE EXECUTION (Next 3 Trading Days)**:
  - Apple: Reduce from $45.2M (8.2%) to $33.0M (6.0%) - Sell $12.2M
    * Execute via TWAP over 3 days (current ADV $180M supports $4M/day)
    * Estimated market impact: 8-12bps based on historical analysis
    * Complete before earnings blackout begins Thursday
    * Settlement provides $12.2M cash on T+2
  - Risk budget impact: Tracking error reduces from 4.8% to 4.5% (within 5% limit)

- **TAX AND LIQUIDITY ANALYSIS**:
  - Tax implications: Realizes $890K capital gain - offset with CMC position (-$340K loss)
  - Cash available: $8.1M current + $12.2M from Apple sale = $20.3M total
  - Liquidity score: Portfolio remains at 7.2/10 (high liquidity)

- **COMPLIANCE AND APPROVALS**:
  - Position change >5% requires Investment Committee approval per mandate section 4.2
  - Recommend emergency IC call Tuesday 2PM for approval
  - Technology sector allocation moves from 45% to 42% (within 35-45% range)
  - Risk budget utilization: 78% → 72% (well within 85% limit)

- **IMPLEMENTATION TIMELINE**:
  - Day 1: Obtain IC approval, initiate Apple TWAP execution ($4M)
  - Day 2: Continue Apple execution ($4M), assess tax loss harvest for CMC
  - Day 3: Complete Apple execution ($4.2M), execute CMC tax harvest if beneficial
  - Settlement: T+2 cash available for redeployment

- **MARKET CONDITIONS**:
  - Current VIX: 24 (moderate volatility - suitable for systematic execution)
  - Apple earnings: Thursday (complete sales before blackout)
  - No major option expirations during execution window

**Talking Points**:
- **Complete Investment Workflow**: From analysis to specific executable actions
- **Professional Portfolio Management**: Industry-standard implementation planning with exact specifications
- **AI-Powered Decision Support**: Comprehensive analysis translated into precise, actionable investment decisions

**Key Features Highlighted**: 
- **End-to-End Investment Process**: Complete workflow from analysis to implementation
- **Specific Action Planning**: Exact dollar amounts, percentages, and timelines
- **Professional Investment Management**: Industry-standard decision framework with comprehensive risk management

### Scenario Wrap-up

**Business Impact Summary**:
- **Time Savings**: Reduced portfolio analysis time from hours to minutes
- **Risk Management**: Proactive identification of emerging risks and concentration issues
- **Decision Quality**: Enhanced decision-making through integrated quantitative and qualitative insights
- **Operational Efficiency**: Single interface replacing multiple legacy systems and manual processes

**Technical Differentiators**:
- **Semantic Understanding**: Natural language queries automatically converted to complex SQL
- **Real-time Integration**: Live data warehouse connectivity with no batch processing delays
- **AI-Powered Search**: Intelligent document search with automatic relevance ranking and summarization
- **Multi-modal Analysis**: Seamless combination of structured portfolio data with unstructured research content

## Demo Execution Guidelines

### Pre-Demo Checklist
- [ ] Run `python main.py --scenarios portfolio_copilot` successfully
- [ ] Verify semantic view: `DESCRIBE SEMANTIC VIEW SAM_DEMO.AI.SAM_ANALYST_VIEW`
- [ ] Test search services: Use `SNOWFLAKE.CORTEX.SEARCH_PREVIEW()` on each service
- [ ] Configure `portfolio_copilot` agent in Snowflake Intelligence
- [ ] Test agent with validation queries

### Demo Flow Best Practices
1. **Start Simple**: Begin with Step 1 (top holdings) to show basic functionality
2. **Show Integration**: Emphasize how Steps 1→2 flow from quantitative to qualitative
3. **Highlight AI**: Point out document search and automatic citations in Step 2
4. **Show Complexity**: Step 3 demonstrates multi-table benchmark analysis
5. **End with Value**: Step 4 shows proactive risk monitoring

### Current Data Highlights
- **Realistic Portfolios**: SAM Technology & Infrastructure ($90B), SAM ESG Leaders ($108B), SAM Flagship ($150B)
- **Real Tickers**: AAPL, MSFT, NVDA, GOOGL, etc. with proper sector classifications
- **Generated Research**: 1,200 broker reports, 800 earnings transcripts, 800 press releases
- **UK English**: All content generated in professional UK English

### Success Metrics
- ✅ **Speed**: Instant responses to complex portfolio queries
- ✅ **Integration**: Seamless combination of structured and unstructured data
- ✅ **Citations**: Proper source attribution for all document references
- ✅ **Realism**: Authentic-looking financial data and research content

### Thematic Macro Advisor - Investment Theme Analysis ✅ **READY FOR DEMO**

#### Business Context Setup

**Persona**: Anna, Portfolio Manager (Thematic Focus) at Snowcrest Asset Management  
**Business Challenge**: Portfolio managers need to identify and validate investment opportunities across macro trends by combining quantitative portfolio analysis with thematic research. Traditional approaches struggle to connect portfolio positioning with emerging themes and market trends effectively.  
**Value Proposition**: AI-powered thematic analysis that combines current portfolio positioning with comprehensive research synthesis to identify theme-based investment opportunities and optimize strategic allocation decisions.

**Agent**: `thematic_macro_advisor`  
**Data Available**: Portfolio holdings data + 100 broker reports, 75 press releases, 75 earnings transcripts

*[Complete scenario details moved from original Scenario 3 location...]*

---

## Research Analyst

### Research Copilot - Document Research & Analysis ✅ **READY FOR DEMO**

### Business Context Setup

**Persona**: David, Research Analyst at Snowcrest Asset Management  
**Business Challenge**: Research analysts need to combine quantitative financial analysis with qualitative research synthesis across multiple sources (financial data, broker research, earnings calls, press releases) to build comprehensive investment cases. Manual analysis requires hours of data gathering, financial modeling, and document review, often missing critical connections between financial performance and strategic narratives.  
**Value Proposition**: AI-powered research intelligence that seamlessly combines structured financial analysis with unstructured document insights, enabling analysts to build complete investment theses faster and with greater depth than traditional approaches.

**Agent**: `research_copilot`  
**Data Available**: Financial fundamentals & estimates for 14,000+ securities + 100 broker reports, 75 earnings transcripts, 75 press releases

### Demo Flow

**Scene Setting**: David is preparing a thematic research report on technology sector opportunities and needs to quickly synthesize insights from multiple document sources to identify emerging trends and validate investment themes.

#### Step 1: Multi-Source Research Synthesis
**User Input**: 
```
"What is the latest research saying about AI and cloud computing opportunities in technology companies?"
```

**Expected Response**:
- AI and cloud computing investment themes from broker research (featuring Microsoft, Amazon, Google)
- Management commentary on AI strategy and cloud growth from earnings transcripts
- Corporate AI and cloud developments from press releases
- Synthesized technology sector opportunities with proper citations

**Talking Points**:
- AI automatically searches across multiple document types simultaneously for specific themes
- Intelligent synthesis of AI and cloud computing insights from different source perspectives
- Thematic focus ensures relevant results for technology sector analysis

**Key Features Highlighted**: 
- Multi-source Cortex Search integration
- Intelligent document synthesis and summarization
- Automatic source attribution and citation

#### Step 2: Deep-Dive Company Analysis
**User Input**: 
```
"From those companies mentioned in the AI and cloud research, pick the one with the strongest themes and give me a detailed analysis of their recent performance and strategic positioning"
```

**Expected Response**:
- **Company Selection Rationale**: Why this company was chosen based on Step 1 research themes
- **Financial Performance Metrics**: Revenue trends, EPS progression, analyst estimates vs. actuals
- **Earnings Analysis**: Quarterly performance, earnings surprises, financial ratios
- **Management Commentary**: Strategic positioning and forward guidance from earnings calls that align with Step 1 themes
- **Analyst Perspectives**: Research opinions and price targets that connect to AI/cloud opportunities from Step 1
- **Corporate Developments**: Recent strategic announcements that support the themes identified in Step 1
- **Comprehensive Synthesis**: Integration of quantitative performance with the specific qualitative themes from Step 1

**Talking Points**:
- **Contextual Company Selection**: AI automatically identifies the most relevant company from Step 1 research
- **Theme Continuity**: Deep-dive analysis directly builds on the AI/cloud themes from previous research
- **Integrated Intelligence**: Financial analysis validates the qualitative themes identified in Step 1

**Key Features Highlighted**: 
- **Contextual Follow-up**: Automatically selects relevant company based on Step 1 findings
- **Theme-Based Analysis**: Deep-dive specifically addresses themes identified in previous step
- **Integrated Validation**: Financial performance data supports or challenges qualitative research themes

#### Step 3: Competitive Intelligence Gathering
**User Input**: 
```
"How does [the company from Step 2]'s AI strategy compare to what other technology companies mentioned in Step 1 are doing?"
```

**Expected Response**:
- Comparative analysis of AI strategies across the specific companies identified in Steps 1-2
- Management commentary on competitive positioning from earnings calls of the Step 1 companies
- Strategic announcements and partnerships from press releases that connect the Step 1 themes
- Competitive landscape analysis focused on the AI/cloud opportunities from Step 1
- Direct comparison showing how the Step 2 company stacks against Step 1 competitors

**Talking Points**:
- **Building Competitive Context**: Uses the specific companies and themes from previous steps
- **Focused Comparison**: Avoids generic analysis by focusing on the companies already identified
- **Strategic Investment Framework**: Builds a complete competitive picture for investment decision-making

**Key Features Highlighted**: 
- **Multi-Step Intelligence**: Integrates findings from Steps 1 and 2 for focused competitive analysis
- **Theme-Based Comparison**: Competitive analysis specifically addresses AI/cloud themes from Step 1
- **Investment Decision Support**: Provides comparative context needed for investment decisions

#### Step 4: Investment Thesis Validation
**User Input**: 
```
"Based on our analysis of [Step 2 company] and its competitive position, compare what management is saying about AI growth prospects versus what analysts are forecasting for this investment opportunity"
```

**Expected Response**:
- Management outlook and guidance from earnings transcripts specific to the Step 2 company
- Analyst forecasts and price targets from broker research that connect to Step 1 AI/cloud themes
- Strategic initiatives and investments from press releases that support the competitive analysis from Step 3
- Identification of consensus views and potential disconnects specifically for the investment case built in Steps 1-3
- Final investment thesis validation that ties together all previous analysis

**Talking Points**:
- **Complete Investment Case**: Validates the entire research workflow from themes to company to competition
- **Consensus Analysis**: Identifies alignment or disagreement between management and analysts for the specific opportunity
- **Investment Decision Ready**: Provides final validation needed for investment committee presentation

**Key Features Highlighted**: 
- **Multi-Step Synthesis**: Integrates themes (Step 1), company analysis (Step 2), and competitive position (Step 3)
- **Investment Thesis Validation**: Tests the strength of the complete investment case built through previous steps
- **Decision Support**: Provides final consensus analysis needed for investment decisions

### Scenario Wrap-up

**Business Impact Summary**:
- **Research Efficiency**: Reduced comprehensive company analysis time from days to minutes
- **Analysis Completeness**: Seamless integration of quantitative financial data with qualitative research insights
- **Investment Thesis Quality**: Enhanced ability to build complete investment cases with both numbers and narrative
- **Competitive Intelligence**: Faster identification of financial performance trends and strategic positioning

**Technical Differentiators**:
- **Hybrid Analytics Platform**: Seamless combination of Cortex Analyst (structured data) and Cortex Search (documents)
- **Comprehensive Data Integration**: Financial fundamentals, estimates, and earnings data combined with research documents
- **Intelligent Financial Analysis**: Automated calculation of earnings surprises, trend analysis, and ratio comparisons
- **Multi-Source Research Synthesis**: Unified analysis across financial data, management commentary, and analyst research

### Pre-Demo Checklist
- [ ] Run `python main.py --scenarios research_copilot` successfully
- [ ] Verify semantic view: `DESCRIBE SEMANTIC VIEW SAM_DEMO.AI.SAM_RESEARCH_VIEW`
- [ ] Test search services: Use `SNOWFLAKE.CORTEX.SEARCH_PREVIEW()` on broker research and earnings services
- [ ] Configure `research_copilot` agent in Snowflake Intelligence with `financial_analyzer` + 3 search tools
- [ ] Test agent with validation queries combining financial analysis and document search

### Demo Flow Best Practices
1. **Start with Earnings**: Begin with Step 1 to show financial analysis capabilities
2. **Show Time Series**: Use Step 2 to demonstrate longitudinal analysis
3. **Visualize Data**: Step 3 highlights chart generation from financial data
4. **Competitive Intelligence**: Step 4 shows sector-wide analysis capabilities

### Research Copilot - Earnings Intelligence Extensions ✅ **READY FOR DEMO**

### Business Context Setup

**Persona**: Sarah, Senior Research Analyst at Snowcrest Asset Management  
**Business Challenge**: Research analysts need to rapidly analyze quarterly earnings releases, integrate financial data with management commentary, and identify sentiment shifts that could signal investment opportunities or risks. Traditional earnings analysis requires hours of manual transcription, data extraction, and cross-referencing across multiple documents, often missing subtle but critical sentiment changes.  
**Value Proposition**: AI-powered earnings intelligence that automatically processes financial filings, earnings call transcripts, and press releases to provide instant financial analysis combined with sentiment insights, enabling analysts to detect emerging trends and risks within minutes of earnings releases.

**Agent**: `research_copilot`  
**Data Available**: SEC filings for 14,000+ securities, earnings transcripts, press releases, financial fundamentals

### Demo Flow

**Scene Setting**: Sarah is analyzing the latest quarterly earnings for a major technology holding and needs to quickly assess the financial performance, understand management sentiment, and identify any shifts in forward guidance that could impact the investment thesis.

#### Step 1: Integrated Earnings Analysis
**User Input**: 
```
"Give me a comprehensive analysis of Microsoft's latest quarterly earnings, including reported financial metrics versus consensus estimates and key management commentary from the earnings call."
```

**Expected Response**:
- **Financial Performance**: Reported revenue, net income, and EPS vs. analyst consensus estimates from SEC filings
- **Key Metrics Analysis**: Margin trends, growth rates, and segment performance from FACT_SEC_FILINGS
- **Management Commentary**: Key quotes and themes from earnings transcript regarding future outlook
- **Guidance Updates**: Forward-looking statements and any revisions to company guidance
- **Document Sources**: Citations from SEC filings, earnings transcript, and press releases

**Talking Points**:
- Instant integration of structured financial data with unstructured earnings commentary
- Automatic comparison of reported results against consensus estimates
- AI-powered extraction of key management insights from lengthy earnings calls

**Key Features Highlighted**: 
- SEC filings integration providing authentic financial data (28.7M records)
- Multi-document synthesis combining quantitative and qualitative analysis
- Real-time financial analysis with management commentary context

#### Step 2: Sentiment Analysis and Red Flags
**User Input**: 
```
"Compare the sentiment between Microsoft's prepared remarks and the Q&A session. Are there any concerning shifts or defensive language that could indicate management uncertainty?"
```

**Expected Response**:
- **Sentiment Comparison**: Quantified sentiment scores for prepared remarks vs. Q&A session
- **Tone Analysis**: Description of management confidence levels and any defensive language
- **Key Questions**: Specific analyst questions that triggered defensive responses
- **Risk Indicators**: Areas where management showed uncertainty or provided evasive answers
- **Comparative Context**: How this sentiment compares to previous quarters

**Talking Points**:
- AI quantifies subjective "gut feelings" about earnings call tone into measurable data
- Sentiment delta between prepared remarks and Q&A often reveals management confidence levels
- Early warning system for detecting management pressure before it shows in financial results

**Key Features Highlighted**: 
- Advanced sentiment analysis turning qualitative assessments into quantitative signals
- Comparative analysis across different sections of earnings calls
- Predictive insights from management tone and language patterns

#### Step 3: Strategic Commentary Evolution
**User Input**: 
```
"How has Microsoft's commentary on cloud computing and AI strategy evolved over the past three quarters? Are there any shifts in their strategic messaging or capital allocation priorities?"
```

**Expected Response**:
- **Strategic Theme Evolution**: Changes in management emphasis on cloud computing and AI initiatives
- **Investment Priorities**: Shifts in capital expenditure focus and R&D allocation
- **Competitive Positioning**: How Microsoft's messaging has evolved relative to market dynamics
- **Forward Guidance**: Changes in growth expectations for cloud and AI segments
- **Historical Context**: Comparison with previous quarters' strategic commentary

**Talking Points**:
- Historical analysis reveals strategic shifts that may not be apparent in single-quarter analysis
- AI tracks consistency in management messaging and identifies strategic pivots
- Long-term strategic evolution analysis supports investment thesis development

**Key Features Highlighted**: 
- Multi-quarter analysis tracking strategic narrative evolution
- Cross-document intelligence linking financial data with strategic commentary
- Historical context providing deeper investment insights

#### Step 4: Investment Committee Summary
**User Input**: 
```
"Draft a concise investment committee memo summarizing Microsoft's earnings results, highlighting the key financial metrics, sentiment analysis findings, and any strategic shifts that impact our investment thesis."
```

**Expected Response**:
- **Executive Summary**: Key financial highlights and performance vs. expectations
- **Sentiment Assessment**: Summary of management confidence and any concerning shifts
- **Strategic Updates**: Notable changes in cloud/AI strategy and capital allocation
- **Investment Implications**: How findings support or challenge current investment thesis
- **Action Items**: Recommended follow-up analysis or portfolio actions
- **Supporting Data**: References to specific SEC filing metrics and transcript quotes

**Talking Points**:
- Automated synthesis of complex earnings analysis into executive-ready format
- Integration of quantitative financial analysis with qualitative sentiment insights
- Professional documentation supporting investment decision-making process

**Key Features Highlighted**: 
- Comprehensive report generation combining multiple data sources and analytical perspectives
- Professional formatting suitable for investment committee review
- Complete audit trail with source citations for compliance and verification

### Scenario Wrap-up

**Business Impact Summary**:
- **Speed Enhancement**: Earnings analysis reduced from hours to minutes, enabling faster decision-making
- **Analytical Depth**: Combined quantitative and qualitative analysis provides comprehensive investment insights
- **Risk Detection**: Sentiment analysis creates early warning system for management confidence shifts
- **Strategic Intelligence**: Multi-quarter analysis reveals strategic evolution and competitive positioning changes

**Technical Differentiators**:
- **Authentic Data Integration**: Real SEC filings (28.7M records) provide institutional-grade financial analysis
- **Multi-Modal Intelligence**: Seamless combination of structured financial data with unstructured earnings commentary
- **Predictive Sentiment Analysis**: Quantified sentiment scoring creates measurable signals from qualitative management tone
- **Historical Context Engine**: Multi-quarter strategic analysis reveals long-term trends and strategic pivots

---

## Quantitative Analyst

### Quant Analyst - Factor Analysis & Performance Attribution ✅ **READY FOR DEMO**

*[This section will be moved later - placeholder for now]*

---

## Client Relations  

### Sales Advisor - Client Reporting & Template Formatting ✅ **READY FOR DEMO**

*[This section will be moved later - placeholder for now]*

---

## Risk & Compliance Officer

### ESG Guardian - ESG Risk Monitoring & Policy Compliance 🔄 **READY FOR IMPLEMENTATION**

*[This section will be moved later - placeholder for now]*

### Compliance Advisor - Mandate Monitoring & Breach Detection 🔄 **READY FOR IMPLEMENTATION**

*[This section will be moved later - placeholder for now]*

### Business Context Setup

**Persona**: Anna, Portfolio Manager (Thematic Focus) at Snowcrest Asset Management  
**Business Challenge**: Portfolio managers need to identify and validate investment opportunities across macro trends by combining quantitative portfolio analysis with thematic research. Traditional approaches struggle to connect portfolio positioning with emerging themes and market trends effectively.  
**Value Proposition**: AI-powered thematic analysis that combines current portfolio positioning with comprehensive research synthesis to identify theme-based investment opportunities and optimize strategic allocation decisions.

**Agent**: `thematic_macro_advisor`  
**Data Available**: Portfolio holdings data + 100 broker reports, 75 press releases, 75 earnings transcripts

### Demo Flow

**Scene Setting**: Anna is developing the quarterly thematic investment strategy and needs to assess current portfolio positioning against emerging macro trends, identify new thematic opportunities, and optimize portfolio allocation for maximum theme exposure.

#### Step 1: Current Thematic Positioning
**User Input**: 
```
"Analyze our current exposure to AI and technology themes across portfolios"
```

**Expected Response**:
- Technology sector allocation by portfolio
- AI-related company holdings and weights
- Thematic concentration analysis
- Benchmark comparison where available

**Talking Points**:
- Quantitative analysis of current thematic positioning across all portfolios
- Identification of theme concentration and diversification opportunities
- Benchmark comparison to assess relative thematic positioning

**Key Features Highlighted**: 
- Cross-portfolio thematic exposure analysis
- Sector and theme-based portfolio analytics
- Benchmark comparison and relative positioning

#### Step 2: Thematic Research Discovery  
**User Input**: 
```
"Based on our current AI and technology exposure from Step 1, what are the emerging thematic investment opportunities that could enhance our positioning?"
```

**Expected Response**:
- Emerging investment themes from broker research that complement current AI/tech holdings
- Corporate strategic initiatives from press releases in areas where we have limited exposure
- Management outlook on themes from earnings calls that extend our current positioning
- Synthesis of macro trends that build on our existing AI/technology exposure from Step 1
- Gap analysis: themes where we could increase exposure vs themes where we're already well-positioned

**Talking Points**:
- **Strategic Theme Extension**: Identifies opportunities that build on current portfolio positioning
- **Portfolio Gap Analysis**: Highlights thematic opportunities where current exposure is limited
- **Complementary Trends**: Discovers themes that enhance rather than duplicate existing positioning

**Key Features Highlighted**: 
- **Portfolio-Contextual Research**: Theme discovery specifically informed by current positioning
- **Strategic Enhancement**: Identifies themes that extend and complement existing exposures
- **Gap-Based Opportunity Identification**: Focuses on themes where portfolio could be enhanced

#### Step 3: Strategic Positioning Analysis
**User Input**: 
```
"From the emerging themes identified in Step 2, pick the most promising one and analyze how we should position our portfolios, considering our current AI/tech exposure from Step 1"
```

**Expected Response**:
- Selection rationale: why this theme was chosen from Step 2 opportunities
- Current portfolio exposure analysis for the selected theme (building on Step 1 foundation)
- Research validation for the selected theme from Step 2 findings
- Strategic positioning recommendations that complement existing AI/tech holdings
- Portfolio optimization suggestions: specific actions to increase exposure to the selected theme
- Integration analysis: how the new theme positioning works with existing AI/tech exposure

**Talking Points**:
- **Theme Selection Logic**: AI selects the most promising theme from Step 2 based on portfolio context
- **Integrated Positioning Strategy**: Recommendations consider both current positioning and new opportunities
- **Portfolio Optimization**: Specific actions that build on existing strengths while adding new themes

**Key Features Highlighted**: 
- **Multi-Step Strategy Development**: Integrates current positioning (Step 1) with emerging opportunities (Step 2)
- **Contextual Theme Selection**: Chooses optimal theme based on portfolio positioning and research strength
- **Integrated Investment Strategy**: Develops positioning that enhances rather than conflicts with existing exposures

#### Step 4: Integrated Investment Strategy
**User Input**: 
```
"Based on our AI/tech positioning from Step 1 and the [selected theme from Step 3], create an integrated investment strategy that optimizes our thematic exposure across portfolios"
```

**Expected Response**:
- Integrated strategy that combines AI/tech exposure (Step 1) with selected theme (Step 3)
- Cross-theme intersection analysis: companies that fit both themes
- Portfolio allocation recommendations for optimal thematic balance
- Research validation from Step 2 that supports the integrated approach
- Implementation roadmap with specific actions for each portfolio
- Risk assessment: concentration and diversification considerations for the integrated theme strategy

**Talking Points**:
- **Complete Thematic Integration**: Develops unified strategy across multiple themes and portfolios
- **Cross-Theme Optimization**: Identifies companies and sectors that provide exposure to multiple themes
- **Implementation Ready**: Provides specific portfolio actions and allocation recommendations

**Key Features Highlighted**: 
- **Multi-Step Strategy Synthesis**: Integrates analysis from all previous steps into comprehensive strategy
- **Cross-Portfolio Optimization**: Develops theme allocation strategy across all portfolios
- **Implementation Framework**: Provides actionable roadmap for thematic investment strategy

### Scenario Wrap-up

**Business Impact Summary**:
- **Strategic Positioning**: Enhanced ability to position portfolios for emerging macro trends
- **Theme Identification**: Faster discovery of new investment themes and opportunities
- **Portfolio Optimization**: Data-driven recommendations for thematic allocation optimization
- **Competitive Advantage**: Earlier identification of thematic convergence and intersection opportunities

**Technical Differentiators**:
- **Thematic Intelligence**: AI-powered identification of emerging investment themes from research
- **Cross-Portfolio Analysis**: Comprehensive thematic positioning analysis across multiple portfolios
- **Multi-Theme Intersection**: Advanced analysis of theme convergence and overlap opportunities
- **Strategic Integration**: Seamless combination of quantitative positioning with qualitative thematic research

