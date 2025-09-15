# WAM AI Demo - Wealth Management AI Demonstration

A comprehensive demonstration of Snowflake AI capabilities for wealth management, featuring three AI-powered personas using Cortex Analyst and Cortex Search.

## Overview

This demo showcases:
- **advisor_ai** (Wealth Manager): Client relationship management with portfolio analytics
- **analyst_ai** (Portfolio Manager): Investment research and risk analysis
- **guardian_ai** (Compliance Officer): Communications surveillance and regulatory analysis

## Key Features

- **Enhanced Data Model**: Industry-standard dimensional model with immutable SecurityID and issuer hierarchy
- **Real Data Integration**: Authentic assets and market data from Snowflake Marketplace with CSV fallback
- **Hybrid Market Data**: Real OHLCV data for anchor portfolios, synthetic data for scale
- **Realistic Unstructured Data**: AI-generated communications, research, and regulatory content
- **Two Semantic Views**: CLIENT_FINANCIALS_SV and CLIENT_INTERACTIONS_SV
- **Three Search Services**: Communications, Research, and Regulatory search
- **Comprehensive Validation**: Systematic testing of all components
- **Universal Compatibility**: Works with or without Marketplace access

## Prerequisites

1. **Snowflake Account** with:
   - Cross-Region Inference enabled for Cortex Complete
   - Access to Cortex Analyst and Cortex Search
   - Sufficient compute credits for data generation
   - **Optional**: Access to 'Public Data Financials & Economics: Enterprise' from Snowflake Marketplace for real data

2. **Python Environment**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Snowflake Connection**:
   - Uses connection `sfseeurope-mstellwall-aws-us-west3` by default
   - Automatically reads from `~/.snowflake/connections.toml`
   - Alternative: Specify different connection with `--connection <name>`

## Quick Start

### 1. Setup Connection
```bash
# Uses default connection automatically
# No setup required if you have ~/.snowflake/connections.toml configured

# Alternative: Use different connection
python main.py --connection <your_connection_name>
```

### 2. Extract Real Data (Optional but Recommended)

**For Enhanced Demo Authenticity** - Extract real financial data from Snowflake Marketplace:

```bash
# Extract real assets from Snowflake Marketplace (requires access)
python main.py --extract-real-assets

# Extract real market data from Snowflake Marketplace (requires access)
python main.py --extract-real-market-data
```

**Successful Extraction Example**:
```
📊 Extracting real assets from Marketplace...
  → Extracting real assets from Snowflake Marketplace...
    ✅ Marketplace data accessible
    → Running asset extraction query...
    📊 Extracted assets by region:
       Other: 63,597
       USA: 6,019
       APAC/EM: 757
       EU: 225
    ✅ Extracted 2,539 real assets to ./data/real_assets.csv
    📋 Final dataset breakdown:
       USA: 2,004
       APAC/EM: 300
       EU: 225
    📊 Asset class distribution:
       Equity: 2,148
       ETF: 391
```

**Market Data Extraction Example**:
```
📈 Extracting real market data from Marketplace...
  → Extracting real market data from Snowflake Marketplace...
    ✅ Market data accessible
    📊 Using 50 additional tickers from real assets CSV
    → Extracting market data for 56 tickers...
    → Date range: 2023-09-10 to 2025-09-09
    📊 Market data extracted:
       Total records: 22,974
       Unique tickers: 51
       Date range: 2023-09-11 to 2025-09-05
    ✅ Extracted 22,974 market data records to ./data/real_market_data.csv
```

**Golden Ticker Coverage**:
- ✅ **AAPL**: 498 trading days ($179.60 → $239.23)
- ✅ **MSFT**: 498 trading days with authentic volatility patterns  
- ✅ **NVDA**: 498 trading days with real volume data
- ✅ **JPM, V, SAP**: Complete OHLCV coverage

**What this provides**:
- ✅ **Authentic ticker symbols** (AAPL, MSFT, NVDA, etc.) instead of synthetic ones
- ✅ **Real company names** and industry classifications
- ✅ **Actual market volatility** patterns and trading volumes
- ✅ **Geographic accuracy** with proper US/EU distribution
- ✅ **Enhanced credibility** for customer demonstrations

**Fallback**: If you don't have Marketplace access, the system automatically uses high-quality synthetic data that still provides an excellent demo experience.

### 3. Run Full Build
```bash
# Full build (replace all components)
python main.py --mode replace_all

# Test mode (reduced data volumes)
python main.py --mode replace_all --test-mode

# Data only (regenerate data, keep AI services)
python main.py --mode data_only

# AI services only (recreate semantic views and search services)
python main.py --mode semantics_and_search_only
```

### 4. Validate Components
```bash
# Run validation only (includes all component validation)
python main.py --validate-only

# Full build includes validation automatically
python main.py --mode replace_all
```

### 5. Configure Agents
After successful build and validation:
1. **Follow the complete setup guide**: [AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md)
2. **Create three agents** in Snowflake Intelligence: advisor_ai, analyst_ai, guardian_ai
3. **Test with provided queries** to verify functionality
4. **Run demo scenarios** for customer presentations

## Real Data Integration Quick Reference

### Extract Real Data (One-Time Setup)
```bash
# For accounts WITH Marketplace access:
python main.py --extract-real-assets          # Creates ./data/real_assets.csv
python main.py --extract-real-market-data     # Creates ./data/real_market_data.csv

# Then build with enhanced authenticity:
python main.py --mode replace_all
```

### Build Without Marketplace Access
```bash
# For accounts WITHOUT Marketplace access:
python main.py --mode replace_all              # Uses synthetic data (still excellent quality)
```

### Benefits of Real Data
- **Authentic Tickers**: AAPL, MSFT, NVDA instead of synthetic symbols
- **Real Company Names**: Apple Inc., Microsoft Corporation, etc.
- **Actual Market Patterns**: True volatility, correlations, and trading volumes
- **Industry Accuracy**: Proper GICS sectors and geographic distributions
- **Enhanced Credibility**: Customers recognize real securities in demos

## Configuration

Key settings in `config.py`:

```python
# Volumes
NUM_ADVISORS = 5
CLIENTS_PER_ADVISOR = 25
COMMS_PER_CLIENT = 50

# Golden Tickers (easy to change)
GOLDEN_TICKERS = ["AAPL", "MSFT", "NVDA", "JPM", "V", "SAP"]

# Real Data Integration
USE_REAL_ASSETS_CSV = True
USE_REAL_MARKET_DATA = True

# Market Data
MARKET_REAL_PORTFOLIOS = ["US MegaTech Focus", "US Financials Core"]

# Build Modes
BUILD_MODES = ['replace_all', 'data_only', 'semantics_and_search_only']
```

## Data Architecture

### Enhanced Data Model with Real Data Integration
- **Dimension Tables**: DIM_ADVISOR, DIM_CLIENT, DIM_SECURITY, DIM_ISSUER, DIM_PORTFOLIO
- **Fact Tables**: FACT_TRANSACTION, FACT_POSITION_DAILY_ABOR, FACT_MARKETDATA_TIMESERIES
- **Corpus Tables**: COMMUNICATIONS_CORPUS, RESEARCH_CORPUS, REGULATORY_CORPUS
- **Real Data Sources**: Snowflake Marketplace integration with CSV extraction capability

### Real Data Integration Architecture
```
Snowflake Marketplace (Optional)
├── OpenFIGI Security Index     → real_assets.csv
├── Stock Price Timeseries      → real_market_data.csv
└── Company Characteristics

CSV Files (Fallback)           Hybrid Data Generation
├── real_assets.csv       →    ├── Real company names & tickers
└── real_market_data.csv  →    ├── Authentic OHLCV patterns
                               ├── Proper industry sectors
                               └── Synthetic completion for full coverage
```

### Schema Organization
```
WAM_AI_DEMO/
├── RAW/                 # Temporary and staging data
├── CURATED/            # Business-ready dimensional model
└── AI/                 # Semantic views and search services
```

## AI Components

### Semantic Views
1. **CLIENT_FINANCIALS_SV**: Portfolio analytics with issuer hierarchy
2. **CLIENT_INTERACTIONS_SV**: Communication patterns and metrics

### Search Services
1. **COMMUNICATIONS_SEARCH**: Client emails, calls, meetings
2. **RESEARCH_SEARCH**: Investment research and analyst reports
3. **REGULATORY_SEARCH**: Compliance rules and guidance

## Agent Configuration

After running the build, configure agents in Snowflake Intelligence:

### Quick Setup Guide
1. **Access**: Navigate to Snowsight → Projects → Snowflake Intelligence
2. **Verify Components**: Run validation queries to ensure AI services exist
3. **Create Agents**: Follow step-by-step setup in `.cursor/rules/agents.mdc`

### Agent Overview

#### advisor_ai (Wealth Manager)
- **Tools**: cortex_analyst_client_financials, cortex_analyst_client_interactions, search_communications, search_research
- **Test Query**: `"I have a meeting with Sarah Johnson in 30 minutes. Please prepare a briefing."`
- **Demo Scenario**: Client-specific meeting preparation with portfolio analysis and communication history

#### analyst_ai (Portfolio Manager)
- **Tools**: cortex_analyst_client_financials, search_research
- **Test Query**: `"Find research on Apple and Microsoft"`
- **Demo Scenario**: Investment research and portfolio exposure analysis

#### guardian_ai (Compliance)
- **Tools**: search_communications, search_regulatory
- **Test Query**: `"Find FINRA regulations about communications"`
- **Demo Scenario**: Communications surveillance and regulatory analysis

### Complete Setup Instructions
See **[AGENT_SETUP_GUIDE.md](AGENT_SETUP_GUIDE.md)** for detailed step-by-step GUI instructions including:
- Complete agent creation process with exact tool configurations
- Copy-paste ready Planning and Response Instructions
- Troubleshooting guidance for common setup issues

### Demo Presentation Guide
See **[DEMO_SCENARIOS.md](DEMO_SCENARIOS.md)** for complete customer presentation scenarios including:
- Client-specific advisor meeting preparation workflows
- Investment research and risk analysis demonstrations
- Compliance monitoring and surveillance scenarios
- Cross-persona integration demonstrations
- Talking points, business impact, and presentation guidelines

## Build Process

### Phase 1: Database Setup
- Create database WAM_AI_DEMO with schemas RAW, CURATED, AI
- Create warehouses with WAM_AI_ prefix
- Set up stage for PDF documents

### Phase 2: Data Generation
- Generate structured data following enhanced model
- Create unstructured data using Cortex Complete
- Validate data quality and relationships

### Phase 3: AI Services
- Create semantic views with proper syntax and synonyms
- Build search services with correct attributes
- Validate all AI components

### Phase 4: Validation
- Test semantic views with business queries
- Validate search services with domain-specific searches
- Run business scenario tests for each persona

## Troubleshooting

### Common Issues

**Connection Errors**:
- Verify connections.toml configuration
- Check account identifier and credentials
- Ensure Cross-Region Inference is enabled

**Real Data Extraction Errors**:
- Verify access to 'Public Data Financials & Economics: Enterprise' from Snowflake Marketplace
- Check warehouse size for complex extraction queries
- Ensure sufficient compute credits for data extraction
- **Note**: System gracefully falls back to synthetic data if extraction fails

**Marketplace Access Issues**:
```
❌ Error: Marketplace data not accessible!
💡 You need access to 'Public Data Financials & Economics: Enterprise' dataset
   from Snowflake Marketplace
   Falling back to synthetic generation...
```
**Solution**: Contact your Snowflake account team to enable Marketplace access, or proceed with synthetic data

**Semantic View Errors**:
- Check table column names with `DESCRIBE TABLE`
- Ensure synonyms are unique across all dimensions/metrics
- Verify foreign key relationships exist

**Search Service Errors**:
- Verify ATTRIBUTES match SELECT column names exactly
- Check corpus tables have content
- Ensure WAREHOUSE parameter is specified

**Data Generation Issues**:
- Check warehouse size for data volume
- Verify Cortex Complete model availability
- Monitor for quota limits on AI functions

### Validation Queries

```sql
-- Check semantic views
SHOW SEMANTIC VIEWS IN WAM_AI_DEMO.AI;

-- Test semantic view
SELECT * FROM SEMANTIC_VIEW(
    WAM_AI_DEMO.AI.CLIENT_FINANCIALS_SV
    METRICS TOTAL_MARKET_VALUE
    DIMENSIONS PORTFOLIONAME
) LIMIT 5;

-- Check search services
SHOW CORTEX SEARCH SERVICES IN WAM_AI_DEMO.AI;

-- Test search service
SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
    'WAM_AI_DEMO.AI.COMMUNICATIONS_SEARCH',
    '{"query": "portfolio performance", "limit": 1}'
);

-- Verify real data integration
SELECT 
    'Real Assets' as data_type,
    COUNT(*) as record_count,
    COUNT(DISTINCT GICS_SECTOR) as unique_sectors,
    COUNT(DISTINCT COUNTRYOFINCORPORATION) as unique_countries
FROM WAM_AI_DEMO.CURATED.DIM_ISSUER;

-- Check market data coverage
SELECT 
    'Market Data' as data_type,
    COUNT(*) as total_records,
    COUNT(DISTINCT SecurityID) as unique_securities,
    MIN(PriceDate) as earliest_date,
    MAX(PriceDate) as latest_date
FROM WAM_AI_DEMO.CURATED.FACT_MARKETDATA_TIMESERIES;
```

## Support

For issues or questions:
1. Check the validation output for specific error messages
2. Review the troubleshooting section above
3. Examine the detailed implementation in `.cursor/rules/`

## Architecture Decisions

This implementation follows industry best practices:
- **Transaction-based holdings**: Audit trail for compliance
- **Immutable SecurityID**: Corporate action resilience  
- **Issuer hierarchy**: Enhanced risk analysis
- **Real data integration**: Authentic market data with graceful fallback
- **Hybrid architecture**: Best of real and synthetic data
- **Deterministic generation**: Repeatable builds
- **Comprehensive validation**: Production-ready quality

## Real Data Integration Details

### Extraction Process
1. **Real Assets**: Uses comprehensive OpenFIGI query to extract ~3,000 securities
   - Proper asset class categorization (Equity, Corporate Bond, ETF, etc.)
   - Geographic classification (USA, EU, APAC/EM)  
   - Industry sector mapping from SIC descriptions
   - Ensures golden tickers (AAPL, MSFT, NVDA, JPM, V, SAP) are included

2. **Real Market Data**: Extracts 2 years of OHLCV data
   - Covers golden tickers + additional liquid securities
   - Quality filters (requires close price, NASDAQ/NYSE focus)
   - Realistic trading volumes and price patterns

### Integration Benefits
- **Demo Credibility**: Real company names and ticker symbols
- **Market Authenticity**: Actual volatility patterns and correlations
- **Customer Confidence**: Recognizable securities in portfolio analysis
- **Scalability**: Works at any volume with hybrid approach
- **Flexibility**: Easy to extract once and reuse for multiple demos

### Data Quality Guarantees
- ✅ Golden tickers always included in extraction
- ✅ 80% US / 20% EU region mix maintained
- ✅ Asset class distribution preserved
- ✅ Foreign key relationships validated
- ✅ Portfolio weights sum to 100% (±0.1% tolerance)
- ✅ No negative prices or invalid market values
