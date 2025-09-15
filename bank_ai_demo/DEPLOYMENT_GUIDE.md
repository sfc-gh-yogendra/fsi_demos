# Glacier First Bank AI Intelligence Demo - Deployment Guide

## Quick Start Deployment

### Prerequisites
- Snowflake account with Cortex AI enabled
- Python 3.8+ with pip
- Database creation privileges
- Warehouse creation privileges

### 1. Environment Setup

```bash
# Clone and navigate to project
git clone <repository-url>
cd bank_ai_demo

# Install dependencies
pip install -r requirements.txt

# Set connection (choose one method)
export CONNECTION_NAME="your_snowflake_connection"
# OR use --connection flag in commands below
```

### 2. One-Command Deployment

```bash
# Full deployment with demo-scale data
python deploy.py --connection your_connection_name

# Quick test deployment with minimal data
python deploy.py --scale mini

# Production deployment with full data
python deploy.py --scale full
```

### 3. Verify Deployment

The deployment script automatically validates the setup. Look for:
- ✅ All validation tests passed
- 🎉 Demo ready message
- Next steps guidance

## Deployment Options

### Scale Options

| Scale | Entities | Transactions | Documents | Use Case |
|-------|----------|--------------|-----------|----------|
| `mini` | 50 | 5,000 | 250 | Quick testing |
| `demo` | 500 | 50,000 | 2,000 | Live demos |
| `full` | 2,000 | 200,000 | 8,000 | Stress testing |

### Deployment Modes

```bash
# Infrastructure only (no data)
python deploy.py --infrastructure-only

# Data generation only (requires existing infrastructure)
python deploy.py --data-only --scale demo

# Validation only (check existing deployment)
python deploy.py --validate-only

# Skip validation (faster deployment)
python deploy.py --no-validate
```

## Manual Step-by-Step Deployment

If you prefer manual control or need to troubleshoot:

### Step 1: Database Infrastructure

```bash
# Execute SQL setup scripts
python src/main.py --connection your_connection --infrastructure-only
```

This creates:
- Database: `BANK_AI_DEMO`
- Schemas: `RAW_DATA`, `CURATED_DATA`, `SEMANTIC_LAYER`, `AGENT_FRAMEWORK`
- Warehouses: `BANK_AI_DEMO_COMPUTE_WH`, `BANK_AI_DEMO_SEARCH_WH`
- Tables: 12 core tables for entities, relationships, transactions, documents

### Step 2: Generate Demo Data

```bash
# Generate realistic demo data
python src/main.py --connection your_connection --data-only --scale demo
```

This generates:
- **Key Entities**: Global Trade Ventures S.A., Innovate GmbH, Northern Supply Chain Ltd
- **Cross-Domain Relationships**: Shared vendor dependencies for risk contagion
- **Financial Data**: Loan applications with policy breaches for credit analysis
- **Compliance Documents**: Onboarding docs, adverse media, PEP records
- **External Data Simulation**: S&P Global, Reuters, Dow Jones data patterns

### Step 3: Create Semantic Views

```sql
-- Execute semantic view creation
USE DATABASE BANK_AI_DEMO;
USE WAREHOUSE BANK_AI_DEMO_COMPUTE_WH;

-- Run sql/02_create_semantic_views.sql
```

Creates three semantic views:
- `credit_risk_sv`: Financial ratios, cohort analysis, policy thresholds
- `customer_risk_sv`: AML flags, transaction patterns, compliance status  
- `ecosystem_risk_sv`: Entity relationships, risk contagion, vendor dependencies

### Step 4: Create Search Services

```sql
-- Execute search service creation
USE WAREHOUSE BANK_AI_DEMO_SEARCH_WH;

-- Run sql/03_create_search_services.sql
```

Creates four search services:
- `compliance_docs_search_svc`: AML/KYC documents with entity/risk filtering
- `credit_policy_search_svc`: Policy documents with section/date filtering
- `loan_documents_search_svc`: Business plans with applicant/section filtering
- `news_research_search_svc`: Market intelligence with entity/source filtering

### Step 5: Validate Deployment

```bash
# Run comprehensive validation
python tests/test_scenarios.py
```

Validates:
- **AML/KYC Scenario**: Entity identification, UBO extraction, adverse media screening
- **Credit Analysis**: Ratio calculation, policy flagging, cohort analysis
- **Cross-Domain Intelligence**: Ecosystem connections, risk contagion, evidence synthesis

## Agent Configuration

After successful deployment, configure AI agents in Snowflake Intelligence:

### AML Officer Agent

```yaml
Agent Name: aml_officer_agent
Tools:
  - compliance_docs_search_svc (Cortex Search)
  - customer_risk_sv (Cortex Analyst)
Instructions: See docs/agent_instructions.md
```

### Credit Analyst Agent

```yaml
Agent Name: credit_analyst_agent  
Tools:
  - credit_risk_sv (Cortex Analyst)
  - credit_policy_search_svc (Cortex Search)
  - loan_documents_search_svc (Cortex Search)
Instructions: See docs/agent_instructions.md
```

## Demo Scenarios

### Scenario A: AML/KYC Enhanced Due Diligence

**Entity**: Global Trade Ventures S.A.

**Demo Flow**:
1. "Compile an EDD on Global Trade Ventures S.A.: structure, UBOs, adverse media."
2. "Summarise the specific allegations in Reuters_IT_Political_Scandal_20240612.txt"
3. "Draft an RFI requesting source-of-funds clarification for their €5M deposit"
4. "Provide an audit summary of all steps performed"

**Expected Features**:
- Multi-step reasoning across documents and structured data
- PEP identification (Elena Rossi - Italian Transport Minister's daughter)
- Adverse media analysis with specific allegations and quotes
- Risk assessment with regulatory compliance considerations

### Scenario B: Credit Risk Analysis

**Entity**: Innovate GmbH

**Demo Flow**:
1. "Analyse Innovate GmbH's credit application and highlight policy breaches"
2. "What's the 5-year default rate for Software Services companies with D/E >3.0?"
3. "Summarise the 'Market Strategy' section of Innovate GmbH's business plan"
4. "How does Northern Supply Chain Ltd affect our portfolio risk exposure?"

**Expected Features**:
- Policy threshold flagging (🚨 DSCR breach, ⚠️ D/E warning, 🚨 concentration breach)
- Historical cohort analysis with statistical confidence
- Business plan document analysis with strategy assessment
- Cross-domain risk contagion through shared vendor relationships

## Troubleshooting

### Common Issues

**1. Connection Errors**
```bash
# Verify connection name
snowsql -c your_connection_name -q "SELECT CURRENT_USER()"

# Set environment variable
export CONNECTION_NAME="your_connection_name"
```

**2. Permission Issues**
```sql
-- Verify privileges
SHOW GRANTS TO USER your_username;

-- Required privileges:
-- CREATE DATABASE, CREATE WAREHOUSE, CREATE SCHEMA, CREATE TABLE
-- USAGE on CORTEX functions
```

**3. Search Service Creation Fails**
```sql
-- Check Cortex AI availability
SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', 'test');

-- Verify warehouse permissions
USE WAREHOUSE BANK_AI_DEMO_SEARCH_WH;
```

**4. Data Generation Issues**
```bash
# Use smaller scale for testing
python deploy.py --scale mini

# Check available compute
SHOW WAREHOUSES;
```

### Debug Mode

```bash
# Enable detailed logging
export LOG_LEVEL=DEBUG
python deploy.py --scale mini
```

### Validation Failures

```bash
# Run specific validation tests
python -c "
from tests.test_scenarios import *
from src.config_manager import *
from snowflake.snowpark import Session

# Create session and run specific tests
session = Session.builder.configs({'connection_name': 'your_connection'}).create()
config = GlacierDemoConfig()
validator = ScenarioValidator(session, config)

# Test specific components
print('Entity ID test:', validator._test_entity_identification())
print('Ratio analysis test:', validator._test_ratio_analysis())
"
```

## Performance Optimization

### Warehouse Sizing

```sql
-- Adjust warehouse sizes based on usage
ALTER WAREHOUSE BANK_AI_DEMO_COMPUTE_WH SET WAREHOUSE_SIZE = 'LARGE';
ALTER WAREHOUSE BANK_AI_DEMO_SEARCH_WH SET WAREHOUSE_SIZE = 'MEDIUM';
```

### Query Performance

```sql
-- Monitor query performance
SELECT 
    query_text,
    execution_time,
    warehouse_name
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY 
WHERE database_name = 'BANK_AI_DEMO'
ORDER BY start_time DESC
LIMIT 10;
```

### Search Service Optimization

```sql
-- Check search service refresh status
SHOW CORTEX SEARCH SERVICES IN BANK_AI_DEMO.AGENT_FRAMEWORK;

-- Force refresh if needed
ALTER CORTEX SEARCH SERVICE compliance_docs_search_svc REFRESH;
```

## Monitoring and Maintenance

### Health Checks

```bash
# Daily validation
python deploy.py --validate-only

# Performance monitoring
python -c "
import time
from snowflake.snowpark import Session

session = Session.builder.configs({'connection_name': 'your_connection'}).create()

# Test query performance
start = time.time()
result = session.sql('SELECT COUNT(*) FROM BANK_AI_DEMO.RAW_DATA.ENTITIES').collect()
end = time.time()

print(f'Entity count: {result[0][0]}')
print(f'Query time: {end - start:.2f} seconds')
"
```

### Data Refresh

```bash
# Refresh demo data (preserves infrastructure)
python deploy.py --data-only --scale demo
```

### Backup and Recovery

```sql
-- Create backup schema
CREATE SCHEMA BANK_AI_DEMO.BACKUP_$(DATE);

-- Clone critical tables
CREATE TABLE BANK_AI_DEMO.BACKUP_$(DATE).ENTITIES 
CLONE BANK_AI_DEMO.RAW_DATA.ENTITIES;
```

## Support and Resources

- **Configuration Reference**: `config/glacier_demo_config.yaml`
- **Agent Instructions**: `docs/agent_instructions.md`
- **API Documentation**: Generated from source code docstrings
- **Performance Benchmarks**: Target response times in README.md
- **Architecture Overview**: Cross-domain intelligence patterns in rules

## Success Criteria

Deployment is successful when:
- ✅ All validation tests pass (100% success rate)
- ✅ Key entities exist (Global Trade Ventures, Innovate GmbH, Northern Supply Chain)
- ✅ Cross-domain relationships established (shared vendor dependencies)
- ✅ Policy breaches correctly flagged (Innovate GmbH financial ratios)
- ✅ Search services return relevant results for business queries
- ✅ Semantic views support complex analytical queries
- ✅ Multi-step reasoning workflows complete successfully

---

**Ready to demonstrate the future of AI-powered financial services!** 🚀
