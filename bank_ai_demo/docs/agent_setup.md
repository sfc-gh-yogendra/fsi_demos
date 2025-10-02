# Agent Configuration Guide

This document provides step-by-step instructions for configuring the AI agents in Snowflake Intelligence and validating their functionality.

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
**Semantic View**: `BANK_AI_DEMO.AI.aml_kyc_risk_sv`  
**Description**: Analyze customer risk profiles, AML flags, KYC status, and due diligence requirements. Query for high-risk customers, overdue reviews, and suspicious flag patterns using natural language.

#### Tool 2: Compliance Documents Search
**Tool Name**: `compliance_docs_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AI.compliance_docs_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `ENTITY_NAME`, `DOC_TYPE`, `PUBLISH_DATE`, `RISK_SIGNAL`  
**Description**: Search compliance documents including onboarding docs, adverse media, PEP/sanctions records, and internal memos. Filter by entity name, document type, and risk signal level.

#### Tool 3: News & Adverse Media Search
**Tool Name**: `news_adverse_media_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AI.news_research_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `ENTITY_NAME`, `ARTICLE_TYPE`, `PUBLISH_DATE`, `SENTIMENT_SCORE`, `SOURCE`  
**Description**: Search news articles and research reports for adverse media, regulatory investigations, political exposure, and reputational risks. Filter by sentiment score and source.

#### Tool 4: Document Templates Search
**Tool Name**: `document_templates_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AI.document_templates_search_svc`  
**ID Column**: `TEMPLATE_ID`  
**Title Column**: `TEMPLATE_NAME`  
**Attributes**: `TEMPLATE_ID`, `TEMPLATE_NAME`, `TEMPLATE_TYPE`, `SCENARIO`, `USE_CASE`, `REGULATORY_FRAMEWORK`, `REQUIRED_VARIABLES`  
**Description**: Search document templates for RFIs, SARs, compliance reports, and external communications. Filter by template type, scenario, and use case.

#### Tool 5: PDF Report Generator
**Tool Name**: `pdf_report_generator`  
**Type**: Custom Tool  
**Resource Type**: Procedure  
**Custom Tool Identifier**: `BANK_AI_DEMO.AI.GENERATE_PDF_REPORT`  
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

### Quick Validation Tests

Test the AML Officer Agent with these simple queries:

1. **Risk Assessment Test**:
   ```
   "Show me all HIGH risk customers who require EDD and have outstanding AML flags."
   ```
   **Expected**: Should identify high-risk customers with REQUIRES_EDD status.

2. **Comprehensive EDD Test**:
   ```
   "Compile an EDD on Global Trade Ventures S.A.: risk profile, structure, UBOs, adverse media."
   ```
   **Expected**: Should discover €5M deposit, identify Marcus Weber and Elena Rossi as UBOs, and find Elena Rossi adverse media.

3. **PDF Generation Test**:
   ```
   "Generate a PDF report for Global Trade Ventures S.A. EDD analysis."
   ```
   **Expected**: Should perform EDD analysis AND generate PDF with formatted response.

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
**Service**: `BANK_AI_DEMO.AI.credit_policy_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `POLICY_SECTION`, `EFFECTIVE_DATE`  
**Description**: Search credit policy documents for ratio thresholds, industry guidelines, and lending criteria. Filter by policy section and effective date.

#### Tool 2: Loan Documents Search
**Tool Name**: `loan_documents_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AI.loan_documents_search_svc`  
**ID Column**: `ID`  
**Title Column**: `TITLE`  
**Attributes**: `ID`, `TITLE`, `CONTENT`, `APPLICANT_NAME`, `DOC_TYPE`, `UPLOAD_DATE`, `DOCUMENT_SECTION`  
**Description**: Search loan application documents including business plans, financial statements, and legal documents. Filter by applicant name, document type, and section.

#### Tool 3: Document Templates Search
**Tool Name**: `document_templates_search`  
**Type**: Cortex Search  
**Service**: `BANK_AI_DEMO.AI.document_templates_search_svc`  
**ID Column**: `TEMPLATE_ID`  
**Title Column**: `TEMPLATE_NAME`  
**Attributes**: `TEMPLATE_ID`, `TEMPLATE_NAME`, `TEMPLATE_TYPE`, `SCENARIO`, `USE_CASE`, `REGULATORY_FRAMEWORK`, `REQUIRED_VARIABLES`  
**Description**: Search document templates for credit memos, decline letters, and external communications. Filter by template type and credit scenario.

#### Tool 4: PDF Report Generator
**Tool Name**: `pdf_report_generator`  
**Type**: Custom Tool  
**Resource Type**: Procedure  
**Custom Tool Identifier**: `BANK_AI_DEMO.AI.GENERATE_PDF_REPORT`  
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

### Quick Validation Tests

Test the Credit Analyst Agent with these simple queries:

1. **Policy Breach Analysis Test**:
   ```
   "Analyse Innovate GmbH's credit application and highlight any policy breaches or risk factors."
   ```
   **Expected**: Should flag DSCR breach (1.15), D/E warning (3.2), and concentration breach (72%).

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

## Setup Complete

Both agents are now configured and ready for use. Test them with the validation queries above to ensure proper functionality.

**Key Demo Entities**:
- **Global Trade Ventures S.A.** (Luxembourg) - AML subject with PEP connections
- **Innovate GmbH** (Germany) - Credit applicant with policy breaches  
- **Northern Supply Chain Ltd** (UK) - Shared vendor for cross-domain risk

For technical support or deployment questions, refer to the main README.md file.

---
