#!/usr/bin/env python3
"""
WAM AI Demo - Main Implementation Script
Orchestrates the complete build process for the wealth management demo
"""

import sys
import argparse
from snowflake.snowpark import Session
import config
from src.setup import setup_database_and_schemas
from src.generate_structured import generate_structured_data, generate_advisors, generate_clients, generate_issuers_and_securities, generate_portfolios_and_accounts, generate_simplified_positions, generate_market_data, create_watchlists
from src.generate_unstructured import generate_unstructured_data, enhance_esg_content
from src.create_semantic_views import create_semantic_views
from src.create_search_services import create_search_services
from src.validate_components import validate_all_components

def create_session(connection_name: str = None) -> Session:
    """Create Snowpark session using connections.toml"""
    if connection_name is None:
        connection_name = config.get_connection_name()
    
    try:
        if connection_name:
            session = Session.builder.config("connection_name", connection_name).create()
            print(f"✅ Connected to Snowflake using connection: {connection_name}")
        else:
            # Use default connection from ~/.snowflake/connections.toml
            session = Session.builder.create()
            print(f"✅ Connected to Snowflake using default connection")
        return session
    except Exception as e:
        print(f"❌ Failed to connect to Snowflake: {e}")
        print(f"💡 Check your ~/.snowflake/connections.toml file")
        print(f"   Or specify a connection with --connection <name>")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='WAM AI Demo Implementation')
    parser.add_argument('--connection', help='Snowflake connection name from connections.toml')
    parser.add_argument('--mode', choices=config.BUILD_MODES, default='replace_all',
                       help='Build mode: replace_all, data_only, or semantics_and_search_only')
    parser.add_argument('--test-mode', action='store_true', 
                       help='Run in test mode with reduced data volumes')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only run validation without building')
    parser.add_argument('--extract-real-assets', action='store_true',
                       help='Extract real assets from Snowflake Marketplace to CSV')
    # parser.add_argument('--extract-real-market-data', action='store_true',
    #                    help='Extract real market data from Snowflake Marketplace to CSV - DEPRECATED')
    parser.add_argument('--phase2', action='store_true',
                       help='Include Phase 2 enhancements: watchlists, enhanced ESG, expanded capabilities')
    
    args = parser.parse_args()
    
    # Create session
    session = create_session(args.connection)
    
    try:
        # Handle extraction modes first
        if args.extract_real_assets:
            print("\n📊 Extracting real assets from Marketplace...")
            from src.extract_real_data import extract_real_assets_to_csv
            extract_real_assets_to_csv(session)
            return
        
        # Real market data extraction is deprecated - system now uses synthetic market data only
        # if args.extract_real_market_data:
        #     print("\n📈 Extracting real market data from Marketplace...")
        #     from src.extract_real_data import extract_real_market_data_to_csv
        #     extract_real_market_data_to_csv(session)
        #     return
        
        print(f"\n🚀 Starting WAM AI Demo build in {args.mode} mode")
        print(f"   Database: {config.DATABASE_NAME}")
        print(f"   Test mode: {args.test_mode}")
        
        if args.validate_only:
            print("\n📋 Running validation only...")
            validate_all_components(session)
            return
        
        # Phase 1: Setup (always run)
        if args.mode in ['replace_all']:
            print("\n🔧 Phase 1: Database and Schema Setup")
            setup_database_and_schemas(session)
        
        # Phase 2: Data Generation
        if args.mode in ['replace_all', 'data_only']:
            print("\n📊 Phase 2: Data Generation")
            
            # Generate structured data (dimensions only)
            from src.setup import create_foundation_tables
            
            print("  → Creating foundation tables...")
            create_foundation_tables(session)
            
            print("  → Generating structured data...")
            generate_advisors(session)
            generate_clients(session)
            generate_issuers_and_securities(session)
            generate_portfolios_and_accounts(session)
            
            # Generate positions and market data
            generate_simplified_positions(session)
            generate_market_data(session)
        
        # Phase 3: AI Services
        if args.mode in ['replace_all', 'semantics_and_search_only']:
            print("\n🤖 Phase 3: AI Services Setup")
            
            print("  → Creating semantic views...")
            create_semantic_views(session, include_phase2=args.phase2)
            
            print("  → Creating search services...")
            create_search_services(session)
            
            # Phase 2 Enhancements
            if args.phase2:
                print("\n🚀 Phase 2: Enhanced Capabilities")
                
                print("  → Creating watchlists...")
                create_watchlists(session)
                
                print("  → Enhancing ESG content...")
                enhance_esg_content(session)
        
        # Phase 4: Validation
        print("\n✅ Phase 4: Component Validation")
        validate_all_components(session)
        
        print(f"\n🎉 WAM AI Demo build completed successfully!")
        print(f"   Ready for agent configuration in Snowflake Intelligence")
        
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)
    
    finally:
        session.close()

if __name__ == "__main__":
    main()
