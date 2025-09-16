# WAM AI Demo - Wealth Management AI Demonstration

A comprehensive demonstration of Snowflake AI capabilities for wealth management, featuring three AI-powered personas using Cortex Analyst and Cortex Search to showcase modern financial services workflows.

## Prerequisites

### Repository Setup
Clone or download this repository to your local machine:
```bash
git clone <repository-url>
cd wam_ai_demo
```

### Snowflake Requirements

#### Snowflake Account
You need a Snowflake account with the following capabilities enabled:

#### Cross-Region Inference (Required)
Enable cross-region inference for Cortex Complete functionality:
- **Documentation**: [Cross-Region Inference Setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)
- **Minimum Requirement**: AWS_EU enabled
- **Recommended**: ANY_REGIONS for optimal performance

#### Snowflake Intelligence (Required)
Enable Snowflake Intelligence for agent configuration:
- **Documentation**: [Snowflake Intelligence Setup](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence)
- **Required for**: Agent configuration and deployment

#### (Optional): Access to "Data Financials & Economics: Enterprise" marketplace dataset
Only required if you want to update the real_assets.csv file with fresh data

### Local Python Environment

#### Python Version
- **Required**: Python 3.10 or higher

#### Dependencies Installation
```bash
pip install -r requirements.txt
```

### Configure Snowflake Connection

Set up your Snowflake connection in `~/.snowflake/connections.toml`:
```toml
[your_connection_name]
account = "your-account-identifier"
user = "your-username"
password = "your-password"
warehouse = "your-warehouse"
database = "your-database"
schema = "your-schema"
role = "your-role"
```

## How to Build Demo

### Standard Build (Complete Demo)
```bash
# Build complete demo with all scenarios and features
python main.py --connection your_connection_name
```

### Scenario-Specific Builds
```bash
# Build specific scenarios
python main.py --connection your_connection_name --scenarios advisor
python main.py --connection your_connection_name --scenarios advisor analyst
python main.py --connection your_connection_name --scenarios guardian --test-mode
```

### Scope-Specific Builds
```bash
# Build only data layer
python main.py --connection your_connection_name --scope data

# Build only semantic views
python main.py --connection your_connection_name --scope semantic

# Build only search services
python main.py --connection your_connection_name --scope search
```

### Optional: Extract Real Market Data
For enhanced demo authenticity (requires Snowflake Marketplace access):
```bash
# Extract real financial data from Snowflake Marketplace
python main.py --connection your_connection_name --extract-real-assets

# Then build the demo
python main.py --connection your_connection_name
```

### Validation
```bash
# Validate components without building
python main.py --connection your_connection_name --validate-only

# Test mode with reduced data volumes
python main.py --connection your_connection_name --test-mode
```

## Next Steps

### Agent Configuration
Configure the three AI agents in Snowflake Intelligence:
- **Setup Guide**: See [AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md) for complete step-by-step instructions
- **GUI Configuration**: Detailed Snowflake Intelligence setup process
- **Tool Configuration**: Exact settings for Cortex Analyst and Cortex Search tools

### Run the Demo
Execute customer demonstration scenarios:
- **Demo Guide**: See [DEMO_SCENARIOS.md](DEMO_SCENARIOS.md) for complete presentation flows
- **Business Scenarios**: Client meeting preparation, investment analysis, compliance monitoring
- **Talking Points**: Business impact and value proposition guidance

## Demo Overview

This demo showcases three wealth management personas powered by Snowflake AI:

### Available Demo Scenarios

#### advisor_ai (Wealth Manager)
- **Persona**: Client-facing wealth advisor
- **Capabilities**: Portfolio analytics, client relationship insights, meeting preparation
- **Tools**: Client financials analysis, communication history, research synthesis
- **Demo Query**: *"I have a meeting with Sarah Johnson in 30 minutes. Please prepare a briefing."*

#### analyst_ai (Portfolio Manager)
- **Persona**: Investment portfolio manager
- **Capabilities**: Investment research, risk analysis, performance attribution
- **Tools**: Portfolio analytics, research analysis, market commentary
- **Demo Query**: *"Analyze our portfolio exposure to technology sector and find recent research."*

#### guardian_ai (Compliance Officer)
- **Persona**: Regulatory compliance officer
- **Capabilities**: Communications surveillance, regulatory analysis, risk monitoring
- **Tools**: Communication monitoring, regulatory guidance, compliance verification
- **Demo Query**: *"Search for any communications containing performance guarantees."*

### Enhanced Features (Phase 2)
- **Thematic Watchlists**: Carbon Negative Leaders, AI Innovation Leaders, ESG Leaders
- **ESG Analytics**: Sustainability reporting, carbon neutrality analysis
- **Advanced Insights**: Watchlist exposure analysis, ESG scoring

## Configuration Defaults

Configuration settings are stored in `config.py`. Key defaults include:

| Setting | Default Value | Description |
|---------|---------------|-------------|
| `NUM_ADVISORS` | `5` | Number of wealth advisors to generate |
| `CLIENTS_PER_ADVISOR` | `25` | Number of clients per advisor (125 total clients) |
| `ACCOUNTS_PER_CLIENT` | `2` | Number of accounts per client |
| `COMMS_PER_CLIENT` | `50` | Number of communications per client over lifespan |
| `GOLDEN_TICKERS` | `["AAPL", "MSFT", "NVDA", "JPM", "V", "SAP"]` | Key securities used in demonstrations |
| `REGION_MIX` | `{"us": 0.8, "eu": 0.2}` | Geographic distribution of securities (80% US, 20% EU) |
| `BUILD_SCOPES` | `['all', 'data', 'semantic', 'search']` | Available build scope options |
| `AVAILABLE_SCENARIOS` | `['advisor', 'analyst', 'guardian', 'all']` | Available demo scenarios |
| `MODEL_BY_CORPUS` | `"llama3.1-70b"` | AI model used for document generation across all corpora |
| `SEARCH_TARGET_LAG` | `'5 minutes'` | Refresh frequency for Cortex Search services |
| `DATABASE_NAME` | `"WAM_AI_DEMO"` | Target database name |
| `WAREHOUSE_PREFIX` | `"WAM_AI_"` | Prefix for created warehouses |
| `REAL_ASSETS_CSV_PATH` | `'./data/real_assets.csv'` | Path for real asset data extraction |

## Project Structure

```
wam_ai_demo/
├── main.py                    # Main build orchestration
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── AGENT_SETUP_GUIDE.md       # Agent configuration guide
├── DEMO_SCENARIOS.md          # Demo presentation guide
├── data/                      # Real data storage (when extracted)
│   ├── real_assets.csv        # Real securities data
│   └── real_market_data.csv   # Real market prices
└── src/                       # Implementation modules
    ├── setup.py               # Database and schema setup
    ├── generate_structured.py # Structured data generation
    ├── generate_unstructured.py # Document generation
    ├── create_semantic_views.py # Semantic view creation
    ├── create_search_services.py # Search service setup
    ├── extract_real_data.py   # Marketplace data extraction
    └── validate_components.py # Component validation
```

## Data Architecture

### Database Schema Organization
```
WAM_AI_DEMO/
├── RAW/                 # Staging and temporary data
│   ├── CLIENT_DOCS/     # PDF documents stage
│   └── TEMP_* tables    # Processing tables
├── CURATED/            # Business-ready dimensional model
│   ├── DIM_* tables    # Dimension tables (Client, Security, Portfolio, etc.)
│   ├── FACT_* tables   # Fact tables (Positions, Transactions, Market Data)
│   └── *_CORPUS tables # Document corpora for search
└── AI/                 # AI and ML components
    ├── Semantic Views  # CLIENT_FINANCIALS_SV, CLIENT_INTERACTIONS_SV
    └── Search Services # COMMUNICATIONS_SEARCH, RESEARCH_SEARCH, REGULATORY_SEARCH
```

### Data Model Highlights
- **Enhanced Dimensional Model**: Industry-standard fact/dimension architecture
- **Immutable SecurityID**: Handles corporate actions and ticker changes
- **Issuer Hierarchy**: Supports corporate relationship analysis
- **Transaction-Based Holdings**: Full audit trail for compliance
- **Real Data Integration**: Authentic market data with synthetic fallback

### AI Components

#### Semantic Views
- **CLIENT_FINANCIALS_SV**: Portfolio analytics with multi-table joins
- **CLIENT_INTERACTIONS_SV**: Communication patterns and metrics
- **WATCHLIST_ANALYTICS_SV**: Thematic investment analysis (Phase 2)

#### Search Services
- **COMMUNICATIONS_SEARCH**: Client emails, calls, meeting notes
- **RESEARCH_SEARCH**: Investment research, analyst reports, ESG content
- **REGULATORY_SEARCH**: Compliance rules, regulatory guidance

## Troubleshooting

### Connection Issues
**Error**: `Failed to connect to Snowflake`
**Solution**: 
- Verify `~/.snowflake/connections.toml` configuration
- Check account identifier and credentials
- Ensure connection name matches `--connection` parameter

### Cortex Requirements
**Error**: `Cross-region inference not enabled`
**Solution**: 
- Enable cross-region inference: [Setup Guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cross-region-inference)
- Minimum requirement: AWS_EU enabled
- Recommended: ANY_REGIONS for best performance

**Error**: `Snowflake Intelligence not available`
**Solution**: 
- Enable Snowflake Intelligence: [Setup Guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence)
- Required for agent configuration

### Build Failures
**Error**: `Table not found` or `Object does not exist`
**Solution**: 
- Run full build: `python main.py --connection your_connection --scope all`
- Check warehouse permissions and size
- Verify database creation succeeded

**Error**: `Semantic view creation failed`
**Solution**: 
- Ensure data tables exist first: `--scope data` then `--scope semantic`
- Check column names with `DESCRIBE TABLE`
- Verify foreign key relationships

**Error**: `Search service creation failed`
**Solution**: 
- Verify corpus tables have content
- Check ATTRIBUTES match SELECT column names exactly
- Ensure warehouse parameter is specified

### Real Data Extraction
**Error**: `Marketplace data not accessible`
**Solution**: 
- Request access to 'Public Data Financials & Economics: Enterprise'
- Contact Snowflake account team for Marketplace access
- System will fallback to synthetic data automatically

**Note**: Demo works excellently with synthetic data if Marketplace access unavailable

### Component Validation
Run validation to identify specific issues:
```bash
python main.py --connection your_connection --validate-only
```

### Common Validation Queries
```sql
-- Check AI components exist
SHOW SEMANTIC VIEWS IN WAM_AI_DEMO.AI;
SHOW CORTEX SEARCH SERVICES IN WAM_AI_DEMO.AI;

-- Test semantic view
SELECT * FROM SEMANTIC_VIEW(
    WAM_AI_DEMO.AI.CLIENT_FINANCIALS_SV
    METRICS TOTAL_MARKET_VALUE
    DIMENSIONS PORTFOLIONAME
) LIMIT 5;

-- Test search service  
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'WAM_AI_DEMO.AI.COMMUNICATIONS_SEARCH',
    '{"query": "portfolio", "limit": 1}'
);
```

### Performance Issues
**Slow builds**: 
- Use `--test-mode` for faster iteration
- Increase warehouse size for large data volumes
- Consider `--scope data` first, then `--scope semantic` and `--scope search`

**Memory errors**: 
- Reduce data volumes in `config.py`
- Use larger warehouse for data generation
- Build in phases using different scopes

For additional support, refer to the detailed implementation rules in the project documentation and validation output messages.