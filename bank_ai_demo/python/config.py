"""
Glacier First Bank AI Intelligence Demo Configuration
Master configuration for all phases and scenarios
"""

import os
from datetime import datetime, timedelta
from typing import Dict, Any, List

# =============================================================================
# GLOBAL SETTINGS
# =============================================================================

DEMO_NAME = "Glacier First Bank AI Intelligence Demo"
INSTITUTION_NAME = "Glacier First Bank"
INSTITUTION_PROFILE = "pan-EU universal bank; strong Corporate & Commercial; strong Wealth"

# =============================================================================
# ENVIRONMENT CONFIGURATION
# =============================================================================

SNOWFLAKE = {
    "database": "BANK_AI_DEMO",
    "compute_warehouse": "BANK_AI_DEMO_COMPUTE_WH",
    "search_warehouse": "BANK_AI_DEMO_SEARCH_WH",
    "ai_schema": "AI"  # Unified schema for all AI objects (Cortex Search, Semantic Views, Custom Tools)
}

# =============================================================================
# DEMO STANDARDS
# =============================================================================

LANGUAGE = "en-GB"
CURRENCY = "EUR"
CURRENCY_FORMAT = "€1,234,567.89"
REGULATORY_FRAMEWORK = "EU/EBA"
TIMEZONE = "Europe/Brussels"

# =============================================================================
# CONTENT GENERATION
# =============================================================================

LLM_MODEL = "llama3.1-70b"
GENERATION_TEMPERATURE = 0.7
GENERATION_SEED = 42
MAX_TOKENS = 4000

# =============================================================================
# PHASE CONFIGURATION
# =============================================================================

CURRENT_PHASE = 1
PHASE_1 = {
    "name": "Foundation - AML/KYC & Credit Analysis",
    "scenarios": ["aml_kyc_edd", "credit_analysis"],
    "completion_criteria": [
        "Both scenarios work end-to-end with realistic data",
        "Cross-domain intelligence connections demonstrable",
        "All wow moments polished and reliable",
        "Presenter guidance complete"
    ]
}

# =============================================================================
# DATA GENERATION SCALE CONFIGURATION
# =============================================================================

SCALES = {
    "mini": {
        "description": "Fast testing scale",
        # Phase 1 data
        "entities": 50,
        "entity_relationships": 100,
        "customers": 25,
        "transactions": 5000,
        "compliance_documents": 100,
        "loan_applications": 5,
        "historical_loans": 150,
        "news_articles": 150,
        "alerts": 50,
        "alert_disposition_history": 500,
        # Phase 2 data
        "client_crm_records": 20,
        "client_opportunities": 40,
        "client_documents": 60,  # call notes, emails, news
        "holdings": 100,  # holdings across all wealth clients
        "model_portfolios": 3,  # conservative, balanced, growth
        "wealth_clients": 10,  # subset of customers with wealth profiles
        "wealth_meeting_notes": 30,
    },
    "demo": {
        "description": "Balanced demo scale - optimal for agent responses",
        # Phase 1 data
        "entities": 500,
        "entity_relationships": 1200,
        "customers": 200,
        "transactions": 50000,
        "compliance_documents": 800,
        "loan_applications": 25,
        "historical_loans": 1500,
        "news_articles": 1200,
        "alerts": 250,
        "alert_disposition_history": 2500,
        # Phase 2 data
        "client_crm_records": 150,
        "client_opportunities": 300,
        "client_documents": 450,  # call notes, emails, news
        "holdings": 600,  # holdings across all wealth clients
        "model_portfolios": 5,  # conservative, balanced, growth, aggressive, income
        "wealth_clients": 50,  # subset of customers with wealth profiles
        "wealth_meeting_notes": 200,
    }
}

DEFAULT_SCALE = "demo"

# =============================================================================
# DATE RANGES
# =============================================================================

# Calculate dates dynamically based on current date
_current_date = datetime.now().date()
_yesterday = _current_date - timedelta(days=1)

DATE_RANGES = {
    "historical_start": (_yesterday - timedelta(days=365*5)).strftime("%Y-%m-%d"),  # 5 years before yesterday
    "historical_end": _yesterday.strftime("%Y-%m-%d"),
    "current_date": _yesterday.strftime("%Y-%m-%d"),
    "future_projections": (_yesterday + timedelta(days=365*2)).strftime("%Y-%m-%d")  # 2 years from yesterday
}

# =============================================================================
# KEY ENTITIES FOR DEMO SCENARIOS
# =============================================================================

KEY_ENTITIES = {
    "primary_aml_subject": {
        "entity_id": "GTV_SA_001",
        "name": "Global Trade Ventures S.A.",
        "country": "LUX",
        "industry": "International Trade",
        "esg_rating": "C+"
    },
    "primary_credit_applicant": {
        "entity_id": "INN_DE_001",
        "name": "Innovate GmbH",
        "country": "DEU",
        "industry": "Software Services",
        "esg_rating": "B+"
    },
    "shared_risk_vendor": {
        "entity_id": "NSC_UK_001",
        "name": "Northern Supply Chain Ltd",
        "country": "GBR",
        "industry": "Logistics & Transportation",
        "risk_profile": "HIGH"
    },
    # Shell company network for network analysis scenario
    "shell_network_1": {
        "entity_id": "SHELL_NET_001",
        "name": "Baltic Trade Ltd",
        "country": "GIB",
        "industry": "Import/Export",
        "esg_rating": "D"
    },
    "shell_network_2": {
        "entity_id": "SHELL_NET_002",
        "name": "Nordic Commerce S.A.",
        "country": "GIB",
        "industry": "Import/Export",
        "esg_rating": "D"
    },
    "shell_network_3": {
        "entity_id": "SHELL_NET_003",
        "name": "Alpine Export GmbH",
        "country": "GIB",
        "industry": "Import/Export",
        "esg_rating": "D"
    },
    "shell_network_4": {
        "entity_id": "SHELL_NET_004",
        "name": "Adriatic Import Ltd",
        "country": "GIB",
        "industry": "Import/Export",
        "esg_rating": "D"
    },
    "shell_network_5": {
        "entity_id": "SHELL_NET_005",
        "name": "Aegean Trade S.A.",
        "country": "GIB",
        "industry": "Import/Export",
        "esg_rating": "D"
    },
    # Phase 2 key entities
    "primary_rm_client": {
        "entity_id": "EAG_FR_001",
        "name": "European Automotive Group S.A.",
        "country": "FRA",
        "industry": "Automotive Manufacturing",
        "esg_rating": "B",
        "relationship_manager": "Claire Dubois",
        "account_status": "ACTIVE"
    },
    "primary_wealth_client": {
        "entity_id": "HTF_LUX_001",
        "name": "Heritage Trust Fund",
        "country": "LUX",
        "industry": "Private Investment",
        "esg_rating": "A",
        "wealth_advisor": "Marcus Weber",
        "risk_tolerance": "MODERATE",
        "aum": 50000000  # €50M assets under management
    },
    "opportunity_target": {
        "entity_id": "RES_IT_001",
        "name": "Renewable Energy Solutions Italia",
        "country": "ITA",
        "industry": "Renewable Energy",
        "esg_rating": "A+",
        "relationship_status": "PROSPECT"
    }
}

# =============================================================================
# MARKET CONTEXT THEMES
# =============================================================================

MARKET_THEMES = [
    {
        "name": "ESG Compliance",
        "weight": 0.30,
        "keywords": ["sustainability", "ESG reporting", "green finance", "carbon footprint", "sustainable development goals"],
        "document_types": ["policy_docs", "news_articles", "research_reports"]
    },
    {
        "name": "Supply Chain Risk",
        "weight": 0.25,
        "keywords": ["supply chain disruption", "geopolitical risk", "logistics", "vendor dependency", "supply chain resilience"],
        "document_types": ["news_articles", "risk_reports", "compliance_documents"]
    },
    {
        "name": "Inflation Impact",
        "weight": 0.20,
        "keywords": ["inflation", "interest rates", "debt service", "margin pressure", "cost inflation"],
        "document_types": ["credit_documents", "financial_analysis", "market_reports"]
    },
    {
        "name": "Digital Transformation",
        "weight": 0.15,
        "keywords": ["digitalization", "AI adoption", "cybersecurity", "cloud migration", "automation"],
        "document_types": ["business_plans", "technology_reports"]
    },
    {
        "name": "Regulatory Change",
        "weight": 0.10,
        "keywords": ["regulatory update", "compliance requirements", "Basel III", "MiFID II", "AML directive"],
        "document_types": ["policy_docs", "regulatory_updates"]
    }
]

# =============================================================================
# EXTERNAL DATA PROVIDER SIMULATION
# =============================================================================

EXTERNAL_DATA_PROVIDERS = {
    "financial_data": {
        "sp_global": {
            "name": "S&P Global Market Intelligence",
            "attribution": "S&P Global Market Intelligence via Snowflake Marketplace",
            "data_types": ["financial_statements", "company_profiles", "credit_ratings"],
            "coverage": "Global public and large private companies",
            "update_frequency": "quarterly"
        },
        "moody_analytics": {
            "name": "Moody's Analytics",
            "attribution": "Moody's Analytics via Snowflake Marketplace",
            "data_types": ["credit_scores", "probability_of_default", "financial_ratios"],
            "coverage": "Corporate credit analysis",
            "update_frequency": "monthly"
        }
    },
    "news_media": {
        "reuters": {
            "name": "Reuters News Feed",
            "attribution": "Reuters News Feed via Snowflake Marketplace",
            "data_types": ["breaking_news", "financial_news", "corporate_announcements"],
            "languages": ["en", "de", "fr"],
            "update_frequency": "real-time"
        },
        "bloomberg": {
            "name": "Bloomberg News",
            "attribution": "Bloomberg News via Snowflake Marketplace",
            "data_types": ["market_analysis", "company_news", "regulatory_updates"],
            "focus": "Financial markets and regulation",
            "update_frequency": "real-time"
        }
    },
    "compliance_data": {
        "dow_jones": {
            "name": "Dow Jones Risk & Compliance",
            "attribution": "Dow Jones Risk & Compliance via Snowflake Marketplace",
            "data_types": ["pep_lists", "sanctions_screening", "adverse_media"],
            "coverage": "Global compliance and regulatory data",
            "update_frequency": "daily"
        },
        "lseg": {
            "name": "LSEG World-Check",
            "attribution": "LSEG World-Check via Snowflake Marketplace",
            "data_types": ["sanctions_lists", "pep_screening", "enhanced_due_diligence"],
            "coverage": "Global risk intelligence",
            "update_frequency": "daily"
        }
    }
}

# =============================================================================
# SCENARIO CONFIGURATION
# =============================================================================

SCENARIOS = {
    "aml_kyc_edd": {
        "name": "AML/KYC Enhanced Due Diligence",
        "description": "AI-powered enhanced due diligence with cross-domain intelligence",
        "required_data": ["entities", "compliance_documents", "news_articles", "entity_relationships"],
        "required_services": ["compliance_docs_search_svc", "news_research_search_svc"],
        "required_views": ["customer_risk_sv", "ecosystem_risk_sv"]
    },
    "credit_analysis": {
        "name": "Credit Risk Analysis & Cohort Modeling",
        "description": "AI-enhanced credit analysis with historical cohort modeling",
        "required_data": ["loan_applications", "historical_loans", "credit_policy_documents"],
        "required_services": ["credit_policy_search_svc", "loan_documents_search_svc"],
        "required_views": ["credit_risk_sv"]
    },
    "transaction_monitoring": {
        "name": "Intelligent Transaction Monitoring & Alert Triage",
        "description": "AI-powered alert triage with ML-based false positive reduction and network analysis",
        "required_data": ["alerts", "alert_disposition_history", "customers", "transactions"],
        "required_services": ["compliance_docs_search_svc", "news_research_search_svc"],
        "required_views": ["transaction_monitoring_sv", "aml_kyc_risk_sv"]
    },
    "periodic_kyc_review": {
        "name": "Streamlined Periodic KYC Reviews",
        "description": "Automated periodic KYC review with change detection and low-touch processing",
        "required_data": ["customers", "transactions", "compliance_documents"],
        "required_services": ["compliance_docs_search_svc", "news_research_search_svc"],
        "required_views": ["aml_kyc_risk_sv"]
    },
    "network_analysis": {
        "name": "Trade-Based Money Laundering Network Detection",
        "description": "Graph-based network analysis for shell company detection and TBML typology identification",
        "required_data": ["entities", "entity_relationships", "transactions", "customers"],
        "required_services": ["compliance_docs_search_svc"],
        "required_views": ["network_analysis_sv", "cross_domain_intelligence_sv"]
    },
    # Phase 2 Scenarios
    "corp_relationship_manager": {
        "name": "Corporate Relationship Manager - Client Intelligence",
        "description": "Proactive opportunity sourcing and client intelligence with cross-entity reasoning",
        "required_data": ["customers", "transactions", "entity_relationships", "client_crm", "client_opportunities", "client_documents"],
        "required_services": ["client_documents_search_svc"],
        "required_views": ["corporate_client_360_sv"]
    },
    "wealth_advisor": {
        "name": "Wealth Advisor - Portfolio Alignment & Rebalancing",
        "description": "Portfolio alignment analysis and what-if rebalancing with tax impact and risk calculations",
        "required_data": ["customers", "holdings", "model_portfolios", "wealth_client_profiles", "wealth_meeting_notes"],
        "required_services": ["wealth_notes_search_svc"],
        "required_views": ["wealth_client_sv"],
        "custom_tools": ["portfolio_modeler"]
    }
}

# =============================================================================
# PHASE 2 DATA SCHEMAS
# =============================================================================

PHASE_2_SCHEMAS = {
    "client_crm": {
        "table_name": "CLIENT_CRM",
        "schema": "RAW_DATA",
        "columns": {
            "CRM_ID": "STRING",  # Primary key
            "CUSTOMER_ID": "STRING",  # Foreign key to CUSTOMERS
            "RELATIONSHIP_MANAGER": "STRING",
            "LAST_CONTACT_DATE": "DATE",
            "ACCOUNT_STATUS": "STRING",  # ACTIVE, PROSPECT, INACTIVE
            "ACCOUNT_TIER": "STRING",  # PREMIUM, STANDARD, BASIC
            "NOTES_SUMMARY": "STRING",  # Brief summary of recent interactions
            "RISK_OPPORTUNITIES_COUNT": "NUMBER",
            "CREATED_DATE": "TIMESTAMP_NTZ"
        },
        "constraints": {
            "primary_key": ["CRM_ID"],
            "foreign_keys": [{"column": "CUSTOMER_ID", "references": "CUSTOMERS(CUSTOMER_ID)"}]
        }
    },
    "client_opportunities": {
        "table_name": "CLIENT_OPPORTUNITIES",
        "schema": "CURATED",
        "columns": {
            "OPPORTUNITY_ID": "STRING",  # Primary key
            "CUSTOMER_ID": "STRING",  # Foreign key to CUSTOMERS
            "OPPORTUNITY_TYPE": "STRING",  # CROSS_SELL, UPSELL, RISK_MITIGATION, NEW_PRODUCT
            "OPPORTUNITY_DESCRIPTION": "STRING",
            "POTENTIAL_VALUE": "NUMBER",  # Estimated revenue impact
            "SOURCE_TYPE": "STRING",  # call_note, internal_email, news, transaction_pattern
            "SOURCE_DOCUMENT_ID": "STRING",  # Reference to originating document
            "PRIORITY": "STRING",  # HIGH, MEDIUM, LOW
            "STATUS": "STRING",  # OPEN, IN_PROGRESS, CLOSED_WON, CLOSED_LOST
            "CREATED_DATE": "TIMESTAMP_NTZ",
            "LAST_UPDATED_DATE": "TIMESTAMP_NTZ"
        },
        "constraints": {
            "primary_key": ["OPPORTUNITY_ID"],
            "foreign_keys": [{"column": "CUSTOMER_ID", "references": "CUSTOMERS(CUSTOMER_ID)"}]
        }
    },
    "holdings": {
        "table_name": "HOLDINGS",
        "schema": "CURATED",
        "columns": {
            "HOLDING_ID": "STRING",  # Primary key
            "CUSTOMER_ID": "STRING",  # Foreign key to CUSTOMERS
            "ASSET_TYPE": "STRING",  # EQUITY, BOND, ALTERNATIVE, CASH
            "ASSET_CLASS": "STRING",  # DOMESTIC_EQUITY, INTL_EQUITY, GOVT_BOND, CORP_BOND, REAL_ESTATE, etc.
            "ASSET_NAME": "STRING",
            "TICKER_SYMBOL": "STRING",
            "QUANTITY": "NUMBER",
            "CURRENT_VALUE": "NUMBER",  # in EUR
            "COST_BASIS": "NUMBER",  # for tax calculations
            "UNREALIZED_GAIN_LOSS": "NUMBER",
            "ALLOCATION_PCT": "NUMBER",  # percentage of total portfolio
            "AS_OF_DATE": "DATE",
            "LAST_UPDATED_DATE": "TIMESTAMP_NTZ"
        },
        "constraints": {
            "primary_key": ["HOLDING_ID"],
            "foreign_keys": [{"column": "CUSTOMER_ID", "references": "CUSTOMERS(CUSTOMER_ID)"}]
        }
    },
    "model_portfolios": {
        "table_name": "MODEL_PORTFOLIOS",
        "schema": "CURATED",
        "columns": {
            "MODEL_ID": "STRING",  # Primary key
            "MODEL_NAME": "STRING",  # CONSERVATIVE, BALANCED, GROWTH, AGGRESSIVE, INCOME
            "RISK_PROFILE": "STRING",  # LOW, MODERATE, HIGH
            "TARGET_EQUITY_PCT": "NUMBER",
            "TARGET_BOND_PCT": "NUMBER",
            "TARGET_ALTERNATIVE_PCT": "NUMBER",
            "TARGET_CASH_PCT": "NUMBER",
            "EXPECTED_ANNUAL_RETURN_PCT": "NUMBER",
            "EXPECTED_VOLATILITY_PCT": "NUMBER",  # Standard deviation
            "DESCRIPTION": "STRING",
            "REBALANCE_FREQUENCY_DAYS": "NUMBER",  # 90, 180, 365
            "CREATED_DATE": "TIMESTAMP_NTZ"
        },
        "constraints": {
            "primary_key": ["MODEL_ID"]
        }
    },
    "wealth_client_profiles": {
        "table_name": "WEALTH_CLIENT_PROFILES",
        "schema": "CURATED",
        "columns": {
            "PROFILE_ID": "STRING",  # Primary key
            "CUSTOMER_ID": "STRING",  # Foreign key to CUSTOMERS
            "MODEL_PORTFOLIO_ID": "STRING",  # Foreign key to MODEL_PORTFOLIOS
            "WEALTH_ADVISOR": "STRING",
            "RISK_TOLERANCE": "STRING",  # CONSERVATIVE, MODERATE, AGGRESSIVE
            "TAX_STATUS": "STRING",  # STANDARD, TAX_DEFERRED, TAX_EXEMPT
            "INVESTMENT_OBJECTIVES": "STRING",  # GROWTH, INCOME, PRESERVATION, BALANCED
            "TOTAL_AUM": "NUMBER",  # Assets under management in EUR
            "CONCENTRATION_THRESHOLD_PCT": "NUMBER",  # Alert if any single holding exceeds this %
            "REBALANCE_TRIGGER_PCT": "NUMBER",  # Trigger rebalance if deviation exceeds this %
            "LAST_REBALANCE_DATE": "DATE",
            "NEXT_REVIEW_DATE": "DATE",
            "CREATED_DATE": "TIMESTAMP_NTZ",
            "LAST_UPDATED_DATE": "TIMESTAMP_NTZ"
        },
        "constraints": {
            "primary_key": ["PROFILE_ID"],
            "foreign_keys": [
                {"column": "CUSTOMER_ID", "references": "CUSTOMERS(CUSTOMER_ID)"},
                {"column": "MODEL_PORTFOLIO_ID", "references": "MODEL_PORTFOLIOS(MODEL_ID)"}
            ]
        }
    }
}

PHASE_2_DOCUMENT_TYPES = {
    "client_documents": [
        {"type": "call_note", "weight": 0.4, "description": "Relationship manager call notes from client meetings"},
        {"type": "internal_email", "weight": 0.3, "description": "Internal emails about client strategy and risks"},
        {"type": "client_news", "weight": 0.3, "description": "News articles about client companies"}
    ],
    "wealth_meeting_notes": [
        {"type": "portfolio_review", "weight": 0.4, "description": "Quarterly portfolio review meeting notes"},
        {"type": "investment_strategy", "weight": 0.3, "description": "Investment strategy discussion notes"},
        {"type": "rebalancing_decision", "weight": 0.3, "description": "Portfolio rebalancing decision documentation"}
    ]
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_snowflake_config(connection_name: str = None) -> Dict[str, str]:
    """Get Snowflake connection configuration."""
    if not connection_name:
        connection_name = os.getenv('CONNECTION_NAME')
    
    if not connection_name:
        raise ValueError("Connection name is required. Provide --connection-name or set CONNECTION_NAME environment variable.")
    
    config = SNOWFLAKE.copy()
    config["connection_name"] = connection_name
    return config

def get_scale_config(scale: str = None) -> Dict[str, Any]:
    """Get data generation scale configuration."""
    scale = scale or DEFAULT_SCALE
    if scale not in SCALES:
        raise ValueError(f"Invalid scale '{scale}'. Valid scales: {list(SCALES.keys())}")
    return SCALES[scale]

def get_scenario_config(scenario: str) -> Dict[str, Any]:
    """Get configuration for a specific scenario."""
    if scenario not in SCENARIOS:
        raise ValueError(f"Invalid scenario '{scenario}'. Valid scenarios: {list(SCENARIOS.keys())}")
    return SCENARIOS[scenario]

def get_all_scenarios() -> List[str]:
    """Get list of all available scenarios."""
    return list(SCENARIOS.keys())

def validate_scenarios(scenarios: List[str]) -> List[str]:
    """Validate and return list of scenarios."""
    if not scenarios or scenarios == ["all"]:
        return get_all_scenarios()
    
    invalid_scenarios = [s for s in scenarios if s not in SCENARIOS]
    if invalid_scenarios:
        raise ValueError(f"Invalid scenarios: {invalid_scenarios}. Valid scenarios: {list(SCENARIOS.keys())}")
    
    return scenarios

def validate_connection(connection_name: str) -> bool:
    """Validate Snowflake connection name."""
    if not connection_name or not connection_name.strip():
        return False
    return True

def validate_scale(scale: str) -> bool:
    """Validate data generation scale."""
    return scale in SCALES