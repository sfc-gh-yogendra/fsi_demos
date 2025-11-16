#!/usr/bin/env python3
# setup.py
# Main setup script for Frost Markets Intelligence Demo

import argparse
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.snowpark_session import get_snowpark_session, create_demo_warehouses, set_demo_context, close_session
from config import DemoConfig


def create_database_schema(session, mode="full"):
    """Execute schema creation SQL based on mode
    
    Args:
        session: Snowpark session
        mode: Setup mode ('full' or 'data-only')
            - 'full': Creates fresh database and schemas (drops existing)
            - 'data-only': Creates database/schemas only if they don't exist (preserves AI objects)
    """
    print(f"\n🏗️  Creating database schemas (mode: {mode})...")
    
    try:
        if mode == "full":
            # Full mode: Create or replace everything
            print("   📊 Creating database (full mode - will replace existing)...")
            session.sql(f"CREATE OR REPLACE DATABASE {DemoConfig.DATABASE_NAME} COMMENT = '{DemoConfig.DATABASE['comment']}'").collect()
            
            # Set database context
            print("   🏗️  Setting database context...")
            session.sql(f"USE DATABASE {DemoConfig.DATABASE_NAME}").collect()
            
            # Create schemas with industry-standard names
            print("   📁 Creating schemas...")
            session.sql("CREATE OR REPLACE SCHEMA RAW COMMENT = 'Raw external data and unstructured documents'").collect()
            session.sql("CREATE OR REPLACE SCHEMA CURATED COMMENT = 'Industry-standard dimension/fact model for analysis'").collect()
            session.sql("CREATE OR REPLACE SCHEMA AI COMMENT = 'Semantic views, Cortex Search services, and AI components'").collect()
            
        elif mode == "data-only":
            # Data-only mode: Create only if not exists (preserves AI objects)
            print("   📊 Creating database if not exists (data-only mode - preserving AI objects)...")
            session.sql(f"CREATE DATABASE IF NOT EXISTS {DemoConfig.DATABASE_NAME} COMMENT = '{DemoConfig.DATABASE['comment']}'").collect()
            
            # Set database context
            print("   🏗️  Setting database context...")
            session.sql(f"USE DATABASE {DemoConfig.DATABASE_NAME}").collect()
            
            # Create schemas only if they don't exist (preserves AI objects in AI schema)
            print("   📁 Creating schemas if not exist...")
            session.sql("CREATE SCHEMA IF NOT EXISTS RAW COMMENT = 'Raw external data and unstructured documents'").collect()
            session.sql("CREATE SCHEMA IF NOT EXISTS CURATED COMMENT = 'Industry-standard dimension/fact model for analysis'").collect()
            session.sql("CREATE SCHEMA IF NOT EXISTS AI COMMENT = 'Semantic views, Cortex Search services, and AI components'").collect()
        
        # Set default context
        print("   🎯 Setting default context...")
        session.sql("USE SCHEMA RAW").collect()
        session.sql(f"USE WAREHOUSE {DemoConfig.COMPUTE_WAREHOUSE}").collect()
        
        print("✅ Database schemas created successfully")
        
    except Exception as e:
        print(f"❌ Error creating schemas: {str(e)}")
        # Try to show what went wrong
        try:
            current_db = session.get_current_database()
            print(f"   Current database: {current_db}")
        except:
            print("   Could not determine current database")
        raise


def generate_data(session, mode, data_type="all"):
    """Generate demo data based on specified type
    
    Args:
        session: Snowpark session
        mode: Setup mode (full or data-only)
        data_type: Type of data to generate (all, structured, unstructured)
    """
    print(f"\n📊 Generating demo data (mode: {mode}, type: {data_type})...")
    
    if mode == "data-only":
        print("   ℹ️  Data-only mode: Search services and agents will be preserved")
        if data_type == "all":
            print("   ⚠️  Note: Semantic views will need to be recreated after data regeneration")
        elif data_type == "structured":
            print("   ℹ️  Preserving: Unstructured data, semantic views, search services, agents")
        elif data_type == "unstructured":
            print("   ℹ️  Preserving: Structured data, semantic views, search services, agents")
    
    try:
        # Import data generation modules
        from data_generation.event_log import generate_master_event_log
        from data_generation.structured_data import generate_all_structured_data
        from data_generation.unstructured_data import generate_all_unstructured_data
        
        # Generate based on data type
        if data_type in ["all", "structured"]:
            # Generate master event log first (drives all correlations)
            print("  🎯 Generating master event log...")
            generate_master_event_log(session)
            
            # Generate structured data
            print("  📈 Generating structured data...")
            generate_all_structured_data(session)
        else:
            print("  ⏭️  Skipping structured data generation")
        
        if data_type in ["all", "unstructured"]:
            # Generate unstructured data using Cortex
            print("  📄 Generating unstructured data with Cortex...")
            generate_all_unstructured_data(session)
        else:
            print("  ⏭️  Skipping unstructured data generation")
        
        print("✅ Demo data generated successfully")
        
    except Exception as e:
        print(f"❌ Error generating data: {str(e)}")
        raise


def create_ai_components(session, mode, ai_type="all"):
    """Create Snowflake AI components based on specified type
    
    Args:
        session: Snowpark session
        mode: Setup mode (full or ai-only)
        ai_type: Type of AI components to create (all, semantic-views, search-services, custom-tools, agents)
    """
    print(f"\n🤖 Creating AI components (mode: {mode}, type: {ai_type})...")
    
    if mode == "ai-only":
        print("   ℹ️  AI-only mode: Data tables in RAW and CURATED schemas will be preserved")
        if ai_type == "semantic-views":
            print("   ℹ️  Preserving: Search services, custom tools, and agents")
        elif ai_type == "search-services":
            print("   ℹ️  Preserving: Semantic views, custom tools, and agents")
        elif ai_type == "custom-tools":
            print("   ℹ️  Preserving: Semantic views, search services, and agents")
        elif ai_type == "agents":
            print("   ℹ️  Preserving: Semantic views, search services, and custom tools")
    
    try:
        from ai_components.semantic_views import create_all_semantic_views
        from ai_components.search_services import create_all_search_services
        from ai_components.custom_tools import create_all_custom_tools
        from ai_components.agents import create_all_agents
        
        # Create based on AI type
        if ai_type in ["all", "semantic-views"]:
            print("  🔍 Creating semantic views...")
            create_all_semantic_views(session)
        else:
            print("  ⏭️  Skipping semantic views creation")
        
        if ai_type in ["all", "search-services"]:
            print("  🔎 Creating search services...")
            create_all_search_services(session)
        else:
            print("  ⏭️  Skipping search services creation")
        
        if ai_type in ["all", "custom-tools"]:
            print("  🔧 Creating custom tools...")
            create_all_custom_tools(session)
        else:
            print("  ⏭️  Skipping custom tools creation")
        
        if ai_type in ["all", "agents"]:
            print("  🤖 Creating Snowflake Intelligence agents...")
            create_all_agents(session, DemoConfig.SCENARIOS)
        else:
            print("  ⏭️  Skipping agents creation")
        
        print("✅ AI components created successfully")
        
    except Exception as e:
        print(f"❌ Error creating AI components: {str(e)}")
        raise


def validate_setup(session):
    """Basic validation of the demo setup"""
    print("\n✅ Validating demo setup...")
    
    try:
        from utils.validation import validate_all_components
        validate_all_components(session)
        print("✅ Demo validation completed successfully")
        
    except Exception as e:
        print(f"⚠️  Validation warnings: {str(e)}")


def main():
    """Main setup function with granular mode options"""
    parser = argparse.ArgumentParser(
        description="Frost Markets Intelligence Demo Setup",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full setup
  python setup.py --mode full
  
  # Regenerate only structured data (preserves unstructured data and AI components)
  python setup.py --mode data-only --data-type structured
  
  # Regenerate only unstructured data (preserves structured data and AI components)
  python setup.py --mode data-only --data-type unstructured
  
  # Recreate only semantic views (preserves search services, custom tools, and agents)
  python setup.py --mode ai-only --ai-type semantic-views
  
  # Recreate only search services (preserves semantic views, custom tools, and agents)
  python setup.py --mode ai-only --ai-type search-services
  
  # Recreate only custom tools (preserves semantic views, search services, and agents)
  python setup.py --mode ai-only --ai-type custom-tools
  
  # Recreate only agents (preserves semantic views, search services, and custom tools)
  python setup.py --mode ai-only --ai-type agents
        """
    )
    parser.add_argument(
        "--mode", 
        choices=["full", "data-only", "ai-only", "scenario-specific"],
        default="full",
        help="""Setup mode:
        - full: Complete setup (creates/replaces everything)
        - data-only: Regenerate data tables (use --data-type to specify which)
        - ai-only: Recreate AI components (use --ai-type to specify which)
        - scenario-specific: Setup specific demo scenario"""
    )
    parser.add_argument(
        "--data-type",
        choices=["all", "structured", "unstructured"],
        default="all",
        help="""Data type to generate (only with --mode=data-only):
        - all: All data (structured + unstructured)
        - structured: Only structured data (companies, prices, clients, etc.)
        - unstructured: Only unstructured data (documents, reports, transcripts)"""
    )
    parser.add_argument(
        "--ai-type",
        choices=["all", "semantic-views", "search-services", "custom-tools", "agents"],
        default="all",
        help="""AI components to create (only with --mode=ai-only):
        - all: All AI components (semantic views + search services + custom tools + agents)
        - semantic-views: Only semantic views for Cortex Analyst
        - search-services: Only Cortex Search services
        - custom-tools: Only custom tools (Python stored procedures)
        - agents: Only Snowflake Intelligence agents"""
    )
    parser.add_argument(
        "--scenario",
        choices=DemoConfig.SCENARIOS,
        help="Specific scenario to setup (requires --mode=scenario-specific)"
    )
    parser.add_argument(
        "--connection_name",
        default=DemoConfig.SNOWFLAKE_CONNECTION_NAME,
        help="Connection name from connections.toml"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validation step"
    )
    
    args = parser.parse_args()
    
    print("🏔️  Frost Markets Intelligence Demo Setup")
    print("=" * 50)
    print(f"Mode: {args.mode}")
    if args.mode == "data-only":
        print(f"Data Type: {args.data_type}")
    if args.mode == "ai-only":
        print(f"AI Type: {args.ai_type}")
    if args.scenario:
        print(f"Scenario: {args.scenario}")
    print(f"Connection: {args.connection_name}")
    print()
    
    session = None
    try:
        # Create Snowpark session
        session = get_snowpark_session(args.connection_name)
        
        # Create warehouses first (required for all operations)
        create_demo_warehouses(session)
        
        # Execute setup based on mode
        if args.mode in ["full", "data-only"]:
            create_database_schema(session, mode=args.mode)
            set_demo_context(session)
            data_type = "all" if args.mode == "full" else args.data_type
            generate_data(session, args.mode, data_type=data_type)
            
        if args.mode in ["full", "ai-only"]:
            if args.mode == "ai-only":
                # For ai-only mode, just set context without creating/replacing schemas
                set_demo_context(session)
            ai_type = "all" if args.mode == "full" else args.ai_type
            create_ai_components(session, args.mode, ai_type=ai_type)
            
        if args.mode == "scenario-specific":
            if not args.scenario:
                print("❌ --scenario required when using --mode=scenario-specific")
                sys.exit(1)
            # TODO: Implement scenario-specific setup
            print(f"🎯 Setting up scenario: {args.scenario}")
            
        # Validation
        if not args.skip_validation:
            from utils.validation import validate_all_components
            validate_all_components(session)
            
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Open Snowsight and navigate to Snowflake Intelligence")
        print("   2. Agents are automatically created and ready to use!")
        print("   3. Test demo scenarios with the created agents:")
        print("      - Earnings Analysis Assistant")
        print("      - Thematic Investment Research Assistant")
        print("      - Global Macro Strategy Assistant")
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        sys.exit(1)
        
    finally:
        if session:
            close_session(session)


if __name__ == "__main__":
    main()
