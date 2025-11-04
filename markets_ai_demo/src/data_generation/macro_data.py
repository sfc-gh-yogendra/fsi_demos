# src/data_generation/macro_data.py
# Macroeconomic signals data generation for Global Macro Strategy scenario

import random
import sys
import os
from datetime import datetime, timedelta
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

# Add the src directory to the path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DemoConfig
from utils.date_utils import get_dynamic_date_range


def generate_macro_signals(session: Session) -> None:
    """Generate proprietary macroeconomic signals data"""
    
    print("   🌍 Generating macroeconomic signals data...")
    
    # Create PROPRIETARY_SIGNALS table
    create_table_sql = """
    CREATE OR REPLACE TABLE RAW.PROPRIETARY_SIGNALS (
        SIGNAL_DATE DATE,
        SIGNAL_NAME VARCHAR(100),
        SIGNAL_VALUE FLOAT,
        SIGNAL_CATEGORY VARCHAR(50),
        SIGNAL_REGION VARCHAR(50),
        SIGNAL_DESCRIPTION VARCHAR(500)
    )
    """
    session.sql(create_table_sql).collect()
    
    # Define proprietary signals
    signals_config = [
        {
            "name": "Frost Global Shipping Volume Index",
            "category": "Trade Activity",
            "region": "Global",
            "description": "Proprietary index tracking global container shipping volumes as a leading indicator of economic activity",
            "base_value": 100.0,
            "volatility": 0.02,
            "trend": 0.001  # Slight upward trend
        },
        {
            "name": "Frost Central Bank Liquidity Indicator",
            "category": "Monetary Policy",
            "region": "Global",
            "description": "Composite indicator measuring global central bank balance sheet changes and policy stance",
            "base_value": 75.0,
            "volatility": 0.015,
            "trend": -0.002  # Slight downward trend (tightening)
        },
        {
            "name": "Frost Manufacturing PMI Composite",
            "category": "Economic Activity",
            "region": "Global",
            "description": "Proprietary composite of manufacturing PMI data across major economies",
            "base_value": 52.0,
            "volatility": 0.01,
            "trend": 0.0005
        },
        {
            "name": "Frost Consumer Sentiment Index",
            "category": "Consumer Behavior",
            "region": "US",
            "description": "Real-time consumer sentiment tracking based on alternative data sources",
            "base_value": 65.0,
            "volatility": 0.02,
            "trend": 0.001
        },
        {
            "name": "Frost Credit Conditions Indicator",
            "category": "Financial Conditions",
            "region": "Global",
            "description": "Composite measure of global credit market conditions and lending standards",
            "base_value": 50.0,
            "volatility": 0.018,
            "trend": -0.001  # Slight tightening
        },
        {
            "name": "Frost Commodity Price Momentum",
            "category": "Commodities",
            "region": "Global",
            "description": "Momentum indicator for broad commodity price movements",
            "base_value": 110.0,
            "volatility": 0.03,
            "trend": 0.002
        },
        {
            "name": "Frost Emerging Markets Capital Flow",
            "category": "Capital Flows",
            "region": "Emerging Markets",
            "description": "Real-time tracking of capital flows into and out of emerging market assets",
            "base_value": 80.0,
            "volatility": 0.025,
            "trend": 0.0
        },
        {
            "name": "Frost Technology Capex Tracker",
            "category": "Investment",
            "region": "Global",
            "description": "Leading indicator of technology sector capital expenditure trends",
            "base_value": 95.0,
            "volatility": 0.022,
            "trend": 0.003  # Strong upward trend
        }
    ]
    
    # Get events for signal impact
    events_df = session.table("MASTER_EVENT_LOG").collect()
    
    # Generate time series data for each signal
    signals_data = []
    start_date, end_date = get_dynamic_date_range()
    
    for signal_config in signals_config:
        print(f"     📊 Generating {signal_config['name']}...")
        
        current_value = signal_config['base_value']
        current_date = start_date
        
        while current_date <= end_date:
            # Check for relevant events that might impact this signal
            event_impact = 0.0
            for event in events_df:
                if event['EVENT_DATE'] == current_date.date():
                    event_type = event['EVENT_TYPE']
                    
                    # Different signals react to different event types
                    if signal_config['category'] == "Trade Activity" and event_type in ["Supply Chain Issue", "Geopolitical Event"]:
                        event_impact = random.uniform(-0.05, -0.02)  # Negative impact
                    elif signal_config['category'] == "Monetary Policy" and event_type in ["Regulatory Change", "Credit Event"]:
                        event_impact = random.uniform(-0.03, 0.03)
                    elif signal_config['category'] == "Economic Activity" and event_type in ["Natural Disaster", "Market Disruption"]:
                        event_impact = random.uniform(-0.04, -0.01)
                    elif signal_config['category'] == "Investment" and event_type in ["Technology Breakthrough"]:
                        event_impact = random.uniform(0.02, 0.05)  # Positive impact
            
            # Generate daily movement with trend + volatility + events
            daily_change = (
                signal_config['trend'] +  # Long-term trend
                random.normalvariate(0, signal_config['volatility']) +  # Random volatility
                event_impact  # Event-driven shocks
            )
            
            current_value *= (1 + daily_change)
            
            # Add weekly data points to reduce volume (every 7 days)
            if (current_date - start_date).days % 7 == 0:
                signals_data.append({
                    "SIGNAL_DATE": current_date.strftime("%Y-%m-%d"),
                    "SIGNAL_NAME": signal_config['name'],
                    "SIGNAL_VALUE": round(current_value, 2),
                    "SIGNAL_CATEGORY": signal_config['category'],
                    "SIGNAL_REGION": signal_config['region'],
                    "SIGNAL_DESCRIPTION": signal_config['description']
                })
            
            current_date += timedelta(days=1)
    
    # Save to Snowflake
    if signals_data:
        signals_df = session.create_dataframe(signals_data)
        signals_df.write.mode("overwrite").save_as_table("RAW.PROPRIETARY_SIGNALS")
        print(f"   ✅ Generated {len(signals_data)} signal data points")
    else:
        print("   ⚠️  No signal data generated")


def generate_economic_regions(session: Session) -> None:
    """Generate economic regions reference data for dimensional analysis"""
    
    print("   🗺️  Generating economic regions data...")
    
    create_table_sql = """
    CREATE OR REPLACE TABLE RAW.ECONOMIC_REGIONS (
        REGION_CODE VARCHAR(10) PRIMARY KEY,
        REGION_NAME VARCHAR(100),
        REGION_TYPE VARCHAR(50),
        GDP_TRILLIONS FLOAT,
        POPULATION_MILLIONS FLOAT
    )
    """
    session.sql(create_table_sql).collect()
    
    regions_data = [
        {"REGION_CODE": "US", "REGION_NAME": "United States", "REGION_TYPE": "Developed", "GDP_TRILLIONS": 27.0, "POPULATION_MILLIONS": 335},
        {"REGION_CODE": "EU", "REGION_NAME": "European Union", "REGION_TYPE": "Developed", "GDP_TRILLIONS": 17.0, "POPULATION_MILLIONS": 450},
        {"REGION_CODE": "CN", "REGION_NAME": "China", "REGION_TYPE": "Emerging", "GDP_TRILLIONS": 18.0, "POPULATION_MILLIONS": 1400},
        {"REGION_CODE": "JP", "REGION_NAME": "Japan", "REGION_TYPE": "Developed", "GDP_TRILLIONS": 4.2, "POPULATION_MILLIONS": 125},
        {"REGION_CODE": "UK", "REGION_NAME": "United Kingdom", "REGION_TYPE": "Developed", "GDP_TRILLIONS": 3.5, "POPULATION_MILLIONS": 68},
        {"REGION_CODE": "IN", "REGION_NAME": "India", "REGION_TYPE": "Emerging", "GDP_TRILLIONS": 3.7, "POPULATION_MILLIONS": 1420},
        {"REGION_CODE": "BR", "REGION_NAME": "Brazil", "REGION_TYPE": "Emerging", "GDP_TRILLIONS": 2.1, "POPULATION_MILLIONS": 215},
        {"REGION_CODE": "EMEA", "REGION_NAME": "EMEA Region", "REGION_TYPE": "Mixed", "GDP_TRILLIONS": 25.0, "POPULATION_MILLIONS": 2000},
        {"REGION_CODE": "APAC", "REGION_NAME": "Asia Pacific", "REGION_TYPE": "Mixed", "GDP_TRILLIONS": 35.0, "POPULATION_MILLIONS": 4500},
        {"REGION_CODE": "GLOBAL", "REGION_NAME": "Global", "REGION_TYPE": "Aggregate", "GDP_TRILLIONS": 105.0, "POPULATION_MILLIONS": 8000}
    ]
    
    regions_df = session.create_dataframe(regions_data)
    regions_df.write.mode("overwrite").save_as_table("RAW.ECONOMIC_REGIONS")
    print(f"   ✅ Generated {len(regions_data)} economic regions")


def generate_sector_correlations(session: Session) -> None:
    """Generate sector correlation data with macro signals"""
    
    print("   📈 Generating sector-macro correlations...")
    
    create_table_sql = """
    CREATE OR REPLACE TABLE RAW.SECTOR_MACRO_CORRELATIONS (
        SECTOR VARCHAR(100),
        SIGNAL_NAME VARCHAR(100),
        CORRELATION_COEFFICIENT FLOAT,
        INTERPRETATION VARCHAR(500)
    )
    """
    session.sql(create_table_sql).collect()
    
    correlations_data = [
        # Technology sector correlations
        {"SECTOR": "Technology", "SIGNAL_NAME": "Frost Technology Capex Tracker", "CORRELATION_COEFFICIENT": 0.85, 
         "INTERPRETATION": "Strong positive correlation - technology stocks benefit from increased capex spending"},
        {"SECTOR": "Technology", "SIGNAL_NAME": "Frost Central Bank Liquidity Indicator", "CORRELATION_COEFFICIENT": 0.72,
         "INTERPRETATION": "Positive correlation - tech valuations sensitive to liquidity conditions"},
        {"SECTOR": "Technology", "SIGNAL_NAME": "Frost Consumer Sentiment Index", "CORRELATION_COEFFICIENT": 0.65,
         "INTERPRETATION": "Moderate positive correlation - consumer tech demand tied to sentiment"},
        
        # Energy sector correlations
        {"SECTOR": "Energy", "SIGNAL_NAME": "Frost Commodity Price Momentum", "CORRELATION_COEFFICIENT": 0.91,
         "INTERPRETATION": "Very strong positive correlation - energy stocks move with commodity prices"},
        {"SECTOR": "Energy", "SIGNAL_NAME": "Frost Global Shipping Volume Index", "CORRELATION_COEFFICIENT": 0.78,
         "INTERPRETATION": "Strong positive correlation - shipping volumes indicate energy demand"},
        {"SECTOR": "Energy", "SIGNAL_NAME": "Frost Manufacturing PMI Composite", "CORRELATION_COEFFICIENT": 0.69,
         "INTERPRETATION": "Positive correlation - manufacturing activity drives energy consumption"},
        
        # Financial Services correlations
        {"SECTOR": "Financial Services", "SIGNAL_NAME": "Frost Credit Conditions Indicator", "CORRELATION_COEFFICIENT": 0.88,
         "INTERPRETATION": "Strong positive correlation - financials benefit from healthy credit conditions"},
        {"SECTOR": "Financial Services", "SIGNAL_NAME": "Frost Central Bank Liquidity Indicator", "CORRELATION_COEFFICIENT": -0.45,
         "INTERPRETATION": "Negative correlation - tightening liquidity can compress margins"},
        {"SECTOR": "Financial Services", "SIGNAL_NAME": "Frost Emerging Markets Capital Flow", "CORRELATION_COEFFICIENT": 0.71,
         "INTERPRETATION": "Positive correlation - capital flows drive trading and investment banking revenues"},
        
        # Consumer Discretionary correlations
        {"SECTOR": "Consumer Discretionary", "SIGNAL_NAME": "Frost Consumer Sentiment Index", "CORRELATION_COEFFICIENT": 0.89,
         "INTERPRETATION": "Very strong positive correlation - discretionary spending follows consumer confidence"},
        {"SECTOR": "Consumer Discretionary", "SIGNAL_NAME": "Frost Credit Conditions Indicator", "CORRELATION_COEFFICIENT": 0.76,
         "INTERPRETATION": "Strong positive correlation - consumer access to credit enables purchases"},
        
        # Healthcare correlations
        {"SECTOR": "Healthcare", "SIGNAL_NAME": "Frost Consumer Sentiment Index", "CORRELATION_COEFFICIENT": 0.35,
         "INTERPRETATION": "Low positive correlation - healthcare demand is relatively stable"},
        {"SECTOR": "Healthcare", "SIGNAL_NAME": "Frost Technology Capex Tracker", "CORRELATION_COEFFICIENT": 0.62,
         "INTERPRETATION": "Moderate positive correlation - healthcare tech innovation driven by capex"},
        
        # Consumer Staples correlations
        {"SECTOR": "Consumer Staples", "SIGNAL_NAME": "Frost Consumer Sentiment Index", "CORRELATION_COEFFICIENT": 0.28,
         "INTERPRETATION": "Low positive correlation - staples demand is defensive and stable"},
        {"SECTOR": "Consumer Staples", "SIGNAL_NAME": "Frost Commodity Price Momentum", "CORRELATION_COEFFICIENT": -0.41,
         "INTERPRETATION": "Negative correlation - rising commodity costs pressure margins"}
    ]
    
    correlations_df = session.create_dataframe(correlations_data)
    correlations_df.write.mode("overwrite").save_as_table("RAW.SECTOR_MACRO_CORRELATIONS")
    print(f"   ✅ Generated {len(correlations_data)} correlation mappings")


def generate_all_macro_data(session: Session) -> None:
    """Generate all macroeconomic data for the Global Macro Strategy scenario"""
    
    print("\n🌍 Generating Macroeconomic Data...")
    print("="*60)
    
    generate_macro_signals(session)
    generate_economic_regions(session)
    generate_sector_correlations(session)
    
    print("="*60)
    print("✅ All macroeconomic data generated successfully")

