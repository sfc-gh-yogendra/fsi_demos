# Glacier First Bank AI Intelligence Demo

An enterprise-wide banking AI demo showcasing Snowflake's Cortex AI capabilities across compliance, commercial banking, and wealth management.

## Overview

A comprehensive demonstration of AI-powered financial services intelligence, showcasing **7 end-to-end scenarios** spanning:

**Phase 1 - AML/KYC Compliance & Risk (5 scenarios)**:
- **AML/KYC Enhanced Due Diligence**: Automated compliance analysis with cross-domain intelligence
- **Credit Risk Analysis**: Sophisticated loan origination assessment with cohort analysis
- **Transaction Monitoring & Alert Triage**: ML-based false positive reduction and priority scoring
- **Periodic KYC Reviews**: Automated change detection and low-touch review processing
- **Network Analysis for TBML Detection**: Graph-based shell company identification and Trade-Based Money Laundering detection

**Phase 2 - Commercial & Wealth Banking (2 scenarios)**:
- **Corporate Relationship Manager**: Proactive client intelligence with AI-powered opportunity discovery
- **Wealth Advisor**: Portfolio alignment monitoring with what-if rebalancing analysis  

## Prerequisites

### Snowflake Requirements
- **Snowflake Intelligence** [enabled](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence) for your account
- **Cross-Region Inference** [enabled](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference) (minimum: AWS_EU, preferred: ANY_REGIONS)
- Database and warehouse creation privileges

### Local Environment
- **Python 3.10+** (required for Snowpark compatibility)
- **Snowflake connection** configured in `~/.snowflake/connections.toml`

```bash
# Install dependencies
pip install -r requirements.txt
```

**Example connection configuration**:
```toml
[my_connection]
account = "your-account.snowflakecomputing.com"
user = "your-username"
password = "your-password"  # or use SSO/key-pair/OAuth
database = "BANK_AI_DEMO"
schema = "RAW_DATA"
warehouse = "BANK_AI_DEMO_COMPUTE_WH"
```

## Quick Start

Deploy the complete demo environment with a single command:

```bash
# Full deployment with demo-scale data
python python/main.py --connection your_connection_name

# Quick test deployment with minimal data
python python/main.py --connection your_connection_name --scale mini
```

### Deployment Options

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `--connection` | string | *required* | Snowflake connection name from connections.toml |
| `--scale` | `mini`, `demo`, `full` | `demo` | Data generation scale |
| `--no-validate` | flag | false | Skip validation tests after deployment |
| `--data-only` | flag | false | Only generate data (requires existing infrastructure) |
| `--validate-only` | flag | false | Only run validation (check existing deployment) |

### Data Scale Options

| Scale | Entities | Transactions | Documents | Alerts | CRM/Opportunities | Holdings | Use Case |
|-------|----------|--------------|-----------|--------|-------------------|----------|----------|
| `mini` | 50 | 5,000 | 250 | 50 | 20/30 | 200 | Quick testing |
| `demo` | 500 | 50,000 | 3,000 | 250 | 100/150 | 1,000 | Live demos |

**Note**: Phase 2 data (CRM, opportunities, holdings, wealth profiles) is generated when Phase 2 scenarios are requested.

## Post-Deployment Setup

### 1. Configure AI Agents
Configure all 4 agents in Snowflake Intelligence:
- **Agent 1**: AML Officer Agent (Compliance & Risk)
- **Agent 2**: Credit Analyst Agent (Credit Risk)
- **Agent 3**: Corporate RM Agent (Commercial Banking) *Phase 2*
- **Agent 4**: Wealth Advisor Agent (Wealth Management) *Phase 2*

📖 **See**: [docs/agent_setup.md](docs/agent_setup.md)

### 2. Run Demo Scenarios  
Review the guided demo flows for all 7 scenarios and practice with sample queries.

📖 **See**: [docs/demo_scenarios.md](docs/demo_scenarios.md)

## Demo Scenarios

### Phase 1: AML/KYC Compliance & Credit Risk (Implemented)

| Scenario | Agent | Key Capabilities | Business Impact |
|----------|-------|------------------|-----------------|
| **AML/KYC Enhanced Due Diligence** | `aml_officer_agent` | • Automated compliance analysis<br>• Beneficial ownership extraction<br>• Adverse media screening<br>• PEP identification<br>• Cross-domain risk assessment | EDD time: 4-6 hrs → 15-20 mins |
| **Credit Risk Analysis** | `credit_analyst_agent` | • Financial ratio analysis<br>• Policy threshold flagging<br>• Historical cohort modeling<br>• Document analysis<br>• Multi-step reasoning | Credit analysis: 2-3 days → 2-3 hrs |
| **Transaction Monitoring & Alert Triage** | `aml_officer_agent` | • ML-based priority scoring<br>• False positive reduction (50-70%)<br>• Network analysis<br>• Automated SAR generation<br>• Contextual investigation | Investigation: 4-6 hrs → 30-45 mins<br>50-70% FP reduction |
| **Periodic KYC Reviews** | `aml_officer_agent` | • Automated change detection<br>• Low-touch processing<br>• Sanctions/PEP screening<br>• Transaction pattern analysis<br>• Review queue management | Review time: 45-60 mins → <1 min<br>Capacity: 6-7x multiplier |
| **Network Analysis for TBML** | `aml_officer_agent` | • Shell company detection<br>• Shared director/address analysis<br>• Circular payment patterns<br>• TBML typology classification<br>• Graph-based visualization | Network analysis: weeks → hours<br>Detects coordinated schemes |

### Phase 2: Commercial & Wealth Banking (Implemented)

| Scenario | Agent | Key Capabilities | Business Impact |
|----------|-------|------------------|-----------------|
| **Corporate Relationship Manager** | `corporate_rm_agent` | • Portfolio prioritization<br>• AI-powered opportunity discovery<br>• Client intelligence synthesis<br>• Call preparation automation<br>• Cross-domain risk awareness | Opportunity discovery: 5-10x<br>Portfolio coverage: 2-3x clients<br>Revenue: Proactive engagement |
| **Wealth Advisor** | `wealth_advisor_agent` | • Portfolio drift monitoring<br>• Model alignment analysis<br>• What-if rebalancing scenarios<br>• Tax-aware recommendations<br>• Meeting history synthesis | Portfolio analysis: 3-5x faster<br>Client preparation: automated<br>Compliance: documented suitability |

### Cross-Domain Intelligence (All Scenarios)

**Enterprise-Wide Integration**: Risk contagion detection across compliance, credit, commercial, and wealth banking
- Compliance issues surface in RM portfolios
- Credit deterioration alerts wealth advisors
- Network analysis informs relationship management
- Unified client view across all business lines

### Planned Additional Scenarios (Phase 3)

| Scenario | Agent | Status |
|----------|-------|--------|
| **M&A Target Screening** | `ma_analyst_agent` | 📋 Phase 3 Roadmap |
| **Virtual Data Room Interrogation** | `due_diligence_agent` | 📋 Phase 3 Roadmap |
| **Regulatory Examination Prep** | `aml_officer_agent` | 🔄 Future Enhancement |
| **Executive AML Program Reporting** | `aml_officer_agent` | 🔄 Future Enhancement |

### Key Demo Entities

**Phase 1 (AML/KYC & Credit)**:

| Entity | Country | Industry | Role in Demo |
|--------|---------|----------|--------------|
| **Global Trade Ventures S.A.** | Luxembourg | International Trade | Primary AML/KYC subject with PEP connections, structuring alert (ALERT_STRUCT_001) |
| **Innovate GmbH** | Germany | Software Services | Primary credit applicant with policy breaches |
| **Northern Supply Chain Ltd** | UK | Logistics | Shared vendor creating cross-domain risk |
| **Shell Network Entities** | Gibraltar | Import/Export | 5-entity TBML network with shared director (Anya Sharma) and common address |
| **Nordic Industries S.A.** | Various | Manufacturing | Low-touch periodic review example; also RM client with compliance concerns |

**Phase 2 (Commercial & Wealth)**:

| Entity/Client | Type | Role in Demo |
|---------------|------|--------------|
| **AutoNordic GmbH** | Corporate Client | Premium tier RM client with missed contact alert and €850K financing opportunity |
| **TechVentures S.A.** | Corporate Client | Series B funded client with €1.2M cross-sell opportunity pipeline |
| **WC_045** | Wealth Client | €2.8M AUM with 12.3% allocation drift requiring rebalancing |
| **WC_128** | Wealth Client | €5.2M AUM Growth Portfolio with high unrealized gains and tax considerations |

## Architecture

### Data Model

**Phase 1 (Compliance & Risk)**:
- **Entities & Relationships**: Companies, partnerships, ownership structures, network analysis (shared directors, addresses)
- **Financial Data**: Loan applications, transactions, historical performance
- **Transaction Monitoring**: Alerts with ML priority scoring, historical dispositions (75% FP rate for training)
- **Compliance Data**: KYC documents, adverse media, regulatory filings, periodic review schedules

**Phase 2 (Commercial & Wealth)**:
- **CRM & Opportunities**: Relationship manager data, client opportunities with revenue potential
- **Wealth Management**: Holdings, model portfolios, client profiles with risk tolerance
- **Client Documents**: Call notes, internal emails, client news articles
- **Meeting Notes**: Portfolio reviews, investment strategy discussions, rebalancing decisions

**AI Services**: 7 semantic views, 6 search services, 4 agents, cross-domain intelligence, graph-based network analysis

### Project Structure
```
bank_ai_demo/
├── python/                         # Main Python codebase
│   ├── main.py                     # Single orchestration script
│   ├── config.py                   # Configuration management
│   ├── generate_structured.py     # Structured data generation
│   ├── generate_unstructured.py   # Unstructured data generation
│   ├── create_semantic_views.py   # Cortex Analyst semantic views
│   └── create_search_services.py  # Cortex Search services
├── sql/                            # SQL scripts archive
│   └── archive/                    # Reference SQL files
├── docs/                           # Documentation
│   ├── agent_setup.md             # Agent configuration guide
│   ├── demo_scenarios.md          # Demo scenario guide
│   └── DEPLOYMENT_COMPLETE.md     # Deployment verification
├── tests/                          # Validation test suite
│   └── test_scenarios.py          # Scenario validation tests
├── research/                       # Research and development notes
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

### Configuration Defaults

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Institution** | Glacier First Bank | Demo bank name |
| **Database** | BANK_AI_DEMO | Snowflake database name |
| **Compute Warehouse** | BANK_AI_DEMO_COMPUTE_WH | Main processing warehouse |
| **Search Warehouse** | BANK_AI_DEMO_SEARCH_WH | Cortex Search dedicated warehouse |
| **Data Scale** | demo | Default data generation scale (500 entities, 50K transactions) |
| **Currency** | EUR | Euro for pan-European banking |
| **Language** | en-GB | British English for regulatory compliance |
| **LLM Model** | llama3.1-70b | Cortex Complete model for content generation |

## Troubleshooting

### Common Issues

#### Connection Problems
**Error**: `Connection failed` or `Connection name must be provided`
- **Solution**: Ensure `--connection` parameter is provided
- **Check**: Verify connection exists in `~/.snowflake/connections.toml`
- **Check**: Connection has database creation privileges

#### Cortex AI Not Available
**Error**: `Cortex Search Service does not exist`
- **Solution**: Ensure Snowflake Intelligence is enabled for your account
- **Check**: Cross-region inference is configured with AWS_EU minimum

#### Data Generation Fails
**Error**: `Database does not exist or not authorized`
- **Solution**: Ensure connection has CREATE DATABASE privileges
- **Check**: Warehouse exists and is accessible

#### Validation Tests Fail
- **Solution**: Run with `--no-validate` to skip tests
- **Check**: All semantic views and search services were created successfully

### Debug Mode
```bash
# Run with minimal scale for testing
python python/main.py --connection your_connection --scale mini

# Check deployment logs
tail -f glacier_demo.log

# Validate specific components
python python/main.py --connection your_connection --validate-only
```

### Performance Optimization
```sql
-- Monitor query performance
SELECT query_text, execution_time, warehouse_name
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY 
WHERE database_name = 'BANK_AI_DEMO'
ORDER BY start_time DESC LIMIT 10;

-- Refresh search services if needed
ALTER CORTEX SEARCH SERVICE compliance_docs_search_svc REFRESH;
```

## Success Criteria

**Phase 1 Deployment** is successful when:
- ✅ All Phase 1 validation tests pass
- ✅ Key entities exist (Global Trade Ventures, Innovate GmbH, Northern Supply Chain, Shell Network)
- ✅ Cross-domain relationships established
- ✅ Transaction monitoring alerts generated (including ALERT_STRUCT_001 for GTV)
- ✅ Shell company network created (5 entities with shared director/address)
- ✅ Periodic review dates set (8+ medium-risk customers due within 30 days)
- ✅ Policy breaches correctly flagged (Innovate GmbH financial ratios)
- ✅ 5 semantic views and 4 search services operational
- ✅ Multi-step reasoning workflows complete successfully across all 5 Phase 1 scenarios

**Phase 2 Deployment** (if Phase 2 scenarios requested) adds:
- ✅ CRM data with relationship manager assignments and opportunities
- ✅ Wealth client profiles with model portfolio assignments
- ✅ Holdings data with allocation percentages and unrealized gains
- ✅ Client documents (call notes, emails, news) searchable
- ✅ Wealth meeting notes searchable
- ✅ Corporate client 360 and wealth client semantic views operational
- ✅ 2 additional search services (client documents, wealth meeting notes)
- ✅ Phase 2 agents configured and validated

## Key Technical Differentiators

This demo showcases Snowflake's unique capabilities for enterprise-wide AI in financial services:

| Capability | Implementation | Business Value |
|------------|----------------|----------------|
| **ML-Based Alert Triage** | Historical disposition data (75% FP rate) trains priority scoring models | 50-70% reduction in false positives |
| **Graph-Based Network Analysis** | Entity relationships with shared characteristics (directors, addresses) | Detects coordinated schemes traditional monitoring misses |
| **Automated Change Detection** | Review date tracking with transaction pattern baselines | 6-7x productivity multiplier for periodic reviews |
| **AI-Powered Opportunity Discovery** | NLP extraction from unstructured documents (call notes, emails, news) | 5-10x improvement in cross-sell identification |
| **Portfolio Intelligence** | Real-time drift monitoring with tax-aware rebalancing calculations | 3-5x faster portfolio analysis and what-if modeling |
| **Enterprise Cross-Domain Intelligence** | Unified data platform connecting compliance, credit, commercial, and wealth | Risk contagion detection, revenue protection, unified client view |
| **Complete Audit Trails** | Source attribution for every fact, regulatory framework integration | Regulatory compliance built-in (FATF, EBA, MiFID II) |
| **Native Integration** | All AI services in Snowflake, no middleware or data movement | Simplified architecture, enterprise security, 4 agents on single platform |

## Next Steps

1. **Configure Agents**: Follow [docs/agent_setup.md](docs/agent_setup.md) to set up all 4 agents:
   - Phase 1: AML Officer Agent (7 tools) + Credit Analyst Agent (6 tools)
   - Phase 2: Corporate RM Agent (4 tools) + Wealth Advisor Agent (2 tools)
2. **Practice Scenarios**: Use [docs/demo_scenarios.md](docs/demo_scenarios.md) for guided 7-scenario demo flows
3. **Monitor Performance**: Check query times and search service health
4. **Validate Coverage**: 
   - Phase 1: Test all 5 AML/KYC scenarios with validation queries
   - Phase 2: Test both commercial and wealth scenarios
5. **Explore Cross-Domain**: Demonstrate risk contagion and enterprise-wide intelligence

---

**Ready to demonstrate the future of AI-powered financial services!** 🚀

*Showcasing 7 comprehensive scenarios across compliance, credit, commercial banking, and wealth management - the only unified AI platform delivering this breadth of financial services intelligence.*

**Phase 1**: 5 AML/KYC scenarios (Enhanced Due Diligence, Credit Analysis, Transaction Monitoring, Periodic Reviews, Network Analysis)  
**Phase 2**: 2 Commercial & Wealth scenarios (Relationship Manager Intelligence, Portfolio Advisory)  
**Enterprise Impact**: 50-70% FP reduction | 6-7x review capacity | 5-10x opportunity discovery | 3-5x portfolio analysis speed