# Agent Configuration Checklist

Quality assurance checklist for validating Cortex Agent configurations before deployment.

**Purpose**: Ensure all agent configurations follow best practices and include all required elements for production readiness.

**Related Documentation**:
- `docs/agent_config_enhanced_example.md` - Complete reference template
- `docs/agents_setup.md` - All SAM demo agent configurations
- `.cursor/rules/agent-config.mdc` - Configuration patterns

---

## Quick Start

Use this checklist to validate each agent configuration systematically. Each section corresponds to a major component of agent configuration.

**Validation Process**:
1. Review Agent Metadata
2. Validate Response Instructions
3. Check All Tool Configurations
4. Verify Planning Instructions
5. Test with Sample Queries

---

## 1. Agent Metadata Validation

### Basic Information
- [ ] **Agent Name**: Lowercase with underscores (e.g., `portfolio_copilot`)
- [ ] **Display Name**: Title case, 2-4 words (e.g., "Portfolio Copilot")
- [ ] **Description**: 2-3 sentences covering:
  - [ ] Target persona (e.g., "Expert AI assistant for portfolio managers")
  - [ ] Primary capabilities (e.g., "portfolio analytics, holdings analysis")
  - [ ] Key value proposition (e.g., "instant access to portfolio data")
  - [ ] Business context (e.g., "helps make informed investment decisions")

### Common Mistakes to Avoid
- ❌ Agent name with spaces or capital letters
- ❌ Display name too long (>6 words)
- ❌ Generic description without specific value proposition
- ❌ Missing persona or target user specification

---

## 2. Response Instructions Validation

### Style Section (Required)
- [ ] **Tone**: Specific for persona (not just "professional")
  - Example: "Data-driven, action-oriented for portfolio managers"
- [ ] **Lead With**: Answer pattern specified
  - Example: "Direct answer first, then supporting analysis"
- [ ] **Terminology**: Domain-specific terms defined
  - Example: "UK English, financial terminology, concentration warnings"
- [ ] **Precision**: Detail level specified
  - Example: "Percentages to 1 decimal, exact dates with timezone"
- [ ] **Limitations**: Gap communication pattern
  - Example: "State data limitations clearly, offer alternatives"
- [ ] **Domain Focus**: Specific emphasis area
  - Example: "Actionable insights, compliance adherence"

### Presentation Section (Required)
- [ ] **Tables**: Criteria specified with threshold
  - Example: "Use for >4 rows, comparisons, compliance checks"
- [ ] **Charts**: Specific chart types for specific data
  - Example: "Bar charts for sector allocation, line charts for time series"
- [ ] **Single Metrics**: Exact formatting pattern with example
  - Example: "Weight is 8.2% (⚠️ exceeds 6.5%) as of 31 Dec 2024"
- [ ] **Flags/Indicators**: Specific symbols for specific conditions
  - Example: "🚨 BREACH (>7%), ⚠️ WARNING (6.5-7%), ✅ COMPLIANT"
- [ ] **Data Freshness**: Always-include pattern
  - Example: "As of DD MMM YYYY market close"

### Domain-Specific Formatting (If Applicable)
- [ ] Special formatting rules for domain included
- [ ] Examples provided for each rule
- [ ] Consistent with domain best practices

### Response Structure Templates (Required: 2-3)
For Each Template:
- [ ] **Template Pattern**: Elements listed in order
  - Example: "[Summary] + [Table] + [Analysis] + [Recommendations]"
- [ ] **Complete Example**: Full question and response provided
  - [ ] Example question is realistic
  - [ ] Example response shows all template elements
  - [ ] Proper formatting (tables, bullets, flags)
  - [ ] Includes data freshness
  - [ ] Demonstrates domain terminology

### Common Mistakes to Avoid
- ❌ Generic style guidance ("be professional and helpful")
- ❌ No specific formatting patterns with examples
- ❌ Response structures without complete examples
- ❌ Missing data freshness requirements
- ❌ Inconsistent terminology across sections

---

## 3. Tool Configuration Validation

### For Each Cortex Analyst Tool

#### Basic Information
- [ ] Tool name is descriptive and unique
- [ ] Semantic view path is correct (DATABASE.SCHEMA.VIEW_NAME)
- [ ] Type explicitly stated as "Cortex Analyst"

#### Description Structure (Required)
- [ ] **One-sentence purpose**: Clear, specific capability statement
- [ ] **Data Coverage** (5 required elements):
  - [ ] Historical: Time range with specifics (e.g., "12 months of data")
  - [ ] Current: Update frequency (e.g., "Daily at 4 PM ET")
  - [ ] Sources: Underlying tables listed (e.g., "DIM_SECURITY, FACT_POSITION")
  - [ ] Records: Approximate scale (e.g., "14,000+ securities")
  - [ ] Refresh: Schedule with timezone (e.g., "Daily at 4 PM ET with 2-hour lag")

- [ ] **Semantic Model Contents** (4 elements):
  - [ ] Tables: List with brief purpose
  - [ ] Key Metrics: Primary metrics available
  - [ ] Time Dimensions: Date columns and granularity
  - [ ] Common Filters: Frequently used dimensions

- [ ] **When to Use** (3-4 required examples):
  - [ ] Specific use case 1 with example query
  - [ ] Specific use case 2 with example query
  - [ ] Specific use case 3 with example query
  - [ ] "Questions like:" with 2 example questions

- [ ] **When NOT to Use** (3 required anti-patterns):
  - [ ] Anti-pattern 1 with alternative tool specified
  - [ ] Anti-pattern 2 with alternative tool specified
  - [ ] Anti-pattern 3 with explanation

- [ ] **Query Best Practices** (3+ required):
  - [ ] Each guideline has context
  - [ ] ✅ Good query example provided
  - [ ] ❌ Bad query example with reason provided
  - [ ] Examples are realistic and specific

#### Common Mistakes for Cortex Analyst Tools
- ❌ Generic "Use for data analysis" descriptions
- ❌ Missing Data Coverage section
- ❌ "When NOT to Use" without alternative tools
- ❌ Query examples without ✅/❌ indicators
- ❌ Vague guidelines ("be specific") without examples

### For Each Cortex Search Tool

#### Basic Information
- [ ] Tool name follows `search_{document_type}` pattern
- [ ] Service path is correct (DATABASE.SCHEMA.SERVICE_NAME)
- [ ] ID Column specified (usually `DOCUMENT_ID`)
- [ ] Title Column specified (usually `DOCUMENT_TITLE`)
- [ ] Type explicitly stated as "Cortex Search"

#### Description Structure (Required)
- [ ] **One-sentence purpose**: Clear document search capability

- [ ] **Data Sources** (5 required elements):
  - [ ] Document Types: Types included
  - [ ] Update Frequency: How often documents added
  - [ ] Historical Range: Age range of documents
  - [ ] Index Freshness: Lag from creation to searchability
  - [ ] Typical Count: Approximate number of documents

- [ ] **When to Use** (3-4 required examples):
  - [ ] Specific use case 1 with example
  - [ ] Specific use case 2 with example
  - [ ] Specific use case 3 with example
  - [ ] "Queries like:" with example question

- [ ] **When NOT to Use** (3 required anti-patterns):
  - [ ] Anti-pattern 1 with alternative tool
  - [ ] Anti-pattern 2 with alternative tool
  - [ ] Anti-pattern 3 with explanation

- [ ] **Search Query Best Practices** (3+ required):
  - [ ] Each guideline has context
  - [ ] ✅ Good search query example
  - [ ] ❌ Bad search query with reason
  - [ ] Relevance handling guidance (for scores <0.5)
  - [ ] No results handling guidance

#### Common Mistakes for Cortex Search Tools
- ❌ Generic "Search documents" descriptions
- ❌ Missing Data Sources section
- ❌ No relevance/no-results handling guidance
- ❌ Search examples without ✅/❌ indicators
- ❌ Missing keyword strategy guidance

---

## 4. Planning Instructions Validation

### Business Context Section (Required)

#### Organization Context (3-4 elements)
- [ ] Organization name and type
- [ ] Key operational metrics (e.g., "Manages $XB across N strategies")
- [ ] Regulatory framework (e.g., "SEC-regulated with quarterly reviews")
- [ ] Data operations (e.g., "Data refreshes daily at 4 PM ET")

#### Key Business Terms (3-5 terms)
For Each Term:
- [ ] Term name clearly stated
- [ ] Definition with specific thresholds/values
- [ ] Example showing real-world application
- [ ] No generic definitions - all have exact numbers/processes

#### Domain Categories (2-4 categories)
For Each Category:
- [ ] Category name
- [ ] Description with key characteristics
- [ ] Example showing defining features

### Tool Selection Logic (Required)
- [ ] Query types categorized (3-5 types)
- [ ] For each query type:
  - [ ] ✅ Correct tool(s) specified
  - [ ] ❌ Anti-patterns specified
  - [ ] Clear decision criteria
- [ ] Tool sequence for multi-tool queries specified

### Complete Workflow Examples (Required: 2-3)

For Each Workflow:
- [ ] **Trigger**: Example question pattern that starts workflow
- [ ] **Step-by-Step Execution** (3-5 steps):
  - [ ] Each step specifies exact tool
  - [ ] Each step has exact query/search pattern
  - [ ] "Extract from results" specified for each step
  - [ ] "Why this step" business justification provided
  - [ ] Steps show data flow between tools

- [ ] **Synthesize Final Response**:
  - [ ] Elements specified with source steps
  - [ ] Format specified
  - [ ] Required inclusions listed (thresholds, citations, etc.)

- [ ] **Example Complete Interaction**:
  - [ ] Realistic user question
  - [ ] Complete agent response showing all workflow elements
  - [ ] Response demonstrates proper formatting
  - [ ] Includes all required elements

### Error Handling (Required: 3-5 scenarios)

For Each Scenario:
- [ ] **Scenario Name**: Clear error condition
- [ ] **Detection**: How to identify error occurred
- [ ] **Recovery Steps**: Numbered list (2-4 steps)
- [ ] **User Message**: Exact message pattern in quotes
- [ ] **Alternative**: What to suggest or how to proceed

#### Required Error Scenarios
- [ ] Entity/Portfolio Not Found scenario
- [ ] Search Returns No Results scenario
- [ ] Date Ambiguity scenario
- [ ] Metric Unavailable scenario
- [ ] Insufficient Data scenario (if quantitative agent)

### Common Mistakes in Planning Instructions
- ❌ No Business Context section
- ❌ Business terms without exact thresholds
- ❌ Workflows without step-by-step tool sequences
- ❌ Workflows without complete example interactions
- ❌ Error handling without specific recovery steps
- ❌ Generic "handle errors gracefully" instead of scenarios

---

## 5. Testing and Validation

### Pre-Deployment Testing

#### Component Testing
- [ ] Each Cortex Analyst tool tested independently
  - [ ] Basic query returns results
  - [ ] Metric calculations work correctly
  - [ ] Dimension filters work as expected
- [ ] Each Cortex Search tool tested independently
  - [ ] Basic search returns documents
  - [ ] Relevance scores reasonable
  - [ ] Attributes searchable (if configured)

#### Integration Testing
- [ ] Multi-tool workflows tested
  - [ ] Data flows correctly between tools
  - [ ] Synthesis produces coherent responses
  - [ ] All workflow steps execute successfully

#### Business Scenario Testing
- [ ] Test with realistic queries for agent's domain
- [ ] Verify response formatting matches instructions
- [ ] Confirm flagging/warnings appear correctly
- [ ] Check data freshness included in responses

#### Error Handling Testing
- [ ] Test each error scenario
  - [ ] Error detected correctly
  - [ ] Recovery steps work
  - [ ] User messages are helpful
  - [ ] Alternatives are reasonable

### Sample Query Testing

For Each Agent, Test Minimum:
- [ ] 3 simple queries (single tool)
- [ ] 2 complex queries (multiple tools)
- [ ] 1 edge case query (error scenario)

Document Results:
- [ ] All queries return reasonable responses
- [ ] Response formatting matches instructions
- [ ] No linter errors or warnings
- [ ] Performance acceptable (<30 seconds)

---

## 6. Documentation and Maintenance

### Documentation Requirements
- [ ] Agent configuration documented in `docs/agents_setup.md`
- [ ] Test queries documented with expected responses
- [ ] Known limitations documented
- [ ] Related agents cross-referenced

### Version Control
- [ ] Configuration changes tracked
- [ ] Breaking changes noted
- [ ] Semantic view changes coordinated
- [ ] Search service updates synchronized

### Maintenance Plan
- [ ] Regular review schedule established
- [ ] Performance monitoring configured
- [ ] User feedback collection process
- [ ] Update procedures documented

---

## Validation Summary Template

Use this template to summarize validation results:

```
Agent Name: [agent_name]
Validated By: [name]
Date: [YYYY-MM-DD]

Metadata: ✅ PASS / ❌ FAIL
- Issues: [list any issues]

Response Instructions: ✅ PASS / ❌ FAIL
- Style: ✅ Complete / ❌ Missing elements
- Presentation: ✅ Complete / ❌ Missing elements
- Response Structures: [N] provided (minimum 2)
- Issues: [list any issues]

Tool Configurations: ✅ PASS / ❌ FAIL
- Cortex Analyst Tools: [N] total
  - All have Data Coverage: ✅ YES / ❌ NO
  - All have When to Use/NOT: ✅ YES / ❌ NO
  - All have Query Best Practices: ✅ YES / ❌ NO
- Cortex Search Tools: [N] total
  - All have Data Sources: ✅ YES / ❌ NO
  - All have Search Best Practices: ✅ YES / ❌ NO
- Issues: [list any issues]

Planning Instructions: ✅ PASS / ❌ FAIL
- Business Context: ✅ Complete / ❌ Missing elements
- Workflow Examples: [N] provided (minimum 2)
- Error Handling: [N] scenarios (minimum 3)
- Issues: [list any issues]

Testing: ✅ PASS / ❌ FAIL
- Component tests: ✅ PASS / ❌ FAIL
- Integration tests: ✅ PASS / ❌ FAIL
- Sample queries: [N] tested, [N] passed
- Issues: [list any issues]

Overall Status: ✅ READY FOR DEPLOYMENT / ❌ NEEDS WORK / ⚠️ READY WITH CAVEATS

Next Steps:
1. [Action item 1]
2. [Action item 2]
```

---

## Common Configuration Antipatterns

### ❌ Antipattern 1: Generic Tool Descriptions
**Problem**: Tool description says "Gets data from database" or "Searches documents"
**Impact**: Agent can't distinguish between tools, leads to incorrect selection
**Solution**: Include Data Coverage, When to Use with specific examples, Query Best Practices

### ❌ Antipattern 2: Missing "When NOT to Use"
**Problem**: Tool description only lists capabilities without boundaries
**Impact**: Agent uses wrong tool for queries outside tool's scope
**Solution**: Explicitly list anti-patterns with alternative tools specified

### ❌ Antipattern 3: Assumed Business Context
**Problem**: Planning instructions reference "thresholds" or "limits" without defining them
**Impact**: Agent makes up values or asks user unnecessarily
**Solution**: Include Business Context section with exact thresholds and definitions

### ❌ Antipattern 4: Implicit Workflows
**Problem**: Planning says "Use appropriate tools" without specifying which or when
**Impact**: Inconsistent tool selection, missed multi-tool opportunities
**Solution**: Provide 2-3 complete workflow examples with step-by-step tool sequences

### ❌ Antipattern 5: No Error Handling
**Problem**: No guidance for missing data, ambiguous queries, or edge cases
**Impact**: Poor user experience when things go wrong
**Solution**: Include 3-5 error scenarios with detection, recovery, messages, alternatives

### ❌ Antipattern 6: General Response Guidance
**Problem**: Response instructions say "be professional" or "format nicely"
**Impact**: Inconsistent formatting, missing required elements
**Solution**: Provide Style/Presentation subsections with specific rules and complete examples

---

## Quick Reference: Minimum Requirements

**Agent Metadata:**
- Agent name (lowercase_with_underscores)
- Display name (Title Case, 2-4 words)
- Description (2-3 sentences: persona + capabilities + value)

**Response Instructions:**
- Style section (6 elements: tone, lead-with, terminology, precision, limitations, focus)
- Presentation section (5 elements: tables, charts, metrics, flags, freshness)
- 2-3 Response Structure templates with complete examples

**Each Tool:**
- Cortex Analyst: Data Coverage, Semantic Model Contents, When to Use (3-4), When NOT (3), Query Best Practices (3+)
- Cortex Search: Data Sources, When to Use (3-4), When NOT (3), Search Best Practices (3+)

**Planning Instructions:**
- Business Context (organization, terms, categories)
- Tool Selection with ✅/❌ patterns
- 2-3 Complete Workflow Examples (trigger, steps, synthesis, example interaction)
- 3-5 Error Handling scenarios (detection, recovery, message, alternative)

**Testing:**
- 3 simple queries tested
- 2 complex queries tested
- 1 error scenario tested
- All responses match instructions

---

## Revision History

- **v1.0** (2025-01-15): Initial checklist based on Snowflake Intelligence best practices and SAM demo enhancements

---

Use this checklist systematically to ensure all agent configurations meet production quality standards before deployment.

