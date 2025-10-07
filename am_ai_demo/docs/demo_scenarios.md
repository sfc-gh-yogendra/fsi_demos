# SAM Demo - Scenario Scripts

Reference: See `docs/implementation_plan.md` for the build order and implementation details referenced by these scenarios.

Complete demo scenarios organized by role and agent, with step-by-step conversations, expected responses, and data flows.

## Available Scenarios by Role

### Portfolio Manager
**Agent: Portfolio Copilot**
- Portfolio Insights & Benchmarking ✅ **IMPLEMENTED**
- Real-Time Event Impact & Second-Order Risk Verification ✅ **IMPLEMENTED**
- AI-Assisted Mandate Compliance & Security Replacement ✅ **IMPLEMENTED**

**Agent: Thematic Macro Advisor**  
- Investment Theme Analysis ✅ **IMPLEMENTED**

### Research Analyst
**Agent: Research Copilot**
- Document Research & Analysis ✅ **IMPLEMENTED**
- Earnings Intelligence Extensions ✅ **IMPLEMENTED**

### Quantitative Analyst
**Agent: Quant Analyst**
- Factor Analysis & Performance Attribution ✅ **IMPLEMENTED**

### Client Relations
**Agent: Sales Advisor**
- Client Reporting & Template Formatting ✅ **IMPLEMENTED**

### Risk & Compliance Officer
**Agent: ESG Guardian**
- ESG Risk Monitoring & Policy Compliance ✅ **IMPLEMENTED**

**Agent: Compliance Advisor**
- Mandate Monitoring & Breach Detection ✅ **IMPLEMENTED**

---

## Portfolio Manager

### Portfolio Copilot - Portfolio Insights & Benchmarking

#### Business Context Setup

**Persona**: Anna, Senior Portfolio Manager at Snowcrest Asset Management  
**Business Challenge**: Portfolio managers need instant access to portfolio analytics, holdings information, and supporting research to make informed investment decisions. Traditional systems require multiple tools, manual data gathering, and time-consuming analysis that delays critical investment decisions.  
**Value Proposition**: AI-powered portfolio analytics that combines quantitative holdings data with qualitative research insights in seconds, enabling faster decision-making and better risk management.

**Agent**: `portfolio_copilot`  
**Data Available**: 10 portfolios, 5,000 securities, 2,800 research documents

#### Demo Flow

**Scene Setting**: Anna is preparing for her weekly portfolio review meeting and needs to quickly assess her Technology & Infrastructure portfolio performance, understand current holdings, and identify any emerging risks that require attention.

##### Step 1: Top Holdings Overview
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

##### Step 2: Latest Research for Top Holdings  
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

##### Step 3: Sector Risk Assessment
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

##### Step 4: Integrated Risk & Action Plan
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

##### Step 5: Portfolio Management Decision
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

#### Scenario Wrap-up

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

---

### Portfolio Copilot - Real-Time Event Impact & Second-Order Risk Verification

#### Business Context Setup

**Persona**: Anna, Senior Portfolio Manager at Snowcrest Asset Management  
**Business Challenge**: Portfolio managers need to rapidly assess portfolio exposure when external events occur, including both direct regional/sector exposure and indirect supply chain dependencies. Traditional risk systems can't model multi-hop supply chain relationships or quantify second-order impacts, leaving managers blind to cascading risks.  
**Value Proposition**: AI-powered event risk verification that combines macro event intelligence, direct portfolio exposure analysis, and sophisticated supply chain dependency mapping to quantify both immediate and indirect portfolio impacts in real-time.

**Agent**: `portfolio_copilot`  
**Data Available**: 10 portfolios, supply chain relationships (150+ dependencies), macro events corpus, press releases

#### Demo Flow

**Scene Setting**: Anna receives an external market alert about a major earthquake in Taiwan affecting semiconductor production. She needs to immediately understand her portfolio's exposure - both direct holdings in affected companies and indirect exposure through supply chain dependencies.

##### Step 1: Event Verification
**User Input**: 
```
"I just received an alert about a major earthquake in Taiwan affecting semiconductor production. Can you verify this event and tell me what sectors are affected?"
```

**Expected Response**:
- Event confirmation from macro events database:
  * Event Type: Natural Disaster
  * Region: Taiwan (TW)
  * Severity: Critical
  * Event Date: [Current date]
- Affected sectors identified:
  * Information Technology (primary impact)
  * Consumer Discretionary (secondary impact via automotive)
- Brief impact description:
  * TSMC facilities affected (40-50% of global advanced chip capacity)
  * Expected production halt: 2-4 weeks
  * Recovery timeline: 6-8 weeks for full supply chain normalization

**Talking Points**:
- AI verifies external alerts using structured macro event database
- Extracts precise event characteristics (type, region, severity, sectors)
- Provides authoritative event context for risk assessment

**Key Features Highlighted**: 
- Macro event intelligence repository
- Structured event data with standardized attributes
- Event verification before portfolio impact analysis

##### Step 2: Direct Portfolio Exposure
**User Input**: 
```
"What is my direct exposure to Taiwan-based semiconductor companies across all portfolios?"
```

**Expected Response**:
- Table showing direct Taiwan semiconductor exposure by portfolio:
  * Portfolio Name | Taiwan Semiconductor Exposure (USD) | % of Portfolio | Key Holdings (TSM, etc.)
  * Flag portfolios with >2% exposure to Taiwan semiconductor sector
- Total Taiwan semiconductor exposure across all portfolios
- Specific companies held:
  * Taiwan Semiconductor Manufacturing (TSM) - if held
  * ASE Technology Holding, ChipMOS Technologies, Himax Technologies, etc.
- Regional exposure breakdown: Taiwan % of total portfolio

**Talking Points**:
- Immediate quantification of direct regional exposure
- Portfolio-level impact assessment
- Specific holdings identified for monitoring

**Key Features Highlighted**: 
- Multi-dimensional filtering (country + sector)
- Cross-portfolio exposure aggregation
- Automatic threshold-based flagging

##### Step 3: Second-Order Supply Chain Exposure
**User Input**: 
```
"What is my indirect exposure through supply chain dependencies? Show me which US companies in my portfolio depend on Taiwan semiconductor suppliers."
```

**Expected Response**:
- Multi-hop supply chain analysis with decay factors:
  * **First-Order Dependencies** (Direct customers of Taiwan semis):
    - NVIDIA: 25% revenue dependency on TSM (High) → Portfolio exposure: [weight]%
    - AMD: 18% revenue dependency on TSM (High) → Portfolio exposure: [weight]%
    - Apple: 30% revenue dependency on TSM (High) → Portfolio exposure: [weight]%
  * **Second-Order Dependencies** (50% decay applied):
    - General Motors: 8% chip dependency on NVIDIA (Medium) → Effective exposure: 4% post-decay
    - Ford: 6% chip dependency on NVIDIA (Medium) → Effective exposure: 3% post-decay
- Summary table:
  * Company | Relationship Type | Dependency % | Post-Decay Exposure | Portfolio Weight | Risk Rating
- Total indirect exposure calculation (weighted by portfolio holdings)
- Flag High dependency relationships (≥20% post-decay)

**Talking Points**:
- **Multi-Hop Analysis**: AI traverses supply chain graph to identify indirect dependencies
- **Decay Factors**: 50% decay per hop reflects diminishing impact through supply chain
- **Criticality Assessment**: Automatic flagging of high-dependency relationships
- **Portfolio Weighting**: Second-order exposure weighted by actual portfolio holdings

**Key Features Highlighted**: 
- Supply chain graph traversal with configurable depth
- Decay factor application for realistic impact modeling
- Upstream (cost) and downstream (revenue) relationship analysis
- Portfolio-weighted exposure calculation

##### Step 4: Corroborating Evidence & Next Steps
**User Input**: 
```
"Do we have any recent press releases or company statements from NVIDIA or AMD about their Taiwan supply chain?"
```

**Expected Response**:
- Press release search results:
  * NVIDIA - "Q4 2024 Earnings Call: Taiwan Fab Partnership Update" (Jan 2024)
    - Confirms TSMC as primary manufacturing partner
    - Mentions geographic diversification plans (2025 timeline)
  * AMD - "Supply Chain Update" (Dec 2023)
    - TSMC accounts for majority of advanced node production
    - Alternative sourcing being explored but limited near-term options
- Synthesis and recommendations:
  * **Direct Exposure**: [X]% total exposure to Taiwan IT sector
  * **Indirect Exposure**: [Y]% effective exposure through supply chain (post-decay)
  * **Total Risk**: [X+Y]% combined exposure to Taiwan semiconductor disruption
  * **Recommended Actions**:
    1. Monitor: Track TSMC facility restoration updates
    2. Engage: Contact NVIDIA/AMD investor relations for supply impact guidance
    3. Assess: Review positions for potential trim if exposure exceeds risk budget
    4. Hedge: Consider short-term hedging strategies if event extends beyond 4 weeks

**Talking Points**:
- **Document Corroboration**: AI finds supporting evidence from corporate communications
- **Comprehensive Risk View**: Direct + indirect exposure quantified
- **Actionable Recommendations**: Specific next steps based on total exposure
- **Risk Management Framework**: Monitoring, engagement, and hedging strategies

**Key Features Highlighted**: 
- Multi-source intelligence synthesis (portfolio data + supply chain + press releases)
- Total risk calculation combining direct and indirect exposures
- Professional risk management framework with specific actions
- Timeline-based response recommendations

#### Scenario Wrap-up

**Business Impact Summary**:
- **Rapid Event Response**: Assess portfolio impact within minutes vs hours/days with traditional systems
- **Hidden Risk Discovery**: Quantify indirect supply chain exposures that traditional systems miss
- **Comprehensive Risk View**: Combine direct holdings with multi-hop supply chain dependencies
- **Actionable Intelligence**: Specific recommendations with timelines and thresholds

**Technical Differentiators**:
- **Graph Database Analytics**: Multi-hop supply chain traversal with decay factors and criticality scoring
- **Event Intelligence Repository**: Structured macro event database with standardized attributes
- **Real-Time Risk Quantification**: Instant calculation of portfolio-weighted supply chain exposures
- **Multi-Modal Intelligence**: Seamless integration of event data, portfolio holdings, supply chain graphs, and corporate communications

---

### Portfolio Copilot - AI-Assisted Mandate Compliance & Security Replacement

#### Business Context Setup

**Persona**: David Chen, Senior Portfolio Manager at Snowcrest Asset Management  
**Business Challenge**: Portfolio managers must respond quickly to mandate compliance breaches (e.g., ESG downgrades) by identifying suitable replacement securities that maintain portfolio strategy while meeting compliance requirements. Traditional processes involve manual screening, multiple system lookups, and time-consuming committee documentation.  
**Value Proposition**: AI-powered compliance workflow that automatically identifies pre-screened replacement candidates, analyzes their strategic fit, and generates investment committee documentation—reducing breach response time from days to minutes.

**Agent**: `portfolio_copilot`  
**Data Available**: SAM AI & Digital Innovation portfolio, compliance alerts, pre-screened replacements, ESG data, financial filings, broker research

#### Demo Flow

**Scene Setting**: David receives a compliance alert that META has been downgraded to ESG grade D due to governance concerns, violating the SAM AI & Digital Innovation fund's minimum BBB ESG requirement. He needs to identify a suitable replacement that maintains the portfolio's AI/digital innovation focus while meeting all mandate requirements, then document his recommendation for the investment committee.

##### Step 1: Verify Compliance Breach
**User Input**: 
```
"I've received an alert that META has been downgraded to ESG grade D. Can you verify this breach for the SAM AI & Digital Innovation portfolio and show me our current exposure?"
```

**Expected Response**:
- Confirmation of META's ESG downgrade from BBB to D
- Current portfolio exposure to META (weight %, market value)
- Mandate requirement: Minimum ESG grade BBB
- Breach severity: Critical (grade D vs required BBB)
- Recommendation: Identify replacement security

**Talking Points**:
- Instant compliance verification using mandate_compliance_analyzer
- Clear identification of mandate breach with specific thresholds
- Portfolio-specific exposure analysis for impact assessment

**Key Features Highlighted**: 
- Cortex Analyst for compliance rule checking
- Real-time ESG data integration
- Portfolio-specific mandate requirements

##### Step 2: Identify Pre-Screened Replacement Candidates
**User Input**: 
```
"Based on that breach, what are our pre-screened replacement candidates that meet the mandate requirements and maintain our AI growth focus?"
```

**Expected Response**:
- Table of pre-screened candidates (NVDA, MSFT, GOOGL):
  - Ticker, Company Name
  - AI Growth Score (0-10 scale)
  - ESG Grade (A/BBB/B)
  - Current portfolio weight
  - Strategic fit rationale
- Ranking by AI Growth Score
- ESG compliance status (all meet BBB+ requirement)

**Talking Points**:
- Pre-screened candidates ensure compliance and strategic fit
- AI Growth Score quantifies alignment with portfolio theme
- Multiple options provide flexibility for committee decision

**Key Features Highlighted**: 
- Mandate-aware candidate identification
- Thematic scoring (AI Growth Score)
- Portfolio positioning context

##### Step 3: Analyze Top Replacement Candidate
**User Input**: 
```
"Give me a comprehensive analysis of NVDA as a replacement—include financial health, recent analyst views, and earnings guidance"
```

**Expected Response**:
- **Financial Health** (from SEC filings):
  - Revenue growth trends, profit margins, cash flow strength
  - Debt-to-equity ratio, balance sheet quality
- **Analyst Views** (from broker research):
  - Recent rating: Buy/Outperform
  - Price targets and investment thesis
  - AI/semiconductor growth outlook
- **Earnings Guidance** (from transcripts):
  - Recent quarter performance
  - Management guidance on AI demand
  - Forward-looking statements

**Talking Points**:
- Multi-source analysis combining structured and unstructured data
- Authentic SEC filing data for fundamental analysis
- Real broker research and earnings commentary for market context

**Key Features Highlighted**: 
- SAM_SEC_FILINGS_VIEW for financial analysis
- Cortex Search across multiple document types
- Integrated quantitative + qualitative insights

##### Step 4: Generate Investment Committee Report
**User Input**: 
```
"Generate an investment committee memo documenting this compliance breach and recommending NVDA as a replacement"
```

**Expected Response**:
- Confirmation: "I've generated your investment committee memo. Synthesizing from template guidance..."
- Report includes:
  - **Executive Summary**: Clear recommendation to replace META with NVDA
  - **Breach Details**: ESG downgrade specifics and mandate violation
  - **Replacement Analysis**: 
    * NVDA's AI Growth Score (9/10) vs META (8/10)
    * ESG compliance (A grade vs required BBB)
    * Financial strength metrics
    * Analyst support and market positioning
  - **Risk Assessment**: Implementation risks and monitoring requirements
  - **Appendices**: Supporting data tables and research citations
- PDF file path: `@SAM_REPORTS_STAGE/SAM_AI_Digital_Innovation_META_Replacement_YYYYMMDD_HHMMSS.pdf`

**Talking Points**:
- Automated report generation following firm templates
- Comprehensive documentation for audit trail
- Professional PDF output ready for committee review
- Entire workflow completed in minutes vs days

**Key Features Highlighted**: 
- Template-guided report synthesis
- Custom Python stored procedure for PDF generation
- Snowflake stage for secure report storage
- Complete audit trail from alert to documentation

#### Scenario Wrap-up

**Business Impact Summary**:
- **Response Time**: Compliance breach resolution from days to minutes
- **Risk Mitigation**: Immediate identification of compliant alternatives
- **Decision Quality**: Multi-source analysis (financial + research + ESG)
- **Audit Trail**: Automated committee documentation with full lineage

**Technical Differentiators**:
- **Mandate-Aware AI**: Compliance rules integrated into agent planning
- **Multi-View Analytics**: Combines SAM_ANALYST_VIEW, SAM_SEC_FILINGS_VIEW, and Cortex Search
- **Custom Tool Integration**: Python stored procedures for PDF generation
- **Secure Report Storage**: Snowflake stage for governed document management

---

### Thematic Macro Advisor - Investment Theme Analysis

#### Business Context Setup

**Persona**: Anna, Portfolio Manager (Thematic Focus) at Snowcrest Asset Management  
**Business Challenge**: Portfolio managers need to identify and validate investment opportunities across macro trends by combining quantitative portfolio analysis with thematic research. Traditional approaches struggle to connect portfolio positioning with emerging themes and market trends effectively.  
**Value Proposition**: AI-powered thematic analysis that combines current portfolio positioning with comprehensive research synthesis to identify theme-based investment opportunities and optimize strategic allocation decisions.

**Agent**: `thematic_macro_advisor`  
**Data Available**: Portfolio holdings data + 100 broker reports, 75 press releases, 75 earnings transcripts

#### Demo Flow

**Scene Setting**: Anna is developing the quarterly thematic investment strategy and needs to assess current portfolio positioning against emerging macro trends, identify new thematic opportunities, and optimize portfolio allocation for maximum theme exposure.

##### Step 1: Current Thematic Positioning
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

##### Step 2: Thematic Research Discovery  
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

##### Step 3: Strategic Positioning Analysis
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

##### Step 4: Integrated Investment Strategy
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

#### Scenario Wrap-up

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

---

## Research Analyst

### Research Copilot - Document Research & Analysis

#### Business Context Setup

**Persona**: David, Research Analyst at Snowcrest Asset Management  
**Business Challenge**: Research analysts need to combine quantitative financial analysis with qualitative research synthesis across multiple sources (financial data, broker research, earnings calls, press releases) to build comprehensive investment cases. Manual analysis requires hours of data gathering, financial modeling, and document review, often missing critical connections between financial performance and strategic narratives.  
**Value Proposition**: AI-powered research intelligence that seamlessly combines structured financial analysis with unstructured document insights, enabling analysts to build complete investment theses faster and with greater depth than traditional approaches.

**Agent**: `research_copilot`  
**Data Available**: Financial fundamentals & estimates for 14,000+ securities + 100 broker reports, 75 earnings transcripts, 75 press releases

#### Demo Flow

**Scene Setting**: David is preparing a thematic research report on technology sector opportunities and needs to quickly synthesize insights from multiple document sources to identify emerging trends and validate investment themes.

##### Step 1: Multi-Source Research Synthesis
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

##### Step 2: Deep-Dive Company Analysis
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

##### Step 3: Competitive Intelligence Gathering
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

##### Step 4: Investment Thesis Validation
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

#### Scenario Wrap-up

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


### Research Copilot - Earnings Intelligence Extensions

#### Business Context Setup

**Persona**: Sarah, Senior Research Analyst at Snowcrest Asset Management  
**Business Challenge**: Research analysts need to rapidly analyze quarterly earnings releases, integrate financial data with management commentary, and identify sentiment shifts that could signal investment opportunities or risks. Traditional earnings analysis requires hours of manual transcription, data extraction, and cross-referencing across multiple documents, often missing subtle but critical sentiment changes.  
**Value Proposition**: AI-powered earnings intelligence that automatically processes financial filings, earnings call transcripts, and press releases to provide instant financial analysis combined with sentiment insights, enabling analysts to detect emerging trends and risks within minutes of earnings releases.

**Agent**: `research_copilot`  
**Data Available**: SEC filings for 14,000+ securities, earnings transcripts, press releases, financial fundamentals

#### Demo Flow

**Scene Setting**: Sarah is analyzing the latest quarterly earnings for a major technology holding and needs to quickly assess the financial performance, understand management sentiment, and identify any shifts in forward guidance that could impact the investment thesis.

##### Step 1: Integrated Earnings Analysis
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

##### Step 2: Sentiment Analysis and Red Flags
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

##### Step 3: Strategic Commentary Evolution
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

##### Step 4: Investment Committee Summary
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

#### Scenario Wrap-up

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

### Quant Analyst - Factor Analysis & Performance Attribution

#### Business Context Setup

**Persona**: Dr. James Chen, Quantitative Analyst at Snowcrest Asset Management  
**Business Challenge**: Quantitative analysts need advanced factor analysis, performance attribution, and systematic strategy development tools to identify patterns, screen securities, and develop data-driven investment approaches. Traditional quant tools are siloed and don't integrate fundamental research insights with quantitative analysis.  
**Value Proposition**: AI-powered quantitative analysis that instantly accesses comprehensive factor exposures and combines sophisticated factor modeling with fundamental research integration, enabling systematic strategy development with both quantitative rigor and qualitative context in seconds rather than minutes.

**Agent**: `quant_analyst`  
**Data Available**: Enhanced factor exposures (7 factors × 5 years × monthly), fundamentals data, 1,200 broker reports, 800 earnings transcripts

#### Demo Flow

**Scene Setting**: Dr. Chen is developing a new systematic strategy focused on quality and momentum factors. He needs to screen securities, analyze factor exposures, backtest strategies, and validate findings with fundamental research to present a comprehensive investment case.

##### Step 1: Factor Screening
**User Input**: 
```
"Screen for stocks with improving momentum and quality factors over the last 6 months."
```

**Alternative Query (if needed)**: 
```
"Show me stocks with the highest momentum and quality factor exposures from the latest data."
```

**Expected Response**:
- Table of securities with highest momentum and quality factor scores from recent period
- Specific momentum and quality factor exposures (numerical values showing factor loadings)
- Securities ranked by combined momentum and quality factor characteristics
- Available factors confirmed: Market, Size, Value, Growth, Momentum, Quality, Volatility
- Portfolio context showing which screened securities are already held

**Talking Points**:
- **Instant Factor Recognition**: Agent immediately understands available factors (Momentum, Quality, Value, Growth, etc.) without data exploration
- **Direct Factor Screening**: Systematic screening using pre-built factor metrics with statistical rigor
- **Portfolio Integration**: Immediate identification of factor exposures with portfolio context

**Key Features Highlighted**: 
- **Enhanced Factor Metrics**: Pre-built factor-specific metrics (MOMENTUM_SCORE, QUALITY_SCORE, VALUE_SCORE, GROWTH_SCORE)
- **Time-Series Factor Analysis**: Monthly factor exposures over 5 years enabling trend identification
- **Comprehensive Factor Coverage**: Complete factor universe (Market, Size, Value, Growth, Momentum, Quality, Volatility)

##### Step 2: Factor Comparison Analysis
**User Input**: 
```
"For the stocks with improving momentum and quality factors, compare their factor loadings against our current Value strategy and Growth strategy portfolios."
```

**Expected Response**:
- Side-by-side factor loading comparison between screened securities and current portfolio holdings
- Statistical significance of differences between high momentum/quality stocks and portfolio averages
- Factor tilt analysis showing how these securities would impact portfolio factor exposure
- Risk-adjusted performance implications of adding screened securities to existing portfolios
- Style drift assessment: would adding these securities maintain or shift portfolio style characteristics

**Talking Points**:
- **Targeted Factor Analysis**: Factor comparison focused on high momentum/quality securities vs existing holdings
- **Portfolio Impact Assessment**: Understanding how these securities would change factor exposures
- **Style Consistency Evaluation**: Maintaining investment style while improving factor characteristics

**Key Features Highlighted**: 
- **Conversation-Aware Analysis**: Factor analysis that builds directly on previous screening conversation
- **Portfolio Integration Analysis**: Assessment of how screened securities fit with existing factor exposures
- **Style Impact Evaluation**: Understanding factor changes from incorporating screened securities

##### Step 3: Factor Evolution Analysis
**User Input**: 
```
"Analyze the factor exposure trends of our momentum and quality securities over the last 3 years and show how their factor characteristics have evolved."
```

**Expected Response**:
- Time-series analysis of momentum and quality factor exposures for screened securities
- Factor stability analysis showing consistency of factor characteristics over time
- Comparison of factor evolution between screened securities and benchmark constituents
- Statistical significance of factor improvements over the 3-year period
- Portfolio impact assessment: how factor evolution affects current holdings

**Talking Points**:
- **Time-Series Factor Analysis**: Sophisticated analysis of factor evolution using 5 years of monthly data
- **Factor Stability Assessment**: Understanding consistency and persistence of factor characteristics
- **Trend Validation**: Statistical validation of factor improvement trends over time

**Key Features Highlighted**: 
- **Time-Series Analysis**: 5 years of monthly factor exposure data enabling sophisticated trend analysis
- **Factor Persistence Studies**: Understanding factor stability and consistency over time periods
- **Statistical Validation**: Rigorous analysis of factor improvement trends with significance testing

##### Step 4: Fundamental Context Integration
**User Input**: 
```
"For the securities with the strongest factor evolution trends, what fundamental themes and research support their improving factor characteristics?"
```

**Expected Response**:
- Analysis of fundamental characteristics of top-performing momentum and quality securities
- Earnings trends and analyst sentiment for securities that drove the strategy performance
- Thematic and sector drivers that explain the success of momentum and quality factor selection
- Research validation showing fundamental support for the quantitative factor improvements
- Integration of the complete workflow: factor screening → factor analysis → performance validation → fundamental context

**Talking Points**:
- **Complete Investment Validation**: Fundamental research validates the entire momentum/quality quantitative process
- **Factor-Fundamental Integration**: Understanding why the factor approach worked from both quantitative and qualitative perspectives  
- **Investment Thesis Completion**: Full investment case combining systematic factor analysis with fundamental validation

**Key Features Highlighted**: 
- **End-to-End Integration**: Complete quantitative-to-qualitative workflow validation from screening to fundamental context
- **Conversational Synthesis**: Fundamental analysis that validates and explains the quantitative findings developed in conversation
- **Comprehensive Investment Process**: Complete systematic investment approach combining factor analysis, backtesting, and fundamental research

#### Scenario Wrap-up

**Business Impact Summary**:
- **Speed & Efficiency**: Instant factor screening and analysis eliminating traditional data exploration delays (seconds vs minutes)
- **Strategy Development**: Enhanced systematic strategy development with pre-built factor metrics and time-series analysis
- **Investment Edge**: Earlier identification of factor-based opportunities with comprehensive 7-factor model coverage
- **Research Integration**: Seamless combination of quantitative factor models with fundamental research validation

**Technical Differentiators**:
- **Pre-Built Factor Metrics**: Instant access to factor-specific metrics (MOMENTUM_SCORE, QUALITY_SCORE) eliminating data exploration delays
- **Time-Series Factor Analysis**: 5 years of monthly factor exposures enabling sophisticated trend analysis and screening
- **Complete Factor Universe**: 7-factor model (Market, Size, Value, Growth, Momentum, Quality, Volatility) with sector-specific characteristics
- **Research Integration**: Unique combination of quantitative factor analysis with fundamental research validation

---

## Client Relations  

### Sales Advisor - Client Reporting & Template Formatting

#### Business Context Setup

**Persona**: James Mitchell, Client Relationship Manager at Snowcrest Asset Management  
**Business Challenge**: Client relationship managers need to produce professional, compliant, and compelling client reports that integrate performance data with approved messaging templates and investment philosophy. Traditional processes require manual data gathering, template formatting, compliance review, and brand alignment, consuming significant time and introducing formatting inconsistencies.  
**Value Proposition**: AI-powered client reporting that automatically combines portfolio analytics with approved templates, investment philosophy, and compliance language to generate professional, relationship-building client communications in minutes.

**Agent**: `sales_advisor`  
**Data Available**: Portfolio performance data, sales report templates, investment philosophy documents, compliance policies, brand messaging guidelines

#### Demo Flow

**Scene Setting**: James needs to prepare a monthly client report for a key institutional client with their SAM Technology & Infrastructure portfolio, ensuring professional presentation with proper compliance language and brand messaging.

##### Step 1: Portfolio Performance Foundation
**User Input**: 
```
"Generate a client report for the SAM Technology & Infrastructure portfolio showing quarterly performance, top holdings, and sector allocation"
```

**Expected Response**:
- **Performance Summary**: Quarterly returns vs benchmark with multiple time periods
- **Top Holdings Table**: Largest positions with weights and contribution to performance
- **Sector Allocation**: Technology sector breakdown with allocation percentages
- **Performance Attribution**: Key contributors and detractors to portfolio performance
- **Concentration Warnings**: Flag any positions >6.5% with "⚠️ CONCENTRATION WARNING"
- **Professional Structure**: Executive summary format with clear data presentation

**Talking Points**:
- **Comprehensive Analytics**: AI instantly gathers all required portfolio data for client reporting
- **Professional Formatting**: Automatically structures data in client-appropriate format
- **Risk Highlighting**: Proactive flagging of concentration risks for client transparency

**Key Features Highlighted**: 
- **SAM_ANALYST_VIEW**: Complete portfolio analytics for client reporting foundation
- **Automated Formatting**: AI structures complex portfolio data for client presentation
- **Risk Management**: Automatic concentration warning and risk disclosure

##### Step 2: Template Integration and Professional Formatting
**User Input**: 
```
"Format this into a professional monthly client report using our approved template structure with proper sections and branding"
```

**Expected Response**:
- **Template Structure**: Monthly Client Report format with standardised sections
- **Executive Summary**: Key performance highlights and market commentary section
- **Performance Analysis**: Detailed returns analysis with benchmark comparison
- **Holdings Overview**: Portfolio composition and changes section
- **Market Commentary**: Template-guided market outlook section
- **Professional Layout**: Consistent formatting with SAM branding elements
- **Section Headers**: Clear, template-compliant section organisation

**Talking Points**:
- **Template Compliance**: AI automatically applies approved report templates for consistency
- **Brand Standards**: Ensures all client communications follow SAM brand guidelines
- **Professional Presentation**: Client-ready formatting that enhances relationship value

**Key Features Highlighted**: 
- **SAM_SALES_TEMPLATES**: Comprehensive template library for consistent client communications
- **Automated Formatting**: AI applies professional structure and branding consistently
- **Template Intelligence**: Smart adaptation of content to template requirements

##### Step 3: Investment Philosophy and Brand Integration
**User Input**: 
```
"Integrate our ESG investment philosophy and technology innovation messaging to align the report with SAM's strategic positioning"
```

**Expected Response**:
- **ESG Integration**: SAM's sustainable investment approach woven into performance narrative
- **Technology Focus**: Innovation leadership messaging aligned with technology portfolio theme
- **Investment Philosophy**: Core beliefs about ESG and technology investing naturally integrated
- **Brand Messaging**: Competitive differentiators and unique capabilities highlighted
- **Strategic Positioning**: SAM's forward-thinking, technology-enhanced approach emphasised
- **Value Proposition**: Clear articulation of why SAM's approach benefits clients

**Talking Points**:
- **Philosophy Alignment**: Seamlessly integrates SAM's investment beliefs into client communications
- **Brand Consistency**: Ensures all client touchpoints reinforce strategic positioning
- **Relationship Building**: Enhances client understanding of SAM's unique value proposition

**Key Features Highlighted**: 
- **SAM_PHILOSOPHY_DOCS**: Comprehensive investment philosophy and brand messaging library
- **Natural Integration**: AI weaves philosophy into performance narrative without appearing promotional
- **Strategic Messaging**: Consistent reinforcement of SAM's competitive differentiators

##### Step 4: Compliance Review and Final Document
**User Input**: 
```
"Complete the compliance review by adding all required regulatory disclosures, risk warnings, and fiduciary language for final client delivery"
```

**Expected Response**:
- **Regulatory Disclosures**: All mandatory disclaimers and risk warnings included
- **Performance Disclaimers**: "Past performance does not guarantee future results" and appropriate caveats
- **Fiduciary Language**: Professional standard disclaimers for investment advice
- **Risk Warnings**: Market risk, concentration risk, and investment limitation disclosures
- **Compliance Standards**: Full regulatory compliance for client communication
- **Final Document**: Complete, compliance-ready client report for immediate delivery

**Talking Points**:
- **Regulatory Compliance**: AI ensures all client communications meet regulatory standards
- **Risk Management**: Comprehensive risk disclosure protects both client and firm
- **Fiduciary Excellence**: Professional-grade compliance language maintains highest standards

**Key Features Highlighted**: 
- **SAM_POLICY_DOCS**: Complete compliance manual and regulatory requirements library
- **Compliance Automation**: AI automatically includes all required disclosures and warnings
- **Professional Standards**: Ensures client communications meet institutional investment standards

#### Scenario Wrap-up

**Business Impact Summary**:
- **Productivity Gains**: Client report generation reduced from hours to minutes, enabling more client interaction time
- **Consistency Assurance**: Automated template and brand compliance ensures professional standard across all client communications
- **Compliance Excellence**: Comprehensive regulatory disclosure automation reduces compliance risk and review time
- **Relationship Enhancement**: Professional, compelling reports strengthen client relationships and demonstrate institutional capabilities

**Technical Differentiators**:
- **Multi-Source Integration**: Seamlessly combines portfolio data, templates, philosophy, and compliance requirements in single workflow
- **Template Intelligence**: AI-powered formatting that adapts content to professional report structures while maintaining brand consistency
- **Compliance Automation**: Comprehensive regulatory disclosure integration ensures client communications meet institutional standards
- **Brand Integration**: Natural weaving of investment philosophy and strategic messaging into performance narratives

---

## Risk & Compliance Officer

### ESG Guardian - ESG Risk Monitoring & Policy Compliance

#### Business Context Setup

**Persona**: Sofia, ESG & Risk Officer at Snowcrest Asset Management  
**Business Challenge**: ESG officers need proactive monitoring of sustainability risks, policy compliance, and engagement tracking to maintain ESG leadership and avoid reputational damage. Manual monitoring of ESG controversies across hundreds of portfolio companies is time-consuming and risks missing critical issues.  
**Value Proposition**: AI-powered ESG risk monitoring that automatically scans for controversies, tracks engagement history, and ensures policy compliance, enabling proactive risk management and comprehensive ESG governance.

**Agent**: `esg_guardian`  
**Data Available**: 500 NGO reports, 150 engagement notes, 8 policy documents

#### Demo Flow

**Scene Setting**: Sofia has received alerts about potential ESG issues affecting portfolio companies and needs to quickly assess the situation, review engagement history, check policy compliance, and prepare a comprehensive report for the ESG committee.

##### Step 1: Proactive Controversy Scanning
**User Input**: 
```
"Scan for any new ESG controversies affecting our portfolio companies in the last 30 days."
```

**Expected Response**:
- List of flagged controversies with severity levels (High/Medium/Low)
- Affected portfolio companies and exposure amounts
- Source citations with NGO names and publication dates

**Talking Points**:
- Automated ESG controversy detection across all portfolio holdings
- Risk severity assessment and prioritization for immediate action
- Comprehensive source attribution for credibility and follow-up

**Key Features Highlighted**: 
- Proactive ESG risk monitoring and automatic flagging
- Portfolio exposure analysis for risk quantification
- Multi-source NGO report analysis and synthesis

##### Step 2: Internal Context Retrieval
**User Input**: 
```
"For the companies flagged in Step 1, do we have any engagement history with these companies regarding the specific ESG issues identified?"
```

**Expected Response**:
- Summary of previous engagement meetings and topics for each flagged company from Step 1
- Key commitments made by management specific to the ESG issues from Step 1
- Follow-up actions and timelines from engagement logs that relate to the Step 1 controversies
- Gap analysis: which flagged companies have no prior engagement history

**Talking Points**:
- **Contextual Engagement Review**: Focuses on the specific companies and issues from Step 1
- **Issue-Specific History**: Reviews engagement records that directly relate to the identified controversies
- **Strategic Gap Identification**: Highlights companies requiring new engagement based on Step 1 findings

**Key Features Highlighted**: 
- **Context-Aware Search**: Engagement search specifically targets Step 1 flagged companies and issues
- **Issue-Specific Intelligence**: Historical context directly relevant to current controversies
- **Strategic Planning Support**: Identifies engagement gaps based on current risk assessment

##### Step 3: Policy Compliance Assessment
**User Input**: 
```
"What does our ESG policy say about the specific issues identified in Step 1, and what's our total exposure to each of the flagged companies?"
```

**Expected Response**:
- Relevant policy clauses with exact text and section references for each ESG issue type from Step 1
- Current total AUM exposure across all funds for each company flagged in Step 1
- Policy-mandated actions specific to each issue type (review, exclusion, engagement requirements)
- Compliance assessment: which flagged situations require immediate action vs monitoring
- Integration with Step 2 findings: where existing engagement supports policy compliance

**Talking Points**:
- **Issue-Specific Policy Guidance**: Policy assessment directly addresses the controversies from Step 1
- **Comprehensive Exposure Analysis**: Total firm exposure to each specific flagged company
- **Integrated Compliance Framework**: Combines policy requirements with engagement history from Step 2

**Key Features Highlighted**: 
- **Context-Specific Policy Search**: Policy analysis tailored to Step 1 ESG issues
- **Multi-Company Risk Aggregation**: Total exposure analysis for all Step 1 flagged companies
- **Integrated Compliance Assessment**: Policy requirements viewed alongside engagement history

##### Step 4: Committee Reporting
**User Input**: 
```
"Draft a comprehensive ESG committee summary covering all the companies and issues we've analyzed in Steps 1-3."
```

**Expected Response**:
- Executive summary covering all controversies identified in Step 1 with severity prioritization
- Portfolio impact assessment with exposure calculations for each flagged company
- Engagement status review for each company based on Step 2 findings
- Policy compliance analysis for each issue type from Step 3
- Recommended actions with timelines, prioritization, and policy references
- Integration of all previous analysis into comprehensive ESG governance report

**Talking Points**:
- **Complete ESG Governance Report**: Synthesizes all findings from the 3-step analysis process
- **Executive Decision Support**: Provides prioritized action plan based on comprehensive assessment
- **Audit-Ready Documentation**: Creates complete record of ESG risk assessment and response

**Key Features Highlighted**: 
- **Multi-Step Synthesis**: Integrates controversy detection, engagement review, and policy analysis
- **Executive Reporting**: Complete ESG governance report ready for committee decision-making
- **Comprehensive Documentation**: Full audit trail of ESG risk assessment and recommended actions

#### Scenario Wrap-up

**Business Impact Summary**:
- **Risk Mitigation**: Proactive identification and management of ESG controversies
- **Governance Excellence**: Comprehensive ESG committee reporting and decision support
- **Compliance Assurance**: Automated policy compliance checking and guidance
- **Operational Efficiency**: Reduced manual monitoring and reporting time from days to minutes

**Technical Differentiators**:
- **Proactive Monitoring**: AI-powered controversy detection across multiple NGO sources
- **Historical Context**: Comprehensive engagement tracking and commitment monitoring
- **Policy Integration**: Automated compliance checking with policy-based action guidance
- **Executive Reporting**: Multi-source synthesis for comprehensive ESG governance

### Compliance Advisor - Mandate Monitoring & Breach Detection

#### Business Context Setup

**Persona**: Michael, Compliance Officer at Snowcrest Asset Management  
**Business Challenge**: Compliance officers need automated monitoring of investment mandates, breach detection, and policy adherence to ensure regulatory compliance and fiduciary responsibility. Manual compliance monitoring across multiple portfolios is error-prone and time-consuming, risking regulatory violations and client mandate breaches.  
**Value Proposition**: AI-powered compliance monitoring that automatically detects breaches, provides policy guidance, and generates audit-ready documentation, ensuring continuous compliance and reducing regulatory risk.

**Agent**: `compliance_advisor`  
**Data Available**: 8 policy documents, 150 engagement logs, portfolio holdings

#### Demo Flow

**Scene Setting**: Michael is conducting his daily compliance review and needs to check for any mandate breaches, investigate specific concentration limits, plan remediation actions, and prepare documentation for audit purposes.

##### Step 1: Compliance Breach Detection
**User Input**: 
```
"Check all portfolios for active compliance breaches as of today."
```

**Expected Response**:
- List of breaches by portfolio and rule type
- Severity assessment (breach vs warning thresholds)
- Affected positions with amounts and percentages

**Talking Points**:
- Automated daily compliance monitoring across all portfolios
- Real-time breach detection with severity assessment
- Comprehensive coverage of all mandate and regulatory requirements

**Key Features Highlighted**: 
- Automated compliance monitoring and breach detection
- Real-time portfolio analysis against mandate requirements
- Risk prioritization with severity assessment

##### Step 2: Rule Documentation
**User Input**: 
```
"For the specific breaches identified in Step 1, show me the exact policy clauses and concentration limits that are being violated"
```

**Expected Response**:
- Exact policy text with section references for each breach type from Step 1
- Specific concentration limits and thresholds that apply to each flagged position
- Applicable portfolios and any exceptions for each breach
- Historical context and rationale for each rule being violated
- Severity assessment: which breaches are hard limits vs warnings

**Talking Points**:
- **Context-Specific Policy Research**: Policy lookup directly addresses the breaches from Step 1
- **Breach-Specific Documentation**: Exact clauses and limits for each identified violation
- **Compliance Severity Assessment**: Understanding which violations require immediate action

**Key Features Highlighted**: 
- **Contextual Policy Search**: Policy research specifically targets Step 1 breach types
- **Violation-Specific Intelligence**: Exact clauses and limits for each identified compliance issue
- **Severity Classification**: Understanding of breach vs warning thresholds for prioritization

##### Step 3: Remediation Planning
**User Input**: 
```
"For each breach identified in Steps 1-2, what are our remediation options and what's the priority order for addressing these violations?"
```

**Expected Response**:
- Remediation options for each specific breach from Step 1, considering the policy requirements from Step 2
- Calculation of excess exposure amounts above limits for each violation
- Multiple reduction scenarios with market impact considerations for each breach
- Priority ranking based on severity assessment from Step 2 (hard breaches vs warnings)
- Timeline recommendations for compliance restoration with sequencing based on priority
- Resource allocation: which breaches can be addressed simultaneously vs requiring sequential action

**Talking Points**:
- **Comprehensive Remediation Strategy**: Addresses all breaches identified in Steps 1-2 with integrated planning
- **Priority-Based Approach**: Sequences remediation based on severity and policy requirements
- **Resource Optimization**: Efficient remediation plan considering market impact and operational capacity

**Key Features Highlighted**: 
- **Multi-Breach Remediation Planning**: Integrated approach to addressing all compliance issues simultaneously
- **Priority-Based Sequencing**: Remediation order based on severity assessment from Step 2
- **Market Impact Optimization**: Remediation plans that minimize trading costs and market disruption

##### Step 4: Audit Trail Documentation
**User Input**: 
```
"Generate a comprehensive compliance incident report covering all breaches identified in Steps 1-3 with our complete remediation plan"
```

**Expected Response**:
- Formal incident documentation covering all breaches from Step 1 with timeline
- Policy references and breach calculations for each violation identified in Step 2
- Complete remediation plan from Step 3 with milestones, priorities, and responsibilities
- Executive summary of compliance status and remediation strategy
- Regulatory documentation ready for audit review
- Integration of all analysis from Steps 1-3 into comprehensive compliance record

**Talking Points**:
- **Comprehensive Compliance Documentation**: Complete audit trail covering all breaches and remediation plans
- **Regulatory-Ready Reporting**: Full documentation meeting all audit and regulatory requirements
- **Integrated Compliance Management**: Single report covering detection, analysis, and remediation strategy

**Key Features Highlighted**: 
- **Multi-Step Documentation Synthesis**: Integrates breach detection, policy analysis, and remediation planning
- **Regulatory Compliance Reporting**: Audit-ready documentation with complete compliance workflow
- **Comprehensive Audit Trail**: Full record of compliance assessment and response for regulatory review

#### Scenario Wrap-up

**Business Impact Summary**:
- **Regulatory Compliance**: Automated monitoring ensures continuous compliance with all mandates
- **Risk Reduction**: Proactive breach detection prevents regulatory violations and client issues
- **Operational Efficiency**: Reduced manual compliance monitoring time by 80%
- **Audit Readiness**: Comprehensive documentation and audit trails for regulatory reviews

**Technical Differentiators**:
- **Real-time Monitoring**: Continuous compliance assessment across all portfolios and mandates
- **Policy Intelligence**: AI-powered policy search and interpretation with exact clause retrieval
- **Impact Analysis**: Sophisticated remediation planning with market impact considerations
- **Audit Documentation**: Automated generation of regulatory-ready compliance reports

