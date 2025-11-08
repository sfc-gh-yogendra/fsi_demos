# Wealth Advisor Scenarios - Glacier First Bank AI Intelligence Demo

[← Back to Demo Scenarios Index](../demo_scenarios.md)

This document contains demo scenarios for the **Wealth Advisor** persona, demonstrating AI-powered portfolio alignment monitoring and what-if rebalancing analysis.

**Category**: Wealth Management  
**Persona**: Wealth Advisor  
**Scenarios**: 1 comprehensive portfolio management workflow

---

## Wealth Advisor - Portfolio Alignment & What-If Rebalancing Scenario

**Category**: Wealth Management  
**Persona**: Wealth Advisor  
**Business Context**: Wealth advisors need to monitor client portfolios for drift from target allocations, identify rebalancing opportunities, conduct what-if scenario analysis, and demonstrate model portfolio alignment. This requires real-time analysis of holdings, model portfolios, tax implications, and meeting note history.

**Value Proposition**:
- **Portfolio Monitoring**: Automated detection of allocation drift and concentration risks
- **Model Alignment**: Quick verification that client holdings match assigned model portfolio
- **What-If Analysis**: Instant scenario modeling for rebalancing decisions
- **Client Communication**: AI-synthesized portfolio review summaries from meeting notes
- **Productivity**: 3-5x faster portfolio analysis and rebalancing recommendations

**Agent Tools**:
1. **Wealth Client Analysis Tool** (Cortex Analyst on `wealth_client_sv`)
   - Query portfolio holdings, allocations, and performance metrics
   - Analyze model portfolio alignment and drift calculations
   - Monitor concentration risks and diversification
2. **Meeting Notes Search** (Cortex Search on `wealth_meeting_notes_search_svc`)
   - Search portfolio review notes, investment strategy discussions, rebalancing decisions
   - Extract client preferences, risk tolerance changes, and stated objectives
3. **Model Portfolio Tool** (Cortex Analyst on `wealth_client_sv`)
   - Compare current allocations to target model portfolios
   - Calculate rebalancing trades needed to restore target weights

**Data Available**:
- **WEALTH_CLIENT_PROFILES**: Client risk tolerance, investment objectives, advisor assignments, model portfolio links
- **HOLDINGS**: Individual investment positions with current values, cost basis, unrealized gains/losses
- **MODEL_PORTFOLIOS**: Target allocation definitions (equity/bond/alternative/cash percentages) with expected returns
- **WEALTH_MEETING_NOTES**: Unstructured notes from portfolio reviews, strategy discussions, rebalancing decisions

---

### Demo Flow

**Setup**: "Let me demonstrate how Glacier First Bank's Wealth Advisors use AI to monitor portfolios, assess model alignment, and conduct what-if rebalancing analysis."

---

#### Turn 1: Portfolio Status and Drift Detection

**User Query**:
> "Show me my client portfolios that are out of alignment with their target models. Which ones need rebalancing?"

**Expected Agent Response**:
```
Let me analyze portfolio drift across your client base.

**Portfolios Requiring Rebalancing** (exceeding 10% drift trigger):

1. **Client**: WC_045 (€2.8M AUM)
   - **Model Portfolio**: Balanced Portfolio
   - **Risk Tolerance**: MODERATE
   - **Advisor**: Sophia Müller (you)
   
   **Allocation Analysis**:
   - **Equity**: 62.3% (Target: 50.0%) → +12.3% drift ⚠️
   - **Bonds**: 30.1% (Target: 40.0%) → -9.9% drift
   - **Alternatives**: 5.8% (Target: 7.0%) → -1.2% drift
   - **Cash**: 1.8% (Target: 3.0%) → -1.2% drift
   
   **Trigger**: Exceeded 10% rebalance threshold
   **Last Rebalance**: 8 months ago
   **Unrealized Gains**: €312K (tax consideration)
   **Recommendation**: Rebalance priority - HIGH

2. **Client**: WC_128 (€5.2M AUM)
   - **Model Portfolio**: Growth Portfolio
   - **Risk Tolerance**: AGGRESSIVE
   
   **Allocation Analysis**:
   - **Equity**: 82.5% (Target: 70.0%) → +12.5% drift ⚠️
   - **Bonds**: 10.2% (Target: 20.0%) → -9.8% drift
   - **Alternatives**: 6.1% (Target: 8.0%) → -1.9% drift
   - **Cash**: 1.2% (Target: 2.0%) → -0.8% drift
   
   **Trigger**: Exceeded 10% rebalance threshold
   **Last Rebalance**: 11 months ago
   **Unrealized Gains**: €687K (significant tax consideration)
   **Recommendation**: Rebalance priority - MEDIUM (consider tax-loss harvesting)

3. **Client**: WC_089 (€1.5M AUM)
   - **Model Portfolio**: Conservative Portfolio
   - **Risk Tolerance**: CONSERVATIVE
   
   **Concentration Alert**: 28% in single equity holding (exceeds 25% threshold) ⚠️
   - **Position**: AAPL (Apple Inc.)
   - **Current Value**: €420K
   - **Unrealized Gain**: €145K
   
   **Allocation Analysis**: Within normal ranges except concentration
   **Recommendation**: Rebalance priority - HIGH (concentration risk)

**Summary**:
- **Total Clients**: 24 wealth management relationships
- **Requiring Rebalancing**: 3 clients (12.5% of portfolio)
- **Estimated Trade Volume**: €450K across rebalancing activities
- **Tax Consideration**: €1.14M total unrealized gains across flagged portfolios

Would you like me to generate specific rebalancing recommendations for any client?
```

**Talking Points**:
- **Automated Monitoring**: AI continuously tracks allocation drift across entire client book
- **Model-Based Management**: Compares actual vs. target allocations from assigned models
- **Threshold Triggers**: Alerts when drift exceeds client-specific rebalancing parameters
- **Concentration Risk**: Identifies single-position concentration issues automatically
- **Tax Awareness**: Surfaces unrealized gains for tax-efficient rebalancing planning

---

#### Turn 2: What-If Rebalancing Scenario

**User Query**:
> "For client WC_045, show me what trades would be needed to rebalance back to the Balanced Portfolio target. What would be the tax impact?"

**Expected Agent Response**:
```
Let me generate a rebalancing analysis for WC_045.

**Current Portfolio** (€2,800,000 AUM):
- Equity: €1,744,400 (62.3%)
- Bonds: €842,800 (30.1%)
- Alternatives: €162,400 (5.8%)
- Cash: €50,400 (1.8%)

**Target Portfolio** (Balanced Model):
- Equity: €1,400,000 (50.0%)
- Bonds: €1,120,000 (40.0%)
- Alternatives: €196,000 (7.0%)
- Cash: €84,000 (3.0%)

**Required Trades**:

**SELL Positions** (reduce overweight equity):
1. Domestic Equity Index: SELL €150,000 (unrealized gain: €42K)
2. International Equity: SELL €130,000 (unrealized gain: €31K)
3. Technology Sector Fund: SELL €64,400 (unrealized gain: €18K)

**BUY Positions** (increase bonds and rebalance):
1. Government Bond Fund: BUY €180,000
2. Corporate Bond Fund: BUY €97,200
3. Alternative Investments Fund: BUY €33,600
4. Move to Cash: BUY €33,600 (money market)

**Tax Impact Analysis**:
- **Total Realized Gains**: €91,000
- **Estimated Tax** (25% capital gains): €22,750
- **After-Tax Cost**: €22,750 (0.81% of portfolio)

**Alternative Tax-Efficient Approach**:
If we prioritize tax-loss positions and defer high-gain sales:
- Use new contributions/dividends for rebalancing (if available)
- Harvest any tax losses to offset gains
- Phase rebalancing over 2-3 quarters to spread tax impact

**Risk Considerations**:
- **Current Risk**: Overexposure to equity volatility (12.3% over target)
- **Market Timing**: Strong equity market has driven drift
- **Client Tolerance**: MODERATE risk tolerance suggests rebalance is appropriate

**Recommendation**: 
Proceed with full rebalancing given significant drift (12.3%) and moderate risk tolerance. The €22,750 tax cost is justified by bringing portfolio back to client's agreed risk profile. Alternative phased approach would leave client overexposed for extended period.

**Next Steps**:
1. Schedule client call to review recommendation
2. Obtain signed rebalancing authorization
3. Execute trades (estimated 1-2 business days)
4. Document decision in meeting notes
```

**Talking Points**:
- **Precise Trade Recommendations**: AI calculates exact buy/sell amounts to restore target allocation
- **Tax-Aware Analysis**: Automatically calculates tax implications of rebalancing trades
- **Alternative Scenarios**: Suggests tax-efficient alternatives (phasing, loss harvesting)
- **Risk Quantification**: Articulates risk of NOT rebalancing vs. cost of rebalancing
- **Workflow Integration**: Provides complete next-steps checklist for execution

---

#### Turn 3: Client Meeting Preparation

**User Query**:
> "I have a portfolio review meeting with WC_045 tomorrow. Summarize our recent discussions and any decisions we made in previous meetings."

**Expected Agent Response**:
```
Let me prepare your meeting brief for client WC_045.

**Client Profile**:
- **Total AUM**: €2.8M
- **Risk Tolerance**: MODERATE
- **Investment Objectives**: BALANCED (growth + income)
- **Model Portfolio**: Balanced Portfolio (50/40/7/3)
- **Tax Status**: STANDARD (taxable account)

**Recent Meeting History**:

**Last Portfolio Review** (78 days ago):
Key Discussion Points:
- Client satisfied with overall performance (+6.2% YTD)
- Expressed concern about equity market volatility
- Discussed importance of staying disciplined with asset allocation
- Agreed to rebalance if equity allocation exceeded 60%
- Action Item: Review allocation quarterly (THIS MEETING)

**Investment Strategy Discussion** (154 days ago):
Key Decisions:
- Confirmed Balanced Portfolio model remains appropriate
- Client's retirement timeline: 12 years
- Income needs: Not immediate, wealth accumulation phase
- Rebalancing trigger: Set at 10% drift from target
- Review frequency: Quarterly for first year, then semi-annual

**Previous Rebalancing Decision** (247 days ago):
Trades Executed:
- Reduced equity from 58% to 50% (rebalanced €224K)
- Increased bond allocation to target 40%
- Tax impact: €18K realized gains
- Client comfortable with tax cost for risk management
- Performance since rebalance: +4.1%

**Current Situation Requiring Discussion**:

1. **Allocation Drift**: Equity now at 62.3% (exceeded 60% client threshold)
   - Matches scenario from last review (client said "rebalance if over 60%")
   - Client pre-agreed to this action

2. **Tax Impact**: €22,750 estimated (similar to last rebalancing)
   - Previous experience: client accepted €18K tax cost
   - Expectation: likely comfortable with this amount

3. **Market Context**: Strong equity performance drove drift (not risk-seeking behavior)
   - Validates staying disciplined vs. chasing performance
   - Aligns with client's stated concern about volatility

**Recommended Meeting Agenda**:

1. **Performance Review** (5 min):
   - YTD performance vs. benchmark
   - Attribution: equity gains drove portfolio returns

2. **Allocation Discussion** (10 min):
   - Show 62.3% equity allocation (exceeds threshold)
   - Reference client's previous guidance ("rebalance if over 60%")
   - Present specific rebalancing trades and tax impact

3. **Decision** (5 min):
   - Recommend proceeding with rebalancing per client's previous instruction
   - Obtain authorization
   - Confirm next review in 3 months

**Meeting Positioning**:
"We're here today exactly as planned. Your equity allocation has grown to 62.3%, which is above your 60% comfort threshold. Based on our previous discussions, I'm recommending we rebalance back to your Balanced model. This is disciplined portfolio management, not a market timing decision."

**Client Sentiment Expectation**: Positive. Client has consistently valued discipline and previously authorized similar rebalancing with similar tax impact.
```

**Talking Points**:
- **Meeting History Synthesis**: AI extracts key decisions from unstructured meeting notes
- **Client Preference Memory**: Recalls specific thresholds and preferences client previously stated
- **Contextual Recommendations**: Positions current recommendation based on past agreements
- **Meeting Efficiency**: Pre-prepared agenda saves advisor preparation time
- **Client Relationship**: Demonstrates advisor remembers client priorities and concerns

---

#### Turn 4: Model Portfolio Comparison

**User Query**:
> "Is the Balanced Portfolio still appropriate for WC_045, or should we consider moving to a more conservative model given their concern about volatility?"

**Expected Agent Response**:
```
Let me compare portfolio models for client WC_045's situation.

**Current Model: Balanced Portfolio**
- **Target Allocation**: 50% Equity / 40% Bonds / 7% Alternatives / 3% Cash
- **Risk Profile**: MODERATE
- **Expected Annual Return**: 6.5%
- **Expected Volatility**: 9.2%
- **Investment Horizon**: Medium to long-term (5-15 years)

**Alternative: Conservative Portfolio**
- **Target Allocation**: 30% Equity / 60% Bonds / 7% Alternatives / 3% Cash
- **Risk Profile**: LOW
- **Expected Annual Return**: 4.8%
- **Expected Volatility**: 5.8%
- **Investment Horizon**: Short to medium-term (3-10 years)

**Comparison Analysis**:

**If Client Moves to Conservative Model**:
- **Risk Reduction**: -3.4% volatility (37% reduction)
- **Return Trade-off**: -1.7% expected annual return
- **Impact on €2.8M Portfolio**: ~€47,600 less annual growth
- **Over 12 years to retirement**: ~€765K less accumulated wealth (compound effect)

**Client Situation Assessment**:

**Factors SUPPORTING Current Balanced Model**:
✓ 12-year retirement timeline (adequate time horizon)
✓ No immediate income needs (wealth accumulation phase)
✓ Risk tolerance assessed as MODERATE (matches Balanced)
✓ Previous rebalancing behavior shows discipline (stayed with model)
✓ "Concern about volatility" is normal investor sentiment, not panic

**Factors POTENTIALLY SUPPORTING Conservative Model**:
⚠️ Expressed concern about volatility (but this was 78 days ago, during market correction)
⚠️ Some clients feel more comfortable with lower volatility as they age

**Recommendation: MAINTAIN Balanced Portfolio**

**Rationale**:
1. **Time Horizon**: 12 years to retirement provides adequate recovery time for market volatility
2. **Opportunity Cost**: Conservative model would sacrifice ~€765K wealth accumulation
3. **Volatility Context**: Client's concern was expressed during temporary market volatility, not fundamental risk tolerance change
4. **Historical Behavior**: Client has consistently stayed disciplined with Balanced model through multiple rebalancing cycles
5. **Risk Tolerance Assessment**: Still appropriate for MODERATE tolerance and BALANCED objectives

**Meeting Approach**:
"I want to address your previous concern about volatility. What you're feeling is normal investor sentiment - nobody enjoys seeing their portfolio fluctuate. However, your 12-year timeline means short-term volatility is less important than long-term growth. Moving to a Conservative model would reduce volatility by 37%, but would cost approximately €765K in accumulated wealth by retirement. The Balanced model remains appropriate for your situation. That said, if your risk tolerance has fundamentally changed, we should discuss it."

**Alternative If Client Insists**:
Consider intermediate step: "Moderate Growth" model (40% equity / 50% bonds) as compromise
- Risk reduction: -2.1% volatility
- Return trade-off: -1.0% annual return  
- Wealth impact: ~€385K less over 12 years (better than full Conservative move)
```

**Talking Points**:
- **Model Comparison Intelligence**: AI quantifies trade-offs between portfolio models
- **Long-Term Impact**: Calculates compound effect of model changes over investment horizon
- **Client-Specific Context**: Evaluates recommendation against client's stated timeline and objectives
- **Behavioral Finance**: Distinguishes between temporary discomfort and fundamental risk tolerance change
- **Professional Guidance**: Provides advisor with data to have confident, client-centric conversations
- **Alternative Solutions**: Offers compromise options if client has concerns

---

### Scenario Wrap-up

**Business Impact Summary**:
- **Portfolio Management Efficiency**: 3-5x faster portfolio analysis and rebalancing recommendations
- **Proactive Monitoring**: Automated drift detection across entire client book
- **Client Communication**: AI-synthesized meeting preparation from unstructured notes
- **Risk Management**: Early identification of concentration and allocation issues
- **Regulatory Compliance**: Documented model alignment and suitability

**Technical Differentiators**:
- **Real-Time Holdings Analysis**: Current positions and valuations with allocation calculations
- **Model Portfolio Intelligence**: Sophisticated comparison across portfolio strategies
- **Tax-Aware Recommendations**: Automatic calculation of tax implications
- **Meeting Note Synthesis**: AI extraction of key decisions from unstructured documents
- **What-If Scenario Modeling**: Instant trade recommendations for rebalancing

---

[← Back to Demo Scenarios Index](../demo_scenarios.md)

