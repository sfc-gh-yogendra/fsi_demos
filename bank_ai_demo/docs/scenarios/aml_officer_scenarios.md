# AML Officer Scenarios - Glacier First Bank AI Intelligence Demo

[← Back to Demo Scenarios Index](../demo_scenarios.md)

This document contains all demo scenarios for the **AML Officer** persona, covering the complete AML/KYC lifecycle from Enhanced Due Diligence to Network Analysis.

**Persona**: Sarah Mitchell & Maria Santos, AML/KYC Compliance Officers at Glacier First Bank  
**Agent**: `BD_aml_officer_agent`  
**Scenarios**: 4 comprehensive AML/KYC workflows

---

## AML/KYC Enhanced Due Diligence Scenario

### Business Context Setup

**Persona**: Sarah Mitchell, AML Compliance Officer at Glacier First Bank  
**Business Challenge**: Compliance officers need to conduct Enhanced Due Diligence (EDD) on corporate clients with complex ownership structures and potential PEP connections. Traditional manual processes require hours of document review, cross-referencing multiple databases, and synthesising conflicting information from various sources. This creates compliance risks, delays customer onboarding, and increases operational costs.  
**Value Proposition**: AI-powered EDD automation provides instant access to corporate structures, beneficial ownership analysis, adverse media screening, and PEP identification with complete audit trails. This reduces EDD time from hours to minutes while ensuring comprehensive compliance coverage and regulatory documentation.

**Agent**: `BD_aml_officer_agent`  
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
- Recent transaction activity: €5M deposit received (flagged for PEP source-of-funds review)
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

## Transaction Monitoring & Alert Triage Scenario

### Business Context Setup

**Persona**: Maria Santos, AML/SAR Analyst at Glacier First Bank  
**Business Challenge**: AML analysts are overwhelmed by high-volume, low-accuracy transaction monitoring alerts. Legacy rule-based systems generate 90%+ false positives, creating massive manual workloads and alert fatigue. This leads to analyst burnout, increased operational costs, and the risk that genuine suspicious activity is missed in the noise. ML-based triage and network analysis can dramatically reduce false positives while improving detection of true financial crime.  
**Value Proposition**: AI-powered alert triage with ML-based priority scoring reduces false positives by 50-70% while identifying 2-4x more confirmed suspicious activity. Automated network analysis uncovers hidden connections between seemingly unrelated alerts, enabling faster SAR generation with complete audit trails.

**Agent**: `BD_aml_officer_agent`  
**Tools Available**: 
- Cortex Analyst (`transaction_monitoring_sv`) - Alert triage, priority scoring, disposition analysis
- Cortex Analyst (`aml_kyc_risk_sv`) - Customer risk profiles and transaction history
- Cortex Search (`compliance_docs_search_svc`) - Relationship manager notes, case files
- Cortex Search (`news_research_search_svc`) - Adverse media screening

**Data Available**: Transaction monitoring alerts, alert disposition history (for ML training), customer risk profiles, transaction data, compliance documents, relationship manager notes

### Demo Flow

**Scene Setting**: Maria begins her Monday morning by reviewing the overnight alert queue. The ML-based triage system has already prioritized alerts by suspicion score, filtering out likely false positives. A structuring alert for customer Global Trade Ventures S.A. sits at the top with a 95% suspicion score - five cash deposits of $9,500 each across five branches over two days.

#### Step 1: ML-Based Alert Triage
**User Input**: 
```
"What's my highest priority alert this morning?"
```

**Expected Response**:
- **Top Priority Alert**: ALERT_STRUCT_001 for Global Trade Ventures S.A.
- **ML Suspicion Score**: 95% (high priority)
- **Alert Type**: Structuring (5 cash deposits @ $9,500 each)
- **Customer Risk Rating**: HIGH
- **Key Risk Factors**: 
  - Pattern deviates significantly from 5-year transaction baseline
  - Amount precisely structured below $10,000 CTR threshold
  - Multi-branch execution suggests deliberate avoidance
  - Customer has 2 existing AML flags
- **Recommended Action**: Priority investigation required
- **Demo disclaimer**: "⚠️ Demo Notice: This analysis uses synthetic data for demonstration purposes only."

**Talking Points**:
- **ML-Based Prioritization**: AI triage model elevates high-suspicion alerts, suppresses likely false positives
- **Contextual Analysis**: Alert assessed against customer's historical baseline, not just rigid rules
- **Efficiency Gains**: Analysts focus on high-value investigations vs. clearing benign alerts
- **Risk-Based Approach**: Priority score combines multiple factors (pattern, customer risk, amount, timing)

#### Step 2: Contextual Investigation & Evidence Gathering
**User Input**: 
```
"Give me the full picture on Global Trade Ventures S.A. - customer profile, recent activity, and any relevant notes."
```

**Expected Response**:
- **Customer Profile**: Global Trade Ventures S.A., Luxembourg-based importer/exporter
- **Risk Rating**: HIGH (due to PEP connection - Elena Rossi, 40% UBO)
- **Recent Activity**: €5M wire transfer received 2 weeks ago (also flagged)
- **Relationship Manager Note** (from KYC file): "Customer mentioned selling classic car for cash 6 months ago, expects funds soon"
- **Timing Mismatch**: Cash sale note was 6 months ago, deposits are happening now
- **Transaction Pattern**: $47,500 total across 5 branches in 2 days suggests coordinated structuring
- **Risk Assessment**: Note provides partial context but doesn't explain current timing or multi-branch pattern

**Talking Points**:
- **360-Degree View**: AI instantly assembles customer profile, transaction history, and unstructured notes
- **Contextual Analysis**: Human judgment needed - note provides plausible explanation but timing is suspicious
- **Unstructured Data Integration**: CRM notes accessible via Cortex Search provide investigative leads
- **Transparent Reasoning**: AI presents evidence, analyst makes final disposition decision

#### Step 3: Network Analysis & Hidden Connections
**User Input**: 
```
"Has Global Trade Ventures or its principals interacted with any known high-risk entities in our system?"
```

**Expected Response**:
- **Network Analysis Result**: Connection identified to 'Global Parts LLC'
- **Relationship**: $20,000 wire transfer from GTV to Global Parts LLC 2 weeks after cash deposits
- **Prior History**: Global Parts LLC was subject of SAR filing 3 months ago (trade-based money laundering suspicion)
- **Risk Escalation**: Connection to previously reported entity significantly elevates suspicion
- **Network Graph**: Visual representation shows GTV → Global Parts → offshore entities
- **Recommendation**: Escalate to SAR with network analysis

**Talking Points**:
- **Hidden Connections**: Network analysis reveals non-obvious relationships between customers
- **Historical Intelligence**: System cross-references against prior SARs and investigations
- **Graph Analytics**: Visual network representation aids understanding of fund flows
- **Risk Contagion**: One customer's suspicious activity can indicate risk in connected accounts

#### Step 4: Automated SAR Narrative Generation
**User Input**: 
```
"Generate a complete draft SAR narrative incorporating all findings - the structuring pattern, the timing mismatch with the RM note, and the connection to Global Parts LLC."
```

**Expected Response**:
- **SAR Narrative Structure**:
  - **Summary**: Structured cash deposits totaling $47,500 across 5 branches
  - **Customer Background**: Luxembourg importer/exporter, HIGH risk, PEP connection
  - **Suspicious Activity**: Five deposits of exactly $9,500 (below CTR threshold)
  - **Pattern Analysis**: Coordinated multi-branch execution suggests deliberate structuring
  - **Contextual Factors**: Prior RM note about car sale provides partial explanation but timing doesn't match
  - **Network Connection**: Subsequent wire to Global Parts LLC (prior SAR subject for TBML)
  - **Conclusion**: Pattern consistent with intentional currency reporting evasion, escalated by connection to known suspicious entity
- **Source Citations**: All findings include document IDs, dates, transaction references
- **Recommendation**: File SAR with FinCEN, maintain enhanced monitoring

**Talking Points**:
- **Automated Drafting**: AI generates comprehensive, well-structured SAR narrative in seconds
- **Regulatory Compliance**: Narrative includes all required elements (summary, basis, supporting facts)
- **Complete Audit Trail**: Every fact cited with source document and date
- **Analyst Oversight**: Draft ready for analyst review and refinement, not autonomous filing
- **Efficiency Gains**: SAR drafting time reduced from hours to minutes

### Scenario Wrap-up

**Business Impact Summary**:
- **False Positive Reduction**: ML triage reduces alert queue by 50-70%, focusing analysts on true risks
- **Detection Enhancement**: Network analysis identifies 2-4x more confirmed suspicious activity
- **Productivity Gains**: Investigation time reduced from 4-6 hours to 30-45 minutes per alert
- **Quality Improvement**: Comprehensive SARs with complete audit trails and network context
- **Analyst Experience**: Reduced burnout from eliminating low-value false positive clearing

**Technical Differentiators**:
- **ML-Based Triage**: Priority scoring trained on historical disposition outcomes
- **Network Analytics**: Graph-based analysis uncovers hidden connections across customer base
- **Contextual Intelligence**: Seamless integration of structured alerts and unstructured notes
- **Automated Documentation**: Professional SAR narratives with regulatory compliance built-in

---

## Periodic KYC Reviews Scenario

### Business Context Setup

**Persona**: Sarah Mitchell, KYC Analyst at Glacier First Bank (same persona as Scenario A)  
**Business Challenge**: KYC analysts spend 85% of their time on manual data gathering for periodic customer reviews. Most reviews find no material changes, yet require hours of work to re-screen sanctions lists, check adverse media, and verify transaction patterns. This creates a massive operational burden and delays reviews for customers who genuinely need enhanced scrutiny.  
**Value Proposition**: AI-powered change detection and automated screening enables "low-touch" processing for customers with no material changes, reducing review time from 45-60 minutes to under 1 minute. This frees analysts to focus on complex, high-risk reviews that require human judgment.

**Agent**: `BD_aml_officer_agent`  
**Tools Available**: 
- Cortex Analyst (`aml_kyc_risk_sv`) - Customer risk profiles, review schedules, transaction patterns
- Cortex Search (`compliance_docs_search_svc`) - PEP/sanctions lists, customer documents
- Cortex Search (`news_research_search_svc`) - Adverse media screening

**Data Available**: Customer profiles with review dates, transaction history, sanctions/PEP lists, adverse media archives

### Demo Flow

**Scene Setting**: Sarah is processing her weekly queue of periodic reviews. The system has identified 15 customers due for review this week. The AI has pre-processed all of them, running automated checks and flagging 3 for manual review due to detected changes. The remaining 12 are recommended for "low-touch" processing.

#### Step 1: Review Queue Analysis
**User Input**: 
```
"Show me periodic reviews due this week, prioritized by risk and flag any that need manual attention."
```

**Expected Response**:
- **Total Reviews Due**: 15 customers
- **Low-Touch Eligible**: 12 customers (no material changes detected)
- **Manual Review Required**: 3 customers (changes detected)
  - Customer A: New adverse media hit (regulatory investigation)
  - Customer B: Significant transaction pattern change (+150% volume)
  - Customer C: PEP status change (family member appointed to government role)
- **Prioritization**: Manual reviews ranked by severity
- **Time Savings**: Estimated 8-9 hours saved through automated low-touch processing
- **Demo disclaimer**: "⚠️ Demo Notice: This analysis uses synthetic data for demonstration purposes only."

**Talking Points**:
- **Intelligent Automation**: AI pre-processes entire queue, identifies reviews needing human attention
- **Change Detection**: Automated comparison against last review baseline
- **Risk-Based Allocation**: Human analysts focus on complex cases with actual changes
- **Productivity Multiplier**: 12 reviews completed automatically vs. manual processing

#### Step 2: Low-Touch Review Processing
**User Input**: 
```
"Open the low-touch review for customer Nordic Industries S.A. and show me the automated check results."
```

**Expected Response**:
- **Customer**: Nordic Industries S.A., Medium-risk manufacturing client
- **Last Review**: 12 months ago (annual cycle)
- **Automated Checks Completed**:
  - ✅ **Sanctions Screening**: No new hits (checked against OFAC, UN, EU lists)
  - ✅ **PEP Screening**: No status changes for principals or UBOs
  - ✅ **Adverse Media**: No new negative news articles found
  - ✅ **Transaction Pattern Analysis**: Activity consistent with historical baseline
    - Average monthly volume: €850K (historical: €820K, variance: +3.7%)
    - Transaction frequency: 45 transactions/month (historical: 42, variance: +7%)
    - High-risk country exposure: 0% (unchanged)
  - ✅ **KYC Documents**: All documents current, no expiring within 90 days
- **Recommendation**: **Low-Touch Approval** - No material changes detected
- **Review Form**: Pre-populated with all check results and supporting data
- **Required Action**: Analyst adds approval comment and submits (< 30 seconds)

**Talking Points**:
- **Comprehensive Automation**: All standard checks performed automatically
- **Change Detection**: Quantitative comparison shows minimal variance from baseline
- **Data Freshness**: Real-time screening against current sanctions/PEP lists
- **Audit Trail**: Complete record of all checks performed with timestamps
- **Efficiency**: 45-60 minute manual review reduced to 30-second approval

#### Step 3: Approval & Efficiency Metrics
**User Input**: 
```
"Approve this review with standard comment and show me time saved."
```

**Expected Response**:
- **Review Status**: APPROVED
- **Comment Added**: "Periodic review completed via automated low-touch process. No material changes identified. All screening checks passed. Risk profile remains stable at MEDIUM rating."
- **Next Review Date**: Auto-calculated for 12 months (based on MEDIUM risk)
- **Processing Time**: 45 seconds (vs. historical average 48 minutes)
- **Time Saved**: 47 minutes 15 seconds per review
- **Productivity Gain**: Analyst can process 60+ low-touch reviews per day vs. 8-10 manual reviews
- **Quality Assurance**: 100% screening coverage vs. potential human oversight

**Talking Points**:
- **Quantifiable ROI**: Clear metrics on time savings and productivity gains
- **Scalability**: Automated process handles high volumes without additional headcount
- **Consistency**: Standardized checks eliminate variability in review quality
- **Regulatory Compliance**: Complete audit trail meets EBA and local regulatory requirements
- **Human Oversight**: Analyst retains final approval authority, AI supports not replaces

### Scenario Wrap-up

**Business Impact Summary**:
- **Efficiency Gains**: 70-80% of periodic reviews eligible for low-touch processing
- **Time Savings**: 45-55 minutes saved per low-touch review
- **Capacity Multiplier**: Analysts can handle 6-7x more reviews with same headcount
- **Quality Improvement**: 100% consistent screening vs. manual variability
- **Risk Focus**: Human analysts allocated to high-risk, complex reviews needing judgment

**Technical Differentiators**:
- **Automated Change Detection**: AI compares current state against last review baseline
- **Real-Time Screening**: Live checks against current sanctions/PEP/adverse media data
- **Pattern Analysis**: Transaction behavior analyzed for anomalies vs. historical norms
- **Workflow Automation**: Pre-populated forms and recommendations streamline approvals

---

## Network Analysis for TBML Detection Scenario

### Business Context Setup

**Persona**: Maria Santos, Senior AML Analyst at Glacier First Bank  
**Business Challenge**: Traditional transaction monitoring focuses on individual customer behavior, missing coordinated schemes involving multiple seemingly unrelated entities. Trade-Based Money Laundering (TBML) and shell company networks deliberately fragment activity to evade detection. Network analysis can uncover these hidden patterns by identifying shared directors, common addresses, and circular payment flows that are invisible when reviewing customers in isolation.  
**Value Proposition**: Graph-based network analysis identifies coordinated money laundering schemes involving multiple shell companies. By analyzing corporate structure data, relationship patterns, and payment flows simultaneously, the system detects Trade-Based Money Laundering typologies that evade traditional rule-based monitoring.

**Agent**: `BD_aml_officer_agent`  
**Tools Available**: 
- Cortex Analyst (`network_analysis_sv`) - Entity relationships, shared characteristics, network metrics
- Cortex Analyst (`aml_kyc_risk_sv`) - Customer and transaction data
- Cortex Search (`compliance_docs_search_svc`) - Corporate structure documents, UBO records

**Data Available**: Entity relationships with shared directors/addresses, corporate structure data, transaction flows, customer profiles

### Demo Flow

**Scene Setting**: Maria receives an alert from the anomaly detection model flagging a cluster of five import/export businesses. Individually, each company appears unremarkable with modest transaction volumes. However, the ML model has identified suspicious patterns in their collective behavior: rapid onboarding within 45 days, shared corporate director, common registered address, and high-velocity circular payment activity.

#### Step 1: Network Alert Investigation
**User Input**: 
```
"Explain this network alert involving Baltic Trade Ltd, Nordic Commerce S.A., Alpine Export GmbH, Adriatic Import Ltd, and Aegean Trade S.A."
```

**Expected Response**:
- **Network Alert Type**: Shell Company Network / Coordinated Entity Cluster
- **Entities Involved**: 5 import/export companies, all incorporated in Gibraltar
- **Suspicious Characteristics**:
  - **Shared Director**: Anya Sharma (appears as director on all 5 companies)
  - **Common Address**: "42 Mailbox Lane, Virtual Office Complex, Gibraltar" (mail forwarding service)
  - **Incorporation Timing**: All 5 entities incorporated within 45-day window
  - **Industry**: All classified as Import/Export (common TBML typology)
  - **Circular Relationships**: VENDOR relationships form closed loop (A→B→C→D→E→A)
- **Risk Assessment**: HIGH - multiple shell company indicators present
- **Typology**: Suspected Trade-Based Money Laundering network
- **Demo disclaimer**: "⚠️ Demo Notice: This analysis uses synthetic data for demonstration purposes only."

**Talking Points**:
- **Hidden Patterns**: Network analysis reveals connections invisible in individual customer reviews
- **Shell Company Indicators**: Shared director + address + rapid incorporation = classic typology
- **Graph Analytics**: Relationship visualization shows circular vendor network structure
- **Typology Detection**: AI identifies pattern matching known TBML methodology

#### Step 2: Fund Flow Visualization
**User Input**: 
```
"Show me the fund flow for this entire network over the last 90 days."
```

**Expected Response**:
- **Network Transaction Analysis**: 
  - **Total Volume**: €15.7M processed through 5-entity network in 90 days
  - **Flow Pattern**: Funds enter from various sources → rapid consolidation → exit to 3 offshore shell entities
  - **Velocity**: Average fund residence time: 48 hours (extremely rapid)
  - **Beneficiaries**: Final destinations are high-risk jurisdictions (BVI, Panama, Seychelles)
- **Payment Chain**:
  1. Multiple inbound payments to network entities (€15.7M total)
  2. Rapid circular transfers between the 5 companies (layering)
  3. Consolidation and wire-out to 3 offshore entities within 48 hours
- **Red Flags**:
  - No legitimate business purpose for rapid circular transfers
  - Transaction values inconsistent with declared business size
  - Immediate outflow to high-risk offshore jurisdictions
  - Pattern consistent with TBML layering and integration phases
- **Graph Visualization**: Animated network diagram shows money flow through circular structure

**Talking Points**:
- **Ecosystem Intelligence**: Complete picture of coordinated scheme across multiple entities
- **Flow Analysis**: Traces money movement through layering and integration phases
- **Quantification**: €15.7M in 90 days shows scale of suspected laundering operation
- **Visual Intelligence**: Network graph makes complex scheme immediately comprehensible
- **Typology Matching**: Pattern matches established TBML methodology

#### Step 3: Typology Classification & TBML Identification
**User Input**: 
```
"What money laundering typology does this pattern match, and what are the specific indicators?"
```

**Expected Response**:
- **Primary Typology**: **Trade-Based Money Laundering (TBML)**
- **Specific Variant**: Shell company network with rapid layering
- **TBML Indicators Present**:
  - ✓ Multiple import/export entities (trade narrative cover)
  - ✓ Circular vendor relationships (no legitimate business rationale)
  - ✓ Rapid fund movement (layering phase)
  - ✓ Offshore integration (high-risk jurisdictions)
  - ✓ Shell company characteristics (shared director, virtual office, recent incorporation)
  - ✓ High velocity, low substance (funds never remain in accounts)
- **Regulatory References**: 
  - FATF Trade-Based Money Laundering indicators
  - EU AML Directive Article 18 (shell company red flags)
- **Historical Context**: Similar networks identified in [jurisdiction] investigations
- **Confidence Level**: HIGH (8 out of 10 TBML indicators present)

**Talking Points**:
- **Typology Library**: AI matches pattern against known money laundering methodologies
- **Regulatory Intelligence**: References specific FATF and EU AML framework indicators
- **Evidence-Based**: Each indicator supported by specific data points from network
- **Educational**: Helps analysts understand TBML schemes for future detection

#### Step 4: Comprehensive Network SAR
**User Input**: 
```
"Generate a comprehensive SAR covering all 5 entities, documenting the shell company structure, circular payments, and TBML typology. Also recommend account actions."
```

**Expected Response**:
- **Master SAR Generated**:
  - **Subject Entities**: All 5 companies listed with full details
  - **Principal**: Anya Sharma (shared director across network)
  - **Network Structure**: Documented with corporate registry evidence
  - **Transaction Analysis**: €15.7M in 90 days, circular flow pattern documented
  - **Typology Classification**: TBML with shell company network
  - **FATF Indicators**: All 8 applicable indicators cited with supporting evidence
  - **Timeline**: 45-day incorporation → 30-day network activation → 90-day high-velocity activity
  - **Beneficiaries**: 3 offshore entities identified as ultimate recipients
  - **Source Attribution**: Complete references to corporate docs, transaction records, registry data
- **Recommended Actions**:
  - ⚠️ **Immediate**: Place holds on all outbound wires from 5 entities pending review
  - 🚨 **Urgent**: Escalate to Financial Intelligence Unit (FIU)
  - 📋 **Administrative**: Flag Anya Sharma in internal watchlist
  - 🔒 **Account Action**: Initiate exit procedures for all 5 entities
  - 🔍 **Monitoring**: Enhanced scrutiny for any new entities with Anya Sharma as director/UBO
- **File Status**: Ready for analyst review and submission to FinCEN/relevant FIU

**Talking Points**:
- **Comprehensive Reporting**: Single master SAR covers entire coordinated scheme
- **Network Context**: SAR documents relationships, not just individual transactions
- **Regulatory Compliance**: Includes all required TBML indicators and evidence
- **Actionable Intelligence**: Specific recommendations for account management and monitoring
- **Preventive Measures**: Flags principal for future detection (Anya Sharma)

### Scenario Wrap-up

**Business Impact Summary**:
- **Detection Enhancement**: Network analysis identifies coordinated schemes missed by individual monitoring
- **Scheme Sophistication**: Uncovers Trade-Based Money Laundering and shell company networks
- **Investigation Efficiency**: Complete network analysis in hours vs. weeks of manual work
- **Regulatory Impact**: Comprehensive SARs provide law enforcement with actionable intelligence
- **Preventive Value**: Network insights enable proactive blocking of similar schemes

**Technical Differentiators**:
- **Graph Analytics**: Native network analysis across entity relationships and payment flows
- **Pattern Recognition**: ML models trained on known TBML typologies
- **Shared Characteristic Detection**: Automated identification of common directors, addresses, timing patterns
- **Ecosystem Intelligence**: Cross-domain analysis connecting corporate structure to transaction behavior
- **Typology Classification**: AI-powered matching against regulatory frameworks (FATF, EBA)

---

[← Back to Demo Scenarios Index](../demo_scenarios.md)

