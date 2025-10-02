# Glacier First Bank AI Intelligence Demo

A banking demo showcasing Snowflake's Cortex AI capabilities for financial services, featuring cross-domain risk analysis and contradictory evidence synthesis.

## Overview
The following scenarios are currently implemented, see futher down for planned addtional ones.

- **AML/KYC Enhanced Due Diligence**: Automated compliance analysis with cross-domain intelligence
- **Credit Risk Analysis**: Sophisticated loan origination assessment with cohort analysis  

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

| Scale | Entities | Transactions | Documents | Use Case |
|-------|----------|--------------|-----------|----------|
| `mini` | 50 | 5,000 | 250 | Quick testing |
| `demo` | 500 | 50,000 | 2,000 | Live demos |
| `full` | 2,000 | 200,000 | 8,000 | Stress testing |

## Post-Deployment Setup

### 1. Configure AI Agents
Configure the AML Officer and Credit Analyst agents in Snowflake Intelligence using the provided templates.

📖 **See**: [docs/agent_setup.md](docs/agent_setup.md)

### 2. Run Demo Scenarios  
Review the guided demo flows and practice with sample queries.

📖 **See**: [docs/demo_scenarios.md](docs/demo_scenarios.md)

## Demo Scenarios

### Currently Implemented

| Scenario | Agent | Key Capabilities |
|----------|-------|------------------|
| **AML/KYC Enhanced Due Diligence** | `aml_officer_agent` | • Automated compliance analysis<br>• Beneficial ownership extraction<br>• Adverse media screening<br>• PEP identification<br>• Cross-domain risk assessment |
| **Credit Risk Analysis** | `credit_analyst_agent` | • Financial ratio analysis<br>• Policy threshold flagging<br>• Historical cohort modeling<br>• Document analysis<br>• Multi-step reasoning |
| **Cross-Domain Intelligence** | Both agents | • Risk contagion analysis<br>• Shared vendor assessment<br>• Contradictory evidence synthesis<br>• Ecosystem impact analysis |

### Planned Additional Scenarios

| Scenario | Agent | Status |
|----------|-------|--------|
| **Investment Portfolio Risk** | `portfolio_analyst_agent` | ❌ Not implemented |
| **Fraud Detection** | `fraud_analyst_agent` | ❌ Not implemented |

### Key Demo Entities

| Entity | Country | Industry | Role in Demo |
|--------|---------|----------|--------------|
| **Global Trade Ventures S.A.** | Luxembourg | International Trade | Primary AML/KYC subject with PEP connections |
| **Innovate GmbH** | Germany | Software Services | Primary credit applicant with policy breaches |
| **Northern Supply Chain Ltd** | UK | Logistics | Shared vendor creating cross-domain risk |

## Architecture

### Data Model
- **Entities & Relationships**: Companies, partnerships, ownership structures
- **Financial Data**: Loan applications, transactions, historical performance  
- **Compliance Data**: KYC documents, adverse media, regulatory filings
- **AI Services**: 3 semantic views, 4 search services, cross-domain intelligence

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

Deployment is successful when:
- ✅ All validation tests pass
- ✅ Key entities exist (Global Trade Ventures, Innovate GmbH, Northern Supply Chain)  
- ✅ Cross-domain relationships established
- ✅ Policy breaches correctly flagged (Innovate GmbH financial ratios)
- ✅ Search services return relevant results
- ✅ Multi-step reasoning workflows complete successfully

## Next Steps

1. **Configure Agents**: Follow [docs/agent_setup.md](docs/agent_setup.md)
2. **Practice Scenarios**: Use [docs/demo_scenarios.md](docs/demo_scenarios.md) 
3. **Monitor Performance**: Check query times and search service health
4. **Scale Up**: Use `--scale full` for stress testing

---

**Ready to demonstrate the future of AI-powered financial services!** 🚀