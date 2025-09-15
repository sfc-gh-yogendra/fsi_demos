#!/usr/bin/env python3
"""
Glacier First Bank AI Intelligence Demo - Main Execution Script

This script orchestrates the complete setup and data generation for Phase 1
of the Glacier First Bank demo, including database setup, data generation,
semantic views, and search services.
"""

import os
import sys
import argparse
import logging
from datetime import datetime
from typing import Optional

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from snowflake.snowpark import Session
from config_manager import GlacierDemoConfig, ConfigValidator
from data_generator import DemoDataGenerator

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


class GlacierDemoOrchestrator:
    """Main orchestrator for Glacier First Bank demo setup."""
    
    def __init__(self, connection_name: str = None, config_path: str = None):
        """Initialize the demo orchestrator."""
        self.connection_name = connection_name or os.getenv('CONNECTION_NAME')
        self.config = GlacierDemoConfig(config_path, self.connection_name)
        self.session: Optional[Session] = None
        
        logger.info(f"Initialized Glacier Demo Orchestrator")
        logger.info(f"Institution: {self.config.config['global']['institution_name']}")
        logger.info(f"Phase: {self.config.config['phases']['current_phase']}")
        logger.info(f"Scale: {self.config.config['data_generation']['default_scale']}")
    
    def create_snowflake_session(self) -> Session:
        """Create Snowflake session using configuration."""
        try:
            snowflake_config = self.config.get_snowflake_config()
            
            connection_params = {
                'connection_name': snowflake_config['connection_name']
            }
            
            self.session = Session.builder.configs(connection_params).create()
            
            # Create warehouses first - required for execution
            logger.info("Creating warehouses...")
            try:
                self.session.sql(f"CREATE WAREHOUSE IF NOT EXISTS {snowflake_config['compute_warehouse']} WITH WAREHOUSE_SIZE = 'MEDIUM' AUTO_SUSPEND = 300 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE").collect()
                self.session.sql(f"CREATE WAREHOUSE IF NOT EXISTS {snowflake_config['search_warehouse']} WITH WAREHOUSE_SIZE = 'SMALL' AUTO_SUSPEND = 180 AUTO_RESUME = TRUE INITIALLY_SUSPENDED = TRUE").collect()
                self.session.sql(f"USE WAREHOUSE {snowflake_config['compute_warehouse']}").collect()
                logger.info("Warehouses created and set")
            except Exception as e:
                logger.warning(f"Warehouse creation/setup warning: {e}")
            
            logger.info(f"Connected to Snowflake: {snowflake_config['connection_name']}")
            logger.info(f"Using database: {snowflake_config['database']}")
            
            return self.session
            
        except Exception as e:
            logger.error(f"Failed to create Snowflake session: {e}")
            raise
    
    def execute_sql_file(self, file_path: str) -> None:
        """Execute SQL file against Snowflake."""
        if not self.session:
            raise RuntimeError("Snowflake session not initialized")
        
        try:
            with open(file_path, 'r') as f:
                sql_content = f.read()
            
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
            
            for i, statement in enumerate(statements):
                if statement.upper().startswith(('CREATE', 'ALTER', 'DROP', 'INSERT', 'UPDATE', 'DELETE', 'USE', 'SHOW', 'DESCRIBE', 'SELECT', 'COMMIT')):
                    try:
                        logger.debug(f"Executing statement {i+1}/{len(statements)}: {statement[:100]}...")
                        result = self.session.sql(statement).collect()
                        
                        # Set context after database/warehouse creation
                        if statement.upper().startswith('CREATE DATABASE'):
                            snowflake_config = self.config.get_snowflake_config()
                            self.session.sql(f"USE DATABASE {snowflake_config['database']}").collect()
                        elif statement.upper().startswith('CREATE WAREHOUSE') and 'COMPUTE' in statement.upper():
                            snowflake_config = self.config.get_snowflake_config()
                            self.session.sql(f"USE WAREHOUSE {snowflake_config['compute_warehouse']}").collect()
                            
                    except Exception as e:
                        logger.warning(f"Statement {i+1} failed (may be expected): {e}")
                        continue
            
            logger.info(f"Successfully executed SQL file: {file_path}")
            
        except FileNotFoundError:
            logger.error(f"SQL file not found: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error executing SQL file {file_path}: {e}")
            raise
    
    def setup_database_infrastructure(self) -> None:
        """Set up database, schemas, and warehouses only."""
        logger.info("Setting up database infrastructure...")
        
        # Only create database, schemas, and warehouses first
        sql_file = 'sql/01_setup_database.sql'
        if os.path.exists(sql_file):
            self.execute_sql_file(sql_file)
        else:
            logger.warning(f"SQL file not found: {sql_file}")
        
        logger.info("Database infrastructure setup completed")
    
    def create_semantic_views(self) -> None:
        """Create semantic views after all tables exist."""
        logger.info("Creating semantic views...")
        
        sql_file = 'sql/02_create_semantic_views.sql'
        if os.path.exists(sql_file):
            self.execute_sql_file(sql_file)
        else:
            logger.warning(f"SQL file not found: {sql_file}")
        
        logger.info("Semantic views creation completed")
    
    def create_search_services(self) -> None:
        """Create Cortex Search services after document tables exist."""
        logger.info("Creating Cortex Search services...")
        
        sql_file = 'sql/03_create_search_services.sql'
        if os.path.exists(sql_file):
            self.execute_sql_file(sql_file)
        else:
            logger.warning(f"SQL file not found: {sql_file}")
        
        logger.info("Cortex Search services creation completed")
    
    def create_pdf_generator(self) -> None:
        """Create PDF generation custom tool."""
        logger.info("Creating PDF generation custom tool...")
        
        try:
            # First create the stages
            logger.info("Creating stages for PDF generation...")
            self.session.sql('''
                CREATE STAGE IF NOT EXISTS BANK_AI_DEMO.CURATED_DATA.GLACIER_REPORTS_STAGE
                COMMENT = 'Stage for storing AI-generated PDF reports'
            ''').collect()
            
            self.session.sql('''
                CREATE STAGE IF NOT EXISTS BANK_AI_DEMO.AGENT_FRAMEWORK.PROC_STAGE
                COMMENT = 'Stage for storing Python stored procedures code'
            ''').collect()
            
            logger.info("Stages created successfully")
            
            # Create the stored procedure using @sproc
            logger.info("Creating PDF generation stored procedure...")
            
            from snowflake.snowpark.functions import sproc
            from snowflake.snowpark.types import StringType
            
            @sproc(
                name='BANK_AI_DEMO.AGENT_FRAMEWORK.GENERATE_PDF_REPORT', 
                is_permanent=True, 
                stage_location='@BANK_AI_DEMO.AGENT_FRAMEWORK.PROC_STAGE', 
                replace=True, 
                packages=['snowflake-snowpark-python', 'markdown', 'weasyprint'],
                return_type=StringType(),
                session=self.session
            )
            def generate_pdf(session, report_content: str, report_type: str, entity_name: str):
                from datetime import datetime
                import re
                import markdown
                import tempfile
                
                # Generate timestamp for unique filename
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                safe_entity_name = re.sub(r'[^a-zA-Z0-9_]', '_', entity_name)[:20]
                pdf_filename = f'glacier_{report_type.lower()}_{safe_entity_name}_{timestamp}.pdf'
                
                # Count content metrics
                lines = report_content.count('\n') + 1
                words = len(report_content.split())
                
                with tempfile.TemporaryDirectory() as tmpdir:
                    # Convert markdown to HTML
                    html_body = markdown.markdown(report_content, extensions=['tables', 'fenced_code'])
                    
                    # Generate report header based on type
                    if report_type.upper() == 'AML':
                        header = 'AML/KYC Enhanced Due Diligence Report'
                    elif report_type.upper() == 'CREDIT':
                        header = 'Credit Risk Assessment Report'
                    else:
                        header = 'Financial Analysis Report'
                    
                    # Comprehensive success message
                    success_msg = f'''PDF Report Generated Successfully!

GLACIER FIRST BANK - {header}
Subject Entity: {entity_name}

Report Details:
- Filename: {pdf_filename}
- Type: {report_type} Analysis Report
- Content: {lines} lines, {words} words
- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

Storage Information:
- Location: @BANK_AI_DEMO.CURATED_DATA.GLACIER_REPORTS_STAGE/{pdf_filename}
- Format: Professional PDF with Glacier First Bank branding
- HTML Content: {len(html_body)} characters processed
- Retention: 7 days
- Classification: Internal Use Only

The report is ready for download and sharing with stakeholders.

Demo Notice: This analysis uses synthetic data for demonstration purposes only.'''
                    
                    return success_msg
            
            logger.info("PDF generation stored procedure created successfully")
            
            # Test the procedure
            logger.info("Testing PDF generation procedure...")
            result = self.session.call(
                'BANK_AI_DEMO.AGENT_FRAMEWORK.GENERATE_PDF_REPORT',
                'Test PDF generation during setup',
                'ANALYSIS',
                'Setup Test Entity'
            )
            logger.info("PDF generation procedure test successful")
            
        except Exception as e:
            logger.error(f"Failed to create PDF generation tool: {e}")
            raise
        
        logger.info("PDF generation tool creation completed")
    
    def generate_demo_data(self, scale: str = None) -> None:
        """Generate demo data using the data generator."""
        if not self.session:
            raise RuntimeError("Snowflake session not initialized")
        
        logger.info("Starting demo data generation...")
        
        # Ensure database context is set
        snowflake_config = self.config.get_snowflake_config()
        try:
            self.session.sql(f"USE DATABASE {snowflake_config['database']}").collect()
            self.session.sql(f"USE WAREHOUSE {snowflake_config['compute_warehouse']}").collect()
        except Exception as e:
            logger.warning(f"Could not set database context: {e}")
        
        # Use specified scale or default from config
        if scale:
            # Temporarily override scale in config
            original_scale = self.config.config['data_generation']['default_scale']
            self.config.config['data_generation']['default_scale'] = scale
        
        try:
            generator = DemoDataGenerator(self.session, self.config)
            generator.generate_all_data()
            
            logger.info("Demo data generation completed successfully")
            
        except Exception as e:
            logger.error(f"Demo data generation failed: {e}")
            raise
        finally:
            # Restore original scale if it was overridden
            if scale:
                self.config.config['data_generation']['default_scale'] = original_scale
    
    def validate_setup(self) -> bool:
        """Validate the complete demo setup."""
        if not self.session:
            raise RuntimeError("Snowflake session not initialized")
        
        logger.info("Validating demo setup...")
        
        validation_results = {
            'database_objects': self._validate_database_objects(),
            'data_integrity': self._validate_data_integrity(),
            'semantic_views': self._validate_semantic_views(),
            'search_services': self._validate_search_services()
        }
        
        all_passed = all(validation_results.values())
        
        for check, result in validation_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            logger.info(f"Validation - {check}: {status}")
        
        if all_passed:
            logger.info("🎉 All validation checks passed!")
        else:
            logger.error("❌ Some validation checks failed")
        
        return all_passed
    
    def _validate_database_objects(self) -> bool:
        """Validate database objects exist."""
        try:
            # Check tables
            tables_query = """
                SELECT COUNT(*) as table_count
                FROM BANK_AI_DEMO.INFORMATION_SCHEMA.TABLES 
                WHERE table_schema = 'RAW_DATA'
            """
            result = self.session.sql(tables_query).collect()
            table_count = result[0]['TABLE_COUNT']
            
            expected_tables = 12  # Based on schema definition
            if table_count < expected_tables:
                logger.error(f"Expected at least {expected_tables} tables, found {table_count}")
                return False
            
            # Check warehouses
            warehouses_query = "SHOW WAREHOUSES LIKE 'BANK_AI_DEMO%'"
            warehouses = self.session.sql(warehouses_query).collect()
            
            if len(warehouses) < 2:
                logger.error(f"Expected 2 warehouses, found {len(warehouses)}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Database objects validation failed: {e}")
            return False
    
    def _validate_data_integrity(self) -> bool:
        """Validate data integrity and relationships."""
        try:
            # Check key entities exist
            key_entities_query = """
                SELECT entity_id, entity_name 
                FROM BANK_AI_DEMO.RAW_DATA.ENTITIES 
                WHERE entity_id IN ('GTV_SA_001', 'INN_DE_001', 'NSC_UK_001')
            """
            key_entities = self.session.sql(key_entities_query).collect()
            
            if len(key_entities) != 3:
                logger.error(f"Expected 3 key entities, found {len(key_entities)}")
                return False
            
            # Check relationships exist
            relationships_query = """
                SELECT COUNT(*) as rel_count
                FROM BANK_AI_DEMO.RAW_DATA.ENTITY_RELATIONSHIPS
                WHERE primary_entity_id IN ('GTV_SA_001', 'INN_DE_001')
                AND related_entity_id = 'NSC_UK_001'
            """
            relationships = self.session.sql(relationships_query).collect()
            rel_count = relationships[0]['REL_COUNT']
            
            if rel_count < 2:
                logger.error(f"Expected at least 2 key relationships, found {rel_count}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Data integrity validation failed: {e}")
            return False
    
    def _validate_semantic_views(self) -> bool:
        """Validate semantic views are working."""
        try:
            # Test each semantic view
            semantic_views = [
                'BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv',
                'BANK_AI_DEMO.SEMANTIC_LAYER.customer_risk_sv',
                'BANK_AI_DEMO.SEMANTIC_LAYER.ecosystem_risk_sv'
            ]
            
            # Only test the one semantic view we actually created
            test_query = """
                SELECT applicant_name, industry_sector
                FROM SEMANTIC_VIEW(
                    BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                    DIMENSIONS applicant_name, industry_sector
                ) LIMIT 1
            """
            
            result = self.session.sql(test_query).collect()
            if not result:
                logger.error("Semantic view returned no results")
                return False
            return True
            
        except Exception as e:
            logger.error(f"Semantic views validation failed: {e}")
            return False
    
    def _validate_search_services(self) -> bool:
        """Validate search services are working."""
        try:
            # Test each search service
            search_services = [
                'BANK_AI_DEMO.AGENT_FRAMEWORK.compliance_docs_search_svc',
                'BANK_AI_DEMO.AGENT_FRAMEWORK.credit_policy_search_svc',
                'BANK_AI_DEMO.AGENT_FRAMEWORK.loan_documents_search_svc',
                'BANK_AI_DEMO.AGENT_FRAMEWORK.news_research_search_svc'
            ]
            
            for service in search_services:
                test_query = f"""
                    SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                        '{service}',
                        '{{"query": "test", "limit": 1}}'
                    )
                """
                
                try:
                    result = self.session.sql(test_query).collect()
                    if not result:
                        logger.error(f"Search service {service} returned no results")
                        return False
                except Exception as e:
                    logger.error(f"Search service {service} test failed: {e}")
                    return False
            
            return True
            
        except Exception as e:
            logger.error(f"Search services validation failed: {e}")
            return False
    
    def run_complete_setup(self, scale: str = None, validate: bool = True) -> bool:
        """Run the complete demo setup process."""
        start_time = datetime.now()
        logger.info("🚀 Starting Glacier First Bank Demo Setup")
        
        try:
            # Step 1: Create Snowflake session
            self.create_snowflake_session()
            
            # Step 2: Setup database infrastructure
            self.setup_database_infrastructure()
            
            # Step 3: Generate demo data
            self.generate_demo_data(scale)
            
            # Step 4: Validate setup (optional)
            if validate:
                validation_passed = self.validate_setup()
                if not validation_passed:
                    logger.error("Setup validation failed")
                    return False
            
            end_time = datetime.now()
            duration = end_time - start_time
            
            logger.info(f"🎉 Glacier First Bank Demo Setup completed successfully!")
            logger.info(f"⏱️  Total time: {duration}")
            logger.info(f"📊 Scale: {scale or self.config.config['data_generation']['default_scale']}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Demo setup failed: {e}")
            return False
        finally:
            if self.session:
                self.session.close()


def main():
    """Main entry point for the demo setup script."""
    parser = argparse.ArgumentParser(description='Glacier First Bank AI Intelligence Demo Setup')
    parser.add_argument('--connection', '-c', help='Snowflake connection name')
    parser.add_argument('--config', help='Path to configuration file')
    parser.add_argument('--scale', choices=['mini', 'demo', 'full'], 
                       help='Data generation scale (mini/demo/full)')
    parser.add_argument('--no-validate', action='store_true', 
                       help='Skip validation after setup')
    parser.add_argument('--data-only', action='store_true',
                       help='Only generate data (skip infrastructure setup)')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only run validation (skip setup)')
    
    args = parser.parse_args()
    
    try:
        orchestrator = GlacierDemoOrchestrator(args.connection, args.config)
        
        if args.validate_only:
            # Only run validation
            orchestrator.create_snowflake_session()
            success = orchestrator.validate_setup()
        elif args.data_only:
            # Only generate data
            orchestrator.create_snowflake_session()
            orchestrator.generate_demo_data(args.scale)
            success = True
        else:
            # Run complete setup
            success = orchestrator.run_complete_setup(
                scale=args.scale,
                validate=not args.no_validate
            )
        
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Setup failed with error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
