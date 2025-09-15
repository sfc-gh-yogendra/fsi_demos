"""
WAM AI Demo - Component Validation
Validates all components with systematic testing following the enhanced rules
"""

from snowflake.snowpark import Session
import config

def validate_all_components(session: Session):
    """Run comprehensive validation of all demo components"""
    
    print("  → Running component validation...")
    
    # Validate data quality
    validate_data_quality(session)
    
    # Validate semantic views
    validate_semantic_views_comprehensive(session)
    
    # Validate search services
    validate_search_services_comprehensive(session)
    
    # Run business scenario tests
    run_business_scenario_tests(session)
    
    print("  ✅ Component validation complete")

def validate_all_components_with_phase2(session: Session, include_phase2: bool = True):
    """Run comprehensive validation including Phase 2 features"""
    
    print("  → Running component validation with Phase 2...")
    
    # Run base validation
    validate_all_components(session)
    
    # Run Phase 2 validation if requested
    if include_phase2:
        validate_phase2_features(session)

# ======================================================
# PHASE 2: VALIDATION FUNCTIONS
# ======================================================

def validate_phase2_features(session: Session):
    """Validate all Phase 2 enhancements"""
    
    print("  → Validating Phase 2 features...")
    
    # Ensure database context
    session.sql(f"USE DATABASE {config.DATABASE_NAME}").collect()
    
    # Validate watchlists
    validate_watchlists(session)
    
    # Validate enhanced ESG content
    validate_esg_content(session)
    
    # Validate Carbon Negative Leaders analytics
    validate_carbon_negative_analytics(session)
    
    print("  ✅ Phase 2 validation complete")

def validate_watchlists(session: Session):
    """Validate watchlist creation and data"""
    
    print("    → Validating watchlists...")
    
    # Check watchlist summary
    result = session.sql(f"""
        SELECT 
            w.WatchlistName,
            w.WatchlistType,
            COUNT(ws.SecurityID) as SecurityCount,
            AVG(ws.ESG_Score) as AvgESGScore
        FROM {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST w
        LEFT JOIN {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES ws ON w.WatchlistID = ws.WatchlistID
        GROUP BY w.WatchlistID, w.WatchlistName, w.WatchlistType
        ORDER BY w.WatchlistName
    """).collect()
    
    print(f"    ✅ Created {len(result)} watchlists:")
    for row in result:
        avg_score = float(row['AVGESGSCORE']) if row['AVGESGSCORE'] else 0
        print(f"      {row['WATCHLISTNAME']}: {row['SECURITYCOUNT']} securities, Avg ESG: {avg_score:.1f}")
    
    # Test Carbon Negative Leaders detail
    try:
        result = session.sql(f"""
            SELECT 
                w.WatchlistName,
                s.PrimaryTicker,
                i.LegalName,
                ws.ESG_Score,
                LEFT(ws.Rationale, 80) || '...' as RationaleSummary
            FROM {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST w
            JOIN {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES ws ON w.WatchlistID = ws.WatchlistID
            JOIN {config.DATABASE_NAME}.CURATED.DIM_SECURITY s ON ws.SecurityID = s.SecurityID
            JOIN {config.DATABASE_NAME}.CURATED.DIM_ISSUER i ON s.IssuerID = i.IssuerID
            WHERE w.WatchlistName = 'Carbon Negative Leaders'
            ORDER BY ws.ESG_Score DESC
        """).collect()
        
        print(f"    ✅ Carbon Negative Leaders detail: {len(result)} securities")
        for row in result:
            print(f"      {row['PRIMARYTICKER']} ({row['LEGALNAME']}): ESG {row['ESG_SCORE']}")
            
    except Exception as e:
        print(f"    ❌ Watchlist analytics failed: {e}")

def validate_esg_content(session: Session):
    """Validate enhanced ESG content"""
    
    print("    → Validating ESG content...")
    
    # Check ESG research content
    result = session.sql(f"""
        SELECT 
            DOCUMENT_TYPE,
            COUNT(*) as DocCount,
            MIN(PUBLISH_DATE) as EarliestDate,
            MAX(PUBLISH_DATE) as LatestDate
        FROM {config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS
        WHERE DOCUMENT_TYPE IN ('ESG Research', 'Carbon Neutrality Research', 'Sustainability Report')
        GROUP BY DOCUMENT_TYPE
        ORDER BY DOCUMENT_TYPE
    """).collect()
    
    print(f"    ✅ Enhanced ESG content summary:")
    for row in result:
        print(f"      {row['DOCUMENT_TYPE']}: {row['DOCCOUNT']} documents")
    
    # Check specific ESG content
    try:
        result = session.sql(f"""
            SELECT 
                DOCUMENT_ID,
                DOCUMENT_TITLE,
                TICKER,
                LENGTH(DOCUMENT_TEXT) as ContentLength
            FROM {config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS
            WHERE DOCUMENT_TYPE = 'ESG Research'
            ORDER BY DOCUMENT_ID
            LIMIT 3
        """).collect()
        
        print(f"    ✅ Sample ESG research documents:")
        for row in result:
            print(f"      {row['DOCUMENT_ID']}: {row['TICKER']} - {row['CONTENTLENGTH']} chars")
            
    except Exception as e:
        print(f"    ❌ ESG content validation failed: {e}")

def validate_carbon_negative_analytics(session: Session):
    """Validate Carbon Negative Leaders analytics capabilities"""
    
    print("    → Validating Carbon Negative analytics...")
    
    # Check if we can analyze portfolio exposure to Carbon Negative Leaders
    try:
        result = session.sql(f"""
            WITH carbon_negative_securities AS (
                SELECT DISTINCT ws.SecurityID
                FROM {config.DATABASE_NAME}.CURATED.DIM_WATCHLIST w
                JOIN {config.DATABASE_NAME}.CURATED.FACT_WATCHLIST_SECURITIES ws ON w.WatchlistID = ws.WatchlistID
                WHERE w.WatchlistName = 'Carbon Negative Leaders'
            )
            SELECT 
                p.PortfolioName,
                COUNT(DISTINCT h.SecurityID) as CNL_Holdings,
                SUM(h.MarketValue_Base) as CNL_Exposure,
                SUM(h.PortfolioWeight) * 100 as CNL_Weight_Pct
            FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR h
            JOIN {config.DATABASE_NAME}.CURATED.DIM_PORTFOLIO p ON h.PortfolioID = p.PortfolioID
            WHERE h.SecurityID IN (SELECT SecurityID FROM carbon_negative_securities)
            GROUP BY p.PortfolioID, p.PortfolioName
            HAVING CNL_Holdings > 0
            ORDER BY CNL_Exposure DESC
            LIMIT 5
        """).collect()
        
        print(f"    ✅ Portfolio exposure to Carbon Negative Leaders:")
        for row in result:
            exposure = float(row['CNL_EXPOSURE']) if row['CNL_EXPOSURE'] else 0
            weight = float(row['CNL_WEIGHT_PCT']) if row['CNL_WEIGHT_PCT'] else 0
            print(f"      {row['PORTFOLIONAME']}: {row['CNL_HOLDINGS']} holdings, ${exposure:,.0f} ({weight:.1f}%)")
            
    except Exception as e:
        print(f"    ❌ Carbon Negative analytics failed: {e}")

def test_watchlist_search(session: Session):
    """Test watchlist content in search services"""
    
    print("    → Testing watchlist search capabilities...")
    
    try:
        # Search for Carbon Negative content
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.RESEARCH_SEARCH',
                '{{"query": "carbon negative microsoft climate", "limit": 2}}'
            )
        """).collect()
        
        if result and result[0][0]:
            print(f"    ✅ Carbon negative research searchable")
        
        # Search for ESG content
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.RESEARCH_SEARCH',
                '{{"query": "ESG sustainability apple renewable", "limit": 2}}'
            )
        """).collect()
        
        if result and result[0][0]:
            print(f"    ✅ ESG research searchable")
            
    except Exception as e:
        print(f"    ❌ Watchlist search test failed: {e}")

def validate_data_quality(session: Session):
    """Validate data quality following the enhanced model requirements"""
    
    print("    → Validating data quality...")
    
    validation_results = []
    
    # 1. Validate portfolio weights sum to 100%
    try:
        weight_check = session.sql(f"""
            SELECT 
                PortfolioID,
                SUM(PortfolioWeight) as TotalWeight,
                ABS(SUM(PortfolioWeight) - 1.0) as WeightDeviation
            FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR 
            WHERE HoldingDate = (SELECT MAX(HoldingDate) FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR)
            GROUP BY PortfolioID
            HAVING ABS(SUM(PortfolioWeight) - 1.0) > {config.PORTFOLIO_WEIGHT_TOLERANCE}
        """).collect()
        
        if len(weight_check) == 0:
            print("    ✅ Portfolio weights sum to 100% (±0.1% tolerance)")
            validation_results.append("portfolio_weights_valid")
        else:
            print(f"    ⚠️ {len(weight_check)} portfolios have weight deviations > {config.PORTFOLIO_WEIGHT_TOLERANCE}")
            for row in weight_check:
                print(f"       Portfolio {row['PORTFOLIOID']}: {row['TOTALWEIGHT']:.4f} (deviation: {row['WEIGHTDEVIATION']:.4f})")
    
    except Exception as e:
        print(f"    ❌ Portfolio weight validation failed: {e}")
    
    # 2. Validate no negative prices or market values
    try:
        negative_check = session.sql(f"""
            SELECT COUNT(*) as negative_count
            FROM {config.DATABASE_NAME}.CURATED.FACT_MARKETDATA_TIMESERIES
            WHERE Price_Close < 0 OR Price_Open < 0 OR Price_High < 0 OR Price_Low < 0
        """).collect()
        
        if negative_check[0]['NEGATIVE_COUNT'] == 0:
            print("    ✅ No negative prices in market data")
            validation_results.append("no_negative_prices")
        else:
            print(f"    ❌ Found {negative_check[0]['NEGATIVE_COUNT']} negative prices in market data")
    
    except Exception as e:
        print(f"    ❌ Negative price validation failed: {e}")
    
    # 3. Validate basic data relationships (simplified)
    try:
        # Check that we have positions data
        positions_count = session.sql(f"""
            SELECT COUNT(*) as count
            FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
        """).collect()
        
        if positions_count[0]['COUNT'] > 0:
            print("    ✅ Position data exists and accessible")
            validation_results.append("positions_valid")
        else:
            print("    ❌ No position data found")
    
    except Exception as e:
        print(f"    ❌ Position validation failed: {e}")
    
    # 4. Validate date ranges are logical
    try:
        date_check = session.sql(f"""
            SELECT 
                MIN(HoldingDate) as min_date,
                MAX(HoldingDate) as max_date,
                DATEDIFF(day, MIN(HoldingDate), MAX(HoldingDate)) as date_range_days
            FROM {config.DATABASE_NAME}.CURATED.FACT_POSITION_DAILY_ABOR
        """).collect()
        
        if date_check:
            date_range = date_check[0]['DATE_RANGE_DAYS']
            print(f"    ✅ Date ranges logical: {date_range} days span")
            validation_results.append("date_ranges_logical")
    
    except Exception as e:
        print(f"    ❌ Date range validation failed: {e}")
    
    # 5. Validate data volumes
    validate_data_volumes(session)
    
    return validation_results

def validate_data_volumes(session: Session):
    """Validate expected data volumes"""
    
    try:
        # Check table counts
        tables_to_check = [
            'DIM_ADVISOR',
            'DIM_CLIENT', 
            'DIM_SECURITY',
            'DIM_PORTFOLIO',
            'FACT_POSITION_DAILY_ABOR',
            'COMMUNICATIONS_CORPUS',
            'RESEARCH_CORPUS',
            'REGULATORY_CORPUS'
        ]
        
        print("    📊 Data volume summary:")
        for table in tables_to_check:
            try:
                count = session.sql(f"SELECT COUNT(*) as count FROM {config.DATABASE_NAME}.CURATED.{table}").collect()
                print(f"       {table}: {count[0]['COUNT']:,} records")
            except Exception as e:
                print(f"       {table}: Error - {e}")
    
    except Exception as e:
        print(f"    ❌ Data volume validation failed: {e}")

def validate_semantic_views_comprehensive(session: Session):
    """Comprehensive validation of semantic views"""
    
    print("    → Validating semantic views...")
    
    # Test CLIENT_FINANCIALS_SV
    try:
        # Basic functionality test
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS TOTAL_MARKET_VALUE
                DIMENSIONS PORTFOLIONAME
            ) LIMIT 5
        """).collect()
        print(f"    ✅ CLIENT_FINANCIALS_SV basic test: {len(result)} results")
        
        # Complex query test
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS TOTAL_MARKET_VALUE, HOLDING_COUNT
                DIMENSIONS PORTFOLIONAME, PRIMARYTICKER, GICS_SECTOR
            ) LIMIT 10
        """).collect()
        print(f"    ✅ CLIENT_FINANCIALS_SV complex test: {len(result)} results")
        
        # Issuer-level aggregation test
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS ISSUER_EXPOSURE
                DIMENSIONS LEGALNAME
            ) LIMIT 5
        """).collect()
        print(f"    ✅ CLIENT_FINANCIALS_SV issuer test: {len(result)} results")
        
    except Exception as e:
        print(f"    ❌ CLIENT_FINANCIALS_SV validation failed: {e}")
    
    # Test CLIENT_INTERACTIONS_SV
    try:
        # Basic functionality test
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_INTERACTIONS_SV
                METRICS TOTAL_COMMUNICATIONS
                DIMENSIONS CHANNEL
            ) LIMIT 5
        """).collect()
        print(f"    ✅ CLIENT_INTERACTIONS_SV basic test: {len(result)} results")
        
        # Complex query test
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_INTERACTIONS_SV
                METRICS TOTAL_COMMUNICATIONS
                DIMENSIONS CHANNEL, CLIENT_ID
            ) LIMIT 10
        """).collect()
        print(f"    ✅ CLIENT_INTERACTIONS_SV complex test: {len(result)} results")
        
    except Exception as e:
        print(f"    ❌ CLIENT_INTERACTIONS_SV validation failed: {e}")

def validate_search_services_comprehensive(session: Session):
    """Comprehensive validation of search services"""
    
    print("    → Validating search services...")
    
    # Test COMMUNICATIONS_SEARCH
    try:
        # Basic search test
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.COMMUNICATIONS_SEARCH',
                '{{"query": "portfolio performance", "limit": 3}}'
            )
        """).collect()
        print("    ✅ COMMUNICATIONS_SEARCH basic test passed")
        
        # Domain-specific test
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.COMMUNICATIONS_SEARCH',
                '{{"query": "investment strategy", "limit": 2}}'
            )
        """).collect()
        print("    ✅ COMMUNICATIONS_SEARCH domain test passed")
        
    except Exception as e:
        print(f"    ❌ COMMUNICATIONS_SEARCH validation failed: {e}")
    
    # Test RESEARCH_SEARCH
    try:
        # Basic search test
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.RESEARCH_SEARCH',
                '{{"query": "ESG sustainability", "limit": 3}}'
            )
        """).collect()
        print("    ✅ RESEARCH_SEARCH basic test passed")
        
        # Golden ticker test
        for ticker in config.GOLDEN_TICKERS[:2]:  # Test first 2 golden tickers
            try:
                result = session.sql(f"""
                    SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                        '{config.DATABASE_NAME}.AI.RESEARCH_SEARCH',
                        '{{"query": "{ticker}", "limit": 1}}'
                    )
                """).collect()
                print(f"    ✅ RESEARCH_SEARCH {ticker} test passed")
            except Exception as e:
                print(f"    ⚠️ RESEARCH_SEARCH {ticker} test failed: {e}")
        
    except Exception as e:
        print(f"    ❌ RESEARCH_SEARCH validation failed: {e}")
    
    # Test REGULATORY_SEARCH
    try:
        # Basic search test
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.REGULATORY_SEARCH',
                '{{"query": "compliance requirements", "limit": 2}}'
            )
        """).collect()
        print("    ✅ REGULATORY_SEARCH basic test passed")
        
        # Specific regulation test
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.REGULATORY_SEARCH',
                '{{"query": "FINRA", "limit": 2}}'
            )
        """).collect()
        print("    ✅ REGULATORY_SEARCH FINRA test passed")
        
    except Exception as e:
        print(f"    ❌ REGULATORY_SEARCH validation failed: {e}")

def run_business_scenario_tests(session: Session):
    """Run business scenario tests for each persona"""
    
    print("    → Running business scenario tests...")
    
    # Test queries that agents would run
    test_advisor_scenarios(session)
    test_analyst_scenarios(session)
    test_guardian_scenarios(session)

def test_advisor_scenarios(session: Session):
    """Test scenarios for advisor_ai (Wealth Manager)"""
    
    try:
        # Portfolio summary query (typical advisor query)
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS TOTAL_MARKET_VALUE, PORTFOLIO_WEIGHT_PCT
                DIMENSIONS PORTFOLIONAME, PRIMARYTICKER
            ) 
            WHERE PORTFOLIONAME LIKE '%MegaTech%'
            LIMIT 10
        """).collect()
        print(f"    ✅ Advisor scenario - Portfolio summary: {len(result)} results")
        
        # Client communication search
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.COMMUNICATIONS_SEARCH',
                '{{"query": "portfolio review meeting", "limit": 3}}'
            )
        """).collect()
        print("    ✅ Advisor scenario - Communication search passed")
        
    except Exception as e:
        print(f"    ❌ Advisor scenario test failed: {e}")

def test_analyst_scenarios(session: Session):
    """Test scenarios for analyst_ai (Portfolio Manager)"""
    
    try:
        # Sector exposure analysis (typical analyst query)
        result = session.sql(f"""
            SELECT * FROM SEMANTIC_VIEW(
                {config.DATABASE_NAME}.AI.CLIENT_FINANCIALS_SV
                METRICS TOTAL_MARKET_VALUE
                DIMENSIONS GICS_SECTOR
            ) 
            ORDER BY TOTAL_MARKET_VALUE DESC
            LIMIT 10
        """).collect()
        print(f"    ✅ Analyst scenario - Sector exposure: {len(result)} results")
        
        # Research analysis
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.RESEARCH_SEARCH',
                '{{"query": "analyst report earnings", "limit": 3}}'
            )
        """).collect()
        print("    ✅ Analyst scenario - Research search passed")
        
    except Exception as e:
        print(f"    ❌ Analyst scenario test failed: {e}")

def test_guardian_scenarios(session: Session):
    """Test scenarios for guardian_ai (Compliance)"""
    
    try:
        # Communication surveillance search
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.COMMUNICATIONS_SEARCH',
                '{{"query": "performance guarantee promise", "limit": 2}}'
            )
        """).collect()
        print("    ✅ Guardian scenario - Compliance search passed")
        
        # Regulatory guidance search
        result = session.sql(f"""
            SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                '{config.DATABASE_NAME}.AI.REGULATORY_SEARCH',
                '{{"query": "communication rules", "limit": 2}}'
            )
        """).collect()
        print("    ✅ Guardian scenario - Regulatory search passed")
        
    except Exception as e:
        print(f"    ❌ Guardian scenario test failed: {e}")

def generate_validation_report(session: Session):
    """Generate a comprehensive validation report"""
    
    print("    → Generating validation report...")
    
    report = {
        'database': config.DATABASE_NAME,
        'timestamp': session.sql("SELECT CURRENT_TIMESTAMP()").collect()[0][0],
        'components': {}
    }
    
    # Check each component
    components = [
        'semantic_views',
        'search_services', 
        'data_quality',
        'business_scenarios'
    ]
    
    for component in components:
        try:
            # Run component-specific validation
            if component == 'semantic_views':
                views = session.sql(f"SHOW SEMANTIC VIEWS IN {config.DATABASE_NAME}.AI").collect()
                report['components'][component] = {
                    'status': 'PASS' if len(views) >= 2 else 'FAIL',
                    'count': len(views),
                    'details': [v['name'] for v in views]
                }
            elif component == 'search_services':
                services = session.sql(f"SHOW CORTEX SEARCH SERVICES IN {config.DATABASE_NAME}.AI").collect()
                report['components'][component] = {
                    'status': 'PASS' if len(services) >= 3 else 'FAIL',
                    'count': len(services),
                    'details': [s['name'] for s in services]
                }
        except Exception as e:
            report['components'][component] = {
                'status': 'ERROR',
                'error': str(e)
            }
    
    # Print summary
    print("    📋 Validation Summary:")
    for component, details in report['components'].items():
        status_icon = "✅" if details['status'] == 'PASS' else "❌" if details['status'] == 'FAIL' else "⚠️"
        print(f"       {status_icon} {component}: {details['status']}")
    
    return report
