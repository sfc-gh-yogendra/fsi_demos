# Glacier First Bank AI Intelligence Demo

A comprehensive AI-powered banking intelligence demo showcasing Snowflake's Cortex AI capabilities for financial services, featuring cross-domain risk analysis, multi-step reasoning, and contradictory evidence synthesis.

**This demo focuses on implementing complete end-to-end scenarios with realistic data generation. Check the "Available Demo Scenarios" section for implementation status. NOT IMPLEMENTED scenarios have no supporting data or objects created.**

**Architecture**: The demo uses a modern, functional Python architecture with module-level configuration, table validation, and single-script orchestration for reliable, repeatable deployments.

## High Level Overview

This demo implements Phase 1 of the Glacier First Bank AI Intelligence platform, focusing on:

- **AML/KYC Enhanced Due Diligence**: Automated compliance analysis with cross-domain intelligence
- **Credit Risk Analysis**: Sophisticated loan origination assessment with cohort analysis  
- **Cross-Domain Intelligence**: Risk contagion analysis through shared business relationships
- **Multi-Step Reasoning**: Complex analytical workflows chaining evidence from multiple sources

The platform demonstrates how financial institutions can leverage AI to automate complex analytical workflows while maintaining regulatory compliance and providing complete audit trails.

## Prerequisites

### Repository Setup
1. **Download or clone the repository**:
   ```bash
   git clone <repository-url>
   cd bank_ai_demo
   ```

2. **Navigate to the project folder**:
   ```bash
   cd bank_ai_demo
   ```

### Snowflake Prerequisites

#### Cross-Region Inference
You must have cross-region inference enabled in your Snowflake account. At minimum, you need **AWS_EU** enabled, but **ANY_REGIONS** is preferred for optimal performance.

📖 **Documentation**: [Cross-Region Inference Setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)

#### Snowflake Intelligence
Snowflake Intelligence must be enabled for your account for this demo.

📖 **Documentation**: [Snowflake Intelligence Setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence)

### Python Prerequisites

- **Python 3.10+** (required for Snowpark compatibility)
- **Install dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

### Configure Snowflake Connection

You need to ensure that `~/.snowflake/connections.toml` has a valid connection configured.

**Example connection configuration**:
```toml
[my_connection]
account = "your-account.snowflakecomputing.com"
user = "your-username"
password = "your-password"  # or use other auth methods
database = "BANK_AI_DEMO"
schema = "RAW_DATA"
warehouse = "BANK_AI_DEMO_COMPUTE_WH"
```

**Alternative authentication methods**:
- SSO/SAML
- Key pair authentication
- OAuth

Refer to [Snowflake connection documentation](https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-connect) for detailed setup instructions.

## Build Demo Environment

Deploy the complete demo environment with a single command:

```bash
# Deploy all scenarios with demo scale
python python/main.py --connection-name my_connection

# Deploy specific scenarios
python python/main.py --connection-name my_connection --scenarios aml_kyc_edd --scale demo

# Deploy only data (structured + unstructured)
python python/main.py --connection-name my_connection --scope data --scale mini

# Deploy only semantic views (requires data to exist)
python python/main.py --connection-name my_connection --scope semantic
```

### Build Parameters

| Parameter | Options | Default | Description |
|-----------|---------|---------|-------------|
| `--connection-name` | string | *required* | Snowflake connection name from connections.toml |
| `--scenarios` | `aml_kyc_edd`, `credit_analysis`, `all` | `all` | Comma-separated scenarios to build |
| `--scope` | `all`, `data`, `semantic`, `search` | `all` | Build scope (infrastructure, data, views, services) |
| `--scale` | `mini`, `demo` | `demo` | Data generation scale |
| `--no-validate` | flag | false | Skip validation tests after build |
| `--quiet` | flag | false | Suppress banner and detailed output |

## Next Steps After Build

### 1. Agent Configuration
Configure AI agents in Snowflake Intelligence using the provided templates and instructions.

📖 **See**: [docs/agent_setup.md](docs/agent_setup.md)

### 2. Demo Scenarios  
Review available demo scenarios and practice the guided demo flows.

📖 **See**: [docs/demo_scenarios.md](docs/demo_scenarios.md)

## Demo Overview

### Available Demo Scenarios

| Scenario | Agent | Status | Key Capabilities |
|----------|-------|--------|------------------|
| **AML/KYC Enhanced Due Diligence** | `aml_officer_agent` | ✅ IMPLEMENTED | • Automated compliance analysis<br>• Beneficial ownership extraction<br>• Adverse media screening<br>• PEP identification<br>• Cross-domain risk assessment |
| **Credit Risk Analysis** | `credit_analyst_agent` | ✅ IMPLEMENTED | • Financial ratio analysis<br>• Policy threshold flagging<br>• Historical cohort modeling<br>• Document analysis<br>• Multi-step reasoning |
| **Cross-Domain Intelligence** | Both agents | ✅ IMPLEMENTED | • Risk contagion analysis<br>• Shared vendor assessment<br>• Contradictory evidence synthesis<br>• Ecosystem impact analysis |
| **Investment Portfolio Risk** | `portfolio_analyst_agent` | ❌ NOT IMPLEMENTED | • Portfolio concentration analysis<br>• ESG risk assessment<br>• Market correlation analysis |
| **Fraud Detection** | `fraud_analyst_agent` | ❌ NOT IMPLEMENTED | • Transaction pattern analysis<br>• Anomaly detection<br>• Risk scoring |

### Configuration Defaults

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Institution** | Glacier First Bank | Demo bank name |
| **Database** | BANK_AI_DEMO | Snowflake database name |
| **Compute Warehouse** | BANK_AI_DEMO_COMPUTE_WH | Main processing warehouse |
| **Search Warehouse** | BANK_AI_DEMO_SEARCH_WH | Cortex Search dedicated warehouse |
| **Connection** | *Required* | No fallback - connection name must be provided |
| **Data Scale** | demo | Default data generation scale (500 entities, 50K transactions) |
| **Language** | en-GB | British English for regulatory compliance |
| **Currency** | EUR | Euro for pan-European banking |
| **Regulatory Framework** | EU/EBA | European Banking Authority standards |
| **LLM Model** | llama3.1-70b | Cortex Complete model for content generation |
| **Generation Seed** | 42 | Reproducible data generation |

**Configuration Management**: Python-based module-level configuration in `python/config.py` with direct variable access and helper functions.

### Architecture Approach

The demo follows a **functional, module-based architecture**:

- ✅ **Module-Level Functions**: No classes - all functionality as standalone functions
- ✅ **Direct Configuration Access**: `import config` → `config.INSTITUTION_NAME`
- ✅ **Separate Concerns**: Distinct modules for structured data, unstructured data, views, and services
- ✅ **Table Validation**: Pre-creation checks ensure all dependencies exist
- ✅ **Single Orchestration**: One `main.py` script manages entire deployment
- ✅ **Required Connections**: No fallback connections - explicit security-first approach

## Project Structure

```
bank_ai_demo/
├── python/                          # Main Python codebase
│   ├── main.py                      # Single orchestration script
│   ├── config.py                    # Module-level configuration
│   ├── generate_structured.py      # Structured data generation
│   ├── generate_unstructured.py    # Unstructured data generation
│   ├── create_semantic_views.py    # Cortex Analyst semantic views
│   └── create_search_services.py   # Cortex Search services
├── sql/                             # SQL archive and reference
│   └── archive/                     # Archived SQL files (reference only)
│       ├── 01_setup_database.sql
│       ├── 02_create_semantic_views.sql
│       ├── 03_create_search_services.sql
│       └── 04_create_pdf_generator.sql
├── tests/                           # Validation test suite
│   └── test_scenarios.py           # Scenario validation tests
├── docs/                           # Documentation
│   ├── agent_setup.md              # Agent configuration guide
│   ├── demo_scenarios.md           # Demo scenario guide
│   ├── DEPLOYMENT_COMPLETE.md      # Deployment verification
│   └── DEPLOYMENT_GUIDE.md         # Detailed deployment guide
├── research/                       # Research and development notes
├── .cursor/                        # Cursor IDE rules and templates
│   └── rules/                      # Code generation rules
├── requirements.txt                # Python dependencies
├── .gitignore                      # Git ignore patterns
└── README.md                       # This file
```

## Data Architecture

### Core Data Model

The demo uses a realistic banking data model with cross-domain relationships:

#### **Entities & Relationships**
- **Entities**: Companies, organizations, and individuals
- **Entity Relationships**: Business partnerships, vendor relationships, ownership structures
- **Customers**: Bank customers linked to entities

#### **Financial Data**
- **Loan Applications**: Credit applications with financial ratios and policy checks
- **Historical Loans**: Past loan performance for cohort analysis
- **Transactions**: Banking transactions with risk scoring

#### **Compliance Data**
- **Compliance Documents**: KYC documents, onboarding records, due diligence reports
- **News & Research**: Adverse media, regulatory updates, market analysis
- **External Data**: Simulated marketplace data (S&P Global, Reuters, Dow Jones)

#### **AI Services**
- **Semantic Views**: 5 views supporting complex analytical queries (created via Python)
- **Search Services**: 5 services for unstructured document analysis (created via Python)
- **Cross-Domain Intelligence**: Shared relationships enabling risk contagion analysis
- **PDF Generation**: Custom Snowpark stored procedure for report generation

### Key Demo Entities

| Entity | Country | Industry | Role in Demo |
|--------|---------|----------|--------------|
| **Global Trade Ventures S.A.** | Luxembourg | International Trade | Primary AML/KYC subject |
| **Innovate GmbH** | Germany | Software Services | Primary credit applicant |
| **Northern Supply Chain Ltd** | UK | Logistics | Shared vendor creating cross-domain risk |

## Troubleshooting

### Common Issues

#### 1. Connection Problems
**Error**: `Connection failed` or `Connection name must be provided`
- **Solution**: Ensure `--connection-name` parameter is provided (no fallback connections)
- **Check**: Verify connection name exists in `~/.snowflake/connections.toml`
- **Check**: Connection has necessary privileges (database creation, warehouse usage)

#### 2. Cortex AI Not Available
**Error**: `Cortex Search Service does not exist` or `Semantic View not authorized`
- **Solution**: Ensure Snowflake Intelligence is enabled for your account
- **Check**: Cross-region inference is configured with AWS_EU minimum

#### 3. Data Generation Fails
**Error**: `Database does not exist or not authorized`
- **Solution**: Ensure connection has CREATE DATABASE privileges
- **Check**: Warehouse exists and is accessible

#### 4. Validation Tests Fail
**Error**: Various SQL compilation errors in validation
- **Solution**: Run with `--no-validate` to skip tests, or ensure all services are created
- **Check**: All semantic views and search services were created successfully

#### 5. Table Dependencies Missing
**Error**: `Required table {table_name} does not exist`
- **Solution**: Module validates table existence before creating dependent objects
- **Check**: Run with `--scope data` first to ensure all base tables exist
- **Check**: Verify data generation completed successfully

### Support Resources

- **Agent Configuration**: [docs/agent_setup.md](docs/agent_setup.md)
- **Demo Scenarios**: [docs/demo_scenarios.md](docs/demo_scenarios.md)
- **Deployment Guide**: [docs/DEPLOYMENT_GUIDE.md](docs/DEPLOYMENT_GUIDE.md)

### Getting Help

1. Check deployment logs: `tail -f glacier_demo.log`
2. Validate prerequisites are met
3. Try minimal scale deployment: `--scale mini`
4. Review connection configuration

---

## License

This demo is provided for educational and demonstration purposes. See LICENSE file for details.