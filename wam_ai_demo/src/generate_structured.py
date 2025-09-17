"""
WAM AI Demo - Structured Data Generation
Generates realistic structured data following the enhanced model
"""

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit, uniform, random, when_matched, when_not_matched
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, DecimalType, DateType
import config
from src.setup import create_foundation_tables
from src.extract_real_data import load_real_assets_from_csv
from src.golden_records_handler import apply_golden_client_overrides, is_golden_client_record, generate_golden_portfolio_positions
from datetime import datetime, timedelta
import random as py_random
import pandas as pd
import os

def generate_structured_data(session: Session, test_mode: bool = False):
    """Generate all structured data following the enhanced model"""
    
    # Adjust volumes for test mode
    if test_mode:
        config.NUM_ADVISORS = 2
        config.CLIENTS_PER_ADVISOR = 5
        config.UNSTRUCTURED_DOCS_PER_TICKER = 5
        config.COMMS_PER_CLIENT = 10
        print("  📊 Running in test mode with reduced volumes")
    
    # Create foundation tables
    create_foundation_tables(session)
    
    # Generate data in dependency order
    generate_managers(session)
    generate_advisors(session)
    generate_clients(session)
    generate_issuers_and_securities(session)
    generate_portfolios_and_accounts(session)
    
    # Use simplified positions generation for reliability
    generate_simplified_positions(session)
    generate_market_data(session)
    
    # Generate advisor benchmarking data
    generate_advisor_client_relationships(session)
    generate_advisor_roster(session)
    generate_advisor_summary_ttm(session)
    
    print("  ✅ Structured data generation complete")


# ======================================================
# WATCHLIST CREATION
# ======================================================

def create_watchlists(session: Session):
    """Create thematic watchlists"""
    
    # Ensure database context
    session.sql(f"USE DATABASE {config.DATABASE_NAME}").collect()
    
    # Create watchlist tables
    create_watchlist_tables(session)
    
    # Create watchlists from configuration
    for watchlist_name, watchlist_config in config.WATCHLIST_DEFINITIONS.items():
        create_watchlist_from_config(session, watchlist_name, watchlist_config)

def create_watchlist_tables(session: Session):
    """Create watchlist infrastructure tables"""
    
    # Create watchlist master table
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST (
            WatchlistID BIGINT IDENTITY(1,1) PRIMARY KEY,
            WatchlistName VARCHAR(255) NOT NULL,
            WatchlistType VARCHAR(100),
            Description TEXT,
            CreatedDate DATE DEFAULT CURRENT_DATE(),
            IsActive BOOLEAN DEFAULT TRUE
        )
    """).collect()
    
    # Create watchlist securities mapping table
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES (
            WatchlistSecurityID BIGINT IDENTITY(1,1) PRIMARY KEY,
            WatchlistID BIGINT NOT NULL,
            SecurityID BIGINT NOT NULL,
            AddedDate DATE DEFAULT CURRENT_DATE(),
            Rationale TEXT,
            ESG_Score DECIMAL(3,2),
            IsActive BOOLEAN DEFAULT TRUE
        )
    """).collect()

def create_watchlist_from_config(session: Session, watchlist_name: str, watchlist_config: dict):
    """Create a watchlist from configuration"""
    
    print(f"    → Creating {watchlist_name} watchlist...")
    
    # Create the watchlist
    escaped_description = watchlist_config['description'].replace("'", "''")
    session.sql(f"""
        INSERT INTO {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST (WatchlistName, WatchlistType, Description)
        VALUES ('{watchlist_name}', '{watchlist_config['type']}', '{escaped_description}')
    """).collect()
    
    # Get the watchlist ID
    watchlist_result = session.sql(f"""
        SELECT WatchlistID FROM {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST 
        WHERE WatchlistName = '{watchlist_name}'
    """).collect()
    
    if watchlist_result:
        watchlist_id = watchlist_result[0]['WATCHLISTID']
        
        # Add securities to watchlist
        for security in watchlist_config['securities']:
            # Get SecurityID for this ticker
            security_result = session.sql(f"""
                SELECT SecurityID FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY 
                WHERE PrimaryTicker = '{security['ticker']}'
            """).collect()
            
            if security_result:
                security_id = security_result[0]['SECURITYID']
                
                # Escape single quotes in rationale
                escaped_rationale = security['rationale'].replace("'", "''")
                
                session.sql(f"""
                    INSERT INTO {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES 
                    (WatchlistID, SecurityID, ESG_Score, Rationale)
                    VALUES ({watchlist_id}, {security_id}, {security['esg_score']}, '{escaped_rationale}')
                """).collect()
                
                print(f"      ✅ Added {security['ticker']} to {watchlist_name}")

def create_carbon_negative_leaders_watchlist(session: Session):
    """Create the Carbon Negative Leaders thematic watchlist"""
    
    print("    → Creating Carbon Negative Leaders watchlist...")
    
    # Create the watchlist
    session.sql(f"""
        INSERT INTO {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST
        (WatchlistName, WatchlistType, Description)
        VALUES
        ('Carbon Negative Leaders', 'ESG Thematic', 
         'Companies with strong carbon neutrality commitments and measurable progress toward net-zero emissions goals. Focus on technology and industrial leaders driving climate innovation.')
    """).collect()
    
    # Get the watchlist ID
    watchlist_result = session.sql(f"""
        SELECT WatchlistID FROM {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST 
        WHERE WatchlistName = 'Carbon Negative Leaders'
    """).collect()
    
    if watchlist_result:
        watchlist_id = watchlist_result[0]['WATCHLISTID']
        
        # Define Carbon Negative Leaders based on our golden tickers
        carbon_leaders = [
            {'ticker': 'MSFT', 'rationale': 'Committed to being carbon negative by 2030, $1B climate innovation fund', 'esg_score': 8.5},
            {'ticker': 'AAPL', 'rationale': 'Carbon neutral by 2030, renewable energy initiatives, sustainable supply chain', 'esg_score': 8.2},
            {'ticker': 'NVDA', 'rationale': 'AI solutions for climate modeling and energy efficiency optimization', 'esg_score': 7.8}
        ]
        
        # Get security IDs for these tickers
        for leader in carbon_leaders:
            ticker = leader['ticker']
            security_result = session.sql(f"""
                SELECT SecurityID FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY 
                WHERE PrimaryTicker = '{ticker}'
            """).collect()
            
            if security_result:
                security_id = security_result[0]['SECURITYID']
                
                # Add to watchlist
                session.sql(f"""
                    INSERT INTO {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES
                    (WatchlistID, SecurityID, Rationale, ESG_Score)
                    VALUES
                    ({watchlist_id}, {security_id}, '{leader['rationale']}', {leader['esg_score']})
                """).collect()
                
                print(f"      ✅ Added {ticker} to Carbon Negative Leaders")

def create_ai_innovation_watchlist(session: Session):
    """Create AI Innovation Leaders watchlist"""
    
    print("    → Creating AI Innovation Leaders watchlist...")
    
    # Create the watchlist
    session.sql(f"""
        INSERT INTO {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST
        (WatchlistName, WatchlistType, Description)
        VALUES
        ('AI Innovation Leaders', 'Technology Thematic', 
         'Companies leading artificial intelligence development and implementation across chips, software, and cloud infrastructure.')
    """).collect()
    
    # Get the watchlist ID
    watchlist_result = session.sql(f"""
        SELECT WatchlistID FROM {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST 
        WHERE WatchlistName = 'AI Innovation Leaders'
    """).collect()
    
    if watchlist_result:
        watchlist_id = watchlist_result[0]['WATCHLISTID']
        
        # Define AI Innovation Leaders
        ai_leaders = [
            {'ticker': 'NVDA', 'rationale': 'Leading AI chip architecture for training and inference', 'esg_score': 7.5},
            {'ticker': 'MSFT', 'rationale': 'AI infrastructure through Azure, OpenAI partnership, Copilot integration', 'esg_score': 8.5},
            {'ticker': 'AAPL', 'rationale': 'On-device AI processing, machine learning capabilities', 'esg_score': 8.2}
        ]
        
        # Add securities to watchlist
        for leader in ai_leaders:
            ticker = leader['ticker']
            security_result = session.sql(f"""
                SELECT SecurityID FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY 
                WHERE PrimaryTicker = '{ticker}'
            """).collect()
            
            if security_result:
                security_id = security_result[0]['SECURITYID']
                
                session.sql(f"""
                    INSERT INTO {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES
                    (WatchlistID, SecurityID, Rationale, ESG_Score)
                    VALUES
                    ({watchlist_id}, {security_id}, '{leader['rationale']}', {leader['esg_score']})
                """).collect()
                
                print(f"      ✅ Added {ticker} to AI Innovation Leaders")

def create_esg_leaders_watchlist(session: Session):
    """Create ESG Leaders watchlist"""
    
    print("    → Creating ESG Leaders watchlist...")
    
    # Create the watchlist
    session.sql(f"""
        INSERT INTO {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST
        (WatchlistName, WatchlistType, Description)
        VALUES
        ('ESG Leaders', 'ESG Comprehensive', 
         'Companies demonstrating leadership across Environmental, Social, and Governance factors with strong sustainability commitments.')
    """).collect()
    
    # Get the watchlist ID
    watchlist_result = session.sql(f"""
        SELECT WatchlistID FROM {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST 
        WHERE WatchlistName = 'ESG Leaders'
    """).collect()
    
    if watchlist_result:
        watchlist_id = watchlist_result[0]['WATCHLISTID']
        
        # Define ESG Leaders
        esg_leaders = [
            {'ticker': 'MSFT', 'rationale': 'Comprehensive ESG leadership: carbon negative goals, diversity initiatives, strong governance', 'esg_score': 9.1},
            {'ticker': 'AAPL', 'rationale': 'Environmental leadership, supply chain sustainability, privacy governance', 'esg_score': 8.7},
            {'ticker': 'SAP', 'rationale': 'European ESG standards, sustainability software solutions, climate action', 'esg_score': 8.3}
        ]
        
        # Add securities to watchlist
        for leader in esg_leaders:
            ticker = leader['ticker']
            security_result = session.sql(f"""
                SELECT SecurityID FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY 
                WHERE PrimaryTicker = '{ticker}'
            """).collect()
            
            if security_result:
                security_id = security_result[0]['SECURITYID']
                
                session.sql(f"""
                    INSERT INTO {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES
                    (WatchlistID, SecurityID, Rationale, ESG_Score)
                    VALUES
                    ({watchlist_id}, {security_id}, '{leader['rationale']}', {leader['esg_score']})
                """).collect()
                
                print(f"      ✅ Added {ticker} to ESG Leaders")

def generate_managers(session: Session):
    """Generate manager data"""
    print("    → Generating managers...")
    
    # Ensure database context is set
    session.sql(f"USE DATABASE {config.DATABASE_NAME}").collect()
    
    # Generate single manager for now
    import pandas as pd
    managers_data = [{
        'MANAGERNAME': config.MANAGER_CONFIG['name'],
        'MANAGERTITLE': config.MANAGER_CONFIG['title'],
        'STARTDATE': config.get_history_start_date(),
        'ACTIVEFLAG': True
    }]
    
    managers_df = pd.DataFrame(managers_data)
    session.write_pandas(managers_df, "CURATED.DIM_MANAGER", overwrite=True, quote_identifiers=False)
    print(f"      ✅ Generated {len(managers_data)} manager(s)")

def generate_advisors(session: Session):
    """Generate advisor data using pandas and write_pandas for efficiency"""
    print("    → Generating advisors...")
    
    # Ensure database context is set
    session.sql(f"USE DATABASE {config.DATABASE_NAME}").collect()
    
    # Get manager ID
    manager_result = session.sql("SELECT ManagerID FROM CURATED.DIM_MANAGER LIMIT 1").collect()
    manager_id = manager_result[0]['MANAGERID'] if manager_result else 1
    
    # Generate advisor data using pandas for efficiency
    import pandas as pd
    advisors_data = []
    for i in range(config.NUM_ADVISORS):
        advisors_data.append({
            'MANAGERID': manager_id,
            'FIRSTNAME': f'Advisor{i+1}',
            'LASTNAME': f'Smith{i+1}',
            'EMAIL': f'advisor{i+1}@wealthfirm.com',
            'TEAM': f'Team {chr(65+i)}',
            'ISACTIVE': True
        })
    
    advisors_df = pd.DataFrame(advisors_data)
    
    # Use write_pandas with quote_identifiers=False for IDENTITY column compatibility
    session.write_pandas(
        advisors_df, 
        "CURATED.DIM_ADVISOR",  # Use schema-qualified name since database is set
        overwrite=True,
        quote_identifiers=False
    )
    
    print(f"    ✅ Generated {config.NUM_ADVISORS} advisors")

def generate_clients(session: Session):
    """Generate client data with varied tenure and departures for benchmarking"""
    print("    → Generating clients...")
    
    # Get advisor IDs using Snowpark
    advisors = session.sql(f"SELECT AdvisorID FROM {config.DATABASE_NAME}.CURATED.DIM_ADVISOR").collect()
    
    # Generate client data using pandas for efficiency
    import pandas as pd
    clients_data = []
    client_id = 1
    golden_clients_created = set()  # Track which golden clients have been created
    
    for advisor in advisors:
        advisor_id = advisor['ADVISORID']
        for i in range(config.CLIENTS_PER_ADVISOR):
            # Use realistic client names for demo
            first_names = config.DEMO_FIRST_NAMES
            last_names = config.DEMO_LAST_NAMES
            
            first_name = first_names[(client_id - 1) % len(first_names)]
            last_name = last_names[(client_id - 1) % len(last_names)]
            
            # Check if this would be a golden client and if we've already created it
            potential_golden_name = f"{first_name} {last_name}"
            if config.get_golden_client_config(potential_golden_name) and potential_golden_name in golden_clients_created:
                # Skip this golden client since we've already created it, use next name instead
                client_id += 1
                first_name = first_names[(client_id - 1) % len(first_names)]
                last_name = last_names[(client_id - 1) % len(last_names)]
                potential_golden_name = f"{first_name} {last_name}"
            
            # Generate varied client tenure (6 months to 5 years)
            tenure_months = py_random.randint(config.CLIENT_TENURE_MONTHS["min"], config.CLIENT_TENURE_MONTHS["max"])
            onboarding_date = config.get_history_end_date() - timedelta(days=tenure_months * 30)
            
            # Determine if client has departed based on departure rate
            has_departed = py_random.random() < config.CLIENT_DEPARTURE_RATE_ANNUAL * (tenure_months / 12.0)
            
            # Set departure details if applicable
            end_date = None
            departure_reason = None
            departure_notes = None
            is_active = True
            
            if has_departed and tenure_months > 12:  # Only clients with >1 year tenure can depart
                # Set departure date within last 2 years
                months_since_departure = py_random.randint(1, min(24, tenure_months - 6))
                end_date = config.get_history_end_date() - timedelta(days=months_since_departure * 30)
                departure_reason = py_random.choices(
                    list(config.DEPARTURE_REASONS.keys()),
                    weights=list(config.DEPARTURE_REASONS.values())
                )[0]
                departure_notes = f"Client departed due to {departure_reason.lower()}"
                is_active = False
            
            client_data = {
                'ADVISORID': advisor_id,
                'FIRSTNAME': first_name,
                'LASTNAME': last_name,
                'EMAIL': f'{first_name.lower()}.{last_name.lower()}@{config.DEMO_EMAIL_DOMAIN}',
                'PHONE': f'+1-555-{1000+client_id:04d}',
                'DATEOFBIRTH': datetime(1960 + (client_id % 40), 1 + (client_id % 12), 1 + (client_id % 28)).date(),
                'RISKTOLERANCE': py_random.choice(config.RISK_TOLERANCE_OPTIONS),
                'INVESTMENTHORIZON': py_random.choice(config.INVESTMENT_HORIZON_OPTIONS),
                'ONBOARDINGDATE': onboarding_date,
                'ENDDATE': end_date,
                'DEPARTUREREASON': departure_reason,
                'DEPARTURENOTES': departure_notes,
                'ISACTIVE': is_active
            }
            
            # Apply golden record overrides if this is a golden client
            if is_golden_client_record(client_data):
                client_data = apply_golden_client_overrides(client_data)
                golden_clients_created.add(f"{client_data['FIRSTNAME']} {client_data['LASTNAME']}")
                print(f"Applied golden record overrides for {client_data['FIRSTNAME']} {client_data['LASTNAME']}")
            
            clients_data.append(client_data)
            client_id += 1
    
    clients_df = pd.DataFrame(clients_data)
    
    # Use write_pandas with quote_identifiers=False for IDENTITY column compatibility
    session.write_pandas(
        clients_df,
        "CURATED.DIM_CLIENT",  # Use schema-qualified name
        overwrite=True,
        quote_identifiers=False
    )
    
    print(f"    ✅ Generated {len(clients_data)} clients")

def generate_issuers_and_securities(session: Session):
    """Generate issuers and securities based on REQUIRED real assets CSV"""
    print("    → Generating issuers and securities from real assets...")
    
    # Load real assets - this will raise an exception if file is missing
    real_assets_df = load_real_assets_from_csv()
    
    # Generate from real assets data
    generate_from_real_assets(session, real_assets_df)

def generate_from_real_assets(session: Session, real_assets_df: pd.DataFrame):
    """Generate issuers and securities from real assets CSV using optimized Snowpark operations"""
    print("    → Using optimized Snowpark operations for real assets data...")
    
    # Upload to temporary table for efficient processing (will be reused by other functions)
    real_assets_snowpark_df = session.create_dataframe(real_assets_df)
    real_assets_snowpark_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_REAL_ASSETS")
    print("    ✅ Created TEMP_REAL_ASSETS table for optimized processing")
    
    # Import required Snowpark functions
    from snowflake.snowpark.functions import (
        col, lit, ifnull, row_number, abs as abs_func, hash as hash_func,
        regexp_replace, substr, trim, to_varchar, concat, when, length
    )
    from snowflake.snowpark import Window
    
    # Get the temp table as a DataFrame for further processing
    temp_assets_df = session.table(f"{config.DATABASE_NAME}.RAW.TEMP_REAL_ASSETS")
    
    # Calculate target counts and create selection logic
    total_securities = 50  # Reasonable number for demo
    us_count = int(total_securities * config.REGION_MIX['us'])
    eu_count = int(total_securities * config.REGION_MIX['eu'])
    
    # Select assets with optimized filtering - prioritize golden tickers, then by region
    selected_assets_df = (temp_assets_df
        .withColumn("IS_GOLDEN_TICKER", col("PRIMARY_TICKER").isin(config.GOLDEN_TICKERS))
        .withColumn("PRIORITY", 
            when(col("IS_GOLDEN_TICKER"), lit(1))
            .when(col("MARKET_REGION") == lit("USA"), lit(2))
            .when(col("MARKET_REGION") == lit("EU"), lit(3))
            .otherwise(lit(4))
        )
        .withColumn("ROW_NUM", 
            row_number().over(
                Window.partition_by(col("MARKET_REGION"))
                .order_by(col("PRIORITY"), col("PRIMARY_TICKER"))
            )
        )
        .filter(
            (col("IS_GOLDEN_TICKER") == lit(True)) |
            ((col("MARKET_REGION") == lit("USA")) & (col("ROW_NUM") <= lit(us_count))) |
            ((col("MARKET_REGION") == lit("EU")) & (col("ROW_NUM") <= lit(eu_count)))
        )
        .drop("IS_GOLDEN_TICKER", "PRIORITY", "ROW_NUM")
    )
    
    # Generate issuers using efficient Snowpark operations
    print("    → Generating issuers with Snowpark operations...")
    generate_optimized_issuers(session, selected_assets_df)
    
    # Generate securities using efficient Snowpark operations  
    print("    → Generating securities with Snowpark operations...")
    generate_optimized_securities(session, selected_assets_df)
    
    # Report statistics
    report_generation_statistics(session, selected_assets_df)
    
    # Clean up temporary table
    session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_REAL_ASSETS").collect()
    print("    ✅ Cleaned up temporary table")

def generate_optimized_issuers(session: Session, selected_assets_df):
    """Build issuer dimension from selected assets using efficient Snowpark operations"""
    from snowflake.snowpark.functions import (
        col, lit, ifnull, row_number, abs as abs_func, hash as hash_func,
        regexp_replace, substr, trim, to_varchar, concat, length
    )
    from snowflake.snowpark import Window
    
    # Create issuers DataFrame using optimized Snowpark operations
    issuers_df = (selected_assets_df.select(
        ifnull(col("ISSUER_NAME"), col("SECURITY_NAME")).alias("LegalName"),
        ifnull(col("COUNTRY_OF_DOMICILE"), lit("US")).alias("CountryOfIncorporation"),
        ifnull(col("INDUSTRY_SECTOR"), lit('Diversified')).alias("INDUSTRY_SECTOR")
    )
    .filter((col("LegalName").isNotNull()) & (col("LegalName") != lit("Unknown")))
    .distinct()
    .select(
        # Add required columns for the DIM_ISSUER table (IssuerID will be auto-generated by IDENTITY)
        lit(None).alias("UltimateParentIssuerID"),
        substr(trim(col("LegalName")), 1, 255).alias("LegalName"),  # Ensure it fits column
        concat(
            lit("LEI"),
            to_varchar(abs_func(hash_func(col("LegalName"))) % lit(1000000))
        ).substr(1, 20).alias("LEI"),  # Generate LEI with proper format
        col("CountryOfIncorporation"),
        col("INDUSTRY_SECTOR").alias("GICS_Sector")  # Keep same column name for compatibility
    ))
    
    # Create temporary table then use SQL INSERT to handle IDENTITY column properly
    issuers_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_ISSUERS")
    
    # Use SQL INSERT to populate DIM_ISSUER with IDENTITY column
    session.sql(f"""
        INSERT INTO {config.DATABASE_NAME}.CURATED.DIM_ISSUER (
            UltimateParentIssuerID, LegalName, LEI, CountryOfIncorporation, GICS_Sector
        )
        SELECT 
            UltimateParentIssuerID, LegalName, LEI, CountryOfIncorporation, GICS_Sector
        FROM {config.DATABASE_NAME}.RAW.TEMP_ISSUERS
    """).collect()
    
    # Clean up temp table
    session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_ISSUERS").collect()
    
    issuer_count = issuers_df.count()
    print(f"    ✅ Created {issuer_count} issuers from real asset data using Snowpark operations")

def generate_optimized_securities(session: Session, selected_assets_df):
    """Build security dimension from selected assets using efficient Snowpark operations"""
    from snowflake.snowpark.functions import (
        col, lit, ifnull, row_number, when, substr, trim
    )
    from snowflake.snowpark import Window
    
    # Create securities DataFrame with join to issuers for IssuerID lookup
    securities_df = (selected_assets_df
        .join(
            session.table(f"{config.DATABASE_NAME}.CURATED.DIM_ISSUER"),
            ifnull(selected_assets_df.col("ISSUER_NAME"), selected_assets_df.col("SECURITY_NAME")) == 
            session.table(f"{config.DATABASE_NAME}.CURATED.DIM_ISSUER").col("LegalName"),
            "inner"
        )
        .select(
            session.table(f"{config.DATABASE_NAME}.CURATED.DIM_ISSUER").col("IssuerID"),
            selected_assets_df.col("PRIMARY_TICKER").alias("PrimaryTicker"),
            ifnull(
                selected_assets_df.col("SECURITY_NAME"), 
                selected_assets_df.col("PRIMARY_TICKER")
            ).alias("Description"),
            ifnull(selected_assets_df.col("ASSET_CATEGORY"), lit("Equity")).alias("AssetClass"),
            when(selected_assets_df.col("ASSET_CATEGORY") == lit("Equity"), lit("Common Stock"))
            .otherwise(selected_assets_df.col("ASSET_CATEGORY")).alias("SecurityType"),
            ifnull(selected_assets_df.col("COUNTRY_OF_DOMICILE"), lit("US")).alias("CountryOfRisk"),
            lit(True).alias("IsActive")
        )
    )
    
    # Create temporary table then use SQL INSERT to handle IDENTITY column properly
    securities_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_SECURITIES")
    
    # Use SQL INSERT to populate DIM_SECURITY with IDENTITY column
    session.sql(f"""
        INSERT INTO {config.DATABASE_NAME}.CURATED.DIM_SECURITY (
            IssuerID, PrimaryTicker, Description, AssetClass, SecurityType, CountryOfRisk, IsActive
        )
        SELECT 
            IssuerID, PrimaryTicker, Description, AssetClass, SecurityType, CountryOfRisk, IsActive
        FROM {config.DATABASE_NAME}.RAW.TEMP_SECURITIES
    """).collect()
    
    # Clean up temp table
    session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_SECURITIES").collect()
    
    security_count = securities_df.count()
    print(f"    ✅ Created {security_count} securities from real asset data using Snowpark operations")

def report_generation_statistics(session: Session, selected_assets_df):
    """Report generation statistics using Snowpark aggregations"""
    from snowflake.snowpark.functions import col, count
    
    # Region distribution
    region_stats = (selected_assets_df
        .group_by(col("MARKET_REGION"))
        .agg(count("*").alias("COUNT"))
        .collect()
    )
    
    # Asset class distribution  
    asset_stats = (selected_assets_df
        .group_by(col("ASSET_CATEGORY"))
        .agg(count("*").alias("COUNT"))
        .collect()
    )
    
    print("    📊 Region distribution:")
    for row in region_stats:
        print(f"       {row['MARKET_REGION']}: {row['COUNT']}")
        
    print("    📊 Asset class distribution:")
    for row in asset_stats:
        print(f"       {row['ASSET_CATEGORY']}: {row['COUNT']}")

# def generate_synthetic_assets(session: Session):
#     """Generate synthetic issuers and securities (fallback) - DEPRECATED"""
#     # This function is no longer used since real assets CSV is now mandatory
#     # Keeping commented for reference but not actively maintained
#     pass

def generate_security_identifiers(session: Session, securities_data):
    """Generate security identifier cross-reference table"""
    
    xref_data = []
    for i, security in enumerate(securities_data, 1):
        ticker = security['PrimaryTicker']
        
        # Create TICKER identifier
        xref_data.append({
            'SecurityID': i,
            'IdentifierType': 'TICKER',
            'IdentifierValue': ticker,
            'EffectiveStartDate': config.get_history_start_date(),
            'EffectiveEndDate': datetime(2099, 12, 31).date(),
            'IsPrimaryForType': True
        })
        
        # Create CUSIP identifier (synthetic)
        xref_data.append({
            'SecurityID': i,
            'IdentifierType': 'CUSIP',
            'IdentifierValue': f"{abs(hash(ticker)) % 100000000:08d}",
            'EffectiveStartDate': config.get_history_start_date(),
            'EffectiveEndDate': datetime(2099, 12, 31).date(),
            'IsPrimaryForType': True
        })
    
    xref_df = session.create_dataframe(xref_data)
    xref_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.DIM_SECURITY_IDENTIFIER_XREF", )

def generate_portfolios_and_accounts(session: Session):
    """Generate client accounts first, then account-specific portfolios"""
    print("    → Generating accounts and portfolios...")
    
    # Step 1: Generate client accounts first
    clients = session.sql(f"SELECT ClientID, OnboardingDate FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT").collect()
    accounts_data = []
    
    for client in clients:
        client_id = client['CLIENTID']
        # Create 2 accounts per client as specified
        for i in range(config.ACCOUNTS_PER_CLIENT):
            account_id = f"ACC{client_id:04d}{i+1:02d}"
            model_portfolios = ['US MegaTech Focus', 'US Financials Core', 'Balanced Growth', 'Conservative Income']
            portfolio_name = py_random.choice(model_portfolios)
            
            accounts_data.append({
                'ACCOUNTID': account_id,
                'CLIENTID': client_id,
                'ACCOUNTTYPE': py_random.choice(['Brokerage', 'IRA', '401k']),
                'MODELPORTFOLIONAME': portfolio_name,
                'OPENDATE': client['ONBOARDINGDATE'],
                'ISACTIVE': True
            })
    
    # Create accounts using write_pandas
    import pandas as pd
    accounts_df = pd.DataFrame(accounts_data)
    session.write_pandas(
        accounts_df,
        "CURATED.DIM_ACCOUNT",
        overwrite=True,
        quote_identifiers=False
    )
    print(f"    ✅ Generated {len(accounts_data)} accounts")
    
    # Step 2: Now create account-specific portfolios
    accounts = session.sql(f"""
        SELECT AccountID, ClientID, ModelPortfolioName
        FROM {config.DATABASE_NAME}.CURATED.DIM_ACCOUNT
        ORDER BY AccountID
    """).collect()
    
    # Create account-specific portfolios following wealth management model
    portfolios_data = []
    for account in accounts:
        account_id = account['ACCOUNTID']
        model_name = account['MODELPORTFOLIONAME']
        
        portfolios_data.append({
            'AccountID': account_id,
            'PortfolioCode': f'PORT_{account_id}',
            'PortfolioName': f'{model_name} - {account_id}',
            'Strategy': model_name.split()[-1] if len(model_name.split()) > 1 else model_name,
            'BaseCurrency': 'USD',
            'InceptionDate': config.get_history_start_date(),
            'IsActive': True
        })
    
    # Use pandas and write_pandas for efficient bulk insert
    import pandas as pd
    
    # Convert to pandas DataFrame with proper column names including AccountID
    portfolios_df_data = []
    for portfolio in portfolios_data:
        portfolios_df_data.append({
            'ACCOUNTID': portfolio['AccountID'],
            'PORTFOLIOCODE': portfolio['PortfolioCode'],
            'PORTFOLIONAME': portfolio['PortfolioName'],
            'STRATEGY': portfolio['Strategy'],
            'BASECURRENCY': portfolio['BaseCurrency'],
            'INCEPTIONDATE': portfolio['InceptionDate'],
            'ISACTIVE': portfolio['IsActive']
        })
    
    portfolios_df = pd.DataFrame(portfolios_df_data)
    session.write_pandas(
        portfolios_df,
        "CURATED.DIM_PORTFOLIO",  # Use schema-qualified name
        overwrite=True,
        quote_identifiers=False
    )
    
    print(f"    ✅ Generated {len(accounts_data)} accounts and {len(portfolios_data)} portfolios")

def generate_simplified_positions(session: Session):
    """Generate simplified positions for demo purposes"""
    print("    → Generating transactions and positions...")
    
    # Create the positions table structure first
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR AS
        WITH portfolios AS (
            SELECT PortfolioID, PortfolioName
            FROM {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO
        ),
        securities AS (
            SELECT SecurityID, PrimaryTicker, AssetClass
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY
            WHERE IsActive = TRUE
        ),
        position_data AS (
            SELECT 
                '{config.get_history_end_date()}' as HoldingDate,
                p.PortfolioID,
                s.SecurityID,
                UNIFORM(100, 5000, RANDOM()) as Quantity,
                UNIFORM(50, 500, RANDOM()) * UNIFORM(100, 5000, RANDOM()) as MarketValue_Base
            FROM portfolios p
            CROSS JOIN securities s
            WHERE UNIFORM(0, 1, RANDOM()) < 0.3  -- 30% chance of holding each security
        )
        SELECT 
            HoldingDate::date as HoldingDate,
            PortfolioID,
            SecurityID,
            Quantity,
            MarketValue_Base as MarketValue_Local,
            MarketValue_Base,
            MarketValue_Base * 0.95 as CostBasis_Local,
            MarketValue_Base * 0.95 as CostBasis_Base,
            0 as AccruedInterest_Local,
            MarketValue_Base / SUM(MarketValue_Base) OVER (PARTITION BY PortfolioID) as PortfolioWeight
        FROM position_data
    """).collect()
    
    # Now generate golden portfolio positions for golden clients
    print("    → Applying golden portfolio allocations...")
    
    # Get all clients and their portfolios to check for golden clients
    client_portfolios = session.sql(f"""
        SELECT 
            c.ClientID,
            c.FirstName,
            c.LastName,
            p.PortfolioID
        FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT c
        JOIN {config.DATABASE_NAME}.CURATED.DIM_ACCOUNT a ON c.ClientID = a.ClientID
        JOIN {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO p ON a.AccountID = p.AccountID
        WHERE c.IsActive = TRUE
    """).collect()
    
    golden_clients_processed = 0
    
    for client_portfolio in client_portfolios:
        client_name = f"{client_portfolio['FIRSTNAME']} {client_portfolio['LASTNAME']}"
        
        # Check if this is a golden client
        golden_config = config.get_golden_client_config(client_name)
        if golden_config:
            # Clear existing positions for this portfolio
            session.sql(f"""
                DELETE FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR 
                WHERE PortfolioID = {client_portfolio['PORTFOLIOID']}
            """).collect()
            
            # Generate golden positions
            success = generate_golden_portfolio_positions(
                session, 
                client_portfolio['CLIENTID'], 
                client_portfolio['PORTFOLIOID']
            )
            
            if success:
                golden_clients_processed += 1
                print(f"    ✅ Applied golden allocations for {client_name}")
    
    print(f"    ✅ Generated positions ({golden_clients_processed} golden clients processed)")

def generate_market_data(session: Session):
    """Generate synthetic market data time series for demo purposes"""
    print("    → Generating synthetic market data...")
    
    # Use only synthetic generation for consistent, predictable demo data
    generate_synthetic_market_data(session)

# def generate_hybrid_market_data(session: Session, real_market_df: pd.DataFrame):
#     """Generate market data using hybrid approach with real data - DEPRECATED"""
#     # This function is no longer used since we now use only synthetic market data
#     # Keeping commented for reference but not actively maintained
#     pass

def generate_advisor_client_relationships(session: Session):
    """Generate advisor-client relationship history"""
    print("    → Generating advisor-client relationships...")
    
    # Get all clients with their advisors and dates
    clients = session.sql("""
        SELECT ClientID, AdvisorID, OnboardingDate, EndDate, IsActive
        FROM CURATED.DIM_CLIENT
    """).collect()
    
    relationships_data = []
    for client in clients:
        # Create primary relationship
        relationships_data.append({
            'ADVISORID': client['ADVISORID'],
            'CLIENTID': client['CLIENTID'],
            'STARTDATE': client['ONBOARDINGDATE'],
            'ENDDATE': client['ENDDATE'],
            'RELATIONSHIPSTATUS': 'Terminated' if client['ENDDATE'] else 'Active'
        })
        
        # For some clients, generate advisor transfer history (10% chance)
        if py_random.random() < 0.10 and client['ONBOARDINGDATE']:
            # Get different advisor
            advisors = session.sql("SELECT AdvisorID FROM CURATED.DIM_ADVISOR").collect()
            previous_advisor = py_random.choice([a['ADVISORID'] for a in advisors if a['ADVISORID'] != client['ADVISORID']])
            
            # Create previous relationship
            transfer_date = client['ONBOARDINGDATE'] + timedelta(days=py_random.randint(90, 365))
            relationships_data.append({
                'ADVISORID': previous_advisor,
                'CLIENTID': client['CLIENTID'],
                'STARTDATE': client['ONBOARDINGDATE'],
                'ENDDATE': transfer_date,
                'RELATIONSHIPSTATUS': 'Transferred'
            })
            
            # Update current relationship start date
            relationships_data[-2]['STARTDATE'] = transfer_date
    
    import pandas as pd
    relationships_df = pd.DataFrame(relationships_data)
    session.write_pandas(relationships_df, "CURATED.FACT_ADVISOR_CLIENT_RELATIONSHIP", overwrite=True, quote_identifiers=False)
    print(f"      ✅ Generated {len(relationships_data)} relationship records")

def generate_advisor_roster(session: Session):
    """Generate advisor roster summary"""
    print("    → Generating advisor roster...")
    
    # Get advisor and manager data
    advisor_data = session.sql("""
        SELECT a.AdvisorID, a.FirstName || ' ' || a.LastName as AdvisorName,
               a.ManagerID, m.ManagerName, a.Team as TeamName, a.IsActive as ActiveFlag
        FROM CURATED.DIM_ADVISOR a
        LEFT JOIN CURATED.DIM_MANAGER m ON a.ManagerID = m.ManagerID
    """).collect()
    
    # Calculate current AUM per advisor for peer grouping
    aum_data = session.sql("""
        SELECT a.AdvisorID, COALESCE(SUM(p.MarketValue_Base), 0) as CurrentAUM
        FROM CURATED.DIM_ADVISOR a
        LEFT JOIN CURATED.DIM_CLIENT c ON a.AdvisorID = c.AdvisorID AND c.IsActive = TRUE
        LEFT JOIN CURATED.DIM_ACCOUNT acc ON c.ClientID = acc.ClientID AND acc.IsActive = TRUE
        LEFT JOIN CURATED.DIM_PORTFOLIO po ON acc.AccountID = po.AccountID AND po.IsActive = TRUE
        LEFT JOIN CURATED.FACT_POSITION_DAILY_ABOR p ON po.PortfolioID = p.PortfolioID 
            AND p.HoldingDate = CURRENT_DATE()
        GROUP BY a.AdvisorID
    """).collect()
    
    # Create AUM lookup
    aum_lookup = {row['ADVISORID']: row['CURRENTAUM'] for row in aum_data}
    
    roster_data = []
    for advisor in advisor_data:
        current_aum = aum_lookup.get(advisor['ADVISORID'], 0)
        
        # Determine peer group based on AUM
        if current_aum < config.PEER_GROUP_THRESHOLDS['small_max']:
            peer_group = 'Small'
        elif current_aum < config.PEER_GROUP_THRESHOLDS['medium_max']:
            peer_group = 'Medium'
        else:
            peer_group = 'Large'
        
        roster_data.append({
            'ADVISORID': advisor['ADVISORID'],
            'ADVISORNAME': advisor['ADVISORNAME'],
            'MANAGERID': advisor['MANAGERID'],
            'MANAGERNAME': advisor['MANAGERNAME'],
            'TEAMNAME': advisor['TEAMNAME'],
            'PEERGROUP': peer_group,
            'STARTDATE': config.get_history_start_date(),
            'ACTIVEFLAG': advisor['ACTIVEFLAG']
        })
    
    import pandas as pd
    roster_df = pd.DataFrame(roster_data)
    session.write_pandas(roster_df, "CURATED.ADVISOR_ROSTER", overwrite=True, quote_identifiers=False)
    print(f"      ✅ Generated advisor roster for {len(roster_data)} advisors")

def generate_advisor_summary_ttm(session: Session):
    """Generate TTM advisor performance summary"""
    print("    → Generating advisor TTM summary...")
    
    # For now, create placeholder data - in a real implementation this would calculate actual metrics
    advisors = session.sql("SELECT AdvisorID, PeerGroup FROM CURATED.ADVISOR_ROSTER").collect()
    
    summary_data = []
    for advisor in advisors:
        # Generate realistic but simplified TTM metrics
        advisor_id = advisor['ADVISORID']
        peer_group = advisor['PEERGROUP']
        
        # Base AUM varies by peer group
        if peer_group == 'Small':
            base_aum = py_random.uniform(10_000_000, 40_000_000)
        elif peer_group == 'Medium':
            base_aum = py_random.uniform(60_000_000, 120_000_000)
        else:
            base_aum = py_random.uniform(160_000_000, 300_000_000)
        
        # Generate metrics with some variance
        starting_aum = base_aum * py_random.uniform(0.9, 1.1)
        ending_aum = starting_aum * py_random.uniform(0.95, 1.15)
        net_flows = py_random.uniform(-0.05, 0.10) * starting_aum
        
        summary_data.append({
            'ADVISORID': advisor_id,
            'PERIODENDDATE': config.get_history_end_date(),
            'STARTINGAUM': round(starting_aum, 2),
            'ENDINGAUM': round(ending_aum, 2),
            'INFLOWS': round(max(0, net_flows), 2),
            'OUTFLOWS': round(abs(min(0, net_flows)), 2),
            'NETFLOWS': round(net_flows, 2),
            'CLIENTSSTART': py_random.randint(20, 30),
            'CLIENTSLOST': py_random.randint(0, 3),
            'CLIENTSEND': py_random.randint(20, 30),
            'AUMLOSTFROMDEPARTURES': round(py_random.uniform(0, starting_aum * 0.05), 2),
            'INTERACTIONSCOUNT': py_random.randint(300, 800),
            'UNIQUECLIENTSCONTACTED': py_random.randint(20, 25),
            'AVGDAYSBETWEENCONTACTS': round(py_random.uniform(25, 45), 1),
            'POSITIVEPCT': round(py_random.uniform(20, 35), 1),
            'NEUTRALPCT': round(py_random.uniform(50, 70), 1),
            'NEGATIVEPCT': round(py_random.uniform(5, 20), 1),
            'PLANNINGHOUSEHOLDS': py_random.randint(15, 22),
            'TOTALHOUSEHOLDS': py_random.randint(20, 25),
            'PLANNINGCOVERAGEPCT': round(py_random.uniform(60, 90), 1),
            'AVGAUM_TTM': round((starting_aum + ending_aum) / 2, 2),
            'REVENUE_TTM': round(((starting_aum + ending_aum) / 2) * 0.0075, 2),  # ~0.75% avg fee
            'RISKFLAGS': py_random.randint(0, 8),
            'RISKFLAGSPER100': round(py_random.uniform(0.5, 3.0), 2),
            'PEERGROUP': peer_group
        })
    
    import pandas as pd
    summary_df = pd.DataFrame(summary_data)
    session.write_pandas(summary_df, "CURATED.ADVISOR_SUMMARY_TTM", overwrite=True, quote_identifiers=False)
    print(f"      ✅ Generated TTM summary for {len(summary_data)} advisors")

def generate_synthetic_market_data(session: Session):
    """Generate synthetic market data time series for consistent demo experience"""
    print("    → Generating synthetic market data with realistic patterns...")
    
    session.sql(f"""
        CREATE OR REPLACE TABLE {config.DATABASE_NAME}.CURATED.FACT_MARKETDATA_TIMESERIES AS
        WITH business_dates AS (
            SELECT DATEADD(day, seq4(), '{config.get_history_start_date()}') as price_date
            FROM TABLE(GENERATOR(rowcount => {config.get_market_data_rowcount()}))
            WHERE DAYOFWEEK(price_date) BETWEEN 2 AND 6
              AND price_date <= '{config.get_history_end_date()}'
        ),
        securities AS (
            SELECT ROW_NUMBER() OVER (ORDER BY PrimaryTicker) as SecurityID, PrimaryTicker
            FROM {config.DATABASE_NAME}.CURATED.DIM_SECURITY
            WHERE IsActive = TRUE
        )
        SELECT 
            bd.price_date as PriceDate,
            s.SecurityID,
            UNIFORM(50, 500, RANDOM()) as Price_Close,
            UNIFORM(45, 495, RANDOM()) as Price_Open,
            UNIFORM(55, 505, RANDOM()) as Price_High,
            UNIFORM(40, 490, RANDOM()) as Price_Low,
            UNIFORM(1000, 1000000, RANDOM()) as Volume,
            1.0 as TotalReturnFactor_Daily
        FROM business_dates bd
        CROSS JOIN securities s
    """).collect()
    
    # Report generation statistics
    market_data_stats = session.sql(f"""
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT SecurityID) as unique_securities,
            MIN(PriceDate) as start_date,
            MAX(PriceDate) as end_date
        FROM {config.DATABASE_NAME}.CURATED.FACT_MARKETDATA_TIMESERIES
    """).collect()
    
    if market_data_stats:
        stats = market_data_stats[0]
        print(f"    ✅ Generated synthetic market data: {stats['TOTAL_RECORDS']:,} records")
        print(f"    📊 {stats['UNIQUE_SECURITIES']} securities with price history")
        print(f"    📅 Date range: {stats['START_DATE']} to {stats['END_DATE']}")
    else:
        print("    ✅ Generated synthetic market data")
