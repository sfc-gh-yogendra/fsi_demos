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

# Date ranges (extended for advisor benchmarking)
HISTORY_YEARS = 5  # Number of years of history to generate

# Note: Use functions to ensure dates are calculated when called, not when module is imported
def get_history_end_date():
    """Get the end date for historical data generation (today)"""
    return datetime.now().date()

def get_history_start_date():
    """Get the start date for historical data generation"""
    return get_history_end_date() - timedelta(days=365 * HISTORY_YEARS)

def get_market_data_rowcount():
    """Calculate rowcount needed for market data generation based on history years"""
    # Need enough days to cover all years plus some buffer
    # Estimate ~365 days per year + 10% buffer to ensure we have enough
    return int(HISTORY_YEARS * 365 * 1.1)

# For compatibility with existing code, but these should be replaced with function calls
HISTORY_END_DATE = None  # Use get_history_end_date() instead
HISTORY_START_DATE = None  # Use get_history_start_date() instead
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

# Build Scopes
BUILD_SCOPES = ['all', 'data', 'semantic', 'search']

# Available Scenarios
AVAILABLE_SCENARIOS = ['advisor', 'analyst', 'guardian', 'manager', 'all']

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

# Advisor Benchmarking Configuration
PEER_GROUP_THRESHOLDS = {
    "small_max": 50_000_000,      # < $50M
    "medium_max": 150_000_000     # $50M-$150M (>$150M = Large)
}

FEE_SCHEDULE_BPS = {
    "tier_1": {"min": 0, "max": 1_000_000, "bps": 0.0085},           # 0-$1M: 0.85%
    "tier_2": {"min": 1_000_000, "max": 5_000_000, "bps": 0.0070},   # $1-$5M: 0.70%
    "tier_3": {"min": 5_000_000, "max": 10_000_000, "bps": 0.0055},  # $5-$10M: 0.55%
    "tier_4": {"min": 10_000_000, "max": float('inf'), "bps": 0.0040} # >$10M: 0.40%
}

PLANNING_FEE_PER_HOUSEHOLD = 1000  # $1,000/household/year when current
PLANNING_RECENCY_MONTHS = 6        # ≤6 months = "current"
ENGAGEMENT_TARGET_PER_MONTH = 1    # 1 interaction per client per month

# Client Departure Configuration
CLIENT_DEPARTURE_RATE_ANNUAL = 0.075  # 7.5% annual departure rate
DEPARTURE_REASONS = {
    "Performance Dissatisfaction": 0.30,
    "Fee Concerns": 0.25,
    "Advisor Change": 0.20,
    "Life Event": 0.15,
    "Competitor": 0.10
}

# Transaction Configuration
TRANSACTIONS_PER_ACCOUNT_MONTH = {"min": 2, "max": 5}
ACTIVE_TRADER_PERCENTAGE = 0.20  # 20% of accounts are more active
ACTIVE_TRADER_TRANSACTIONS_MONTH = {"min": 5, "max": 10}

# Risk Signal Configuration
RISK_FLAG_RATE = 0.025  # 2.5% of communications have risk flags
RISK_CATEGORIES = [
    "PERFORMANCE_GUARANTEE",
    "SUITABILITY_MISMATCH", 
    "UNDOCUMENTED_REC",
    "PII_BREACH",
    "ESG_GREENWASHING"
]

# Planning Document Configuration
PLANNING_MULTIPLE_VERSIONS_RATE = 0.40  # 40% of clients have multiple versions
PLANNING_VERSIONS_RANGE = {"min": 1, "max": 3}

# Client Tenure Configuration (for varied history)
CLIENT_TENURE_MONTHS = {"min": 6, "max": HISTORY_YEARS * 12}  # 6 months to configured history years

def get_build_mode():
    """Get build mode from environment or default to replace_all"""
    return os.getenv('BUILD_MODE', 'replace_all')
