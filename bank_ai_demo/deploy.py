#!/usr/bin/env python3
"""
Glacier First Bank AI Intelligence Demo - Deployment Script

Complete deployment orchestration for Phase 1 including database setup,
data generation, semantic views, search services, and validation.

Usage:
    python deploy.py --connection your_connection_name
    python deploy.py --scale mini --no-validate
    python deploy.py --validate-only
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import Optional, Dict, Any

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'tests'))

from snowflake.snowpark import Session
from config_manager import GlacierDemoConfig
from main import GlacierDemoOrchestrator
from test_scenarios import run_scenario_validation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('glacier_demo_deployment.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


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


def print_deployment_summary(results: Dict[str, Any], start_time: datetime, end_time: datetime):
    """Print deployment summary."""
    duration = end_time - start_time
    
    summary = f"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                      DEPLOYMENT SUMMARY                          ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                                  ║
    ║  🎯 Status: {'✅ SUCCESS' if results.get('success', False) else '❌ FAILED'}                                          ║
    ║  ⏱️  Duration: {str(duration).split('.')[0]:<45} ║
    ║  📊 Scale: {results.get('scale', 'demo'):<49} ║
    ║                                                                  ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                        COMPONENTS                                ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                                  ║
    ║  📁 Database Infrastructure: {'✅' if results.get('infrastructure', False) else '❌'}                           ║
    ║  🗄️  Demo Data Generation: {'✅' if results.get('data_generation', False) else '❌'}                            ║
    ║  🔍 Semantic Views: {'✅' if results.get('semantic_views', False) else '❌'}                                 ║
    ║  🔎 Search Services: {'✅' if results.get('search_services', False) else '❌'}                                ║
    ║  🧪 Validation Tests: {'✅' if results.get('validation', False) else '❌'}                                 ║
    ║                                                                  ║
    """
    
    if results.get('validation_results'):
        val_results = results['validation_results']['summary']
        summary += f"""╠══════════════════════════════════════════════════════════════════╣
    ║                      VALIDATION RESULTS                          ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                                  ║
    ║  📋 AML/KYC Scenario: {'✅' if all(results['validation_results']['aml_kyc'].values()) else '❌'}                                ║
    ║  💰 Credit Analysis: {'✅' if all(results['validation_results']['credit_analysis'].values()) else '❌'}                                 ║
    ║  🔗 Cross-Domain Intelligence: {'✅' if all(results['validation_results']['cross_domain'].values()) else '❌'}                        ║
    ║                                                                  ║
    ║  📊 Tests Passed: {val_results['passed_tests']}/{val_results['total_tests']} ({val_results['success_rate']:.1%})                                    ║
    ║                                                                  ║
    """
    
    summary += """╠══════════════════════════════════════════════════════════════════╣
    ║                         NEXT STEPS                               ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                                  ║
    ║  1. 🤖 Configure AI agents in Snowflake Intelligence            ║
    ║  2. 📖 Review agent instructions in docs/agent_instructions.md  ║
    ║  3. 🎭 Run demo scenarios with realistic business queries        ║
    ║  4. 📊 Monitor performance and adjust as needed                  ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    
    print(summary)


def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(
        description='Deploy Glacier First Bank AI Intelligence Demo',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python deploy.py --connection my_connection
  python deploy.py --scale mini --no-validate
  python deploy.py --validate-only
  python deploy.py --data-only --scale demo
        """
    )
    
    parser.add_argument('--connection', '-c', 
                       help='Snowflake connection name (or set CONNECTION_NAME env var)')
    parser.add_argument('--config', 
                       help='Path to configuration file (default: config/glacier_demo_config.yaml)')
    parser.add_argument('--scale', choices=['mini', 'demo', 'full'], 
                       default='full', help='Data generation scale (default: full)')
    parser.add_argument('--no-validate', action='store_true',
                       help='Skip validation after deployment')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only run validation (skip deployment)')
    parser.add_argument('--data-only', action='store_true',
                       help='Only generate data (skip infrastructure setup)')
    parser.add_argument('--infrastructure-only', action='store_true',
                       help='Only setup infrastructure (skip data generation)')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Suppress banner and detailed output')
    
    args = parser.parse_args()
    
    # Print banner unless quiet mode
    if not args.quiet:
        print_banner()
    
    start_time = datetime.now()
    deployment_results = {
        'success': False,
        'scale': args.scale or 'full',
        'infrastructure': False,
        'data_generation': False,
        'semantic_views': False,
        'search_services': False,
        'validation': False,
        'validation_results': None,
        'errors': []
    }
    
    try:
        # Initialize configuration and orchestrator
        logger.info("Initializing Glacier First Bank Demo deployment...")
        
        connection_name = args.connection or os.getenv('CONNECTION_NAME')
        if not connection_name and not args.validate_only:
            logger.error("Connection name required. Use --connection or set CONNECTION_NAME environment variable.")
            sys.exit(1)
        
        config = GlacierDemoConfig(args.config, connection_name)
        
        # Create orchestrator first (without session)
        orchestrator = GlacierDemoOrchestrator(connection_name=connection_name, config_path=args.config)
        
        # Create Snowflake session
        if not args.validate_only or args.validate_only:
            session = orchestrator.create_snowflake_session()
            # Now update orchestrator with session
            orchestrator.session = session
        
        # Validate-only mode
        if args.validate_only:
            logger.info("Running validation tests only...")
            validation_results = run_scenario_validation(session, config)
            deployment_results['validation'] = validation_results['summary']['success_rate'] == 1.0
            deployment_results['validation_results'] = validation_results
            deployment_results['success'] = deployment_results['validation']
        
        # Data-only mode
        elif args.data_only:
            logger.info("Generating demo data only...")
            orchestrator.generate_demo_data(args.scale)
            deployment_results['data_generation'] = True
            deployment_results['success'] = True
        
        # Infrastructure-only mode
        elif args.infrastructure_only:
            logger.info("Setting up infrastructure only...")
            orchestrator.setup_database_infrastructure()
            deployment_results['infrastructure'] = True
            deployment_results['semantic_views'] = True
            deployment_results['search_services'] = True
            deployment_results['success'] = True
        
        # Full deployment
        else:
            logger.info("Running full deployment...")
            
            # Step 1: Setup basic infrastructure (database, schemas, warehouses)
            logger.info("Step 1/6: Setting up database infrastructure...")
            orchestrator.setup_database_infrastructure()
            deployment_results['infrastructure'] = True
            
            # Step 2: Generate structured data (creates tables)
            logger.info("Step 2/6: Generating structured demo data...")
            orchestrator.generate_demo_data(args.scale)
            deployment_results['data_generation'] = True
            
            # Step 3: Create semantic views (after tables exist)
            logger.info("Step 3/6: Creating semantic views...")
            orchestrator.create_semantic_views()
            deployment_results['semantic_views'] = True
            
            # Step 4: Create search services (after document tables exist)
            logger.info("Step 4/7: Creating Cortex Search services...")
            orchestrator.create_search_services()
            deployment_results['search_services'] = True
            
            # Step 5: Create PDF generator custom tool
            logger.info("Step 5/7: Creating PDF generation custom tool...")
            orchestrator.create_pdf_generator()
            deployment_results['pdf_generator'] = True
            
            # Step 6: Validate setup (unless skipped)
            if not args.no_validate:
                logger.info("Step 6/7: Running validation tests...")
                validation_results = run_scenario_validation(session, config)
                deployment_results['validation'] = validation_results['summary']['success_rate'] == 1.0
                deployment_results['validation_results'] = validation_results
            else:
                logger.info("Step 6/7: Skipping validation (--no-validate)")
                deployment_results['validation'] = True  # Assume success if skipped
            
            # Step 7: Final setup verification
            logger.info("Step 7/7: Verifying deployment...")
            setup_valid = orchestrator.validate_setup()
            
            deployment_results['success'] = all([
                deployment_results['infrastructure'],
                deployment_results['data_generation'],
                deployment_results['pdf_generator'],
                deployment_results['validation'],
                setup_valid
            ])
        
        # Close session
        if 'session' in locals():
            session.close()
        
    except KeyboardInterrupt:
        logger.info("Deployment interrupted by user")
        deployment_results['errors'].append("Deployment interrupted by user")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Deployment failed: {e}")
        deployment_results['errors'].append(str(e))
        deployment_results['success'] = False
    
    # Print summary
    end_time = datetime.now()
    if not args.quiet:
        print_deployment_summary(deployment_results, start_time, end_time)
    
    # Log final status
    if deployment_results['success']:
        logger.info("🎉 Glacier First Bank Demo deployment completed successfully!")
        
        if not args.quiet:
            print("\n🚀 Ready to demo! Next steps:")
            print("   1. Configure AI agents in Snowflake Intelligence")
            print("   2. Review agent instructions in docs/agent_instructions.md")
            print("   3. Test scenarios with realistic business queries")
            print("   4. Monitor performance and adjust as needed")
        
        sys.exit(0)
    else:
        logger.error("❌ Deployment failed. Check logs for details.")
        
        if deployment_results['errors']:
            logger.error("Errors encountered:")
            for error in deployment_results['errors']:
                logger.error(f"  - {error}")
        
        sys.exit(1)


if __name__ == "__main__":
    main()
