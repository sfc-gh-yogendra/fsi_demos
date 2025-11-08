# Glacier First Bank AI Intelligence Demo - Scenarios Index

This is the master index for all Glacier First Bank AI Intelligence demo scenarios. Scenarios are organized by persona for easier navigation and presentation planning.

## Demo Overview

**Institution**: Glacier First Bank (pan-EU universal bank)  
**Coverage**: Enterprise-wide AI Intelligence across Compliance, Credit Risk, Commercial Banking, and Wealth Management  
**Duration**: 15-20 minutes per scenario (or 45-60 minutes for comprehensive demo)  
**Audience**: Banking executives, risk managers, compliance officers, IT leaders, business line managers  

**Key Value Propositions**:
- **Cross-Domain Intelligence**: Risk contagion analysis through shared business relationships
- **Multi-Step Reasoning**: Complex analytical workflows with transparent audit trails
- **Contradictory Evidence Synthesis**: Balanced analysis of conflicting signals
- **Regulatory Compliance**: Automated EDD with complete source attribution
- **Revenue Optimization**: AI-powered opportunity discovery and portfolio intelligence
- **Operational Efficiency**: Dramatic productivity gains across all business lines

---

## Scenarios by Persona

### AML Officer Scenarios
**Persona**: Sarah Mitchell & Maria Santos, AML/KYC Compliance Officers  
**Agent**: `BD_aml_officer_agent`  
**Scenarios**: 4 comprehensive AML/KYC workflows

📄 **[View AML Officer Scenarios](scenarios/aml_officer_scenarios.md)**

1. **AML/KYC Enhanced Due Diligence Scenario**
   - Comprehensive EDD with PEP screening, adverse media, and cross-domain risk analysis
   - Multi-source validation and regulatory communication
   - **Value**: EDD time reduced from 4-6 hours to 15-20 minutes

2. **Transaction Monitoring & Alert Triage Scenario**
   - ML-based alert prioritization with 95% suspicion scoring
   - Network analysis identifying hidden connections
   - Automated SAR narrative generation
   - **Value**: 50-70% false positive reduction, 2-4x more confirmed suspicious activity

3. **Periodic KYC Reviews Scenario**
   - Automated change detection and low-touch processing
   - Real-time sanctions/PEP/adverse media screening
   - **Value**: 70-80% of reviews eligible for low-touch, 6-7x productivity multiplier

4. **Network Analysis for TBML Detection Scenario**
   - Graph-based shell company network identification
   - Fund flow visualization and typology classification
   - Comprehensive network SAR generation
   - **Value**: Uncovers coordinated schemes missed by traditional monitoring

---

### Credit Analyst Scenarios
**Persona**: James Wilson, Senior Credit Analyst  
**Agent**: `BD_credit_analyst_agent`  
**Scenarios**: 1 comprehensive credit risk workflow

📄 **[View Credit Analyst Scenarios](scenarios/credit_analyst_scenarios.md)**

1. **Credit Risk Analysis & Portfolio Intelligence Scenario**
   - Automated financial ratio analysis with policy threshold flagging
   - Historical cohort analysis with predictive loss modeling
   - Business plan document intelligence
   - Cross-domain portfolio risk assessment
   - **Value**: Credit analysis time reduced from 2-3 days to 2-3 hours

---

### Corporate Relationship Manager Scenarios
**Persona**: Corporate Relationship Manager  
**Agent**: `BD_corp_rm_agent`  
**Scenarios**: 1 comprehensive relationship management workflow

📄 **[View Corporate RM Scenarios](scenarios/corporate_rm_scenarios.md)**

1. **Corporate Relationship Manager - Proactive Client Intelligence Scenario**
   - Portfolio prioritization with automated opportunity discovery
   - AI extraction of opportunities from call notes, emails, and news
   - Cross-domain risk integration (compliance → RM)
   - Comprehensive call preparation with news integration
   - **Value**: 5-10x improvement in opportunity identification, 2-3x portfolio coverage

---

### Wealth Advisor Scenarios
**Persona**: Wealth Advisor  
**Agent**: `BD_wealth_advisor_agent`  
**Scenarios**: 1 comprehensive portfolio management workflow

📄 **[View Wealth Advisor Scenarios](scenarios/wealth_advisor_scenarios.md)**

1. **Wealth Advisor - Portfolio Alignment & What-If Rebalancing Scenario**
   - Automated drift detection across client portfolios
   - What-if rebalancing with tax impact analysis
   - Meeting note synthesis for client preparation
   - Model portfolio comparison with long-term impact quantification
   - **Value**: 3-5x faster portfolio analysis, proactive drift monitoring

---

## Cross-Domain Intelligence Demonstration (7 Scenarios)

### Connecting All Seven Scenarios

The Glacier First Bank demo now showcases comprehensive AI intelligence across **AML/KYC Compliance (5 scenarios)** and **Commercial/Wealth Banking (2 scenarios)**, demonstrating how Snowflake's unified data platform enables enterprise-wide insights.

**AML/KYC Compliance Intelligence**

**Shared Entity Analysis**: Northern Supply Chain Ltd and the Shell Company Network demonstrate risk contagion:
- **AML Perspective**: NSC as vendor to GTV (EDD Scenario) and potential money laundering risk through complex supply chains
- **Credit Perspective**: NSC as vendor to Innovate GmbH (Credit Risk Scenario), creating concentration risk
- **Transaction Monitoring**: Structuring alerts for GTV link back to NSC transactions (Alert Triage Scenario)
- **Periodic Review**: NSC appears in vendor analysis during routine reviews (Periodic KYC Scenario)
- **Network Analysis**: Shell company network may have transacted with NSC (TBML Detection Scenario)
- **Portfolio View**: Single vendor disruption or financial crime exposure affects multiple business lines

**Multi-Step Reasoning Across Scenarios**:
1. **Entity Identification**: AI recognizes shared vendors and network connections
2. **Risk Correlation**: Links supply chain disruption to credit risk AND money laundering risk
3. **Portfolio Impact**: Calculates concentration exposure across all affected clients
4. **Network Contagion**: Models how issues propagate through business ecosystem
5. **Mitigation Strategy**: Recommends diversification AND enhanced monitoring protocols

**Commercial & Wealth Banking Integration**

**Cross-Business Line Intelligence**:
- **Corporate RM → AML Risk**: Nordic Industries S.A. appears in both relationship manager portfolio (Corporate RM Scenario) AND network analysis shell company investigation (TBML Detection Scenario)
  - RM alerted to compliance concerns automatically
  - Converts risk issue into advisory opportunity (supply chain finance)
  - Demonstrates coordinated client management across compliance and relationship functions

- **Wealth → Credit Risk**: Wealth client holdings in corporate debt (Wealth Advisor Scenario) can be cross-referenced with credit analysis (Credit Risk Scenario)
  - Advisor alerted if client holds bonds of deteriorating credit
  - Portfolio rebalancing recommendations consider credit intelligence
  - Protects wealth clients from concentration in declining credits

- **RM → Compliance Intelligence**: Relationship manager CRM notes and opportunities (Corporate RM Scenario) inform compliance risk assessment (EDD, Alert Triage, Periodic KYC Scenarios)
  - Call notes automatically analyzed for suspicious activity indicators
  - Business rationale from RM discussions informs EDD investigations
  - Reduces false positives by providing business context

**Enterprise-Wide Value**:
1. **Unified Client View**: Single platform across compliance, commercial banking, and wealth management
2. **Risk Contagion Detection**: Automatically surfaces how issues in one area affect others
3. **Opportunity Discovery**: Compliance issues become relationship management touchpoints
4. **Coordinated Client Experience**: Seamless hand-offs between compliance, RM, and wealth teams
5. **Revenue Protection**: Early warning of client deterioration protects multiple revenue streams

**Demo Impact**: Showcases Snowflake as enterprise-wide AI platform, not just compliance tool


