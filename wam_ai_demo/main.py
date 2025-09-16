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
from src.generate_structured import generate_advisors, generate_clients, generate_issuers_and_securities, generate_portfolios_and_accounts, generate_simplified_positions, generate_market_data, create_watchlists
from src.generate_unstructured import generate_unstructured_data, enhance_esg_content
from src.create_semantic_views import create_semantic_views
from src.create_search_services import create_search_services
from src.validate_components import validate_all_components

def create_session(connection_name: str) -> Session:
    """Create Snowpark session using connections.toml"""
    try:
        session = Session.builder.config("connection_name", connection_name).create()
        print(f"✅ Connected to Snowflake using connection: {connection_name}")
        return session
    except Exception as e:
        print(f"❌ Failed to connect to Snowflake: {e}")
        print(f"💡 Check your ~/.snowflake/connections.toml file")
        print(f"   Make sure the connection '{connection_name}' exists and is properly configured")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='WAM AI Demo Implementation')
    parser.add_argument('--connection', required=True, help='Snowflake connection name from connections.toml')
    parser.add_argument('--scenarios', nargs='*', default=['all'],
                       help='Scenarios to build: advisor, analyst, guardian, or all (default: all)')
    parser.add_argument('--scope', choices=['all', 'data', 'semantic', 'search'], default='all',
                       help='Scope of build: all, data, semantic, or search (default: all)')
    parser.add_argument('--extract-real-assets', action='store_true',
                       help='Extract real asset data from Snowflake Marketplace and save to CSV')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only run validation without building')
    parser.add_argument('--test-mode', action='store_true', 
                       help='Run in test mode with reduced data volumes')
    
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
        
        
        print(f"\n🚀 Starting WAM AI Demo build")
        print(f"   Database: {config.DATABASE_NAME}")
        print(f"   Scenarios: {', '.join(args.scenarios)}")
        print(f"   Scope: {args.scope}")
        print(f"   Test mode: {args.test_mode}")
        
        if args.validate_only:
            print("\n📋 Running validation only...")
            validate_all_components(session)
            return
        
        # Setup (always run for scope 'all' or 'data')
        if args.scope in ['all', 'data']:
            print("\n🔧 Database and Schema Setup")
            setup_database_and_schemas(session)
        
        # Data Generation
        if args.scope in ['all', 'data']:
            print("\n📊 Data Generation")
            
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
            
            # Generate watchlists (part of structured data)
            print("  → Creating watchlists...")
            create_watchlists(session)
            
            # Generate unstructured data (communications, research, regulatory)
            print("  → Generating unstructured data...")
            generate_unstructured_data(session)
            
            # Generate ESG content (part of unstructured data)
            print("  → Creating ESG research content...")
            enhance_esg_content(session)
        
        # AI Services
        if args.scope in ['all', 'semantic', 'search']:
            print("\n🤖 AI Services Setup")
            
            if args.scope in ['all', 'semantic']:
                print("  → Creating semantic views...")
                create_semantic_views(session)
            
            if args.scope in ['all', 'search']:
                print("  → Creating search services...")
                create_search_services(session)
        
        # Validation
        print("\n✅ Component Validation")
        validate_all_components(session)
        
        print(f"\n🎉 WAM AI Demo build completed successfully!")
        print(f"   ✅ Full demo with enhanced capabilities (watchlists, ESG analytics)")
        print(f"   Ready for agent configuration in Snowflake Intelligence")
        
    except Exception as e:
        print(f"\n❌ Build failed: {e}")
        sys.exit(1)
    
    finally:
        session.close()

if __name__ == "__main__":
    main()
