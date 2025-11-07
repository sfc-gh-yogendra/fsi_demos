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
from snowflake.snowpark import Session, Window
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
    """Generate entities with key demo entities guaranteed using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list, random_date_in_past, generate_id_from_prefix
    
    logger.info("Generating entities (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    key_entities = config.KEY_ENTITIES
    
    # Build SQL for key entities using UNION ALL
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
    
    key_entities_sql = " UNION ALL ".join(key_entity_selects)
    key_entities_df = session.sql(key_entities_sql)
    
    # Generate additional entities server-side
    additional_count = scale_config['entities'] - len(key_entities)
    
    if additional_count > 0:
        # Define lists for random selection
        countries = ['DEU', 'FRA', 'NLD', 'BEL', 'LUX', 'ITA', 'ESP', 'GBR']
        industries = [
            'Software Services', 'Manufacturing', 'Financial Services',
            'Healthcare', 'Retail', 'Construction', 'Energy', 'Transportation'
        ]
        esg_ratings = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D']
        statuses = ['ACTIVE', 'ACTIVE', 'ACTIVE', 'UNDER_REVIEW']  # Weighted toward ACTIVE
        
        prefixes = ['Euro', 'Global', 'Advanced', 'Innovative', 'Strategic', 'Dynamic', 'Premier']
        roots = ['Tech', 'Solutions', 'Systems', 'Industries', 'Services', 'Group', 'Holdings']
        suffixes = ['GmbH', 'S.A.', 'Ltd', 'B.V.', 'S.p.A.', 'AG']
        
        # Generate additional entities using generator
        additional_df = (
            session.generator(F.seq4(), rowcount=additional_count)
            .with_column("SEQ_NUM", F.row_number().over(Window.order_by(F.seq4())))
            .with_column(
                "ENTITY_ID",
                F.concat(
                    F.lit("ENT_"),
                    F.substr(F.call_builtin('UUID_STRING'), 1, 8)
                )
            )
            .with_column(
                "ENTITY_NAME",
                F.concat(
                    random_choice_from_list(prefixes, F.seq4()),
                    F.lit(" "),
                    random_choice_from_list(roots, F.seq4() + 1),
                    F.lit(" "),
                    random_choice_from_list(suffixes, F.seq4() + 2)
                )
            )
            .with_column("ENTITY_TYPE", F.lit("CORPORATE"))
            .with_column("COUNTRY_CODE", random_choice_from_list(countries, F.seq4() + 3))
            .with_column("INDUSTRY_SECTOR", random_choice_from_list(industries, F.seq4() + 4))
            .with_column(
                "INCORPORATION_DATE",
                F.dateadd("day", -F.uniform(1500, 5000, F.seq4() + 5), F.current_date())
            )
            .with_column("REGULATORY_STATUS", random_choice_from_list(statuses, F.seq4() + 6))
            .with_column("ESG_RATING", random_choice_from_list(esg_ratings, F.seq4() + 7))
            .with_column("CREATED_DATE", F.current_timestamp())
            .with_column("LAST_UPDATED", F.current_timestamp())
            .select(
                "ENTITY_ID", "ENTITY_NAME", "ENTITY_TYPE", "COUNTRY_CODE",
                "INDUSTRY_SECTOR", "INCORPORATION_DATE", "REGULATORY_STATUS",
                "ESG_RATING", "CREATED_DATE", "LAST_UPDATED"
            )
        )
        
        # Combine key entities with additional entities
        entities_df = key_entities_df.union_all(additional_df)
    else:
        entities_df = key_entities_df
    
    # Save to table
    entities_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES", 
        mode="overwrite"
    )
    
    logger.info(f"Generated {scale_config['entities']} entities ({len(key_entities)} key entities) using server-side operations")


def generate_entity_relationships(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate entity relationships for cross-domain intelligence using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list, random_date_in_past
    
    logger.info("Generating entity relationships (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    
    # Define key relationships and shell network as SQL
    shared_director_name = 'Anya Sharma'
    shared_address = '42 Mailbox Lane, Virtual Office Complex, Gibraltar'
    
    key_relationships_sql = f"""
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
    """
    
    key_relationships_df = session.sql(key_relationships_sql)
    key_count = 8  # 3 key relationships + 5 shell network relationships
    
    # Generate additional random relationships using self-join pattern
    additional_count = scale_config['entity_relationships'] - key_count
    
    if additional_count > 0:
        relationship_types = ['VENDOR', 'CUSTOMER', 'COMPETITOR', 'SUBSIDIARY']
        relationship_strengths = ['PRIMARY', 'SECONDARY', 'INDIRECT']
        director_names = ['John Smith', 'Maria Garcia', 'Hans Mueller', 'Sophie Dubois', 'Marco Rossi']
        
        # Create random relationships by sampling entities twice and joining
        entities_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES")
        
        additional_df = (
            session.generator(F.seq4(), rowcount=additional_count)
            .with_column("SEQ_NUM", F.row_number().over(Window.order_by(F.seq4())))
            .with_column("RAND_SEED_1", F.seq4())
            .with_column("RAND_SEED_2", F.seq4() + 1000000)
            .join(
                entities_df.select(
                    F.col("ENTITY_ID").alias("PRIMARY_ENTITY_ID")
                ).order_by(F.random()).limit(additional_count),
                on=(F.lit(1) == F.lit(1)),  # Cross join trick
                how="cross"
            )
            .with_column("ROW_NUM_PRIMARY", F.row_number().over(Window.partition_by("SEQ_NUM").order_by(F.random())))
            .filter(F.col("ROW_NUM_PRIMARY") == 1)
            .join(
                entities_df.select(
                    F.col("ENTITY_ID").alias("RELATED_ENTITY_ID")
                ).order_by(F.random()).limit(additional_count),
                on=(F.lit(1) == F.lit(1)),  # Cross join trick
                how="cross"
            )
            .with_column("ROW_NUM_RELATED", F.row_number().over(Window.partition_by("SEQ_NUM", "PRIMARY_ENTITY_ID").order_by(F.random())))
            .filter(F.col("ROW_NUM_RELATED") == 1)
            .filter(F.col("PRIMARY_ENTITY_ID") != F.col("RELATED_ENTITY_ID"))  # Avoid self-relationships
            .with_column("RELATIONSHIP_ID", F.call_builtin('UUID_STRING'))
            .with_column("RELATIONSHIP_TYPE", random_choice_from_list(relationship_types, F.col("RAND_SEED_1")))
            .with_column("RELATIONSHIP_STRENGTH", random_choice_from_list(relationship_strengths, F.col("RAND_SEED_1") + 1))
            .with_column("EFFECTIVE_DATE", F.dateadd("day", -F.uniform(365, 1095, F.col("RAND_SEED_1") + 2), F.current_date()))
            .with_column("END_DATE", F.lit(None).cast("date"))
            .with_column("RISK_IMPACT_SCORE", F.uniform(10, 90, F.col("RAND_SEED_1") + 3) / F.lit(100.0))
            .with_column("HAS_SHARED_CHARS", F.uniform(0, 100, F.col("RAND_SEED_1") + 4) < 10)  # 10% chance
            .with_column(
                "SHARED_DIRECTOR_NAME",
                F.when(F.col("HAS_SHARED_CHARS"), random_choice_from_list(director_names, F.col("RAND_SEED_1") + 5))
                 .otherwise(F.lit(None))
            )
            .with_column("SHARED_ADDRESS_FLAG", F.col("HAS_SHARED_CHARS"))
            .with_column(
                "SHARED_ADDRESS",
                F.when(F.col("HAS_SHARED_CHARS"), F.lit("Virtual Office, Business Center"))
                 .otherwise(F.lit(None))
            )
            .with_column(
                "INCORPORATION_PROXIMITY_DAYS",
                F.when(F.col("HAS_SHARED_CHARS"), F.uniform(1, 90, F.col("RAND_SEED_1") + 6))
                 .otherwise(F.lit(None).cast("int"))
            )
            .with_column("CREATED_DATE", F.current_timestamp())
            .select(
                "RELATIONSHIP_ID", "PRIMARY_ENTITY_ID", "RELATED_ENTITY_ID",
                "RELATIONSHIP_TYPE", "RELATIONSHIP_STRENGTH", "EFFECTIVE_DATE",
                "END_DATE", "RISK_IMPACT_SCORE", "SHARED_DIRECTOR_NAME",
                "SHARED_ADDRESS_FLAG", "SHARED_ADDRESS", "INCORPORATION_PROXIMITY_DAYS",
                "CREATED_DATE"
            )
        )
        
        # Combine key relationships with additional random ones
        relationships_df = key_relationships_df.union_all(additional_df)
    else:
        relationships_df = key_relationships_df
    
    # Save to database
    relationships_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITY_RELATIONSHIPS", 
        mode="overwrite"
    )
    
    logger.info(f"Generated {scale_config['entity_relationships']} entity relationships using server-side operations")


def generate_customers(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate customer profiles linked to entities using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating customers (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    key_entities = config.KEY_ENTITIES
    
    # Get key entity IDs
    key_entity_ids = [spec['entity_id'] for spec in key_entities.values()]
    
    # Define key customers with specific characteristics as SQL
    key_customers_sql = """
        -- Global Trade Ventures (HIGH risk, REQUIRES_EDD)
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
        -- Innovate GmbH (MEDIUM risk, COMPLETE)
        SELECT 
            'CUST_INN_DE_001', 'INN_DE_001', 'CORPORATE',
            DATEADD(year, -8, CURRENT_DATE()), 'MEDIUM', 'COMPLETE',
            DATEADD(month, -6, CURRENT_DATE()), DATEADD(month, 6, CURRENT_DATE()),
            12, 'James Wilson', 0, CURRENT_TIMESTAMP()
        UNION ALL
        -- Northern Supply Chain (for cross-domain scenario)
        SELECT 
            'CUST_NSC_UK_001', 'NSC_UK_001', 'CORPORATE',
            DATEADD(year, -10, CURRENT_DATE()), 'MEDIUM', 'COMPLETE',
            DATEADD(month, -4, CURRENT_DATE()), DATEADD(month, 8, CURRENT_DATE()),
            12, 'Michael Brown', 0, CURRENT_TIMESTAMP()
    """
    
    key_customers_df = session.sql(key_customers_sql)
    key_count = 3  # Number of key customers
    
    # Generate additional customers from entities
    additional_count = scale_config['customers'] - key_count
    
    if additional_count > 0:
        risk_ratings = ['LOW', 'LOW', 'MEDIUM', 'MEDIUM', 'HIGH']  # Weighted distribution
        kyc_statuses = ['COMPLETE', 'COMPLETE', 'COMPLETE', 'PENDING', 'REQUIRES_EDD']
        rm_names = ['James Wilson', 'Sarah Mitchell', 'Michael Brown', 'Emma Thompson', 
                    'David Chen', 'Lisa Anderson', 'Robert Garcia', 'Anna Mueller']
        
        # Sample additional customers from entities
        additional_df = (
            session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES")
            .filter(F.col("ENTITY_TYPE") == "CORPORATE")
            .filter(~F.col("ENTITY_ID").isin(key_entity_ids))  # Exclude key entities
            .order_by(F.random())
            .limit(additional_count)
            .with_column("SEQ", F.row_number().over(Window.order_by(F.random())))
            .with_column("CUSTOMER_ID", F.concat(F.lit("CUST_"), F.col("ENTITY_ID")))
            .with_column("CUSTOMER_TYPE", F.lit("CORPORATE"))
            .with_column(
                "ONBOARDING_DATE",
                F.dateadd("day", -F.uniform(365, 1680, F.col("SEQ")), F.current_date())  # 1-4.6 years ago
            )
            .with_column("RISK_RATING", random_choice_from_list(risk_ratings, F.col("SEQ") + 1))
            .with_column("KYC_STATUS", random_choice_from_list(kyc_statuses, F.col("SEQ") + 2))
            .with_column(
                "AML_FLAGS",
                F.when(F.col("RISK_RATING") == "HIGH", F.uniform(0, 3, F.col("SEQ") + 3))
                 .when(F.col("RISK_RATING") == "MEDIUM", F.uniform(0, 1, F.col("SEQ") + 4))
                 .otherwise(F.lit(0))
            )
            .with_column(
                "REVIEW_FREQUENCY_MONTHS",
                F.when(F.col("RISK_RATING") == "HIGH", F.lit(6))
                 .when(F.col("RISK_RATING") == "MEDIUM", F.lit(12))
                 .otherwise(F.lit(24))
            )
            .with_column(
                "LAST_REVIEW_DATE",
                F.dateadd("day", -F.uniform(30, 365, F.col("SEQ") + 5), F.current_date())
            )
            .with_column(
                "NEXT_REVIEW_DATE",
                F.dateadd(
                    "month",
                    F.col("REVIEW_FREQUENCY_MONTHS"),
                    F.col("LAST_REVIEW_DATE")
                )
            )
            .with_column(
                "RELATIONSHIP_MANAGER",
                random_choice_from_list(rm_names, F.col("SEQ") + 6)
            )
            .with_column("CREATED_DATE", F.current_timestamp())
            .select(
                "CUSTOMER_ID", "ENTITY_ID", "CUSTOMER_TYPE", "ONBOARDING_DATE",
                "RISK_RATING", "KYC_STATUS", "LAST_REVIEW_DATE", "NEXT_REVIEW_DATE",
                "REVIEW_FREQUENCY_MONTHS", "RELATIONSHIP_MANAGER", "AML_FLAGS", "CREATED_DATE"
            )
        )
        
        # Override next_review_date for first 8 MEDIUM risk customers to be due soon (periodic review scenario)
        additional_df = additional_df.with_column(
            "ROW_NUM",
            F.row_number().over(Window.partition_by(F.col("RISK_RATING") == "MEDIUM").order_by(F.col("SEQ")))
        ).with_column(
            "NEXT_REVIEW_DATE",
            F.when(
                (F.col("RISK_RATING") == "MEDIUM") & (F.col("ROW_NUM") <= 8),
                F.dateadd("day", F.uniform(1, 30, F.col("SEQ") + 7), F.current_date())
            ).otherwise(F.col("NEXT_REVIEW_DATE"))
        ).drop("ROW_NUM")
        
        # Combine key and additional customers
        customers_df = key_customers_df.union_all(additional_df)
    else:
        customers_df = key_customers_df
    
    # Save to database
    customers_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS", 
        mode="overwrite"
    )
    
    logger.info(f"Generated {scale_config['customers']} customers using server-side operations")


def generate_transactions(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate transaction history for customers using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating transactions (server-side)...")
    
    # Define key transaction for GTV (€5M deposit for EDD scenario)
    key_transaction_sql = """
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
    """
    
    key_transaction_df = session.sql(key_transaction_sql)
    
    # Generate regular transactions for all customers via cross join
    transaction_types = ['CREDIT', 'DEBIT', 'TRANSFER']
    counterparty_names = ['European Trading Co', 'Nordic Logistics Ltd', 'Baltic Import/Export', 
                          'Swiss Finance AG', 'Amsterdam Trade House']
    counterparty_countries = ['DEU', 'FRA', 'NLD', 'BEL', 'CHE', 'AUT']
    descriptions = ['Trade settlement', 'Service payment', 'Equipment purchase', 
                    'Consulting fees', 'Supply chain payment']
    
    # Calculate transaction counts per risk level
    # HIGH: 80-120, MEDIUM: 40-80, LOW: 20-40
    # We'll use a simple average and generate via cross join
    avg_txn_per_customer = 60  # Average across risk levels
    
    regular_transactions_df = (
        session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
        .select("CUSTOMER_ID", "RISK_RATING")
        # Cross join with generator to create multiple transactions per customer
        .cross_join(
            session.generator(F.seq4(), rowcount=avg_txn_per_customer)
            .with_column("TXN_SEQ", F.row_number().over(Window.order_by(F.seq4())))
        )
        # Filter based on risk rating to get correct transaction count per customer
        .with_column(
            "KEEP_TXN",
            F.when(F.col("RISK_RATING") == "HIGH", F.col("TXN_SEQ") <= 100)  # ~80-120 range
             .when(F.col("RISK_RATING") == "MEDIUM", F.col("TXN_SEQ") <= 60)  # ~40-80 range
             .otherwise(F.col("TXN_SEQ") <= 30)  # ~20-40 range for LOW
        )
        .filter(F.col("KEEP_TXN"))
        .with_column(
            "TRANSACTION_ID",
            F.concat(
                F.lit("TXN_"),
                F.col("CUSTOMER_ID"),
                F.lit("_"),
                F.lpad(F.col("TXN_SEQ").cast("string"), 4, "0")
            )
        )
        .with_column(
            "TRANSACTION_DATE",
            F.dateadd("day", -F.uniform(1, 365, F.seq4()), F.current_timestamp())
        )
        .with_column(
            "AMOUNT",
            F.uniform(1000, 100000, F.seq4() + 1).cast("DECIMAL(18,2)")
        )
        .with_column("CURRENCY", F.lit(config.CURRENCY))
        .with_column(
            "TRANSACTION_TYPE",
            random_choice_from_list(transaction_types, F.seq4() + 2)
        )
        .with_column(
            "COUNTERPARTY_NAME",
            random_choice_from_list(counterparty_names, F.seq4() + 3)
        )
        .with_column(
            "COUNTERPARTY_COUNTRY",
            random_choice_from_list(counterparty_countries, F.seq4() + 4)
        )
        .with_column(
            "DESCRIPTION",
            random_choice_from_list(descriptions, F.seq4() + 5)
        )
        .with_column(
            "RISK_SCORE",
            F.when(
                F.col("RISK_RATING") == "HIGH",
                F.uniform(10, 80, F.seq4() + 6) / F.lit(100.0)
            ).otherwise(
                F.uniform(10, 40, F.seq4() + 7) / F.lit(100.0)
            )
        )
        .with_column(
            "SUSPICIOUS_ACTIVITY_FLAG",
            F.uniform(0, 100, F.seq4() + 8) < 5  # 5% chance
        )
        .with_column("CREATED_DATE", F.current_timestamp())
        .select(
            "TRANSACTION_ID", "CUSTOMER_ID", "TRANSACTION_DATE", "AMOUNT",
            "CURRENCY", "TRANSACTION_TYPE", "COUNTERPARTY_NAME", 
            "COUNTERPARTY_COUNTRY", "DESCRIPTION", "RISK_SCORE",
            "SUSPICIOUS_ACTIVITY_FLAG", "CREATED_DATE"
        )
    )
    
    # Combine key transaction with regular transactions
    all_transactions_df = key_transaction_df.union_all(regular_transactions_df)
    
    # Save to database (no batching needed!)
    all_transactions_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.TRANSACTIONS", 
        mode="overwrite"
    )
    
    logger.info(f"Generated transactions using server-side operations (estimated 50K-150K transactions)")


def generate_loan_applications(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate loan applications with realistic financial metrics using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating loan applications (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    
    # Define key application for Innovate GmbH (credit risk scenario)
    key_application_sql = """
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
    """
    
    key_application_df = session.sql(key_application_sql)
    
    # Generate additional applications from customers
    additional_count = scale_config['loan_applications'] - 1
    
    if additional_count > 0:
        application_statuses = ['PENDING', 'UNDER_REVIEW', 'APPROVED', 'REJECTED']
        risk_ratings = ['LOW', 'MEDIUM', 'HIGH']
        industries = ['Software Services', 'Manufacturing', 'Retail', 'Healthcare', 
                     'Construction', 'Transportation', 'Financial Services']
        
        additional_df = (
            session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
            .filter(F.col("ENTITY_ID") != "INN_DE_001")  # Exclude key customer
            .order_by(F.random())
            .limit(additional_count)
            .with_column("SEQ", F.row_number().over(Window.order_by(F.random())))
            .with_column(
                "APPLICATION_ID",
                F.concat(F.lit("APP_"), F.col("ENTITY_ID"))
            )
            .with_column(
                "REQUESTED_AMOUNT",
                F.uniform(500000, 10000000, F.col("SEQ")).cast("DECIMAL(18,2)")
            )
            .with_column(
                "APPLICATION_DATE",
                F.dateadd("day", -F.uniform(1, 180, F.col("SEQ") + 1), F.current_date())
            )
            .with_column(
                "APPLICATION_STATUS",
                random_choice_from_list(application_statuses, F.col("SEQ") + 2)
            )
            .with_column(
                "DSCR",
                F.uniform(80, 300, F.col("SEQ") + 3) / F.lit(100.0)  # 0.8 to 3.0
            )
            .with_column(
                "DEBT_TO_EQUITY",
                F.uniform(50, 500, F.col("SEQ") + 4) / F.lit(100.0)  # 0.5 to 5.0
            )
            .with_column(
                "CURRENT_RATIO",
                F.uniform(80, 250, F.col("SEQ") + 5) / F.lit(100.0)  # 0.8 to 2.5
            )
            .with_column(
                "CLIENT_CONCENTRATION",
                F.uniform(10, 80, F.col("SEQ") + 6) / F.lit(100.0)  # 0.1 to 0.8
            )
            .with_column(
                "INDUSTRY",
                random_choice_from_list(industries, F.col("SEQ") + 7)
            )
            .with_column(
                "RISK_RATING",
                F.when(F.col("DSCR") < 1.25, F.lit("HIGH"))
                 .when(F.col("DEBT_TO_EQUITY") > 3.0, F.lit("HIGH"))
                 .when(F.col("DSCR") > 2.0, F.lit("LOW"))
                 .otherwise(F.lit("MEDIUM"))
            )
            .with_column("CREATED_DATE", F.current_timestamp())
            .select(
                "APPLICATION_ID", "CUSTOMER_ID", "ENTITY_ID", "REQUESTED_AMOUNT",
                "APPLICATION_DATE", "APPLICATION_STATUS", "DSCR", "DEBT_TO_EQUITY",
                "CURRENT_RATIO", "CLIENT_CONCENTRATION", "INDUSTRY", "RISK_RATING",
                "CREATED_DATE"
            )
        )
        
        # Combine key and additional applications
        applications_df = key_application_df.union_all(additional_df)
    else:
        applications_df = key_application_df
    
    # Save to database
    applications_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.LOAN_APPLICATIONS",
        mode="overwrite"
    )
    
    logger.info(f"Generated {scale_config['loan_applications']} loan applications using server-side operations")


def generate_historical_loans(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate historical loan performance data for cohort analysis using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating historical loans (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    
    industries = ['Software Services', 'Manufacturing', 'Healthcare', 'Financial Services', 
                 'Retail', 'Construction']
    loan_statuses = ['PERFORMING', 'PERFORMING', 'PERFORMING', 'DEFAULTED']  # 75% performing
    company_prefixes = ['Tech', 'Euro', 'Nordic', 'Baltic', 'Global']
    company_roots = ['Solutions', 'Industries', 'Holdings', 'Services', 'Group']
    company_suffixes = ['Ltd', 'S.A.', 'GmbH', 'B.V.']
    
    loans_df = (
        session.generator(F.seq4(), rowcount=scale_config['historical_loans'])
        .with_column("SEQ", F.row_number().over(Window.order_by(F.seq4())))
        .with_column(
            "LOAN_ID",
            F.concat(F.lit("HIST_LOAN_"), F.substr(F.call_builtin('UUID_STRING'), 1, 8))
        )
        .with_column("CUSTOMER_ID", F.lit(None).cast("string"))  # Historical loans may not have current customer IDs
        .with_column(
            "APPLICANT_NAME",
            F.concat(
                random_choice_from_list(company_prefixes, F.col("SEQ")),
                F.lit(" "),
                random_choice_from_list(company_roots, F.col("SEQ") + 1),
                F.lit(" "),
                random_choice_from_list(company_suffixes, F.col("SEQ") + 2)
            )
        )
        .with_column(
            "ORIGINATION_DATE",
            F.to_date(
                F.concat(
                    F.uniform(2019, 2023, F.col("SEQ") + 3).cast("string"),
                    F.lit("-"),
                    F.lpad(F.uniform(1, 12, F.col("SEQ") + 4).cast("string"), 2, "0"),
                    F.lit("-"),
                    F.lpad(F.uniform(1, 28, F.col("SEQ") + 5).cast("string"), 2, "0")
                )
            )
        )
        .with_column(
            "MATURITY_DATE",
            F.dateadd("day", F.uniform(1095, 2190, F.col("SEQ") + 6), F.col("ORIGINATION_DATE"))  # 3-6 years
        )
        .with_column(
            "ORIGINAL_AMOUNT",
            F.uniform(500000, 20000000, F.col("SEQ") + 7).cast("DECIMAL(18,2)")
        )
        .with_column("CURRENCY", F.lit(config.CURRENCY))
        .with_column(
            "INDUSTRY_SECTOR",
            random_choice_from_list(industries, F.col("SEQ") + 8)
        )
        .with_column(
            "DEBT_TO_EQUITY_AT_ORIGINATION",
            F.uniform(100, 500, F.col("SEQ") + 9) / F.lit(100.0)  # 1.0 to 5.0
        )
        .with_column(
            "DSCR_AT_ORIGINATION",
            F.uniform(80, 250, F.col("SEQ") + 10) / F.lit(100.0)  # 0.8 to 2.5
        )
        .with_column(
            "CURRENT_RATIO_AT_ORIGINATION",
            F.uniform(80, 200, F.col("SEQ") + 11) / F.lit(100.0)  # 0.8 to 2.0
        )
        .with_column(
            "CLIENT_CONCENTRATION_AT_ORIGINATION",
            F.uniform(15, 85, F.col("SEQ") + 12) / F.lit(1.0)  # 15 to 85
        )
        .with_column(
            "LOAN_STATUS",
            random_choice_from_list(loan_statuses, F.col("SEQ") + 13)
        )
        .with_column(
            "DEFAULT_DATE",
            F.when(
                F.col("LOAN_STATUS") == "DEFAULTED",
                F.dateadd("day", F.uniform(365, 1460, F.col("SEQ") + 14), F.col("ORIGINATION_DATE"))
            ).otherwise(F.lit(None).cast("date"))
        )
        .with_column(
            "LOSS_AMOUNT",
            F.when(
                F.col("LOAN_STATUS") == "DEFAULTED",
                (F.col("ORIGINAL_AMOUNT") * F.uniform(20, 80, F.col("SEQ") + 15) / F.lit(100.0)).cast("DECIMAL(18,2)")
            ).otherwise(F.lit(None).cast("decimal(18,2)"))
        )
        .with_column("CREATED_DATE", F.current_timestamp())
        .select(
            "LOAN_ID", "CUSTOMER_ID", "APPLICANT_NAME", "ORIGINATION_DATE",
            "MATURITY_DATE", "ORIGINAL_AMOUNT", "CURRENCY", "INDUSTRY_SECTOR",
            "DEBT_TO_EQUITY_AT_ORIGINATION", "DSCR_AT_ORIGINATION",
            "CURRENT_RATIO_AT_ORIGINATION", "CLIENT_CONCENTRATION_AT_ORIGINATION",
            "LOAN_STATUS", "DEFAULT_DATE", "LOSS_AMOUNT", "CREATED_DATE"
        )
    )
    
    # Save to database
    loans_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.HISTORICAL_LOANS",
        mode="overwrite"
    )
    
    logger.info(f"Generated {scale_config['historical_loans']} historical loans using server-side operations")


def generate_alerts(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate transaction monitoring alerts for AML investigation scenarios using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating transaction monitoring alerts (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    
    # Define key structuring alert for demo scenario (GTV)
    key_alert_sql = """
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
    """
    
    key_alert_df = session.sql(key_alert_sql)
    
    # Generate additional alerts by sampling customers
    additional_count = scale_config['alerts'] - 1
    
    if additional_count > 0:
        alert_types = ['Structuring', 'Large Cash', 'Rapid Movement', 'High Risk Country', 'Unusual Pattern']
        alert_statuses = ['OPEN', 'UNDER_INVESTIGATION', 'CLOSED']
        analyst_names = ['Maria Santos', 'John Chen', 'Sarah Mitchell', 'David Kumar', 'Emma Rodriguez']
        dispositions = ['SAR_FILED', 'FALSE_POSITIVE', 'CLEARED']
        
        additional_df = (
            session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
            .order_by(F.random())
            .limit(additional_count)
            .with_column("SEQ", F.row_number().over(Window.order_by(F.random())))
            .with_column(
                "ALERT_ID",
                F.concat(F.lit("ALERT_"), F.substr(F.call_builtin('UUID_STRING'), 1, 8))
            )
            .with_column(
                "ALERT_TYPE",
                random_choice_from_list(alert_types, F.col("SEQ"))
            )
            .with_column(
                "ALERT_DATE",
                F.dateadd("day", -F.uniform(1, 180, F.col("SEQ") + 1), F.current_timestamp())
            )
            .with_column(
                "ALERT_STATUS",
                random_choice_from_list(alert_statuses, F.col("SEQ") + 2)
            )
            .with_column(
                "PRIORITY_SCORE",
                F.when(F.col("RISK_RATING") == "HIGH", F.uniform(70, 95, F.col("SEQ") + 3) / F.lit(100.0))
                 .when(F.col("RISK_RATING") == "MEDIUM", F.uniform(40, 70, F.col("SEQ") + 4) / F.lit(100.0))
                 .otherwise(F.uniform(10, 40, F.col("SEQ") + 5) / F.lit(100.0))
            )
            .with_column(
                "ASSIGNED_TO",
                random_choice_from_list(analyst_names, F.col("SEQ") + 6)
            )
            .with_column(
                "RESOLUTION_DATE",
                F.when(
                    F.col("ALERT_STATUS") == "CLOSED",
                    F.dateadd("day", F.uniform(1, 30, F.col("SEQ") + 7), F.col("ALERT_DATE"))
                ).otherwise(F.lit(None).cast("timestamp"))
            )
            .with_column(
                "DISPOSITION",
                F.when(
                    F.col("ALERT_STATUS") == "CLOSED",
                    random_choice_from_list(dispositions, F.col("SEQ") + 8)
                ).otherwise(F.lit(None).cast("string"))
            )
            .with_column(
                "ALERT_DESCRIPTION",
                F.concat(F.col("ALERT_TYPE"), F.lit(" pattern detected"))
            )
            .with_column(
                "FLAGGED_TRANSACTION_COUNT",
                F.uniform(1, 10, F.col("SEQ") + 9)
            )
            .with_column(
                "TOTAL_FLAGGED_AMOUNT",
                F.uniform(10000, 500000, F.col("SEQ") + 10).cast("DECIMAL(18,2)")
            )
            .with_column("CREATED_DATE", F.current_timestamp())
            .select(
                "ALERT_ID", "CUSTOMER_ID", "ALERT_TYPE", "ALERT_DATE",
                "ALERT_STATUS", "PRIORITY_SCORE", "ASSIGNED_TO", "RESOLUTION_DATE",
                "DISPOSITION", "ALERT_DESCRIPTION", "FLAGGED_TRANSACTION_COUNT",
                "TOTAL_FLAGGED_AMOUNT", "CREATED_DATE"
            )
        )
        
        # Combine key and additional alerts
        alerts_df = key_alert_df.union_all(additional_df)
    else:
        alerts_df = key_alert_df
    
    # Save to database
    alerts_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.ALERTS",
        mode="overwrite"
    )
    
    logger.info(f"Generated {scale_config['alerts']} transaction monitoring alerts using server-side operations")


def generate_alert_disposition_history(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate historical alert disposition data for ML model training using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating alert disposition history (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    
    # Check if alerts table exists
    try:
        session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ALERTS").count()
    except Exception as e:
        logger.warning(f"No alerts table found. Skipping disposition history generation: {e}")
        return
    
    analyst_names = ['Maria Santos', 'John Chen', 'Sarah Mitchell', 'David Kumar', 'Emma Rodriguez']
    
    # Generate dispositions with 75% false positive rate
    # We use UNIFORM to generate a random value 0-100, then map to dispositions
    dispositions_df = (
        session.generator(F.seq4(), rowcount=scale_config['alert_disposition_history'])
        .with_column("SEQ", F.row_number().over(Window.order_by(F.seq4())))
        .with_column("DISPOSITION_ID", F.call_builtin('UUID_STRING'))
        .with_column(
            "ALERT_ID",
            F.concat(F.lit("HIST_ALERT_"), F.substr(F.call_builtin('UUID_STRING'), 1, 8))
        )
        .with_column("RAND_VAL", F.uniform(0, 100, F.col("SEQ")))  # 0-100 for distribution
        .with_column(
            "FINAL_DISPOSITION",
            F.when(F.col("RAND_VAL") < 75, F.lit("FALSE_POSITIVE"))  # 75%
             .when(F.col("RAND_VAL") < 95, F.lit("CLEARED"))          # 20%
             .otherwise(F.lit("SAR_FILED"))                            # 5%
        )
        .with_column(
            "INVESTIGATION_NOTES",
            F.when(
                F.col("FINAL_DISPOSITION") == "FALSE_POSITIVE",
                F.lit("Transaction pattern consistent with normal business activity. No suspicious indicators found.")
            ).when(
                F.col("FINAL_DISPOSITION") == "CLEARED",
                F.lit("Customer provided satisfactory documentation. Activity verified as legitimate.")
            ).otherwise(
                F.lit("Suspicious activity identified. SAR filed with FinCEN/relevant authority.")
            )
        )
        .with_column(
            "ANALYST_NAME",
            random_choice_from_list(analyst_names, F.col("SEQ") + 1)
        )
        .with_column(
            "INVESTIGATION_HOURS",
            F.uniform(50, 800, F.col("SEQ") + 2) / F.lit(100.0)  # 0.5 to 8.0 hours
        )
        .with_column(
            "CLOSED_DATE",
            F.dateadd("day", -F.uniform(30, 730, F.col("SEQ") + 3), F.current_timestamp())
        )
        .with_column("CREATED_DATE", F.current_timestamp())
        .select(
            "DISPOSITION_ID", "ALERT_ID", "FINAL_DISPOSITION", "INVESTIGATION_NOTES",
            "ANALYST_NAME", "INVESTIGATION_HOURS", "CLOSED_DATE", "CREATED_DATE"
        )
    )
    
    # Save to database
    dispositions_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.ALERT_DISPOSITION_HISTORY",
        mode="overwrite"
    )
    
    logger.info(f"Generated {scale_config['alert_disposition_history']} historical alert dispositions (75% false positive rate) using server-side operations")


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
    """Generate client CRM records for relationship manager scenario using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating client CRM records (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('client_crm_records', 0)
    
    if target_count == 0:
        logger.info("Skipping client CRM generation (not in scale config)")
        return
    
    relationship_managers = [
        'Claire Dubois', 'Marcus Weber', 'Sofia Rossi', 'Hans Schmidt', 'Emma Johnson',
        'Pierre Lefebvre', 'Anna Müller', 'Giovanni Bianchi', 'Laura Martinez', 'Thomas Anderson'
    ]
    
    account_statuses = ['ACTIVE', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'ACTIVE', 'PROSPECT', 'PROSPECT', 'INACTIVE']  # 70/20/10 split
    account_tiers = ['PREMIUM', 'PREMIUM', 'STANDARD', 'STANDARD', 'STANDARD', 'STANDARD', 'STANDARD', 'BASIC', 'BASIC', 'BASIC']  # 20/50/30 split
    opportunity_counts = ['0', '0', '0', '1', '1', '1', '2', '2', '3', '4']  # Weighted distribution
    
    # Check if primary RM client exists
    primary_rm_client = config.KEY_ENTITIES.get('primary_rm_client')
    
    # Define key CRM record for primary RM client
    if primary_rm_client:
        key_crm_sql = f"""
            SELECT 
                'CRM_00001' AS CRM_ID,
                '{primary_rm_client['entity_id']}' AS CUSTOMER_ID,
                '{primary_rm_client['relationship_manager']}' AS RELATIONSHIP_MANAGER,
                DATEADD(day, -UNIFORM(1, 60, SEQ4()), CURRENT_DATE()) AS LAST_CONTACT_DATE,
                '{primary_rm_client['account_status']}' AS ACCOUNT_STATUS,
                'PREMIUM' AS ACCOUNT_TIER,
                'Strategic account. Multiple cross-sell opportunities identified.' AS NOTES_SUMMARY,
                3 AS RISK_OPPORTUNITIES_COUNT,
                CURRENT_TIMESTAMP() AS CREATED_DATE
        """
        key_crm_df = session.sql(key_crm_sql)
        additional_count = target_count - 1
    else:
        key_crm_df = None
        additional_count = target_count
    
    # Generate additional CRM records by sampling customers
    if additional_count > 0:
        additional_df = (
            session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
            .order_by(F.random())
            .limit(additional_count)
            .with_column("SEQ", F.row_number().over(Window.order_by(F.random())))
            .with_column(
                "CRM_ID",
                F.concat(F.lit("CRM_"), F.lpad((F.col("SEQ") + (1 if primary_rm_client else 0)).cast("string"), 5, "0"))
            )
            .with_column(
                "RELATIONSHIP_MANAGER",
                random_choice_from_list(relationship_managers, F.col("SEQ"))
            )
            .with_column(
                "LAST_CONTACT_DATE",
                F.dateadd("day", -F.uniform(1, 60, F.col("SEQ") + 1), F.current_date())
            )
            .with_column(
                "ACCOUNT_STATUS",
                random_choice_from_list(account_statuses, F.col("SEQ") + 2)
            )
            .with_column(
                "ACCOUNT_TIER",
                random_choice_from_list(account_tiers, F.col("SEQ") + 3)
            )
            .with_column(
                "RISK_OPPORTUNITIES_COUNT",
                random_choice_from_list(opportunity_counts, F.col("SEQ") + 4).cast("int")
            )
            .with_column(
                "NOTES_SUMMARY",
                F.concat(
                    F.lit("Last contact: "),
                    F.to_char(F.col("LAST_CONTACT_DATE"), "YYYY-MM-DD"),
                    F.lit(". Account tier: "),
                    F.col("ACCOUNT_TIER"),
                    F.lit(". "),
                    F.col("RISK_OPPORTUNITIES_COUNT").cast("string"),
                    F.lit(" opportunities identified.")
                )
            )
            .with_column("CREATED_DATE", F.current_timestamp())
            .select(
                "CRM_ID", "CUSTOMER_ID", "RELATIONSHIP_MANAGER", "LAST_CONTACT_DATE",
                "ACCOUNT_STATUS", "ACCOUNT_TIER", "NOTES_SUMMARY", 
                "RISK_OPPORTUNITIES_COUNT", "CREATED_DATE"
            )
        )
        
        # Combine key and additional records
        if key_crm_df:
            crm_df = key_crm_df.union_all(additional_df)
        else:
            crm_df = additional_df
    else:
        crm_df = key_crm_df
    
    # Save to database
    crm_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM",
        mode="overwrite"
    )
    
    logger.info(f"Generated {target_count} client CRM records using server-side operations")


def generate_client_opportunities(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate client opportunities for relationship manager scenario using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating client opportunities (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('client_opportunities', 0)
    
    if target_count == 0:
        logger.info("Skipping client opportunities generation (not in scale config)")
        return
    
    # Check if CRM table exists
    try:
        crm_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM")
        crm_df.count()
    except:
        logger.warning("No CRM records found, skipping opportunities generation")
        return
    
    opportunity_types = [
        'CROSS_SELL', 'UPSELL', 'RISK_MITIGATION', 'NEW_PRODUCT', 
        'INVESTMENT_ADVISORY', 'TRADE_FINANCE', 'FX_HEDGING'
    ]
    
    source_types = ['call_note', 'internal_email', 'news', 'transaction_pattern', 'market_intelligence']
    priorities = ['HIGH', 'HIGH', 'MEDIUM', 'MEDIUM', 'MEDIUM', 'MEDIUM', 'MEDIUM', 'LOW', 'LOW', 'LOW']  # 20/50/30 split
    statuses = ['OPEN', 'OPEN', 'OPEN', 'OPEN', 'IN_PROGRESS', 'IN_PROGRESS', 'IN_PROGRESS', 'CLOSED_WON', 'CLOSED_WON', 'CLOSED_LOST']  # 40/30/20/10
    potential_values = [50000, 100000, 250000, 500000, 1000000, 2500000]
    
    # Generate opportunities by sampling CRM records
    opportunities_df = (
        crm_df
        .order_by(F.random())
        .limit(target_count)
        .with_column("SEQ", F.row_number().over(Window.order_by(F.random())))
        .with_column(
            "OPPORTUNITY_ID",
            F.concat(F.lit("OPP_"), F.lpad(F.col("SEQ").cast("string"), 6, "0"))
        )
        .with_column(
            "OPPORTUNITY_TYPE",
            random_choice_from_list(opportunity_types, F.col("SEQ"))
        )
        .with_column(
            "OPPORTUNITY_DESCRIPTION",
            F.when(F.col("OPPORTUNITY_TYPE") == "CROSS_SELL", 
                   F.lit("Cross-sell FX hedging products to protect against currency fluctuation"))
             .when(F.col("OPPORTUNITY_TYPE") == "UPSELL",
                   F.lit("Upsell to premium banking tier for expanded trade finance limits"))
             .when(F.col("OPPORTUNITY_TYPE") == "RISK_MITIGATION",
                   F.lit("Address concentration risk through supplier diversification advisory"))
             .when(F.col("OPPORTUNITY_TYPE") == "NEW_PRODUCT",
                   F.lit("Introduce sustainable finance solutions aligned with ESG goals"))
             .when(F.col("OPPORTUNITY_TYPE") == "INVESTMENT_ADVISORY",
                   F.lit("Offer treasury optimization services for excess cash management"))
             .when(F.col("OPPORTUNITY_TYPE") == "TRADE_FINANCE",
                   F.lit("Expand documentary credit facilities for international expansion"))
             .otherwise(F.lit("Implement forward contracts to hedge EUR/USD exposure"))
        )
        .with_column(
            "POTENTIAL_VALUE",
            random_choice_from_list([str(v) for v in potential_values], F.col("SEQ") + 1).cast("decimal(18,2)")
        )
        .with_column(
            "SOURCE_TYPE",
            random_choice_from_list(source_types, F.col("SEQ") + 2)
        )
        .with_column(
            "SOURCE_DOCUMENT_ID",
            F.concat(F.lit("DOC_"), F.uniform(1000, 9999, F.col("SEQ") + 3).cast("string"))
        )
        .with_column(
            "PRIORITY",
            random_choice_from_list(priorities, F.col("SEQ") + 4)
        )
        .with_column(
            "STATUS",
            random_choice_from_list(statuses, F.col("SEQ") + 5)
        )
        .with_column(
            "CREATED_DATE",
            F.dateadd("day", -F.uniform(1, 90, F.col("SEQ") + 6), F.current_timestamp())
        )
        .with_column(
            "LAST_UPDATED_DATE",
            F.dateadd("day", -F.uniform(0, 30, F.col("SEQ") + 7), F.current_timestamp())
        )
        .select(
            "OPPORTUNITY_ID", "CUSTOMER_ID", "OPPORTUNITY_TYPE", "OPPORTUNITY_DESCRIPTION",
            "POTENTIAL_VALUE", "SOURCE_TYPE", "SOURCE_DOCUMENT_ID", "PRIORITY", 
            "STATUS", "CREATED_DATE", "LAST_UPDATED_DATE"
        )
    )
    
    # Save to database
    opportunities_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_OPPORTUNITIES",
        mode="overwrite"
    )
    
    logger.info(f"Generated {target_count} client opportunities using server-side operations")


def generate_model_portfolios(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate model portfolios for wealth advisor scenario using pure SQL."""
    import snowflake.snowpark.functions as F
    
    logger.info("Generating model portfolios (server-side)...")
    
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
    
    # Save to database
    portfolios_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.MODEL_PORTFOLIOS",
        mode="overwrite"
    )
    
    logger.info(f"Generated {portfolio_count} model portfolios using server-side operations")


def generate_holdings(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate investment holdings for wealth clients using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating holdings (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    total_holdings = scale_config.get('holdings', 0)
    wealth_client_count = scale_config.get('wealth_clients', 0)
    
    if total_holdings == 0 or wealth_client_count == 0:
        logger.info("Skipping holdings generation (not in scale config)")
        return
    
    # Sample wealth clients from customers
    wealth_clients_df = (
        session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CUSTOMERS")
        .order_by(F.random())
        .limit(wealth_client_count)
        .select("CUSTOMER_ID")
    )
    
    # Define assets as lists (will be combined for random selection)
    asset_types = ['EQUITY', 'EQUITY', 'EQUITY', 'EQUITY', 'EQUITY', 'BOND', 'BOND', 'BOND', 'ALTERNATIVE', 'CASH']  # Weighted
    asset_classes = ['DOMESTIC_EQUITY', 'INTL_EQUITY', 'EMERGING_MARKETS', 'GOVT_BOND', 'CORP_BOND', 
                     'REAL_ESTATE', 'COMMODITIES', 'INFRASTRUCTURE', 'MONEY_MARKET']
    asset_names = ['DAX 40 ETF', 'S&P 500 ETF', 'MSCI World ETF', 'MSCI EM ETF', 'German Government Bonds',
                   'EUR Corporate Bond ETF', 'European REIT ETF', 'Gold ETF', 'EUR Money Market Fund']
    tickers = ['EXS1.DE', 'SPY', 'IWDA.AS', 'EEM', 'BUND', 'CORP.PA', 'IQQP.AS', 'GLD', 'MMF_EUR']
    
    holdings_per_client = total_holdings // wealth_client_count if wealth_client_count > 0 else 0
    
    # Generate holdings via cross join (similar to transactions pattern)
    holdings_df = (
        wealth_clients_df
        .cross_join(
            session.generator(F.seq4(), rowcount=holdings_per_client)
            .with_column("HOLDING_SEQ", F.row_number().over(Window.order_by(F.seq4())))
        )
        .with_column("GLOBAL_SEQ", F.row_number().over(Window.order_by(F.col("CUSTOMER_ID"), F.col("HOLDING_SEQ"))))
        .with_column(
            "HOLDING_ID",
            F.concat(F.lit("HOLD_"), F.lpad(F.col("GLOBAL_SEQ").cast("string"), 6, "0"))
        )
        .with_column("ASSET_TYPE", random_choice_from_list(asset_types, F.col("GLOBAL_SEQ")))
        .with_column("ASSET_CLASS", random_choice_from_list(asset_classes, F.col("GLOBAL_SEQ") + 1))
        .with_column("ASSET_NAME", random_choice_from_list(asset_names, F.col("GLOBAL_SEQ") + 2))
        .with_column("TICKER_SYMBOL", random_choice_from_list(tickers, F.col("GLOBAL_SEQ") + 3))
        .with_column(
            "QUANTITY",
            F.uniform(100, 10000, F.col("GLOBAL_SEQ") + 4).cast("DECIMAL(18,2)")
        )
        .with_column(
            "COST_BASIS_PER_UNIT",
            F.uniform(50, 500, F.col("GLOBAL_SEQ") + 5).cast("DECIMAL(18,2)")
        )
        .with_column(
            "CURRENT_PRICE_PER_UNIT",
            (F.col("COST_BASIS_PER_UNIT") * F.uniform(80, 130, F.col("GLOBAL_SEQ") + 6) / F.lit(100.0)).cast("DECIMAL(18,2)")
        )
        .with_column(
            "CURRENT_VALUE",
            (F.col("QUANTITY") * F.col("CURRENT_PRICE_PER_UNIT")).cast("DECIMAL(18,2)")
        )
        .with_column(
            "COST_BASIS",
            (F.col("QUANTITY") * F.col("COST_BASIS_PER_UNIT")).cast("DECIMAL(18,2)")
        )
        .with_column(
            "UNREALIZED_GAIN_LOSS",
            (F.col("CURRENT_VALUE") - F.col("COST_BASIS")).cast("DECIMAL(18,2)")
        )
        .with_column("AS_OF_DATE", F.current_date())
        .with_column("LAST_UPDATED_DATE", F.current_timestamp())
    )
    
    # Calculate allocation percentages using window function
    holdings_df = holdings_df.with_column(
        "TOTAL_VALUE_PER_CUSTOMER",
        F.sum(F.col("CURRENT_VALUE")).over(Window.partition_by("CUSTOMER_ID"))
    ).with_column(
        "ALLOCATION_PCT",
        ((F.col("CURRENT_VALUE") / F.col("TOTAL_VALUE_PER_CUSTOMER")) * F.lit(100.0)).cast("DECIMAL(5,2)")
    ).select(
        "HOLDING_ID", "CUSTOMER_ID", "ASSET_TYPE", "ASSET_CLASS", "ASSET_NAME",
        "TICKER_SYMBOL", "QUANTITY", "CURRENT_VALUE", "COST_BASIS", 
        "UNREALIZED_GAIN_LOSS", "ALLOCATION_PCT", "AS_OF_DATE", "LAST_UPDATED_DATE"
    )
    
    # Save to database
    holdings_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.HOLDINGS",
        mode="overwrite"
    )
    
    logger.info(f"Generated {total_holdings} holdings for {wealth_client_count} wealth clients using server-side operations")


def generate_wealth_client_profiles(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate wealth client profiles linking customers to model portfolios using server-side operations."""
    import snowflake.snowpark.functions as F
    from snowpark_helpers import random_choice_from_list
    
    logger.info("Generating wealth client profiles (server-side)...")
    
    scale_config = config.get_scale_config(scale)
    wealth_client_count = scale_config.get('wealth_clients', 0)
    
    if wealth_client_count == 0:
        logger.info("Skipping wealth client profiles generation (not in scale config)")
        return
    
    # Check if holdings and model portfolios exist
    try:
        holdings_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.HOLDINGS")
        portfolios_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.MODEL_PORTFOLIOS")
    except:
        logger.warning("No holdings or model portfolios found, skipping wealth profiles generation")
        return
    
    wealth_advisors = ['Marcus Weber', 'Sofia Rossi', 'Jean-Pierre Dubois', 'Anna Müller', 'Laura Martinez']
    risk_tolerances = ['CONSERVATIVE', 'MODERATE', 'AGGRESSIVE']
    tax_statuses = ['STANDARD', 'TAX_DEFERRED', 'TAX_EXEMPT']
    investment_objectives = ['GROWTH', 'INCOME', 'PRESERVATION', 'BALANCED']
    
    # Get unique wealth customers from holdings and calculate their AUM
    wealth_customers_aum = (
        holdings_df
        .group_by("CUSTOMER_ID")
        .agg(F.sum("CURRENT_VALUE").alias("TOTAL_AUM"))
    )
    
    # Assign profiles to each wealth customer
    profiles_df = (
        wealth_customers_aum
        .with_column("SEQ", F.row_number().over(Window.order_by("CUSTOMER_ID")))
        .with_column(
            "PROFILE_ID",
            F.concat(F.lit("WCP_"), F.lpad(F.col("SEQ").cast("string"), 5, "0"))
        )
        .with_column(
            "RISK_TOLERANCE",
            random_choice_from_list(risk_tolerances, F.col("SEQ"))
        )
        .with_column(
            "MODEL_PORTFOLIO_ID",
            # Map risk tolerance to model portfolio
            F.when(F.col("RISK_TOLERANCE") == "CONSERVATIVE", F.lit("MODEL_CONSERVATIVE"))
             .when(F.col("RISK_TOLERANCE") == "AGGRESSIVE", F.lit("MODEL_AGGRESSIVE"))
             .otherwise(F.lit("MODEL_BALANCED"))  # MODERATE maps to BALANCED
        )
        .with_column(
            "WEALTH_ADVISOR",
            random_choice_from_list(wealth_advisors, F.col("SEQ") + 1)
        )
        .with_column(
            "TAX_STATUS",
            random_choice_from_list(tax_statuses, F.col("SEQ") + 2)
        )
        .with_column(
            "INVESTMENT_OBJECTIVES",
            random_choice_from_list(investment_objectives, F.col("SEQ") + 3)
        )
        .with_column("CONCENTRATION_THRESHOLD_PCT", F.lit(70.0))
        .with_column("REBALANCE_TRIGGER_PCT", F.lit(10.0))
        .with_column(
            "LAST_REBALANCE_DATE",
            F.dateadd("day", -F.uniform(30, 180, F.col("SEQ") + 4), F.current_date())
        )
        .with_column(
            "NEXT_REVIEW_DATE",
            F.dateadd("day", F.uniform(30, 90, F.col("SEQ") + 5), F.current_date())
        )
        .with_column(
            "CREATED_DATE",
            F.dateadd("day", -F.uniform(365, 1095, F.col("SEQ") + 6), F.current_timestamp())
        )
        .with_column("LAST_UPDATED_DATE", F.current_timestamp())
        .select(
            "PROFILE_ID", "CUSTOMER_ID", "MODEL_PORTFOLIO_ID", "WEALTH_ADVISOR",
            "RISK_TOLERANCE", "TAX_STATUS", "INVESTMENT_OBJECTIVES", "TOTAL_AUM",
            "CONCENTRATION_THRESHOLD_PCT", "REBALANCE_TRIGGER_PCT", 
            "LAST_REBALANCE_DATE", "NEXT_REVIEW_DATE", "CREATED_DATE", "LAST_UPDATED_DATE"
        )
    )
    
    # Save to database
    profiles_df.write.save_as_table(
        f"{config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_CLIENT_PROFILES",
        mode="overwrite"
    )
    
    logger.info(f"Generated {wealth_client_count} wealth client profiles using server-side operations")


def main():
    """Main function for testing structured data generation."""
    print("Structured data generator module loaded successfully")
    print("Use generate_all_structured_data() method to create structured demo data")


if __name__ == "__main__":
    main()
