# Snowcrest Asset Management (SAM) AI Demo - 100% Real Assets

A comprehensive demonstration of Snowflake Intelligence for asset management customers, covering Portfolio Managers, Research Analysts, Quantitative Analysts, Client Relationship Managers, and Risk & Compliance Officers.

Focus is to showcase Snowflake Intelligence/Cortex Agents using a number of scenarios that all use Agents.

## Available Scenarios by Role

### Portfolio Manager
**Agent: Portfolio Copilot**
- **Portfolio Insights & Benchmarking** ✅ **IMPLEMENTED**
  - Portfolio analytics that combines quantitative holdings data with qualitative research insights in seconds, enabling faster decision-making and better risk management.
  
- **Real-Time Event Impact & Second-Order Risk Verification** ✅ **IMPLEMENTED**
  -Event risk verification that combines macro event intelligence, direct portfolio exposure analysis, and sophisticated supply chain dependency mapping to quantify both immediate and indirect portfolio impacts in real-time.
  
- **AI-Assisted Mandate Compliance & Security Replacement** ✅ **IMPLEMENTED**
  - Compliance workflow that automatically identifies pre-screened replacement candidates, analyzes their strategic fit, and generates investment committee documentation—reducing breach response time from days to minutes.

**Agent: Thematic Macro Advisor**  
- **Investment Theme Analysis** ✅ **IMPLEMENTED**
  - Thematic analysis that combines current portfolio positioning with comprehensive research synthesis to identify theme-based investment opportunities and optimize strategic allocation decisions.

### Research Analyst
**Agent: Research Copilot**
- **Document Research & Analysis** ✅ **IMPLEMENTED**
  - Research synthesis that analyzes thousands of documents across broker reports, earnings transcripts, and press releases to deliver comprehensive investment insights and market intelligence in seconds.
  
- **Earnings Intelligence Extensions** ✅ **IMPLEMENTED**
  - Earnings analysis that combines transcript commentary with financial estimates, guidance tracking, and surprise calculations to provide comprehensive quarterly earnings insights.

### Quantitative Analyst
**Agent: Quant Analyst**
- **Factor Analysis & Performance Attribution** ✅ **IMPLEMENTED**
  - Factor analysis that screens portfolios against multiple quantitative factors, tracks factor evolution over time, and generates professional investment research reports with comprehensive statistical analysis.

### Client Relations
**Agent: Sales Advisor**
- **Client Reporting & Template Formatting** ✅ **IMPLEMENTED**
  - Client reporting that synthesizes portfolio data, performance metrics, and firm philosophy into professionally formatted quarterly letters following exact template specifications.

### Risk & Compliance Officer
**Agent: ESG Guardian**
- **ESG Risk Monitoring & Policy Compliance** ✅ **IMPLEMENTED**
  - ESG monitoring that scans portfolio holdings against NGO reports and sustainability policies to identify controversies, assess severity, and recommend engagement actions aligned with firm ESG commitments.

**Agent: Compliance Advisor**
- **Mandate Monitoring & Breach Detection** ✅ **IMPLEMENTED**
  - Mandate compliance that continuously monitors portfolio positions against investment guidelines, automatically detects concentration breaches and ESG violations, and cites specific policy sections for immediate remediation.


## Quick Start

### Prerequisites

#### **Repository Setup**
- Clone or download this repository to your local machine
- Navigate to the project directory: `cd am_ai_demo`

#### **Snowflake Account**
- Cross-region inference enabled: [Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)
  - Minimum: `AWS_EU` enabled
  - Recommended: `ANY_REGIONS`
- Snowflake Intelligence enabled: [Setup Guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence)
- SEC Filings dataset: [Snowflake Marketplace](https://app.snowflake.com/marketplace/listing/GZTSZAS2KH9/snowflake-public-data-products-sec-filings)

#### **Python Environment**
- Python 3.10+
- Install dependencies: `pip install -r requirements.txt`

#### Configure Snowflake Connection
Ensure your `~/.snowflake/connections.toml` contains a valid connection profile:

```toml
[my_demo_connection]
account = "your-account"
user = "your-username" 
password = "your-password"
warehouse = "your-warehouse"
```

### Build Demo Environment (100% Real Assets)
```bash
# Build everything with 14,000+ real securities (all scenarios)
python python/main.py --connection-name my_demo_connection

# Test mode: Build with 1,400 real securities for faster development testing
python python/main.py --connection-name my_demo_connection --test-mode

# Build specific scenarios only
python python/main.py --connection-name my_demo_connection --scenarios portfolio_copilot,research_copilot

# Build only data layer
python python/main.py --connection-name my_demo_connection --scope data
```

## Next Steps After Build

### 1. Validate Build Success

Check that all components were created successfully:

```sql
-- Verify core semantic views
DESCRIBE SEMANTIC VIEW SAM_DEMO.AI.SAM_ANALYST_VIEW;

-- Test semantic view functionality  
SELECT * FROM SEMANTIC_VIEW(
    SAM_DEMO.AI.SAM_ANALYST_VIEW
    METRICS TOTAL_MARKET_VALUE
    DIMENSIONS PORTFOLIONAME
) LIMIT 5;

-- Test search services
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'SAM_DEMO.AI.SAM_BROKER_RESEARCH',
    '{"query": "technology investment", "limit": 2}'
);

-- Verify data volumes
SELECT 'Securities' as table_name, COUNT(*) as record_count FROM SAM_DEMO.CURATED.DIM_SECURITY
UNION ALL SELECT 'Issuers', COUNT(*) FROM SAM_DEMO.CURATED.DIM_ISSUER
UNION ALL SELECT 'Holdings', COUNT(*) FROM SAM_DEMO.CURATED.FACT_POSITION_DAILY_ABOR
UNION ALL SELECT 'Market Data', COUNT(*) FROM SAM_DEMO.CURATED.FACT_MARKETDATA_TIMESERIES
UNION ALL SELECT 'Documents', COUNT(*) FROM SAM_DEMO.CURATED.BROKER_RESEARCH_CORPUS;
```

**Expected Results**:
- Securities: ~14,000 (or ~1,400 in test mode)
- Issuers: ~14,800 (includes synthetic issuers for complete coverage)
- Holdings: ~27,000 positions
- Market Data: ~4M+ records
- Documents: ~2,800+ documents

### 2. Configure Agents

Follow the detailed instructions in `docs/agents_setup.md` to configure agents in Snowflake Intelligence:

1. Navigate to Snowflake Intelligence in Snowsight
2. Create new agent (e.g., `portfolio_copilot`)
3. Add tools (Cortex Analyst + Cortex Search)
4. Configure planning and response instructions

### 3. Test Agent

Quick validation query:
```
"What are my top 10 holdings by market value in the SAM Global Thematic Growth portfolio?"
```

**Expected Response**: 
- Table with Ticker, Company Name, Weight %, Market Value
- Concentration warnings for positions >6.5%
- Total exposure percentage
- Clean data with no duplicates

### 4. Run Demo Scenarios

Use the complete demo scripts in `docs/demo_scenarios.md` for professional demonstrations.

## Configuration Defaults

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Connection** | Required via `--connection-name` | Must specify connection from ~/.snowflake/connections.toml |
| **History** | 5 years | Historical data range |
| **Securities** | 14,000 real securities (1,400 test mode) | 100% authentic from OpenFIGI dataset |
| **Issuers** | 3,303 real companies | Corporate hierarchies and relationships |
| **Identifiers** | TICKER + Bloomberg FIGI | 100% authentic regulatory identifiers |
| **Language** | UK English | All generated content and agent responses |
| **Currency** | USD (fully hedged) | Base currency for all analytics |
| **Returns** | Monthly | Performance calculation frequency |
| **Real Assets** | ✅ Always Used | 14,000+ authentic securities from SEC Filings dataset |
| **Market Data** | Synthetic | Realistic OHLCV prices for all securities |
| **Test Mode** | Available | 10% data volumes for faster development |
| **Warehouses** | Dedicated | Separate warehouses for execution and Cortex Search |

## Project Structure

```
/
├── .cursor/rules/              # Cursor AI development rules (internal)
├── content_library/            # Pre-generated content templates (50+ templates)
│   ├── _rules/                 # Template configuration (placeholders, bounds, providers)
│   ├── security/               # Security-level documents (broker research, earnings, etc.)
│   ├── issuer/                 # Issuer-level documents (NGO reports, engagement notes)
│   ├── portfolio/              # Portfolio-level documents (IPS, reviews)
│   ├── global/                 # Global documents (policies, templates, market data)
│   └── regulatory/             # Regulatory documents (Form ADV, CRS, updates)
├── docs/                       # Documentation
│   ├── agents_setup.md         # Agent configuration instructions
│   ├── demo_scenarios.md       # Complete demo scripts and flows
│   ├── data_model.md           # Schema and data documentation
│   └── document_specs_*.md     # Detailed document specifications by category
├── python/                     # Python implementation
│   ├── config.py               # Configuration constants (CAPS naming)
│   ├── main.py                 # CLI orchestrator
│   ├── generate_structured.py # Structured data generation (100% real assets)
│   ├── generate_unstructured.py # Unstructured content generation (template-based)
│   ├── hydration_engine.py    # Template hydration engine
│   ├── build_ai.py            # AI components (semantic views, search services)
│   └── extract_real_assets.py # Real asset view creation from SEC Filings
├── research/                   # Background research and analysis
├── .gitignore                  # Git ignore patterns (logs, cache, backups)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Data Architecture

### Database: `SAM_DEMO`
- **RAW Schema**: External provider simulation + raw documents
- **CURATED Schema**: Industry-standard dimension/fact model
- **AI Schema**: Enhanced semantic views and Cortex Search services

## Troubleshooting

### Build Issues

**Connection Error**
```bash
Error: Could not connect to Snowflake
```
- **Solution**: Verify `~/.snowflake/connections.toml` is configured correctly
- Check connection name matches the one specified in `--connection-name`
- Test connection manually: `snowsql -c your_connection_name`

**Module Not Found**
```bash
ModuleNotFoundError: No module named 'snowflake.snowpark'
```
- **Solution**: Install dependencies: `pip install -r requirements.txt`

**SEC Filings Access Error**
```bash
Error: SEC_FILINGS database not found
```
- **Solution**: Install SEC Filings dataset from [Snowflake Marketplace](https://app.snowflake.com/marketplace/listing/GZTSZAS2KH9/snowflake-public-data-products-sec-filings)
- Verify access: `SELECT COUNT(*) FROM SEC_FILINGS.CYBERSYN.COMPANY_INDEX;`

**Warehouse Not Active**
```bash
Error: No active warehouse selected
```
- **Solution**: Ensure warehouse specified in connection profile exists and is running
- Recommend MEDIUM or larger for full builds
- Build will auto-create `SAM_DEMO_EXECUTION_WH` and `SAM_DEMO_CORTEX_WH` if needed
