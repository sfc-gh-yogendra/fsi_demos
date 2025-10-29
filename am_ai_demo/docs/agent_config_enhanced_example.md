# Agent Configuration Enhanced Example

Complete reference template showing all best practices for Cortex Agent configuration in Snowflake Intelligence.

**Purpose**: This document serves as a comprehensive reference for configuring production-quality Cortex Agents with detailed tool descriptions, business context, workflows, error handling, and structured response patterns.

**Related Documentation**:
- `docs/agents_setup.md` - All 7 SAM demo agent configurations
- `.cursor/rules/agent-config.mdc` - Internal configuration patterns
- `research/FINAL_ Definitive Guide for Building Cortex Agents.md` - Snowflake best practices

## Table of Contents

1. [Agent Metadata](#agent-metadata)
2. [Response Instructions](#response-instructions)
3. [Tool Configurations](#tool-configurations)
4. [Planning Instructions](#planning-instructions)
5. [Validation Checklist](#validation-checklist)

---

## Agent Metadata

### Agent Name
`example_agent`

**Guidelines**:
- Use lowercase with underscores
- Descriptive of agent's primary function
- Unique within namespace

### Display Name
Example Agent

**Guidelines**:
- Title case, human-readable
- 2-4 words maximum
- Clear role indication

### Agent Description
Expert AI assistant for [persona] focused on [primary capabilities]. Provides [key value propositions] to help [target users] [achieve specific outcomes]. Integrates [data sources] with [analytical capabilities] for [business context].

**Guidelines**:
- 2-3 sentences maximum
- Clear persona and capabilities
- Specific value proposition
- Business context included

---

## Response Instructions

```
Style:
- Tone: [Specific tone for persona, e.g., "Professional, data-driven, action-oriented"]
- Lead With: [Answer pattern, e.g., "Direct answer first, then supporting analysis"]
- Terminology: [Domain-specific terms, e.g., "UK English, financial terminology"]
- Precision: [Detail level, e.g., "Percentages to 1 decimal, exact dates"]
- Limitations: [How to communicate gaps, e.g., "State data limitations clearly"]
- [Domain] Focus: [Domain-specific emphasis, e.g., "Actionable insights, compliance focus"]

Presentation:
- Tables: Use for [specific criteria with threshold, e.g., ">4 rows, comparisons"]
- Charts: Bar charts for [criteria], line charts for [criteria]
- Single Metrics: Format as "[pattern example]"
- Flags/Indicators: Use [specific symbols] for [specific conditions]
- Data Freshness: Always include "[pattern example]"

[Domain-Specific Formatting]:
- [Special formatting rule 1 with example]
- [Special formatting rule 2 with example]
- [Special formatting rule 3 with example]

Response Structure for [Common Query Type 1]:
Template: "[Element 1] + [Element 2] + [Element 3] + [Element 4]"

Example:
User: "[Example question]"
Response: "[Complete example response showing all elements]

[Element 1 with data]:
- [Bullet point 1]
- [Bullet point 2]

[Element 2 with table]:
| Column 1 | Column 2 | Column 3 |
|---|---|---|
| Data 1 | Data 2 | Data 3 |

[Element 3 with analysis]:
[Paragraph with insights]

[Element 4 with recommendations]:
[Actionable next steps]"

Response Structure for [Common Query Type 2]:
Template: "[Different structure for different query type]"

Example:
User: "[Example question 2]"
Response: "[Complete example response 2]"
```

**Key Principles**:
- Structure with clear subsections (Style, Presentation, Response Structures)
- Provide specific patterns, not general guidance
- Include complete example responses for common query types
- Use domain-specific terminology and formatting rules
- Show exact formatting patterns with examples

---

## Tool Configurations

### Tool 1: [tool_name] (Cortex Analyst)

- **Type**: Cortex Analyst
- **Semantic View**: `DATABASE.SCHEMA.SEMANTIC_VIEW_NAME`
- **Description**:
```
[One-sentence purpose statement describing what this tool analyzes]

Data Coverage:
- Historical: [time range of historical data, e.g., "12 months of transaction history"]
- Current: [update frequency, e.g., "Daily at 4 PM ET market close"]
- Sources: [underlying data tables, e.g., "DIM_SECURITY, FACT_POSITION_DAILY_ABOR"]
- Records: [approximate scale, e.g., "14,000+ securities, 27,000+ holdings"]
- Refresh: [refresh schedule with timezone, e.g., "Daily at 4 PM ET with 2-hour lag"]

Semantic Model Contents:
- Tables: [table list with brief purpose]
- Key Metrics: [primary metrics available]
- Time Dimensions: [date columns and granularity]
- Common Filters: [frequently used dimension filters]

When to Use:
- [Specific use case 1 with example query pattern]
- [Specific use case 2 with example query pattern]
- [Specific use case 3 with example query pattern]
- Questions like: "[example question 1]", "[example question 2]"

When NOT to Use:
- [Anti-pattern 1 with alternative: "Use [other_tool] instead"]
- [Anti-pattern 2 with alternative: "Use [other_tool] instead"]
- [Anti-pattern 3 with explanation of limitation]

Query Best Practices:
1. [Query guideline 1 with good/bad examples]:
   ✅ [Good query example]
   ❌ [Bad query example with reason]

2. [Query guideline 2 with good/bad examples]:
   ✅ [Good query example]
   ❌ [Bad query example with reason]

3. [Query guideline 3 with good/bad examples]:
   ✅ [Good query example]
   ❌ [Bad query example with reason]
```

### Tool 2: [tool_name] (Cortex Search)

- **Type**: Cortex Search
- **Service**: `DATABASE.SCHEMA.SERVICE_NAME`
- **ID Column**: `DOCUMENT_ID`
- **Title Column**: `DOCUMENT_TITLE`
- **Description**: |
  [One-sentence purpose statement describing document search capability]
  
  Data Sources:
  - Document Types: [types of documents included]
  - Update Frequency: [how often new documents added]
  - Historical Range: [typical age range of documents]
  - Index Freshness: [lag between document creation and searchability]
  - Typical Count: [approximate number of documents]
  
  When to Use:
  - Questions about [domain] requiring document content
  - [Specific use case 1 with example]
  - [Specific use case 2 with example]
  - Queries like: "[example question]"
  
  When NOT to Use:
  - [Anti-pattern 1 with alternative tool]
  - [Anti-pattern 2 with alternative tool]
  - [Anti-pattern 3 with explanation]
  
  Search Query Best Practices:
  1. [Search guideline 1 with good/bad examples]:
     ✅ [Good search query example]
     ❌ [Bad search query with reason]
  
  2. [Search guideline 2 with good/bad examples]:
     ✅ [Good search query example]
     ❌ [Bad search query with reason]
  
  3. [Search guideline 3]:
     - [Specific guidance for handling low relevance]
     - [Guidance for handling no results]
     - [Guidance for rephrasing strategies]

**Key Principles for Tool Descriptions**:
- Data Coverage section is mandatory for Cortex Analyst tools
- "When to Use" must have 3-4 specific examples with query patterns
- "When NOT to Use" must specify alternative tools
- Query/Search Best Practices must show ✅/❌ examples
- All guidance must be specific and actionable

---

## Planning Instructions

```
Business Context:

Organization Context:
- [Organization name and type, e.g., "Company X is a [industry] firm"]
- [Key operational metrics, e.g., "Manages $XB across N strategies"]
- [Regulatory framework, e.g., "SEC-regulated with quarterly reviews"]
- [Data operations, e.g., "Data refreshes daily at market close"]

Key Business Terms:
- [Term 1]: [Definition with specific thresholds/values]
  Example: "[Business rule with exact threshold]"
- [Term 2]: [Definition with specific thresholds/values]
  Example: "[Business rule with exact threshold]"
- [Term 3]: [Definition with specific process]
  Example: "[Business process description]"

[Domain] Categories:
- [Category 1]: [Description with key characteristics]
  Example: "[Category example with defining features]"
- [Category 2]: [Description with key characteristics]
  Example: "[Category example with defining features]"

1. Analyze user query to identify [domain-specific] category:
   - [Category 1 description]
   - [Category 2 description]
   - [Category 3 description]

2. Tool Selection by Query Type:

   [Query Type 1]:
   ✅ Use [tool_name] for [specific purpose]
   ✅ Then [tool_name_2] for [specific purpose]
   ❌ Don't [anti-pattern description]

   [Query Type 2]:
   ✅ Use [different tool] for [specific purpose]
   ✅ Use [complementary tool] for [specific purpose]
   ❌ Don't [anti-pattern description]

3. [Domain-Specific] Approach:
   - Step 1: [First action with specific tool]
   - Step 2: [Second action using Step 1 results]
   - Step 3: [Third action for synthesis]

Complete Workflow Examples:

Workflow 1: [Workflow Name]
Trigger: User asks "[example question pattern]"

Step-by-Step Execution:
1. [First Action with Specific Tool]
   Tool: [tool_name]
   Query/Search: "[exact query pattern to send to tool]"
   Extract from results: [specific information to capture]
   Why this step: [business justification]

2. [Second Action with Specific Tool]
   Tool: [tool_name_2]
   Query/Search: "[exact query pattern, incorporating Step 1 results]"
   Use context from Step 1: [how to use previous results]
   Extract from results: [specific information to capture]

3. [Third Action if needed]
   Tool: [tool_name_3]
   Context: [what context from previous steps to include]
   Query/Search: "[exact query pattern]"
   Extract from results: [specific information to capture]

4. Synthesize Final Response:
   - [Element 1]: From Step [X] results
   - [Element 2]: From Step [Y] results
   - [Element 3]: Calculated from Steps [X] and [Y]
   - Format as: [specific format with example]
   - Include: [required elements like thresholds, citations, warnings]

Example Complete Interaction:
User Question: "[realistic example question]"
Agent Response: "[complete synthesized response showing all elements with tables, calculations, and recommendations]"

Workflow 2: [Another Common Workflow]
Trigger: User asks "[different example question pattern]"

[Repeat same structure as Workflow 1]

Error Handling and Edge Cases:

Scenario 1: [Error Condition]
Detection: [How to identify this error has occurred]
Recovery Steps:
  1. [First recovery action]
  2. [Second recovery action if first fails]
  3. [Final fallback action]
User Message: "[Exact message pattern to provide user]"
Alternative: [What to suggest instead or how to rephrase]

Scenario 2: [Different Error Condition]
Detection: [How to identify this error]
Recovery Steps: [List of recovery actions]
User Message: "[Exact message pattern]"
Alternative: [Alternative approach]

[Continue for 3-5 common error scenarios]
```

**Key Principles for Planning Instructions**:
- Business Context section comes first with exact thresholds
- Tool Selection must specify query patterns that trigger each tool
- Include 2-3 complete workflow examples with step-by-step tool sequences
- Error Handling covers 3-5 common scenarios
- All guidance is specific and actionable, not general

---

## Validation Checklist

Use this checklist to validate agent configurations before deployment:

### Agent Metadata
- [ ] Agent name is lowercase with underscores
- [ ] Display name is clear and concise (2-4 words)
- [ ] Description includes persona, capabilities, and value proposition
- [ ] Description is 2-3 sentences

### Response Instructions
- [ ] Style section includes tone, lead-with pattern, terminology, precision
- [ ] Presentation section specifies table/chart criteria with thresholds
- [ ] Domain-specific formatting rules included where applicable
- [ ] 2-3 Response Structure templates provided
- [ ] Each Response Structure has complete example

### Tool Configurations
#### For Each Cortex Analyst Tool:
- [ ] Data Coverage section with 5 elements (historical, current, sources, records, refresh)
- [ ] Semantic Model Contents described
- [ ] "When to Use" has 3-4 specific examples
- [ ] "When NOT to Use" specifies alternative tools
- [ ] Query Best Practices has 3+ ✅/❌ examples

#### For Each Cortex Search Tool:
- [ ] Data Sources section with 5 elements
- [ ] "When to Use" has 3-4 specific examples
- [ ] "When NOT to Use" specifies alternative tools
- [ ] Search Query Best Practices has 3+ ✅/❌ examples
- [ ] Relevance handling guidance included

### Planning Instructions
- [ ] Business Context section with Organization Context, Key Terms, Categories
- [ ] Tool Selection specifies query patterns with ✅/❌ examples
- [ ] 2-3 Complete Workflow Examples with step-by-step sequences
- [ ] Each workflow includes trigger, steps, synthesis, and complete example
- [ ] Error Handling covers 3-5 common scenarios
- [ ] Each error scenario has detection, recovery, message, alternative

### Overall Quality
- [ ] No generic guidance - all instructions are specific
- [ ] Domain terminology used consistently
- [ ] All thresholds and metrics explicitly defined
- [ ] All examples are realistic and complete
- [ ] Formatting follows established patterns

---

## Common Pitfalls to Avoid

### Tool Description Pitfalls

❌ **Generic, Vague Descriptions**
```yaml
Bad: "Gets data from the database"
```

✅ **Specific, Detailed Descriptions**
```yaml
Good: "Analyzes portfolio holdings with 12 months history, 14,000+ securities, 
daily refresh at 4 PM ET. Use for holdings questions, concentration analysis, 
sector breakdowns."
```

---

❌ **Missing "When NOT to Use"**
```yaml
Bad: Tool description only lists capabilities
```

✅ **Explicit Anti-Patterns with Alternatives**
```yaml
Good: "When NOT to Use:
- Real-time data (data is EOD only, use market feed)
- Implementation costs (use implementation_analyzer)"
```

### Orchestration Pitfalls

❌ **Assumed Business Context**
```yaml
Bad: "Check for violations"
```

✅ **Explicit Business Rules**
```yaml
Good: "Business Context:
- Concentration Threshold: 6.5% warning, 7.0% breach per policy
- Check positions against explicit thresholds from policy documents"
```

---

❌ **Implicit Workflow Sequences**
```yaml
Bad: "Use appropriate tools"
```

✅ **Step-by-Step Workflows**
```yaml
Good: "Workflow: Concentration Analysis
1. Retrieve thresholds from search_policy
2. Get holdings from quantitative_analyzer
3. Apply thresholds and flag positions
4. Synthesize with recommendations"
```

### Response Instructions Pitfalls

❌ **General Style Guidance**
```yaml
Bad: "Be professional"
```

✅ **Specific Format Rules**
```yaml
Good: "Style:
- Lead With: Direct answer first
- Tables: Use for >4 rows
- Format: 'Weight is 8.2% (⚠️ exceeds 6.5%) as of 31 Dec 2024'"
```

---

## Summary

This enhanced example demonstrates all best practices for Cortex Agent configuration:

1. **Comprehensive Tool Descriptions**: Data Coverage, When to Use/NOT, Query Best Practices
2. **Business Context**: Organization details, exact thresholds, domain categories
3. **Complete Workflows**: Multi-step processes with tool sequences and examples
4. **Error Handling**: Common scenarios with recovery steps and user messages
5. **Structured Responses**: Style, Presentation, and complete example templates

Use this template as a reference when configuring new agents or enhancing existing configurations.

