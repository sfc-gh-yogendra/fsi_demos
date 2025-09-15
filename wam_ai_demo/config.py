# WAM AI Demo - Configuration
# Centralized, parameterized configuration for deterministic rebuilds

import os
from datetime import datetime, timedelta

# Connection & Runtime
DEFAULT_CONNECTION_NAME = "IE_DEMO65_CODE_USER"  # Default connection, can be overridden
DATABASE_NAME = "WAM_AI_DEMO"
WAREHOUSE_PREFIX = "WAM_AI_"
BUILD_WAREHOUSE = f"{WAREHOUSE_PREFIX}BUILD_WH"
CORTEX_WAREHOUSE = f"{WAREHOUSE_PREFIX}CORTEX_WH"

# Stages
CLIENT_DOCS_STAGE = f"{DATABASE_NAME}.RAW.CLIENT_DOCS"

# Volumes and Windows
NUM_ADVISORS = 5
CLIENTS_PER_ADVISOR = 25
ACCOUNTS_PER_CLIENT = 2
MIN_HOLDINGS_PER_ACCOUNT = 12
MAX_HOLDINGS_PER_ACCOUNT = 18

# Date ranges
HISTORY_END_DATE = datetime.now().date()
HISTORY_START_DATE = HISTORY_END_DATE - timedelta(days=365 * 2)  # 2 years
UNSTRUCTURED_DOCS_PER_TICKER = 15
COMMS_PER_CLIENT = 50

# Market Integration
USE_HYBRID_MARKET_DATA = True
MARKET_REAL_PORTFOLIOS = ["US MegaTech Focus", "US Financials Core"]
REGION_MIX = {"us": 0.8, "eu": 0.2}

# Golden Tickers (parameterized for easy changes)
GOLDEN_TICKERS = ["AAPL", "MSFT", "NVDA", "JPM", "V", "SAP"]

# Cortex Complete Configuration (per-corpus overrides)
MODEL_BY_CORPUS = {
    "communications": "llama3.1-70b",
    "research": "llama3.1-70b", 
    "regulatory": "llama3.1-70b"
}

TEMPERATURE_BY_CORPUS = {
    "communications": 0.7,
    "research": 0.4,
    "regulatory": 0.4
}

# Search Services
SEARCH_TARGET_LAG = '5 minutes'

# Build Modes
BUILD_MODES = ['replace_all', 'data_only', 'semantics_and_search_only']

# Communications Mix (Phase 1 distribution targets)
COMMUNICATIONS_MIX = {
    "emails": 0.45,  # 25% of these are threads
    "phone_transcripts": 0.30,  # 15-45 min duration
    "online_meetings": 0.25     # 15-45 min duration
}

# Sentiment Distribution
SENTIMENT_DISTRIBUTION = {
    "neutral": 0.60,
    "positive": 0.25,
    "negative": 0.15
}

# Data Quality Settings
CONTROLLED_NOISE_RATE = 0.025  # 2.5% noise for realism
PORTFOLIO_WEIGHT_TOLERANCE = 0.001  # ±0.1% tolerance

# Enhanced Data Model Settings
USE_TRANSACTION_BASED_MODEL = True
GENERATE_CORPORATE_HIERARCHIES = True
ISSUER_HIERARCHY_DEPTH = 2

# Real Asset Data Integration (REQUIRED)
# System now requires real assets CSV for enhanced demo authenticity
# Set EXTRACT_REAL_ASSETS = True to extract from Marketplace if CSV is missing
USE_REAL_ASSETS_CSV = True  # Always True - real assets are mandatory
REAL_ASSETS_CSV_PATH = './data/real_assets.csv'
EXTRACT_REAL_ASSETS = False  # Set to True to extract from Marketplace

# Market Data Generation (SYNTHETIC ONLY)
# System now uses only synthetic market data for consistent, predictable demo experience
# This ensures deterministic results and eliminates external data dependencies
USE_REAL_MARKET_DATA = False  # Always False - synthetic market data only
# REAL_MARKET_DATA_CSV_PATH = './data/real_market_data.csv'  # DEPRECATED
# EXTRACT_REAL_MARKET_DATA = False  # DEPRECATED

# Marketplace Data Source (requires subscription)
MARKETPLACE_DATABASE = 'FINANCIALS_ECONOMICS_ENTERPRISE'
OPENFIGI_SCHEMA = 'CYBERSYN'

# Transaction Generation Settings
SYNTHETIC_TRANSACTION_MONTHS = 12
TRANSACTION_TYPES = ['BUY', 'SELL', 'DIVIDEND', 'CORPORATE_ACTION']
AVERAGE_MONTHLY_TRANSACTIONS_PER_SECURITY = 2.5

# PDF Generation
PDFS_PER_CLIENT = 2  # questionnaire, advisory agreement

# Validation Settings
REQUIRED_VALIDATIONS = [
    "portfolio_weights_sum_to_100",
    "transaction_log_balances_to_positions", 
    "security_identifier_xref_integrity",
    "issuer_hierarchy_relationships_valid",
    "no_negative_prices_or_market_values",
    "date_ranges_logical_and_consistent",
    "all_foreign_key_relationships_valid"
]

def get_connection_name():
    """Get connection name from environment or use default"""
    return os.getenv('SNOWFLAKE_CONNECTION_NAME', DEFAULT_CONNECTION_NAME)

def get_build_mode():
    """Get build mode from environment or default to replace_all"""
    return os.getenv('BUILD_MODE', 'replace_all')
