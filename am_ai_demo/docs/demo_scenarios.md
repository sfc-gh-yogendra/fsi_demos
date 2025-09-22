# SAM Demo - Scenario Scripts

Reference: See `docs/implementation_plan.md` for the build order and implementation details referenced by these scenarios.

Complete demo scenario for Portfolio Copilot with step-by-step conversations, expected responses, and data flows.

## Current Implementation Status

✅ **Phase 1 & 2 Complete**: 3 scenarios fully operational for demonstration
- **Portfolio Copilot**: ✅ Portfolio analytics and benchmarking (Phase 1)
- **Research Copilot**: ✅ Document research and analysis (Phase 2)
- **Thematic Macro Advisor**: ✅ Thematic investment strategy (Phase 2)

✅ **Phase 4 Complete**: Advanced factor analysis and client reporting
- **Quant Analyst**: ✅ Factor analysis and performance attribution (Phase 4)
- **Sales Advisor**: ✅ Client reporting and template formatting (Phase 4)

🔄 **Phase 3 Ready for Implementation**: ESG & Compliance scenarios
- **ESG Guardian**: ESG risk monitoring and policy compliance
- **Compliance Advisor**: Mandate monitoring and breach detection

## Scenario 1: Portfolio Copilot - Portfolio Insights & Benchmarking

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

## Scenario 2: Research Copilot - Document Research & Analysis ✅ PHASE 2

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

## Scenario 3: Thematic Macro Advisor - Investment Theme Analysis ✅ PHASE 2

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

## Scenario 4: ESG Guardian - ESG Risk Monitoring

### Business Context Setup

**Persona**: Sofia, ESG & Risk Officer at Snowcrest Asset Management  
**Business Challenge**: ESG officers need proactive monitoring of sustainability risks, policy compliance, and engagement tracking to maintain ESG leadership and avoid reputational damage. Manual monitoring of ESG controversies across hundreds of portfolio companies is time-consuming and risks missing critical issues.  
**Value Proposition**: AI-powered ESG risk monitoring that automatically scans for controversies, tracks engagement history, and ensures policy compliance, enabling proactive risk management and comprehensive ESG governance.

**Agent**: `esg_guardian`  
**Data Available**: 500 NGO reports, 150 engagement notes, 8 policy documents

### Demo Flow

**Scene Setting**: Sofia has received alerts about potential ESG issues affecting portfolio companies and needs to quickly assess the situation, review engagement history, check policy compliance, and prepare a comprehensive report for the ESG committee.

#### Step 1: Proactive Controversy Scanning
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

#### Step 2: Internal Context Retrieval
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

#### Step 3: Policy Compliance Assessment
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

#### Step 4: Committee Reporting
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

### Scenario Wrap-up

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

## Scenario 5: Compliance Advisor - Mandate Monitoring

### Business Context Setup

**Persona**: Michael, Compliance Officer at Snowcrest Asset Management  
**Business Challenge**: Compliance officers need automated monitoring of investment mandates, breach detection, and policy adherence to ensure regulatory compliance and fiduciary responsibility. Manual compliance monitoring across multiple portfolios is error-prone and time-consuming, risking regulatory violations and client mandate breaches.  
**Value Proposition**: AI-powered compliance monitoring that automatically detects breaches, provides policy guidance, and generates audit-ready documentation, ensuring continuous compliance and reducing regulatory risk.

**Agent**: `compliance_advisor`  
**Data Available**: 8 policy documents, 150 engagement logs, portfolio holdings

### Demo Flow

**Scene Setting**: Michael is conducting his daily compliance review and needs to check for any mandate breaches, investigate specific concentration limits, plan remediation actions, and prepare documentation for audit purposes.

#### Step 1: Compliance Breach Detection
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

#### Step 2: Rule Documentation
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

#### Step 3: Remediation Planning
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

#### Step 4: Audit Trail Documentation
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

### Scenario Wrap-up

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

## Scenario 6: Sales Advisor - Client Reporting

### Business Context Setup

**Persona**: Sarah, Client Relationship Manager at Snowcrest Asset Management  
**Business Challenge**: Client relationship managers need to generate professional client reports, integrate investment philosophy, and maintain consistent messaging while ensuring compliance with regulatory requirements. Manual report creation is time-consuming and risks inconsistent messaging or missing compliance disclosures.  
**Value Proposition**: AI-powered client reporting that automatically generates professional reports, integrates approved messaging and philosophy, and ensures compliance adherence, enabling consistent high-quality client communication at scale.

**Agent**: `sales_advisor`  
**Data Available**: 2 sales templates, 3 philosophy documents, 8 policy documents

### Demo Flow

**Scene Setting**: Sarah needs to prepare the monthly performance report for a key institutional client invested in the ESG Leaders Global Equity portfolio. The report must be professional, include the firm's investment philosophy, and meet all regulatory compliance requirements.

#### Step 1: Performance Report Generation
**User Input**: 
```
"Generate a monthly performance report for the ESG Leaders Global Equity portfolio."
```

**Expected Response**:
- Performance summary vs benchmark with key metrics
- Top contributors and detractors to performance
- Sector allocation and ESG score summary
- Professional formatting with appropriate disclaimers

**Talking Points**:
- Automated performance reporting with comprehensive analytics
- Professional formatting and presentation ready for client delivery
- Integration of ESG metrics relevant to the strategy

**Key Features Highlighted**: 
- Automated performance reporting and data synthesis
- ESG-specific analytics and scoring integration
- Professional client-ready formatting

#### Step 2: Template Integration
**User Input**: 
```
"Format the ESG Leaders portfolio performance from Step 1 using our standard monthly client template"
```

**Expected Response**:
- Report restructured following template format using the specific performance data from Step 1
- Professional sections (Executive Summary, Performance, Holdings, Outlook) populated with ESG Leaders data
- Consistent branding and compliance language applied to the Step 1 performance metrics
- Client-appropriate tone and structure that incorporates the specific portfolio results
- Template formatting that maintains the quantitative analysis from Step 1

**Talking Points**:
- **Data-Template Integration**: Professional formatting applied to specific portfolio analysis from Step 1
- **Performance-Driven Presentation**: Template structure enhances rather than replaces the analytical content
- **Consistent Professional Standards**: Quality formatting while preserving analytical rigor

**Key Features Highlighted**: 
- **Content-Aware Formatting**: Template application that preserves and enhances Step 1 analytical content
- **Data-Driven Presentation**: Professional formatting of specific portfolio performance and metrics
- **Integrated Client Communication**: Seamless combination of analytics and professional presentation

#### Step 3: Philosophy Integration
**User Input**: 
```
"Add our ESG investment philosophy to this templated report, specifically explaining how it connects to the performance results shown in Steps 1-2"
```

**Expected Response**:
- Integration of approved ESG messaging and philosophy that specifically addresses the portfolio performance from Step 1
- Alignment of performance narrative with investment approach using the templated format from Step 2
- Strategic positioning that explains how the philosophy drives the results shown in the report
- Consistent brand voice that connects investment approach to actual performance outcomes
- Philosophy sections that reference specific metrics and performance data from Steps 1-2

**Talking Points**:
- **Performance-Philosophy Alignment**: ESG philosophy specifically connected to actual portfolio results
- **Results-Driven Messaging**: Philosophy explanation that validates the performance outcomes
- **Integrated Value Proposition**: Clear connection between investment approach and delivered results

**Key Features Highlighted**: 
- **Performance-Driven Philosophy**: Investment approach explanation that directly relates to portfolio results
- **Integrated Messaging**: Philosophy integration that builds on performance data and professional formatting
- **Results Validation**: Philosophy positioning that supports and explains the performance outcomes

#### Step 4: Compliance Review
**User Input**: 
```
"Review this complete ESG Leaders report from Steps 1-3 and ensure it includes all required compliance disclosures, disclaimers, and regulatory language appropriate for the performance data and philosophy statements included"
```

**Expected Response**:
- Addition of mandatory regulatory disclosures specific to ESG Leaders portfolio performance from Step 1
- Risk warnings and performance disclaimers that address the specific metrics and results shown
- Fiduciary language and limitations appropriate for the ESG investment philosophy from Step 3
- ESG-specific compliance language and disclaimers relevant to sustainable investing
- Template-compliant disclaimer placement that works with the formatting from Step 2
- Compliance-ready final document that integrates all elements from previous steps

**Talking Points**:
- **Context-Aware Compliance**: Regulatory language specifically appropriate for ESG portfolio and performance data
- **Integrated Compliance Framework**: Disclaimers and disclosures that address all report elements
- **Complete Regulatory Coverage**: Full compliance review of performance, philosophy, and presentation

**Key Features Highlighted**: 
- **Content-Specific Compliance**: Regulatory requirements tailored to ESG portfolio performance and philosophy
- **Integrated Regulatory Framework**: Compliance review that addresses all report components from Steps 1-3
- **Complete Audit Readiness**: Final document ready for regulatory review with comprehensive compliance coverage

### Scenario Wrap-up

**Business Impact Summary**:
- **Client Service Excellence**: Professional, consistent reporting that enhances client relationships
- **Operational Efficiency**: Reduced report preparation time from hours to minutes
- **Compliance Assurance**: Automated inclusion of all required disclosures and disclaimers
- **Brand Consistency**: Unified messaging and philosophy integration across all client communications

**Technical Differentiators**:
- **Template Intelligence**: AI-powered formatting using approved templates and branding guidelines
- **Philosophy Integration**: Seamless incorporation of investment philosophy and messaging
- **Compliance Automation**: Automated inclusion of regulatory disclosures and risk warnings
- **Scalable Reporting**: Consistent high-quality reports across multiple clients and strategies

## Scenario 7: Quant Analyst - Factor Analysis

### Business Context Setup

**Persona**: Dr. James Chen, Quantitative Analyst at Snowcrest Asset Management  
**Business Challenge**: Quantitative analysts need advanced factor analysis, performance attribution, and systematic strategy development tools to identify patterns, screen securities, and develop data-driven investment approaches. Traditional quant tools are siloed and don't integrate fundamental research insights with quantitative analysis.  
**Value Proposition**: AI-powered quantitative analysis that instantly accesses comprehensive factor exposures and combines sophisticated factor modeling with fundamental research integration, enabling systematic strategy development with both quantitative rigor and qualitative context in seconds rather than minutes.

**Agent**: `quant_analyst`  
**Data Available**: Enhanced factor exposures (7 factors × 5 years × monthly), fundamentals data, 1,200 broker reports, 800 earnings transcripts

### Demo Flow

**Scene Setting**: Dr. Chen is developing a new systematic strategy focused on quality and momentum factors. He needs to screen securities, analyze factor exposures, backtest strategies, and validate findings with fundamental research to present a comprehensive investment case.

#### Step 1: Factor Screening
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

#### Step 2: Factor Comparison Analysis
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

#### Step 3: Factor Evolution Analysis
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

#### Step 4: Fundamental Context Integration
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

### Scenario Wrap-up

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

## Scenario 7: Quant Analyst - Factor Analysis & Attribution ❌ PHASE 4

### Business Context Setup

**Persona**: Dr. Sarah Chen, Quantitative Analyst at Snowcrest Asset Management  
**Business Challenge**: Quantitative analysts need to conduct systematic factor analysis, performance attribution, and backtesting across complex multi-factor models. Traditional approaches require complex data extraction, manual factor calculation, and time-consuming statistical analysis across multiple systems, limiting the speed and depth of quantitative research.  
**Value Proposition**: AI-powered quantitative analysis that instantly combines factor exposures, fundamental metrics, and performance data to enable systematic strategy development, rigorous backtesting, and comprehensive attribution analysis in minutes rather than hours.

**Agent**: `quant_analyst`  
**Data Available**: Factor exposures for 6 factors across 14,000+ securities, fundamentals & estimates, market data, benchmark holdings, portfolio positions

### Demo Flow

**Scene Setting**: Dr. Chen is developing a systematic factor strategy for the quantitative equity team and needs to analyze factor exposures, conduct performance attribution, and validate strategy backtesting across multiple quantitative models.

#### Step 1: Factor Screening and Portfolio Analysis
**User Input**: 
```
"Show me securities in our portfolios with high Quality factor exposure (>0.5) and their current portfolio weights across all strategies"
```

**Expected Response**:
- **Factor-Filtered Securities**: Table showing companies with Quality factor >0.5
- **Current Holdings**: Portfolio weights and exposures across SAM strategies  
- **Factor Statistics**: Quality factor loadings, R-squared values, statistical significance
- **Portfolio Impact**: Total exposure to high-quality securities by strategy
- **Factor Characteristics**: Sector distribution and fundamental metrics of quality-screened securities

**Talking Points**:
- **Systematic Screening**: AI automatically filters 14,000+ securities by quantitative factor criteria
- **Multi-Portfolio View**: Instant analysis across all portfolio strategies simultaneously
- **Statistical Validation**: R-squared and significance testing for factor model reliability

**Key Features Highlighted**: 
- **SAM_QUANT_VIEW**: Advanced semantic view with factor exposures, fundamentals, and portfolio data
- **Quantitative Filtering**: Sophisticated factor-based security screening capabilities
- **Statistical Analysis**: Factor model validation with R-squared and significance metrics

#### Step 2: Performance Attribution Analysis
**User Input**: 
```
"For the SAM Technology & Infrastructure portfolio, break down last quarter's performance attribution by factor exposures - show me which factors contributed most to returns"
```

**Expected Response**:
- **Factor Attribution Table**: Contribution to returns by factor (Market, Value, Growth, Quality, Momentum, Volatility)
- **Active vs Passive**: Factor-based attribution of active return vs benchmark
- **Statistical Significance**: Confidence intervals and t-statistics for factor contributions
- **Risk Decomposition**: Systematic vs specific risk attribution with factor model context
- **Attribution Summary**: Total factor effects vs security selection effects

**Talking Points**:
- **Systematic Attribution**: AI decomposes performance using rigorous factor models
- **Risk-Adjusted Analysis**: Factor attribution with proper statistical validation
- **Active Management Insight**: Quantifies skill vs factor exposure in performance

**Key Features Highlighted**: 
- **Factor Model Integration**: Comprehensive factor-based performance attribution
- **Statistical Rigor**: Confidence intervals and significance testing for attribution analysis
- **Risk Analytics**: Systematic risk decomposition using factor model framework

#### Step 3: Factor Strategy Backtesting
**User Input**: 
```
"Backtest a momentum factor strategy: screen for securities with momentum factor >0.3, equal-weight them, and show performance vs S&P 500 over the last 2 years with full risk metrics"
```

**Expected Response**:
- **Strategy Definition**: Momentum factor >0.3 screening criteria and methodology
- **Backtesting Results**: Strategy performance vs S&P 500 with monthly rebalancing
- **Risk Metrics**: Sharpe ratio, information ratio, maximum drawdown, tracking error
- **Factor Analysis**: Strategy's factor exposures vs benchmark over time
- **Statistical Validation**: T-statistics, confidence intervals, and significance of outperformance
- **Risk Attribution**: Factor-based risk decomposition and concentration analysis

**Talking Points**:
- **Systematic Strategy Testing**: Rigorous backtesting with factor-based methodology
- **Comprehensive Risk Analysis**: Multiple risk metrics with statistical validation
- **Factor Consistency**: Tracking factor exposure drift and strategy stability over time

**Key Features Highlighted**: 
- **Advanced Backtesting**: Sophisticated strategy simulation with factor model integration
- **Risk-Adjusted Performance**: Comprehensive risk metrics with statistical significance
- **Factor Stability Analysis**: Tracking systematic factor exposure consistency over time

#### Step 4: Fundamental Validation and Research Integration
**User Input**: 
```
"For the top 5 performing securities in that momentum strategy, show me their fundamental metrics and any recent earnings commentary to validate the factor signal"
```

**Expected Response**:
- **Top Performers**: 5 best-performing securities from momentum strategy with factor scores
- **Fundamental Validation**: Revenue growth, earnings trends, fundamental momentum metrics
- **Management Commentary**: Earnings call excerpts supporting business momentum themes
- **Analyst Research**: Broker research supporting fundamental momentum narratives  
- **Factor Confirmation**: Statistical validation of fundamental momentum vs factor momentum
- **Integrated Analysis**: Synthesis of quantitative factor signals with fundamental business drivers

**Talking Points**:
- **Factor Validation**: Confirms quantitative signals with fundamental business drivers
- **Integrated Research**: Combines systematic factor analysis with qualitative fundamental insights
- **Signal Verification**: Validates statistical factor models with business reality

**Key Features Highlighted**: 
- **Multi-Source Integration**: Combines factor analysis with fundamental research and management commentary
- **Signal Validation**: Sophisticated approach to confirming quantitative models with qualitative evidence
- **Systematic Research**: AI-driven validation of factor strategies using multiple data sources

### Scenario Wrap-up

**Business Impact Summary**:
- **Research Velocity**: Factor analysis and backtesting completed in minutes vs hours, enabling rapid strategy iteration
- **Statistical Rigor**: Comprehensive significance testing and validation provides confidence in systematic strategies
- **Integrated Analysis**: Seamless combination of quantitative factor models with fundamental validation enhances decision quality
- **Risk Management**: Detailed factor attribution and risk decomposition enables superior risk-adjusted strategy development

**Technical Differentiators**:
- **SAM_QUANT_VIEW**: Purpose-built semantic view combining factor exposures, fundamentals, market data, and portfolio holdings
- **Factor Model Integration**: Native factor-based attribution and risk analysis with statistical validation throughout
- **Systematic Research Framework**: AI-powered integration of quantitative factor analysis with qualitative fundamental research  
- **Advanced Statistical Analysis**: Comprehensive significance testing, confidence intervals, and model validation capabilities

## Scenario 8: Sales Advisor - Client Reporting & Templates ✅ PHASE 4

### Business Context Setup

**Persona**: James Mitchell, Client Relationship Manager at Snowcrest Asset Management  
**Business Challenge**: Client relationship managers need to produce professional, compliant, and compelling client reports that integrate performance data with approved messaging templates and investment philosophy. Traditional processes require manual data gathering, template formatting, compliance review, and brand alignment, consuming significant time and introducing formatting inconsistencies.  
**Value Proposition**: AI-powered client reporting that automatically combines portfolio analytics with approved templates, investment philosophy, and compliance language to generate professional, relationship-building client communications in minutes.

**Agent**: `sales_advisor`  
**Data Available**: Portfolio performance data, sales report templates, investment philosophy documents, compliance policies, brand messaging guidelines

### Demo Flow

**Scene Setting**: James needs to prepare a monthly client report for a key institutional client with their SAM Technology & Infrastructure portfolio, ensuring professional presentation with proper compliance language and brand messaging.

#### Step 1: Portfolio Performance Foundation
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

#### Step 2: Template Integration and Professional Formatting
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

#### Step 3: Investment Philosophy and Brand Integration
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

#### Step 4: Compliance Review and Final Document
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

### Scenario Wrap-up

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
