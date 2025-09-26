#!/usr/bin/env python3
"""
Snowcrest Asset Management (SAM) Demo - Main CLI Orchestrator

This script orchestrates the creation of the complete SAM demo environment,
including structured data generation, unstructured content creation, and AI component setup.

Usage:
    python main.py --connection-name CONNECTION [--scenarios SCENARIO_LIST] [--scope SCOPE]

Examples:
    python main.py --connection-name my_demo                              # Build everything 
    python main.py --connection-name my_demo --scenarios portfolio_copilot # Build foundation + portfolio scenario
    python main.py --connection-name my_demo --scope structured          # Build only structured data (tables)
    python main.py --connection-name my_demo --scope unstructured        # Build only unstructured data (documents)
    python main.py --connection-name my_demo --scope data                # Build structured + unstructured data
    python main.py --connection-name my_demo --scope ai                  # Build only AI components (semantic + search)
    python main.py --connection-name my_demo --test-mode                 # Use test mode
"""

import argparse
import sys
from typing import List, Optional
from datetime import datetime

# Import configuration
from config import (
    DEFAULT_CONNECTION_NAME, 
    AVAILABLE_SCENARIOS,
    SCENARIO_DATA_REQUIREMENTS,
    DATABASE_NAME
)

def parse_arguments() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Build Snowcrest Asset Management (SAM) AI Demo Environment'
    )
    
    parser.add_argument(
        '--connection-name',
        type=str,
        required=True,
        help='Snowflake connection name from ~/.snowflake/connections.toml (required)'
    )
    
    parser.add_argument(
        '--scenarios',
        type=str,
        default='all',
        help='Comma-separated list of scenarios to build, or "all" for all scenarios (default: all)'
    )
    
    parser.add_argument(
        '--scope',
        type=str,
        choices=['all', 'data', 'structured', 'unstructured', 'ai', 'semantic', 'search'],
        default='all',
        help='Scope of build: all=everything, data=structured+unstructured, structured=tables only, unstructured=documents only, ai=semantic+search, semantic=views only, search=services only'
    )
    
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Use test mode with 10 percent of data for faster development testing (500 securities vs 5,000)'
    )
    
    return parser.parse_args()

def validate_scenarios(scenario_list: List[str]) -> List[str]:
    """Validate and return list of valid scenarios."""
    invalid_scenarios = [s for s in scenario_list if s not in AVAILABLE_SCENARIOS]
    if invalid_scenarios:
        print(f"❌ Invalid scenarios: {invalid_scenarios}")
        print(f"Available scenarios: {AVAILABLE_SCENARIOS}")
        sys.exit(1)
    
    return scenario_list

def get_required_document_types(scenarios: List[str]) -> List[str]:
    """Get unique list of document types required for the specified scenarios."""
    required_types = set()
    for scenario in scenarios:
        if scenario in SCENARIO_DATA_REQUIREMENTS:
            required_types.update(SCENARIO_DATA_REQUIREMENTS[scenario])
    return list(required_types)

def create_snowpark_session(connection_name: str):
    """Create and validate Snowpark session."""
    try:
        from snowflake.snowpark import Session
        
        print(f"🔗 Connecting to Snowflake using connection: {connection_name}")
        session = Session.builder.config("connection_name", connection_name).create()
        
        # Test connection
        result = session.sql("SELECT CURRENT_VERSION()").collect()
        print(f"✅ Connected successfully to Snowflake version: {result[0][0]}")
        
        # Create dedicated warehouses for the demo
        create_demo_warehouses(session)
        
        return session
        
    except ImportError:
        print("❌ Error: snowflake-snowpark-python not installed")
        print("Install with: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print(f"Please ensure:")
        print(f"  1. Connection '{connection_name}' exists in ~/.snowflake/connections.toml")
        print(f"  2. Connection details (account, user, password, etc.) are correct")
        print(f"  3. Your Snowflake account has the required permissions")
        sys.exit(1)

def create_demo_warehouses(session):
    """Create dedicated warehouses for demo execution and Cortex Search services."""
    from config import EXECUTION_WAREHOUSE, CORTEX_SEARCH_WAREHOUSE, WAREHOUSE_SIZE
    
    try:
        print("🏗️ Creating demo warehouses...")
        
        # Create execution warehouse for data generation and code execution
        session.sql(f"""
            CREATE OR REPLACE WAREHOUSE {EXECUTION_WAREHOUSE}
            WITH WAREHOUSE_SIZE = {WAREHOUSE_SIZE}
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
            COMMENT = 'Warehouse for SAM demo data generation and execution'
        """).collect()
        print(f"✅ Created execution warehouse: {EXECUTION_WAREHOUSE}")
        
        # Create Cortex Search warehouse for search services
        session.sql(f"""
            CREATE OR REPLACE WAREHOUSE {CORTEX_SEARCH_WAREHOUSE}
            WITH WAREHOUSE_SIZE = {WAREHOUSE_SIZE}
            AUTO_SUSPEND = 60
            AUTO_RESUME = TRUE
            COMMENT = 'Warehouse for SAM demo Cortex Search services'
        """).collect()
        print(f"✅ Created Cortex Search warehouse: {CORTEX_SEARCH_WAREHOUSE}")
        
        # Set session to use execution warehouse by default
        session.use_warehouse(EXECUTION_WAREHOUSE)
        print(f"✅ Session configured to use: {EXECUTION_WAREHOUSE}")
        
    except Exception as e:
        print(f"⚠️ Warning: Failed to create warehouses: {e}")
        print("Continuing with existing warehouse from connection...")

def main():
    """Main execution function."""
    start_time = datetime.now()
    
    print("🏔️  Snowcrest Asset Management (SAM) Demo Builder")
    print("=" * 60)
    print(f"⏰ Build started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Parse arguments
    args = parse_arguments()
    
    # Parse and validate scenarios
    if args.scenarios.lower() == 'all':
        scenario_list = AVAILABLE_SCENARIOS
    else:
        scenario_list = [s.strip() for s in args.scenarios.split(',')]
    validated_scenarios = validate_scenarios(scenario_list)
    
    print(f"🎭 Scenarios: {', '.join(validated_scenarios)}")
    print(f"🏗️  Scope: {args.scope}")
    print(f"🔗 Connection: {args.connection_name}")
    if args.test_mode:
        print(f"🧪 Test Mode: Using 10% data volumes")
    print()
    print("=" * 60)
    
    # Create Snowpark session
    session = create_snowpark_session(args.connection_name)
    
    # Determine what to build based on scope
    build_structured = args.scope in ['all', 'data', 'structured']
    build_unstructured = args.scope in ['all', 'data', 'unstructured']
    build_semantic = args.scope in ['all', 'ai', 'semantic'] 
    build_search = args.scope in ['all', 'ai', 'search']
    
    step_number = 1
    total_steps = sum([
        build_structured and 1 or 0,
        build_unstructured and 1 or 0, 
        (build_semantic or build_search) and 1 or 0
    ])
    
    try:
        # Step 1: Build structured data (foundation + scenario-specific)
        if build_structured:
            print(f"📊 Step {step_number}/{total_steps}: Building structured data...")
            step_number += 1
            # Import and run structured data generation
            import generate_structured
            generate_structured.build_all(session, validated_scenarios, args.test_mode)
            
        # Step 2: Build unstructured data (documents and content)
        if build_unstructured:
            print(f"📝 Step {step_number}/{total_steps}: Building unstructured data...")
            step_number += 1
            
            # Validate that structured data exists (unstructured depends on it)
            try:
                session.sql(f"SELECT COUNT(*) FROM {DATABASE_NAME}.CURATED.DIM_SECURITY LIMIT 1").collect()
            except Exception as e:
                print("❌ Unstructured data generation requires structured data to exist first.")
                print("💡 Run with --scope structured first, or use --scope data to build both together.")
                print(f"   Error details: {e}")
                raise
            
            # Import and run unstructured data generation
            import generate_unstructured
            required_doc_types = get_required_document_types(validated_scenarios)
            generate_unstructured.build_all(session, required_doc_types, args.test_mode)
        
        # Step 3: Build AI components
        if build_semantic or build_search:
            print(f"🤖 Step {step_number}/{total_steps}: Building AI components...")
            import build_ai
            build_ai.build_all(session, validated_scenarios, build_semantic, build_search)
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        print()
        print("=" * 60)
        print("🎉 SAM Demo Environment Build Complete!")
        print(f"⏰ Build completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⌛ Total duration: {duration}")
        print(f"📍 Database: {DATABASE_NAME}")
        print(f"🎭 Scenarios: {', '.join(validated_scenarios)}")
        print()
        print("Next steps:")
        print("1. Configure agents in Snowflake Intelligence (see docs/agents_setup.md)")
        print("2. Test demo scenarios (see docs/demo_scenarios.md)")
        print("3. Run validation checks (see docs/runbooks.md)")
        
    except ImportError as e:
        print(f"❌ Missing module: {e}")
        print("Ensure all required Python modules are created:")
        print("- python/generate_structured.py")
        print("- python/generate_unstructured.py") 
        print("- python/build_ai.py")
        sys.exit(1)
    except Exception as e:
        end_time = datetime.now()
        duration = end_time - start_time
        print()
        print("=" * 60)
        print("🛑 BUILD FAILED!")
        print(f"❌ Error: {str(e)}")
        print(f"⏰ Failed after: {duration}")
        print("=" * 60)
        print()
        print("💡 Troubleshooting tips:")
        print("1. Check error message above for specific component that failed")
        print("2. Verify all required data tables exist before AI component creation")
        print("3. Review connection permissions and warehouse availability")
        print("4. See docs/runbooks.md for common issues and solutions")
        print()
        sys.exit(1)
    finally:
        if 'session' in locals():
            session.close()

if __name__ == "__main__":
    main()
