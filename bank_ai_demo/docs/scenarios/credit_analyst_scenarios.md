# Credit Analyst Scenarios - Glacier First Bank AI Intelligence Demo

[← Back to Demo Scenarios Index](../demo_scenarios.md)

This document contains demo scenarios for the **Credit Analyst** persona, demonstrating AI-powered credit risk analysis and portfolio intelligence.

**Persona**: James Wilson, Senior Credit Analyst at Glacier First Bank  
**Agent**: `credit_analyst_agent`  
**Scenarios**: 1 comprehensive credit risk workflow

---

## Credit Risk Analysis & Portfolio Intelligence Scenario

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

[← Back to Demo Scenarios Index](../demo_scenarios.md)

