# Corporate Relationship Manager Scenarios - Glacier First Bank AI Intelligence Demo

[← Back to Demo Scenarios Index](../demo_scenarios.md)

This document contains demo scenarios for the **Corporate Relationship Manager** persona, demonstrating AI-powered proactive client intelligence and opportunity discovery.

**Category**: Commercial Banking  
**Persona**: Corporate Relationship Manager  
**Scenarios**: 1 comprehensive relationship management workflow

---

## Corporate Relationship Manager - Proactive Client Intelligence Scenario

**Category**: Commercial Banking  
**Persona**: Corporate Relationship Manager (RM)  
**Business Context**: Relationship managers need to proactively identify opportunities, monitor client health, and provide strategic advisory services across their corporate client portfolio. This requires synthesizing structured CRM data, unstructured call notes/emails, external news, and cross-bank intelligence to deliver personalized, timely recommendations.

**Value Proposition**:
- **Opportunity Discovery**: AI automatically surfaces cross-sell, upsell, and risk mitigation opportunities from unstructured documents
- **Client Intelligence**: 360-degree view combining CRM, transaction data, news, and relationship history
- **Proactive Engagement**: Early warning of client risks and timely identification of revenue opportunities
- **Productivity**: 5-10x improvement in portfolio coverage through AI-driven prioritization and insights

**Agent Tools**:
1. **Corporate Client 360 Tool** (Cortex Analyst on `corporate_client_360_sv`)
   - Query client metrics, opportunity pipeline, transaction volumes, vendor relationships
   - Analyze account tier, status, and relationship manager assignments
2. **Client Documents Search** (Cortex Search on `client_documents_search_svc`)
   - Search call notes, internal emails, and client news articles
   - Extract opportunities, risks, and action items from unstructured text
3. **Cross-Domain Risk Analysis** (Cortex Analyst on `aml_kyc_risk_sv`)
   - Check client AML risk profile and compliance status
   - Identify potential compliance issues that might affect relationship

**Data Available**:
- **CLIENT_CRM**: Relationship manager assignments, account status/tier, last contact date, risk opportunities count
- **CLIENT_OPPORTUNITIES**: Identified opportunities (cross-sell, upsell, risk mitigation) with potential value, priority, status
- **CLIENT_DOCUMENTS**: Unstructured call notes, internal emails, and client news articles
- **Corporate Client 360 View**: Aggregated metrics on opportunities, transaction volumes, vendor relationships
- **Cross-entity data**: Transactions, risk ratings, compliance documents

---

### Demo Flow

**Setup**: "Let me show you how Glacier First Bank's Corporate Relationship Managers use AI to proactively manage their client portfolio and identify revenue opportunities."

---

#### Turn 1: Portfolio Overview and Prioritization

**User Query**:
> "Show me my corporate client portfolio summary. Which clients need my attention this week?"

**Expected Agent Response**:
```
Let me analyze your client portfolio and identify priorities.

**Portfolio Summary**:
- **Total Clients**: 15 corporate relationships
- **Premium Tier**: 4 clients (€125M combined transaction volume)
- **Standard Tier**: 8 clients (€68M combined transaction volume)  
- **Basic Tier**: 3 clients (€12M combined transaction volume)

**Clients Requiring Attention This Week**:

1. **AutoNordic GmbH** (Premium Tier)
   - **Last Contact**: 45 days ago (exceeds 30-day policy)
   - **Open Opportunities**: 2 (€850K pipeline value)
   - **Recent Activity**: €15.2M transaction volume (90 days)
   - **Action**: Schedule strategic account review

2. **TechVentures S.A.** (Standard Tier)
   - **Status**: Recently upgraded to Standard from Basic
   - **Open Opportunities**: 3 (€1.2M pipeline value)
   - **Recent News**: Secured Series B funding (€25M)
   - **Action**: Discuss expanded banking services

3. **Nordic Industries S.A.** (Standard Tier)
   - **Risk Alert**: 3 high-risk vendor relationships identified
   - **Compliance Status**: Pending enhanced due diligence
   - **Action**: Risk mitigation consultation required

**Recommendation**: Prioritize AutoNordic for immediate outreach (relationship maintenance), followed by TechVentures (growth opportunity) and Nordic Industries (risk management).

Would you like me to prepare briefing materials for any of these clients?
```

**Talking Points**:
- **Portfolio Intelligence**: AI synthesizes CRM, transaction, and opportunity data for prioritized action
- **Relationship Health**: Automated tracking of contact frequency and engagement metrics
- **Risk-Adjusted Prioritization**: Balances revenue opportunities with risk management needs
- **Proactive Alerts**: Surfaces issues before they become problems (e.g., 45-day no-contact)

---

#### Turn 2: Deep Dive on Growth Opportunity

**User Query**:
> "Tell me more about TechVentures S.A. What opportunities have we identified and what's their recent business activity?"

**Expected Agent Response**:
```
Let me gather comprehensive intelligence on TechVentures S.A.

**Client Overview**:
- **Industry**: Software Services
- **Account Tier**: Standard (recently upgraded)
- **Relationship Manager**: You (Sarah Chen)
- **Last Contact**: 12 days ago
- **Risk Rating**: LOW

**Identified Opportunities** (3 open):

1. **Treasury Management Upgrade** - Priority: HIGH
   - **Potential Value**: €450K annual revenue
   - **Source**: Internal email (discovered in team discussion)
   - **Context**: CFO mentioned frustration with current cash management system
   - **Status**: IN_PROGRESS
   - **Next Step**: Present multi-currency solution demo

2. **Trade Finance Package** - Priority: MEDIUM
   - **Potential Value**: €520K annual revenue  
   - **Source**: Call note from recent conversation
   - **Context**: Expanding into Asian markets, needs letters of credit capability
   - **Status**: OPEN
   - **Next Step**: Connect with trade finance specialists

3. **FX Risk Management** - Priority: MEDIUM
   - **Potential Value**: €280K annual revenue
   - **Source**: Client news article
   - **Context**: Series B funding includes USD/SGD currency exposure
   - **Status**: OPEN
   - **Next Step**: Introduce hedging solutions

**Recent Business Activity**:

From news article (published 8 days ago):
"TechVentures S.A. announced closing of €25M Series B funding round led by Asian investors. Funds will support expansion into Singapore and Tokyo markets, with plans to double headcount by year-end. CFO Martinez stated: 'This capital enables our aggressive international growth strategy.'"

**Call Note Summary** (18 days ago):
- Discussed current banking relationship satisfaction
- CFO expressed need for more sophisticated cash management
- Planning to open Asian subsidiaries in Q2
- Mentioned previous bank couldn't support multi-currency complexity

**Strategic Recommendation**:
Schedule meeting to present comprehensive package:
- Treasury management platform upgrade
- Trade finance capabilities for Asia expansion  
- Multi-currency FX solutions
- Potential combined value: €1.25M annual revenue

This timing is ideal given their funding and expansion plans.
```

**Talking Points**:
- **Opportunity Sourcing**: AI extracts opportunities from call notes, emails, and news automatically
- **Comprehensive Intelligence**: Combines structured data (CRM, transactions) with unstructured insights (documents)
- **Revenue Optimization**: Clear pipeline value quantification for each opportunity
- **Strategic Packaging**: AI recognizes opportunity synergies (all related to Asia expansion)
- **Timely Engagement**: Proactive outreach aligned with client business events

---

#### Turn 3: Risk Mitigation for Existing Client

**User Query**:
> "What's the issue with Nordic Industries S.A.? Should I be concerned about this relationship?"

**Expected Agent Response**:
```
Let me provide a complete risk assessment for Nordic Industries S.A.

**Client Profile**:
- **Industry**: International Trade
- **Account Tier**: Standard
- **Current Risk Rating**: MEDIUM (elevated from LOW last quarter)
- **Transaction Volume (90d)**: €8.4M
- **Vendor Relationships**: 5 entities (3 flagged as high-risk)

**Risk Concerns Identified**:

1. **High-Risk Vendor Relationships** (from network analysis):
   - Trading with 3 entities in high-risk jurisdictions
   - 2 vendors share suspicious characteristics (shell company indicators)
   - Payment patterns suggest potential TBML activity
   
2. **Compliance Status**:
   - Enhanced Due Diligence (EDD) triggered last month
   - Compliance team reviewing transaction patterns
   - No transactions blocked, but under enhanced monitoring

3. **Recent Call Notes** (from RM discussions):
   - Client aware of compliance review, cooperative
   - Provided business rationale for vendor selection (cost optimization)
   - Expressed willingness to diversify supplier base if needed

**Recommended Actions**:

1. **Immediate** (This Week):
   - Schedule call to discuss compliance review findings
   - Present risk mitigation options (vendor diversification)
   - Position as partnership/advisory (not enforcement)

2. **Short-Term** (This Month):
   - Introduce supply chain finance solution as alternative to high-risk vendors
   - Offer trade compliance advisory services
   - Convert risk issue into revenue opportunity (€180K potential)

3. **Ongoing**:
   - Monthly check-ins during enhanced monitoring period
   - Collaborate with compliance team for streamlined client experience

**Risk Assessment**: Manageable concern, not relationship-threatening. Client is cooperative and this presents opportunity to deepen advisory relationship while improving risk profile.

**Strategic Positioning**: Frame conversation as "helping client navigate complex international trade environment" rather than "compliance problem."
```

**Talking Points**:
- **Risk-Aware Relationship Management**: AI surfaces compliance issues before they escalate
- **Cross-Domain Intelligence**: Connects network analysis findings to RM workflow
- **Opportunity in Risk**: Converts compliance issue into advisory/revenue opportunity
- **Client Partnership**: Positions bank as strategic advisor, not just regulator
- **Coordinated Response**: Seamless collaboration between RM and compliance functions

---

#### Turn 4: Call Preparation and Next Steps

**User Query**:
> "I want to call AutoNordic GmbH today since it's been 45 days. What should I discuss? Any recent news or opportunities I should mention?"

**Expected Agent Response**:
```
Let me prepare your call briefing for AutoNordic GmbH.

**Call Preparation Brief**:

**Client Context**:
- **Last Contact**: 45 days ago (your call note: routine quarterly check-in)
- **Account Health**: Excellent (Premium tier, €15.2M quarterly volume)
- **Relationship Duration**: 4.5 years
- **Decision Maker**: CFO Klaus Bergmann

**Recent Business Activity**:

**News Article** (published 22 days ago):
"AutoNordic GmbH announces new electric vehicle production facility in Leipzig. €50M investment will create 200 jobs and triple EV manufacturing capacity by 2026. CEO stated facility aligns with company's 'electric transformation strategy.'"

**Previous Call Notes** (45 days ago):
- Discussed working capital optimization
- CFO mentioned cash flow pressure from inventory buildup
- Expressed interest in supply chain finance solutions
- Action item: Send proposal for inventory financing (STATUS: Not yet sent)

**Identified Opportunities**:

1. **Capital Investment Financing** - NEW (from news)
   - **Potential Value**: €850K (estimated from €50M facility financing)
   - **Context**: Leipzig facility investment
   - **Approach**: Offer structured project financing package
   - **Priority**: HIGH (time-sensitive, construction likely starting soon)

2. **Supply Chain Finance** - EXISTING
   - **Potential Value**: €420K annual revenue
   - **Context**: CFO's previous interest from 45 days ago
   - **Follow-up**: We missed sending the proposal (action item)
   - **Priority**: HIGH (recover momentum, address previous commitment)

**Recommended Call Structure**:

1. **Opening** (2 min):
   - Reference the Leipzig facility announcement
   - Congratulate on expansion into EV manufacturing

2. **Acknowledge Miss** (1 min):
   - Apologize for not sending supply chain finance proposal
   - "I wanted to call before sending it to ensure it addresses your specific needs"

3. **Present Opportunities** (5 min):
   - Leipzig facility project financing (NEW)
   - Supply chain finance for inventory management (FOLLOW-UP)
   - Bundle both for comprehensive working capital solution

4. **Schedule Next Steps** (2 min):
   - In-person meeting with credit team next week
   - Tour of Leipzig facility (relationship building)
   - Establish regular monthly touchpoints going forward

**Pre-Call Actions**:
- Review credit appetite for €50M project financing
- Prepare preliminary term sheet for both opportunities
- Coordinate with infrastructure lending team for facility expertise

**Expected Outcome**: Re-engage relationship, secure meeting, position for €1.2M+ revenue opportunity.
```

**Talking Points**:
- **Call Preparation Intelligence**: AI automates briefing material creation from multiple sources
- **Accountability**: Tracks follow-up items and surfaces missed commitments
- **News Integration**: Automatically connects external business events to banking opportunities
- **Structured Approach**: Provides conversation framework for effective client engagement
- **Cross-Sell Positioning**: Bundles multiple solutions for larger relationship impact

---

### Scenario Wrap-up

**Business Impact Summary**:
- **Revenue Growth**: 5-10x improvement in opportunity identification and conversion
- **Portfolio Coverage**: RMs can effectively manage 2-3x more client relationships
- **Proactive Engagement**: Shift from reactive to proactive client advisory
- **Risk Management**: Earlier identification and mitigation of relationship risks
- **Client Satisfaction**: More informed, timely, and relevant interactions

**Technical Differentiators**:
- **Unified Data Platform**: Seamless integration of CRM, transactions, documents, and external news
- **AI-Powered Extraction**: Automatic opportunity identification from unstructured content
- **Cross-Domain Intelligence**: Connects compliance, credit, and relationship data
- **Real-Time Insights**: Near real-time search service updates (5-minute lag)
- **Comprehensive Semantic Views**: Rich metadata enables sophisticated natural language queries

---

[← Back to Demo Scenarios Index](../demo_scenarios.md)

