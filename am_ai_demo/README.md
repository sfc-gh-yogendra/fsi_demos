# Snowcrest Asset Management (SAM) AI Demo - 100% Real Assets

A comprehensive demonstration of Snowflake Intelligence capabilities for asset management customers, featuring 14,000+ authentic securities from OpenFIGI, realistic multi-asset portfolios, AI-powered analytics, and intelligent agents.

**Please be aware that everything is not 100% tested and the focus has been to make sure there is data that support the demo scenarios, meaning having data supporting the flow described in docs/demo_scenarios.md`. Also check the status in the  Available Demo Scenarios section, if something has the NOT IMPLEMENTED status then it means there is no data genrated or objects created for supporting that scenario.**

## Quick Start

### Prerequisites

#### **Repository Setup**
- Clone or download this repository to your local machine
- Navigate to the project directory: `cd am_ai_demo`

#### **Snowflake Account**
- Make sure you have cross-region inference enabled: https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference, at minimum you need to have AWS_EU enabled byt ANY_REGIONS is prefered.
- Snowflake Intelligence enabled: https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence
- Access to "SEC Filings", https://app.snowflake.com/marketplace/listing/GZTSZAS2KH9/snowflake-public-data-products-sec-filings?search=SEC%20fillings, product from Snowflake Marketplace

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

1. **Configure Agents**: Follow standardized format in `docs/agents_setup.md`
2. **Test Scenarios**: Use 'portfolio' terminology from `docs/demo_scenarios.md`  
3. **Validate Data**: Execute quality checks from `docs/runbooks.md`
4. **Demo Preparation**: All 7 scenarios ready with enhanced issuer-level capabilities

### Quick Agent Test
```
"What are my top 10 holdings by market value in the SAM Global Thematic Growth portfolio?"
```
**Expected**: Clean list with enhanced issuer information and stable SecurityID linkage

**Note**: All commands now require the `--connection-name` parameter to specify which connection from `~/.snowflake/connections.toml` to use.

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

- **✅ ALL SCENARIOS IMPLEMENTED**: Complete demo suite ready for use

**To Build All Scenarios**:
```bash
# Build all implemented scenarios (includes ESG Guardian & Compliance Advisor)
python main.py --connection-name [your-connection] --scenarios all --test-mode
```

## Configuration Defaults

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Connection** | Required via `--connection-name` | Must specify connection from ~/.snowflake/connections.toml |
| **Model** | `llama3.1-70b` | LLM for content generation |
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
├── docs/                       # Documentation
│   ├── agents_setup.md         # Agent configuration instructions
│   ├── demo_scenarios.md       # Complete demo scripts
│   ├── data_model.md           # Schema and data documentation
│   └── runbooks.md             # Setup and execution procedures
├── python/                     # Python implementation
│   ├── config.py               # Configuration constants
│   ├── main.py                 # CLI orchestrator
│   ├── generate_structured.py  # Structured data generation
│   ├── generate_unstructured.py # Unstructured content generation
│   ├── build_ai.py             # AI components (semantic views, search)
│   └── extract_real_assets.py  # Real asset view creation
├── data/                       # Optional data storage directory
├── generic_rules/              # Development patterns and rules
├── research/                   # Background research and analysis
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

## Troubleshooting

### Common Issues
- **Connection fails**: Verify `~/.snowflake/connections.toml` configuration
- **Module not found**: Run `pip install -r requirements.txt` to install dependencies  
- **Permission denied**: Check Snowflake account has Cortex features enabled
- **Build fails**: Check warehouse has sufficient compute resources
- **Enhanced data model**: Uses SecurityID-based architecture with transaction audit trails
- **Agent terminology**: Agents now understand both 'fund' and 'portfolio' queries
- **Real assets missing**: Ensure access to SEC Filings dataset - view is created automatically

### Support Resources
- **Setup Instructions**: Complete documentation in `docs/` directory
- **Agent Configuration**: See `docs/agents_setup.md` for detailed agent setup
- **Demo Scripts**: Ready-to-use conversation flows in `docs/demo_scenarios.md`
- **Troubleshooting**: Validation procedures in `docs/runbooks.md`

## Real Asset Data

The demo uses 14,000+ authentic financial instruments from the SEC Filings dataset (OpenFIGI). This provides maximum realism and authenticity for customer demonstrations with 100% real Bloomberg identifiers.

**Usage**: Real assets are automatically loaded via the `V_REAL_ASSETS` view created from the SEC Filings dataset during the build process. No manual data extraction or CSV files needed.
