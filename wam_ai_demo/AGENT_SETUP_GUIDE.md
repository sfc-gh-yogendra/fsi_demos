# WAM AI Demo - Snowflake Intelligence Agent Setup Guide

This guide provides complete step-by-step instructions for configuring the three AI agents in Snowflake Intelligence after running the WAM AI Demo build.

## Prerequisites

### 1. Verify Demo Build Completion
Ensure the main build completed successfully with validation:
```bash
# Run full build with validation
python main.py --mode replace_all

# Or run validation only
python main.py --validate-only
```

**Expected Output:**
```
✅ Connected to Snowflake
📊 Checking Semantic Views...
  ✅ CLIENT_FINANCIALS_SV
  ✅ CLIENT_INTERACTIONS_SV
🔍 Checking Search Services...
  ✅ COMMUNICATIONS_SEARCH
  ✅ RESEARCH_SEARCH
  ✅ REGULATORY_SEARCH
📋 Checking Data Content...
  ✅ Positions: 6 records
  ✅ Communications: 3 records
  ✅ Research: 3 records
  ✅ Regulatory: 2 records
🎯 Checking Golden Ticker Coverage...
  ✅ AAPL: Research content available
  ✅ MSFT: Research content available
  ✅ NVDA: Research content available
```

### 2. Access Snowflake Intelligence
1. Open Snowsight in your web browser
2. Navigate to **Projects** → **Snowflake Intelligence**
3. Ensure you have the necessary permissions:
   - `CREATE AGENT` privilege
   - Access to the `WAM_AI_DEMO` database
   - `USAGE` privilege on the `WAM_AI_CORTEX_WH` warehouse

### 3. Required Database Objects
Before creating agents, verify these objects exist in your Snowflake account:
- **Database**: `WAM_AI_DEMO`
- **Schemas**: `WAM_AI_DEMO.AI`, `WAM_AI_DEMO.CURATED`
- **Semantic Views**: `CLIENT_FINANCIALS_SV`, `CLIENT_INTERACTIONS_SV`
- **Search Services**: `COMMUNICATIONS_SEARCH`, `RESEARCH_SEARCH`, `REGULATORY_SEARCH`

## Agent Configuration

### Agent 1: advisor_copilot (Wealth Manager)

#### Step 1: Create Agent
1. Click **"Create Agent"** in Snowflake Intelligence
2. **Agent Configuration**:
   - **Agent Name**: `advisor_copilot`
   - **Display Name**: `Wealth Advisory CoPilot`
   - **Description**: `Expert CoPilot for wealth managers providing comprehensive client insights by combining portfolio analytics with communication history and research intelligence. Your intelligent partner for superior client relationship management.`
   - **Orchestration Model**: `Claude 4`

#### Step 2: Add Tools (in this exact order)

**Tool 1: cortex_analyst_client_financials**
- **Type**: Cortex Analyst
- **Name**: `cortex_analyst_client_financials`
- **Semantic View**: `WAM_AI_DEMO.AI.CLIENT_FINANCIALS_SV`
- **Description**: 
  ```
  Use for portfolio analytics, holdings analysis, sector breakdowns, performance metrics, and quantitative calculations about client portfolios and positions.
  ```

**Tool 2: cortex_analyst_client_interactions**
- **Type**: Cortex Analyst
- **Name**: `cortex_analyst_client_interactions`
- **Semantic View**: `WAM_AI_DEMO.AI.CLIENT_INTERACTIONS_SV`
- **Description**: 
  ```
  Use for analyzing client communication patterns, contact frequency, channel preferences, and interaction history metrics.
  ```

**Tool 3: search_communications**
- **Type**: Cortex Search
- **Name**: `search_communications`
- **Service**: `WAM_AI_DEMO.AI.COMMUNICATIONS_SEARCH`
- **ID Column**: `COMMUNICATION_ID`
- **Title Column**: `TITLE`
- **Description**: 
  ```
  Search client communications including emails, call transcripts, and meeting notes. Use for finding client preferences, concerns, or past discussions.
  ```

**Tool 4: search_research**
- **Type**: Cortex Search
- **Name**: `search_research`
- **Service**: `WAM_AI_DEMO.AI.RESEARCH_SEARCH`
- **ID Column**: `DOCUMENT_ID`
- **Title Column**: `TITLE`
- **Description**: 
  ```
  Search research reports and analyst coverage. Use for finding investment opinions, ratings, and market commentary on specific securities.
  ```

**Tool 5: search_planning**
- **Type**: Cortex Search
- **Name**: `search_planning`
- **Service**: `WAM_AI_DEMO.AI.PLANNING_SEARCH`
- **ID Column**: `DOCUMENT_ID`
- **Title Column**: `TITLE`
- **Description**: 
  ```
  Search financial planning documents, investment policy statements, and client goal documentation. Use for understanding client objectives, life events, and strategic planning context.
  ```

#### Step 3: Planning Instructions
Copy and paste this text into the Planning Instructions field:
```
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
   - search_planning: Financial plans, investment policy statements, client goals, life event planning
5. For planning and goal questions: Use search_planning for:
   - Client financial plans, investment policy statements, goal documentation
   - Life event planning, retirement timelines, education funding strategies
   - Risk tolerance documentation, investment constraints, strategic objectives
6. For thematic questions: 
   - Use search_research for ESG content, sustainability reports, carbon neutrality analysis
   - Combine with cortex_analyst_client_financials to analyze portfolio exposure to themes
7. For comprehensive advisory: Combine portfolio data with planning documents to assess:
   - Goal progress and timeline alignment
   - IPS compliance and allocation drift
   - Life event impacts on strategic planning
8. For mixed questions: Use appropriate analyst tool first, then search tools with results as context
9. Always synthesize multiple tool outputs into coherent response
10. If user requests charts/visualizations, use data_to_chart tool
```

#### Step 4: Response Instructions
Copy and paste this text into the Response Instructions field:
```
You are a professional Wealth Advisory CoPilot. As an intelligent partner to wealth managers, your responses should be:
- Concise and data-driven, presented in clear, easy-to-read format using markdown
- Never provide financial advice or make promissory statements
- Always refer to data as being 'according to our records'
- Cite document sources with type and date when referencing qualitative content
- Focus on actionable insights and client relationship implications
- Use professional, collaborative tone as a trusted advisor partner
- When discussing ESG or sustainability topics, reference specific metrics and commitments
- Highlight thematic investment opportunities (Carbon Negative Leaders, AI Innovation, ESG Leaders)
- Support wealth managers in delivering superior client experiences through intelligent insights
```

#### Step 5: Test advisor_copilot
After creating the agent, test with these client-focused queries:

**Test Query 1**: `"Show me the total market value by portfolio"`
- **Expected**: Agent should use cortex_analyst_client_financials to display portfolio breakdown with market values
- **Validates**: Basic Cortex Analyst functionality

**Test Query 2**: `"Search for communications about AAPL"`
- **Expected**: Agent should use search_communications to find Apple-related client discussions
- **Validates**: Cortex Search functionality

**Test Query 3**: `"What research do we have on MSFT performance?"`
- **Expected**: Agent should use search_research to find Microsoft research documents
- **Validates**: Multi-tool research search capability

**Test Query 4**: `"I have a meeting with Sarah Johnson. Please prepare a briefing."`
- **Expected**: Agent should combine portfolio data with communication history for comprehensive client briefing
- **Validates**: Multi-tool integration and client relationship management

**Test Query 5**: `"What are her financial goals according to her planning documents?"`
- **Expected**: Agent should use search_planning to find client's documented financial objectives and timelines
- **Validates**: Planning document search and goal analysis capabilities

---

### Agent 2: analyst_copilot (Portfolio Manager)

#### Step 1: Create Agent
1. Click **"Create Agent"** in Snowflake Intelligence
2. **Agent Configuration**:
   - **Agent Name**: `analyst_copilot`
   - **Display Name**: `Portfolio Analysis CoPilot`
   - **Description**: `Expert CoPilot for portfolio managers providing quantitative analysis, research synthesis, and investment insights across structured and unstructured data sources. Your intelligent partner for superior investment decision-making.`
   - **Orchestration Model**: `Claude 4`

#### Step 2: Add Tools

**Tool 1: cortex_analyst_client_financials**
- **Type**: Cortex Analyst
- **Name**: `cortex_analyst_client_financials`
- **Semantic View**: `WAM_AI_DEMO.AI.CLIENT_FINANCIALS_SV`
- **Description**: 
  ```
  Use for quantitative analysis of portfolio data, fund holdings, market metrics, performance calculations, and financial ratios. Can calculate exposures and generate charts.
  ```

**Tool 2: search_research**
- **Type**: Cortex Search
- **Name**: `search_research`
- **Service**: `WAM_AI_DEMO.AI.RESEARCH_SEARCH`
- **ID Column**: `DOCUMENT_ID`
- **Title Column**: `TITLE`
- **Description**: 
  ```
  Search research reports, analyst coverage, and market commentary. Use for investment thesis development and qualitative analysis.
  ```

**Tool 3: search_planning**
- **Type**: Cortex Search
- **Name**: `search_planning`
- **Service**: `WAM_AI_DEMO.AI.PLANNING_SEARCH`
- **ID Column**: `DOCUMENT_ID`
- **Title Column**: `TITLE`
- **Description**: 
  ```
  Search financial planning documents and investment policy statements. Use for understanding client strategic objectives and investment constraints when making portfolio decisions.
  ```

#### Step 3: Planning Instructions
```
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
4. For planning context: Use search_planning for:
   - Investment policy statement guidelines and constraints
   - Client strategic objectives and investment goals
   - Asset allocation targets and rebalancing guidelines
   - Risk tolerance and investment horizon considerations
5. For ESG/sustainability analysis:
   - Search for ESG research documents and sustainability reports
   - Analyze portfolio exposure to high ESG-scored securities
   - Identify carbon negative investment opportunities
6. For investment decisions: Combine portfolio analytics with planning documents to ensure:
   - Compliance with IPS guidelines and allocation targets
   - Alignment with documented client objectives
   - Adherence to stated risk tolerance and constraints
7. For complex queries spanning multiple domains, use tools systematically
8. Generate charts and visualizations when requested or when they enhance understanding
9. Always synthesize findings from multiple sources into investment-focused insights
```

#### Step 4: Response Instructions
```
You are a professional Portfolio Analysis CoPilot. As an intelligent partner to portfolio managers, your responses must be:
- Analytical, precise, and objective
- Present data using tables where appropriate
- Summarize research findings without adding personal opinions
- Cite sources (e.g., 'According to the Q2 earnings transcript...')
- Focus on investment implications and portfolio impact
- Use quantitative language and metrics appropriate for portfolio management
- When discussing ESG factors, provide specific scores, commitments, and timelines
- Highlight thematic investment opportunities and their portfolio fit
- Support portfolio managers in making superior investment decisions through intelligent analysis
```

#### Step 5: Test analyst_copilot
Test with these investment-focused queries:

**Test Query 1**: `"What is the total market value across all portfolios?"`
- **Expected**: Agent should use cortex_analyst_client_financials for firm-wide portfolio analytics
- **Validates**: Basic quantitative analysis capability

**Test Query 2**: `"Find research on AAPL and MSFT"`
- **Expected**: Agent should use search_research to locate Apple and Microsoft research documents
- **Validates**: Research discovery functionality

**Test Query 3**: `"What ESG research do we have on technology companies?"`
- **Expected**: Agent should search for ESG-related content and summarize findings by sector
- **Validates**: Thematic research analysis and ESG capabilities

**Test Query 4**: `"Is our current portfolio allocation within the guidelines specified in the client's IPS?"`
- **Expected**: Agent should use search_planning to find IPS allocation targets and compare with current portfolio positions
- **Validates**: Planning document integration and compliance analysis

---

### Agent 3: compliance_copilot (Compliance)

#### Step 1: Create Agent
1. Click **"Create Agent"** in Snowflake Intelligence
2. **Agent Configuration**:
   - **Agent Name**: `compliance_copilot`
   - **Display Name**: `Compliance CoPilot`
   - **Description**: `Expert CoPilot for compliance officers providing comprehensive surveillance, regulatory analysis, and risk monitoring across communications and client interactions. Your intelligent partner for superior risk management and regulatory adherence.`
   - **Orchestration Model**: `Claude 4`

#### Step 2: Add Tools

**Tool 1: search_communications**
- **Type**: Cortex Search
- **Name**: `search_communications`
- **Service**: `WAM_AI_DEMO.AI.COMMUNICATIONS_SEARCH`
- **ID Column**: `COMMUNICATION_ID`
- **Title Column**: `TITLE`
- **Description**: 
  ```
  Search and analyze all electronic communications for potential compliance violations, such as promising returns, sharing PII, or client complaints.
  ```

**Tool 2: search_regulatory**
- **Type**: Cortex Search
- **Name**: `search_regulatory`
- **Service**: `WAM_AI_DEMO.AI.REGULATORY_SEARCH`
- **ID Column**: `DOCUMENT_ID`
- **Title Column**: `TITLE`
- **Description**: 
  ```
  Search regulatory documents and compliance rules. Use for finding specific regulations, compliance requirements, or policy guidance.
  ```

#### Step 3: Planning Instructions
```
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
5. For systematic surveillance, analyze patterns across multiple communications
6. Always recommend human review for potential violations
7. Focus on factual findings and regulatory compliance
```

#### Step 4: Response Instructions
```
You are a professional Compliance CoPilot. As an intelligent partner to compliance officers, your tone must be:
- Formal and factual without ambiguity
- Present findings clearly stating facts and potential policy violations
- Reference specific regulations or rules when identifying issues
- Always recommend review by a human compliance officer
- Focus on risk mitigation and regulatory adherence
- Use compliance terminology and cite relevant regulations
- Never make final compliance determinations - flag for human review
- When reviewing ESG-related content, verify claims against source documents
- Flag any potential greenwashing or unsubstantiated sustainability claims
- Support compliance officers in maintaining superior risk management and regulatory adherence
```

#### Step 5: Test compliance_copilot
Test with these compliance-focused queries:

**Test Query 1**: `"Search for any communications containing performance guarantees"`
- **Expected**: Agent should use search_communications to scan for promissory language violations
- **Validates**: Compliance surveillance functionality

**Test Query 2**: `"Find FINRA regulations about client communications"`
- **Expected**: Agent should use search_regulatory to locate relevant regulatory guidance
- **Validates**: Regulatory knowledge base search

**Test Query 3**: `"Are there any ESG-related compliance concerns in recent communications?"`
- **Expected**: Agent should search for potential greenwashing claims or unsubstantiated ESG statements
- **Validates**: ESG compliance monitoring and risk identification

## Demo Scenarios (3-4 Step Workflows)

### Advisor AI Demo Scenario: Client Meeting Preparation
**Scenario**: Preparing for a meeting with client Sarah Jones

1. **User**: "I have a meeting with Sarah Jones in 30 minutes. Please prepare a full briefing."
   - **Expected**: Agent uses cortex_analyst_client_financials + search_communications to create comprehensive client briefing
   - **Demo Value**: Shows unified client view combining portfolio data with communication history

2. **User**: "What are her top 5 holdings and any recent news about them?"
   - **Expected**: Agent uses cortex_analyst_client_financials for holdings, then search_research for related news
   - **Demo Value**: Demonstrates seamless pivot from structured to unstructured data

3. **User**: "Search for any communications where she mentioned Apple or investment concerns"
   - **Expected**: Agent uses search_communications to find client-specific discussions about Apple
   - **Demo Value**: Shows personalized communication intelligence and client relationship insights

4. **User**: "Based on this analysis, what should be my key talking points for the meeting?"
   - **Expected**: Agent synthesizes portfolio performance, holdings, communications, and research into actionable meeting agenda
   - **Demo Value**: Demonstrates AI-powered meeting preparation and personalized relationship management

### Analyst AI Demo Scenario: Investment Research
**Scenario**: Conducting investment analysis and research synthesis

1. **User**: "What is our total exposure across all portfolios?"
   - **Expected**: Agent uses cortex_analyst_client_financials for portfolio analytics
   - **Demo Value**: Shows firm-wide risk and exposure analysis

2. **User**: "Find research on technology companies like AAPL and MSFT"
   - **Expected**: Agent uses search_research to locate relevant research documents
   - **Demo Value**: Demonstrates research discovery and document intelligence

3. **User**: "What does the research say about ESG and sustainability?"
   - **Expected**: Agent searches for ESG-related content and summarizes findings
   - **Demo Value**: Shows thematic research analysis and trend identification

4. **User**: "How should this influence our portfolio strategy?"
   - **Expected**: Agent synthesizes research findings with portfolio data for investment insights
   - **Demo Value**: Demonstrates AI-augmented investment decision support

### Guardian AI Demo Scenario: Compliance Monitoring
**Scenario**: Monitoring communications for compliance violations

1. **User**: "Search for any communications that mention performance guarantees"
   - **Expected**: Agent uses search_communications to scan for compliance risks
   - **Demo Value**: Shows automated compliance surveillance capability

2. **User**: "What do FINRA regulations say about communication standards?"
   - **Expected**: Agent uses search_regulatory to find relevant FINRA rules
   - **Demo Value**: Demonstrates regulatory knowledge base search

3. **User**: "Are there any other compliance concerns in recent communications?"
   - **Expected**: Agent performs broader compliance surveillance search
   - **Demo Value**: Shows comprehensive risk monitoring

4. **User**: "What action should be taken based on these findings?"
   - **Expected**: Agent provides compliance recommendations with regulatory citations
   - **Demo Value**: Demonstrates AI-powered compliance guidance and risk mitigation

## Troubleshooting

### Common Setup Issues

**Agent Creation Fails:**
- Verify you have permissions to create agents in Snowflake Intelligence
- Check that you're in the correct Snowflake account and database
- Ensure all prerequisite AI components exist

**Tool Configuration Errors:**
- **Semantic View Not Found**: Run `SHOW SEMANTIC VIEWS IN WAM_AI_DEMO.AI;` to verify views exist
- **Search Service Not Found**: Run `SHOW CORTEX SEARCH SERVICES IN WAM_AI_DEMO.AI;` to verify services exist
- **Column Name Errors**: Use exact column names: `COMMUNICATION_ID`, `DOCUMENT_ID`, `TITLE`

**Agent Not Responding:**
- Test individual tools first before testing full scenarios
- Verify data exists in underlying tables
- Check warehouse is active and has sufficient size
- Ensure the `WAM_AI_CORTEX_WH` warehouse is running (agents require active warehouse)
- Verify Cortex services are enabled in your Snowflake account

**Tool-Specific Issues:**
- **Cortex Analyst Tools**: Ensure semantic views return data when queried directly
- **Cortex Search Tools**: Test search services with `SNOWFLAKE.CORTEX.SEARCH_PREVIEW()` function
- **Missing Data**: If agents report no data, verify the demo build completed successfully
- **Permission Errors**: Ensure agent service account has access to all `WAM_AI_DEMO` objects

### Current Implementation Notes

**Phase 2 Enhancements (Included)**: The demo now includes advanced ESG and thematic capabilities:
- ✅ **Thematic Watchlists**: Carbon Negative Leaders, AI Innovation, ESG Leaders
- ✅ **Enhanced ESG Content**: 18 additional ESG/sustainability documents in research corpus
- ✅ **Portfolio Analytics**: Exposure analysis to watchlist themes
- ✅ **ESG Compliance**: Greenwashing detection and sustainability verification

**Table Structure Status**: The current implementation has a known limitation where IDENTITY primary keys are not fully implemented due to Snowpark DataFrame behavior. However, the demo is fully functional with:
- ✅ **Working semantic views**: CLIENT_FINANCIALS_SV and CLIENT_INTERACTIONS_SV
- ✅ **Working search services**: All 3 services operational with ESG content
- ✅ **Real data integration**: 2,539 authentic securities + 22,974 market records
- ✅ **Business scenarios**: All agent workflows validated including ESG themes

### Verification Queries

Run these queries in Snowsight to verify components before agent setup:

```sql
-- Check semantic views exist and work
SHOW SEMANTIC VIEWS IN WAM_AI_DEMO.AI;

SELECT * FROM SEMANTIC_VIEW(
    WAM_AI_DEMO.AI.CLIENT_FINANCIALS_SV
    METRICS TOTAL_MARKET_VALUE
    DIMENSIONS PORTFOLIOID
) LIMIT 5;

-- Check search services exist and work
SHOW CORTEX SEARCH SERVICES IN WAM_AI_DEMO.AI;

SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'WAM_AI_DEMO.AI.COMMUNICATIONS_SEARCH',
    '{"query": "portfolio", "limit": 1}'
);

SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'WAM_AI_DEMO.AI.RESEARCH_SEARCH',
    '{"query": "AAPL", "limit": 1}'
);

SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'WAM_AI_DEMO.AI.REGULATORY_SEARCH',
    '{"query": "FINRA", "limit": 1}'
);
```

## Demo Presentation Tips

### Key Talking Points

**Unified Data Platform:**
- "Notice how the agent seamlessly combines portfolio analytics with communication history and research intelligence"
- "This demonstrates Snowflake's unique ability to unify structured financial data with unstructured documents"

**AI-Powered Insights:**
- "The agent automatically identifies relevant research based on portfolio holdings"
- "Communication patterns and client preferences are surfaced without manual searching"

**Compliance and Governance:**
- "All interactions are monitored for compliance risks using AI-powered surveillance"
- "Regulatory knowledge is instantly accessible and properly cited"

### Demo Flow Recommendations

1. **Start with Advisor AI**: Most relatable for wealth management audiences
2. **Show Data Integration**: Highlight how portfolio data connects to communications and research
3. **Demonstrate Search**: Show the power of finding relevant information across thousands of documents
4. **End with Compliance**: Emphasize governance and risk management capabilities

### Golden Ticker Strategy

The demo includes these recognizable securities for maximum credibility:
- **AAPL** (Apple Inc.): Technology portfolio anchor
- **MSFT** (Microsoft Corp): ESG and AI theme leader  
- **NVDA** (NVIDIA Corp): AI/semiconductor theme
- **JPM** (JPMorgan Chase): Financial services anchor
- **V** (Visa Inc.): Payment processing leader
- **SAP** (SAP SE): European technology representation

Use these tickers in demo queries as they have guaranteed research content and realistic portfolio positions.

## Quick Reference

### Ready-to-Use Demo Queries

**Portfolio Analysis:**
```
"Show me the total market value by portfolio"
"What are the top holdings by market value?"
"Show me the portfolio weight distribution"
```

**Research and Communications:**
```
"Search for communications about AAPL"
"Find research on MSFT ESG initiatives"
"What research do we have on NVDA performance?"
```

**Compliance Monitoring:**
```
"Search for any communications containing performance guarantees"
"Find FINRA regulations about client communications"
"Are there any compliance concerns in recent communications?"
```

### Agent Capabilities Summary

| CoPilot | Primary Use Case | Key Strengths | Demo Value |
|---------|------------------|---------------|------------|
| **advisor_copilot** | Client relationship management | Portfolio + Communication + Planning synthesis | Meeting preparation, client insights |
| **analyst_copilot** | Investment research | Research discovery + Portfolio analytics + IPS compliance | Investment thesis, market analysis |
| **compliance_copilot** | Compliance monitoring | Communication surveillance + Regulatory search | Risk monitoring, compliance guidance |

## Support

If you encounter issues during setup:
1. Run `python main.py --validate-only` to check component status
2. Verify all prerequisite queries work in Snowsight
3. Check the troubleshooting section above
4. Ensure all agent tools are configured with exact names and descriptions provided
5. Test individual tools before testing full agent scenarios

## Setup Completion Checklist

Before conducting demos, verify you have completed all steps:

### ✅ Prerequisites
- [ ] Demo build completed successfully (`python main.py --mode replace_all`)
- [ ] Validation passed (`python main.py --validate-only`)
- [ ] Snowflake Intelligence access confirmed
- [ ] Required permissions verified (`CREATE AGENT`, database access)

### ✅ Agent Configuration
- [ ] **advisor_copilot** created with 5 tools (2 Cortex Analyst + 3 Cortex Search)
- [ ] **analyst_copilot** created with 3 tools (1 Cortex Analyst + 2 Cortex Search)
- [ ] **compliance_copilot** created with 2 tools (2 Cortex Search)

### ✅ Agent Testing
- [ ] All test queries work for advisor_copilot
- [ ] All test queries work for analyst_copilot
- [ ] All test queries work for compliance_copilot
- [ ] Demo scenarios tested end-to-end

### ✅ Demo Readiness
- [ ] Golden ticker queries prepared (AAPL, MSFT, NVDA, JPM, V, SAP)
- [ ] Demo talking points reviewed
- [ ] Backup queries ready in case of issues

---

**Your WAM CoPilot Demo agents are now ready for customer demonstrations!** 🎉
