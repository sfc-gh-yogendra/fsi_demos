# Glacier First Bank - Scenario Validation Checklist

This document provides step-by-step validation procedures for all demo scenarios. Follow these procedures after deploying the demo to ensure all scenarios work as expected.

---

## Phase 1: Extended AML/KYC Foundation Validation

### Scenario C: Transaction Monitoring & Alert Triage

**Prerequisites**:
- `aml_officer_agent` configured in Snowflake Intelligence
- `transaction_monitoring_analysis` tool (Cortex Analyst on `transaction_monitoring_sv`) configured
- `aml_risk_analysis` tool available for customer profile lookups
- `compliance_docs_search` and `news_adverse_media_search` tools configured

**Validation Steps**:

#### Turn 1: ML-Based Alert Triage
**Query**: 
```
What's my highest priority alert this morning?
```

**Expected Response Elements**:
- ✅ Identifies ALERT_STRUCT_001 for Global Trade Ventures S.A.
- ✅ ML Suspicion Score: 95% (high priority)
- ✅ Alert Type: Structuring (5 cash deposits @ $9,500 each)
- ✅ Customer Risk Rating: HIGH
- ✅ Key Risk Factors listed:
  - Pattern deviates from 5-year transaction baseline
  - Amount precisely structured below $10,000 CTR threshold
  - Multi-branch execution suggests deliberate avoidance
  - Customer has 2 existing AML flags
- ✅ Recommended Action: Priority investigation required
- ✅ Demo disclaimer present

**Validation SQL** (optional - verify data exists):
```sql
SELECT ALERT_ID, CUSTOMER_ID, ALERT_TYPE, PRIORITY_SCORE, ALERT_STATUS
FROM BANK_AI_DEMO.RAW_DATA.ALERTS
WHERE ALERT_ID = 'ALERT_STRUCT_001';
```

**Acceptance Criteria**:
- Response time < 15 seconds
- All expected elements present
- Priority score displayed correctly
- Risk factors are contextual and specific

---

#### Turn 2: Contextual Investigation & Evidence Gathering
**Query**:
```
Give me the full picture on Global Trade Ventures S.A. - customer profile, recent activity, and any relevant notes.
```

**Expected Response Elements**:
- ✅ Customer Profile: Global Trade Ventures S.A., Luxembourg-based importer/exporter
- ✅ Risk Rating: HIGH (due to PEP connection - Elena Rossi, 40% UBO)
- ✅ Recent Activity: €5M wire transfer received 2 weeks ago (also flagged)
- ✅ Relationship Manager Note from KYC file: "Customer mentioned selling classic car for cash 6 months ago, expects funds soon"
- ✅ Timing Mismatch: Cash sale note was 6 months ago, deposits are happening now
- ✅ Transaction Pattern: $47,500 total across 5 branches in 2 days suggests coordinated structuring
- ✅ Risk Assessment: Note provides partial context but doesn't explain current timing or multi-branch pattern

**Validation Check**:
- Agent should use both `aml_risk_analysis` (customer profile) and `compliance_docs_search` (RM notes)
- Multi-tool orchestration demonstrated

**Acceptance Criteria**:
- 360-degree customer view assembled
- Unstructured data (RM notes) retrieved and integrated
- Temporal analysis present (6 months ago vs. now)
- Balanced risk assessment (acknowledges note but identifies gaps)

---

#### Turn 3: Network Analysis & Hidden Connections
**Query**:
```
Has Global Trade Ventures or its principals interacted with any known high-risk entities in our system?
```

**Expected Response Elements**:
- ✅ Network Analysis Result: Connection identified to 'Global Parts LLC'
- ✅ Relationship: $20,000 wire transfer from GTV to Global Parts LLC 2 weeks after cash deposits
- ✅ Prior History: Global Parts LLC was subject of SAR filing 3 months ago (trade-based money laundering suspicion)
- ✅ Risk Escalation: Connection to previously reported entity significantly elevates suspicion
- ✅ Network Graph: Visual representation shows GTV → Global Parts → offshore entities
- ✅ Recommendation: Escalate to SAR with network analysis

**Validation SQL** (optional - verify relationship exists):
```sql
SELECT * FROM BANK_AI_DEMO.RAW_DATA.ENTITY_RELATIONSHIPS
WHERE PRIMARY_ENTITY_ID = 'GTV_SA_001' OR RELATED_ENTITY_ID = 'GTV_SA_001';
```

**Acceptance Criteria**:
- Network connections discovered
- Historical intelligence cross-referenced (prior SARs)
- Risk contagion identified
- Graph visualization data available

---

#### Turn 4: Automated SAR Narrative Generation
**Query**:
```
Generate a complete draft SAR narrative incorporating all findings - the structuring pattern, the timing mismatch with the RM note, and the connection to Global Parts LLC.
```

**Expected Response Elements**:
- ✅ SAR Narrative Structure:
  - Summary: Structured cash deposits totaling $47,500 across 5 branches
  - Customer Background: Luxembourg importer/exporter, HIGH risk, PEP connection
  - Suspicious Activity: Five deposits of exactly $9,500 (below CTR threshold)
  - Pattern Analysis: Coordinated multi-branch execution suggests deliberate structuring
  - Contextual Factors: Prior RM note about car sale provides partial explanation but timing doesn't match
  - Network Connection: Subsequent wire to Global Parts LLC (prior SAR subject for TBML)
  - Conclusion: Pattern consistent with intentional currency reporting evasion, escalated by connection to known suspicious entity
- ✅ Source Citations: All findings include document IDs, dates, transaction references
- ✅ Recommendation: File SAR with FinCEN, maintain enhanced monitoring

**Acceptance Criteria**:
- Comprehensive SAR narrative generated
- All evidence sources cited
- Regulatory compliance elements present
- Complete audit trail
- Human oversight emphasized (draft for review)

---

**Overall Scenario C Success Criteria**:
- ✅ All 4 turns completed within 15 minutes total
- ✅ ML priority scoring demonstrated
- ✅ Multi-tool orchestration (Cortex Analyst + Cortex Search)
- ✅ Network analysis revealed hidden connections
- ✅ Complete audit trail with source attribution
- ✅ Professional SAR narrative generated

---

### Scenario D: Streamlined Periodic KYC Reviews

**Prerequisites**:
- `aml_officer_agent` configured in Snowflake Intelligence
- `aml_risk_analysis` tool with next_review_date filtering capability
- `compliance_docs_search` and `news_adverse_media_search` tools configured

**Validation Steps**:

#### Turn 1: Review Queue Analysis
**Query**:
```
Show me periodic reviews due this week, prioritized by risk and flag any that need manual attention.
```

**Expected Response Elements**:
- ✅ Total Reviews Due: 15 customers
- ✅ Low-Touch Eligible: 12 customers (no material changes detected)
- ✅ Manual Review Required: 3 customers (changes detected)
  - Customer A: New adverse media hit (regulatory investigation)
  - Customer B: Significant transaction pattern change (+150% volume)
  - Customer C: PEP status change (family member appointed to government role)
- ✅ Prioritization: Manual reviews ranked by severity
- ✅ Time Savings: Estimated 8-9 hours saved through automated low-touch processing
- ✅ Demo disclaimer present

**Validation SQL** (optional - verify review dates):
```sql
SELECT CUSTOMER_ID, ENTITY_NAME, RISK_RATING, NEXT_REVIEW_DATE, REVIEW_FREQUENCY_MONTHS
FROM BANK_AI_DEMO.RAW_DATA.CUSTOMERS
WHERE NEXT_REVIEW_DATE <= DATEADD(day, 7, CURRENT_DATE())
ORDER BY RISK_RATING DESC, NEXT_REVIEW_DATE;
```

**Acceptance Criteria**:
- Correct count of reviews due (15)
- Change detection logic working (12 low-touch, 3 manual)
- Risk-based prioritization
- Time savings quantified

---

#### Turn 2: Low-Touch Review Processing
**Query**:
```
Open the low-touch review for customer Nordic Industries S.A. and show me the automated check results.
```

**Expected Response Elements**:
- ✅ Customer: Nordic Industries S.A., Medium-risk manufacturing client
- ✅ Last Review: 12 months ago (annual cycle)
- ✅ Automated Checks Completed:
  - ✅ Sanctions Screening: No new hits (checked against OFAC, UN, EU lists)
  - ✅ PEP Screening: No status changes for principals or UBOs
  - ✅ Adverse Media: No new negative news articles found
  - ✅ Transaction Pattern Analysis: Activity consistent with historical baseline
    - Average monthly volume: €850K (historical: €820K, variance: +3.7%)
    - Transaction frequency: 45 transactions/month (historical: 42, variance: +7%)
    - High-risk country exposure: 0% (unchanged)
  - ✅ KYC Documents: All documents current, no expiring within 90 days
- ✅ Recommendation: Low-Touch Approval - No material changes detected
- ✅ Review Form: Pre-populated with all check results and supporting data
- ✅ Required Action: Analyst adds approval comment and submits (< 30 seconds)

**Acceptance Criteria**:
- Comprehensive automated checks performed
- Quantitative variance analysis (3.7%, 7%)
- Change detection threshold logic working
- Complete audit trail of checks

---

#### Turn 3: Approval & Efficiency Metrics
**Query**:
```
Approve this review with standard comment and show me time saved.
```

**Expected Response Elements**:
- ✅ Review Status: APPROVED
- ✅ Comment Added: "Periodic review completed via automated low-touch process. No material changes identified. All screening checks passed. Risk profile remains stable at MEDIUM rating."
- ✅ Next Review Date: Auto-calculated for 12 months (based on MEDIUM risk)
- ✅ Processing Time: 45 seconds (vs. historical average 48 minutes)
- ✅ Time Saved: 47 minutes 15 seconds per review
- ✅ Productivity Gain: Analyst can process 60+ low-touch reviews per day vs. 8-10 manual reviews
- ✅ Quality Assurance: 100% screening coverage vs. potential human oversight

**Acceptance Criteria**:
- Approval workflow complete
- Next review date calculated correctly (12 months for MEDIUM risk)
- Efficiency metrics quantified and realistic
- Quality benefits articulated

---

**Overall Scenario D Success Criteria**:
- ✅ All 3 turns completed within 15 minutes total
- ✅ Automated change detection working
- ✅ Low-touch vs. manual review logic correct
- ✅ Efficiency gains quantified (6-7x productivity multiplier)
- ✅ Review date calculations accurate

---

### Scenario E: Uncovering Trade-Based Money Laundering Networks

**Prerequisites**:
- `aml_officer_agent` configured in Snowflake Intelligence
- `network_risk_analysis` tool (Cortex Analyst on `network_analysis_sv`) configured
- `aml_risk_analysis` tool for transaction data
- `compliance_docs_search` tool for corporate structure docs

**Validation Steps**:

#### Turn 1: Network Alert Investigation
**Query**:
```
Explain this network alert involving Baltic Trade Ltd, Nordic Commerce S.A., Alpine Export GmbH, Adriatic Import Ltd, and Aegean Trade S.A.
```

**Expected Response Elements**:
- ✅ Network Alert Type: Shell Company Network / Coordinated Entity Cluster
- ✅ Entities Involved: 5 import/export companies, all incorporated in Gibraltar
- ✅ Suspicious Characteristics:
  - Shared Director: Anya Sharma (appears as director on all 5 companies)
  - Common Address: "42 Mailbox Lane, Virtual Office Complex, Gibraltar" (mail forwarding service)
  - Incorporation Timing: All 5 entities incorporated within 45-day window
  - Industry: All classified as Import/Export (common TBML typology)
  - Circular Relationships: VENDOR relationships form closed loop (A→B→C→D→E→A)
- ✅ Risk Assessment: HIGH - multiple shell company indicators present
- ✅ Typology: Suspected Trade-Based Money Laundering network
- ✅ Demo disclaimer present

**Validation SQL** (optional - verify shell network):
```sql
SELECT ENTITY_ID, ENTITY_NAME, COUNTRY_CODE, INCORPORATION_DATE
FROM BANK_AI_DEMO.RAW_DATA.ENTITIES
WHERE ENTITY_ID LIKE 'SHELL_NET_%'
ORDER BY ENTITY_ID;

SELECT * FROM BANK_AI_DEMO.RAW_DATA.ENTITY_RELATIONSHIPS
WHERE PRIMARY_ENTITY_ID LIKE 'SHELL_NET_%' OR RELATED_ENTITY_ID LIKE 'SHELL_NET_%';
```

**Acceptance Criteria**:
- All 5 shell entities identified
- Shared characteristics detected (director, address, timing)
- Circular relationship pattern recognized
- TBML typology correctly classified

---

#### Turn 2: Fund Flow Visualization
**Query**:
```
Show me the fund flow for this entire network over the last 90 days.
```

**Expected Response Elements**:
- ✅ Network Transaction Analysis:
  - Total Volume: €15.7M processed through 5-entity network in 90 days
  - Flow Pattern: Funds enter from various sources → rapid consolidation → exit to 3 offshore shell entities
  - Velocity: Average fund residence time: 48 hours (extremely rapid)
  - Beneficiaries: Final destinations are high-risk jurisdictions (BVI, Panama, Seychelles)
- ✅ Payment Chain:
  1. Multiple inbound payments to network entities (€15.7M total)
  2. Rapid circular transfers between the 5 companies (layering)
  3. Consolidation and wire-out to 3 offshore entities within 48 hours
- ✅ Red Flags:
  - No legitimate business purpose for rapid circular transfers
  - Transaction values inconsistent with declared business size
  - Immediate outflow to high-risk offshore jurisdictions
  - Pattern consistent with TBML layering and integration phases
- ✅ Graph Visualization: Animated network diagram shows money flow through circular structure

**Acceptance Criteria**:
- Total volume quantified (€15.7M)
- Flow pattern clearly described
- Velocity metrics calculated (48 hours)
- Red flags identified with regulatory context

---

#### Turn 3: Typology Classification & TBML Identification
**Query**:
```
What money laundering typology does this pattern match, and what are the specific indicators?
```

**Expected Response Elements**:
- ✅ Primary Typology: Trade-Based Money Laundering (TBML)
- ✅ Specific Variant: Shell company network with rapid layering
- ✅ TBML Indicators Present:
  - ✓ Multiple import/export entities (trade narrative cover)
  - ✓ Circular vendor relationships (no legitimate business rationale)
  - ✓ Rapid fund movement (layering phase)
  - ✓ Offshore integration (high-risk jurisdictions)
  - ✓ Shell company characteristics (shared director, virtual office, recent incorporation)
  - ✓ High velocity, low substance (funds never remain in accounts)
- ✅ Regulatory References:
  - FATF Trade-Based Money Laundering indicators
  - EU AML Directive Article 18 (shell company red flags)
- ✅ Historical Context: Similar networks identified in [jurisdiction] investigations
- ✅ Confidence Level: HIGH (8 out of 10 TBML indicators present)

**Acceptance Criteria**:
- TBML typology correctly identified
- 8+ indicators documented with evidence
- Regulatory framework references (FATF, EU AML)
- Confidence level quantified

---

#### Turn 4: Comprehensive Network SAR
**Query**:
```
Generate a comprehensive SAR covering all 5 entities, documenting the shell company structure, circular payments, and TBML typology. Also recommend account actions.
```

**Expected Response Elements**:
- ✅ Master SAR Generated:
  - Subject Entities: All 5 companies listed with full details
  - Principal: Anya Sharma (shared director across network)
  - Network Structure: Documented with corporate registry evidence
  - Transaction Analysis: €15.7M in 90 days, circular flow pattern documented
  - Typology Classification: TBML with shell company network
  - FATF Indicators: All 8 applicable indicators cited with supporting evidence
  - Timeline: 45-day incorporation → 30-day network activation → 90-day high-velocity activity
  - Beneficiaries: 3 offshore entities identified as ultimate recipients
  - Source Attribution: Complete references to corporate docs, transaction records, registry data
- ✅ Recommended Actions:
  - ⚠️ Immediate: Place holds on all outbound wires from 5 entities pending review
  - 🚨 Urgent: Escalate to Financial Intelligence Unit (FIU)
  - 📋 Administrative: Flag Anya Sharma in internal watchlist
  - 🔒 Account Action: Initiate exit procedures for all 5 entities
  - 🔍 Monitoring: Enhanced scrutiny for any new entities with Anya Sharma as director/UBO
- ✅ File Status: Ready for analyst review and submission to FinCEN/relevant FIU

**Acceptance Criteria**:
- Master SAR covers entire network (not individual entities)
- All TBML indicators documented with evidence
- Actionable recommendations provided
- Complete audit trail with source citations
- Preventive measures included (watchlist Anya Sharma)

---

**Overall Scenario E Success Criteria**:
- ✅ All 4 turns completed within 15 minutes total
- ✅ Shell company network identified (5 entities)
- ✅ Shared characteristics detected (director, address)
- ✅ TBML typology classified correctly
- ✅ Network-level analysis (not just individual entities)
- ✅ Comprehensive master SAR generated

---

## Validation Summary

### Phase 1 Extended - Acceptance Checklist

- [ ] **Scenario C: Transaction Monitoring** - All 4 turns validated
- [ ] **Scenario D: Periodic KYC Reviews** - All 3 turns validated
- [ ] **Scenario E: Network Analysis for TBML** - All 4 turns validated
- [ ] All response times < 15 minutes per scenario
- [ ] Multi-tool orchestration working across scenarios
- [ ] Complete audit trails present
- [ ] Demo disclaimers included in all responses
- [ ] Citations with source documents and dates
- [ ] Quantified efficiency gains accurate

### Next Steps After Validation

1. Document any deviations from expected responses
2. Note any performance issues or slow queries
3. Capture actual agent responses for demo script refinement
4. Update docs/agent_setup.md with any configuration adjustments
5. Proceed to Phase 1 documentation updates (Task 4)

---

**Note**: This validation must be performed in a live Snowflake Intelligence environment with configured agents. The queries and expected responses documented here serve as the validation script for live testing.

