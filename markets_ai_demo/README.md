# Frost Markets Intelligence - Snowflake AI Demo

A comprehensive demonstration of Snowflake AI capabilities for financial markets research, showcasing intelligence augmentation for equity research analysts and market insights professionals.

## 🏔️ Overview

This demo creates a fictional financial markets research firm "Frost Markets Intelligence" to demonstrate:

- **Snowflake Intelligence** with conversational AI agents
- **Cortex Analyst** for semantic data analysis
- **Cortex Search** for unstructured document retrieval  

## 🎯 Demo Scenarios

### All 6 Scenarios (90-minute comprehensive demo)

1. **Equity Research Analyst - Earnings Season Analysis** (15 minutes)
   - Accelerating quarterly earnings season analysis
   - Beat/miss analysis across coverage universe
   - Management commentary extraction and sentiment analysis
   - Professional research note generation

2. **Equity Research Analyst - Thematic Research** (15 minutes)
   - Discovering investment themes from alternative data
   - Cross-sector trend analysis (AI/ML, Carbon Capture, EVs)
   - Company exposure mapping and stock performance correlation
   - Sentiment analysis of thematic developments

3. **Global Research & Market Insights - Market Structure Reports** (15 minutes)
   - Hyper-personalizing quarterly market structure reports
   - Client engagement analytics and strategic targeting
   - EMIR 3.0 regulatory impact assessment for asset managers
   - Identifying high-value client opportunities

4. **Global Research & Market Insights - Client Strategy Preparation** (15 minutes)
   - Data-driven 1-to-1 strategic client engagements
   - Portfolio-specific market impact analysis
   - Recent theme correlation with client holdings
   - Pre-meeting intelligence synthesis

5. **Market Risk Analyst - Real-Time Market Event Impact Assessment** (15 minutes)
   - Real-time assessment of market events (e.g., Taiwan earthquake)
   - Firm-wide exposure analysis by sector, geography, and credit quality
   - Portfolio stress testing with VaR calculations
   - Quantifying downside risk under adverse scenarios

6. **Global Research - Global Macro Strategy Report Generation** (15 minutes)
   - Proprietary macroeconomic signal analysis
   - Sector-macro correlation identification
   - Cross-asset strategy development
   - Regional economic trend analysis

## 🚀 Quick Start

### Prerequisites
- Snowflake account with Cortex features enabled
- Snowflake Intelligence enabled: [Setup Guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#set-up-sf-intelligence) **Please make sure the SNowflake user you use when running the setup has USAGE and MODIFY permissions on SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT**
- Python 3.11+ with pip
- A `connections.toml` file configured (see [Snowflake docs](https://docs.snowflake.com/en/developer-guide/snowpark/python/creating-session#connect-by-using-the-connections-toml-file))

### Installation

```bash
# Clone/download the demo files
cd markets_ai_demo

# Install Python dependencies
pip install -r requirements.txt

# Configure connection (optional - defaults to 'markets_demo')
# Edit config.py to change SNOWFLAKE_CONNECTION_NAME if needed
```
**Snowflake Connection**:
Configure your connection in `~/.snowflake/connections.toml`:

```toml
[your_connection_name]
account = "your_account_identifier"
user = "your_username"
password = "your_password"  # Or use authenticator for SSO
role = "YOUR_ROLE"  # Role with required permissions
```

### Setup Demo Environment

```bash
# Full setup (using SNOWFLAKE_CONNECTION_NAME inconfig.py )
python setup.py --mode=full

# Or specify connection name
python setup.py --mode=full --connection_name your_connection_name

# Other setup modes:
python setup.py --mode=data-only      # Regenerate data only (see details below)
python setup.py --mode=ai-only        # Recreate AI components only (see details below)
python setup.py --mode=scenario-specific --scenario=equity_research_earnings
```

### 🔄 Setup Modes Explained

#### Primary Modes

| Mode | What it Does | What it Preserves | When to Use |
|------|-------------|-------------------|-------------|
| **`full`** | Complete setup from scratch | Nothing (fresh start) | Initial setup or complete reset |
| **`data-only`** | Regenerates data tables (use `--data-type` for granular control) | AI components in AI schema | After changing data generation logic |
| **`ai-only`** | Recreates AI components (use `--ai-type` for granular control) | All data in RAW and CURATED schemas | After modifying AI configurations |
| **`scenario-specific`** | Setup for specific demo scenario | TBD (Phase 2) | Testing individual scenarios |

#### Granular Data Control (`--data-type`)

Use with `--mode=data-only` to regenerate specific data types:

| Data Type | What it Regenerates | What it Preserves | Example Use Case |
|-----------|-------------------|-------------------|------------------|
| **`all`** (default) | All data tables | Search services, agents | Changed company list or event templates |
| **`structured`** | Companies, prices, clients, estimates | Unstructured data, all AI components | Added new tickers or modified pricing logic |
| **`unstructured`** | Documents, reports, transcripts, news | Structured data, all AI components | Updated content generation prompts |

#### Granular AI Control (`--ai-type`)

Use with `--mode=ai-only` to recreate specific AI components:

| AI Type | What it Recreates | What it Preserves | Example Use Case |
|---------|------------------|-------------------|------------------|
| **`all`** (default) | All AI components | All data tables | After data regeneration or complete AI refresh |
| **`semantic-views`** | Only semantic views | Search services, custom tools, agents, all data | Modified semantic view definitions |
| **`search-services`** | Only Cortex Search services | Semantic views, custom tools, agents, all data | Updated search service configuration |
| **`custom-tools`** | Only custom tools (Python stored procedures) | Semantic views, search services, agents, all data | Modified VaR calculation logic |
| **`agents`** | Only Snowflake Intelligence agents | Semantic views, search services, custom tools, all data | Changed agent instructions or added disclaimer |

**Important Notes:**
- **`data-only` mode**: Semantic views may need recreation if structured data changes (run `--mode=ai-only --ai-type=semantic-views`)
- **Granular modes**: Allow precise control to minimize regeneration time and preserve specific components
- For iterative development: Use granular modes to update only what changed

**Example Workflows:**
```bash
# Scenario 1: Added new companies to TICKER_LIST
python setup.py --mode=data-only --data-type=structured
python setup.py --mode=ai-only --ai-type=semantic-views

# Scenario 2: Updated agent disclaimer instructions
python setup.py --mode=ai-only --ai-type=agents

# Scenario 3: Modified document generation prompts
python setup.py --mode=data-only --data-type=unstructured

# Scenario 4: Updated semantic view definitions
python setup.py --mode=ai-only --ai-type=semantic-views

# Scenario 5: Complete data refresh, preserve AI
python setup.py --mode=data-only --data-type=all
python setup.py --mode=ai-only --ai-type=all
```

The setup process will:
1. ✅ Create database schemas and warehouse
2. ✅ Generate master event log for data correlations
3. ✅ Generate structured data (companies, prices, clients, firm positions)
4. ✅ Generate unstructured data using Cortex Complete
5. ✅ Create semantic views for Cortex Analyst
6. ✅ Create Cortex Search services
7. ✅ Create custom tools (Python stored procedures for VaR calculations)
8. ✅ **Create Snowflake Intelligence agents automatically via SQL**
9. ✅ Validate all components

## 🤖 Agents (Automatically Created)

The setup process **automatically creates** all agents via SQL - no manual configuration needed!

**Agents Created:**

All agents are created in `MARKETS_AI_DEMO.AI` schema and automatically registered with Snowflake Intelligence:

- **MR_EARNINGS_ANALYSIS_AGENT** - Analyzes quarterly earnings, consensus estimates, and management commentary
- **MR_THEMATIC_RESEARCH_AGENT** - Discovers emerging themes and cross-sector trends
- **MR_GLOBAL_MACRO_STRATEGY_AGENT** - Analyzes proprietary macroeconomic signals and develops investment strategies
- **MR_MARKET_REPORTS_AGENT** - Specializes in market structure analysis, regulatory changes, and institutional client insights
- **MR_CLIENT_STRATEGY_AGENT** - Prepares data-driven client meetings and personalized strategic recommendations
- **MR_MARKET_RISK_AGENT** - Performs real-time market risk assessment, portfolio stress testing, and firm-wide exposure analysis

After setup completes, agents are immediately available in:
**Snowsight** → **AI & ML** → **Snowflake Intelligence** → **SNOWFLAKE_INTELLIGENCE_OBJECT_DEFAULT**

> **Note**: Agents are created using SQL `CREATE AGENT` statements during setup, then registered with `ALTER SNOWFLAKE INTELLIGENCE`. See `.cursor/rules/agent-creation.mdc` for implementation details.

## 🎭 Demo Delivery

For complete demo scripts, talking points, and delivery guidance:

👉 **[📋 Complete Demo Script](docs/demo_script.md)**

**Duration**: 90 minutes total (six 15-minute scenarios)

## 📊 Data Architecture

### Database Structure
```
MARKETS_AI_DEMO/
├── RAW/                # Raw event/reference data and temporary staging tables
│   ├── MASTER_EVENT_LOG
│   └── TEMP_PROMPTS_* (ephemeral tables created during data generation)
├── CURATED/            # Industry-standard dimension/fact model
│   ├── DIM_SECTOR
│   ├── DIM_COMPANY
│   ├── DIM_CLIENT
│   ├── DIM_COMPANY_GEO_REVENUE
│   ├── DIM_COMPANY_CREDIT_RATING
│   ├── FACT_STOCK_PRICE_DAILY
│   ├── FACT_CONSENSUS_ESTIMATE
│   ├── FACT_CLIENT_TRADE
│   ├── FACT_PORTFOLIO_HOLDING
│   ├── FACT_CLIENT_ENGAGEMENT
│   ├── FACT_CLIENT_DISCUSSION
│   ├── FACT_EARNINGS_ACTUAL
│   ├── FACT_FIRM_POSITION (NEW: firm-wide portfolio holdings for risk analysis)
│   ├── FACT_MACRO_SIGNAL
│   ├── SEC_FILINGS_CORPUS
│   ├── EARNINGS_TRANSCRIPTS_CORPUS
│   ├── NEWS_ARTICLES_CORPUS
│   └── RESEARCH_REPORTS_CORPUS
└── AI/                 # Semantic views, Cortex Search services, custom tools, and agents
    ├── EARNINGS_ANALYSIS_VIEW (semantic view)
    ├── THEMATIC_RESEARCH_VIEW (semantic view)
    ├── CLIENT_MARKET_IMPACT_VIEW (semantic view)
    ├── GLOBAL_MACRO_SIGNALS_VIEW (semantic view)
    ├── FIRM_EXPOSURE_VIEW (NEW: semantic view for market risk analysis)
    ├── EARNINGS_TRANSCRIPTS_SEARCH (search service)
    ├── RESEARCH_REPORTS_SEARCH (search service)
    ├── NEWS_ARTICLES_SEARCH (search service)
    └── CALCULATE_PORTFOLIO_VAR (NEW: custom tool - Python stored procedure for VaR calculations)
```

### Key Design Principles
- **Event-Driven Correlations**: Master event log drives realistic relationships between prices, news, and earnings
  - Taiwan earthquake events impact semiconductor stocks (NVDA, AMD, AAPL)
  - AI breakthroughs and carbon capture milestones correlated with news and price movements
  - Events placed in middle 80% of date range to ensure proper price correlation
- **Real Tickers, Synthetic Data**: Uses actual stock symbols (AAPL, MSFT, NVDA) with generated financial data
- **Sector and Industry Classification**: Companies organized by both sector (Technology, Healthcare) and industry (Semiconductors, Biotechnology)
- **Geographic Revenue Exposure**: Country-level revenue breakdown for Taiwan, China, US exposure analysis
- **Modular Scenarios**: Each demo segment is completely self-contained (15-minute segments)
- **AI-Generated Content**: Unstructured documents created using Cortex Complete for realism

## 🔧 Configuration

Edit `config.py` to customize:

```python
# Data volume
NUM_COMPANIES = 18               # Number of companies to generate (includes semiconductors)
NUM_CLIENTS = 25                 # Number of client profiles
NUM_HISTORICAL_QUARTERS = 8     # Number of quarters to generate (dynamic)
NUM_HISTORICAL_YEARS = 2        # Number of years of data (calculated from quarters)
NUM_MAJOR_EVENTS = 8            # Number of market events (5 specific + 3 random)

# Company and sector configuration
TICKER_LIST = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX",
               "JNJ", "PG", "KO", "XOM", "JPM", "BAC", "WMT",
               "LIN", "SIEGY", "JMPLY"]  # Includes carbon capture companies

SECTOR_LIST = ["Technology", "Healthcare", "Financial Services", 
               "Consumer Discretionary", "Energy", "Consumer Staples", "Industrials"]

THEMATIC_TAGS = ["Carbon Capture", "Direct Air Capture", "AI/ML", "Cloud Computing",
                 "Electric Vehicles", "Renewable Energy", "Biotechnology",
                 "Supply Chain Disruption", "Geopolitical Risk"]

# AI model configuration
CORTEX_MODEL_NAME = "llama3.1-70b"
AGENT_ORCHESTRATION_MODEL = "claude-sonnet-4-5"

# Connection
SNOWFLAKE_CONNECTION_NAME = "sfseeurope-mstellwall-aws-us-west3"

# Warehouses
COMPUTE_WAREHOUSE = "MARKETS_AI_DEMO_COMPUTE_WH"  # For data processing
SEARCH_WAREHOUSE = "MARKETS_AI_DEMO_SEARCH_WH"    # For Cortex Search
```

## 🧪 Testing & Validation

```bash
# Run validation manually
python -c "
from src.utils.snowpark_session import get_snowpark_session
from src.utils.validation import validate_all_components
session = get_snowpark_session()
validate_all_components(session)
session.close()
"

# Check search service indexing status
python -c "
from src.utils.snowpark_session import get_snowpark_session
from src.ai_components.search_services import get_search_service_status
session = get_snowpark_session()
get_search_service_status(session)
session.close()
"
```

## 🔄 Cleanup & Reset

```bash
# Reset entire demo environment
python sql/cleanup.sql

# Or use SQL directly in Snowsight:
DROP DATABASE IF EXISTS MARKETS_AI_DEMO CASCADE;
```

## 📚 Scenario Extensions

### Adding New Companies
1. Add ticker to `TICKER_LIST` in `config.py`
2. Run `python setup.py --mode=data-only`

### Adding New Themes  
1. Add themes to `THEMATIC_TAGS` in `config.py`
2. Update event templates in `src/data_generation/event_log.py`
3. Regenerate data

### Creating Custom Agents
1. Add configuration to `src/ai_components/agents.py`
2. Create corresponding semantic views if needed
3. Test with sample queries

## 🎯 Business Value Demonstrated

- **50-75% reduction** in earnings analysis time through automated beat/miss analysis
- **Real-time risk assessment** with portfolio stress testing and VaR calculations
- **Cross-sector theme discovery** from unstructured data using AI-powered search
- **Hyper-personalized client insights** at scale with engagement analytics
- **Unified intelligence** across structured and unstructured data sources
- **Event-driven market impact** analysis with correlated price, news, and research data
- **Industry-specific insights** with sector and sub-industry classification (semiconductors, biotech)
- **Geographic exposure analysis** for country-level risk assessment (Taiwan, China)

## 🛠️ Troubleshooting

### Common Issues

**"Connection failed"**
- Verify `connections.toml` exists and has correct connection name
- Check network connectivity to Snowflake

**"Search service not ready"**  
- Search services need 5-10 minutes to index after creation
- Check status with `get_search_service_status()`

**"No data in semantic view"**
- Ensure data generation completed successfully
- Check table row counts in validation

**"Agent not finding results"**
- Verify semantic views work with manual SQL queries
- Check search services are indexed and returning results
- For industry-specific queries (semiconductors), ensure filtering by INDUSTRY not SECTOR
- For geographic queries (Taiwan exposure), verify COUNTRY dimension is being used

**"Low event-price correlation warning"**
- This is expected if events fall at date range edges (first/last 10%)
- Event impacts should show correlation of 60%+ after full data generation
- Check validation output for event count and direction accuracy metrics

**"VaR calculation times out"**
- Increase query timeout in agent configuration (default 30 seconds)
- Verify historical price data exists for all tickers in calculation
- Check that FACT_STOCK_PRICE_DAILY has sufficient data (60+ days)

### Getting Help

1. Run validation: `python setup.py --mode=full --skip-validation=false`
2. Check logs for specific error messages
3. Verify each component individually using test functions

## 📋 Demo Checklist

Before presenting:
- [ ] Run full setup successfully (`python setup.py --mode=full`)
- [ ] Validate all components pass tests
- [ ] Verify all 6 agents were created (check Snowflake Intelligence UI)
- [ ] Test sample queries for each agent/scenario:
  - [ ] Earnings Analysis: "Which companies beat estimates last quarter?"
  - [ ] Thematic Research: "Show me semiconductor companies and carbon capture exposure"
  - [ ] Market Structure: "What are the top EMIR 3.0 topics clients are asking about?"
  - [ ] Client Strategy: "Prepare for meeting with Vanguard Global Equities"
  - [ ] Market Risk: "A 7.0 magnitude earthquake just hit Taiwan. What's our exposure?"
  - [ ] Global Macro: "Show macro signals correlated with Technology sector"
- [ ] Verify search services are indexed (wait 5-10 minutes after setup)
- [ ] Check event-price correlation metrics (should be 60%+)
- [ ] Verify custom tools work: Test VaR calculation with sample tickers
- [ ] Practice demo script timing ([Complete Demo Script](docs/demo_script.md))
- [ ] Review client-specific talking points and business value messages

---
