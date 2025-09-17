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

# ======================================================
# GOLDEN RECORDS CONFIGURATION
# ======================================================

# Golden Demo Clients (clients with controlled data generation)
GOLDEN_CLIENTS = {
    'sarah_johnson': {
        'first_name': 'Sarah',
        'last_name': 'Johnson',
        'risk_tolerance': 'Conservative',
        'investment_horizon': 'Long-term',
        'target_aum': 169920,
        'portfolio_strategy': 'US Financials Core',
        'portfolio_allocations': {
            'V': 0.504,    # $85,620 target (50.4%)
            'JPM': 0.496   # $84,300 target (49.6%)
        },
        'communications_sentiment': 'positive',
        'esg_interest': True,
        'daughter_name': 'Emily',
        'daughter_age': 17,
        'education_funding_status': {
            'total_goal': 200000,
            'current_savings': 180000,
            'funding_gap': 20000,
            'university_start': 'next_month'
        }
    }
}

# Pre-Generated Documents (stored in golden_records directory)
GOLDEN_DOCUMENTS = {
    'planning_documents': {
        'sarah_johnson': [
            'education_funding_plan.md',
            'investment_policy_statement.md', 
            'comprehensive_financial_plan.md'
        ]
    },
    'research_documents': [
        'microsoft_ai_infrastructure_analysis.md',
        'carbon_neutrality_leaders_report.md',
        'esg_sustainability_framework.md'
    ],
    'regulatory_documents': [
        'finra_2210_communications_rule.md',
        'sec_reg_sp_privacy_rule.md'
    ],
    'advisor_performance': [
        'coaching_opportunities_template.md'
    ]
}

# Controlled Data Generation Parameters
GOLDEN_DATA_CONTROLS = {
    'advisor_performance': {
        'top_quartile_advisors': ['Michael Chen', 'Jennifer Williams'],
        'bottom_quartile_advisors': ['Robert Martinez', 'Lisa Anderson'],
        'coaching_opportunity_patterns': [
            'outdated_planning_documents',
            'low_engagement_frequency',
            'negative_sentiment_trends'
        ]
    },
    'risk_communications': {
        'sarah_johnson_risk_flags': [
            'Expressed concern about market volatility during Q2 call',
            'Mentioned competitor offering higher returns in email'
        ]
    },
    'watchlist_securities': {
        'carbon_negative_leaders': ['MSFT', 'AAPL', 'NVDA'],
        'ai_innovation': ['MSFT', 'NVDA', 'GOOGL'],
        'esg_leaders': ['MSFT', 'AAPL', 'JPM', 'V']
    }
}

# Golden Records Directory Structure
GOLDEN_RECORDS_DIR = 'src/golden_records'
GOLDEN_RECORDS_SUBDIRS = {
    'planning': f'{GOLDEN_RECORDS_DIR}/planning',
    'research': f'{GOLDEN_RECORDS_DIR}/research', 
    'regulatory': f'{GOLDEN_RECORDS_DIR}/regulatory',
    'templates': f'{GOLDEN_RECORDS_DIR}/templates'
}

def get_golden_client_config(client_name: str) -> dict:
    """Get golden client configuration by name"""
    for key, config in GOLDEN_CLIENTS.items():
        if f"{config['first_name']} {config['last_name']}" == client_name:
            return config
    return None

def is_golden_client(first_name: str, last_name: str) -> bool:
    """Check if client is a golden demo client"""
    client_name = f"{first_name} {last_name}"
    return get_golden_client_config(client_name) is not None

def get_golden_document_path(category: str, client_name: str = None, document: str = None) -> str:
    """Get path to golden record document"""
    if client_name and document:
        return f"{GOLDEN_RECORDS_SUBDIRS[category]}/{client_name}_{document}"
    elif document:
        return f"{GOLDEN_RECORDS_SUBDIRS[category]}/{document}"
    else:
        return GOLDEN_RECORDS_SUBDIRS[category]

# Client Attribute Options
RISK_TOLERANCE_OPTIONS = ['Conservative', 'Moderate', 'Aggressive']
INVESTMENT_HORIZON_OPTIONS = ['Short-term', 'Medium-term', 'Long-term']

# Demo Names (for consistent generation)
DEMO_FIRST_NAMES = [
    'Sarah', 'Michael', 'Jennifer', 'David', 'Lisa', 'Robert', 'Emily', 'James', 'Jessica', 'William', 
    'Ashley', 'Christopher', 'Amanda', 'Daniel', 'Stephanie', 'Matthew', 'Michelle', 'Anthony', 'Kimberly', 'Mark',
    'Elizabeth', 'Steven', 'Amy', 'Kenneth', 'Angela', 'Joshua', 'Brenda', 'Kevin', 'Emma', 'Brian'
]

DEMO_LAST_NAMES = [
    'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez',
    'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee',
    'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker'
]

# Watchlist Configurations
WATCHLIST_DEFINITIONS = {
    'Carbon Negative Leaders': {
        'type': 'ESG Thematic',
        'description': 'Companies with strong carbon neutrality commitments and measurable progress toward net-zero emissions goals. Focus on technology and industrial leaders driving climate innovation.',
        'securities': [
            {'ticker': 'MSFT', 'rationale': 'Committed to being carbon negative by 2030, $1B climate innovation fund', 'esg_score': 8.5},
            {'ticker': 'AAPL', 'rationale': 'Carbon neutral by 2030, renewable energy initiatives, sustainable supply chain', 'esg_score': 8.2},
            {'ticker': 'NVDA', 'rationale': 'AI solutions for climate modeling and energy efficiency optimization', 'esg_score': 7.8}
        ]
    },
    'AI Innovation Leaders': {
        'type': 'Technology Thematic',
        'description': 'Companies leading artificial intelligence development and implementation across chips, software, and cloud infrastructure.',
        'securities': [
            {'ticker': 'NVDA', 'rationale': 'Leading AI chip architecture for training and inference', 'esg_score': 7.5},
            {'ticker': 'MSFT', 'rationale': 'AI infrastructure through Azure, OpenAI partnership, Copilot integration', 'esg_score': 8.5},
            {'ticker': 'AAPL', 'rationale': 'On-device AI processing, machine learning capabilities', 'esg_score': 8.2}
        ]
    },
    'ESG Leaders': {
        'type': 'ESG Comprehensive', 
        'description': 'Companies demonstrating leadership across Environmental, Social, and Governance factors with strong sustainability commitments.',
        'securities': [
            {'ticker': 'MSFT', 'rationale': 'Top ESG ratings, renewable energy, inclusive workplace, strong governance', 'esg_score': 8.5},
            {'ticker': 'AAPL', 'rationale': 'Environmental leadership, supply chain responsibility, privacy protection', 'esg_score': 8.2},
            {'ticker': 'SAP', 'rationale': 'Sustainability solutions, carbon neutral by 2025, diverse leadership', 'esg_score': 7.9}
        ]
    }
}

# Manager Configuration
MANAGER_CONFIG = {
    'name': 'Regional Manager',
    'title': 'Regional Director',
    'start_date_years_ago': 8
}

# Email Domain
DEMO_EMAIL_DOMAIN = 'email.com'

def get_build_mode():
    """Get build mode from environment or default to replace_all"""
    return os.getenv('BUILD_MODE', 'replace_all')
