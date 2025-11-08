# Glacier First Bank AI Intelligence Demo

An enterprise-wide banking AI demo showcasing Snowflake's Cortex AI capabilities across compliance, commercial banking, and wealth management.

## Overview

A comprehensive demonstration of AI-powered financial services intelligence, showcasing **7 end-to-end scenarios** spanning:

**AML/KYC Compliance & Risk (5 scenarios)**:
- **AML/KYC Enhanced Due Diligence**: Automated compliance analysis with cross-domain intelligence
- **Credit Risk Analysis**: Sophisticated loan origination assessment with cohort analysis
- **Transaction Monitoring & Alert Triage**: ML-based false positive reduction and priority scoring
- **Periodic KYC Reviews**: Automated change detection and low-touch review processing
- **Network Analysis for TBML Detection**: Graph-based shell company identification and Trade-Based Money Laundering detection

**Commercial & Wealth Banking (2 scenarios)**:
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
schema = "CURATED"
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

## Post-Deployment Setup

### 1. Access AI Agents
All 7 agents are automatically created during deployment. Access them in Snowflake Intelligence:
- **AML Officer Agent** (Compliance & Risk) - 7 tools
- **Credit Analyst Agent** (Credit Risk) - 6 tools
- **Transaction Monitoring Agent** (Alert Triage) - 5 tools
- **Cross-Domain Intelligence Agent** (Enterprise Intelligence) - 4 tools
- **Network Analysis Agent** (TBML Detection) - 3 tools
- **Corporate RM Agent** (Commercial Banking) - 4 tools
- **Wealth Advisor Agent** (Wealth Management) - 2 tools

### 2. Run Demo Scenarios  
Review the guided demo flows for all 7 scenarios with sample queries and key demo entities.

📖 **See**: [docs/demo_scenarios.md](docs/demo_scenarios.md)

## Demo Scenarios

### AML/KYC Compliance & Credit Risk

| Scenario | Agent | Key Capabilities | Business Impact |
|----------|-------|------------------|-----------------|
| **AML/KYC Enhanced Due Diligence** | `BD_aml_officer_agent` | • Automated compliance analysis<br>• Beneficial ownership extraction<br>• Adverse media screening<br>• PEP identification<br>• Cross-domain risk assessment | EDD time: 4-6 hrs → 15-20 mins |
| **Credit Risk Analysis** | `BD_credit_analyst_agent` | • Financial ratio analysis<br>• Policy threshold flagging<br>• Historical cohort modeling<br>• Document analysis<br>• Multi-step reasoning | Credit analysis: 2-3 days → 2-3 hrs |
| **Transaction Monitoring & Alert Triage** | `BD_transaction_monitoring_agent` | • ML-based priority scoring<br>• False positive reduction (50-70%)<br>• Network analysis<br>• Automated SAR generation<br>• Contextual investigation | Investigation: 4-6 hrs → 30-45 mins<br>50-70% FP reduction |
| **Periodic KYC Reviews** | `BD_aml_officer_agent` | • Automated change detection<br>• Low-touch processing<br>• Sanctions/PEP screening<br>• Transaction pattern analysis<br>• Review queue management | Review time: 45-60 mins → <1 min<br>Capacity: 6-7x multiplier |
| **Network Analysis for TBML** | `BD_network_analysis_agent` | • Shell company detection<br>• Shared director/address analysis<br>• Circular payment patterns<br>• TBML typology classification<br>• Graph-based visualization | Network analysis: weeks → hours<br>Detects coordinated schemes |

### Commercial & Wealth Banking

| Scenario | Agent | Key Capabilities | Business Impact |
|----------|-------|------------------|-----------------|
| **Corporate Relationship Manager** | `BD_corp_rm_agent` | • Portfolio prioritization<br>• AI-powered opportunity discovery<br>• Client intelligence synthesis<br>• Call preparation automation<br>• Cross-domain risk awareness | Opportunity discovery: 5-10x<br>Portfolio coverage: 2-3x clients<br>Revenue: Proactive engagement |
| **Wealth Advisor** | `BD_wealth_advisor_agent` | • Portfolio drift monitoring<br>• Model alignment analysis<br>• What-if rebalancing scenarios<br>• Tax-aware recommendations<br>• Meeting history synthesis | Portfolio analysis: 3-5x faster<br>Client preparation: automated<br>Compliance: documented suitability |

### Cross-Domain Intelligence (All Scenarios)

**Enterprise-Wide Integration**: Risk contagion detection across compliance, credit, commercial, and wealth banking
- Compliance issues surface in RM portfolios
- Credit deterioration alerts wealth advisors
- Network analysis informs relationship management
- Unified client view across all business lines

### Future Scenario Roadmap

| Scenario | Agent | Status |
|----------|-------|--------|
| **M&A Target Screening** | `ma_analyst_agent` | 📋 Planned |
| **Virtual Data Room Interrogation** | `due_diligence_agent` | 📋 Planned |
| **Regulatory Examination Prep** | `BD_aml_officer_agent` | 🔄 Future Enhancement |
| **Executive AML Program Reporting** | `BD_aml_officer_agent` | 🔄 Future Enhancement |

### Key Demo Entities

**AML/KYC & Credit Scenarios**:

| Entity | Country | Industry | Role in Demo |
|--------|---------|----------|--------------|
| **Global Trade Ventures S.A.** | Luxembourg | International Trade | Primary AML/KYC subject with PEP connections, structuring alert (ALERT_STRUCT_001) |
| **Innovate GmbH** | Germany | Software Services | Primary credit applicant with policy breaches |
| **Northern Supply Chain Ltd** | UK | Logistics | Shared vendor creating cross-domain risk |
| **Shell Network Entities** | Gibraltar | Import/Export | 5-entity TBML network with shared director (Anya Sharma) and common address |
| **Nordic Industries S.A.** | Various | Manufacturing | Low-touch periodic review example; also RM client with compliance concerns |

**Commercial & Wealth Scenarios**:

| Entity/Client | Type | Role in Demo |
|---------------|------|--------------|
| **AutoNordic GmbH** | Corporate Client | Premium tier RM client with missed contact alert and €850K financing opportunity |
| **TechVentures S.A.** | Corporate Client | Series B funded client with €1.2M cross-sell opportunity pipeline |
| **WC_045** | Wealth Client | €2.8M AUM with 12.3% allocation drift requiring rebalancing |
| **WC_128** | Wealth Client | €5.2M AUM Growth Portfolio with high unrealized gains and tax considerations |

## Architecture

### Schema Organization

**RAW_DATA**: Temporary/working tables for data generation
- Source tables: ENTITIES, CUSTOMERS, TRANSACTIONS
- Temporary prompt tables for LLM generation
- Tables not directly consumed by AI services

**CURATED**: All tables consumed by AI services  
- Structured analytics tables: ENTITY_RELATIONSHIPS, CLIENT_OPPORTUNITIES, HOLDINGS, etc.
- Document corpus tables: COMPLIANCE_DOCUMENTS, LOAN_DOCUMENTS, CLIENT_DOCUMENTS, etc.
- Supporting views: customer_risk_view, alert_summary_view, etc.

**AI**: AI infrastructure components
- 7 Semantic views (Cortex Analyst)
- 7 Search services (Cortex Search)
- 7 Agents (Snowflake Intelligence)
- Custom tools (stored procedures)

### Data Model

**Compliance & Risk**:
- **Entities & Relationships**: Companies, partnerships, ownership structures, network analysis (shared directors, addresses)
- **Financial Data**: Loan applications, transactions, historical performance
- **Transaction Monitoring**: Alerts with ML priority scoring, historical dispositions (75% FP rate for training)
- **Compliance Data**: KYC documents, adverse media, regulatory filings, periodic review schedules

**Commercial & Wealth**:
- **CRM & Opportunities**: Relationship manager data, client opportunities with revenue potential
- **Wealth Management**: Holdings, model portfolios, client profiles with risk tolerance
- **Client Documents**: Call notes, internal emails, client news articles
- **Meeting Notes**: Portfolio reviews, investment strategy discussions, rebalancing decisions

**AI Infrastructure**: 7 semantic views, 7 search services, 7 agents, cross-domain intelligence, graph-based network analysis

### Project Structure
```
bank_ai_demo/
├── python/                         # Main Python codebase
│   ├── main.py                     # Single orchestration script
│   ├── config.py                   # Configuration management
│   ├── generate_structured.py     # Structured data generation
│   ├── generate_unstructured.py   # Unstructured data generation
│   ├── create_semantic_views.py   # Cortex Analyst semantic views
│   ├── create_search_services.py  # Cortex Search services
│   └── create_agents.py            # Snowflake Intelligence agents
├── sql/                            # SQL scripts archive
│   └── archive/                    # Reference SQL files
├── docs/                           # Documentation
│   ├── demo_scenarios.md          # Demo scenario guide
│   └── scenarios/                 # Individual scenario guides
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

Deployment is successful when:
- ✅ All validation tests pass
- ✅ Key entities exist (Global Trade Ventures, Innovate GmbH, Northern Supply Chain, Shell Network)
- ✅ Cross-domain relationships established
- ✅ Transaction monitoring alerts generated (including ALERT_STRUCT_001 for GTV)
- ✅ Shell company network created (5 entities with shared director/address)
- ✅ Periodic review dates set (8+ medium-risk customers due within 30 days)
- ✅ Policy breaches correctly flagged (Innovate GmbH financial ratios)
- ✅ 7 semantic views and 7 search services operational
- ✅ 7 agents created and configured
- ✅ Multi-step reasoning workflows complete successfully across all 7 scenarios
- ✅ CRM data with relationship manager assignments and opportunities
- ✅ Wealth client profiles with model portfolio assignments
- ✅ Holdings data with allocation percentages and unrealized gains
- ✅ Client documents (call notes, emails, news) searchable
- ✅ Wealth meeting notes searchable

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
| **Native Integration** | All AI services in Snowflake, no middleware or data movement | Simplified architecture, enterprise security, 7 agents on single platform |

## Next Steps

1. **Access Agents**: Navigate to Snowflake Intelligence → Agents to access all 7 agents with "(Bank Demo)" suffix
2. **Practice Scenarios**: Use [docs/demo_scenarios.md](docs/demo_scenarios.md) for guided demo flows with sample queries
3. **Monitor Performance**: Check query times and search service health
4. **Test Coverage**: Validate all 7 scenarios with key demo entities
5. **Explore Cross-Domain**: Demonstrate risk contagion and enterprise-wide intelligence

---

**Ready to demonstrate the future of AI-powered financial services!** 🚀

*Showcasing 7 comprehensive scenarios across compliance, credit, commercial banking, and wealth management - the only unified AI platform delivering this breadth of financial services intelligence.*

**5 AML/KYC scenarios**: Enhanced Due Diligence, Credit Analysis, Transaction Monitoring, Periodic Reviews, Network Analysis  
**2 Commercial & Wealth scenarios**: Relationship Manager Intelligence, Portfolio Advisory  
**Enterprise Impact**: 50-70% FP reduction | 6-7x review capacity | 5-10x opportunity discovery | 3-5x portfolio analysis speed