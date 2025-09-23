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
    "search_warehouse": "BANK_AI_DEMO_SEARCH_WH"
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
        "entities": 50,
        "entity_relationships": 100,
        "customers": 25,
        "transactions": 5000,
        "compliance_documents": 100,
        "loan_applications": 5,
        "historical_loans": 150,
        "news_articles": 150,
    },
    "demo": {
        "description": "Balanced demo scale - optimal for agent responses",
        "entities": 500,
        "entity_relationships": 1200,
        "customers": 200,
        "transactions": 50000,
        "compliance_documents": 800,
        "loan_applications": 25,
        "historical_loans": 1500,
        "news_articles": 1200,
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
    }
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