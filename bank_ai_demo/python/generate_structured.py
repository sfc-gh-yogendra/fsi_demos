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

import config

logger = logging.getLogger(__name__)


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
    """Generate all structured data for Phase 1."""
    logger.info("Starting structured data generation...")
    
    # Set random seed for reproducible generation
    random.seed(config.GENERATION_SEED)
    
    # Generate in dependency order
    generate_entities(session, scale, scenarios)
    generate_entity_relationships(session, scale, scenarios)
    generate_customers(session, scale, scenarios)
    generate_transactions(session, scale, scenarios)
    generate_loan_applications(session, scale, scenarios)
    generate_historical_loans(session, scale, scenarios)
    generate_external_data_simulation(session, scale, scenarios)
    
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
            'risk_score': 0.85
        },
        {
            'primary': 'INN_DE_001',  # Innovate GmbH
            'related': 'NSC_UK_001',  # Northern Supply Chain
            'type': 'VENDOR',
            'strength': 'SECONDARY',
            'risk_score': 0.45
        },
        # Customer relationship
        {
            'primary': 'INN_DE_001',  # Innovate GmbH
            'related': 'GTV_SA_001',  # Global Trade Ventures
            'type': 'CUSTOMER',
            'strength': 'INDIRECT',
            'risk_score': 0.25
        }
    ]
    
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
            relationship = {
                'relationship_id': str(uuid.uuid4()),
                'primary_entity_id': primary_entity['ENTITY_ID'],
                'related_entity_id': related_entity['ENTITY_ID'],
                'relationship_type': random.choice(['VENDOR', 'CUSTOMER', 'COMPETITOR', 'SUBSIDIARY']),
                'relationship_strength': random.choice(['PRIMARY', 'SECONDARY', 'INDIRECT']),
                'effective_date': _generate_relationship_date(),
                'end_date': None,
                'risk_impact_score': random.uniform(0.1, 0.9),
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
        
        customer = {
            'customer_id': f"CUST_{entity['ENTITY_ID']}",
            'entity_id': entity['ENTITY_ID'],
            'customer_type': 'CORPORATE',
            'onboarding_date': _generate_onboarding_date(),
            'risk_rating': risk_rating,
            'kyc_status': kyc_status,
            'last_review_date': _generate_review_date(),
            'next_review_date': _generate_next_review_date(),
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


def main():
    """Main function for testing structured data generation."""
    print("Structured data generator module loaded successfully")
    print("Use generate_all_structured_data() method to create structured demo data")


if __name__ == "__main__":
    main()
