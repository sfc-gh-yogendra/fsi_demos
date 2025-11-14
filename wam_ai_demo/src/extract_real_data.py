"""
WAM AI Demo - Real Data Extraction
Direct querying of real asset data from SEC Filings Marketplace database
"""

from snowflake.snowpark import Session
import config
import sys
from datetime import datetime, timedelta


def validate_sec_filings_access(session: Session) -> bool:
    """
    Validate access to SEC Filings database and schema.
    Returns False and prints error message with marketplace links if not accessible.
    """
    database = config.SECURITIES['sec_filings_database']
    schema = config.SECURITIES['sec_filings_schema']
    
    print(f"  → Validating SEC Filings database access...")
    
    # Ensure warehouse is active
    try:
        session.sql(f"USE WAREHOUSE {config.BUILD_WAREHOUSE}").collect()
    except:
        pass  # Ignore if warehouse doesn't exist yet
    
    # Check database exists
    try:
        result = session.sql(f"SHOW DATABASES LIKE '{database}'").collect()
        if not result:
            print(f"❌ SEC_FILINGS database '{database}' not accessible")
            print(f"   ")
            print(f"   Required: Access to SEC Filings data from Snowflake Marketplace")
            print(f"   ")
            print(f"   Option 1: SEC Filings Dataset")
            print(f"   https://app.snowflake.com/marketplace/listing/GZTSZAS2KH9/snowflake-public-data-products-sec-filings")
            print(f"   ")
            print(f"   Option 2: Snowflake Public Data (Free)")
            print(f"   https://app.snowflake.com/marketplace/listing/GZTSZ290BV255/snowflake-public-data-products-snowflake-public-data-free")
            print(f"   ")
            print(f"   Note: If using Snowflake Public Data (Free), update SECURITIES dict in config.py")
            print(f"   ")
            return False
        print(f"    ✅ Database '{database}' found")
    except Exception as e:
        print(f"❌ Error checking database '{database}': {e}")
        return False
    
    # Check schema exists
    try:
        result = session.sql(f"SHOW SCHEMAS IN DATABASE {database}").collect()
        schema_names = [row['name'] for row in result]
        if schema not in schema_names:
            print(f"❌ Schema '{schema}' not found in database '{database}'")
            print(f"   Available schemas: {', '.join(schema_names[:5])}")
            print(f"   Check your Marketplace subscription and SECURITIES configuration in config.py")
            return False
        print(f"    ✅ Schema '{schema}' found")
    except Exception as e:
        print(f"❌ Error checking schema '{schema}': {e}")
        return False
    
    # Test table access
    try:
        test_query = f"SELECT 1 FROM {database}.{schema}.OPENFIGI_SECURITY_INDEX LIMIT 1"
        session.sql(test_query).collect()
        print(f"    ✅ Table access verified")
    except Exception as e:
        print(f"❌ Error accessing tables in {database}.{schema}: {e}")
        print(f"   Verify you have SELECT permissions on the schema")
        return False
    
    print(f"  ✅ SEC Filings database access validated")
    return True


def load_real_assets_from_sec_filings(session: Session):
    """
    Load real assets directly from SEC Filings database using direct query.
    Returns Snowpark DataFrame with securities data including CIK for SEC filings integration.
    """
    database = config.SECURITIES['sec_filings_database']
    schema = config.SECURITIES['sec_filings_schema']
    
    print(f"  → Loading real assets from {database}.{schema}...")
    
    # Use the provided SQL query with config parameters
    assets_sql = f"""
    WITH Enriched_Securities AS (
        -- This CTE joins the main security index with geography, company characteristics, and aggregated exchange codes.
        SELECT
            osi.TOP_LEVEL_OPENFIGI_ID,
            osi.SECURITY_NAME,
            osi.ASSET_CLASS,
            osi.SECURITY_TYPE,
            osi.SECURITY_SUBTYPE,
            osi.PRIMARY_TICKER,
            ci.PRIMARY_EXCHANGE_CODE,
            ci.PRIMARY_EXCHANGE_NAME,
            osi.EXCHANGE_CODES,
            ci.COMPANY_NAME AS ISSUER_NAME,
            ci.CIK,  -- Extract CIK for SEC filings integration
            -- Extract Country of Domicile from company characteristics
            MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'business_address_country' THEN char.VALUE END) AS COUNTRY_OF_DOMICILE,
            -- Use SIC Description as a proxy for industry, as GICS is not in this base dataset
            MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'sic_description' THEN char.VALUE END) AS INDUSTRY_SECTOR
        FROM
            {database}.{schema}.OPENFIGI_SECURITY_INDEX AS osi
        LEFT JOIN
            {database}.{schema}.COMPANY_SECURITY_RELATIONSHIPS AS rship 
                ON osi.TOP_LEVEL_OPENFIGI_ID = rship.SECURITY_ID AND osi.TOP_LEVEL_OPENFIGI_ID_TYPE = rship.security_id_type
        LEFT JOIN
            {database}.{schema}.COMPANY_INDEX AS ci ON rship.COMPANY_ID = ci.COMPANY_ID
        LEFT JOIN
            {database}.{schema}.COMPANY_CHARACTERISTICS AS char ON rship.COMPANY_ID = char.COMPANY_ID
        WHERE
            NOT (ARRAY_CONTAINS('CEDEAR'::variant, osi.SECURITY_TYPE) 
                OR ARRAY_CONTAINS('PRIV PLACEMENT'::variant, osi.SECURITY_TYPE)
                OR ARRAY_CONTAINS('Crypto'::variant, osi.SECURITY_TYPE))
        GROUP BY
            osi.TOP_LEVEL_OPENFIGI_ID,
            osi.SECURITY_NAME,
            osi.ASSET_CLASS,
            osi.SECURITY_TYPE,
            osi.SECURITY_SUBTYPE,
            osi.PRIMARY_TICKER,
            ci.PRIMARY_EXCHANGE_CODE,
            ci.PRIMARY_EXCHANGE_NAME,
            osi.EXCHANGE_CODES,
            ci.COMPANY_NAME,
            ci.CIK  -- Include CIK in GROUP BY
    ),
    Categorized_Securities AS (
        -- This CTE applies the asset class and market region logic to each security.
        SELECT
            es.TOP_LEVEL_OPENFIGI_ID,
            es.SECURITY_NAME,
            es.ISSUER_NAME,
            es.PRIMARY_TICKER,
            es.PRIMARY_EXCHANGE_CODE,
            IFNULL(es.PRIMARY_EXCHANGE_NAME, es.EXCHANGE_CODES[0]::varchar) AS PRIMARY_EXCHANGE_NAME,
            es.EXCHANGE_CODES,
            es.INDUSTRY_SECTOR,
            es.COUNTRY_OF_DOMICILE,
            es.CIK,  -- Pass through CIK
            -- Asset Category Classification Logic (Expanded to include more bond types)
            CASE
                WHEN es.ASSET_CLASS = 'Corp' THEN 'Corporate Bond'
                WHEN es.ASSET_CLASS = 'Govt' THEN 'Government Bond'
                WHEN es.ASSET_CLASS = 'Muni' THEN 'Municipal Bond'
                WHEN es.ASSET_CLASS = 'Mtge' THEN 'Mortgage-Backed Security'
                WHEN es.ASSET_CLASS = 'Equity' AND (
                    ARRAY_CONTAINS('ETF'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('Exchange Traded Fund'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('ETN'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('ETP'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('Unit Trust'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('UIT'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('Closed-End Fund'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('Open-End Fund'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('Fund of Funds'::variant, es.SECURITY_TYPE) OR
                    ARRAY_CONTAINS('Mutual Fund'::variant, es.SECURITY_SUBTYPE)
                ) THEN 'ETF'
                WHEN es.ASSET_CLASS = 'Equity' THEN 'Equity'
                ELSE NULL
            END AS ASSET_CATEGORY,
            -- Market Region Logic (USA included)
            CASE
                WHEN es.COUNTRY_OF_DOMICILE IN (
                    'AT', 'BE', 'BG', 'HR', 'CY', 'DK', 'EE', 'FI', 'FR', 'DE', 'GI', 'GG',
                    'GR', 'IS', 'IE', 'IM', 'IT', 'JE', 'LV', 'LI', 'LT', 'LU', 'MT', 'MC',
                    'NL', 'NO', 'PT', 'RO', 'SM', 'SK', 'SI', 'ES', 'SE', 'CH', 'GB', 'VA'
                ) THEN 'Europe'
                WHEN es.COUNTRY_OF_DOMICILE = 'US' THEN 'USA'
                WHEN es.COUNTRY_OF_DOMICILE IN (
                    'AF', 'AU', 'BD', 'BT', 'BR', 'BN', 'KH', 'CL', 'CN', 'CO', 'CK', 'CZ',
                    'KP', 'EG', 'FJ', 'GR', 'HK', 'HU', 'IN', 'ID', 'JP', 'KI', 'KW', 'LA',
                    'MY', 'MV', 'MH', 'MX', 'FM', 'MN', 'MM', 'NR', 'NP', 'NZ', 'PK', 'PW',
                    'PG', 'PE', 'PH', 'PL', 'QA', 'KR', 'WS', 'SA', 'SG', 'SB', 'ZA', 'LK',
                    'TW', 'TH', 'TL', 'TO', 'TR', 'TV', 'AE', 'VU', 'VN'
                ) THEN 'APAC/EM'
                ELSE 'Other'
            END AS MARKET_REGION
        FROM
            Enriched_Securities AS es
    )
    -- Final SELECT Statement with CIK included
    SELECT
        cs.MARKET_REGION,
        cs.ASSET_CATEGORY,
        cs.ISSUER_NAME,
        cs.INDUSTRY_SECTOR,
        cs.TOP_LEVEL_OPENFIGI_ID,
        cs.SECURITY_NAME,
        cs.PRIMARY_TICKER,
        cs.PRIMARY_EXCHANGE_CODE,
        cs.PRIMARY_EXCHANGE_NAME,
        cs.COUNTRY_OF_DOMICILE,
        cs.EXCHANGE_CODES,
        cs.CIK  -- Include CIK in final output
    FROM
        Categorized_Securities cs
    WHERE
        cs.ASSET_CATEGORY IS NOT NULL
    ORDER BY
        cs.MARKET_REGION,
        cs.ASSET_CATEGORY,
        cs.ISSUER_NAME,
        cs.SECURITY_NAME
    """
    
    try:
        # Execute query and return Snowpark DataFrame
        real_assets_df = session.sql(assets_sql)
        
        # Get count for reporting
        count = real_assets_df.count()
        print(f"    ✅ Loaded {count:,} real securities from SEC Filings")
        
        return real_assets_df
        
    except Exception as e:
        print(f"❌ Error loading real assets from SEC Filings: {e}")
        raise

