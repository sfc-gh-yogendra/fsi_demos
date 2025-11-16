# src/data_generation/event_log.py
# Master event log generation for Frost Markets Intelligence Demo

import random
from datetime import datetime, timedelta
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
import sys
import os

# Add the src directory to the path for relative imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import DemoConfig
from utils.date_utils import get_dynamic_date_range


def generate_master_event_log(session: Session) -> None:
    """
    Generate the master event log that drives all data correlations.
    This ensures realistic relationships between prices, news, and filings.
    """
    
    # Create the master event log table in RAW schema
    create_table_sql = """
    CREATE OR REPLACE TABLE RAW.MASTER_EVENT_LOG (
        EVENT_ID STRING,
        EVENT_DATE DATE,
        AFFECTED_TICKER VARCHAR(10),
        EVENT_TYPE VARCHAR(50),
        EVENT_DESCRIPTION VARCHAR(1000),
        EXPECTED_SENTIMENT FLOAT,  -- -1.0 (very negative) to 1.0 (very positive)
        EXPECTED_PRICE_IMPACT FLOAT  -- e.g., 0.05 for a 5% positive impact
    )
    """
    session.sql(create_table_sql).collect()
    print("   📊 Created MASTER_EVENT_LOG table")
    
    # Generate major market events
    events = []
    event_templates = _get_event_templates()
    
    # Generate events spread across the dynamic date range
    # Use middle 80% of date range to avoid edge effects in LAG/LEAD calculations
    start_date, end_date = get_dynamic_date_range()
    date_range_days = (end_date - start_date).days
    safe_start = start_date + timedelta(days=int(date_range_days * 0.1))  # Skip first 10%
    safe_end = end_date - timedelta(days=int(date_range_days * 0.1))      # Skip last 10%
    safe_days = (safe_end - safe_start).days
    
    # First, create specific high-impact events for key demo scenarios
    specific_events = _create_demo_scenario_events(safe_start, safe_end)
    events.extend(specific_events)
    event_id_counter = len(specific_events)
    
    # Then fill remaining slots with random events
    remaining_events = DemoConfig.NUM_MAJOR_EVENTS - len(specific_events)
    for i in range(remaining_events):
        # Pick random date within safe range and ticker
        random_days = random.randint(0, safe_days)
        event_date = safe_start + timedelta(days=random_days)
        ticker = random.choice(DemoConfig.TICKER_LIST)
        
        # Select event template based on ticker/sector
        template = _select_event_template(ticker, event_templates)
        
        event = {
            "EVENT_ID": f"EVT_{event_id_counter + i + 1:03d}",
            "EVENT_DATE": event_date.strftime("%Y-%m-%d"),
            "AFFECTED_TICKER": ticker,
            "EVENT_TYPE": template["type"],
            "EVENT_DESCRIPTION": template["description"].format(ticker=ticker),
            "EXPECTED_SENTIMENT": template["sentiment"],
            "EXPECTED_PRICE_IMPACT": template["price_impact"]
        }
        events.append(event)
    
    # Create DataFrame and save to Snowflake
    events_df = session.create_dataframe(events)
    events_df.write.mode("overwrite").save_as_table("RAW.MASTER_EVENT_LOG")
    
    print(f"   ✅ Generated {len(events)} major market events")
    
    # Display sample events
    sample_events = session.table(f"{DemoConfig.SCHEMAS['RAW']}.MASTER_EVENT_LOG").limit(3).collect()
    print("   📋 Sample events:")
    for event in sample_events:
        print(f"      {event['EVENT_DATE']} - {event['AFFECTED_TICKER']}: {event['EVENT_DESCRIPTION'][:60]}...")


def _get_event_templates():
    """Define event templates for different scenarios"""
    return [
        {
            "type": "Technology Breakthrough",
            "description": "{ticker} announces breakthrough in quantum computing, potential to revolutionize data processing",
            "sentiment": 0.8,
            "price_impact": 0.12,
            "applicable_tickers": ["GOOGL", "IBM", "MSFT", "NVDA"]
        },
        {
            "type": "Regulatory Approval", 
            "description": "{ticker} receives FDA approval for groundbreaking GLP-1 drug for obesity treatment",
            "sentiment": 0.9,
            "price_impact": 0.15,
            "applicable_tickers": ["JNJ", "PFE", "ABBV"]
        },
        {
            "type": "Supply Chain Disruption",
            "description": "{ticker} faces production delays due to semiconductor shortage affecting Q4 guidance",
            "sentiment": -0.6,
            "price_impact": -0.08,
            "applicable_tickers": ["AAPL", "TSLA", "F", "GM"]
        },
        {
            "type": "Climate Initiative",
            "description": "{ticker} unveils $2B investment in direct air capture technology partnership",
            "sentiment": 0.7,
            "price_impact": 0.06,
            "applicable_tickers": ["XOM", "CVX", "MSFT", "GOOGL"]
        },
        {
            "type": "Cyber Security Incident",
            "description": "{ticker} reports data breach affecting customer payment information, immediate remediation underway",
            "sentiment": -0.8,
            "price_impact": -0.12,
            "applicable_tickers": ["META", "AMZN", "NFLX", "PYPL"]
        },
        {
            "type": "Market Expansion",
            "description": "{ticker} announces major expansion into Southeast Asian markets with $500M investment",
            "sentiment": 0.6,
            "price_impact": 0.08,
            "applicable_tickers": ["KO", "PG", "MCD", "SBUX"]
        },
        {
            "type": "Natural Disaster Impact",
            "description": "Major earthquake in Taiwan affects {ticker} manufacturing facilities, production halt expected",
            "sentiment": -0.7,
            "price_impact": -0.10,
            "applicable_tickers": ["AAPL", "NVDA", "AMD", "TSM"]
        },
        {
            "type": "Acquisition Announcement",
            "description": "{ticker} announces $3B acquisition of leading AI startup to accelerate automation capabilities",
            "sentiment": 0.5,
            "price_impact": 0.04,
            "applicable_tickers": ["MSFT", "GOOGL", "AMZN", "META"]
        },
        {
            "type": "Energy Transition",
            "description": "{ticker} commits to carbon neutrality by 2030, massive renewable energy investment announced",
            "sentiment": 0.6,
            "price_impact": 0.07,
            "applicable_tickers": ["XOM", "CVX", "BP", "TOT"]
        },
        {
            "type": "Earnings Surprise",
            "description": "{ticker} reports record quarterly results driven by strong demand for cloud services",
            "sentiment": 0.8,
            "price_impact": 0.10,
            "applicable_tickers": ["MSFT", "AMZN", "GOOGL", "CRM"]
        },
        {
            "type": "Carbon Capture Contract Win",
            "description": "{ticker} secures $500M contract for carbon capture technology deployment at major industrial facility",
            "sentiment": 0.75,
            "price_impact": 0.09,
            "applicable_tickers": ["LIN", "SIEGY", "JMPLY"]
        },
        {
            "type": "Carbon Capture Technology Milestone",
            "description": "{ticker} achieves breakthrough in carbon capture efficiency, reducing costs by 25%",
            "sentiment": 0.8,
            "price_impact": 0.11,
            "applicable_tickers": ["LIN", "JMPLY"]
        },
        {
            "type": "Industrial Partnership Announcement",
            "description": "{ticker} forms strategic partnership with leading energy company for carbon capture infrastructure",
            "sentiment": 0.65,
            "price_impact": 0.07,
            "applicable_tickers": ["LIN", "SIEGY", "JMPLY"]
        },
        {
            "type": "Catalyst Technology Setback",
            "description": "{ticker} delays carbon capture catalyst product launch citing technical challenges and increased competition",
            "sentiment": -0.6,
            "price_impact": -0.08,
            "applicable_tickers": ["JMPLY"]
        }
    ]


def _create_demo_scenario_events(safe_start, safe_end):
    """
    Create specific high-impact events for demo scenarios.
    These ensure demo queries have clear, correlated data to work with.
    """
    date_range_days = (safe_end - safe_start).days
    
    # Calculate event dates distributed across the date range
    # Place Taiwan earthquake in the most recent 25% of the date range
    taiwan_earthquake_date = safe_end - timedelta(days=int(date_range_days * 0.15))
    
    # Other events spread throughout
    ai_breakthrough_date = safe_start + timedelta(days=int(date_range_days * 0.3))
    carbon_capture_date = safe_start + timedelta(days=int(date_range_days * 0.5))
    
    specific_events = [
        # Taiwan Earthquake (Scenario 5 - Market Risk Analyst)
        # This affects semiconductor companies globally
        {
            "EVENT_ID": "EVT_TAIWAN_EQ_001",
            "EVENT_DATE": taiwan_earthquake_date.strftime("%Y-%m-%d"),
            "AFFECTED_TICKER": "NVDA",
            "EVENT_TYPE": "Natural Disaster Impact",
            "EVENT_DESCRIPTION": "7.0 magnitude earthquake hits Taiwan, NVDA supply chain severely impacted with TSMC fab damage",
            "EXPECTED_SENTIMENT": -0.8,
            "EXPECTED_PRICE_IMPACT": -0.12
        },
        {
            "EVENT_ID": "EVT_TAIWAN_EQ_002",
            "EVENT_DATE": taiwan_earthquake_date.strftime("%Y-%m-%d"),
            "AFFECTED_TICKER": "AMD",
            "EVENT_TYPE": "Natural Disaster Impact",
            "EVENT_DESCRIPTION": "7.0 magnitude earthquake hits Taiwan, AMD semiconductor supply chain disrupted",
            "EXPECTED_SENTIMENT": -0.75,
            "EXPECTED_PRICE_IMPACT": -0.10
        },
        {
            "EVENT_ID": "EVT_TAIWAN_EQ_003",
            "EVENT_DATE": taiwan_earthquake_date.strftime("%Y-%m-%d"),
            "AFFECTED_TICKER": "AAPL",
            "EVENT_TYPE": "Natural Disaster Impact",
            "EVENT_DESCRIPTION": "7.0 magnitude earthquake hits Taiwan, AAPL chip suppliers affected, iPhone production at risk",
            "EXPECTED_SENTIMENT": -0.7,
            "EXPECTED_PRICE_IMPACT": -0.08
        },
        # AI Breakthrough (Scenario 2 - Thematic Research)
        {
            "EVENT_ID": "EVT_AI_BREAK_001",
            "EVENT_DATE": ai_breakthrough_date.strftime("%Y-%m-%d"),
            "AFFECTED_TICKER": "NVDA",
            "EVENT_TYPE": "Technology Breakthrough",
            "EVENT_DESCRIPTION": "NVDA unveils revolutionary AI chip architecture, 10x performance improvement for LLM training",
            "EXPECTED_SENTIMENT": 0.9,
            "EXPECTED_PRICE_IMPACT": 0.15
        },
        # Carbon Capture (Scenario 2 - Thematic Research)
        {
            "EVENT_ID": "EVT_CARBON_001",
            "EVENT_DATE": carbon_capture_date.strftime("%Y-%m-%d"),
            "AFFECTED_TICKER": "LIN",
            "EVENT_TYPE": "Carbon Capture Contract Win",
            "EVENT_DESCRIPTION": "LIN secures $800M contract for carbon capture technology deployment across 15 industrial sites",
            "EXPECTED_SENTIMENT": 0.8,
            "EXPECTED_PRICE_IMPACT": 0.12
        }
    ]
    
    return specific_events


def _select_event_template(ticker, templates):
    """Select appropriate event template for the given ticker"""
    
    # Find templates applicable to this ticker
    applicable_templates = [
        template for template in templates 
        if ticker in template.get("applicable_tickers", DemoConfig.TICKER_LIST)
    ]
    
    # If no specific templates, use any template
    if not applicable_templates:
        applicable_templates = templates
    
    template = random.choice(applicable_templates)
    
    # Add some randomness to sentiment and price impact
    sentiment_variation = random.uniform(-0.1, 0.1)
    price_variation = random.uniform(0.8, 1.2)
    
    return {
        "type": template["type"],
        "description": template["description"],
        "sentiment": max(-1.0, min(1.0, template["sentiment"] + sentiment_variation)),
        "price_impact": template["price_impact"] * price_variation
    }
