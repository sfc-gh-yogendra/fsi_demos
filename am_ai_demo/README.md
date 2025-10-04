# Snowcrest Asset Management (SAM) AI Demo - 100% Real Assets

A comprehensive demonstration of Snowflake Intelligence for asset management customers, covering Protfolio Managers, Research Analysts, Quantitative Analysts, Client Relationship Managers, and Risk & Compliance Officers.


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

## Demo Overview

### Company Profile: Snowcrest Asset Management (SAM)
- **Multi-asset investment firm** with 10 portfolios ($12.5B total AUM)
- **Enhanced Architecture**: Industry-standard data model with SecurityID and issuer hierarchies
- **Specializes in**: Thematic growth, ESG leadership, quantitative strategies
- **Geographic focus**: Global with emphasis on US (55%), Europe (30%), APAC/EM (15%)
- **Asset classes**: Equities (70%), Corporate Bonds (20%), ETFs (10%)

### Available Demo Scenarios

✅ **Foundation Complete**: Industry-standard data model with 100% real assets

| Scenario | Agent | Status | Key Capabilities |
|----------|-------|--------|------------------|
| **Portfolio Insights** | `portfolio_copilot` | **✅ IMPLEMENTED** | Holdings analysis, implementation planning, trading costs, risk budgets |
| **Research Intelligence** | `research_copilot` | **✅ IMPLEMENTED** | Document research and analysis across broker reports and earnings |
| **Thematic Analysis** | `thematic_macro_advisor` | **✅ IMPLEMENTED** | Theme discovery, exposure analysis, macro scenario modeling |
| **ESG Monitoring** | `esg_guardian` | **✅ IMPLEMENTED** | Controversy scanning, policy compliance, engagement tracking |
| **Compliance** | `compliance_advisor` | **✅ IMPLEMENTED** | Mandate monitoring, breach detection, policy citation |
| **Client Reporting** | `sales_advisor` | **✅ IMPLEMENTED** | Performance reports, template formatting, philosophy integration |
| **Factor Analysis** | `quant_analyst` | **✅ IMPLEMENTED** | Factor screening, time-series analysis, factor evolution trends |

- **✅ ALL 7 SCENARIOS FULLY IMPLEMENTED**: Complete demo environment with ESG, compliance, and comprehensive analytics capabilities

**To Build Specific Scenarios**:
```bash
# Build ESG & Compliance scenarios (NGO reports, engagement notes, policy docs)
python python/main.py --connection-name [your-connection] --scenarios esg_guardian

# Note: Compliance Advisor shares all components with ESG Guardian (no separate build needed)

# Build all implemented scenarios
python python/main.py --connection-name [your-connection] --scenarios all

# Test mode for faster development
python python/main.py --connection-name [your-connection] --scenarios esg_guardian --test-mode
```

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

## Enhanced Data Architecture

### Database: `SAM_DEMO`
- **RAW Schema**: External provider simulation + raw documents
- **CURATED Schema**: Industry-standard dimension/fact model
- **AI Schema**: Enhanced semantic views and Cortex Search services

### Enhanced Data Model Features
- **Immutable SecurityID**: Corporate action resilience and temporal integrity
- **Transaction-Based Holdings**: ABOR positions built from canonical transaction log
- **Issuer Hierarchies**: Corporate structure and parent company analysis
- **Enhanced Document Integration**: Stable SecurityID/IssuerID linkage
- **Real Data Integration**: Authentic market data with synthetic fallback

### Data Providers (Simulated)
- **NorthStar Data (NSD)**: ESG ratings, equity factors, estimates, MSCI ACWI benchmark
- **PolarMetrics (PLM)**: Market prices, fundamentals, credit ratings, yield curves, S&P 500/Nasdaq benchmarks
- **Internal SAM**: Portfolio holdings, policies, templates, engagement notes

## Key Features

### 🎯 **Realistic Data**
- **Authentic Tickers**: 14,000+ real securities from SEC Filings dataset (AAPL, NVDA, ASML, TSM, NESTLE)
- **Synthetic Market Data**: Realistic OHLCV records for all 14,000+ securities with proper volatility patterns
- **Correlated Relationships**: P/E ratios align with growth, sector-specific factor scores
- **Temporal Consistency**: Earnings dates align with transcripts, quarterly reporting cycles
- **Complex Analytics**: Bond mathematics, ESG ratings, factor exposures, compliance monitoring
- **Global Coverage**: Proper geographic distribution (55% US, 30% EU, 15% APAC/EM)

### 🤖 **Enhanced AI Components**
- **Semantic Views**: Multi-table analytics with issuer hierarchy support + implementation planning
- **Search Services**: Enhanced with SecurityID/IssuerID attributes for stable document linkage
- **Intelligent Agents**: 7 role-specific agents with professional portfolio management capabilities
- **Content Generation**: Deterministic template-based generation (50+ curated templates, no LLM dependencies)
- **ESG & Compliance**: Full document corpus supporting ESG monitoring, mandate compliance, and regulatory tracking
- **Implementation Planning**: Trading costs, liquidity analysis, risk budgets, and execution planning
- **Dedicated Warehouses**: `SAM_DEMO_EXECUTION_WH` and `SAM_DEMO_CORTEX_WH`
- **Industry-Standard Architecture**: Complete professional asset management data model

### 📊 **Investment Themes**
- **On-Device AI**: Semiconductor and software companies
- **Renewable Energy Transition**: Clean energy and infrastructure
- **Cybersecurity**: Security software and services

### ⚖️ **Compliance Monitoring**
- Concentration limits (7% max, 6.5% warning)
- Fixed income guardrails (75% IG minimum, duration tolerance)
- ESG requirements (BBB minimum rating, controversy exclusions)

## Content Generation Approach

The demo uses **template-based content generation** via the hydration engine for all document types:

### Template-Based Generation (Hydration Engine)
- **50+ Curated Templates**: Professional markdown templates with YAML front matter
- **Complete Coverage**: All document types (broker research, earnings transcripts, NGO reports, policies, etc.)
- **Smart Placeholders**: Context-aware replacement with entity data, dates, and metrics
- **Deterministic Output**: Consistent results with same RNG_SEED for reproducible demos
- **Fast Builds**: Near-instant generation using template hydration
- **No LLM Dependencies**: Build-time generation requires no Cortex Complete calls
- **High Quality**: Manually curated templates ensure professional, realistic content

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

### Data Quality Issues

**Duplicate Companies in Holdings**
- This should be resolved with the enhanced issuer linkage
- Verify distinct issuers: `SELECT COUNT(DISTINCT IssuerID) FROM SAM_DEMO.CURATED.DIM_ISSUER;`
- Check for commercial metals co: Should appear only once

**Missing Bond Data**
- Bonds with maturity before 2020 are automatically filtered out
- Check bond counts: `SELECT COUNT(*) FROM SAM_DEMO.CURATED.DIM_SECURITY WHERE AssetClass = 'Corporate Bond';`
- Verify parsed coupon rates: Not all should be 5.0%

**Low Issuer Linkage**
- Expected: ~100% of securities linked to issuers
- Check: `SELECT match_method, COUNT(*) FROM SAM_DEMO.CURATED.DIM_SECURITY GROUP BY match_method;`
- Should see: CIK matches (~10K), SECURITY_NAME matches (~2.5K), SYNTHETIC matches (~1.5K)

### Agent Configuration Issues

**Agent Not Responding**
- Verify agent has access to semantic views and search services
- Test individual tools before configuring agent
- Check tool configurations match exact service names: `SAM_DEMO.AI.SAM_ANALYST_VIEW`

**Search Returns No Results**
- Verify corpus tables have content: `SELECT COUNT(*) FROM SAM_DEMO.CURATED.BROKER_RESEARCH_CORPUS;`
- Check search service exists: `SHOW CORTEX SEARCH SERVICES IN SAM_DEMO.AI;`
- Test search directly with SQL before using in agent

**Semantic View Query Fails**
- Verify view syntax: `DESCRIBE SEMANTIC VIEW SAM_DEMO.AI.SAM_ANALYST_VIEW;`
- Check all referenced tables exist in CURATED schema
- Test simple query first: `SELECT * FROM SEMANTIC_VIEW(...) LIMIT 5;`

### Performance Issues

**Build Takes Too Long**
- **Solution**: Use test mode for development: `--test-mode`
- Reduces securities from 14,000 to 1,400 (10x faster)
- Use larger warehouse (LARGE instead of MEDIUM)

**Agent Response Slow**
- Check warehouse size for Cortex Search
- Verify search service refresh is complete: `SHOW CORTEX SEARCH SERVICES;`
- Consider using dedicated warehouse for agent queries

### Support Resources

- **Agent Configuration**: Complete setup in `docs/agents_setup.md`
- **Demo Scripts**: Ready-to-use flows in `docs/demo_scenarios.md`
- **Data Model**: Schema documentation in `docs/data_model.md`

## Real Asset Data

The demo uses **14,000+ authentic financial instruments** from the SEC Filings dataset (OpenFIGI), providing maximum realism and authenticity for customer demonstrations:

- **100% Real Securities**: All tickers and Bloomberg FIGI identifiers are authentic
- **3,303 Real Issuers**: Complete corporate hierarchies and relationships
- **Global Coverage**: Proper geographic distribution across US, Europe, and APAC/EM
- **Asset Classes**: Equities (10,000), Corporate Bonds (3,000), ETFs (1,000)
- **Automatic Loading**: `V_REAL_ASSETS` view created automatically from SEC Filings dataset
- **No Manual Steps**: No CSV files or data extraction required

## Architecture Highlights

### Data Model Excellence
- **Immutable SecurityID**: Ensures corporate action resilience and temporal integrity
- **Transaction-Based Holdings**: Complete audit trail from transaction log to positions
- **Issuer Hierarchies**: Support for parent company and corporate structure analysis
- **Industry Standard**: Dimension/fact architecture following asset management best practices

### AI Component Integration
- **7 Semantic Views**: Multi-table analytics with comprehensive business logic
- **10+ Search Services**: Document search with SecurityID/IssuerID linkage
- **7 Intelligent Agents**: Role-specific agents with professional capabilities
- **Template Library**: 50+ curated templates for consistent, high-quality content

### Performance Optimization
- **Dedicated Warehouses**: Separate compute for execution and Cortex Search
- **Test Mode**: 10% data volumes (1,400 securities) for rapid development iteration
- **Fast Builds**: Template-based generation (no LLM calls) for near-instant document creation
- **Reproducible Results**: Deterministic outputs using RNG_SEED configuration
- **No External Dependencies**: All content generated from local templates
