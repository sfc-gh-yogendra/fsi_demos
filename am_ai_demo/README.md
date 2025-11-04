# Snowcrest Asset Management (SAM) AI Demo - 100% Real Assets

A comprehensive demonstration of Snowflake Intelligence for asset management customers, covering Portfolio Managers, Research Analysts, Quantitative Analysts, Client Relationship Managers, and Risk & Compliance Officers.

Focus is to showcase Snowflake Intelligence/Cortex Agents using a number of scenarios that all use Agents.

## Available Scenarios by Role

### Portfolio Manager
**[📖 View Portfolio Manager Scenarios](docs/demo_scenarios_portfolio_manager.md)**

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
**[📖 View Research Analyst Scenarios](docs/demo_scenarios_research_analyst.md)**

**Agent: Research Copilot**
- **Document Research & Analysis** ✅ **IMPLEMENTED**
  - Research synthesis that analyzes thousands of documents across broker reports, earnings transcripts, and press releases to deliver comprehensive investment insights and market intelligence in seconds.
  
- **Earnings Intelligence Extensions** ✅ **IMPLEMENTED**
  - Earnings analysis that combines transcript commentary with financial estimates, guidance tracking, and surprise calculations to provide comprehensive quarterly earnings insights.

### Quantitative Analyst
**[📖 View Quantitative Analyst Scenarios](docs/demo_scenarios_quantitative_analyst.md)**

**Agent: Quant Analyst**
- **Factor Analysis & Performance Attribution** ✅ **IMPLEMENTED**
  - Factor analysis that screens portfolios against multiple quantitative factors, tracks factor evolution over time, and generates professional investment research reports with comprehensive statistical analysis.

### Client Relations
**[📖 View Client Relations Scenarios](docs/demo_scenarios_client_relations.md)**

**Agent: Sales Advisor**
- **Client Reporting & Template Formatting** ✅ **IMPLEMENTED**
  - Client reporting that synthesizes portfolio data, performance metrics, and firm philosophy into professionally formatted quarterly letters following exact template specifications.

### Risk & Compliance Officer
**[📖 View Risk & Compliance Scenarios](docs/demo_scenarios_risk_compliance.md)**

**Agent: ESG Guardian**
- **ESG Risk Monitoring & Policy Compliance** ✅ **IMPLEMENTED**
  - ESG monitoring that scans portfolio holdings against NGO reports and sustainability policies to identify controversies, assess severity, and recommend engagement actions aligned with firm ESG commitments.

**Agent: Compliance Advisor**
- **Mandate Monitoring & Breach Detection** ✅ **IMPLEMENTED**
  - Mandate compliance that continuously monitors portfolio positions against investment guidelines, automatically detects concentration breaches and ESG violations, and cites specific policy sections for immediate remediation.

### Middle Office Operations
**[📖 View Middle Office Scenarios](docs/demo_scenarios_middle_office.md)**

**Agent: Middle Office Copilot**
- **NAV Calculation & Settlement Monitoring** ✅ **IMPLEMENTED**
  - Operations intelligence that monitors trade settlements, reconciliation breaks, NAV calculations, corporate actions, and cash management across all portfolios and custodians—providing real-time exception management and automated root cause analysis for middle office operations teams.


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
- SEC Filings dataset: [Snowflake Marketplace - SEC Filings](https://app.snowflake.com/marketplace/listing/GZTSZAS2KH9/snowflake-public-data-products-sec-filings) or [Snowflake Marketplace - Snowflake Public Data (Free)] https://app.snowflake.com/marketplace/listing/GZTSZ290BV255/snowflake-public-data-products-snowflake-public-data-free
**If you use the Snowflake Public Data (Free) dataset, you also need to update the SECURITIES dict in config.py to use the correct database and schema names**

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
# Build everything with ~88,000 real securities (all scenarios)
# Creates data, semantic views, search services, and all 8 agents automatically
python python/main.py --connection-name my_demo_connection

# Test mode: Build with ~8,800 securities for faster development testing
python python/main.py --connection-name my_demo_connection --test-mode

# Build specific scenarios only
python python/main.py --connection-name my_demo_connection --scenarios portfolio_copilot,research_copilot

# Build only data layer (skip AI components)
python python/main.py --connection-name my_demo_connection --scope data

# Build only semantic views and search services (requires data layer)
python python/main.py --connection-name my_demo_connection --scope semantic
python python/main.py --connection-name my_demo_connection --scope search
```

**What Gets Created:**
- ✅ Database: `SAM_DEMO` with RAW, CURATED, and AI schemas
- ✅ Data: ~88,000 real securities, portfolios, holdings, transactions, documents
- ✅ Semantic Views: 7 views for portfolio analytics, research, quantitative analysis, implementation, SEC filings, supply chain, and middle office
- ✅ Search Services: 12+ services for broker research, earnings, press releases, etc.
- ✅ **Agents: All 8 agents automatically created in `SNOWFLAKE_INTELLIGENCE.AGENTS`**
  - Portfolio Copilot, Research Copilot, Thematic Macro Advisor
  - ESG Guardian, Compliance Advisor, Sales Advisor, Quant Analyst, Middle Office Copilot

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
UNION ALL SELECT 'Transactions', COUNT(*) FROM SAM_DEMO.CURATED.FACT_TRANSACTION
UNION ALL SELECT 'SEC Filings', COUNT(*) FROM SAM_DEMO.CURATED.FACT_SEC_FILINGS
UNION ALL SELECT 'Market Data', COUNT(*) FROM SAM_DEMO.CURATED.FACT_MARKETDATA_TIMESERIES
UNION ALL SELECT 'Broker Research', COUNT(*) FROM SAM_DEMO.CURATED.BROKER_RESEARCH_CORPUS
UNION ALL SELECT 'Earnings Transcripts', COUNT(*) FROM SAM_DEMO.CURATED.EARNINGS_TRANSCRIPTS_CORPUS
UNION ALL SELECT 'Press Releases', COUNT(*) FROM SAM_DEMO.CURATED.PRESS_RELEASES_CORPUS;
```

**Expected Results** (Full Mode):
- Securities: ~88,000 (100% real from OpenFIGI dataset)
  - Equity: ~44,000 | Corporate Bonds: ~8,000 | ETFs: ~36,000
- Issuers: ~68,000 (includes synthetic issuers for complete coverage)
  - Real from SEC_FILINGS: ~7,500 with CIK linkage
- Holdings: ~27,000 positions across 10 portfolios
- Transactions: Transaction-based audit trail
- SEC Filings: ~74M real records from SEC_FILINGS database
- Market Data: Synthetic OHLCV for all securities (5 years history)
- Documents: ~100+ (template-generated from 55+ curated templates)
  - Security-Level: Broker Research (8), Earnings Transcripts (8), Press Releases (8), Internal Research (8), Investment Memos (8)
  - Issuer-Level: NGO Reports (8), Engagement Notes (8)
  - Portfolio-Level: IPS (4), Portfolio Reviews (8)
  - Global: Policy Docs (3), Sales Templates (2), Philosophy Docs (3), Compliance Manual (1), Risk Framework (1), Market Data (3), Macro Events (1), Report Templates (1)
  - Regulatory: Form ADV (1), Form CRS (1), Regulatory Updates (5)

**Expected Results** (Test Mode - 10% volumes):
- Securities: ~8,800 (10% of full volumes)
- Documents: Similar counts (minimal reduction due to small base numbers)

### 2. Verify Agents Created

All 8 agents are automatically created during the build. Verify they exist:

```sql
-- Check agents were created in Snowflake Intelligence
SHOW AGENTS IN SNOWFLAKE_INTELLIGENCE.AGENTS;
```

**Expected Agents:**
- `portfolio_copilot` - Portfolio analytics and benchmarking
- `research_copilot` - Document research and company analysis  
- `thematic_macro_advisor` - Thematic investment strategy
- `esg_guardian` - ESG risk monitoring
- `compliance_advisor` - Mandate monitoring and breach detection
- `sales_advisor` - Client reporting and communications
- `quant_analyst` - Factor analysis and performance attribution
- `middle_office_copilot` - NAV calculation and settlement monitoring

**Agent Details:**
- All agents created with SQL `CREATE AGENT` statements
- Instructions properly formatted with YAML escaping
- Full tool configurations (Cortex Analyst + Cortex Search)
- Available immediately in Snowflake Intelligence UI

### 3. Test Agents

Navigate to **Snowflake Intelligence** in Snowsight and test with quick validation queries:

**Portfolio Copilot:**
```
"What are my top 10 holdings by market value in the SAM Global Thematic Growth portfolio?"
```

**Research Copilot:**
```
"Analyze Microsoft's financial health using the latest SEC filings"
```

**ESG Guardian:**
```
"Check ESG risks in our portfolios"
```

**Middle Office Copilot:**
```
"Show me all failed settlements from the past 3 business days"
```

**Expected Response Format**: 
- Professional formatting with tables and charts
- Concentration warnings with severity indicators (⚠️, 🚨)
- Proper source citations with dates
- Clean data with no duplicates

### 4. Run Demo Scenarios

Use the complete demo scripts organized by role:
- **Index**: [`docs/demo_scenarios.md`](docs/demo_scenarios.md) - Overview with links to all role-specific scenarios
- **Role-Specific Scenarios**: Each role has its own detailed demo script file with step-by-step conversation flows

All agents are pre-configured and ready to use - no manual configuration needed!

## Configuration Defaults

| Setting | Default Value | Description |
|---------|---------------|-------------|
| **Connection** | Required via `--connection-name` | Must specify connection from ~/.snowflake/connections.toml |
| **History** | 5 years | Historical data range for time-series data |
| **Securities** | ~88,000 (full) / ~8,800 (test) | 100% authentic from OpenFIGI via SEC Filings dataset |
| **Issuers** | ~68,000 (includes synthetic) | Real companies from SEC_FILINGS + synthetic for coverage |
| **Identifiers** | TICKER + Bloomberg FIGI | 100% authentic regulatory identifiers |
| **Language** | UK English | All generated content and agent responses |
| **Currency** | USD (fully hedged) | Base currency for all analytics |
| **Returns** | Monthly | Performance calculation frequency |
| **Real Assets** | ✅ Always Used | ~103,000 assets available via V_REAL_ASSETS view |
| **SEC Filings** | ~74M records | Real financial data from SEC_FILINGS database |
| **Market Data** | Synthetic OHLCV | Realistic pricing for all securities |
| **Documents** | ~100+ per scenario | 1 document per entity from 55+ curated templates |
| **Test Mode** | Available | 10% data volumes for faster development |
| **Warehouses** | Auto-created | SAM_DEMO_EXECUTION_WH and SAM_DEMO_CORTEX_WH |
| **RNG Seed** | 42 | Deterministic generation for consistent builds |

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
│   ├── build_ai.py            # AI components (semantic views, search services, agents)
│   ├── create_agents.py       # SQL-based agent creation (all 8 agents)
│   └── extract_real_assets.py # Real asset view creation from SEC Filings
├── research/                   # Background research and analysis
├── .gitignore                  # Git ignore patterns (logs, cache, backups)
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Data Architecture

### Database: `SAM_DEMO`
- **RAW Schema**: Real assets view (V_REAL_ASSETS) + raw documents
  - V_REAL_ASSETS: ~103,000 securities from SEC Filings dataset
  - Raw document tables for template-based generation
- **CURATED Schema**: Industry-standard dimension/fact model
  - 20+ dimension and fact tables with complete data model
  - Transaction-based holdings with immutable SecurityID
  - Real SEC filing data (~74M records)
  - Synthetic market data for all securities
- **AI Schema**: Enhanced semantic views and Cortex Search services
  - 7 semantic views (Analyst, Research, Quant, Implementation, SEC Filings, Supply Chain, Middle Office)
  - 12+ Cortex Search services with proper document linkage

### Snowflake Intelligence Agents: `SNOWFLAKE_INTELLIGENCE.AGENTS`
- **Automated Creation**: All 8 agents created via SQL during build process
  - Portfolio Copilot, Research Copilot, Thematic Macro Advisor
  - ESG Guardian, Compliance Advisor, Sales Advisor, Quant Analyst
  - Middle Office Copilot
- **Implementation**: `python/create_agents.py` with proper YAML formatting
- **Availability**: Immediately available in Snowflake Intelligence UI

## Documentation

### Core Documentation

**Agent Configuration Standards**:
- [`docs/agents_setup.md`](docs/agents_setup.md) - **Production-Ready Agent Configurations**
  - All 8 agents fully configured with comprehensive tool descriptions
  - Complete response and orchestration instructions
  - Aligned with Snowflake Intelligence best practices
  - Used as source for automated SQL-based agent creation
  
- `.cursor/rules/agent-config.mdc` - **Complete Agent Creation Guide**
  - SQL-based automated agent creation workflow
  - Comprehensive tool description patterns (Data Coverage, When to Use/NOT, Query Best Practices)
  - Business Context patterns (Organization, Key Terms, Categories)
  - Complete workflow examples with step-by-step sequences
  - Error handling scenarios with recovery steps
  - Structured response templates with complete examples
  - Validation checklist and quality assurance guidance

**Demo Scenarios**:
- [`docs/demo_scenarios.md`](docs/demo_scenarios.md) - Index and overview of all demo scenarios organized by role
- [`docs/demo_scenarios_portfolio_manager.md`](docs/demo_scenarios_portfolio_manager.md) - Portfolio Manager scenarios (Portfolio Copilot, Thematic Macro Advisor)
- [`docs/demo_scenarios_research_analyst.md`](docs/demo_scenarios_research_analyst.md) - Research Analyst scenarios (Research Copilot)
- [`docs/demo_scenarios_quantitative_analyst.md`](docs/demo_scenarios_quantitative_analyst.md) - Quantitative Analyst scenarios (Quant Analyst)
- [`docs/demo_scenarios_client_relations.md`](docs/demo_scenarios_client_relations.md) - Client Relations scenarios (Sales Advisor)
- [`docs/demo_scenarios_risk_compliance.md`](docs/demo_scenarios_risk_compliance.md) - Risk & Compliance scenarios (ESG Guardian, Compliance Advisor)
- [`docs/demo_scenarios_middle_office.md`](docs/demo_scenarios_middle_office.md) - Middle Office Operations scenarios (Middle Office Copilot)

**Data Model**:
- [`docs/data_model.md`](docs/data_model.md) - Industry-standard data architecture
  - 100% real assets from SEC Filings dataset (14,000+ securities)
  - Immutable SecurityID with transaction-based holdings
  - Issuer hierarchies and corporate relationships
  - Enhanced document integration patterns

**Internal Development Rules** (`.cursor/rules/`):
- `agent-config.mdc` - **SQL-based agent creation** with automated deployment patterns
- `semantic-views.mdc` - Semantic view creation with WITH EXTENSION patterns
- `cortex-search.mdc` - Cortex Search service creation and testing
- `data-generation.mdc` - Enhanced data generation with 100% real assets
- `unstructured-data-generation.mdc` - Template-based document generation
- `project-setup.mdc` - Project structure and automated agent status tracking
- `troubleshooting.mdc` - Comprehensive troubleshooting guide

### Configuration Best Practices Summary

#### Tool Descriptions (Cortex Analyst & Cortex Search)
✅ **Required Elements**:
- Data Coverage: Historical range, update frequency, record counts, refresh schedule
- When to Use: 3-4 specific examples with query patterns
- When NOT to Use: Alternative tools for anti-patterns
- Query/Search Best Practices: ✅/❌ examples for good vs bad queries

✅ **Quality Standards**:
- Specific, not generic ("portfolio analytics" not "gets data")
- Exact thresholds and values (">6.5% warning" not "high concentration")
- Clear boundaries between tools with alternatives specified

#### Planning Instructions
✅ **Required Elements**:
- Business Context: Organization details, key terms with exact thresholds, domain categories
- Tool Selection: Query patterns that trigger each tool with ✅/❌ examples
- Complete Workflows: 2-3 multi-step workflows with tool sequences and synthesis patterns
- Error Handling: 3-5 common scenarios with detection, recovery, messages, alternatives

✅ **Quality Standards**:
- Explicit business rules (not assumed context)
- Step-by-step tool sequences (not "use appropriate tools")
- Complete workflow examples with realistic questions and responses

#### Response Instructions
✅ **Required Elements**:
- Style: Tone, lead-with pattern, terminology, precision, limitations
- Presentation: Tables, charts, formatting rules with specific criteria
- Response Structures: 2-3 templates with complete examples

✅ **Quality Standards**:
- Specific patterns ("Weight is 8.2% (⚠️ exceeds 6.5%) as of 31 Dec 2024")
- Not generic guidance ("be professional and helpful")
- Domain-specific formatting rules with examples

### Quick Reference: Agent Enhancement Impact

**Before Enhancement**:
- Tool descriptions: 2-3 sentences per tool
- Planning instructions: Basic tool selection logic
- Response instructions: General style guidance

**After Enhancement** (Following Snowflake Best Practices):
- Tool descriptions: 15-25 lines per tool with comprehensive sections
- Planning instructions: Business context + workflows + error handling
- Response instructions: Structured with style, presentation, and templates
- **Total Enhancement**: 3-4x more detail per agent, all following Snowflake Intelligence best practices

### Related Resources

- [Snowflake Intelligence Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence)
- [Cortex Analyst Guide](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-analyst)
- [Cortex Search Documentation](https://docs.snowflake.com/en/user-guide/snowflake-cortex/cortex-search)
- [Best Practices Guide](research/FINAL_%20Definitive%20Guide%20for%20Building%20Cortex%20Agents.md) - Internal research on Snowflake agent configuration

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
