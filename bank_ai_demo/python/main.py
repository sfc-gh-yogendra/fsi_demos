#!/usr/bin/env python3
"""
Glacier First Bank AI Intelligence Demo - Main Orchestration Script

This script orchestrates the complete setup and data generation for
the Glacier First Bank demo, supporting different scenarios and scopes.
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import List

# Add python directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from snowflake.snowpark import Session
import config
import generate_structured
import generate_unstructured
import create_semantic_views
import create_search_services
import create_agents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('glacier_demo.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# Global session variable to avoid passing it around
_session = None


def validate_connection_name(connection_name: str) -> str:
    """Validate connection name and return validated connection name."""
    if not config.validate_connection(connection_name):
        raise ValueError("Valid connection name is required. Provide --connection-name or set CONNECTION_NAME environment variable.")
    
    logger.info(f"Validated connection: {connection_name}")
    logger.info(f"Institution: {config.INSTITUTION_NAME}")
    return connection_name


def create_snowflake_session(connection_name: str) -> Session:
    """Create and configure Snowflake session."""
    global _session
    
    try:
        # Get snowflake config
        snowflake_config = config.get_snowflake_config(connection_name)
        
        # Create session from connection
        session = Session.builder.config("connection_name", connection_name).create()
        
        # Create warehouses if they don't exist
        logger.info("Creating warehouses...")
        session.sql(f"""
            CREATE OR REPLACE WAREHOUSE {snowflake_config['compute_warehouse']}
            WITH WAREHOUSE_SIZE = 'MEDIUM'
            AUTO_SUSPEND = 300
            AUTO_RESUME = TRUE
            INITIALLY_SUSPENDED = TRUE
        """).collect()
        
        session.sql(f"""
            CREATE OR REPLACE WAREHOUSE {snowflake_config['search_warehouse']}
            WITH WAREHOUSE_SIZE = 'SMALL'
            AUTO_SUSPEND = 180
            AUTO_RESUME = TRUE
            INITIALLY_SUSPENDED = TRUE
        """).collect()
        
        # Set context
        session.sql(f"USE WAREHOUSE {snowflake_config['compute_warehouse']}").collect()
        logger.info("Warehouses created and set")
        
        logger.info(f"Connected to Snowflake: {connection_name}")
        
        # Store session globally
        _session = session
        return session
        
    except Exception as e:
        logger.error(f"Failed to create Snowflake session: {e}")
        raise

def generate_demo_data(session: Session, scale: str, scenarios: List[str]) -> None:
    """Generate all demo data (structured and unstructured)."""
    if not session:
        raise RuntimeError("Snowflake session not initialized")
    
    logger.info(f"Generating demo data for scenarios: {scenarios}")
    
    # Ensure database context is set
    try:
        session.sql(f"USE DATABASE {config.SNOWFLAKE['database']}").collect()
        session.sql(f"USE WAREHOUSE {config.SNOWFLAKE['compute_warehouse']}").collect()
    except Exception as e:
        logger.warning(f"Could not set database context: {e}")
    
    try:
        # Generate structured data (using save_as_table)
        generate_structured.generate_all_structured_data(session, scale, scenarios)
        
        # Generate unstructured data (using Cortex Complete)
        generate_unstructured.generate_all_unstructured_data(session, scale, scenarios)
        
        logger.info("Data generation completed successfully")
        
    except Exception as e:
        logger.error(f"Data generation failed: {e}")
        raise


def create_semantic_views_wrapper(session: Session, scenarios: List[str]) -> None:
    """Create semantic views for specified scenarios."""
    logger.info(f"Creating semantic views for scenarios: {scenarios}")
    
    if not session:
        raise RuntimeError("Snowflake session not initialized")
    
    try:
        create_semantic_views.create_all_semantic_views(session, scenarios)
        logger.info("Semantic views creation completed")
        
    except Exception as e:
        logger.error(f"Semantic views creation failed: {e}")
        raise


def create_search_services_wrapper(session: Session, scenarios: List[str]) -> None:
    """Create Cortex Search services for specified scenarios."""
    logger.info(f"Creating search services for scenarios: {scenarios}")
    
    if not session:
        raise RuntimeError("Snowflake session not initialized")
    
    try:
        create_search_services.create_all_search_services(session, scenarios)
        logger.info("Search services creation completed")
        
    except Exception as e:
        logger.error(f"Search services creation failed: {e}")
        raise


def create_agents_wrapper(session: Session, scenarios: List[str]) -> None:
    """Create Snowflake Intelligence agents for specified scenarios."""
    logger.info(f"Creating agents for scenarios: {scenarios}")
    
    if not session:
        raise RuntimeError("Snowflake session not initialized")
    
    try:
        create_agents.create_all_agents(session, scenarios)
        logger.info("Agents creation completed")
        
    except Exception as e:
        logger.error(f"Agents creation failed: {e}")
        raise


def create_pdf_generator(session: Session) -> None:
    """Create PDF generation custom tool."""
    logger.info("Creating PDF generation custom tool...")
    
    try:
        # First create the stages
        logger.info("Creating stages for PDF generation...")
        session.sql(f'''
            CREATE STAGE IF NOT EXISTS {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.GLACIER_REPORTS_STAGE
            ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
            DIRECTORY = (ENABLE = TRUE)
            COMMENT = 'Stage for storing AI-generated PDF reports'
        ''').collect()
        
        session.sql(f'''
            CREATE STAGE IF NOT EXISTS {config.SNOWFLAKE['database']}.{config.SNOWFLAKE['ai_schema']}.PROC_STAGE
            ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE')
            DIRECTORY = (ENABLE = TRUE)
            COMMENT = 'Stage for storing Python stored procedures code'
        ''').collect()
        
        logger.info("Stages created successfully")
        
        # Create the stored procedure using @sproc
        logger.info("Creating PDF generation stored procedure...")
        
        from snowflake.snowpark.functions import sproc
        from snowflake.snowpark.types import StringType
        
        @sproc(
            name=f'{config.SNOWFLAKE["database"]}.{config.SNOWFLAKE["ai_schema"]}.GENERATE_PDF_REPORT', 
            is_permanent=True, 
            stage_location=f'@{config.SNOWFLAKE["database"]}.{config.SNOWFLAKE["ai_schema"]}.PROC_STAGE', 
            replace=True, 
            packages=['snowflake-snowpark-python', 'markdown', 'weasyprint'],
            return_type=StringType(),
            session=session
        )
        def generate_pdf(session: Session, report_content: str, report_type: str, entity_name: str):
            from datetime import datetime
            import re
            import markdown
            import tempfile
            import os
            
            # Generate timestamp for unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            safe_entity_name = re.sub(r'[^a-zA-Z0-9_]', '_', entity_name)[:20]
            pdf_filename = f'glacier_{report_type.lower()}_{safe_entity_name}_{timestamp}.pdf'
            
            with tempfile.TemporaryDirectory() as tmpdir:
                # Convert markdown to HTML
                html_body = markdown.markdown(report_content, extensions=['tables', 'fenced_code'])
                
                # Professional CSS styling for banking reports
                css = """
                @page { size: A4; margin: 2cm; }
                body { font-family: Arial, sans-serif; line-height: 1.6; color: #2C3E50; }
                h1 { color: #1F4E79; border-bottom: 3px solid #1F4E79; padding-bottom: 10px; }
                h2 { color: #2E75B6; border-left: 4px solid #2E75B6; padding-left: 15px; }
                h3 { color: #3F7CAC; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th { background-color: #1F4E79; color: white; padding: 12px; font-weight: bold; }
                td { padding: 10px; border-bottom: 1px solid #ddd; }
                tr:nth-child(even) { background-color: #F8F9FA; }
                .header { text-align: center; margin-bottom: 30px; }
                .footer { margin-top: 30px; font-size: 12px; color: #666; }
                .warning { background-color: #FFF3CD; border: 1px solid #FFEAA7; padding: 15px; margin: 20px 0; }
                .breach { background-color: #F8D7DA; border: 1px solid #F5C6CB; padding: 15px; margin: 20px 0; }
                .disclaimer { background-color: #E9ECEF; border-left: 4px solid #6C757D; padding: 15px; margin: 20px 0; font-style: italic; }
                """
                
                # Glacier First Bank logo (text-based for demo)
                glacier_logo = """
                <div style="text-align: center; background: linear-gradient(135deg, #1F4E79, #2E75B6); color: white; padding: 20px; margin-bottom: 30px; border-radius: 10px;">
                    <h1 style="margin: 0; font-size: 28px; color: white; border: none;">🏔️ GLACIER FIRST BANK</h1>
                    <p style="margin: 5px 0 0 0; font-size: 14px; opacity: 0.9;">Pan-European Universal Bank</p>
                </div>
                """
                
                # Report type specific headers
                if report_type.upper() == 'AML':
                    report_header = f"""
                    <h2 style="color: #C9302C;">🔍 AML/KYC Enhanced Due Diligence Report</h2>
                    <p><strong>Subject Entity:</strong> {entity_name}</p>
                    <p><strong>Report Type:</strong> Anti-Money Laundering & Know Your Customer Analysis</p>
                    """
                elif report_type.upper() == 'CREDIT':
                    report_header = f"""
                    <h2 style="color: #2E75B6;">💰 Credit Risk Assessment Report</h2>
                    <p><strong>Subject Entity:</strong> {entity_name}</p>
                    <p><strong>Report Type:</strong> Commercial Credit Analysis</p>
                    """
                else:
                    report_header = f"""
                    <h2>📊 Financial Analysis Report</h2>
                    <p><strong>Subject Entity:</strong> {entity_name}</p>
                    <p><strong>Report Type:</strong> {report_type}</p>
                    """
                
                # Complete HTML document
                html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <meta charset="UTF-8">
                    <title>Glacier First Bank - {report_type} Report</title>
                    <style>{css}</style>
                </head>
                <body>
                    {glacier_logo}
                    <div class="header">
                        {report_header}
                        <p><strong>Generated:</strong> {datetime.now().strftime('%B %d, %Y at %I:%M %p UTC')}</p>
                        <hr>
                    </div>
                    {html_body}
                    <div class="footer">
                        <hr>
                        <div class="disclaimer">
                            <p><strong>⚠️ Demo Notice:</strong> This analysis uses synthetic data for demonstration purposes only. All entities, transactions, and documents are fictitious and created for training/demo scenarios.</p>
                        </div>
                        <p><strong>Report ID:</strong> GFB-{report_type.upper()}-{timestamp} | <strong>Generated By:</strong> Snowflake Intelligence</p>
                        <p><strong>Entity:</strong> {entity_name} | <strong>Classification:</strong> Internal Use Only</p>
                        <p><em>This report demonstrates AI-powered banking analytics with Snowflake Cortex</em></p>
                    </div>
                </body>
                </html>
                """
                
                # Create HTML file
                html_path = os.path.join(tmpdir, 'report.html')
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Convert HTML to PDF
                import weasyprint
                pdf_path = os.path.join(tmpdir, pdf_filename)
                weasyprint.HTML(filename=html_path).write_pdf(pdf_path)
                
                # Upload to secure stage (get database name from current context)
                database_name = session.sql("SELECT CURRENT_DATABASE() AS db").collect()[0]['DB']
                ai_schema = session.sql("SELECT CURRENT_SCHEMA() AS sch").collect()[0]['SCH']
                stage_path = f"@{database_name}.{config.SNOWFLAKE['ai_schema']}.GLACIER_REPORTS_STAGE"
                session.file.put(pdf_path, stage_path, overwrite=True, auto_compress=False)
                
                # Generate presigned URL for download
                presigned_url = session.sql(
                    f"SELECT GET_PRESIGNED_URL('{stage_path}', '{pdf_filename}') AS url"
                ).collect()[0]['URL']
                
                # Format response with document name as a clickable link
                report_display_name = f"{report_type.upper()} Report - {entity_name}"
                return f"📄 [{report_display_name}]({presigned_url}) - Professional {report_type.lower()} analysis report generated successfully."
        
        logger.info("PDF generation stored procedure created successfully")
        
        # Test the procedure
        logger.info("Testing PDF generation procedure...")
        result = session.call(
            f'{config.SNOWFLAKE["database"]}.{config.SNOWFLAKE["ai_schema"]}.GENERATE_PDF_REPORT',
            'Test PDF generation during setup',
            'ANALYSIS',
            'Setup Test Entity'
        )
        logger.info("PDF generation procedure test successful")
        
    except Exception as e:
        logger.error(f"Failed to create PDF generation tool: {e}")
        raise
    
    logger.info("PDF generation tool creation completed")


def validate_setup(session: Session, scenarios: List[str]) -> bool:
    """Validate the setup for specified scenarios."""
    logger.info(f"Validating setup for scenarios: {scenarios}")
    
    # Import validation here to avoid circular imports
    try:
        from tests.test_scenarios import run_scenario_validation
        results = run_scenario_validation(session, scenarios)
        return results.get('success', False)
    except ImportError:
        logger.warning("Validation module not found, skipping validation")
        return True
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return False


def deploy(connection_name: str, scenarios: List[str], scope: str, scale: str = "demo", validate: bool = True) -> bool:
    """Deploy the demo with specified parameters."""
    global _session
    start_time = datetime.now()
    logger.info("🚀 Starting Glacier First Bank Demo Deployment")
    logger.info(f"📋 Scenarios: {', '.join(scenarios)}")
    logger.info(f"🎯 Scope: {scope}")
    logger.info(f"📊 Scale: {scale}")
    
    session = None
    try:
        # Step 1: Create Snowflake session
        session = create_snowflake_session(connection_name)
        
        # Step 2: Setup based on scope
        if scope in ['all', 'data', 'semantic', 'search', 'agents']:
            logger.info("Step 1: Setting up database infrastructure...")
            generate_structured.create_database_structure(session)
        
        if scope in ['all', 'data']:
            logger.info("Step 2: Generating demo data (structured and unstructured)...")
            generate_demo_data(session, scale, scenarios)
        
        if scope in ['all', 'semantic']:
            logger.info("Step 3: Creating semantic views...")
            create_semantic_views_wrapper(session, scenarios)
        
        if scope in ['all', 'search']:
            logger.info("Step 4: Creating search services...")
            create_search_services_wrapper(session, scenarios)
        
        if scope == 'all':
            logger.info("Step 5: Creating PDF generation tool...")
            create_pdf_generator(session)
        
        if scope in ['all', 'agents']:
            logger.info("Step 6: Creating Snowflake Intelligence agents...")
            create_agents_wrapper(session, scenarios)
        
        # Validation
        if validate:
            logger.info("Step 7: Running validation...")
            validation_passed = validate_setup(session, scenarios)
            if not validation_passed:
                logger.error("Setup validation failed")
                return False
        
        end_time = datetime.now()
        duration = end_time - start_time
        
        logger.info(f"🎉 Glacier First Bank Demo deployment completed successfully!")
        logger.info(f"⏱️  Total time: {duration}")
        logger.info(f"📋 Scenarios: {', '.join(scenarios)}")
        logger.info(f"🎯 Scope: {scope}")
        logger.info(f"📊 Scale: {scale}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Demo deployment failed: {e}")
        return False
    finally:
        if session:
            session.close()
        _session = None


def print_banner():
    """Print deployment banner."""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║           🏔️  GLACIER FIRST BANK AI INTELLIGENCE DEMO           ║
    ║                                                                  ║
    ║                    Phase 1: Foundation Deployment               ║
    ║                                                                  ║
    ║    🤖 AML/KYC Enhanced Due Diligence                            ║
    ║    💰 Credit Risk Analysis & Cohort Modeling                    ║
    ║    🔗 Cross-Domain Intelligence & Risk Contagion               ║
    ║    🧠 Multi-Step Reasoning & Evidence Synthesis                 ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def main():
    """Main entry point for the demo deployment script."""
    parser = argparse.ArgumentParser(
        description='Glacier First Bank AI Intelligence Demo Deployment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Deploy all scenarios with full scope
  python main.py --connection-name my_connection

  # Deploy only AML scenario with demo scale
  python main.py --connection-name my_connection --scenarios aml_kyc_edd --scale demo

  # Deploy only semantic views for all scenarios
  python main.py --connection-name my_connection --scope semantic

  # Deploy data only for credit analysis
  python main.py --connection-name my_connection --scenarios credit_analysis --scope data
        """
    )
    
    # Required arguments
    parser.add_argument('--connection-name', required=True,
                       help='Snowflake connection name (required)')
    
    # Optional arguments
    parser.add_argument('--scenarios', default='all',
                       help='Comma-separated list of scenarios to build, or "all" for all scenarios (default: all)')
    parser.add_argument('--scope', choices=['all', 'data', 'semantic', 'search', 'agents'], default='all',
                       help='Scope of build: all=everything, data=structured+unstructured, semantic=views only, search=services only, agents=agents only (default: all)')
    parser.add_argument('--scale', choices=['mini', 'demo'], default='demo',
                       help='Data generation scale (default: demo)')
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip validation after deployment')
    parser.add_argument('--quiet', action='store_true',
                       help='Suppress banner and detailed output')
    
    args = parser.parse_args()
    
    # Print banner unless quiet mode
    if not args.quiet:
        print_banner()
    
    try:
        # Parse and validate scenarios
        if args.scenarios == 'all':
            scenarios = config.get_all_scenarios()
        else:
            scenarios = [s.strip() for s in args.scenarios.split(',')]
            scenarios = config.validate_scenarios(scenarios)
        
        # Validate scale
        if not config.validate_scale(args.scale):
            logger.error(f"Invalid scale '{args.scale}'. Valid scales: {list(config.SCALES.keys())}")
            sys.exit(1)
        
        # Validate connection and deploy
        validate_connection_name(args.connection_name)
        success = deploy(
            connection_name=args.connection_name,
            scenarios=scenarios,
            scope=args.scope,
            scale=args.scale,
            validate=not args.no_validate
        )
        
        if success:
            if not args.quiet:
                print("\n🚀 Ready to demo! Next steps:")
                print("   1. Access Snowflake Intelligence to interact with AI agents")
                print("   2. Test agents with realistic business queries")
                print("   3. Review agent responses and tool selection")
                print("   4. Monitor performance and adjust as needed")
            sys.exit(0)
        else:
            logger.error("❌ Deployment failed. Check logs for details.")
            sys.exit(1)
        
    except KeyboardInterrupt:
        logger.info("Deployment interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Deployment failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()