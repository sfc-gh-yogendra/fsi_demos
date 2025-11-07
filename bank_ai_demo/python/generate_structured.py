"""
Glacier First Bank Demo - Structured Data Generator

Generates realistic structured data for Phase 1 scenarios using Snowpark save_as_table.
Includes entities, relationships, customers, transactions, and loan applications.
"""

import uuid
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, FloatType, DateType, TimestampType, DecimalType

import config

logger = logging.getLogger(__name__)


def _get_snowpark_schema(schema_config: dict) -> StructType:
    """Convert config schema definition to Snowpark StructType."""
    type_mapping = {
        'STRING': StringType(),
        'INTEGER': IntegerType(),
        'FLOAT': FloatType(),
        'NUMBER': DecimalType(38, 10),  # Snowflake NUMBER type with precision and scale
        'DATE': DateType(),
        'TIMESTAMP': TimestampType(),
        'TIMESTAMP_NTZ': TimestampType()  # Timestamp without timezone
    }
    
    fields = []
    for col_name, col_type in schema_config['columns'].items():
        snowpark_type = type_mapping.get(col_type, StringType())
        fields.append(StructField(col_name, snowpark_type))
    
    return StructType(fields)


def create_database_structure(session: Session) -> None:
    """Create database, schemas, and initial infrastructure."""
    logger.info("Creating database structure...")
    
    try:
        # Create main database
        session.sql(f"""
            CREATE OR REPLACE DATABASE {config.SNOWFLAKE['database']}
                COMMENT = 'Glacier First Bank AI Intelligence Demo - Phase 1 Foundation'
        """).collect()
        
        logger.info(f"Created database: {config.SNOWFLAKE['database']}")
        
        # Set database context
        session.sql(f"USE DATABASE {config.SNOWFLAKE['database']}").collect()
        
        # Create schemas
        schemas = [
            ('RAW_DATA', 'Raw data tables for entities, transactions, documents'),
            ('CURATED_DATA', 'Curated and processed data for analytics'),
            (config.SNOWFLAKE['ai_schema'], 'Unified AI schema for Cortex Search services, Semantic Views, and Custom Tools')
        ]
        
        for schema_name, comment in schemas:
            session.sql(f"""
                CREATE OR REPLACE SCHEMA {config.SNOWFLAKE['database']}.{schema_name}
                    COMMENT = '{comment}'
            """).collect()
            logger.info(f"Created schema: {schema_name}")
        
        # Set default warehouse context
        session.sql(f"USE WAREHOUSE {config.SNOWFLAKE['compute_warehouse']}").collect()
        
        logger.info("Database structure creation completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to create database structure: {e}")
        raise


@dataclass
class EntityProfile:
    """Data class for entity profiles with realistic business characteristics."""
    entity_id: str
    entity_name: str
    entity_type: str
    country_code: str
    industry_sector: str
    incorporation_date: date
    regulatory_status: str
    esg_rating: str
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    risk_factors: Optional[List[str]] = None


def generate_all_structured_data(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate all structured data for Phase 1 and Phase 2."""
    logger.info("Starting structured data generation...")
    
    # Set random seed for reproducible generation
    random.seed(config.GENERATION_SEED)
    
    # Determine which phases to generate based on scenarios
    phase_2_scenarios = ['corp_relationship_manager', 'wealth_advisor']
    include_phase_2 = scenarios and any(s in phase_2_scenarios for s in scenarios) if scenarios != ["all"] else False
    
    # Phase 1 data generation in dependency order
    generate_entities(session, scale, scenarios)
    generate_entity_relationships(session, scale, scenarios)
    generate_customers(session, scale, scenarios)
    generate_transactions(session, scale, scenarios)
    generate_loan_applications(session, scale, scenarios)
    generate_historical_loans(session, scale, scenarios)
    generate_alerts(session, scale, scenarios)
    generate_alert_disposition_history(session, scale, scenarios)
    generate_external_data_simulation(session, scale, scenarios)
    
    # Phase 2 data generation (if Phase 2 scenarios requested or "all")
    if include_phase_2 or scenarios == ["all"] or not scenarios:
        logger.info("Generating Phase 2 data...")
        generate_model_portfolios(session, scale, scenarios)  # Must be before wealth profiles
        generate_client_crm(session, scale, scenarios)
        generate_client_opportunities(session, scale, scenarios)  # Depends on CRM
        generate_holdings(session, scale, scenarios)  # Must be before wealth profiles
        generate_wealth_client_profiles(session, scale, scenarios)  # Depends on holdings and model portfolios
    
    logger.info("Structured data generation completed successfully")


def generate_entities(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate entities with key demo entities guaranteed."""
    logger.info("Generating entities...")
    
    scale_config = config.get_scale_config(scale)
    key_entities = config.KEY_ENTITIES
    
    entities = []
    
    # Generate key entities first (guaranteed for scenarios)
    for entity_key, entity_spec in key_entities.items():
        entity = EntityProfile(
            entity_id=entity_spec['entity_id'],
            entity_name=entity_spec['name'],
            entity_type='CORPORATE',
            country_code=entity_spec['country'],
            industry_sector=entity_spec['industry'],
            incorporation_date=_generate_incorporation_date(),
            regulatory_status=entity_spec.get('regulatory_status', 'ACTIVE'),
            esg_rating=entity_spec.get('esg_rating', 'B')
        )
        entities.append(entity)
    
    # Generate additional entities to reach scale target
    additional_count = scale_config['entities'] - len(entities)
    entities.extend(_generate_additional_entities(additional_count))
    
    # Convert to DataFrame and save
    entity_data = [_entity_to_dict(entity) for entity in entities]
    entities_df = session.create_dataframe(entity_data)
    entities_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES", mode="overwrite")
    
    logger.info(f"Generated {len(entities)} entities ({len(key_entities)} key entities)")


def generate_entity_relationships(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate entity relationships for cross-domain intelligence."""
    logger.info("Generating entity relationships...")
    
    scale_config = config.get_scale_config(scale)
    
    # Get existing entities
    entities_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES")
    entities = entities_df.collect()
    
    relationships = []
    
    # Create key relationships for demo scenarios
    key_relationships = [
        # Northern Supply Chain as shared vendor
        {
            'primary': 'GTV_SA_001',  # Global Trade Ventures
            'related': 'NSC_UK_001',  # Northern Supply Chain
            'type': 'VENDOR',
            'strength': 'PRIMARY',
            'risk_score': 0.85,
            'shared_director': None,
            'shared_address': False
        },
        {
            'primary': 'INN_DE_001',  # Innovate GmbH
            'related': 'NSC_UK_001',  # Northern Supply Chain
            'type': 'VENDOR',
            'strength': 'SECONDARY',
            'risk_score': 0.45,
            'shared_director': None,
            'shared_address': False
        },
        # Customer relationship
        {
            'primary': 'INN_DE_001',  # Innovate GmbH
            'related': 'GTV_SA_001',  # Global Trade Ventures
            'type': 'CUSTOMER',
            'strength': 'INDIRECT',
            'risk_score': 0.25,
            'shared_director': None,
            'shared_address': False
        }
    ]
    
    # Create shell company network for network analysis scenario
    # Network of 5 import/export businesses with suspicious characteristics
    shell_network_entities = [f'SHELL_NET_{i:03d}' for i in range(1, 6)]
    shared_director_name = 'Anya Sharma'
    shared_address = '42 Mailbox Lane, Virtual Office Complex, Gibraltar'
    
    # Create the shell entities with shared characteristics
    for i, shell_id in enumerate(shell_network_entities):
        shell_entity_name = f'{random.choice(["Baltic", "Nordic", "Alpine", "Adriatic", "Aegean"])} {random.choice(["Trade", "Import", "Export", "Commerce"])} {random.choice(["Ltd", "S.A.", "GmbH"])}'
        
        # These will be picked up when generating entities, but we create relationships here
        # Create circular vendor relationships within the network
        if i < len(shell_network_entities) - 1:
            # Connect to next entity in circular pattern
            relationships.append({
                'relationship_id': str(uuid.uuid4()),
                'primary_entity_id': shell_network_entities[i],
                'related_entity_id': shell_network_entities[i + 1],
                'relationship_type': 'VENDOR',
                'relationship_strength': 'PRIMARY',
                'effective_date': _generate_relationship_date(),
                'end_date': None,
                'risk_impact_score': 0.92,
                'shared_director_name': shared_director_name,
                'shared_address_flag': True,
                'shared_address': shared_address,
                'incorporation_proximity_days': random.randint(1, 45),  # Incorporated within 45 days of each other
                'created_date': datetime.now()
            })
        else:
            # Close the circle - last entity connects back to first
            relationships.append({
                'relationship_id': str(uuid.uuid4()),
                'primary_entity_id': shell_network_entities[i],
                'related_entity_id': shell_network_entities[0],
                'relationship_type': 'VENDOR',
                'relationship_strength': 'PRIMARY',
                'effective_date': _generate_relationship_date(),
                'end_date': None,
                'risk_impact_score': 0.92,
                'shared_director_name': shared_director_name,
                'shared_address_flag': True,
                'shared_address': shared_address,
                'incorporation_proximity_days': random.randint(1, 45),
                'created_date': datetime.now()
            })
    
    for rel in key_relationships:
        relationship = {
            'relationship_id': str(uuid.uuid4()),
            'primary_entity_id': rel['primary'],
            'related_entity_id': rel['related'],
            'relationship_type': rel['type'],
            'relationship_strength': rel['strength'],
            'effective_date': _generate_relationship_date(),
            'end_date': None,
            'risk_impact_score': rel['risk_score'],
            'shared_director_name': rel.get('shared_director'),
            'shared_address_flag': rel.get('shared_address', False),
            'shared_address': None,
            'incorporation_proximity_days': None,
            'created_date': datetime.now()
        }
        relationships.append(relationship)
    
    # Generate additional random relationships
    additional_count = scale_config['entity_relationships'] - len(relationships)
    for i in range(additional_count):
        # Select random entities for relationships
        primary_entity = random.choice(entities)
        related_entity = random.choice(entities)
        
        # Avoid self-relationships
        if primary_entity['ENTITY_ID'] != related_entity['ENTITY_ID']:
            # Small chance of shared director/address for random relationships (10%)
            has_shared_characteristics = random.random() < 0.10
            
            relationship = {
                'relationship_id': str(uuid.uuid4()),
                'primary_entity_id': primary_entity['ENTITY_ID'],
                'related_entity_id': related_entity['ENTITY_ID'],
                'relationship_type': random.choice(['VENDOR', 'CUSTOMER', 'COMPETITOR', 'SUBSIDIARY']),
                'relationship_strength': random.choice(['PRIMARY', 'SECONDARY', 'INDIRECT']),
                'effective_date': _generate_relationship_date(),
                'end_date': None,
                'risk_impact_score': random.uniform(0.1, 0.9),
                'shared_director_name': _generate_director_name() if has_shared_characteristics else None,
                'shared_address_flag': has_shared_characteristics,
                'shared_address': 'Virtual Office, Business Center' if has_shared_characteristics else None,
                'incorporation_proximity_days': random.randint(1, 90) if has_shared_characteristics else None,
                'created_date': datetime.now()
            }
            relationships.append(relationship)
    
    # Save to database
    relationships_df = session.create_dataframe(relationships)
    relationships_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITY_RELATIONSHIPS", mode="overwrite")
    
    logger.info(f"Generated {len(relationships)} entity relationships")


def generate_customers(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate customer profiles linked to entities."""
    logger.info("Generating customers...")
    
    scale_config = config.get_scale_config(scale)
    key_entities = config.KEY_ENTITIES
    
    # Get entities that should be customers
    entities_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES")
    entities = entities_df.filter(col("ENTITY_TYPE") == "CORPORATE").collect()
    
    customers = []
    
    # Create customers for key entities
    key_entity_ids = [spec['entity_id'] for spec in key_entities.values()]
    
    # Counter for medium-risk customers due for review
    medium_risk_due_count = 0
    target_medium_risk_due = 8  # Generate 8 medium-risk customers due for review in next 30 days
    
    for entity in entities[:scale_config['customers']]:
        is_key_entity = entity['ENTITY_ID'] in key_entity_ids
        
        # Set risk characteristics for key entities
        if entity['ENTITY_ID'] == 'GTV_SA_001':  # Global Trade Ventures
            risk_rating = 'HIGH'
            kyc_status = 'REQUIRES_EDD'
            aml_flags = 2
        elif entity['ENTITY_ID'] == 'INN_DE_001':  # Innovate GmbH
            risk_rating = 'MEDIUM'
            kyc_status = 'COMPLETE'
            aml_flags = 0
        else:
            risk_rating = random.choice(['LOW', 'MEDIUM', 'HIGH'])
            kyc_status = random.choice(['COMPLETE', 'PENDING', 'REQUIRES_EDD'])
            aml_flags = random.randint(0, 3) if risk_rating == 'HIGH' else random.randint(0, 1)
        
        # Set review frequency based on risk rating (in months)
        if risk_rating == 'HIGH':
            review_frequency_months = 6
        elif risk_rating == 'MEDIUM':
            review_frequency_months = 12
        else:
            review_frequency_months = 24
        
        last_review_date = _generate_review_date()
        
        # For medium-risk customers, create some due for review soon for periodic review scenario
        if risk_rating == 'MEDIUM' and medium_risk_due_count < target_medium_risk_due:
            # Set next review date within next 30 days
            next_review_date = date.today() + timedelta(days=random.randint(1, 30))
            medium_risk_due_count += 1
        else:
            # Normal review date calculation based on frequency
            next_review_date = last_review_date + timedelta(days=review_frequency_months * 30)
        
        customer = {
            'customer_id': f"CUST_{entity['ENTITY_ID']}",
            'entity_id': entity['ENTITY_ID'],
            'customer_type': 'CORPORATE',
            'onboarding_date': _generate_onboarding_date(),
            'risk_rating': risk_rating,
            'kyc_status': kyc_status,
            'last_review_date': last_review_date,
            'next_review_date': next_review_date,
            'review_frequency_months': review_frequency_months,
            'relationship_manager': _generate_rm_name(),
            'aml_flags': aml_flags,
            'created_date': datetime.now()
        }
        customers.append(customer)
    
    # Save to database
    customers_df = session.create_dataframe(customers)
    customers_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS", mode="overwrite")
    
    logger.info(f"Generated {len(customers)} customers")


def generate_transactions(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate transaction history for customers."""
    logger.info("Generating transactions...")
    
    # Get customers
    customers_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
    customers = customers_df.collect()
    
    transactions = []
    
    # Generate transactions for each customer
    for customer in customers:
        customer_transactions = _generate_customer_transactions(customer)
        transactions.extend(customer_transactions)
    
    # Save to database (in batches for large datasets)
    batch_size = 10000
    for i in range(0, len(transactions), batch_size):
        batch = transactions[i:i + batch_size]
        batch_df = session.create_dataframe(batch)
        mode = "overwrite" if i == 0 else "append"
        batch_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.TRANSACTIONS", mode=mode)
    
    logger.info(f"Generated {len(transactions)} transactions")


def generate_loan_applications(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate loan applications with realistic financial metrics."""
    logger.info("Generating loan applications...")
    
    scale_config = config.get_scale_config(scale)
    
    # Get customers
    customers_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
    customers = customers_df.collect()
    
    applications = []
    
    # Create specific application for Innovate GmbH (key credit scenario)
    innovate_customer = next((c for c in customers if c['ENTITY_ID'] == 'INN_DE_001'), None)
    if innovate_customer:
        app = _create_innovate_loan_application(innovate_customer)
        applications.append(app)
    
    # Generate additional applications
    remaining_customers = [c for c in customers if c['ENTITY_ID'] != 'INN_DE_001']
    additional_count = min(scale_config['loan_applications'] - 1, len(remaining_customers))
    
    for customer in remaining_customers[:additional_count]:
        app = _create_loan_application(customer)
        applications.append(app)
    
    # Save to database
    applications_df = session.create_dataframe(applications)
    applications_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.LOAN_APPLICATIONS", mode="overwrite")
    
    logger.info(f"Generated {len(applications)} loan applications")


def generate_historical_loans(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate historical loan performance data for cohort analysis."""
    logger.info("Generating historical loans...")
    
    scale_config = config.get_scale_config(scale)
    
    loans = []
    
    # Generate loans across different time periods and risk profiles
    for _ in range(scale_config['historical_loans']):
        loan = _create_historical_loan()
        loans.append(loan)
    
    # Save to database
    loans_df = session.create_dataframe(loans)
    loans_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.HISTORICAL_LOANS", mode="overwrite")
    
    logger.info(f"Generated {len(loans)} historical loans")


def generate_alerts(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate transaction monitoring alerts for AML investigation scenarios."""
    logger.info("Generating transaction monitoring alerts...")
    
    scale_config = config.get_scale_config(scale)
    
    # Get customers for alert generation
    customers_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
    customers = customers_df.collect()
    
    if not customers:
        logger.warning("No customers found. Skipping alert generation.")
        return
    
    alerts = []
    
    # Generate key structuring alert for demo scenario (John Smith / GTV)
    gtv_customer = next((c for c in customers if c['ENTITY_ID'] == 'GTV_SA_001'), None)
    if gtv_customer:
        structuring_alert = {
            'alert_id': 'ALERT_STRUCT_001',
            'customer_id': gtv_customer['CUSTOMER_ID'],
            'alert_type': 'Structuring',
            'alert_date': datetime.now() - timedelta(days=1),
            'alert_status': 'OPEN',
            'priority_score': 0.95,
            'assigned_to': 'Maria Santos',
            'resolution_date': None,
            'disposition': None,
            'alert_description': '5 cash deposits of $9,500 each across 5 branches over 2-day period',
            'flagged_transaction_count': 5,
            'total_flagged_amount': 47500.00,
            'created_date': datetime.now()
        }
        alerts.append(structuring_alert)
    
    # Generate additional alerts for other customers
    alert_types = ['Structuring', 'Large Cash', 'Rapid Movement', 'High Risk Country', 'Unusual Pattern']
    alert_statuses = ['OPEN', 'UNDER_INVESTIGATION', 'CLOSED']
    analyst_names = ['Maria Santos', 'John Chen', 'Sarah Mitchell', 'David Kumar', 'Emma Rodriguez']
    
    additional_count = scale_config['alerts'] - len(alerts)
    
    for i in range(additional_count):
        customer = random.choice(customers)
        alert_date = datetime.now() - timedelta(days=random.randint(1, 180))
        alert_status = random.choice(alert_statuses)
        
        # Calculate priority score based on customer risk rating
        if customer['RISK_RATING'] == 'HIGH':
            priority_score = random.uniform(0.7, 0.95)
        elif customer['RISK_RATING'] == 'MEDIUM':
            priority_score = random.uniform(0.4, 0.7)
        else:
            priority_score = random.uniform(0.1, 0.4)
        
        alert = {
            'alert_id': f'ALERT_{str(uuid.uuid4())[:8].upper()}',
            'customer_id': customer['CUSTOMER_ID'],
            'alert_type': random.choice(alert_types),
            'alert_date': alert_date,
            'alert_status': alert_status,
            'priority_score': priority_score,
            'assigned_to': random.choice(analyst_names),
            'resolution_date': alert_date + timedelta(days=random.randint(1, 30)) if alert_status == 'CLOSED' else None,
            'disposition': random.choice(['SAR_FILED', 'FALSE_POSITIVE', 'CLEARED']) if alert_status == 'CLOSED' else None,
            'alert_description': f'{random.choice(alert_types)} pattern detected',
            'flagged_transaction_count': random.randint(1, 10),
            'total_flagged_amount': random.uniform(10000, 500000),
            'created_date': datetime.now()
        }
        alerts.append(alert)
    
    # Save to database
    alerts_df = session.create_dataframe(alerts)
    alerts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ALERTS", mode="overwrite")
    
    logger.info(f"Generated {len(alerts)} transaction monitoring alerts")


def generate_alert_disposition_history(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate historical alert disposition data for ML model training."""
    logger.info("Generating alert disposition history...")
    
    scale_config = config.get_scale_config(scale)
    
    # Get existing alerts
    try:
        alerts_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ALERTS")
        alerts = alerts_df.collect()
    except Exception as e:
        logger.warning(f"No alerts table found. Skipping disposition history generation: {e}")
        return
    
    dispositions = []
    
    # Generate disposition history with 75% false positive rate
    for i in range(scale_config['alert_disposition_history']):
        # Randomly select alert ID pattern
        alert_id = f'HIST_ALERT_{str(uuid.uuid4())[:8].upper()}'
        
        # 75% false positives, 20% cleared, 5% SAR filed
        random_val = random.random()
        if random_val < 0.75:
            final_disposition = 'FALSE_POSITIVE'
            investigation_notes = 'Transaction pattern consistent with normal business activity. No suspicious indicators found.'
        elif random_val < 0.95:
            final_disposition = 'CLEARED'
            investigation_notes = 'Customer provided satisfactory documentation. Activity verified as legitimate.'
        else:
            final_disposition = 'SAR_FILED'
            investigation_notes = 'Suspicious activity identified. SAR filed with FinCEN/relevant authority.'
        
        disposition = {
            'disposition_id': str(uuid.uuid4()),
            'alert_id': alert_id,
            'final_disposition': final_disposition,
            'investigation_notes': investigation_notes,
            'analyst_name': random.choice(['Maria Santos', 'John Chen', 'Sarah Mitchell', 'David Kumar']),
            'investigation_hours': random.uniform(0.5, 8.0),
            'closed_date': datetime.now() - timedelta(days=random.randint(30, 730)),
            'created_date': datetime.now()
        }
        dispositions.append(disposition)
    
    # Save to database
    dispositions_df = session.create_dataframe(dispositions)
    dispositions_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.ALERT_DISPOSITION_HISTORY", 
        mode="overwrite"
    )
    
    logger.info(f"Generated {len(dispositions)} historical alert dispositions (75% false positive rate)")


def generate_external_data_simulation(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate external data provider simulation tables."""
    logger.info("Generating external data provider simulation...")
    
    # Generate S&P Global financials
    _generate_sp_global_financials(session)
    
    logger.info("External data provider simulation completed")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def _generate_customer_transactions(customer: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate transactions for a specific customer."""
    transactions = []
    
    # Add specific €5M deposit for Global Trade Ventures (demo scenario requirement)
    if customer['CUSTOMER_ID'] == 'CUST_GTV_SA_001':
        # Recent €5M deposit that will trigger EDD review
        large_deposit = {
            'TRANSACTION_ID': f'TXN_{customer["CUSTOMER_ID"]}_LARGE_001',
            'CUSTOMER_ID': customer['CUSTOMER_ID'],
            'TRANSACTION_DATE': datetime.now() - timedelta(days=7),  # Recent deposit
            'AMOUNT': 5000000.00,  # €5M
            'CURRENCY': f'{config.CURRENCY}',
            'TRANSACTION_TYPE': 'CREDIT',
            'COUNTERPARTY_NAME': 'International Trade Finance Ltd',
            'COUNTERPARTY_COUNTRY': 'CHE',  # Switzerland
            'DESCRIPTION': 'Large trade settlement - source of funds verification required',
            'RISK_SCORE': 0.85,  # High risk score for large PEP-related deposit
            'SUSPICIOUS_ACTIVITY_FLAG': True,  # Flagged for review
            'CREATED_DATE': datetime.now()
        }
        transactions.append(large_deposit)
    
    # Generate transaction count based on customer risk
    if customer['RISK_RATING'] == 'HIGH':
        transaction_count = random.randint(80, 120)
    elif customer['RISK_RATING'] == 'MEDIUM':
        transaction_count = random.randint(40, 80)
    else:
        transaction_count = random.randint(20, 40)
    
    for i in range(transaction_count):
        transaction = {
            'TRANSACTION_ID': f'TXN_{customer["CUSTOMER_ID"]}_{i+1:04d}',
            'CUSTOMER_ID': customer['CUSTOMER_ID'],
            'TRANSACTION_DATE': datetime.now() - timedelta(days=random.randint(1, 365)),
            'AMOUNT': random.uniform(1000, 100000),
            'CURRENCY': f'{config.CURRENCY}',
            'TRANSACTION_TYPE': random.choice(['CREDIT', 'DEBIT', 'TRANSFER']),
            'COUNTERPARTY_NAME': random.choice(['European Trading Co', 'Nordic Logistics Ltd', 'Baltic Import/Export']),
            'COUNTERPARTY_COUNTRY': random.choice(['DEU', 'FRA', 'NLD', 'BEL']),
            'DESCRIPTION': random.choice(['Trade settlement', 'Service payment', 'Equipment purchase']),
            'RISK_SCORE': random.uniform(0.1, 0.8) if customer['RISK_RATING'] == 'HIGH' else random.uniform(0.1, 0.4),
            'SUSPICIOUS_ACTIVITY_FLAG': random.choice([True, False]) if random.random() < 0.05 else False,
            'CREATED_DATE': datetime.now()
        }
        transactions.append(transaction)
    
    return transactions


def _create_historical_loan(customer: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a single historical loan record."""
    origination_year = random.randint(2019, 2023)
    origination_date = date(origination_year, random.randint(1, 12), random.randint(1, 28))
    
    loan = {
        'LOAN_ID': f'HIST_LOAN_{str(uuid.uuid4())[:8].upper()}',
        'CUSTOMER_ID': None,  # Historical loans may not have current customer IDs
        'APPLICANT_NAME': f'{random.choice(["Tech", "Euro", "Nordic", "Baltic"])} {random.choice(["Solutions", "Industries", "Holdings", "Services"])} {random.choice(["Ltd", "S.A.", "GmbH"])}',
        'ORIGINATION_DATE': origination_date,
        'MATURITY_DATE': origination_date + timedelta(days=random.randint(1095, 2190)),  # 3-6 years
        'ORIGINAL_AMOUNT': random.uniform(500000, 20000000),
        'CURRENCY': f'{config.CURRENCY}',
        'INDUSTRY_SECTOR': random.choice(['Software Services', 'Manufacturing', 'Healthcare', 'Financial Services']),
        'DEBT_TO_EQUITY_AT_ORIGINATION': random.uniform(1.0, 5.0),
        'DSCR_AT_ORIGINATION': random.uniform(0.8, 2.5),
        'CURRENT_RATIO_AT_ORIGINATION': random.uniform(0.8, 2.0),
        'CLIENT_CONCENTRATION_AT_ORIGINATION': random.uniform(15, 85),
        'LOAN_STATUS': random.choice(['PERFORMING', 'PERFORMING', 'PERFORMING', 'DEFAULTED']),  # 75% performing
        'DEFAULT_DATE': None,
        'LOSS_AMOUNT': None,
        'CREATED_DATE': datetime.now()
    }
    
    # Set default details for defaulted loans
    if loan['LOAN_STATUS'] == 'DEFAULTED':
        default_days = random.randint(365, 1460)  # Default within 1-4 years
        loan['DEFAULT_DATE'] = loan['ORIGINATION_DATE'] + timedelta(days=default_days)
        loan['LOSS_AMOUNT'] = loan['ORIGINAL_AMOUNT'] * random.uniform(0.2, 0.8)
    
    return loan


def _create_innovate_loan_application(customer: Dict[str, Any]) -> Dict[str, Any]:
    """Create specific loan application for Innovate GmbH with policy breaches."""
    return {
        'application_id': 'INN-DE-2024-003',
        'customer_id': customer['CUSTOMER_ID'],
        'applicant_name': 'Innovate GmbH',
        'application_date': date(2024, 9, 15),
        'requested_amount': 8500000.00,  # €8.5M
        'currency': f'{config.CURRENCY}',
        'loan_purpose': 'Business expansion and working capital',
        'term_months': 60,
        'application_status': 'UNDER_REVIEW',
        'industry_sector': 'Software Services',
        'annual_revenue': 12500000.00,  # €12.5M
        'total_assets': 8750000.00,
        'total_liabilities': 6200000.00,
        'ebitda': 1875000.00,
        'debt_service_coverage_ratio': 1.15,  # Below warning threshold (1.25)
        'debt_to_equity_ratio': 3.2,  # Above warning threshold (3.0)
        'current_ratio': 1.18,  # Below warning threshold (1.20)
        'single_client_concentration_pct': 72.0,  # Above breach threshold (70%)
        'created_date': datetime.now()
    }


def _create_loan_application(customer: Dict[str, Any]) -> Dict[str, Any]:
    """Create realistic loan application."""
    # Generate realistic financial metrics
    annual_revenue = random.uniform(1000000, 50000000)  # €1M - €50M
    
    return {
        'application_id': f"APP_{str(uuid.uuid4())[:8].upper()}",
        'customer_id': customer['CUSTOMER_ID'],
        'applicant_name': customer['ENTITY_ID'],  # Will be joined with entity name
        'application_date': _generate_application_date(),
        'requested_amount': random.uniform(500000, 20000000),
        'currency': f'{config.CURRENCY}',
        'loan_purpose': random.choice(['Working capital', 'Equipment purchase', 'Business expansion', 'Refinancing']),
        'term_months': random.choice([36, 48, 60, 84]),
        'application_status': random.choice(['SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED']),
        'industry_sector': random.choice(['Manufacturing', 'Services', 'Technology', 'Healthcare']),
        'annual_revenue': annual_revenue,
        'total_assets': annual_revenue * random.uniform(0.5, 1.5),
        'total_liabilities': annual_revenue * random.uniform(0.3, 0.8),
        'ebitda': annual_revenue * random.uniform(0.1, 0.25),
        'debt_service_coverage_ratio': random.uniform(0.8, 2.5),
        'debt_to_equity_ratio': random.uniform(1.0, 4.0),
        'current_ratio': random.uniform(0.8, 2.0),
        'single_client_concentration_pct': random.uniform(10, 80),
        'created_date': datetime.now()
    }


def _generate_sp_global_financials(session: Session) -> None:
    """Generate S&P Global financial data simulation."""
    financials = []
    
    companies = ['Global Trade Ventures S.A.', 'Innovate GmbH', 'Northern Supply Chain Ltd']
    
    for company in companies:
        for year in range(2020, 2025):
            financial = {
                'COMPANY_ID': f'SP_{company.replace(" ", "_").replace(".", "").upper()}',
                'COMPANY_NAME': company,
                'TICKER_SYMBOL': f'{company[:3].upper()}{random.randint(100, 999)}',
                'COUNTRY_CODE': random.choice(['LUX', 'DEU', 'GBR']),
                'INDUSTRY_CODE': random.randint(1000, 9999),
                'FISCAL_YEAR': year,
                'FISCAL_PERIOD': 'FY',
                'REVENUE': random.uniform(5000000, 50000000),
                'EBITDA': random.uniform(500000, 5000000),
                'NET_INCOME': random.uniform(100000, 2000000),
                'TOTAL_ASSETS': random.uniform(10000000, 100000000),
                'TOTAL_DEBT': random.uniform(2000000, 20000000),
                'SHAREHOLDERS_EQUITY': random.uniform(5000000, 30000000),
                'OPERATING_CASH_FLOW': random.uniform(1000000, 8000000),
                'CAPEX': random.uniform(500000, 3000000),
                'CURRENCY': f'{config.CURRENCY}',
                'REPORT_DATE': date(year, 12, 31),
                'DATA_SOURCE': 'S&P Global Market Intelligence via Snowflake Marketplace',
                'LAST_UPDATED': datetime.now()
            }
            financials.append(financial)
    
    if financials:
        financials_df = session.create_dataframe(financials)
        financials_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.SP_GLOBAL_COMPANY_FINANCIALS", mode="overwrite")


def _entity_to_dict(entity: EntityProfile) -> Dict[str, Any]:
    """Convert EntityProfile to dictionary for DataFrame."""
    return {
        'entity_id': entity.entity_id,
        'entity_name': entity.entity_name,
        'entity_type': entity.entity_type,
        'country_code': entity.country_code,
        'industry_sector': entity.industry_sector,
        'incorporation_date': entity.incorporation_date,
        'regulatory_status': entity.regulatory_status,
        'esg_rating': entity.esg_rating,
        'created_date': datetime.now(),
        'last_updated': datetime.now()
    }


def _generate_incorporation_date() -> date:
    """Generate realistic incorporation date."""
    start_date = date(2010, 1, 1)
    end_date = date(2022, 12, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)


def _generate_additional_entities(count: int) -> List[EntityProfile]:
    """Generate additional entities beyond key entities."""
    entities = []
    
    countries = ['DEU', 'FRA', 'NLD', 'BEL', 'LUX', 'ITA', 'ESP', 'GBR']
    industries = [
        'Software Services', 'Manufacturing', 'Financial Services',
        'Healthcare', 'Retail', 'Construction', 'Energy', 'Transportation'
    ]
    esg_ratings = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D']
    
    for i in range(count):
        entity = EntityProfile(
            entity_id=f"ENT_{str(uuid.uuid4())[:8].upper()}",
            entity_name=_generate_company_name(),
            entity_type='CORPORATE',
            country_code=random.choice(countries),
            industry_sector=random.choice(industries),
            incorporation_date=_generate_incorporation_date(),
            regulatory_status=random.choice(['ACTIVE', 'UNDER_REVIEW']),
            esg_rating=random.choice(esg_ratings)
        )
        entities.append(entity)
    
    return entities


def _generate_company_name() -> str:
    """Generate realistic company names."""
    prefixes = ['Euro', 'Global', 'Advanced', 'Innovative', 'Strategic', 'Dynamic', 'Premier']
    roots = ['Tech', 'Solutions', 'Systems', 'Industries', 'Services', 'Group', 'Holdings']
    suffixes = ['GmbH', 'S.A.', 'Ltd', 'B.V.', 'S.p.A.', 'AG']
    
    return f"{random.choice(prefixes)} {random.choice(roots)} {random.choice(suffixes)}"


def _generate_application_date() -> date:
    """Generate realistic application date."""
    start_date = date(2024, 1, 1)
    end_date = date(2024, 9, 30)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)


def _generate_onboarding_date() -> date:
    """Generate realistic customer onboarding date."""
    start_date = date(2020, 1, 1)
    end_date = date(2024, 8, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)


def _generate_review_date() -> date:
    """Generate last review date."""
    return date.today() - timedelta(days=random.randint(30, 365))


def _generate_next_review_date() -> date:
    """Generate next review date."""
    return date.today() + timedelta(days=random.randint(30, 365))


def _generate_rm_name() -> str:
    """Generate relationship manager name."""
    first_names = ['James', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'Robert', 'Anna']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
    return f"{random.choice(first_names)} {random.choice(last_names)}"


def _generate_relationship_date() -> date:
    """Generate relationship effective date."""
    start_date = date(2020, 1, 1)
    end_date = date(2024, 8, 31)
    time_between = end_date - start_date
    days_between = time_between.days
    random_days = random.randrange(days_between)
    return start_date + timedelta(days=random_days)


def _generate_director_name() -> str:
    """Generate director name for entity relationships."""
    first_names = ['Anya', 'Boris', 'Chen', 'Dimitri', 'Elena', 'Francois', 'Giovanni', 'Hans', 'Ivan', 'Jacques']
    last_names = ['Sharma', 'Volkov', 'Zhang', 'Petrov', 'Rossi', 'Dubois', 'Bianchi', 'Schmidt', 'Ivanov', 'Moreau']
    return f"{random.choice(first_names)} {random.choice(last_names)}"


# =============================================================================
# PHASE 2 DATA GENERATION FUNCTIONS
# =============================================================================

def generate_client_crm(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate client CRM records for relationship manager scenario."""
    logger.info("Generating client CRM records...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('client_crm_records', 0)
    
    if target_count == 0:
        logger.info("Skipping client CRM generation (not in scale config)")
        return
    
    # Get existing customers
    customers_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
    customers = customers_df.select("CUSTOMER_ID").collect()
    
    if not customers:
        logger.warning("No customers found, skipping CRM generation")
        return
    
    relationship_managers = [
        'Claire Dubois', 'Marcus Weber', 'Sofia Rossi', 'Hans Schmidt', 'Emma Johnson',
        'Pierre Lefebvre', 'Anna Müller', 'Giovanni Bianchi', 'Laura Martinez', 'Thomas Anderson'
    ]
    
    account_statuses = ['ACTIVE', 'PROSPECT', 'INACTIVE']
    account_tiers = ['PREMIUM', 'STANDARD', 'BASIC']
    
    crm_records = []
    
    # Ensure primary RM client is included
    primary_rm_client = config.KEY_ENTITIES.get('primary_rm_client')
    
    for i in range(target_count):
        customer = random.choice(customers)
        customer_id = customer['CUSTOMER_ID']
        
        # Use primary RM client for first record if it exists
        if i == 0 and primary_rm_client:
            customer_id = primary_rm_client['entity_id']
            rm = primary_rm_client['relationship_manager']
            status = primary_rm_client['account_status']
            tier = 'PREMIUM'
        else:
            rm = random.choice(relationship_managers)
            status = random.choices(account_statuses, weights=[0.7, 0.2, 0.1])[0]
            tier = random.choices(account_tiers, weights=[0.2, 0.5, 0.3])[0]
        
        last_contact = date.today() - timedelta(days=random.randint(1, 60))
        
        # Generate opportunity count
        opportunity_count = random.choices([0, 1, 2, 3, 4, 5], weights=[0.3, 0.3, 0.2, 0.1, 0.05, 0.05])[0]
        
        notes_summary = f"Last contact: {last_contact.strftime('%Y-%m-%d')}. Account tier: {tier}. {opportunity_count} opportunities identified."
        
        crm_record = {
            'crm_id': f"CRM_{i+1:05d}",
            'customer_id': customer_id,
            'relationship_manager': rm,
            'last_contact_date': last_contact,
            'account_status': status,
            'account_tier': tier,
            'notes_summary': notes_summary,
            'risk_opportunities_count': opportunity_count,
            'created_date': datetime.now()
        }
        crm_records.append(crm_record)
    
    # Save to table with schema
    schema = _get_snowpark_schema(config.PHASE_2_SCHEMAS['client_crm'])
    crm_df = session.create_dataframe(crm_records, schema=schema)
    crm_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM", mode="overwrite")
    
    logger.info(f"Generated {len(crm_records)} client CRM records")


def generate_client_opportunities(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate client opportunities for relationship manager scenario."""
    logger.info("Generating client opportunities...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('client_opportunities', 0)
    
    if target_count == 0:
        logger.info("Skipping client opportunities generation (not in scale config)")
        return
    
    # Get existing CRM records
    try:
        crm_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM")
        crm_records = crm_df.select("CUSTOMER_ID", "RISK_OPPORTUNITIES_COUNT").collect()
    except:
        logger.warning("No CRM records found, skipping opportunities generation")
        return
    
    opportunity_types = [
        'CROSS_SELL', 'UPSELL', 'RISK_MITIGATION', 'NEW_PRODUCT', 
        'INVESTMENT_ADVISORY', 'TRADE_FINANCE', 'FX_HEDGING'
    ]
    
    source_types = ['call_note', 'internal_email', 'news', 'transaction_pattern', 'market_intelligence']
    priorities = ['HIGH', 'MEDIUM', 'LOW']
    statuses = ['OPEN', 'IN_PROGRESS', 'CLOSED_WON', 'CLOSED_LOST']
    
    opportunities = []
    
    for i in range(target_count):
        crm_record = random.choice(crm_records)
        customer_id = crm_record['CUSTOMER_ID']
        
        opp_type = random.choice(opportunity_types)
        source_type = random.choice(source_types)
        priority = random.choices(priorities, weights=[0.2, 0.5, 0.3])[0]
        status = random.choices(statuses, weights=[0.4, 0.3, 0.2, 0.1])[0]
        
        # Generate realistic descriptions based on type
        descriptions = {
            'CROSS_SELL': f"Cross-sell FX hedging products to protect against currency fluctuation",
            'UPSELL': f"Upsell to premium banking tier for expanded trade finance limits",
            'RISK_MITIGATION': f"Address concentration risk through supplier diversification advisory",
            'NEW_PRODUCT': f"Introduce sustainable finance solutions aligned with ESG goals",
            'INVESTMENT_ADVISORY': f"Offer treasury optimization services for excess cash management",
            'TRADE_FINANCE': f"Expand documentary credit facilities for international expansion",
            'FX_HEDGING': f"Implement forward contracts to hedge EUR/USD exposure"
        }
        
        potential_value = random.choice([50000, 100000, 250000, 500000, 1000000, 2500000])
        
        opportunity = {
            'opportunity_id': f"OPP_{i+1:06d}",
            'customer_id': customer_id,
            'opportunity_type': opp_type,
            'opportunity_description': descriptions.get(opp_type, f"{opp_type} opportunity"),
            'potential_value': potential_value,
            'source_type': source_type,
            'source_document_id': f"DOC_{random.randint(1000, 9999)}",
            'priority': priority,
            'status': status,
            'created_date': datetime.now() - timedelta(days=random.randint(1, 90)),
            'last_updated_date': datetime.now() - timedelta(days=random.randint(0, 30))
        }
        opportunities.append(opportunity)
    
    # Save to table with schema
    schema = _get_snowpark_schema(config.PHASE_2_SCHEMAS['client_opportunities'])
    opp_df = session.create_dataframe(opportunities, schema=schema)
    opp_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_OPPORTUNITIES", mode="overwrite")
    
    logger.info(f"Generated {len(opportunities)} client opportunities")


def generate_model_portfolios(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate model portfolios for wealth advisor scenario."""
    logger.info("Generating model portfolios...")
    
    scale_config = config.get_scale_config(scale)
    portfolio_count = scale_config.get('model_portfolios', 3)
    
    if portfolio_count == 0:
        logger.info("Skipping model portfolios generation (not in scale config)")
        return
    
    # Define standard model portfolios
    models = [
        {
            'model_id': 'MODEL_CONSERVATIVE',
            'model_name': 'Conservative Growth',
            'risk_profile': 'LOW',
            'target_equity_pct': 30.0,
            'target_bond_pct': 60.0,
            'target_alternative_pct': 5.0,
            'target_cash_pct': 5.0,
            'expected_annual_return_pct': 4.5,
            'expected_volatility_pct': 6.0,
            'description': 'Capital preservation with modest growth. Suitable for risk-averse investors.',
            'rebalance_frequency_days': 180
        },
        {
            'model_id': 'MODEL_BALANCED',
            'model_name': 'Balanced Portfolio',
            'risk_profile': 'MODERATE',
            'target_equity_pct': 50.0,
            'target_bond_pct': 40.0,
            'target_alternative_pct': 7.0,
            'target_cash_pct': 3.0,
            'expected_annual_return_pct': 6.5,
            'expected_volatility_pct': 10.0,
            'description': 'Balanced growth and income with moderate risk. Suitable for long-term investors.',
            'rebalance_frequency_days': 180
        },
        {
            'model_id': 'MODEL_GROWTH',
            'model_name': 'Growth Portfolio',
            'risk_profile': 'MODERATE',
            'target_equity_pct': 70.0,
            'target_bond_pct': 20.0,
            'target_alternative_pct': 8.0,
            'target_cash_pct': 2.0,
            'expected_annual_return_pct': 8.5,
            'expected_volatility_pct': 14.0,
            'description': 'Long-term capital appreciation with higher volatility tolerance.',
            'rebalance_frequency_days': 90
        },
        {
            'model_id': 'MODEL_AGGRESSIVE',
            'model_name': 'Aggressive Growth',
            'risk_profile': 'HIGH',
            'target_equity_pct': 85.0,
            'target_bond_pct': 5.0,
            'target_alternative_pct': 10.0,
            'target_cash_pct': 0.0,
            'expected_annual_return_pct': 10.5,
            'expected_volatility_pct': 18.0,
            'description': 'Maximum growth potential for high risk tolerance and long time horizons.',
            'rebalance_frequency_days': 90
        },
        {
            'model_id': 'MODEL_INCOME',
            'model_name': 'Income Portfolio',
            'risk_profile': 'LOW',
            'target_equity_pct': 25.0,
            'target_bond_pct': 65.0,
            'target_alternative_pct': 5.0,
            'target_cash_pct': 5.0,
            'expected_annual_return_pct': 4.0,
            'expected_volatility_pct': 5.0,
            'description': 'Focus on income generation with low volatility. Suitable for retirees.',
            'rebalance_frequency_days': 365
        }
    ]
    
    # Take only the requested number of models
    portfolios = models[:portfolio_count]
    
    # Add created_date
    for portfolio in portfolios:
        portfolio['created_date'] = datetime.now() - timedelta(days=random.randint(365, 730))
    
    # Save to table with schema
    schema = _get_snowpark_schema(config.PHASE_2_SCHEMAS['model_portfolios'])
    portfolios_df = session.create_dataframe(portfolios, schema=schema)
    portfolios_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.MODEL_PORTFOLIOS", mode="overwrite")
    
    logger.info(f"Generated {len(portfolios)} model portfolios")


def generate_holdings(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate investment holdings for wealth clients."""
    logger.info("Generating holdings...")
    
    scale_config = config.get_scale_config(scale)
    total_holdings = scale_config.get('holdings', 0)
    wealth_client_count = scale_config.get('wealth_clients', 0)
    
    if total_holdings == 0 or wealth_client_count == 0:
        logger.info("Skipping holdings generation (not in scale config)")
        return
    
    # Get existing customers
    try:
        customers_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
        customers = customers_df.select("CUSTOMER_ID").collect()
        
        if len(customers) < wealth_client_count:
            wealth_client_count = len(customers)
            logger.warning(f"Not enough customers, using {wealth_client_count} wealth clients")
        
        # Select random customers to be wealth clients
        wealth_customers = random.sample([c['CUSTOMER_ID'] for c in customers], wealth_client_count)
    except:
        logger.warning("No customers found, skipping holdings generation")
        return
    
    # Define asset types and examples
    assets = {
        'EQUITY': [
            ('DOMESTIC_EQUITY', 'DAX 40 ETF', 'EXS1.DE', 8.5),
            ('DOMESTIC_EQUITY', 'CAC 40 ETF', 'C40.PA', 7.5),
            ('INTL_EQUITY', 'S&P 500 ETF', 'SPY', 12.0),
            ('INTL_EQUITY', 'MSCI World ETF', 'IWDA.AS', 10.0),
            ('EMERGING_MARKETS', 'MSCI EM ETF', 'EEM', 15.0),
        ],
        'BOND': [
            ('GOVT_BOND', 'German Government Bonds', 'BUND', 3.0),
            ('GOVT_BOND', 'EU Sovereign Bond ETF', 'IEAG.AS', 3.5),
            ('CORP_BOND', 'EUR Corporate Bond ETF', 'CORP.PA', 4.5),
            ('CORP_BOND', 'High Yield Bond ETF', 'HYG', 6.0),
        ],
        'ALTERNATIVE': [
            ('REAL_ESTATE', 'European REIT ETF', 'IQQP.AS', 6.5),
            ('COMMODITIES', 'Gold ETF', 'GLD', 8.0),
            ('INFRASTRUCTURE', 'Global Infrastructure', 'IGF', 5.5),
        ],
        'CASH': [
            ('MONEY_MARKET', 'EUR Money Market Fund', 'MMF_EUR', 2.5),
        ]
    }
    
    holdings = []
    holdings_per_client = total_holdings // wealth_client_count
    
    for customer_id in wealth_customers:
        # Generate portfolio for this client
        client_total_value = random.uniform(1000000, 10000000)  # €1M to €10M
        
        # Ensure primary wealth client gets specific AUM if defined
        primary_wealth_client = config.KEY_ENTITIES.get('primary_wealth_client')
        if primary_wealth_client and customer_id == primary_wealth_client['entity_id']:
            client_total_value = primary_wealth_client.get('aum', 50000000)
        
        for i in range(holdings_per_client):
            # Select random asset
            asset_type = random.choice(list(assets.keys()))
            asset_class, asset_name, ticker, volatility = random.choice(assets[asset_type])
            
            # Generate holding details
            quantity = random.uniform(100, 10000)
            cost_basis_per_unit = random.uniform(50, 500)
            current_price_per_unit = cost_basis_per_unit * random.uniform(0.8, 1.3)  # -20% to +30%
            
            current_value = quantity * current_price_per_unit
            cost_basis = quantity * cost_basis_per_unit
            unrealized_gain_loss = current_value - cost_basis
            
            # Will calculate allocation_pct after all holdings generated
            
            holding = {
                'holding_id': f"HOLD_{len(holdings)+1:06d}",
                'customer_id': customer_id,
                'asset_type': asset_type,
                'asset_class': asset_class,
                'asset_name': asset_name,
                'ticker_symbol': ticker,
                'quantity': round(quantity, 2),
                'current_value': round(current_value, 2),
                'cost_basis': round(cost_basis, 2),
                'unrealized_gain_loss': round(unrealized_gain_loss, 2),
                'allocation_pct': 0.0,  # Will calculate below
                'as_of_date': date.today(),
                'last_updated_date': datetime.now()
            }
            holdings.append(holding)
        
        # Calculate allocation percentages for this customer
        customer_holdings = [h for h in holdings if h['customer_id'] == customer_id]
        total_value = sum(h['current_value'] for h in customer_holdings)
        
        for holding in customer_holdings:
            holding['allocation_pct'] = round((holding['current_value'] / total_value) * 100, 2)
    
    # Save to table with schema
    schema = _get_snowpark_schema(config.PHASE_2_SCHEMAS['holdings'])
    holdings_df = session.create_dataframe(holdings, schema=schema)
    holdings_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.HOLDINGS", mode="overwrite")
    
    logger.info(f"Generated {len(holdings)} holdings for {wealth_client_count} wealth clients")


def generate_wealth_client_profiles(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate wealth client profiles linking customers to model portfolios."""
    logger.info("Generating wealth client profiles...")
    
    scale_config = config.get_scale_config(scale)
    wealth_client_count = scale_config.get('wealth_clients', 0)
    
    if wealth_client_count == 0:
        logger.info("Skipping wealth client profiles generation (not in scale config)")
        return
    
    # Get existing holdings to identify wealth customers
    try:
        holdings_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.HOLDINGS")
        wealth_customers = holdings_df.select("CUSTOMER_ID").distinct().collect()
        wealth_customer_ids = [c['CUSTOMER_ID'] for c in wealth_customers]
    except:
        logger.warning("No holdings found, skipping wealth profiles generation")
        return
    
    # Get model portfolios
    try:
        portfolios_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.MODEL_PORTFOLIOS")
        portfolios = portfolios_df.select("MODEL_ID", "RISK_PROFILE").collect()
    except:
        logger.warning("No model portfolios found, skipping wealth profiles generation")
        return
    
    wealth_advisors = ['Marcus Weber', 'Sofia Rossi', 'Jean-Pierre Dubois', 'Anna Müller', 'Laura Martinez']
    risk_tolerances = ['CONSERVATIVE', 'MODERATE', 'AGGRESSIVE']
    tax_statuses = ['STANDARD', 'TAX_DEFERRED', 'TAX_EXEMPT']
    investment_objectives = ['GROWTH', 'INCOME', 'PRESERVATION', 'BALANCED']
    
    profiles = []
    
    for i, customer_id in enumerate(wealth_customer_ids):
        # Select matching model portfolio based on risk tolerance
        risk_tolerance = random.choice(risk_tolerances)
        
        # Map risk tolerance to model
        if risk_tolerance == 'CONSERVATIVE':
            matching_portfolios = [p for p in portfolios if p['RISK_PROFILE'] == 'LOW']
        elif risk_tolerance == 'AGGRESSIVE':
            matching_portfolios = [p for p in portfolios if p['RISK_PROFILE'] == 'HIGH']
        else:
            matching_portfolios = [p for p in portfolios if p['RISK_PROFILE'] == 'MODERATE']
        
        if not matching_portfolios:
            matching_portfolios = portfolios  # Fallback to any
        
        model_portfolio = random.choice(matching_portfolios)
        
        # Get primary wealth client config if this is the primary
        primary_wealth_client = config.KEY_ENTITIES.get('primary_wealth_client')
        if primary_wealth_client and customer_id == primary_wealth_client['entity_id']:
            advisor = primary_wealth_client.get('wealth_advisor', random.choice(wealth_advisors))
            risk_tolerance = primary_wealth_client.get('risk_tolerance', 'MODERATE')
            total_aum = primary_wealth_client.get('aum', 50000000)
        else:
            advisor = random.choice(wealth_advisors)
            total_aum = random.uniform(1000000, 10000000)
        
        # Calculate total AUM from holdings
        try:
            customer_holdings_df = holdings_df.filter(col("CUSTOMER_ID") == customer_id)
            customer_holdings = customer_holdings_df.collect()
            total_aum = sum(h['CURRENT_VALUE'] for h in customer_holdings)
        except:
            pass  # Use generated AUM
        
        last_rebalance = date.today() - timedelta(days=random.randint(30, 180))
        next_review = date.today() + timedelta(days=random.randint(30, 90))
        
        profile = {
            'profile_id': f"WCP_{i+1:05d}",
            'customer_id': customer_id,
            'model_portfolio_id': model_portfolio['MODEL_ID'],
            'wealth_advisor': advisor,
            'risk_tolerance': risk_tolerance,
            'tax_status': random.choice(tax_statuses),
            'investment_objectives': random.choice(investment_objectives),
            'total_aum': round(total_aum, 2),
            'concentration_threshold_pct': 70.0,  # Alert if any holding exceeds 70%
            'rebalance_trigger_pct': 10.0,  # Rebalance if deviation exceeds 10%
            'last_rebalance_date': last_rebalance,
            'next_review_date': next_review,
            'created_date': datetime.now() - timedelta(days=random.randint(365, 1095)),
            'last_updated_date': datetime.now()
        }
        profiles.append(profile)
    
    # Save to table with schema
    schema = _get_snowpark_schema(config.PHASE_2_SCHEMAS['wealth_client_profiles'])
    profiles_df = session.create_dataframe(profiles, schema=schema)
    profiles_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_CLIENT_PROFILES", mode="overwrite")
    
    logger.info(f"Generated {len(profiles)} wealth client profiles")


def main():
    """Main function for testing structured data generation."""
    print("Structured data generator module loaded successfully")
    print("Use generate_all_structured_data() method to create structured demo data")


if __name__ == "__main__":
    main()
