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

# Data Generation Volumes
NUM_ADVISORS = 5
CLIENTS_PER_ADVISOR = 25
ACCOUNTS_PER_CLIENT = 2

# Date ranges
HISTORY_END_DATE = datetime.now().date()
HISTORY_START_DATE = HISTORY_END_DATE - timedelta(days=365 * 2)  # 2 years
UNSTRUCTURED_DOCS_PER_TICKER = 15
COMMS_PER_CLIENT = 50

# Market Integration
REGION_MIX = {"us": 0.8, "eu": 0.2}

# Golden Tickers (parameterized for easy changes)
GOLDEN_TICKERS = ["AAPL", "MSFT", "NVDA", "JPM", "V", "SAP"]

# Cortex Complete Configuration (used by unstructured data generation)
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

# Communications Mix (used by unstructured data generation)
COMMUNICATIONS_MIX = {
    "emails": 0.45,  # 25% of these are threads
    "phone_transcripts": 0.30,  # 15-45 min duration
    "online_meetings": 0.25     # 15-45 min duration
}

# Sentiment Distribution (used by unstructured data generation)
SENTIMENT_DISTRIBUTION = {
    "neutral": 0.60,
    "positive": 0.25,
    "negative": 0.15
}

# Data Quality Settings (used by unstructured data generation)
CONTROLLED_NOISE_RATE = 0.025  # 2.5% noise for realism

# Validation Settings
PORTFOLIO_WEIGHT_TOLERANCE = 0.001  # 0.1% tolerance for portfolio weight validation

# Other removed unused configuration variables:
# - USE_TRANSACTION_BASED_MODEL  
# - GENERATE_CORPORATE_HIERARCHIES, ISSUER_HIERARCHY_DEPTH

# Real Asset Data Integration (REQUIRED)
# System requires real assets CSV for enhanced demo authenticity
# Set EXTRACT_REAL_ASSETS = True to extract from Marketplace if CSV is missing
REAL_ASSETS_CSV_PATH = './data/real_assets.csv'
EXTRACT_REAL_ASSETS = False  # Set to True to extract from Marketplace

# Market Data Generation (SYNTHETIC ONLY)
# System uses only synthetic market data for consistent, predictable demo experience
# This ensures deterministic results and eliminates external data dependencies

# Marketplace Data Source (requires subscription)
MARKETPLACE_DATABASE = 'FINANCIALS_ECONOMICS_ENTERPRISE'
OPENFIGI_SCHEMA = 'CYBERSYN'

# Transaction Generation, PDF Generation, and Validation Settings
# Removed unused configuration variables:
# - SYNTHETIC_TRANSACTION_MONTHS, TRANSACTION_TYPES, AVERAGE_MONTHLY_TRANSACTIONS_PER_SECURITY
# - PDFS_PER_CLIENT, REQUIRED_VALIDATIONS
# These features are either not implemented or use hardcoded values

def get_connection_name():
    """Get connection name from environment or use default"""
    return os.getenv('SNOWFLAKE_CONNECTION_NAME', DEFAULT_CONNECTION_NAME)

def get_build_mode():
    """Get build mode from environment or default to replace_all"""
    return os.getenv('BUILD_MODE', 'replace_all')
