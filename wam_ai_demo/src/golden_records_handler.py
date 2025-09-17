"""
Golden Records Handler
Manages controlled data generation for demo consistency
"""

import config
import pandas as pd
from pathlib import Path
from snowflake.snowpark import Session
import random


def is_golden_client_record(client_data: dict) -> bool:
    """Check if this client should use golden record generation"""
    return config.is_golden_client(client_data.get('FIRSTNAME', ''), client_data.get('LASTNAME', ''))


def apply_golden_client_overrides(client_data: dict) -> dict:
    """Apply golden record overrides to client data"""
    client_name = f"{client_data.get('FIRSTNAME', '')} {client_data.get('LASTNAME', '')}"
    golden_config = config.get_golden_client_config(client_name)
    
    if golden_config:
        # Override with golden record values that exist in DIM_CLIENT schema
        client_data.update({
            'RISKTOLERANCE': golden_config['risk_tolerance'],
            'INVESTMENTHORIZON': golden_config['investment_horizon']
            # Note: target_aum and portfolio_strategy are used in portfolio generation
            # but are not stored as client attributes in DIM_CLIENT table
        })
    
    return client_data


def generate_golden_portfolio_positions(session: Session, client_id: int, portfolio_id: int):
    """Generate controlled portfolio positions for golden clients"""
    try:
        client_name = get_client_name_by_id(session, client_id)
        golden_config = config.get_golden_client_config(client_name)
        
        if not golden_config:
            return False  # Not a golden client, use normal generation
        
        # Get security IDs for golden allocations
        allocations = golden_config['portfolio_allocations']
        target_value = golden_config['target_aum']
        
        positions_data = []
        for ticker, allocation in allocations.items():
            security_id = get_security_id_by_ticker(session, ticker)
            if security_id:
                market_value = target_value * allocation
                
                # Use realistic pricing based on ticker
                if ticker == 'V':
                    price_per_share = 239.23  # Realistic Visa price
                elif ticker == 'JPM':
                    price_per_share = 175.42  # Realistic JPM price
                else:
                    price_per_share = 100.00  # Default fallback
                
                shares = market_value / price_per_share
                
                positions_data.append({
                    'HOLDINGDATE': config.get_history_end_date(),
                    'PORTFOLIOID': portfolio_id,
                    'SECURITYID': security_id,
                    'QUANTITY': shares,
                    'MARKETVALUE_LOCAL': market_value,
                    'MARKETVALUE_BASE': market_value,
                    'COSTBASIS_LOCAL': market_value * 0.95,  # Assume some gain
                    'COSTBASIS_BASE': market_value * 0.95,
                    'ACCRUEDINTEREST_LOCAL': 0,
                    'PORTFOLIOWEIGHT': allocation
                })
        
        # Insert golden positions using SQL to avoid pandas issues
        if positions_data:
            for position in positions_data:
                session.sql(f"""
                    INSERT INTO {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR 
                    (HoldingDate, PortfolioID, SecurityID, Quantity, MarketValue_Local, MarketValue_Base, 
                     CostBasis_Local, CostBasis_Base, AccruedInterest_Local, PortfolioWeight)
                    VALUES (
                        '{position['HOLDINGDATE']}',
                        {position['PORTFOLIOID']},
                        {position['SECURITYID']},
                        {position['QUANTITY']},
                        {position['MARKETVALUE_LOCAL']},
                        {position['MARKETVALUE_BASE']},
                        {position['COSTBASIS_LOCAL']},
                        {position['COSTBASIS_BASE']},
                        {position['ACCRUEDINTEREST_LOCAL']},
                        {position['PORTFOLIOWEIGHT']}
                    )
                """).collect()
            
            return True
    
    except Exception as e:
        print(f"Warning: Could not generate golden portfolio positions for client {client_id}: {e}")
    
    return False


def load_golden_document(category: str, document_name: str, client_name: str = None) -> str:
    """Load pre-generated golden document content"""
    file_path = config.get_golden_document_path(category, client_name, document_name)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Golden document not found: {file_path}")
        return None


def insert_golden_planning_documents(session: Session):
    """Insert pre-generated planning documents for golden clients"""
    for client_key, client_config in config.GOLDEN_CLIENTS.items():
        client_name = f"{client_config['first_name']} {client_config['last_name']}"
        client_id = get_client_id_by_name(session, client_config['first_name'], client_config['last_name'])
        
        if not client_id:
            print(f"Warning: Golden client {client_name} not found in database")
            continue
        
        # Get list of documents for this client
        client_documents = config.GOLDEN_DOCUMENTS['planning_documents'].get(client_key, [])
        
        for doc_filename in client_documents:
            content = load_golden_document('planning', doc_filename, client_key)
            if content:
                # Determine document type from filename
                doc_type = get_document_type_from_filename(doc_filename)
                
                # Insert document
                insert_planning_document(session, client_id, doc_type, content, client_name)


def insert_golden_research_documents(session: Session):
    """Insert pre-generated research documents"""
    research_docs = config.GOLDEN_DOCUMENTS['research_documents']
    
    for doc_filename in research_docs:
        content = load_golden_document('research', doc_filename)
        if content:
            # Extract metadata from filename and content
            ticker = extract_ticker_from_research(doc_filename, content)
            doc_type = extract_doc_type_from_research(doc_filename)
            
            insert_research_document(session, ticker, doc_type, content)


def apply_golden_communication_controls(client_id: int, communications_data: list) -> list:
    """Apply golden record controls to communications generation"""
    client_name = get_client_name_by_id(None, client_id)  # Would need session here
    
    # Check if this is Sarah Johnson
    if client_name == "Sarah Johnson":
        # Ensure positive sentiment for most communications
        for comm in communications_data:
            if comm['CLIENT_ID'] == client_id:
                comm['SENTIMENT_SCORE'] = max(comm['SENTIMENT_SCORE'], 0.6)  # Ensure positive
                
                # Add ESG interest mentions to some communications
                if random.random() < 0.3:  # 30% chance
                    comm['CONTENT'] += " Expressed interest in ESG investment opportunities."
                
        # Add specific risk communications from config
        risk_flags = config.GOLDEN_DATA_CONTROLS['risk_communications'].get('sarah_johnson_risk_flags', [])
        for risk_content in risk_flags[:1]:  # Add one risk communication
            communications_data.append({
                'CLIENT_ID': client_id,
                'CONTENT': risk_content,
                'CHANNEL': 'Phone',
                'SENTIMENT_SCORE': 0.2,  # Negative sentiment for risk communication
                'RISKCATEGORY': 'PERFORMANCE_CONCERN',
                'RISKSEVERITY': 'LOW',
                'RISKFLAGS': 1
            })
    
    return communications_data


def get_golden_advisor_performance_config(advisor_name: str) -> dict:
    """Get performance configuration for golden advisor records"""
    advisor_controls = config.GOLDEN_DATA_CONTROLS['advisor_performance']
    
    if advisor_name in advisor_controls['top_quartile_advisors']:
        return {
            'performance_tier': 'top_quartile',
            'aum_growth': random.uniform(0.12, 0.18),  # 12-18% growth
            'client_retention': random.uniform(0.95, 0.98),  # 95-98% retention
            'engagement_score': random.uniform(0.85, 0.95)
        }
    elif advisor_name in advisor_controls['bottom_quartile_advisors']:
        return {
            'performance_tier': 'bottom_quartile', 
            'aum_growth': random.uniform(0.02, 0.06),  # 2-6% growth
            'client_retention': random.uniform(0.75, 0.85),  # 75-85% retention
            'engagement_score': random.uniform(0.45, 0.65)
        }
    else:
        return {
            'performance_tier': 'middle',
            'aum_growth': random.uniform(0.08, 0.12),  # 8-12% growth
            'client_retention': random.uniform(0.88, 0.94),  # 88-94% retention
            'engagement_score': random.uniform(0.70, 0.85)
        }


# Helper functions
def get_client_name_by_id(session: Session, client_id: int) -> str:
    """Get client name by ID"""
    if not session:
        return None
    
    try:
        result = session.sql(f"""
            SELECT FIRSTNAME, LASTNAME 
            FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT 
            WHERE ClientID = {client_id}
        """).collect()
        
        if result:
            return f"{result[0]['FIRSTNAME']} {result[0]['LASTNAME']}"
    except Exception as e:
        print(f"Warning: Could not get client name for ID {client_id}: {e}")
    return None

def get_client_id_by_name(session: Session, first_name: str, last_name: str) -> int:
    """Get client ID by name"""
    try:
        result = session.sql(f"""
            SELECT ClientID 
            FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT 
            WHERE FirstName = '{first_name}' AND LastName = '{last_name}'
        """).collect()
        
        if result:
            return result[0]['CLIENTID']
    except Exception as e:
        print(f"Warning: Could not get client ID for {first_name} {last_name}: {e}")
    return None

def get_security_id_by_ticker(session: Session, ticker: str) -> int:
    """Get security ID by ticker"""
    try:
        result = session.sql(f"""
            SELECT SecurityID 
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY 
            WHERE PrimaryTicker = '{ticker}' AND IsActive = TRUE
        """).collect()
        
        if result:
            return result[0]['SECURITYID']
    except Exception as e:
        print(f"Warning: Could not get security ID for ticker {ticker}: {e}")
    return None

def get_document_type_from_filename(filename: str) -> str:
    """Extract document type from filename"""
    if 'education' in filename:
        return 'Education Funding Plan'
    elif 'ips' in filename or 'policy' in filename:
        return 'Investment Policy Statement'
    elif 'comprehensive' in filename:
        return 'Comprehensive Financial Plan'
    return 'General Planning'

def extract_ticker_from_research(filename: str, content: str) -> str:
    """Extract ticker from research document"""
    # Implementation would parse filename or content for ticker
    pass

def extract_doc_type_from_research(filename: str) -> str:
    """Extract document type from research filename"""
    # Implementation would categorize research document type
    pass

def insert_planning_document(session: Session, client_id: int, doc_type: str, content: str, client_name: str):
    """Insert planning document into database"""
    try:
        # Create unique document ID
        document_id = f"GOLDEN_{client_name.upper().replace(' ', '_')}_{doc_type.upper().replace(' ', '_')}"
        
        # Escape single quotes in content
        escaped_content = content.replace("'", "''")
        
        session.sql(f"""
            INSERT INTO {config.DATABASE_NAME}.CURATED.PLANNING_CORPUS 
            (DOCUMENT_ID, CLIENT_ID, CLIENT_NAME, ADVISOR_ID, ADVISOR_NAME, 
             DOCUMENT_TYPE, TITLE, DOCUMENT_TEXT, LAST_UPDATE)
            VALUES (
                '{document_id}',
                {client_id},
                '{client_name}',
                (SELECT AdvisorID FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT WHERE ClientID = {client_id}),
                (SELECT a.FirstName || ' ' || a.LastName 
                 FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT c 
                 JOIN {config.DATABASE_NAME}.CURATED.DIM_ADVISOR a ON c.AdvisorID = a.AdvisorID 
                 WHERE c.ClientID = {client_id}),
                '{doc_type}',
                '{doc_type} for {client_name}',
                '{escaped_content}',
                CURRENT_DATE()
            )
        """).collect()
        
        print(f"    ✅ Inserted golden planning document: {doc_type} for {client_name}")
    except Exception as e:
        print(f"Warning: Could not insert planning document for {client_name}: {e}")

def insert_research_document(session: Session, ticker: str, doc_type: str, content: str):
    """Insert research document into database"""
    try:
        # Create unique document ID
        document_id = f"GOLDEN_RESEARCH_{ticker}_{doc_type.upper().replace(' ', '_')}"
        
        # Escape single quotes in content
        escaped_content = content.replace("'", "''")
        
        session.sql(f"""
            INSERT INTO {config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS 
            (DOCUMENT_ID, TICKER, DOCUMENT_TYPE, TITLE, DOCUMENT_TEXT, PUBLISH_DATE, SOURCE)
            VALUES (
                '{document_id}',
                '{ticker}',
                '{doc_type}',
                '{doc_type} - {ticker}',
                '{escaped_content}',
                CURRENT_DATE(),
                'Golden Records Research Team'
            )
        """).collect()
        
        print(f"    ✅ Inserted golden research document: {doc_type} for {ticker}")
    except Exception as e:
        print(f"Warning: Could not insert research document for {ticker}: {e}")
