# Glacier First Bank AI Intelligence Demo

A comprehensive AI-powered banking intelligence demo showcasing Snowflake's Cortex AI capabilities for financial services, featuring cross-domain risk analysis, multi-step reasoning, and contradictory evidence synthesis.

## Overview

This demo implements Phase 1 of the Glacier First Bank AI Intelligence platform, focusing on:

- **AML/KYC Enhanced Due Diligence**: Automated compliance analysis with cross-domain intelligence
- **Credit Risk Analysis**: Sophisticated loan origination assessment with cohort analysis
- **Cross-Domain Intelligence**: Risk contagion analysis through shared business relationships
- **Multi-Step Reasoning**: Complex analytical workflows chaining evidence from multiple sources

## Architecture

### Core Components

- **Configuration Management**: Unified YAML-based configuration system
- **Data Generation**: Realistic demo data with cross-domain relationships
- **Semantic Views**: Cortex Analyst views for structured data analysis
- **Search Services**: Cortex Search for unstructured document analysis
- **Agent Framework**: AI agents with sophisticated reasoning capabilities

### Key Features

- **Realistic Business Scenarios**: Authentic financial services use cases
- **Cross-Domain Intelligence**: Shared ecosystem relationships creating risk contagion
- **Contradictory Evidence Synthesis**: Balanced analysis of conflicting signals
- **External Data Integration**: Simulated marketplace data providers
- **Multi-Step Reasoning**: Transparent analytical workflows with audit trails

## Quick Start

### Prerequisites

- Snowflake account with Cortex AI enabled
- Python 3.8+ with Snowflake Snowpark
- Access to create databases, warehouses, and Cortex services

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd bank_ai_demo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure connection**:
   ```bash
   export CONNECTION_NAME="your_snowflake_connection"
   ```

4. **Run complete setup**:
   ```bash
   python src/main.py --scale demo
   ```

### Configuration

The demo uses a unified configuration system in `config/glacier_demo_config.yaml`:

```yaml
global:
  institution_name: "Glacier First Bank"
  language: "en-GB"
  currency: "EUR"
  snowflake:
    database: "BANK_AI_DEMO"
    compute_warehouse: "BANK_AI_DEMO_COMPUTE_WH"
    search_warehouse: "BANK_AI_DEMO_SEARCH_WH"

data_generation:
  default_scale: "demo"
  scales:
    mini: { entities: 50, transactions: 5000 }
    demo: { entities: 500, transactions: 50000 }
    full: { entities: 2000, transactions: 200000 }
```

## Demo Scenarios

### Scenario A: AML/KYC Enhanced Due Diligence

**Agent**: `aml_officer_agent`  
**Entity**: Global Trade Ventures S.A.

**Demo Flow**:
1. **Initial EDD Investigation**: Compile corporate structure, UBOs, and adverse media
2. **Deep Dive Analysis**: Examine specific allegations and assess relevance
3. **Regulatory Communication**: Draft RFI for source-of-funds clarification
4. **Audit Trail**: Provide complete audit summary with evidence sources

**Key Features**:
- Multi-step reasoning across structured and unstructured data
- PEP identification and risk assessment
- Contradictory evidence synthesis
- Regulatory compliance documentation

### Scenario B: Credit Risk Analysis

**Agent**: `credit_analyst_agent`  
**Entity**: Innovate GmbH

**Demo Flow**:
1. **Initial Credit Assessment**: Analyze financial metrics and identify policy breaches
2. **Historical Cohort Analysis**: Compare against similar risk profiles
3. **Document Analysis**: Review business plan and strategy assessment
4. **Cross-Domain Integration**: Assess shared vendor risks and portfolio impact

**Key Features**:
- Policy threshold flagging with severity indicators
- Historical cohort performance analysis
- Business plan document analysis
- Cross-domain risk contagion assessment

## Cross-Domain Intelligence

### Shared Ecosystem Connections

The demo features realistic business relationships that create authentic risk scenarios:

- **Northern Supply Chain Ltd**: Shared logistics partner affecting multiple clients
- **Regulatory Cascade**: ESG directives impacting both compliance and credit operations
- **Industry Clustering**: Correlated risks across similar business sectors

### Multi-Step Reasoning Examples

```sql
-- Example: Cross-domain risk assessment
WITH vendor_exposure AS (
    SELECT * FROM SEMANTIC_VIEW(
        ecosystem_risk_sv
        METRICS average_risk_impact, relationship_count
        DIMENSIONS primary_entity_name, related_entity_name
        FILTERS relationship_type = 'VENDOR'
    )
),
credit_impact AS (
    SELECT * FROM SEMANTIC_VIEW(
        credit_risk_sv
        METRICS dscr, debt_to_equity, client_concentration
        DIMENSIONS applicant_name
    )
)
SELECT * FROM vendor_exposure v
JOIN credit_impact c ON v.primary_entity_name = c.applicant_name;
```

## Data Model

### Core Entities

- **Global Trade Ventures S.A.** (Luxembourg): Primary AML/KYC subject with PEP connections
- **Innovate GmbH** (Germany): Primary credit applicant with policy breaches
- **Northern Supply Chain Ltd** (UK): Shared vendor creating cross-domain risk

### Key Relationships

```yaml
risk_contagion_network:
  northern_supply_chain:
    clients:
      - global_trade_ventures: { dependency: "PRIMARY", impact: 0.85 }
      - innovate_gmbh: { dependency: "SECONDARY", impact: 0.45 }
      - eurotech_industries: { dependency: "REGIONAL", impact: 0.25 }
```

### External Data Simulation

The demo simulates realistic external data providers:

- **S&P Global Market Intelligence**: Company financials and credit ratings
- **Reuters News Feed**: Real-time news and market updates
- **Thomson Reuters Regulatory Intelligence**: Regulatory updates and compliance guidance
- **MSCI ESG Ratings**: Sustainability metrics and ESG scores
- **Dow Jones Risk & Compliance**: Sanctions lists and PEP databases

## Agent Configuration

### AML Officer Agent

```yaml
agent_name: aml_officer_agent
tools:
  - compliance_docs_search_svc (Cortex Search)
  - customer_risk_sv (Cortex Analyst)
response_instructions: |
  Use professional en-GB banking tone. Cite all sources with IDs/titles and dates.
  Provide objective, non-speculative risk assessments.
planning_instructions: |
  For document analysis → use Cortex Search with entity/date filters.
  For risk metrics → use Cortex Analyst on customer risk semantic view.
```

### Credit Analyst Agent

```yaml
agent_name: credit_analyst_agent
tools:
  - credit_risk_sv (Cortex Analyst)
  - credit_policy_search_svc (Cortex Search)
  - loan_documents_search_svc (Cortex Search)
response_instructions: |
  Flag policy breaches with ⚠️ warnings and 🚨 breach indicators.
  Include policy references and effective dates for all thresholds.
planning_instructions: |
  For ratio analysis → use Cortex Analyst with cohort filters.
  For policy thresholds → search credit policy documents.
  For business plans → search loan documents by applicant.
```

## Validation and Testing

### Automated Validation

The setup includes comprehensive validation:

```bash
# Run validation only
python src/main.py --validate-only

# Setup with validation
python src/main.py --scale demo  # validation included by default

# Skip validation (faster setup)
python src/main.py --scale demo --no-validate
```

### Manual Testing

Test semantic views:
```sql
-- Test credit risk analysis
SELECT * FROM SEMANTIC_VIEW(
    BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
    METRICS dscr, debt_to_equity, client_concentration
    DIMENSIONS applicant_name, industry
    FILTERS applicant_name = 'Innovate GmbH'
);
```

Test search services:
```sql
-- Test compliance document search
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'BANK_AI_DEMO.AGENT_FRAMEWORK.compliance_docs_search_svc',
    '{"query": "Global Trade Ventures beneficial ownership", "limit": 3}'
);
```

## Performance Targets

- **Simple queries**: < 5 seconds
- **Complex analysis**: < 15 seconds
- **Cross-domain intelligence**: < 20 seconds
- **Document synthesis**: < 10 seconds

## Troubleshooting

### Common Issues

1. **Connection Errors**:
   ```bash
   export CONNECTION_NAME="your_connection_name"
   # or
   python src/main.py --connection your_connection_name
   ```

2. **Search Service Creation Fails**:
   - Ensure Cortex AI is enabled in your Snowflake account
   - Verify warehouse permissions for search services
   - Check that source tables have data before creating services

3. **Semantic View Errors**:
   - Validate all referenced tables exist and have data
   - Check foreign key relationships are properly defined
   - Ensure column names match exactly in semantic view definitions

4. **Data Generation Issues**:
   - Use smaller scale for testing: `--scale mini`
   - Check available compute resources
   - Verify database and schema permissions

### Debug Mode

Enable detailed logging:
```bash
export LOG_LEVEL=DEBUG
python src/main.py --scale mini
```

## Extending the Demo

### Adding New Document Types

1. **Update configuration**:
   ```yaml
   document_generation:
     types:
       new_document_type:
         table_name: "NEW_DOCS_RAW"
         corpus_name: "NEW_DOCS_CORPUS"
         word_count_range: [500, 1000]
   ```

2. **Create search service**:
   ```sql
   CREATE CORTEX SEARCH SERVICE new_docs_search_svc
       ON CONTENT
       ATTRIBUTES ID, TITLE, CATEGORY
       WAREHOUSE = BANK_AI_DEMO_SEARCH_WH
       AS SELECT ID, TITLE, CONTENT, CATEGORY FROM NEW_DOCS_RAW;
   ```

### Adding New Entities

Update key entities in configuration:
```yaml
data_generation:
  key_entities:
    new_entity:
      entity_id: "NEW_001"
      name: "New Entity Ltd"
      country: "GBR"
      industry: "Technology"
```

## Support and Documentation

- **Configuration Reference**: See `config/glacier_demo_config.yaml` for all options
- **API Documentation**: Generated from docstrings in source code
- **Architecture Diagrams**: Available in `docs/` directory
- **Performance Benchmarks**: See `docs/performance.md`

## License

This demo is provided for educational and demonstration purposes. See LICENSE file for details.

---

**Glacier First Bank AI Intelligence Demo** - Showcasing the future of AI-powered financial services with Snowflake Cortex AI.
