"""
Glacier First Bank Demo - Structured Data Generator

Generates realistic structured data for all demo scenarios using pure SQL.
Includes entities, relationships, customers, transactions, loan applications, and wealth management data.
"""

import uuid
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging
from snowflake.snowpark import Session
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
                COMMENT = 'Glacier First Bank AI Intelligence Demo'
        """).collect()
        
        logger.info(f"Created database: {config.SNOWFLAKE['database']}")
        
        # Set database context
        session.sql(f"USE DATABASE {config.SNOWFLAKE['database']}").collect()
        
        # Create schemas
        schemas = [
            ('RAW_DATA', 'Raw/temporary working tables for data generation'),
            ('CURATED', 'Curated dimension/fact tables and unstructured document corpus'),
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
    """Generate all structured data for demo scenarios."""
    logger.info("Starting structured data generation...")
    
    # Set random seed for reproducible generation
    random.seed(config.GENERATION_SEED)
    
    # Drop all existing tables to ensure clean slate with unquoted identifiers
    logger.info("Dropping existing tables to ensure clean slate...")
    tables_to_drop = [
        "ENTITIES", "ENTITY_RELATIONSHIPS", "CUSTOMERS", "TRANSACTIONS",
        "LOAN_APPLICATIONS", "HISTORICAL_LOANS", "ALERTS", "ALERT_DISPOSITION_HISTORY",
        "SP_GLOBAL_COMPANY_FINANCIALS", "CLIENT_CRM", "CLIENT_OPPORTUNITIES",
        "MODEL_PORTFOLIOS", "HOLDINGS", "WEALTH_CLIENT_PROFILES"
    ]
    
    for table in tables_to_drop:
        try:
            session.sql(f"DROP TABLE IF EXISTS {config.SNOWFLAKE['database']}.RAW_DATA.{table}").collect()
        except Exception as e:
            logger.debug(f"Could not drop table {table}: {e}")
    
    logger.info("Clean slate established - all tables dropped")
    
    # Determine which data to generate based on scenarios
    commercial_wealth_scenarios = {'corp_relationship_manager', 'wealth_advisor'}
    include_commercial_wealth = (scenarios == ["all"] or not scenarios or 
                                  any(s in commercial_wealth_scenarios for s in scenarios))
    
    # Core data generation in dependency order
    generate_entities(session, scale, scenarios)
    generate_entity_relationships(session, scale, scenarios)
    generate_customers(session, scale, scenarios)
    generate_transactions(session, scale, scenarios)
    generate_loan_applications(session, scale, scenarios)
    generate_historical_loans(session, scale, scenarios)
    generate_alerts(session, scale, scenarios)
    generate_alert_disposition_history(session, scale, scenarios)
    generate_external_data_simulation(session, scale, scenarios)
    
    # Commercial & Wealth data generation (if scenarios requested or "all")
    if include_commercial_wealth:
        logger.info("Generating Commercial & Wealth data...")
        generate_model_portfolios(session, scale, scenarios)  # Must be before wealth profiles
        generate_client_crm(session, scale, scenarios)
        generate_client_opportunities(session, scale, scenarios)  # Depends on CRM
        generate_holdings(session, scale, scenarios)  # Must be before wealth profiles
        generate_wealth_client_profiles(session, scale, scenarios)  # Depends on holdings and model portfolios
    
    logger.info("Structured data generation completed successfully")


def generate_entities(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate entities with key demo entities guaranteed using pure SQL."""
    logger.info("Generating entities (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    key_entities = config.KEY_ENTITIES
    additional_count = scale_config['entities'] - len(key_entities)
    
    # Build key entities SQL
    key_entity_selects = []
    for entity_key, entity_spec in key_entities.items():
        incorporation_days_ago = random.randint(1500, 5000)  # ~4-13 years ago
        key_entity_selects.append(f"""
            SELECT 
                '{entity_spec['entity_id']}' AS ENTITY_ID,
                '{entity_spec['name']}' AS ENTITY_NAME,
                'CORPORATE' AS ENTITY_TYPE,
                '{entity_spec['country']}' AS COUNTRY_CODE,
                '{entity_spec['industry']}' AS INDUSTRY_SECTOR,
                DATEADD(day, -{incorporation_days_ago}, CURRENT_DATE()) AS INCORPORATION_DATE,
                '{entity_spec.get('regulatory_status', 'ACTIVE')}' AS REGULATORY_STATUS,
                '{entity_spec.get('esg_rating', 'B')}' AS ESG_RATING,
                CURRENT_TIMESTAMP() AS CREATED_DATE,
                CURRENT_TIMESTAMP() AS LAST_UPDATED
        """)
    
    key_entities_union = " UNION ALL ".join(key_entity_selects)
    
    create_entities_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES AS
    WITH
    -- Key entities for demo scenarios
    key_entities AS (
        {key_entities_union}
    ),
    -- Additional entities
    additional_entities AS (
        SELECT 
            'ENT_' || SUBSTR(UUID_STRING(), 1, 8) AS ENTITY_ID,
            CASE UNIFORM(0, 6, ROW_SEQ)
                WHEN 0 THEN 'Euro'
                WHEN 1 THEN 'Global'
                WHEN 2 THEN 'Advanced'
                WHEN 3 THEN 'Innovative'
                WHEN 4 THEN 'Strategic'
                WHEN 5 THEN 'Dynamic'
                ELSE 'Premier'
            END || ' ' ||
            CASE UNIFORM(0, 6, ROW_SEQ + 1)
                WHEN 0 THEN 'Tech'
                WHEN 1 THEN 'Solutions'
                WHEN 2 THEN 'Systems'
                WHEN 3 THEN 'Industries'
                WHEN 4 THEN 'Services'
                WHEN 5 THEN 'Group'
                ELSE 'Holdings'
            END || ' ' ||
            CASE UNIFORM(0, 5, ROW_SEQ + 2)
                WHEN 0 THEN 'GmbH'
                WHEN 1 THEN 'S.A.'
                WHEN 2 THEN 'Ltd'
                WHEN 3 THEN 'B.V.'
                WHEN 4 THEN 'S.p.A.'
                ELSE 'AG'
            END AS ENTITY_NAME,
            'CORPORATE' AS ENTITY_TYPE,
            CASE UNIFORM(0, 7, ROW_SEQ + 3)
                WHEN 0 THEN 'DEU'
                WHEN 1 THEN 'FRA'
                WHEN 2 THEN 'NLD'
                WHEN 3 THEN 'BEL'
                WHEN 4 THEN 'LUX'
                WHEN 5 THEN 'ITA'
                WHEN 6 THEN 'ESP'
                ELSE 'GBR'
            END AS COUNTRY_CODE,
            CASE UNIFORM(0, 7, ROW_SEQ + 4)
                WHEN 0 THEN 'Software Services'
                WHEN 1 THEN 'Manufacturing'
                WHEN 2 THEN 'Financial Services'
                WHEN 3 THEN 'Healthcare'
                WHEN 4 THEN 'Retail'
                WHEN 5 THEN 'Construction'
                WHEN 6 THEN 'Energy'
                ELSE 'Transportation'
            END AS INDUSTRY_SECTOR,
            DATEADD(day, -UNIFORM(1500, 5000, ROW_SEQ + 5), CURRENT_DATE()) AS INCORPORATION_DATE,
            CASE MOD(UNIFORM(0, 3, ROW_SEQ + 6), 4)
                WHEN 0 THEN 'ACTIVE'
                WHEN 1 THEN 'ACTIVE'
                WHEN 2 THEN 'ACTIVE'
                ELSE 'UNDER_REVIEW'
            END AS REGULATORY_STATUS,
            CASE UNIFORM(0, 6, ROW_SEQ + 7)
                WHEN 0 THEN 'A+'
                WHEN 1 THEN 'A'
                WHEN 2 THEN 'B+'
                WHEN 3 THEN 'B'
                WHEN 4 THEN 'C+'
                WHEN 5 THEN 'C'
                ELSE 'D'
            END AS ESG_RATING,
            CURRENT_TIMESTAMP() AS CREATED_DATE,
            CURRENT_TIMESTAMP() AS LAST_UPDATED
        FROM (
            SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS ROW_SEQ
            FROM TABLE(GENERATOR(ROWCOUNT => {additional_count}))
        )
    )
    -- Combine key and additional entities
    SELECT * FROM key_entities
    UNION ALL
    SELECT * FROM additional_entities
    """
    
    session.sql(create_entities_sql).collect()
    
    logger.info(f"Generated {scale_config['entities']} entities ({len(key_entities)} key entities) using pure SQL")


def generate_entity_relationships(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate entity relationships for cross-domain intelligence using pure SQL."""
    logger.info("Generating entity relationships (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    
    # Define key relationships and shell network as SQL
    shared_director_name = 'Anya Sharma'
    shared_address = '42 Mailbox Lane, Virtual Office Complex, Gibraltar'
    key_count = 8  # 3 key relationships + 5 shell network relationships
    additional_count = scale_config['entity_relationships'] - key_count
    
    create_relationships_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.CURATED.ENTITY_RELATIONSHIPS AS
    WITH
    -- Key demo relationships and shell network
    key_relationships AS (
        -- Northern Supply Chain as shared vendor for Global Trade Ventures
        SELECT 
            UUID_STRING() AS RELATIONSHIP_ID,
            'GTV_SA_001' AS PRIMARY_ENTITY_ID,
            'NSC_UK_001' AS RELATED_ENTITY_ID,
            'VENDOR' AS RELATIONSHIP_TYPE,
            'PRIMARY' AS RELATIONSHIP_STRENGTH,
            DATEADD(day, -UNIFORM(365, 1095, RANDOM()), CURRENT_DATE()) AS EFFECTIVE_DATE,
            NULL AS END_DATE,
            0.85 AS RISK_IMPACT_SCORE,
            NULL AS SHARED_DIRECTOR_NAME,
            FALSE AS SHARED_ADDRESS_FLAG,
            NULL AS SHARED_ADDRESS,
            NULL AS INCORPORATION_PROXIMITY_DAYS,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        UNION ALL
        -- Northern Supply Chain as vendor for Innovate GmbH
        SELECT 
            UUID_STRING(), 'INN_DE_001', 'NSC_UK_001', 'VENDOR', 'SECONDARY',
            DATEADD(day, -UNIFORM(365, 1095, RANDOM()), CURRENT_DATE()),
            NULL, 0.45, NULL, FALSE, NULL, NULL, CURRENT_TIMESTAMP()
        UNION ALL
        -- Customer relationship between Innovate and Global Trade
        SELECT 
            UUID_STRING(), 'INN_DE_001', 'GTV_SA_001', 'CUSTOMER', 'INDIRECT',
            DATEADD(day, -UNIFORM(365, 1095, RANDOM()), CURRENT_DATE()),
            NULL, 0.25, NULL, FALSE, NULL, NULL, CURRENT_TIMESTAMP()
        UNION ALL
        -- Shell network circular relationships (5 entities in a circle)
        SELECT 
            UUID_STRING(), 'SHELL_NET_001', 'SHELL_NET_002', 'VENDOR', 'PRIMARY',
            DATEADD(day, -UNIFORM(180, 365, RANDOM()), CURRENT_DATE()),
            NULL, 0.92, '{shared_director_name}', TRUE, '{shared_address}',
            UNIFORM(1, 45, RANDOM()), CURRENT_TIMESTAMP()
        UNION ALL
        SELECT 
            UUID_STRING(), 'SHELL_NET_002', 'SHELL_NET_003', 'VENDOR', 'PRIMARY',
            DATEADD(day, -UNIFORM(180, 365, RANDOM()), CURRENT_DATE()),
            NULL, 0.92, '{shared_director_name}', TRUE, '{shared_address}',
            UNIFORM(1, 45, RANDOM()), CURRENT_TIMESTAMP()
        UNION ALL
        SELECT 
            UUID_STRING(), 'SHELL_NET_003', 'SHELL_NET_004', 'VENDOR', 'PRIMARY',
            DATEADD(day, -UNIFORM(180, 365, RANDOM()), CURRENT_DATE()),
            NULL, 0.92, '{shared_director_name}', TRUE, '{shared_address}',
            UNIFORM(1, 45, RANDOM()), CURRENT_TIMESTAMP()
        UNION ALL
        SELECT 
            UUID_STRING(), 'SHELL_NET_004', 'SHELL_NET_005', 'VENDOR', 'PRIMARY',
            DATEADD(day, -UNIFORM(180, 365, RANDOM()), CURRENT_DATE()),
            NULL, 0.92, '{shared_director_name}', TRUE, '{shared_address}',
            UNIFORM(1, 45, RANDOM()), CURRENT_TIMESTAMP()
        UNION ALL
        -- Close the circle
        SELECT 
            UUID_STRING(), 'SHELL_NET_005', 'SHELL_NET_001', 'VENDOR', 'PRIMARY',
            DATEADD(day, -UNIFORM(180, 365, RANDOM()), CURRENT_DATE()),
            NULL, 0.92, '{shared_director_name}', TRUE, '{shared_address}',
            UNIFORM(1, 45, RANDOM()), CURRENT_TIMESTAMP()
    ),
    -- Random entity pairs for additional relationships
    entity_pairs AS (
        SELECT 
            ROW_NUMBER() OVER (ORDER BY SEQ4()) AS PAIR_SEQ,
            PRIMARY_ENTITY_ID,
            RELATED_ENTITY_ID
        FROM (
            SELECT 
                e1.ENTITY_ID AS PRIMARY_ENTITY_ID,
                e2.ENTITY_ID AS RELATED_ENTITY_ID,
                ROW_NUMBER() OVER (ORDER BY RANDOM()) AS RN
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES e1
            CROSS JOIN {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES e2
            WHERE e1.ENTITY_ID != e2.ENTITY_ID
            ORDER BY RANDOM()
            LIMIT {additional_count}
        )
    ),
    -- Additional relationships
    additional_relationships AS (
        SELECT 
            UUID_STRING() AS RELATIONSHIP_ID,
            PRIMARY_ENTITY_ID,
            RELATED_ENTITY_ID,
            CASE UNIFORM(0, 3, PAIR_SEQ)
                WHEN 0 THEN 'VENDOR'
                WHEN 1 THEN 'CUSTOMER'
                WHEN 2 THEN 'COMPETITOR'
                ELSE 'SUBSIDIARY'
            END AS RELATIONSHIP_TYPE,
            CASE UNIFORM(0, 2, PAIR_SEQ + 1)
                WHEN 0 THEN 'PRIMARY'
                WHEN 1 THEN 'SECONDARY'
                ELSE 'INDIRECT'
            END AS RELATIONSHIP_STRENGTH,
            DATEADD(day, -UNIFORM(365, 1095, PAIR_SEQ + 2), CURRENT_DATE()) AS EFFECTIVE_DATE,
            NULL AS END_DATE,
            UNIFORM(10, 90, PAIR_SEQ + 3) / 100.0 AS RISK_IMPACT_SCORE,
            CASE 
                WHEN UNIFORM(0, 100, PAIR_SEQ + 4) < 10 THEN
                    CASE UNIFORM(0, 4, PAIR_SEQ + 5)
                        WHEN 0 THEN 'John Smith'
                        WHEN 1 THEN 'Maria Garcia'
                        WHEN 2 THEN 'Hans Mueller'
                        WHEN 3 THEN 'Sophie Dubois'
                        ELSE 'Marco Rossi'
                    END
                ELSE NULL
            END AS SHARED_DIRECTOR_NAME,
            (UNIFORM(0, 100, PAIR_SEQ + 4) < 10) AS SHARED_ADDRESS_FLAG,
            CASE 
                WHEN UNIFORM(0, 100, PAIR_SEQ + 4) < 10 THEN 'Virtual Office, Business Center'
                ELSE NULL
            END AS SHARED_ADDRESS,
            CASE 
                WHEN UNIFORM(0, 100, PAIR_SEQ + 4) < 10 THEN UNIFORM(1, 90, PAIR_SEQ + 6)
                ELSE NULL
            END AS INCORPORATION_PROXIMITY_DAYS,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        FROM entity_pairs
    )
    -- Combine key and additional relationships
    SELECT * FROM key_relationships
    UNION ALL
    SELECT * FROM additional_relationships
    """
    
    session.sql(create_relationships_sql).collect()
    
    logger.info(f"Generated {scale_config['entity_relationships']} entity relationships using pure SQL")


def generate_customers(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate customer profiles linked to entities using pure SQL."""
    logger.info("Generating customers (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    key_entities = config.KEY_ENTITIES
    
    # Get key entity IDs
    key_entity_ids = [spec['entity_id'] for spec in key_entities.values()]
    key_entity_ids_sql = "'" + "','".join(key_entity_ids) + "'"
    
    additional_count = scale_config['customers'] - 3  # 3 key customers
    
    # Build complete SQL using CTEs for clarity
    create_customers_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS AS
    WITH
    -- Key customers with specific characteristics
    key_customers AS (
        SELECT 
            'CUST_GTV_SA_001' AS CUSTOMER_ID,
            'GTV_SA_001' AS ENTITY_ID,
            'CORPORATE' AS CUSTOMER_TYPE,
            DATEADD(year, -4, CURRENT_DATE()) AS ONBOARDING_DATE,
            'HIGH' AS RISK_RATING,
            'REQUIRES_EDD' AS KYC_STATUS,
            DATEADD(month, -3, CURRENT_DATE()) AS LAST_REVIEW_DATE,
            DATEADD(month, 3, CURRENT_DATE()) AS NEXT_REVIEW_DATE,
            6 AS REVIEW_FREQUENCY_MONTHS,
            'Sarah Mitchell' AS RELATIONSHIP_MANAGER,
            2 AS AML_FLAGS,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        UNION ALL
        SELECT 
            'CUST_INN_DE_001' AS CUSTOMER_ID,
            'INN_DE_001' AS ENTITY_ID,
            'CORPORATE' AS CUSTOMER_TYPE,
            DATEADD(year, -8, CURRENT_DATE()) AS ONBOARDING_DATE,
            'MEDIUM' AS RISK_RATING,
            'COMPLETE' AS KYC_STATUS,
            DATEADD(month, -6, CURRENT_DATE()) AS LAST_REVIEW_DATE,
            DATEADD(month, 6, CURRENT_DATE()) AS NEXT_REVIEW_DATE,
            12 AS REVIEW_FREQUENCY_MONTHS,
            'James Wilson' AS RELATIONSHIP_MANAGER,
            0 AS AML_FLAGS,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        UNION ALL
        SELECT 
            'CUST_NSC_UK_001' AS CUSTOMER_ID,
            'NSC_UK_001' AS ENTITY_ID,
            'CORPORATE' AS CUSTOMER_TYPE,
            DATEADD(year, -10, CURRENT_DATE()) AS ONBOARDING_DATE,
            'MEDIUM' AS RISK_RATING,
            'COMPLETE' AS KYC_STATUS,
            DATEADD(month, -4, CURRENT_DATE()) AS LAST_REVIEW_DATE,
            DATEADD(month, 8, CURRENT_DATE()) AS NEXT_REVIEW_DATE,
            12 AS REVIEW_FREQUENCY_MONTHS,
            'Michael Brown' AS RELATIONSHIP_MANAGER,
            0 AS AML_FLAGS,
            CURRENT_TIMESTAMP() AS CREATED_DATE
    ),
    -- Additional customers from entities
    additional_customers AS (
        SELECT 
            'CUST_' || ENTITY_ID AS CUSTOMER_ID,
            ENTITY_ID,
            'CORPORATE' AS CUSTOMER_TYPE,
            DATEADD(day, -UNIFORM(365, 1680, ROW_SEQ), CURRENT_DATE()) AS ONBOARDING_DATE,
            CASE UNIFORM(0, 4, ROW_SEQ + 1)
                WHEN 0 THEN 'LOW'
                WHEN 1 THEN 'LOW'
                WHEN 2 THEN 'MEDIUM'
                WHEN 3 THEN 'MEDIUM'
                ELSE 'HIGH'
            END AS RISK_RATING,
            CASE UNIFORM(0, 4, ROW_SEQ + 2)
                WHEN 0 THEN 'COMPLETE'
                WHEN 1 THEN 'COMPLETE'
                WHEN 2 THEN 'COMPLETE'
                WHEN 3 THEN 'PENDING'
                ELSE 'REQUIRES_EDD'
            END AS KYC_STATUS,
            DATEADD(day, -UNIFORM(30, 365, ROW_SEQ + 5), CURRENT_DATE()) AS LAST_REVIEW_DATE,
            CASE 
                WHEN UNIFORM(0, 4, ROW_SEQ + 1) IN (2, 3) AND MOD(ROW_SEQ, 3) < 2 
                THEN DATEADD(day, UNIFORM(1, 30, ROW_SEQ + 7), CURRENT_DATE())  -- 8 MEDIUM customers due soon
                ELSE DATEADD(month, 
                    CASE UNIFORM(0, 4, ROW_SEQ + 1)
                        WHEN 0 THEN 24  -- LOW
                        WHEN 1 THEN 24  -- LOW
                        WHEN 2 THEN 12  -- MEDIUM
                        WHEN 3 THEN 12  -- MEDIUM
                        ELSE 6  -- HIGH
                    END,
                    DATEADD(day, -UNIFORM(30, 365, ROW_SEQ + 5), CURRENT_DATE())
                )
            END AS NEXT_REVIEW_DATE,
            CASE UNIFORM(0, 4, ROW_SEQ + 1)
                WHEN 0 THEN 24  -- LOW
                WHEN 1 THEN 24  -- LOW
                WHEN 2 THEN 12  -- MEDIUM
                WHEN 3 THEN 12  -- MEDIUM
                ELSE 6  -- HIGH
            END AS REVIEW_FREQUENCY_MONTHS,
            CASE UNIFORM(0, 7, ROW_SEQ + 6)
                WHEN 0 THEN 'James Wilson'
                WHEN 1 THEN 'Sarah Mitchell'
                WHEN 2 THEN 'Michael Brown'
                WHEN 3 THEN 'Emma Thompson'
                WHEN 4 THEN 'David Chen'
                WHEN 5 THEN 'Lisa Anderson'
                WHEN 6 THEN 'Robert Garcia'
                ELSE 'Anna Mueller'
            END AS RELATIONSHIP_MANAGER,
            CASE 
                WHEN UNIFORM(0, 4, ROW_SEQ + 1) = 4 THEN UNIFORM(0, 3, ROW_SEQ + 3)  -- HIGH risk
                WHEN UNIFORM(0, 4, ROW_SEQ + 1) IN (2, 3) THEN UNIFORM(0, 1, ROW_SEQ + 4)  -- MEDIUM risk
                ELSE 0
            END AS AML_FLAGS,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        FROM (
            SELECT 
                ROW_NUMBER() OVER (ORDER BY RANDOM()) AS ROW_SEQ,
                *
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES
            WHERE ENTITY_TYPE = 'CORPORATE'
              AND ENTITY_ID NOT IN ({key_entity_ids_sql})
            ORDER BY RANDOM()
            LIMIT {additional_count}
        )
    )
    -- Combine key and additional customers
    SELECT * FROM key_customers
    UNION ALL
    SELECT * FROM additional_customers
    """
    
    session.sql(create_customers_sql).collect()
    
    logger.info(f"Generated {scale_config['customers']} customers using pure SQL")


def generate_transactions(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate transaction history for customers using pure SQL."""
    logger.info("Generating transactions (pure SQL)...")
    
    # Use pure SQL with cross join and GENERATOR
    create_transactions_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.TRANSACTIONS AS
    WITH
    -- Key transaction for GTV (€5M deposit for EDD scenario)
    key_transaction AS (
        SELECT 
            'TXN_CUST_GTV_SA_001_LARGE_001' AS TRANSACTION_ID,
            'CUST_GTV_SA_001' AS CUSTOMER_ID,
            DATEADD(day, -7, CURRENT_TIMESTAMP()) AS TRANSACTION_DATE,
            5000000.00 AS AMOUNT,
            'EUR' AS CURRENCY,
            'CREDIT' AS TRANSACTION_TYPE,
            'International Trade Finance Ltd' AS COUNTERPARTY_NAME,
            'CHE' AS COUNTERPARTY_COUNTRY,
            'Large trade settlement - source of funds verification required' AS DESCRIPTION,
            0.85 AS RISK_SCORE,
            TRUE AS SUSPICIOUS_ACTIVITY_FLAG,
            CURRENT_TIMESTAMP() AS CREATED_DATE
    ),
    -- Regular transactions via cross join
    regular_transactions AS (
        SELECT 
            'TXN_' || CUSTOMER_ID || '_' || LPAD(TXN_SEQ::STRING, 4, '0') AS TRANSACTION_ID,
            CUSTOMER_ID,
            DATEADD(day, -UNIFORM(1, 365, SEQ8()), CURRENT_TIMESTAMP()) AS TRANSACTION_DATE,
            UNIFORM(1000, 100000, SEQ8() + 1)::DECIMAL(18,2) AS AMOUNT,
            'EUR' AS CURRENCY,
            CASE UNIFORM(0, 2, SEQ8() + 2)
                WHEN 0 THEN 'CREDIT'
                WHEN 1 THEN 'DEBIT'
                ELSE 'TRANSFER'
            END AS TRANSACTION_TYPE,
            CASE UNIFORM(0, 4, SEQ8() + 3)
                WHEN 0 THEN 'European Trading Co'
                WHEN 1 THEN 'Nordic Logistics Ltd'
                WHEN 2 THEN 'Baltic Import/Export'
                WHEN 3 THEN 'Swiss Finance AG'
                ELSE 'Amsterdam Trade House'
            END AS COUNTERPARTY_NAME,
            CASE UNIFORM(0, 5, SEQ8() + 4)
                WHEN 0 THEN 'DEU'
                WHEN 1 THEN 'FRA'
                WHEN 2 THEN 'NLD'
                WHEN 3 THEN 'BEL'
                WHEN 4 THEN 'CHE'
                ELSE 'AUT'
            END AS COUNTERPARTY_COUNTRY,
            CASE UNIFORM(0, 4, SEQ8() + 5)
                WHEN 0 THEN 'Trade settlement'
                WHEN 1 THEN 'Service payment'
                WHEN 2 THEN 'Equipment purchase'
                WHEN 3 THEN 'Consulting fees'
                ELSE 'Supply chain payment'
            END AS DESCRIPTION,
            CASE 
                WHEN RISK_RATING = 'HIGH' THEN UNIFORM(10, 80, SEQ8() + 6) / 100.0
                ELSE UNIFORM(10, 40, SEQ8() + 7) / 100.0
            END AS RISK_SCORE,
            (UNIFORM(0, 100, SEQ8() + 8) < 5) AS SUSPICIOUS_ACTIVITY_FLAG,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        FROM (
            SELECT 
                CUSTOMER_ID,
                RISK_RATING,
                TXN_SEQ
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS
            CROSS JOIN (
                SELECT ROW_NUMBER() OVER (ORDER BY SEQ8()) AS TXN_SEQ
                FROM TABLE(GENERATOR(ROWCOUNT => 100))  -- Max transactions per customer
            )
            WHERE (RISK_RATING = 'HIGH' AND TXN_SEQ <= 100)
               OR (RISK_RATING = 'MEDIUM' AND TXN_SEQ <= 60)
               OR (RISK_RATING = 'LOW' AND TXN_SEQ <= 30)
        )
    )
    -- Combine key and regular transactions
    SELECT * FROM key_transaction
    UNION ALL
    SELECT * FROM regular_transactions
    """
    
    session.sql(create_transactions_sql).collect()
    
    logger.info(f"Generated transactions using pure SQL")


def generate_loan_applications(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate loan applications with realistic financial metrics using pure SQL."""
    logger.info("Generating loan applications (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    additional_count = scale_config['loan_applications'] - 1
    
    create_loan_applications_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.LOAN_APPLICATIONS AS
    WITH
    -- Key application for Innovate GmbH (credit risk scenario)
    key_application AS (
        SELECT 
            'APP_INN_DE_001' AS APPLICATION_ID,
            'CUST_INN_DE_001' AS CUSTOMER_ID,
            'INN_DE_001' AS ENTITY_ID,
            8500000.00 AS REQUESTED_AMOUNT,
            DATEADD(month, -2, CURRENT_DATE()) AS APPLICATION_DATE,
            'UNDER_REVIEW' AS APPLICATION_STATUS,
            1.15 AS DSCR,
            3.2 AS DEBT_TO_EQUITY,
            1.18 AS CURRENT_RATIO,
            0.72 AS CLIENT_CONCENTRATION,
            'Software Services' AS INDUSTRY,
            'MEDIUM' AS RISK_RATING,
            CURRENT_TIMESTAMP() AS CREATED_DATE
    ),
    -- Additional applications from customers
    additional_applications AS (
        SELECT 
            'APP_' || ENTITY_ID AS APPLICATION_ID,
            CUSTOMER_ID,
            ENTITY_ID,
            UNIFORM(500000, 10000000, ROW_SEQ)::DECIMAL(18,2) AS REQUESTED_AMOUNT,
            DATEADD(day, -UNIFORM(1, 180, ROW_SEQ + 1), CURRENT_DATE()) AS APPLICATION_DATE,
            CASE UNIFORM(0, 3, ROW_SEQ + 2)
                WHEN 0 THEN 'PENDING'
                WHEN 1 THEN 'UNDER_REVIEW'
                WHEN 2 THEN 'APPROVED'
                ELSE 'REJECTED'
            END AS APPLICATION_STATUS,
            UNIFORM(80, 300, ROW_SEQ + 3) / 100.0 AS DSCR,
            UNIFORM(50, 500, ROW_SEQ + 4) / 100.0 AS DEBT_TO_EQUITY,
            UNIFORM(80, 250, ROW_SEQ + 5) / 100.0 AS CURRENT_RATIO,
            UNIFORM(10, 80, ROW_SEQ + 6) / 100.0 AS CLIENT_CONCENTRATION,
            CASE UNIFORM(0, 6, ROW_SEQ + 7)
                WHEN 0 THEN 'Software Services'
                WHEN 1 THEN 'Manufacturing'
                WHEN 2 THEN 'Retail'
                WHEN 3 THEN 'Healthcare'
                WHEN 4 THEN 'Construction'
                WHEN 5 THEN 'Transportation'
                ELSE 'Financial Services'
            END AS INDUSTRY,
            CASE 
                WHEN (UNIFORM(80, 300, ROW_SEQ + 3) / 100.0) < 1.25 THEN 'HIGH'
                WHEN (UNIFORM(50, 500, ROW_SEQ + 4) / 100.0) > 3.0 THEN 'HIGH'
                WHEN (UNIFORM(80, 300, ROW_SEQ + 3) / 100.0) > 2.0 THEN 'LOW'
                ELSE 'MEDIUM'
            END AS RISK_RATING,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        FROM (
            SELECT 
                ROW_NUMBER() OVER (ORDER BY RANDOM()) AS ROW_SEQ,
                CUSTOMER_ID,
                ENTITY_ID
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS
            WHERE ENTITY_ID != 'INN_DE_001'
            ORDER BY RANDOM()
            LIMIT {additional_count}
        )
    )
    -- Combine key and additional applications
    SELECT * FROM key_application
    UNION ALL
    SELECT * FROM additional_applications
    """
    
    session.sql(create_loan_applications_sql).collect()
    
    logger.info(f"Generated {scale_config['loan_applications']} loan applications using pure SQL")


def generate_historical_loans(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate historical loan performance data for cohort analysis using pure SQL."""
    logger.info("Generating historical loans (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    
    create_historical_loans_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.HISTORICAL_LOANS AS
    SELECT 
        'HIST_LOAN_' || SUBSTR(UUID_STRING(), 1, 8) AS LOAN_ID,
        NULL AS CUSTOMER_ID,
        CASE UNIFORM(0, 4, ROW_SEQ)
            WHEN 0 THEN 'Tech'
            WHEN 1 THEN 'Euro'
            WHEN 2 THEN 'Nordic'
            WHEN 3 THEN 'Baltic'
            ELSE 'Global'
        END || ' ' ||
        CASE UNIFORM(0, 4, ROW_SEQ + 1)
            WHEN 0 THEN 'Solutions'
            WHEN 1 THEN 'Industries'
            WHEN 2 THEN 'Holdings'
            WHEN 3 THEN 'Services'
            ELSE 'Group'
        END || ' ' ||
        CASE UNIFORM(0, 3, ROW_SEQ + 2)
            WHEN 0 THEN 'Ltd'
            WHEN 1 THEN 'S.A.'
            WHEN 2 THEN 'GmbH'
            ELSE 'B.V.'
        END AS APPLICANT_NAME,
        TO_DATE(
            UNIFORM(2019, 2023, ROW_SEQ + 3)::STRING || '-' ||
            LPAD(UNIFORM(1, 12, ROW_SEQ + 4)::STRING, 2, '0') || '-' ||
            LPAD(UNIFORM(1, 28, ROW_SEQ + 5)::STRING, 2, '0')
        ) AS ORIGINATION_DATE,
        DATEADD(day, UNIFORM(1095, 2190, ROW_SEQ + 6), 
            TO_DATE(
                UNIFORM(2019, 2023, ROW_SEQ + 3)::STRING || '-' ||
                LPAD(UNIFORM(1, 12, ROW_SEQ + 4)::STRING, 2, '0') || '-' ||
                LPAD(UNIFORM(1, 28, ROW_SEQ + 5)::STRING, 2, '0')
            )
        ) AS MATURITY_DATE,
        UNIFORM(500000, 20000000, ROW_SEQ + 7)::DECIMAL(18,2) AS ORIGINAL_AMOUNT,
        'EUR' AS CURRENCY,
        CASE UNIFORM(0, 5, ROW_SEQ + 8)
            WHEN 0 THEN 'Software Services'
            WHEN 1 THEN 'Manufacturing'
            WHEN 2 THEN 'Healthcare'
            WHEN 3 THEN 'Financial Services'
            WHEN 4 THEN 'Retail'
            ELSE 'Construction'
        END AS INDUSTRY_SECTOR,
        UNIFORM(100, 500, ROW_SEQ + 9) / 100.0 AS DEBT_TO_EQUITY_AT_ORIGINATION,
        UNIFORM(80, 250, ROW_SEQ + 10) / 100.0 AS DSCR_AT_ORIGINATION,
        UNIFORM(80, 200, ROW_SEQ + 11) / 100.0 AS CURRENT_RATIO_AT_ORIGINATION,
        UNIFORM(15, 85, ROW_SEQ + 12) / 1.0 AS CLIENT_CONCENTRATION_AT_ORIGINATION,
        CASE MOD(UNIFORM(0, 3, ROW_SEQ + 13), 4)
            WHEN 0 THEN 'PERFORMING'
            WHEN 1 THEN 'PERFORMING'
            WHEN 2 THEN 'PERFORMING'
            ELSE 'DEFAULTED'
        END AS LOAN_STATUS,
        CASE 
            WHEN MOD(UNIFORM(0, 3, ROW_SEQ + 13), 4) = 3 THEN
                DATEADD(day, UNIFORM(365, 1460, ROW_SEQ + 14),
                    TO_DATE(
                        UNIFORM(2019, 2023, ROW_SEQ + 3)::STRING || '-' ||
                        LPAD(UNIFORM(1, 12, ROW_SEQ + 4)::STRING, 2, '0') || '-' ||
                        LPAD(UNIFORM(1, 28, ROW_SEQ + 5)::STRING, 2, '0')
                    )
                )
            ELSE NULL
        END AS DEFAULT_DATE,
        CASE 
            WHEN MOD(UNIFORM(0, 3, ROW_SEQ + 13), 4) = 3 THEN
                (UNIFORM(500000, 20000000, ROW_SEQ + 7) * UNIFORM(20, 80, ROW_SEQ + 15) / 100.0)::DECIMAL(18,2)
            ELSE NULL
        END AS LOSS_AMOUNT,
        CURRENT_TIMESTAMP() AS CREATED_DATE
    FROM (
        SELECT ROW_NUMBER() OVER (ORDER BY SEQ4()) AS ROW_SEQ
        FROM TABLE(GENERATOR(ROWCOUNT => {scale_config['historical_loans']}))
    )
    """
    
    session.sql(create_historical_loans_sql).collect()
    
    logger.info(f"Generated {scale_config['historical_loans']} historical loans using pure SQL")


def generate_alerts(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate transaction monitoring alerts for AML investigation scenarios using pure SQL."""
    logger.info("Generating alerts (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    additional_count = scale_config['alerts'] - 1
    
    create_alerts_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.ALERTS AS
    WITH
    -- Key structuring alert for demo scenario (GTV)
    key_alert AS (
        SELECT 
            'ALERT_STRUCT_001' AS ALERT_ID,
            'CUST_GTV_SA_001' AS CUSTOMER_ID,
            'Structuring' AS ALERT_TYPE,
            DATEADD(day, -1, CURRENT_TIMESTAMP()) AS ALERT_DATE,
            'OPEN' AS ALERT_STATUS,
            0.95 AS PRIORITY_SCORE,
            'Maria Santos' AS ASSIGNED_TO,
            NULL AS RESOLUTION_DATE,
            NULL AS DISPOSITION,
            '5 cash deposits of $9,500 each across 5 branches over 2-day period' AS ALERT_DESCRIPTION,
            5 AS FLAGGED_TRANSACTION_COUNT,
            47500.00 AS TOTAL_FLAGGED_AMOUNT,
            CURRENT_TIMESTAMP() AS CREATED_DATE
    ),
    -- Additional alerts from customers
    additional_alerts AS (
        SELECT 
            'ALERT_' || SUBSTR(UUID_STRING(), 1, 8) AS ALERT_ID,
            CUSTOMER_ID,
            CASE UNIFORM(0, 4, ROW_SEQ)
                WHEN 0 THEN 'Structuring'
                WHEN 1 THEN 'Large Cash'
                WHEN 2 THEN 'Rapid Movement'
                WHEN 3 THEN 'High Risk Country'
                ELSE 'Unusual Pattern'
            END AS ALERT_TYPE,
            DATEADD(day, -UNIFORM(1, 180, ROW_SEQ + 1), CURRENT_TIMESTAMP()) AS ALERT_DATE,
            CASE UNIFORM(0, 2, ROW_SEQ + 2)
                WHEN 0 THEN 'OPEN'
                WHEN 1 THEN 'UNDER_INVESTIGATION'
                ELSE 'CLOSED'
            END AS ALERT_STATUS,
            CASE 
                WHEN RISK_RATING = 'HIGH' THEN UNIFORM(70, 95, ROW_SEQ + 3) / 100.0
                WHEN RISK_RATING = 'MEDIUM' THEN UNIFORM(40, 70, ROW_SEQ + 4) / 100.0
                ELSE UNIFORM(10, 40, ROW_SEQ + 5) / 100.0
            END AS PRIORITY_SCORE,
            CASE UNIFORM(0, 4, ROW_SEQ + 6)
                WHEN 0 THEN 'Maria Santos'
                WHEN 1 THEN 'John Chen'
                WHEN 2 THEN 'Sarah Mitchell'
                WHEN 3 THEN 'David Kumar'
                ELSE 'Emma Rodriguez'
            END AS ASSIGNED_TO,
            CASE 
                WHEN UNIFORM(0, 2, ROW_SEQ + 2) = 2 THEN 
                    DATEADD(day, UNIFORM(1, 30, ROW_SEQ + 7), 
                        DATEADD(day, -UNIFORM(1, 180, ROW_SEQ + 1), CURRENT_TIMESTAMP()))
                ELSE NULL
            END AS RESOLUTION_DATE,
            CASE 
                WHEN UNIFORM(0, 2, ROW_SEQ + 2) = 2 THEN 
                    CASE UNIFORM(0, 2, ROW_SEQ + 8)
                        WHEN 0 THEN 'SAR_FILED'
                        WHEN 1 THEN 'FALSE_POSITIVE'
                        ELSE 'CLEARED'
                    END
                ELSE NULL
            END AS DISPOSITION,
            CASE UNIFORM(0, 4, ROW_SEQ)
                WHEN 0 THEN 'Structuring'
                WHEN 1 THEN 'Large Cash'
                WHEN 2 THEN 'Rapid Movement'
                WHEN 3 THEN 'High Risk Country'
                ELSE 'Unusual Pattern'
            END || ' pattern detected' AS ALERT_DESCRIPTION,
            UNIFORM(1, 10, ROW_SEQ + 9) AS FLAGGED_TRANSACTION_COUNT,
            UNIFORM(10000, 500000, ROW_SEQ + 10)::DECIMAL(18,2) AS TOTAL_FLAGGED_AMOUNT,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        FROM (
            SELECT 
                ROW_NUMBER() OVER (ORDER BY RANDOM()) AS ROW_SEQ,
                CUSTOMER_ID,
                RISK_RATING
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS
            ORDER BY RANDOM()
            LIMIT {additional_count}
        )
    )
    -- Combine key and additional alerts
    SELECT * FROM key_alert
    UNION ALL
    SELECT * FROM additional_alerts
    """
    
    session.sql(create_alerts_sql).collect()
    
    logger.info(f"Generated {scale_config['alerts']} transaction monitoring alerts using pure SQL")


def generate_alert_disposition_history(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate historical alert disposition data for ML model training using pure SQL."""
    logger.info("Generating alert disposition history (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    
    # Check if alerts table exists
    try:
        session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ALERTS").count()
    except Exception as e:
        logger.warning(f"No alerts table found. Skipping disposition history generation: {e}")
        return
    
    create_disposition_history_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.ALERT_DISPOSITION_HISTORY AS
    SELECT 
        UUID_STRING() AS DISPOSITION_ID,
        'HIST_ALERT_' || SUBSTR(UUID_STRING(), 1, 8) AS ALERT_ID,
        CASE 
            WHEN RAND_VAL < 75 THEN 'FALSE_POSITIVE'
            WHEN RAND_VAL < 95 THEN 'CLEARED'
            ELSE 'SAR_FILED'
        END AS FINAL_DISPOSITION,
        CASE 
            WHEN RAND_VAL < 75 THEN 'Transaction pattern consistent with normal business activity. No suspicious indicators found.'
            WHEN RAND_VAL < 95 THEN 'Customer provided satisfactory documentation. Activity verified as legitimate.'
            ELSE 'Suspicious activity identified. SAR filed with FinCEN/relevant authority.'
        END AS INVESTIGATION_NOTES,
        CASE UNIFORM(0, 4, ROW_SEQ + 1)
            WHEN 0 THEN 'Maria Santos'
            WHEN 1 THEN 'John Chen'
            WHEN 2 THEN 'Sarah Mitchell'
            WHEN 3 THEN 'David Kumar'
            ELSE 'Emma Rodriguez'
        END AS ANALYST_NAME,
        UNIFORM(50, 800, ROW_SEQ + 2) / 100.0 AS INVESTIGATION_HOURS,
        DATEADD(day, -UNIFORM(30, 730, ROW_SEQ + 3), CURRENT_TIMESTAMP()) AS CLOSED_DATE,
        CURRENT_TIMESTAMP() AS CREATED_DATE
    FROM (
        SELECT 
            ROW_NUMBER() OVER (ORDER BY SEQ4()) AS ROW_SEQ,
            UNIFORM(0, 100, SEQ4()) AS RAND_VAL
        FROM TABLE(GENERATOR(ROWCOUNT => {scale_config['alert_disposition_history']}))
    )
    """
    
    session.sql(create_disposition_history_sql).collect()
    
    logger.info(f"Generated {scale_config['alert_disposition_history']} historical alert dispositions (75% false positive rate) using pure SQL")


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
        financials_df.create_or_replace_temp_view("temp_sp_financials")
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.SP_GLOBAL_COMPANY_FINANCIALS
            AS SELECT * FROM temp_sp_financials
        """).collect()


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
# COMMERCIAL & WEALTH DATA GENERATION FUNCTIONS
# =============================================================================

def generate_client_crm(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate client CRM records for relationship manager scenario using pure SQL."""
    logger.info("Generating client CRM records (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('client_crm_records', 0)
    
    if target_count == 0:
        logger.info("Skipping client CRM generation (not in scale config)")
        return
    
    # Check if primary RM client exists
    primary_rm_client = config.KEY_ENTITIES.get('primary_rm_client')
    
    if primary_rm_client:
        key_crm_union = f"""
            SELECT 
                'CRM_00001' AS CRM_ID,
                '{primary_rm_client['entity_id']}' AS CUSTOMER_ID,
                '{primary_rm_client['relationship_manager']}' AS RELATIONSHIP_MANAGER,
                DATEADD(day, -UNIFORM(1, 60, RANDOM()), CURRENT_DATE()) AS LAST_CONTACT_DATE,
                '{primary_rm_client['account_status']}' AS ACCOUNT_STATUS,
                'PREMIUM' AS ACCOUNT_TIER,
                'Strategic account. Multiple cross-sell opportunities identified.' AS NOTES_SUMMARY,
                3 AS RISK_OPPORTUNITIES_COUNT,
                CURRENT_TIMESTAMP() AS CREATED_DATE
        """
        additional_count = target_count - 1
    else:
        key_crm_union = ""
        additional_count = target_count
    
    create_crm_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM AS
    WITH
    {"key_crm AS (" + key_crm_union + ")," if key_crm_union else ""}
    -- Additional CRM records
    additional_crm AS (
        SELECT 
            'CRM_' || LPAD(ROW_SEQ::STRING, 5, '0') AS CRM_ID,
            CUSTOMER_ID,
            CASE UNIFORM(0, 9, ROW_SEQ)
                WHEN 0 THEN 'Claire Dubois'
                WHEN 1 THEN 'Marcus Weber'
                WHEN 2 THEN 'Sofia Rossi'
                WHEN 3 THEN 'Hans Schmidt'
                WHEN 4 THEN 'Emma Johnson'
                WHEN 5 THEN 'Pierre Lefebvre'
                WHEN 6 THEN 'Anna Müller'
                WHEN 7 THEN 'Giovanni Bianchi'
                WHEN 8 THEN 'Laura Martinez'
                ELSE 'Thomas Anderson'
            END AS RELATIONSHIP_MANAGER,
            DATEADD(day, -UNIFORM(1, 60, ROW_SEQ + 1), CURRENT_DATE()) AS LAST_CONTACT_DATE,
            CASE MOD(UNIFORM(0, 9, ROW_SEQ + 2), 10)
                WHEN 0 THEN 'ACTIVE' WHEN 1 THEN 'ACTIVE' WHEN 2 THEN 'ACTIVE'
                WHEN 3 THEN 'ACTIVE' WHEN 4 THEN 'ACTIVE' WHEN 5 THEN 'ACTIVE'
                WHEN 6 THEN 'ACTIVE' WHEN 7 THEN 'PROSPECT' WHEN 8 THEN 'PROSPECT'
                ELSE 'INACTIVE'
            END AS ACCOUNT_STATUS,
            CASE MOD(UNIFORM(0, 9, ROW_SEQ + 3), 10)
                WHEN 0 THEN 'PREMIUM' WHEN 1 THEN 'PREMIUM'
                WHEN 2 THEN 'STANDARD' WHEN 3 THEN 'STANDARD' WHEN 4 THEN 'STANDARD'
                WHEN 5 THEN 'STANDARD' WHEN 6 THEN 'STANDARD'
                WHEN 7 THEN 'BASIC' WHEN 8 THEN 'BASIC'
                ELSE 'BASIC'
            END AS ACCOUNT_TIER,
            UNIFORM(0, 4, ROW_SEQ + 4) AS RISK_OPPORTUNITIES_COUNT,
            'Last contact: ' || TO_CHAR(DATEADD(day, -UNIFORM(1, 60, ROW_SEQ + 1), CURRENT_DATE()), 'YYYY-MM-DD') || 
            '. Account tier: ' || 
            CASE MOD(UNIFORM(0, 9, ROW_SEQ + 3), 10)
                WHEN 0 THEN 'PREMIUM' WHEN 1 THEN 'PREMIUM'
                WHEN 2 THEN 'STANDARD' WHEN 3 THEN 'STANDARD' WHEN 4 THEN 'STANDARD'
                WHEN 5 THEN 'STANDARD' WHEN 6 THEN 'STANDARD'
                WHEN 7 THEN 'BASIC' WHEN 8 THEN 'BASIC'
                ELSE 'BASIC'
            END || '. ' || 
            UNIFORM(0, 4, ROW_SEQ + 4)::STRING || ' opportunities identified.' AS NOTES_SUMMARY,
            CURRENT_TIMESTAMP() AS CREATED_DATE
        FROM (
            SELECT 
                ROW_NUMBER() OVER (ORDER BY RANDOM()) + {1 if primary_rm_client else 0} AS ROW_SEQ,
                CUSTOMER_ID
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS
            ORDER BY RANDOM()
            LIMIT {additional_count}
        )
    )
    -- Combine
    {"SELECT * FROM key_crm UNION ALL BY NAME" if key_crm_union else ""}
    SELECT * FROM additional_crm
    """
    
    session.sql(create_crm_sql).collect()
    
    logger.info(f"Generated {target_count} client CRM records using pure SQL")


def generate_client_opportunities(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate client opportunities for relationship manager scenario using pure SQL."""
    logger.info("Generating client opportunities (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('client_opportunities', 0)
    
    if target_count == 0:
        logger.info("Skipping client opportunities generation (not in scale config)")
        return
    
    # Check if CRM table exists
    try:
        session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM").count()
    except:
        logger.warning("No CRM records found, skipping opportunities generation")
        return
    
    create_opportunities_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.CURATED.CLIENT_OPPORTUNITIES AS
    SELECT 
        'OPP_' || LPAD(ROW_SEQ::STRING, 6, '0') AS OPPORTUNITY_ID,
        CUSTOMER_ID,
        CASE UNIFORM(0, 6, ROW_SEQ)
            WHEN 0 THEN 'CROSS_SELL'
            WHEN 1 THEN 'UPSELL'
            WHEN 2 THEN 'RISK_MITIGATION'
            WHEN 3 THEN 'NEW_PRODUCT'
            WHEN 4 THEN 'INVESTMENT_ADVISORY'
            WHEN 5 THEN 'TRADE_FINANCE'
            ELSE 'FX_HEDGING'
        END AS OPPORTUNITY_TYPE,
        CASE UNIFORM(0, 6, ROW_SEQ)
            WHEN 0 THEN 'Cross-sell FX hedging products to protect against currency fluctuation'
            WHEN 1 THEN 'Upsell to premium banking tier for expanded trade finance limits'
            WHEN 2 THEN 'Address concentration risk through supplier diversification advisory'
            WHEN 3 THEN 'Introduce sustainable finance solutions aligned with ESG goals'
            WHEN 4 THEN 'Offer treasury optimization services for excess cash management'
            WHEN 5 THEN 'Expand documentary credit facilities for international expansion'
            ELSE 'Implement forward contracts to hedge EUR/USD exposure'
        END AS OPPORTUNITY_DESCRIPTION,
        CASE UNIFORM(0, 5, ROW_SEQ + 1)
            WHEN 0 THEN 50000
            WHEN 1 THEN 100000
            WHEN 2 THEN 250000
            WHEN 3 THEN 500000
            WHEN 4 THEN 1000000
            ELSE 2500000
        END::DECIMAL(18,2) AS POTENTIAL_VALUE,
        CASE UNIFORM(0, 4, ROW_SEQ + 2)
            WHEN 0 THEN 'call_note'
            WHEN 1 THEN 'internal_email'
            WHEN 2 THEN 'news'
            WHEN 3 THEN 'transaction_pattern'
            ELSE 'market_intelligence'
        END AS SOURCE_TYPE,
        'DOC_' || UNIFORM(1000, 9999, ROW_SEQ + 3)::STRING AS SOURCE_DOCUMENT_ID,
        CASE MOD(UNIFORM(0, 9, ROW_SEQ + 4), 10)
            WHEN 0 THEN 'HIGH' WHEN 1 THEN 'HIGH'
            WHEN 2 THEN 'MEDIUM' WHEN 3 THEN 'MEDIUM' WHEN 4 THEN 'MEDIUM'
            WHEN 5 THEN 'MEDIUM' WHEN 6 THEN 'MEDIUM'
            WHEN 7 THEN 'LOW' WHEN 8 THEN 'LOW'
            ELSE 'LOW'
        END AS PRIORITY,
        CASE MOD(UNIFORM(0, 9, ROW_SEQ + 5), 10)
            WHEN 0 THEN 'OPEN' WHEN 1 THEN 'OPEN' WHEN 2 THEN 'OPEN' WHEN 3 THEN 'OPEN'
            WHEN 4 THEN 'IN_PROGRESS' WHEN 5 THEN 'IN_PROGRESS' WHEN 6 THEN 'IN_PROGRESS'
            WHEN 7 THEN 'CLOSED_WON' WHEN 8 THEN 'CLOSED_WON'
            ELSE 'CLOSED_LOST'
        END AS STATUS,
        DATEADD(day, -UNIFORM(1, 90, ROW_SEQ + 6), CURRENT_TIMESTAMP()) AS CREATED_DATE,
        DATEADD(day, -UNIFORM(0, 30, ROW_SEQ + 7), CURRENT_TIMESTAMP()) AS LAST_UPDATED_DATE
    FROM (
        SELECT 
            ROW_NUMBER() OVER (ORDER BY RANDOM()) AS ROW_SEQ,
            CUSTOMER_ID
        FROM {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM
        ORDER BY RANDOM()
        LIMIT {target_count}
    )
    """
    
    session.sql(create_opportunities_sql).collect()
    
    logger.info(f"Generated {target_count} client opportunities using pure SQL")


def generate_model_portfolios(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate model portfolios for wealth advisor scenario using pure SQL."""
    logger.info("Generating model portfolios (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    portfolio_count = scale_config.get('model_portfolios', 3)
    
    if portfolio_count == 0:
        logger.info("Skipping model portfolios generation (not in scale config)")
        return
    
    # Define all 5 model portfolios as pure SQL
    all_models_sql = """
        SELECT 
            'MODEL_CONSERVATIVE' AS MODEL_ID,
            'Conservative Growth' AS MODEL_NAME,
            'LOW' AS RISK_PROFILE,
            30.0 AS TARGET_EQUITY_PCT,
            60.0 AS TARGET_BOND_PCT,
            5.0 AS TARGET_ALTERNATIVE_PCT,
            5.0 AS TARGET_CASH_PCT,
            4.5 AS EXPECTED_ANNUAL_RETURN_PCT,
            6.0 AS EXPECTED_VOLATILITY_PCT,
            'Capital preservation with modest growth. Suitable for risk-averse investors.' AS DESCRIPTION,
            180 AS REBALANCE_FREQUENCY_DAYS,
            DATEADD(day, -UNIFORM(365, 730, SEQ4()), CURRENT_TIMESTAMP()) AS CREATED_DATE
        UNION ALL
        SELECT 
            'MODEL_BALANCED', 'Balanced Portfolio', 'MODERATE',
            50.0, 40.0, 7.0, 3.0, 6.5, 10.0,
            'Balanced growth and income with moderate risk. Suitable for long-term investors.',
            180, DATEADD(day, -UNIFORM(365, 730, SEQ4() + 1), CURRENT_TIMESTAMP())
        UNION ALL
        SELECT 
            'MODEL_GROWTH', 'Growth Portfolio', 'MODERATE',
            70.0, 20.0, 8.0, 2.0, 8.5, 14.0,
            'Long-term capital appreciation with higher volatility tolerance.',
            90, DATEADD(day, -UNIFORM(365, 730, SEQ4() + 2), CURRENT_TIMESTAMP())
        UNION ALL
        SELECT 
            'MODEL_AGGRESSIVE', 'Aggressive Growth', 'HIGH',
            85.0, 5.0, 10.0, 0.0, 10.5, 18.0,
            'Maximum growth potential for high risk tolerance and long time horizons.',
            90, DATEADD(day, -UNIFORM(365, 730, SEQ4() + 3), CURRENT_TIMESTAMP())
        UNION ALL
        SELECT 
            'MODEL_INCOME', 'Income Portfolio', 'LOW',
            25.0, 65.0, 5.0, 5.0, 4.0, 5.0,
            'Focus on income generation with low volatility. Suitable for retirees.',
            365, DATEADD(day, -UNIFORM(365, 730, SEQ4() + 4), CURRENT_TIMESTAMP())
    """
    
    # Select only the requested number of models
    portfolios_df = session.sql(all_models_sql).limit(portfolio_count)
    
    # Save to database using SQL to avoid quoted identifiers
    portfolios_df.create_or_replace_temp_view("temp_model_portfolios")
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.CURATED.MODEL_PORTFOLIOS
        AS SELECT * FROM temp_model_portfolios
    """).collect()
    
    logger.info(f"Generated {portfolio_count} model portfolios using server-side operations")


def generate_holdings(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate investment holdings for wealth clients using pure SQL."""
    logger.info("Generating holdings (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    total_holdings = scale_config.get('holdings', 0)
    wealth_client_count = scale_config.get('wealth_clients', 0)
    
    if total_holdings == 0 or wealth_client_count == 0:
        logger.info("Skipping holdings generation (not in scale config)")
        return
    
    holdings_per_client = total_holdings // wealth_client_count if wealth_client_count > 0 else 0
    
    create_holdings_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.CURATED.HOLDINGS AS
    WITH
    -- Sample wealth clients from customers
    wealth_clients AS (
        SELECT CUSTOMER_ID
        FROM {config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS
        ORDER BY RANDOM()
        LIMIT {wealth_client_count}
    ),
    -- Generate holdings via cross join
    holdings_with_values AS (
        SELECT 
            'HOLD_' || LPAD(ROW_NUMBER() OVER (ORDER BY wc.CUSTOMER_ID, gen.HOLDING_SEQ)::STRING, 6, '0') AS HOLDING_ID,
            wc.CUSTOMER_ID,
            CASE MOD(UNIFORM(0, 9, gen.GLOBAL_SEQ), 10)
                WHEN 0 THEN 'EQUITY' WHEN 1 THEN 'EQUITY' WHEN 2 THEN 'EQUITY'
                WHEN 3 THEN 'EQUITY' WHEN 4 THEN 'EQUITY'
                WHEN 5 THEN 'BOND' WHEN 6 THEN 'BOND' WHEN 7 THEN 'BOND'
                WHEN 8 THEN 'ALTERNATIVE'
                ELSE 'CASH'
            END AS ASSET_TYPE,
            CASE UNIFORM(0, 8, gen.GLOBAL_SEQ + 1)
                WHEN 0 THEN 'DOMESTIC_EQUITY'
                WHEN 1 THEN 'INTL_EQUITY'
                WHEN 2 THEN 'EMERGING_MARKETS'
                WHEN 3 THEN 'GOVT_BOND'
                WHEN 4 THEN 'CORP_BOND'
                WHEN 5 THEN 'REAL_ESTATE'
                WHEN 6 THEN 'COMMODITIES'
                WHEN 7 THEN 'INFRASTRUCTURE'
                ELSE 'MONEY_MARKET'
            END AS ASSET_CLASS,
            CASE UNIFORM(0, 8, gen.GLOBAL_SEQ + 2)
                WHEN 0 THEN 'DAX 40 ETF'
                WHEN 1 THEN 'S&P 500 ETF'
                WHEN 2 THEN 'MSCI World ETF'
                WHEN 3 THEN 'MSCI EM ETF'
                WHEN 4 THEN 'German Government Bonds'
                WHEN 5 THEN 'EUR Corporate Bond ETF'
                WHEN 6 THEN 'European REIT ETF'
                WHEN 7 THEN 'Gold ETF'
                ELSE 'EUR Money Market Fund'
            END AS ASSET_NAME,
            CASE UNIFORM(0, 8, gen.GLOBAL_SEQ + 3)
                WHEN 0 THEN 'EXS1.DE'
                WHEN 1 THEN 'SPY'
                WHEN 2 THEN 'IWDA.AS'
                WHEN 3 THEN 'EEM'
                WHEN 4 THEN 'BUND'
                WHEN 5 THEN 'CORP.PA'
                WHEN 6 THEN 'IQQP.AS'
                WHEN 7 THEN 'GLD'
                ELSE 'MMF_EUR'
            END AS TICKER_SYMBOL,
            UNIFORM(100, 10000, gen.GLOBAL_SEQ + 4)::DECIMAL(18,2) AS QUANTITY,
            UNIFORM(50, 500, gen.GLOBAL_SEQ + 5)::DECIMAL(18,2) AS COST_BASIS_PER_UNIT,
            (UNIFORM(50, 500, gen.GLOBAL_SEQ + 5) * UNIFORM(80, 130, gen.GLOBAL_SEQ + 6) / 100.0)::DECIMAL(18,2) AS CURRENT_PRICE_PER_UNIT,
            CURRENT_DATE() AS AS_OF_DATE,
            CURRENT_TIMESTAMP() AS LAST_UPDATED_DATE
        FROM wealth_clients wc
        CROSS JOIN (
            SELECT 
                ROW_NUMBER() OVER (ORDER BY SEQ4()) AS HOLDING_SEQ,
                ROW_NUMBER() OVER (ORDER BY SEQ4()) AS GLOBAL_SEQ
            FROM TABLE(GENERATOR(ROWCOUNT => {holdings_per_client}))
        ) gen
    ),
    -- Calculate derived values and allocation percentages
    holdings_with_derived AS (
        SELECT 
            HOLDING_ID,
            CUSTOMER_ID,
            ASSET_TYPE,
            ASSET_CLASS,
            ASSET_NAME,
            TICKER_SYMBOL,
            QUANTITY,
            (QUANTITY * CURRENT_PRICE_PER_UNIT)::DECIMAL(18,2) AS CURRENT_VALUE,
            (QUANTITY * COST_BASIS_PER_UNIT)::DECIMAL(18,2) AS COST_BASIS,
            ((QUANTITY * CURRENT_PRICE_PER_UNIT) - (QUANTITY * COST_BASIS_PER_UNIT))::DECIMAL(18,2) AS UNREALIZED_GAIN_LOSS,
            AS_OF_DATE,
            LAST_UPDATED_DATE,
            SUM(QUANTITY * CURRENT_PRICE_PER_UNIT) OVER (PARTITION BY CUSTOMER_ID) AS TOTAL_VALUE_PER_CUSTOMER
        FROM holdings_with_values
    )
    -- Final selection with allocation percentage
    SELECT 
        HOLDING_ID,
        CUSTOMER_ID,
        ASSET_TYPE,
        ASSET_CLASS,
        ASSET_NAME,
        TICKER_SYMBOL,
        QUANTITY,
        CURRENT_VALUE,
        COST_BASIS,
        UNREALIZED_GAIN_LOSS,
        ((CURRENT_VALUE / TOTAL_VALUE_PER_CUSTOMER) * 100.0)::DECIMAL(5,2) AS ALLOCATION_PCT,
        AS_OF_DATE,
        LAST_UPDATED_DATE
    FROM holdings_with_derived
    """
    
    session.sql(create_holdings_sql).collect()
    
    logger.info(f"Generated {total_holdings} holdings for {wealth_client_count} wealth clients using pure SQL")


def generate_wealth_client_profiles(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate wealth client profiles linking customers to model portfolios using pure SQL."""
    logger.info("Generating wealth client profiles (pure SQL)...")
    
    scale_config = config.get_scale_config(scale)
    wealth_client_count = scale_config.get('wealth_clients', 0)
    
    if wealth_client_count == 0:
        logger.info("Skipping wealth client profiles generation (not in scale config)")
        return
    
    # Check if holdings and model portfolios exist
    try:
        session.table(f"{config.SNOWFLAKE['database']}.CURATED.HOLDINGS").count()
        session.table(f"{config.SNOWFLAKE['database']}.CURATED.MODEL_PORTFOLIOS").count()
    except:
        logger.warning("No holdings or model portfolios found, skipping wealth profiles generation")
        return
    
    create_wealth_profiles_sql = f"""
    CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.CURATED.WEALTH_CLIENT_PROFILES AS
    WITH
    -- Calculate total AUM per customer from holdings
    wealth_customers_aum AS (
        SELECT 
            CUSTOMER_ID,
            SUM(CURRENT_VALUE) AS TOTAL_AUM
        FROM {config.SNOWFLAKE['database']}.CURATED.HOLDINGS
        GROUP BY CUSTOMER_ID
    ),
    -- Assign profiles
    wealth_profiles AS (
        SELECT 
            'WCP_' || LPAD(ROW_NUMBER() OVER (ORDER BY CUSTOMER_ID)::STRING, 5, '0') AS PROFILE_ID,
            CUSTOMER_ID,
            CASE UNIFORM(0, 2, ROW_NUMBER() OVER (ORDER BY CUSTOMER_ID))
                WHEN 0 THEN 'CONSERVATIVE'
                WHEN 1 THEN 'MODERATE'
                ELSE 'AGGRESSIVE'
            END AS RISK_TOLERANCE,
            TOTAL_AUM,
            ROW_NUMBER() OVER (ORDER BY CUSTOMER_ID) AS ROW_SEQ
        FROM wealth_customers_aum
    )
    SELECT 
        PROFILE_ID,
        CUSTOMER_ID,
        CASE RISK_TOLERANCE
            WHEN 'CONSERVATIVE' THEN 'MODEL_CONSERVATIVE'
            WHEN 'AGGRESSIVE' THEN 'MODEL_AGGRESSIVE'
            ELSE 'MODEL_BALANCED'
        END AS MODEL_PORTFOLIO_ID,
        CASE UNIFORM(0, 4, ROW_SEQ + 1)
            WHEN 0 THEN 'Marcus Weber'
            WHEN 1 THEN 'Sofia Rossi'
            WHEN 2 THEN 'Jean-Pierre Dubois'
            WHEN 3 THEN 'Anna Müller'
            ELSE 'Laura Martinez'
        END AS WEALTH_ADVISOR,
        RISK_TOLERANCE,
        CASE UNIFORM(0, 2, ROW_SEQ + 2)
            WHEN 0 THEN 'STANDARD'
            WHEN 1 THEN 'TAX_DEFERRED'
            ELSE 'TAX_EXEMPT'
        END AS TAX_STATUS,
        CASE UNIFORM(0, 3, ROW_SEQ + 3)
            WHEN 0 THEN 'GROWTH'
            WHEN 1 THEN 'INCOME'
            WHEN 2 THEN 'PRESERVATION'
            ELSE 'BALANCED'
        END AS INVESTMENT_OBJECTIVES,
        TOTAL_AUM,
        70.0 AS CONCENTRATION_THRESHOLD_PCT,
        10.0 AS REBALANCE_TRIGGER_PCT,
        DATEADD(day, -UNIFORM(30, 180, ROW_SEQ + 4), CURRENT_DATE()) AS LAST_REBALANCE_DATE,
        DATEADD(day, UNIFORM(30, 90, ROW_SEQ + 5), CURRENT_DATE()) AS NEXT_REVIEW_DATE,
        DATEADD(day, -UNIFORM(365, 1095, ROW_SEQ + 6), CURRENT_TIMESTAMP()) AS CREATED_DATE,
        CURRENT_TIMESTAMP() AS LAST_UPDATED_DATE
    FROM wealth_profiles
    """
    
    session.sql(create_wealth_profiles_sql).collect()
    
    logger.info(f"Generated {wealth_client_count} wealth client profiles using pure SQL")


def main():
    """Main function for testing structured data generation."""
    print("Structured data generator module loaded successfully")
    print("Use generate_all_structured_data() method to create structured demo data")


if __name__ == "__main__":
    main()
