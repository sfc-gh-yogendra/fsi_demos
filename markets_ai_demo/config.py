# config.py
# Master configuration for the Frost Markets Intelligence Demo

class DemoConfig:
    """Configuration settings for the Frost Markets Intelligence demo"""
    
    # --- Company/Project Information ---
    COMPANY_NAME = "Frost Markets Intelligence"
    PROJECT_NAME = "Snowflake AI Demo"
    
    # --- Data Volume and Scope ---
    NUM_COMPANIES = 15
    NUM_CLIENTS = 25
    
    # --- Helper Functions for SQL Generation ---
    
    @staticmethod
    def safe_sql_tuple(items, default_value="'__NONE__'"):
        """
        Generate SQL-safe tuple from list, handling empty lists.
        
        Args:
            items: List of items to convert to SQL tuple
            default_value: Value to use if list is empty (default: '__NONE__')
            
        Returns:
            String representation of SQL tuple
            
        Examples:
            safe_sql_tuple(['AAPL', 'MSFT']) -> "('AAPL', 'MSFT')"
            safe_sql_tuple(['AAPL']) -> "('AAPL')"
            safe_sql_tuple([]) -> "('__NONE__')"
        """
        if not items:
            return f"({default_value})"
        if len(items) == 1:
            return f"('{items[0]}')"
        return str(tuple(items))
    
    @staticmethod
    def get_demo_company_tickers():
        """Get list of demo company tickers"""
        return DemoConfig.TICKER_LIST
    
    @staticmethod
    def get_demo_company_tickers_sql():
        """Get SQL-safe tuple of demo company tickers"""
        return DemoConfig.safe_sql_tuple(DemoConfig.TICKER_LIST)
    
    @staticmethod
    def get_demo_sectors():
        """Get list of demo sectors"""
        return DemoConfig.SECTOR_LIST
    
    @staticmethod
    def get_demo_sectors_sql():
        """Get SQL-safe tuple of demo sectors"""
        return DemoConfig.safe_sql_tuple(DemoConfig.SECTOR_LIST)
    
    @staticmethod
    def get_thematic_tags():
        """Get list of thematic tags"""
        return DemoConfig.THEMATIC_TAGS
    
    @staticmethod
    def get_thematic_tags_sql():
        """Get SQL-safe tuple of thematic tags"""
        return DemoConfig.safe_sql_tuple(DemoConfig.THEMATIC_TAGS)
    
    # --- Time Series Configuration ---
    # Number of historical quarters to generate (configurable)
    NUM_HISTORICAL_QUARTERS = 8
    # Number of years of data to generate (calculated from quarters, but can be overridden)
    NUM_HISTORICAL_YEARS = 2
    # Generate data dynamically based on current date when setup runs
    
    # --- Company & Market Data Configuration ---
    TICKER_LIST = [
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX",
        "JNJ", "PG", "KO", "XOM", "JPM", "BAC", "WMT"
    ]
    
    SECTOR_LIST = [
        "Technology", "Healthcare", "Financial Services", 
        "Consumer Discretionary", "Energy", "Consumer Staples"
    ]
    
    # --- Thematic & Risk Configuration ---
    THEMATIC_TAGS = [
        "Carbon Capture", "Direct Air Capture", "AI/ML", "Cloud Computing",
        "Electric Vehicles", "Renewable Energy", "Biotechnology",
        "Supply Chain Disruption", "Geopolitical Risk"
    ]
    
    RISK_EVENT_TYPES = [
        "Regulatory Change", "Natural Disaster", "Geopolitical Event",
        "Technology Breakthrough", "Market Disruption", "Credit Event",
        "Supply Chain Issue", "Cyber Security", "Climate Event"
    ]
    
    # --- Event Configuration ---
    NUM_MAJOR_EVENTS = 8
    
    # --- Client Configuration ---
    CLIENT_TYPES = [
        "Asset Manager", "Hedge Fund", "Pension Fund", 
        "Corporate Treasurer", "Insurance Company", "Sovereign Wealth Fund"
    ]
    
    # --- Snowflake AI Configuration ---
    CORTEX_MODEL_NAME = "llama3.1-70b"
    AGENT_ORCHESTRATION_MODEL = "claude-sonnet-4-5"
    AGENT_SCHEMA = "SNOWFLAKE_INTELLIGENCE.AGENTS"
    
    # --- Snowflake Connection Configuration ---
    # This value can be overridden by command-line argument
    SNOWFLAKE_CONNECTION_NAME = "sfseeurope-mstellwall-aws-us-west3"
    
    # --- Database Configuration ---
    # Nested dictionary structure for better organization
    DATABASE = {
        "name": "MARKETS_AI_DEMO",
        "comment": f"{COMPANY_NAME} - {PROJECT_NAME} Database"
    }
    
    # Legacy support
    DATABASE_NAME = "MARKETS_AI_DEMO"
    
    # Schema configuration - Industry standard naming
    SCHEMAS = {
        "RAW": "RAW",
        "CURATED": "CURATED", 
        "AI": "AI"
    }
    
    # Legacy aliases for backward compatibility during transition
    RAW_DATA = "RAW"
    ENRICHED_DATA = "CURATED"
    ANALYTICS = "AI"
    
    # --- Warehouse Configuration ---
    # Nested dictionary structure for better organization
    WAREHOUSES = {
        "compute": {
            "name": "MARKETS_AI_DEMO_COMPUTE_WH",
            "size": "MEDIUM",
            "comment": f"{COMPANY_NAME} - Compute warehouse for data generation and processing"
        },
        "search": {
            "name": "MARKETS_AI_DEMO_SEARCH_WH",
            "size": "SMALL",
            "comment": f"{COMPANY_NAME} - Search warehouse for Cortex Search services"
        }
    }
    
    # Legacy support
    COMPUTE_WAREHOUSE = "MARKETS_AI_DEMO_COMPUTE_WH"
    SEARCH_WAREHOUSE = "MARKETS_AI_DEMO_SEARCH_WH"
    
    # --- Demo Scenario Configuration ---
    SCENARIOS = [
        "equity_research_earnings",
        "equity_research_thematic",
        "global_macro_strategy",
        "global_research_reports",
        "global_research_client_strategy"
    ]
    
    # Legacy support for backward compatibility
    PHASE_1_SCENARIOS = ["equity_research_earnings", "equity_research_thematic"]
    PHASE_2_SCENARIOS = ["global_research_reports", "global_research_client_strategy", "global_macro_strategy"]
