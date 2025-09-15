"""
WAM AI Demo - Real Data Extraction
Extracts real asset and market data from Snowflake Marketplace to CSV files
"""

from snowflake.snowpark import Session
import config
import os
import pandas as pd
from datetime import datetime, timedelta

def extract_real_assets_to_csv(session: Session):
    """Extract real assets using OpenFIGI standard to CSV"""
    
    print("  → Extracting real assets from Snowflake Marketplace...")
    
    # Check if Marketplace data is accessible
    try:
        session.sql(f"SELECT 1 FROM {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.OPENFIGI_SECURITY_INDEX LIMIT 1").collect()
        print("    ✅ Marketplace data accessible")
    except Exception as e:
        print(f"    ❌ Error: Marketplace data not accessible!")
        print(f"       {e}")
        print("    💡 You need access to 'Public Data Financials & Economics: Enterprise' dataset")
        print("       from Snowflake Marketplace")
        return False
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Extract real assets using the provided SQL
    assets_sql = f"""
    WITH
    Enriched_Securities AS (
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
            -- Extract Country of Domicile from company characteristics
            MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'business_address_country' THEN char.VALUE END) AS COUNTRY_OF_DOMICILE,
            -- Use SIC Description as a proxy for industry, as GICS is not in this base dataset
            MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'sic_description' THEN char.VALUE END) AS INDUSTRY_SECTOR
        FROM
            {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.OPENFIGI_SECURITY_INDEX AS osi
        LEFT JOIN
            {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.COMPANY_SECURITY_RELATIONSHIPS AS rship 
                ON osi.TOP_LEVEL_OPENFIGI_ID = rship.SECURITY_ID AND osi.TOP_LEVEL_OPENFIGI_ID_TYPE = rship.security_id_type
        LEFT JOIN
            {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.COMPANY_INDEX AS ci ON rship.COMPANY_ID = ci.COMPANY_ID
        LEFT JOIN
            {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.COMPANY_CHARACTERISTICS AS char ON rship.COMPANY_ID = char.COMPANY_ID
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
            ci.COMPANY_NAME
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
            -- Market Region Classification Logic
            CASE
                WHEN es.COUNTRY_OF_DOMICILE = 'US' THEN 'USA'
                WHEN es.COUNTRY_OF_DOMICILE IN (
                    'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
                    'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
                    'SI', 'ES', 'SE'
                ) THEN 'EU'
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
    -- Final SELECT Statement
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
        cs.EXCHANGE_CODES
    FROM
        Categorized_Securities cs
    WHERE
        cs.ASSET_CATEGORY IS NOT NULL
        AND cs.PRIMARY_TICKER IS NOT NULL
        AND LENGTH(cs.PRIMARY_TICKER) <= 10  -- Filter out overly long tickers
    ORDER BY
        cs.MARKET_REGION,
        cs.ASSET_CATEGORY,
        cs.ISSUER_NAME,
        cs.SECURITY_NAME
    """
    
    try:
        print("    → Running asset extraction query...")
        result = session.sql(assets_sql).collect()
        
        if not result:
            print("    ❌ No assets extracted from Marketplace")
            return False
        
        # Convert to pandas DataFrame
        df = pd.DataFrame([row.asDict() for row in result])
        
        # Apply region mix filter to get balanced dataset
        region_counts = df['MARKET_REGION'].value_counts()
        print(f"    📊 Extracted assets by region:")
        for region, count in region_counts.items():
            print(f"       {region}: {count:,}")
        
        # Apply some filtering to get a manageable dataset
        # Prioritize US and EU to match the 80/20 mix
        filtered_df = pd.concat([
            df[df['MARKET_REGION'] == 'USA'].head(2000),  # Top 2000 US securities
            df[df['MARKET_REGION'] == 'EU'].head(500),    # Top 500 EU securities
            df[df['MARKET_REGION'] == 'APAC/EM'].head(300) # Top 300 APAC/EM securities
        ])
        
        # Ensure golden tickers are included
        golden_tickers_df = df[df['PRIMARY_TICKER'].isin(config.GOLDEN_TICKERS)]
        if not golden_tickers_df.empty:
            filtered_df = pd.concat([filtered_df, golden_tickers_df]).drop_duplicates()
        
        # Save to CSV
        filtered_df.to_csv(config.REAL_ASSETS_CSV_PATH, index=False)
        
        print(f"    ✅ Extracted {len(filtered_df):,} real assets to {config.REAL_ASSETS_CSV_PATH}")
        print(f"    📋 Final dataset breakdown:")
        final_counts = filtered_df['MARKET_REGION'].value_counts()
        for region, count in final_counts.items():
            print(f"       {region}: {count:,}")
        
        # Show asset class distribution
        asset_counts = filtered_df['ASSET_CATEGORY'].value_counts()
        print(f"    📊 Asset class distribution:")
        for asset_class, count in asset_counts.items():
            print(f"       {asset_class}: {count:,}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Failed to extract real assets: {e}")
        return False

def extract_real_market_data_to_csv(session: Session):
    """Extract real market data for selected tickers to CSV"""
    
    print("  → Extracting real market data from Snowflake Marketplace...")
    
    # Check if Marketplace data is accessible
    try:
        session.sql(f"SELECT 1 FROM {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.STOCK_PRICE_TIMESERIES LIMIT 1").collect()
        print("    ✅ Market data accessible")
    except Exception as e:
        print(f"    ❌ Error: Market data not accessible!")
        print(f"       {e}")
        print("    💡 You need access to 'Public Data Financials & Economics: Enterprise' dataset")
        print("       from Snowflake Marketplace")
        return False
    
    # Create data directory
    os.makedirs('data', exist_ok=True)
    
    # Determine which tickers to extract
    tickers_to_extract = config.GOLDEN_TICKERS.copy()
    
    # If real assets CSV exists, get additional tickers from there
    if os.path.exists(config.REAL_ASSETS_CSV_PATH):
        try:
            assets_df = pd.read_csv(config.REAL_ASSETS_CSV_PATH)
            # Get additional US tickers for market data
            us_tickers = assets_df[
                (assets_df['MARKET_REGION'] == 'USA') & 
                (assets_df['ASSET_CATEGORY'] == 'Equity')
            ]['PRIMARY_TICKER'].head(50).tolist()  # Top 50 US equities
            
            tickers_to_extract.extend(us_tickers)
            tickers_to_extract = list(set(tickers_to_extract))  # Remove duplicates
            print(f"    📊 Using {len(us_tickers)} additional tickers from real assets CSV")
        except Exception as e:
            print(f"    ⚠️ Could not read real assets CSV, using golden tickers only: {e}")
    
    # Create ticker list for SQL
    ticker_list = "'" + "', '".join(tickers_to_extract) + "'"
    
    # Set date range for market data (last 2 years)
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=730)  # 2 years
    
    market_data_sql = f"""
    SELECT 
        TICKER,
        DATE,
        PRIMARY_EXCHANGE_CODE,
        PRIMARY_EXCHANGE_NAME,
        MAX(CASE WHEN VARIABLE = 'pre-market_open' THEN VALUE END) as OPEN_PRICE,
        MAX(CASE WHEN VARIABLE = 'all-day_high' THEN VALUE END) as HIGH_PRICE,
        MAX(CASE WHEN VARIABLE = 'all-day_low' THEN VALUE END) as LOW_PRICE,
        MAX(CASE WHEN VARIABLE = 'post-market_close' THEN VALUE END) as CLOSE_PRICE,
        MAX(CASE WHEN VARIABLE = 'nasdaq_volume' THEN VALUE END) as VOLUME
    FROM {config.MARKETPLACE_DATABASE}.{config.OPENFIGI_SCHEMA}.STOCK_PRICE_TIMESERIES
    WHERE TICKER IN ({ticker_list})
        AND DATE >= '{start_date}'
        AND DATE <= '{end_date}'
    GROUP BY TICKER, DATE, PRIMARY_EXCHANGE_CODE, PRIMARY_EXCHANGE_NAME
    HAVING 
        CLOSE_PRICE IS NOT NULL  -- Only require close price
    ORDER BY TICKER, DATE
    """
    
    try:
        print(f"    → Extracting market data for {len(tickers_to_extract)} tickers...")
        print(f"    → Date range: {start_date} to {end_date}")
        
        result = session.sql(market_data_sql).collect()
        
        if not result:
            print("    ❌ No market data extracted from Marketplace")
            return False
        
        # Convert to pandas DataFrame
        df = pd.DataFrame([row.asDict() for row in result])
        
        # Data quality checks
        ticker_counts = df['TICKER'].value_counts()
        print(f"    📊 Market data extracted:")
        print(f"       Total records: {len(df):,}")
        print(f"       Unique tickers: {len(ticker_counts)}")
        print(f"       Date range: {df['DATE'].min()} to {df['DATE'].max()}")
        
        # Show top tickers by data availability
        print(f"    📈 Top tickers by data points:")
        for ticker, count in ticker_counts.head(10).items():
            print(f"       {ticker}: {count:,} records")
        
        # Save to CSV
        df.to_csv(config.REAL_MARKET_DATA_CSV_PATH, index=False)
        
        print(f"    ✅ Extracted {len(df):,} market data records to {config.REAL_MARKET_DATA_CSV_PATH}")
        
        return True
        
    except Exception as e:
        print(f"    ❌ Failed to extract real market data: {e}")
        return False

def load_real_assets_from_csv() -> pd.DataFrame:
    """Load real assets from CSV file with error handling - REQUIRED for operation"""
    
    if not os.path.exists(config.REAL_ASSETS_CSV_PATH):
        error_msg = f"❌ REQUIRED FILE MISSING: Real assets CSV file not found at {config.REAL_ASSETS_CSV_PATH}"
        print(f"    {error_msg}")
        print("    ")
        print("    To fix this, you need to:")
        print("    1. Ensure you have access to 'Public Data Financials & Economics: Enterprise' dataset")
        print("    2. Run: python main.py --extract-real-assets")
        print("    3. Then run your normal build command")
        print("    ")
        print("    This system now requires real assets data for enhanced demo authenticity.")
        raise FileNotFoundError(error_msg)
    
    try:
        df = pd.read_csv(config.REAL_ASSETS_CSV_PATH)
        print(f"    ✅ Loaded {len(df):,} real assets from CSV")
        return df
    except Exception as e:
        error_msg = f"❌ REQUIRED FILE CORRUPTED: Error loading real assets CSV: {e}"
        print(f"    {error_msg}")
        print("    Please re-extract the real assets by running: python main.py --extract-real-assets")
        raise RuntimeError(error_msg)

def load_real_market_data_from_csv() -> pd.DataFrame:
    """Load real market data from CSV file with error handling"""
    
    if not os.path.exists(config.REAL_MARKET_DATA_CSV_PATH):
        print("    ❌ Error: Real market data CSV file not found!")
        print(f"       Expected location: {config.REAL_MARKET_DATA_CSV_PATH}")
        print("       To use real market data, you need:")
        print("       1. Access to 'Public Data Financials & Economics: Enterprise' dataset") 
        print("       2. Run: python main.py --extract-real-market-data")
        print("       3. Then run your normal build command")
        print("       Falling back to synthetic market data generation...")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(config.REAL_MARKET_DATA_CSV_PATH)
        print(f"    ✅ Loaded {len(df):,} real market data records from CSV")
        return df
    except Exception as e:
        print(f"    ❌ Error loading real market data CSV: {e}")
        print("       Falling back to synthetic market data generation...")
        return pd.DataFrame()
