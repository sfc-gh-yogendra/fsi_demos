# Glacier First Bank AI Intelligence Demo - Demo Scenarios

This document provides complete demo scenarios for presenting the Glacier First Bank AI Intelligence capabilities to business and technical audiences.

## Demo Overview

**Institution**: Glacier First Bank (pan-EU universal bank)  
**Focus Areas**: AML/KYC Enhanced Due Diligence & Credit Risk Analysis  
**Duration**: 15-20 minutes total  
**Audience**: Banking executives, risk managers, compliance officers, IT leaders  

**Key Value Propositions**:
- **Cross-Domain Intelligence**: Risk contagion analysis through shared business relationships
- **Multi-Step Reasoning**: Complex analytical workflows with transparent audit trails
- **Contradictory Evidence Synthesis**: Balanced analysis of conflicting signals
- **Regulatory Compliance**: Automated EDD with complete source attribution

---

## Scenario A: AML/KYC Enhanced Due Diligence

### Business Context Setup

**Persona**: Sarah Mitchell, AML Compliance Officer at Glacier First Bank  
**Business Challenge**: Compliance officers need to conduct Enhanced Due Diligence (EDD) on corporate clients with complex ownership structures and potential PEP connections. Traditional manual processes require hours of document review, cross-referencing multiple databases, and synthesising conflicting information from various sources. This creates compliance risks, delays customer onboarding, and increases operational costs.  
**Value Proposition**: AI-powered EDD automation provides instant access to corporate structures, beneficial ownership analysis, adverse media screening, and PEP identification with complete audit trails. This reduces EDD time from hours to minutes while ensuring comprehensive compliance coverage and regulatory documentation.

**Agent**: `aml_officer_agent`  
**Tools Available**: 
- Cortex Analyst (`aml_kyc_risk_sv`) - Customer risk analysis, AML flags, KYC status
- Cortex Search (`compliance_docs_search_svc`) - Onboarding records, PEP databases, internal compliance  
- Cortex Search (`news_research_search_svc`) - Adverse media, regulatory investigations, news sources

**Data Available**: Customer risk profiles, AML flags, compliance documents, onboarding records, adverse media, PEP databases, regulatory filings, news articles, sentiment analysis

### Demo Flow

**Scene Setting**: Sarah needs to complete an Enhanced Due Diligence review for Global Trade Ventures S.A., a Luxembourg-based international trading company that has applied for expanded banking facilities. The client relationship manager has flagged potential complexity due to the company's international operations and beneficial ownership structure. Sarah needs to prepare a comprehensive EDD report for the monthly Risk Committee meeting this afternoon.

#### Step 1: Risk Assessment Overview
**User Input**: 
```
"Show me all HIGH risk customers who require EDD and have outstanding AML flags, ordered by most flags first."
```

**Expected Response**:
- Quantitative risk analysis showing HIGH risk customers requiring EDD:
  1. Global Trade Ventures S.A. (4 AML flags, REQUIRES_EDD)
  2. Premier Holdings AG (3 AML flags, REQUIRES_EDD)  
  3. Innovative Holdings GmbH (3 AML flags, REQUIRES_EDD)
- Clear entity names displayed for business users
- AML flag counts prioritized by risk level
- KYC status breakdown across customer portfolio
- **Demo disclaimer**: "⚠️ Demo Notice: This analysis uses synthetic data for demonstration purposes only."

**Talking Points**:
- **Structured Data Analysis**: Cortex Analyst provides instant quantitative insights
- **Risk-Based Approach**: Prioritize high-risk customers for enhanced monitoring
- **Portfolio Intelligence**: Understand overall risk distribution

#### Step 2: Comprehensive EDD Investigation
**User Input**: 
```
"Compile an EDD on Global Trade Ventures S.A.: risk profile, structure, UBOs, adverse media."
```

**Expected Response**:
- Customer risk rating and AML flag analysis from structured data
- Corporate structure summary from onboarding documents
- Beneficial ownership identification: Marcus Weber (60%) and Elena Rossi (40%)
- PEP flag for Elena Rossi (daughter of former Italian Transport Minister)
- Adverse media screening from both compliance docs and news sources
- Cross-source validation and risk assessment summary

**Talking Points**:
- **Instant Comprehensive Analysis**: AI processes multiple document types simultaneously
- **Cross-Domain Intelligence**: Automatically connects corporate structure to PEP databases
- **Complete Audit Trail**: Every finding includes source document ID and publication date
- **Regulatory Compliance**: Structured output meets EBA EDD requirements

**Key Features Highlighted**: 
- Cortex Search across multiple document types with entity filtering
- Multi-step reasoning combining structured and unstructured data
- Automatic PEP identification and risk flagging
- Professional compliance reporting with source attribution

#### Step 3: Multi-Source Adverse Media Screening
**User Input**: 
```
"Screen for any adverse media or regulatory investigations involving Italian Transport Ministry connections."
```

**Expected Response**:
- **Compliance Documents**: Elena Rossi PEP documentation and family connection details
- **News Sources**: Reuters articles on Italian Transport Ministry scandal investigation
- **Cross-Source Validation**: Corroborating evidence from multiple independent sources
- **Specific Allegations**: €2.3M in preferential contracts to family business
- **Investigation Status**: Parliamentary inquiry ongoing, no criminal charges filed
- **Risk Assessment**: Medium risk due to indirect family connection, monitored ongoing

**Talking Points**:
- **Dual-Source Adverse Media**: Both internal compliance records AND external news sources
- **Cross-Validation**: Multiple independent sources provide robust evidence
- **Comprehensive Coverage**: No adverse media missed through single-source screening
- **Current Intelligence**: Real-time adverse media monitoring with date verification
- **Professional Objectivity**: Non-speculative analysis with factual reporting

**Key Features Highlighted**: 
- Advanced document comprehension and summarisation
- Temporal analysis with investigation timeline tracking
- Risk calibration based on relationship proximity
- Regulatory-compliant adverse media reporting

#### Step 4: Cross-Domain Risk Assessment
**User Input**: 
```
"How does this PEP connection affect our overall risk exposure to Global Trade Ventures?"
```

**Expected Response**:
- PEP risk assessment: Medium (family connection, no direct involvement)
- Enhanced monitoring requirements under EU AML directives
- Recommended review frequency: Every 6 months
- Documentation requirements for ongoing relationship
- Integration with transaction monitoring thresholds

**Talking Points**:
- **Regulatory Intelligence**: Automatic application of EU AML framework
- **Risk-Based Approach**: Calibrated assessment based on connection type
- **Operational Integration**: Links to ongoing monitoring and transaction screening
- **Business Continuity**: Balanced approach enabling relationship continuation

**Key Features Highlighted**: 
- Regulatory framework application with specific directive references
- Risk calibration algorithms based on relationship analysis
- Integration with operational risk management processes
- Compliance workflow automation with review scheduling

#### Step 5: Regulatory Communication Draft
**User Input**: 
```
"Draft an RFI to request additional source-of-funds documentation for their recent €5M deposit."
```

**Expected Response**:
- **Template Search**: Agent finds "RFI_PEP_001" template from document templates
- **Customized RFI Letter**: Professional template populated with:
  - Client Name: Global Trade Ventures S.A.
  - Specific Amount: €5M deposit
  - PEP Connection: Elena Rossi (daughter of former Italian Transport Minister)
  - Required Documentation: Source of funds, PEP disclosures, corporate structure
- **Regulatory References**: EBA Guidelines (EBA/GL/2022/01), EU AML Directive
- **Timeline**: 30-day response requirement with escalation procedures

#### Step 6: PDF Generation of RFI Draft
**User Input**: 
```
"Generate a PDF of the RFI draft for Global Trade Ventures S.A. for formal sending."
```

**Expected Response**:
- **PDF Generation**: Agent uses custom PDF tool to create **real, downloadable RFI letter**
- **Report Details**: 
  - Filename: glacier_aml_Global_Trade_Venture_20241215_143022.pdf
  - Professional Glacier First Bank letterhead with branding
  - Formatted RFI letter with proper business formatting
  - Includes regulatory references, documentation requirements, and timelines
- **Storage**: Uploaded to @GLACIER_REPORTS_STAGE ready for official correspondence
- **Download Link**: Presigned URL for immediate download and distribution

**Talking Points**:
- **Document Automation**: From template search to professional PDF in minutes
- **Regulatory Compliance**: Properly formatted RFI ready for official correspondence
- **Workflow Integration**: Seamless transition from draft to distribution-ready document
- **Professional Standards**: Bank letterhead and formatting for external communications
- **Secure Distribution**: Controlled access with presigned URLs for stakeholder sharing

**Key Features Highlighted**: 
- Regulatory template generation with current guideline integration
- Professional document drafting with compliance standards
- Automated workflow triggers and timeline management
- Audit trail generation for regulatory reporting

### Scenario Wrap-up

**Business Impact Summary**:
- **Efficiency Gains**: EDD completion time reduced from 4-6 hours to 15-20 minutes
- **Risk Intelligence**: Quantitative risk analysis with AML flag monitoring via Cortex Analyst
- **Comprehensive Screening**: Dual-source adverse media from internal compliance + external news
- **Compliance Enhancement**: 100% source attribution with complete audit trails
- **Portfolio Intelligence**: Risk-based customer prioritization with structured data insights
- **Operational Excellence**: Standardised EDD reports meeting regulatory requirements

**Technical Differentiators**:
- **Multi-Tool Integration**: Cortex Analyst + dual Cortex Search services working together
- **Cross-Domain Intelligence**: Seamless integration of structured and unstructured data sources
- **Multi-Step Reasoning**: Complex analytical workflows with transparent decision logic
- **Regulatory Compliance**: Built-in EBA and local regulatory framework application
- **Snowflake AI Integration**: Native Cortex Search with enterprise-grade security and governance

---

## Scenario B: Credit Risk Analysis & Portfolio Intelligence

### Business Context Setup

**Persona**: James Wilson, Senior Credit Analyst at Glacier First Bank  
**Business Challenge**: Credit analysts need to assess commercial loan applications against complex policy frameworks while considering historical cohort performance and cross-domain risk factors. Traditional analysis requires manual ratio calculations, policy threshold lookups, historical data analysis, and document review across multiple systems. This creates analysis delays, inconsistent risk assessment, and missed portfolio concentration risks.  
**Value Proposition**: AI-powered credit analysis provides instant financial ratio computation, automated policy threshold flagging, historical cohort benchmarking, and cross-domain risk assessment. This reduces credit decision time from days to hours while improving risk assessment accuracy and portfolio intelligence.

**Agent**: `credit_analyst_agent`  
**Data Available**: Historical loans, current applications, credit policies, business plans, financial statements, market intelligence

### Demo Flow

**Scene Setting**: James is reviewing the loan application from Innovate GmbH, a German software services company requesting €8.5M for business expansion. The application has been flagged by the automated screening system for potential policy threshold breaches. James needs to complete his credit assessment before tomorrow's Credit Committee meeting, including ratio analysis, policy compliance review, and business plan evaluation.

#### Step 1: Financial Ratio Analysis & Policy Flagging
**User Input**: 
```
"Analyse Innovate GmbH's credit application and highlight any policy breaches or risk factors."
```

**Expected Response**:
- Financial metrics summary: DSCR 1.15, D/E 3.2, Current Ratio 1.18, Client Concentration 72%
- Policy breach flagging:
  - 🚨 **DSCR BREACH**: 1.15 < 1.10 (breach threshold) - Policy ref: Mid-Market Lending Policy v3.2, Section 4.1.2
  - ⚠️ **D/E WARNING**: 3.2 > 3.0 (warning threshold) - Policy ref: Mid-Market Lending Policy v3.2, Section 4.1.1
  - 🚨 **CONCENTRATION BREACH**: 72% > 70% (breach threshold) - Policy ref: Commercial Credit Risk Policy v2.1, Section 5.3.1
- Risk assessment: High risk due to multiple policy breaches
- Recommended mitigants and additional analysis required

**Talking Points**:
- **Instant Policy Compliance**: Automated threshold checking with exact policy references
- **Visual Risk Flagging**: Clear severity indicators (⚠️ warnings, 🚨 breaches) for immediate recognition
- **Comprehensive Analysis**: Multiple ratio assessment with integrated policy framework
- **Decision Support**: Specific mitigant recommendations based on breach patterns

**Key Features Highlighted**: 
- Automated financial ratio calculation with policy threshold integration
- Real-time policy compliance checking with exact regulatory references
- Visual risk flagging system with severity-based indicators
- Intelligent recommendation engine for risk mitigation strategies

#### Step 2: Historical Cohort Analysis
**User Input**: 
```
"What's the 5-year default rate for Software Services companies with similar risk profiles - D/E >3.0 and client concentration >70%?"
```

**Expected Response**:
- Cohort filters applied: Industry = Software Services, D/E > 3.0, Client Concentration > 70%
- Historical cohort size: 12 loans (2019-2024)
- Default rate: 25% (3 out of 12 loans defaulted)
- Sector average default rate: 8% (Software Services overall)
- Average loss given default: 45% of original loan amount
- Statistical confidence: Medium (sample size limitations noted)

**Talking Points**:
- **Predictive Intelligence**: Historical performance analysis with specific risk factor filtering
- **Benchmarking Capability**: Comparison against sector averages for context
- **Statistical Rigor**: Sample size considerations and confidence level reporting
- **Loss Quantification**: Expected loss calculations based on historical patterns

**Key Features Highlighted**: 
- Advanced cohort analysis with multi-dimensional filtering
- Statistical analysis with confidence interval reporting
- Comparative benchmarking against sector and portfolio averages
- Predictive loss modeling based on historical performance data

#### Step 3: Business Plan Document Analysis
**User Input**: 
```
"Summarise the 'Market Strategy' section of Innovate GmbH's business plan and assess execution risk."
```

**Expected Response**:
- Market strategy summary from business plan document (ID: INN_DE_BUSINESS_PLAN_2024)
- Target market: Mid-market enterprises (€50M-€500M revenue)
- Geographic expansion: Benelux and Nordic markets
- Service diversification: AI/ML consulting, cloud migration
- Execution risk assessment: High due to client concentration (72% from AutoTech Industries)
- Mitigation strategies: Client diversification plan required before facility approval

**Talking Points**:
- **Document Intelligence**: Advanced comprehension of complex business documents
- **Strategic Analysis**: AI assessment of business strategy viability and execution risk
- **Risk Integration**: Connection between strategic plans and financial risk factors
- **Actionable Insights**: Specific recommendations for risk mitigation and approval conditions

**Key Features Highlighted**: 
- Sophisticated document analysis with section-specific extraction
- Strategic business plan assessment with risk evaluation
- Cross-referencing between strategic plans and financial metrics
- Intelligent recommendation generation for credit decision support

#### Step 4: Cross-Domain Portfolio Risk Assessment
**User Input**: 
```
"How does Northern Supply Chain Ltd affect our overall portfolio risk exposure?"
```

**Expected Response**:
- Shared vendor analysis: Northern Supply Chain serves both Global Trade Ventures and Innovate GmbH
- Portfolio concentration risk: 2 clients dependent on same logistics provider
- Risk contagion potential: Supply chain disruption could affect multiple borrowers
- Geographic risk: Brexit-related logistics challenges for UK-based provider
- Recommended monitoring: Enhanced due diligence on Northern Supply Chain financial health
- Portfolio limit consideration: Review vendor concentration limits

**Talking Points**:
- **Ecosystem Intelligence**: AI identifies hidden portfolio concentrations through shared relationships
- **Risk Contagion Analysis**: Assessment of how single vendor issues could cascade across portfolio
- **Portfolio Management**: Integration of individual credit decisions with portfolio-level risk
- **Proactive Monitoring**: Early warning system for systemic risk factors

**Key Features Highlighted**: 
- Cross-domain relationship analysis with portfolio-wide impact assessment
- Risk contagion modeling through shared business ecosystem connections
- Portfolio concentration monitoring with vendor dependency tracking
- Systemic risk identification with proactive monitoring recommendations

### Scenario Wrap-up

**Business Impact Summary**:
- **Decision Speed**: Credit analysis time reduced from 2-3 days to 2-3 hours
- **Risk Accuracy**: Comprehensive policy compliance with zero threshold calculation errors
- **Portfolio Intelligence**: Hidden concentration risks identified through ecosystem analysis
- **Regulatory Compliance**: Complete audit trail with policy references and historical benchmarking

**Technical Differentiators**:
- **Multi-Domain Integration**: Seamless analysis across financial data, policies, documents, and market intelligence
- **Advanced Analytics**: Statistical cohort analysis with predictive loss modeling
- **Ecosystem Intelligence**: Cross-domain relationship analysis for portfolio-level risk assessment
- **Snowflake AI Excellence**: Native Cortex capabilities with enterprise-scale performance and security

---

## Cross-Domain Intelligence Demonstration

### Connecting the Scenarios

**Shared Entity Analysis**: Northern Supply Chain Ltd appears in both scenarios as:
- **AML Perspective**: Potential money laundering risk through complex supply chain transactions
- **Credit Perspective**: Vendor concentration risk affecting multiple borrowers
- **Portfolio View**: Systemic risk factor requiring enhanced monitoring

**Multi-Step Reasoning Example**:
1. **Entity Identification**: AI recognises Northern Supply Chain as shared vendor
2. **Risk Correlation**: Links supply chain disruption to credit risk for multiple clients
3. **Portfolio Impact**: Calculates concentration exposure across business lines
4. **Mitigation Strategy**: Recommends enhanced due diligence and monitoring protocols

**Contradictory Evidence Synthesis**:
- **Financial Strength**: Innovate GmbH shows strong revenue growth and market position
- **Risk Signals**: High client concentration and policy threshold breaches
- **AI Analysis**: Balanced assessment acknowledging both positive and negative indicators
- **Decision Support**: Structured recommendation with specific conditions and monitoring requirements

---

## Presentation Tips

### Opening the Demo
- **Set Business Context**: Emphasise real-world banking challenges and regulatory pressures
- **Highlight Integration**: Stress the seamless connection between compliance and credit risk
- **Demonstrate Scale**: Mention the comprehensive data scope (2,000+ documents, 1,500+ loans)

### During the Demo
- **Pause for Impact**: Allow time for audience to absorb the speed and sophistication
- **Highlight Citations**: Point out the complete source attribution and audit trails
- **Emphasise Cross-Domain**: Show how insights from one domain inform decisions in another
- **Technical Differentiation**: Reference Snowflake's unique AI capabilities and enterprise integration

### Closing the Demo
- **Quantify Benefits**: Emphasise time savings, accuracy improvements, and risk reduction
- **Regulatory Compliance**: Highlight audit trail completeness and regulatory framework integration
- **Competitive Advantage**: Position Snowflake's integrated AI platform as unique in the market
- **Next Steps**: Discuss implementation timeline and additional use cases

### Audience-Specific Messaging

**For Business Leaders**:
- Focus on operational efficiency and risk reduction
- Emphasise regulatory compliance and audit trail completeness
- Highlight competitive advantage and customer experience improvement

**For Risk Managers**:
- Stress comprehensive risk assessment and policy compliance
- Demonstrate cross-domain risk correlation and portfolio intelligence
- Show historical benchmarking and predictive analytics capabilities

**For IT Leaders**:
- Emphasise native Snowflake integration and enterprise security
- Highlight scalability and performance of Cortex AI platform
- Demonstrate governance and audit capabilities

**For Compliance Officers**:
- Focus on regulatory framework integration and audit trail completeness
- Show automated EDD capabilities and source attribution
- Demonstrate workflow automation and documentation standards

---

## Success Metrics

**Demo Effectiveness Indicators**:
- Audience engagement during cross-domain intelligence demonstrations
- Questions about implementation timeline and additional use cases
- Interest in technical architecture and integration capabilities
- Requests for follow-up meetings and proof-of-concept discussions

**Key Messages Delivered**:
- ✅ Snowflake AI provides unique cross-domain intelligence capabilities
- ✅ Enterprise-grade security and governance with complete audit trails
- ✅ Significant operational efficiency gains with improved risk assessment
- ✅ Native integration eliminates complex system architectures
- ✅ Regulatory compliance built-in with current framework support

**Next Steps After Demo**:
1. **Technical Deep Dive**: Architecture review and integration planning
2. **Use Case Expansion**: Additional scenarios and business line applications
3. **Proof of Concept**: Pilot implementation with customer data
4. **Implementation Planning**: Timeline, resources, and change management

---

**🎯 Ready to Demonstrate the Future of AI-Powered Financial Services!**

This demo showcases sophisticated AI capabilities that go far beyond simple question-answering, demonstrating true analytical intelligence with cross-domain reasoning and regulatory compliance integration.
