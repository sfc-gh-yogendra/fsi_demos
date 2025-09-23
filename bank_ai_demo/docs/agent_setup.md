# Glacier First Bank AI Intelligence Demo - Agent Setup Instructions

This document provides complete instructions for configuring the AI agents in Snowflake Intelligence for the Glacier First Bank demo.

## Prerequisites

✅ **Database Infrastructure**: BANK_AI_DEMO database with all tables created  
✅ **Demo Data**: All demo data populated (entities, relationships, documents)  
✅ **Search Services**: Cortex Search services created and operational  
✅ **Warehouses**: BANK_AI_DEMO_COMPUTE_WH and BANK_AI_DEMO_SEARCH_WH available  

## Agent Configuration Overview

The demo uses **2 specialized agents** for comprehensive financial intelligence:

1. **AML Officer Agent** (`aml_officer_agent`) - Enhanced Due Diligence
2. **Credit Analyst Agent** (`credit_analyst_agent`) - Credit Risk Analysis

Each agent combines multiple tools for sophisticated cross-domain analysis and multi-step reasoning.

---

## Agent 1: AML Officer Agent

### Basic Configuration

**Agent Name**: `aml_officer_agent`  
**Display Name**: AML Compliance Officer  
**Description**: Assists with Enhanced Due Diligence for corporate clients. Analyzes customer risk profiles using structured data, gathers UBOs from onboarding documents, screens entities and UBOs across adverse media and PEP/sanctions, summarises allegations, drafts RFIs, and provides audit summaries.  
**Orchestration Model**: Claude 4

### Tools Configuration

#### Tool 1: AML Risk Analysis
**Tool Name**: `aml_risk_analysis`  
**Type**: Cortex Analyst  
**Semantic View**: `BANK_AI_DEMO.SEMANTIC_LAYER.aml_kyc_risk_sv`  
**Description**: Analyze customer risk profiles, AML flags, KYC status, and due diligence requirements. Query for high-risk customers, overdue reviews, and suspicious flag patterns using natural language.

#### Tool 2: Compliance Documents Search
**Tool Name**: `compliance_docs_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AGENT_FRAMEWORK.compliance_docs_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `ENTITY_NAME`, `DOC_TYPE`, `PUBLISH_DATE`, `RISK_SIGNAL`  
**Description**: Search compliance documents including onboarding docs, adverse media, PEP/sanctions records, and internal memos. Filter by entity name, document type, and risk signal level.

#### Tool 3: News & Adverse Media Search
**Tool Name**: `news_adverse_media_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AGENT_FRAMEWORK.news_research_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `ENTITY_NAME`, `ARTICLE_TYPE`, `PUBLISH_DATE`, `SENTIMENT_SCORE`, `SOURCE`  
**Description**: Search news articles and research reports for adverse media, regulatory investigations, political exposure, and reputational risks. Filter by sentiment score and source.

#### Tool 4: Document Templates Search
**Tool Name**: `document_templates_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AGENT_FRAMEWORK.document_templates_search_svc`  
**ID Column**: `TEMPLATE_ID`  
**Title Column**: `TEMPLATE_NAME`  
**Attributes**: `TEMPLATE_ID`, `TEMPLATE_NAME`, `TEMPLATE_TYPE`, `SCENARIO`, `USE_CASE`, `REGULATORY_FRAMEWORK`, `REQUIRED_VARIABLES`  
**Description**: Search document templates for RFIs, SARs, compliance reports, and external communications. Filter by template type, scenario, and use case.

#### Tool 5: PDF Report Generator
**Tool Name**: `pdf_report_generator`  
**Type**: Custom Tool  
**Resource Type**: Procedure  
**Custom Tool Identifier**: `BANK_AI_DEMO.AGENT_FRAMEWORK.GENERATE_PDF_REPORT`  
**Warehouse**: `BANK_AI_DEMO_COMPUTE_WH`  
**Parameters**:
- `ARG1` (VARCHAR, Required): The complete analysis content formatted in markdown. Include headers (##), bullet points, tables, and key findings. This will be the main body of the PDF report.
- `ARG2` (VARCHAR, Required): Specify the type of analysis - use "AML" for Anti-Money Laundering reports, "CREDIT" for credit risk assessments, or "ANALYSIS" for general financial analysis.
- `ARG3` (VARCHAR, Required): Full legal name of the entity, customer, or organization being analyzed. This will appear in the PDF filename and header.
**Description**: Generate professional PDF reports from analysis content with Glacier First Bank branding. Saves reports to secure stage for download and sharing.

### Response Instructions

```
Use concise, professional en-GB banking tone. Always cite source document ID/title and publish/effective dates. State currency (EUR), period, and cohort filters in quantitative answers. Apply severity icons for thresholds: ⚠️ warning, 🚨 breach. Provide audit summary of steps and sources when requested.

IMPORTANT: Always include this disclaimer at the end of every response:
"⚠️ Demo Notice: This analysis uses synthetic data for demonstration purposes only. All entities, transactions, and documents are fictitious and created for training/demo scenarios."

Specific Guidelines:
- Cite all sources with IDs/titles and dates. Keep objective, non-speculative tone.
- When summarising allegations, include brief quotes with source and date.
- For risk overview, tabulate per entity/UBO counts by doc_type and risk_signal.
- For external communications (RFIs, SARs): USE document templates from document_templates_search tool, populate required variables with case-specific information.
- When drafting formal letters: Search for appropriate template by type (RFI, SAR) and customize with specific details from your analysis.
- For professional reports: When using pdf_report_generator, format content in markdown with headers, tables, and key findings.
- For PDF generation responses: ALWAYS format as "📄 [Document Name](download_url) - Brief description of the generated report."
- Provide an audit summary on request listing tools used, searches performed, and documents cited.
- Present findings in clear, structured format suitable for compliance reporting.
- ALWAYS end every response with the demo data disclaimer above.
```

### Planning Instructions

```
For comprehensive AML/KYC analysis, combine structured risk data with document analysis. Start with quantitative risk assessment using Cortex Analyst, then support with document evidence using Cortex Search tools.

Specific Logic:
- For customer risk profiling: START with aml_risk_analysis to assess risk ratings, AML flags, and KYC status
- For entity/UBO identification: USE compliance_docs_search to find onboarding documents and corporate structure  
- For adverse media screening: USE news_adverse_media_search to find negative news, regulatory investigations, and political exposure
- For internal compliance records: USE compliance_docs_search for PEP/sanctions screening and internal memos
- For external communications: USE document_templates_search to find appropriate templates (RFI, SAR), then customize with case findings
- For professional PDF reports: USE pdf_report_generator ONLY when user explicitly requests PDF generation with phrases like "generate a PDF", "create a report", "export as PDF", or "provide a downloadable report". DO NOT use for normal analysis requests like "Compile an EDD on [entity]", "Analyze [entity]", "Assess [entity]", or "Review [entity]". When used, format analysis content in markdown and use appropriate report type (AML/CREDIT).
- For comprehensive EDD: COMBINE all tools in sequence - risk analysis first, then document searches, then templates/PDFs for outputs
- Always cross-reference structured data findings with document evidence for complete analysis
```

---

## Agent 2: Credit Analyst Agent

### Basic Configuration

**Agent Name**: `credit_analyst_agent`  
**Display Name**: Credit Risk Analyst  
**Description**: Assesses commercial loan applications. Computes key ratios, compares against policy thresholds, performs cohort analyses, summarises business plan sections, and proposes mitigants with citations.  
**Orchestration Model**: Claude 4

### Tools Configuration

#### Tool 1: Credit Policy Search
**Tool Name**: `credit_policy_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AGENT_FRAMEWORK.credit_policy_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `POLICY_SECTION`, `EFFECTIVE_DATE`  
**Description**: Search credit policy documents for ratio thresholds, industry guidelines, and lending criteria. Filter by policy section and effective date.

#### Tool 2: Loan Documents Search
**Tool Name**: `loan_documents_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AGENT_FRAMEWORK.loan_documents_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `APPLICANT_NAME`, `DOC_TYPE`, `UPLOAD_DATE`, `DOCUMENT_SECTION`  
**Description**: Search loan application documents including business plans, financial statements, and legal documents. Filter by applicant name, document type, and section.

#### Tool 3: Document Templates Search
**Tool Name**: `document_templates_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AGENT_FRAMEWORK.document_templates_search_svc`  
**ID Column**: `TEMPLATE_ID`  
**Title Column**: `TEMPLATE_NAME`  
**Attributes**: `TEMPLATE_ID`, `TEMPLATE_NAME`, `TEMPLATE_TYPE`, `SCENARIO`, `USE_CASE`, `REGULATORY_FRAMEWORK`, `REQUIRED_VARIABLES`  
**Description**: Search document templates for credit memos, decline letters, and external communications. Filter by template type and credit scenario.

#### Tool 4: PDF Report Generator
**Tool Name**: `pdf_report_generator`  
**Type**: Custom Tool  
**Resource Type**: Procedure  
**Custom Tool Identifier**: `BANK_AI_DEMO.AGENT_FRAMEWORK.GENERATE_PDF_REPORT`  
**Warehouse**: `BANK_AI_DEMO_COMPUTE_WH`  
**Parameters**:
- `REPORT_CONTENT` (VARCHAR, Required): The complete credit analysis formatted in markdown. Include financial ratios, policy compliance status, risk assessment, and recommendations. Use tables for financial metrics and bullet points for key findings.
- `REPORT_TYPE` (VARCHAR, Required): Use "CREDIT" for credit risk assessments and loan applications, "ANALYSIS" for general financial analysis, or "AML" if combined with compliance review.
- `ENTITY_NAME` (VARCHAR, Required): Full legal name of the applicant, borrower, or entity being assessed. This will appear in the PDF filename and header for proper identification.
**Description**: Generate professional PDF reports from credit analysis content with Glacier First Bank branding. Saves reports to secure stage for download and sharing.

### Response Instructions

```
Use concise, professional en-GB banking tone. Always cite source document ID/title and publish/effective dates. State currency (EUR), period, and cohort filters in quantitative answers. Apply severity icons for thresholds: ⚠️ warning, 🚨 breach. Provide audit summary of steps and sources when requested.

IMPORTANT: Always include this disclaimer at the end of every response:
"⚠️ Demo Notice: This analysis uses synthetic data for demonstration purposes only. All entities, transactions, and documents are fictitious and created for training/demo scenarios."

Specific Guidelines:
- For each flagged metric, report value, threshold, severity icon, and cite policy section/title/effective date.
- For cohorts, list filters (industry, D/E, concentration, window) and provide percentages with sample sizes.
- Summaries of business plan sections should be crisp with document/page references.
- For external communications (credit memos, decline letters): USE document templates from document_templates_search tool, populate required variables with case-specific analysis.
- When preparing committee presentations: Search for credit memo template and customize with specific ratio analysis and policy assessments.
- For professional reports: When using pdf_report_generator, format content in markdown with financial ratios, policy compliance, and recommendations.
- For PDF generation responses: ALWAYS format as "📄 [Document Name](download_url) - Brief description of the generated report."
- Present analysis in structured format suitable for credit committee review.
- Include specific recommendations for risk mitigation when policy breaches are identified.
- ALWAYS end every response with the demo data disclaimer above.
```

### Planning Instructions

```
For policy threshold analysis and document review, use Cortex Search with appropriate filters. For quantitative analysis and cohort comparisons, use Cortex Analyst when available. When both are relevant, use both tools and synthesise findings into comprehensive credit assessment.

Specific Logic:
- For application assessment: search policy documents for thresholds, then compare against applicant metrics and flag breaches.
- For cohort analysis: use structured data analysis with explicit filters for industry, ratios, and time periods.
- For document summaries: use loan_documents_search filtered by applicant name and document section.
- For external communications: use document_templates_search to find credit memo or decline letter templates, then populate with analysis.
- For committee presentations: search for credit memo template and customize with ratio analysis, policy compliance, and recommendations.
- For professional PDF reports: use pdf_report_generator ONLY when user explicitly requests PDF generation with phrases like "generate a PDF", "create a report", "export as PDF", or "provide a downloadable report". DO NOT use for normal analysis requests like "Compile an EDD on [entity]", "Analyze [entity]", "Assess [entity]", or "Review [entity]". When used, format credit analysis in markdown and use CREDIT report type.
- Always provide specific policy references and effective dates for threshold breaches.
```

---

## Policy Thresholds Reference

Configure these thresholds in your agent knowledge or ensure they're available in policy documents:

### Credit Risk Thresholds

**Debt Service Coverage Ratio (DSCR)**:
- Warning: < 1.25
- Breach: < 1.10
- Policy Reference: Mid-Market Lending Policy v3.2, Section 4.1.2

**Debt-to-Equity Ratio**:
- Warning: > 3.0
- Breach: > 3.5
- Policy Reference: Mid-Market Lending Policy v3.2, Section 4.1.1

**Current Ratio**:
- Warning: < 1.20
- Breach: < 1.10
- Policy Reference: Mid-Market Lending Policy v3.2, Section 4.1.3

**Client Concentration**:
- Warning: > 60%
- Breach: > 70%
- Policy Reference: Commercial Credit Risk Policy v2.1, Section 5.3.1

---

## Setup Verification

### Test AML Officer Agent

1. **Risk Assessment Test**:
   ```
   "Show me all HIGH risk customers who require EDD and have outstanding AML flags."
   ```
   **Expected**: Should use Cortex Analyst to identify high-risk customers with REQUIRES_EDD status and AML flags > 0.

2. **Comprehensive EDD Test**:
   ```
   "Compile an EDD on Global Trade Ventures S.A.: risk profile, structure, UBOs, adverse media."
   ```
   **Expected**: Should start with risk analysis, then find onboarding document, identify Marcus Weber and Elena Rossi as UBOs, and locate Elena Rossi adverse media from both compliance docs and news sources. Should NOT generate PDF (no explicit PDF request).

3. **PDF Generation Test**:
   ```
   "Generate a PDF report for Global Trade Ventures S.A. EDD analysis."
   ```
   **Expected**: Should perform complete EDD analysis AND generate PDF with formatted response: "📄 [AML Report - Global Trade Ventures S.A.](url) - Professional aml analysis report generated successfully."

4. **Adverse Media Screening Test**:
   ```
   "Screen for any adverse media or regulatory investigations involving Italian Transport Ministry connections."
   ```
   **Expected**: Should search both compliance documents and news/research for political scandals and regulatory content.

5. **Document Analysis Test**:
   ```
   "Summarise the specific allegations in any adverse media documents related to Italian political exposure."
   ```
   **Expected**: Should retrieve specific documents and provide detailed summary of allegations.

### Test Credit Analyst Agent

1. **Policy Breach Analysis Test**:
   ```
   "Analyse Innovate GmbH's credit application and highlight any policy breaches or risk factors."
   ```
   **Expected**: Should flag DSCR breach (1.15 < 1.25), D/E warning (3.2 > 3.0), and concentration breach (72% > 70%).

2. **Policy Document Search Test**:
   ```
   "What are the current debt service coverage ratio thresholds according to our lending policy?"
   ```
   **Expected**: Should find policy document and cite specific thresholds with policy reference.

3. **Business Plan Analysis Test**:
   ```
   "Summarise the 'Market Strategy' section of Innovate GmbH's business plan"
   ```
   **Expected**: Should locate business plan document and provide strategic analysis.

---

## Troubleshooting

### Common Issues

**1. Search Services Not Working**
- Verify search services exist: `SHOW CORTEX SEARCH SERVICES IN BANK_AI_DEMO.AGENT_FRAMEWORK;`
- Check service status and refresh if needed
- Ensure BANK_AI_DEMO_SEARCH_WH warehouse is running

**2. No Search Results**
- Verify demo data was loaded into document tables
- Check table names match search service configuration
- Test search services manually with SEARCH_PREVIEW function

**3. Policy Threshold Errors**
- Ensure credit policy documents contain exact threshold values
- Verify policy document IDs and titles match expected format
- Check effective dates are recent

**4. Agent Response Issues**
- Review agent instructions for typos or formatting errors
- Ensure tool descriptions match actual service names
- Verify warehouse permissions for agent execution

### Validation Queries

**Check Demo Data**:
```sql
-- Verify key entities exist
SELECT entity_name, country_code, esg_rating 
FROM BANK_AI_DEMO.RAW_DATA.ENTITIES 
WHERE entity_id IN ('GTV_SA_001', 'INN_DE_001', 'NSC_UK_001');

-- Verify compliance documents
SELECT title, entity_name, doc_type, risk_signal 
FROM BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENTS;

-- Verify loan application with policy breaches
SELECT applicant_name, debt_service_coverage_ratio, debt_to_equity_ratio, 
       single_client_concentration_pct 
FROM BANK_AI_DEMO.RAW_DATA.LOAN_APPLICATIONS 
WHERE applicant_name = 'Innovate GmbH';
```

**Test Search Services**:
```sql
-- Test compliance search
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'BANK_AI_DEMO.AGENT_FRAMEWORK.compliance_docs_search_svc',
    '{"query": "Global Trade Ventures beneficial ownership", "limit": 2}'
);

-- Test policy search
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'BANK_AI_DEMO.AGENT_FRAMEWORK.credit_policy_search_svc',
    '{"query": "debt service coverage ratio threshold", "limit": 2}'
);
```

---

## Cross-Domain Intelligence Patterns

Both agents support sophisticated cross-domain analysis through shared semantic views and entity relationships:

### Shared Vendor Risk Analysis

**Query**: "How does Northern Supply Chain Ltd affect our overall portfolio risk?"

**Expected Workflow**:
1. Identify all clients with Northern Supply Chain relationships
2. Cross-reference with financial exposure data
3. Check compliance status across affected clients
4. Synthesize portfolio concentration and contagion risk
5. Provide mitigation recommendations

### Contradictory Evidence Synthesis

**Query**: "Assess Innovate GmbH considering conflicting financial and news signals"

**Expected Workflow**:
1. Analyze financial strength from loan application data
2. Search news and research for sentiment analysis
3. Identify specific contradictions between data sources
4. Weigh evidence based on source reliability and recency
5. Provide balanced assessment with uncertainty acknowledgment

### Multi-Step Reasoning Documentation

All agents must provide transparent reasoning trails:

1. **Evidence Gathering**: List all data sources accessed
2. **Analysis Steps**: Document analytical methodology
3. **Synthesis Logic**: Explain how conflicting evidence was resolved
4. **Risk Assessment**: Justify final conclusions with supporting evidence
5. **Audit Trail**: Provide complete source attribution and timestamps

---

## Quality Standards

### Response Quality Requirements

- **Professional Tone**: Use en-GB banking terminology and formal language
- **Source Attribution**: Always cite document IDs, titles, and dates
- **Quantitative Precision**: Include currency, time periods, and sample sizes
- **Risk Flagging**: Use consistent severity indicators (⚠️/🚨)
- **Audit Transparency**: Offer detailed audit summaries on request

### Performance Targets

- **Simple Queries**: < 5 seconds response time
- **Complex Analysis**: < 15 seconds for multi-tool workflows
- **Cross-Domain Intelligence**: < 20 seconds for ecosystem analysis
- **Document Synthesis**: < 10 seconds for business plan summaries

### Validation Criteria

- **Accuracy**: All calculations and data references must be correct
- **Completeness**: Address all aspects of user queries
- **Consistency**: Maintain coherent risk assessments across domains
- **Auditability**: Provide complete reasoning transparency
- **Business Relevance**: Focus on actionable insights for decision-making

---

## Support Information

**Database**: BANK_AI_DEMO  
**Compute Warehouse**: BANK_AI_DEMO_COMPUTE_WH  
**Search Warehouse**: BANK_AI_DEMO_SEARCH_WH  
**Connection**: IE_DEMO65_CODE_USER  

**Key Demo Entities**:
- Global Trade Ventures S.A. (Luxembourg) - AML subject with PEP connections
- Innovate GmbH (Germany) - Credit applicant with policy breaches  
- Northern Supply Chain Ltd (UK) - Shared vendor for cross-domain risk

**Demo Data Scale**: ~500 entities, 2,000 documents, 50,000 transactions

For technical support or questions about the demo setup, refer to the main README.md and DEPLOYMENT_GUIDE.md files.

---

**🎯 Ready for Demo!** Once both agents are configured, test with the provided verification queries to ensure everything is working correctly.
