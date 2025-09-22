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
    python main.py --connection-name my_demo --scope data                # Build only data layer
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
        choices=['all', 'data', 'semantic', 'search'],
        default='all',
        help='Scope of build: all=everything, data=structured+unstructured, semantic=views only, search=services only'
    )
    
    parser.add_argument(
        '--extract-real-assets',
        action='store_true',
        help='Extract real asset data from Snowflake Marketplace and save to CSV (requires marketplace access)'
    )
    
    parser.add_argument(
        '--analyze-pdf',
        type=str,
        help='Analyze PDF file to create enhanced document templates (requires PDF path)'
    )
    
    parser.add_argument(
        '--pdf-doc-type',
        type=str,
        choices=['broker_research', 'earnings_transcripts', 'policy_docs', 'press_releases'],
        help='Document type for PDF analysis (required with --analyze-pdf)'
    )
    
    parser.add_argument(
        '--integrate-templates',
        action='store_true',
        help='Integrate enhanced PDF-derived templates with document generation'
    )
    
    parser.add_argument(
        '--interactive-template',
        action='store_true',
        help='Interactive mode for copy/paste PDF text analysis'
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
    
    # Handle PDF template analysis if requested
    if args.analyze_pdf or args.interactive_template:
        if args.analyze_pdf and not args.pdf_doc_type:
            print("❌ Error: --pdf-doc-type required when using --analyze-pdf")
            sys.exit(1)
        
        print("📄 Analyzing PDF to create enhanced document templates...")
        from pdf_template_analyzer import PDFTemplateAnalyzer, PDFTemplateIntegrator
        
        analyzer = PDFTemplateAnalyzer()
        integrator = PDFTemplateIntegrator(analyzer)
        
        try:
            if args.interactive_template:
                print(f"Interactive mode: Please paste your document text below (press Ctrl+D when finished):")
                print("-" * 50)
                import sys as sys_module
                text_input = sys_module.stdin.read()
                
                if not args.pdf_doc_type:
                    print("Enter document type (broker_research, earnings_transcripts, policy_docs, press_releases):")
                    doc_type = input().strip()
                else:
                    doc_type = args.pdf_doc_type
                
                template = integrator.process_text_input(text_input, doc_type)
            else:
                template = integrator.process_pdf_file(args.analyze_pdf, args.pdf_doc_type)
                doc_type = args.pdf_doc_type
            
            # Generate enhanced function
            enhanced_function = integrator.generate_enhanced_prompt_function(template, doc_type)
            integrator.enhanced_templates[doc_type] = enhanced_function
            
            # Display results
            print(f"\n📊 Analysis Results for {doc_type}:")
            print(f"- Total word count: {template.total_word_count}")
            print(f"- Sections found: {len(template.sections)}")
            for section in template.sections:
                print(f"  • {section.title}: {section.word_count} words")
            print(f"- Key phrases: {len(template.key_phrases)}")
            print(f"- Formatting patterns: {template.formatting_patterns}")
            
            # Save enhanced templates
            integrator.save_enhanced_templates("enhanced_templates")
            
            print(f"\n✅ Enhanced template generated and saved to enhanced_templates/{doc_type}_enhanced.py")
            print("\nNext steps:")
            print("1. Review the enhanced template")
            print("2. Run with --integrate-templates to apply changes")
            print("3. Test with your SAM demo data generation")
            
        except Exception as e:
            print(f"❌ PDF analysis failed: {e}")
        
        return  # Exit after PDF analysis
    
    # Handle template integration if requested
    if args.integrate_templates:
        print("🔄 Integrating enhanced PDF-derived templates...")
        from template_integrator import TemplateIntegrationManager
        
        manager = TemplateIntegrationManager("python/generate_unstructured.py")
        manager.integrate_enhanced_templates("enhanced_templates")
        
        if manager.test_integration():
            print("✅ Template integration successful!")
            print("🎯 Enhanced templates are now active in document generation")
        else:
            print("❌ Template integration failed")
            print("💡 Use manager.rollback() if needed")
        
        return  # Exit after template integration
    
    # Handle real asset extraction if requested
    if args.extract_real_assets:
        print("🌍 Extracting real asset data from Snowflake Marketplace...")
        import extract_real_assets
        success = extract_real_assets.extract_real_assets_to_csv(session)
        if success:
            print("✅ Real asset data extracted successfully")
            print("💡 To use real assets in future builds, set USE_REAL_ASSETS_CSV = True in config.py")
        else:
            print("❌ Real asset extraction failed - continuing with generated data")
        print()
        return  # Exit after extraction
    
    # Determine what to build based on scope
    build_data = args.scope in ['all', 'data']
    build_semantic = args.scope in ['all', 'semantic'] 
    build_search = args.scope in ['all', 'search']
    
    step_number = 1
    total_steps = sum([build_data and 2 or 0, (build_semantic or build_search) and 1 or 0])
    
    try:
        # Step 1: Build structured data (foundation + scenario-specific)
        if build_data:
            print(f"📊 Step {step_number}/{total_steps}: Building structured data...")
            step_number += 1
            # Import and run structured data generation
            import generate_structured
            generate_structured.build_all(session, validated_scenarios, args.test_mode)
            
            print(f"📝 Step {step_number}/{total_steps}: Building unstructured data...")
            step_number += 1
            # Import and run unstructured data generation
            import generate_unstructured
            required_doc_types = get_required_document_types(validated_scenarios)
            generate_unstructured.build_all(session, required_doc_types, args.test_mode)
        
        # Step 2: Build AI components
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
