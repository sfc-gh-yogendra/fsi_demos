"""
Glacier First Bank Demo Data Generator

Generates realistic demo data for Phase 1 scenarios with cross-domain intelligence
through shared ecosystem relationships and contradictory evidence patterns.
"""

import uuid
import random
from datetime import datetime, date, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json
import logging
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit, call_function
from snowflake.snowpark.types import StructType, StructField, StringType, IntegerType, DecimalType, DateType, TimestampType

from config_manager import GlacierDemoConfig

logger = logging.getLogger(__name__)


@dataclass
class EntityProfile:
    """Data class for entity profiles with realistic business characteristics."""
    entity_id: str
    entity_name: str
    entity_type: str
    country_code: str
    industry_sector: str
    incorporation_date: date
    regulatory_status: str
    esg_rating: str
    annual_revenue: Optional[float] = None
    employee_count: Optional[int] = None
    risk_factors: Optional[List[str]] = None


class DemoDataGenerator:
    """Main data generator for Glacier First Bank demo."""
    
    def __init__(self, session: Session, config: GlacierDemoConfig):
        self.session = session
        self.config = config
        self.scale_config = config.get_scale_config()
        self.key_entities = config.config['data_generation']['key_entities']
        self.themes = config.get_market_themes()
        
        # Set random seed for reproducible generation
        random.seed(config.config['global']['generation_seed'])
        
        logger.info(f"Initialized data generator with {self.scale_config['description']} scale")
    
    def generate_all_data(self) -> None:
        """Generate all demo data for Phase 1."""
        logger.info("Starting Phase 1 data generation...")
        
        # Generate in dependency order
        self.generate_entities()
        self.generate_entity_relationships()
        self.generate_customers()
        self.generate_transactions()
        self.generate_loan_applications()
        self.generate_historical_loans()
        self.generate_compliance_documents()
        self.generate_credit_policy_documents()
        self.generate_loan_documents()
        self.generate_news_and_research()
        self.generate_external_data_simulation()
        
        logger.info("Phase 1 data generation completed successfully")
    
    def generate_entities(self) -> None:
        """Generate entities with key demo entities guaranteed."""
        logger.info("Generating entities...")
        
        entities = []
        
        # Generate key entities first (guaranteed for scenarios)
        for entity_key, entity_spec in self.key_entities.items():
            entity = EntityProfile(
                entity_id=entity_spec['entity_id'],
                entity_name=entity_spec['name'],
                entity_type='CORPORATE',
                country_code=entity_spec['country'],
                industry_sector=entity_spec['industry'],
                incorporation_date=self._generate_incorporation_date(),
                regulatory_status=entity_spec.get('regulatory_status', 'ACTIVE'),
                esg_rating=entity_spec.get('esg_rating', 'B')
            )
            entities.append(entity)
        
        # Generate additional entities to reach scale target
        additional_count = self.scale_config['entities'] - len(entities)
        entities.extend(self._generate_additional_entities(additional_count))
        
        # Convert to DataFrame and save
        entity_data = [self._entity_to_dict(entity) for entity in entities]
        entities_df = self.session.create_dataframe(entity_data)
        entities_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.ENTITIES", mode="overwrite")
        
        logger.info(f"Generated {len(entities)} entities ({len(self.key_entities)} key entities)")
    
    def generate_entity_relationships(self) -> None:
        """Generate entity relationships for cross-domain intelligence."""
        logger.info("Generating entity relationships...")
        
        # Get existing entities
        entities_df = self.session.table("BANK_AI_DEMO.RAW_DATA.ENTITIES")
        entities = entities_df.collect()
        
        relationships = []
        
        # Create key relationships for demo scenarios
        key_relationships = [
            # Northern Supply Chain as shared vendor
            {
                'primary': 'GTV_SA_001',  # Global Trade Ventures
                'related': 'NSC_UK_001',  # Northern Supply Chain
                'type': 'VENDOR',
                'strength': 'PRIMARY',
                'risk_score': 0.85
            },
            {
                'primary': 'INN_DE_001',  # Innovate GmbH
                'related': 'NSC_UK_001',  # Northern Supply Chain
                'type': 'VENDOR',
                'strength': 'SECONDARY',
                'risk_score': 0.45
            },
            # Customer relationship
            {
                'primary': 'INN_DE_001',  # Innovate GmbH
                'related': 'GTV_SA_001',  # Global Trade Ventures
                'type': 'CUSTOMER',
                'strength': 'INDIRECT',
                'risk_score': 0.25
            }
        ]
        
        for rel in key_relationships:
            relationship = {
                'relationship_id': str(uuid.uuid4()),
                'primary_entity_id': rel['primary'],
                'related_entity_id': rel['related'],
                'relationship_type': rel['type'],
                'relationship_strength': rel['strength'],
                'effective_date': self._generate_relationship_date(),
                'end_date': None,
                'risk_impact_score': rel['risk_score'],
                'created_date': datetime.now()
            }
            relationships.append(relationship)
        
        # Generate additional random relationships
        additional_count = self.scale_config['entity_relationships'] - len(relationships)
        for i in range(additional_count):
            # Select random entities for relationships
            primary_entity = random.choice(entities)
            related_entity = random.choice(entities)
            
            # Avoid self-relationships
            if primary_entity['ENTITY_ID'] != related_entity['ENTITY_ID']:
                relationship = {
                    'relationship_id': str(uuid.uuid4()),
                    'primary_entity_id': primary_entity['ENTITY_ID'],
                    'related_entity_id': related_entity['ENTITY_ID'],
                    'relationship_type': random.choice(['VENDOR', 'CUSTOMER', 'COMPETITOR', 'SUBSIDIARY']),
                    'relationship_strength': random.choice(['PRIMARY', 'SECONDARY', 'INDIRECT']),
                    'effective_date': self._generate_relationship_date(),
                    'end_date': None,
                    'risk_impact_score': random.uniform(0.1, 0.9),
                    'created_date': datetime.now()
                }
                relationships.append(relationship)
        
        # Save to database
        relationships_df = self.session.create_dataframe(relationships)
        relationships_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.ENTITY_RELATIONSHIPS", mode="overwrite")
        
        logger.info(f"Generated {len(relationships)} entity relationships")
    
    def generate_customers(self) -> None:
        """Generate customer profiles linked to entities."""
        logger.info("Generating customers...")
        
        # Get entities that should be customers
        entities_df = self.session.table("BANK_AI_DEMO.RAW_DATA.ENTITIES")
        entities = entities_df.filter(col("ENTITY_TYPE") == "CORPORATE").collect()
        
        customers = []
        
        # Create customers for key entities
        key_entity_ids = [spec['entity_id'] for spec in self.key_entities.values()]
        
        for entity in entities[:self.scale_config['customers']]:
            is_key_entity = entity['ENTITY_ID'] in key_entity_ids
            
            # Set risk characteristics for key entities
            if entity['ENTITY_ID'] == 'GTV_SA_001':  # Global Trade Ventures
                risk_rating = 'HIGH'
                kyc_status = 'REQUIRES_EDD'
                aml_flags = 2
            elif entity['ENTITY_ID'] == 'INN_DE_001':  # Innovate GmbH
                risk_rating = 'MEDIUM'
                kyc_status = 'COMPLETE'
                aml_flags = 0
            else:
                risk_rating = random.choice(['LOW', 'MEDIUM', 'HIGH'])
                kyc_status = random.choice(['COMPLETE', 'PENDING', 'REQUIRES_EDD'])
                aml_flags = random.randint(0, 3) if risk_rating == 'HIGH' else random.randint(0, 1)
            
            customer = {
                'customer_id': f"CUST_{entity['ENTITY_ID']}",
                'entity_id': entity['ENTITY_ID'],
                'customer_type': 'CORPORATE',
                'onboarding_date': self._generate_onboarding_date(),
                'risk_rating': risk_rating,
                'kyc_status': kyc_status,
                'last_review_date': self._generate_review_date(),
                'next_review_date': self._generate_next_review_date(),
                'relationship_manager': self._generate_rm_name(),
                'aml_flags': aml_flags,
                'created_date': datetime.now()
            }
            customers.append(customer)
        
        # Save to database
        customers_df = self.session.create_dataframe(customers)
        customers_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.CUSTOMERS", mode="overwrite")
        
        logger.info(f"Generated {len(customers)} customers")
    
    def generate_loan_applications(self) -> None:
        """Generate loan applications with realistic financial metrics."""
        logger.info("Generating loan applications...")
        
        # Get customers
        customers_df = self.session.table("BANK_AI_DEMO.RAW_DATA.CUSTOMERS")
        customers = customers_df.collect()
        
        applications = []
        
        # Create specific application for Innovate GmbH (key credit scenario)
        innovate_customer = next((c for c in customers if c['ENTITY_ID'] == 'INN_DE_001'), None)
        if innovate_customer:
            app = self._create_innovate_loan_application(innovate_customer)
            applications.append(app)
        
        # Generate additional applications
        remaining_customers = [c for c in customers if c['ENTITY_ID'] != 'INN_DE_001']
        additional_count = min(self.scale_config['loan_applications'] - 1, len(remaining_customers))
        
        for customer in remaining_customers[:additional_count]:
            app = self._create_loan_application(customer)
            applications.append(app)
        
        # Save to database
        applications_df = self.session.create_dataframe(applications)
        applications_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.LOAN_APPLICATIONS", mode="overwrite")
        
        logger.info(f"Generated {len(applications)} loan applications")
    
    def generate_historical_loans(self) -> None:
        """Generate historical loan performance data for cohort analysis."""
        logger.info("Generating historical loans...")
        
        loans = []
        
        # Generate loans across different time periods and risk profiles
        for _ in range(self.scale_config['historical_loans']):
            loan = self._create_historical_loan()
            loans.append(loan)
        
        # Save to database
        loans_df = self.session.create_dataframe(loans)
        loans_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.HISTORICAL_LOANS", mode="overwrite")
        
        logger.info(f"Generated {len(loans)} historical loans")
    
    def generate_compliance_documents(self) -> None:
        """Generate compliance documents using Cortex Complete pipeline."""
        logger.info("Generating compliance documents...")
        
        # Step 1: Generate dynamic prompts based on structured data
        prompts = []
        
        # Get entities for document generation
        entities_df = self.session.table("BANK_AI_DEMO.RAW_DATA.ENTITIES")
        entities = entities_df.collect()
        
        # Generate prompts for key entities
        key_entities = ['GTV_SA_001', 'INN_DE_001', 'NSC_UK_001']
        for entity in entities:
            if entity['ENTITY_ID'] in key_entities:
                prompts.extend(self._create_onboarding_prompts(entity))
                prompts.extend(self._create_adverse_media_prompts(entity))
        
        # Step 2: Store prompts in Snowflake table
        if prompts:
            prompts_df = self.session.create_dataframe(prompts)
            prompts_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENT_PROMPTS", mode="overwrite")
            
            # Step 3-5: Generate content using Cortex Complete and save final documents
            self.session.sql("""
                CREATE OR REPLACE TABLE BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENTS AS
                SELECT 
                    PROMPT_ID AS ID,
                    DOCUMENT_TITLE AS TITLE,
                    SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', PROMPT_TEXT) AS CONTENT,
                    ENTITY_NAME,
                    DOC_TYPE,
                    PUBLISH_DATE,
                    RISK_SIGNAL,
                    SOURCE,
                    LANGUAGE,
                    CONFIDENCE_SCORE,
                    CREATED_DATE
                FROM BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENT_PROMPTS
                WHERE PROMPT_TEXT IS NOT NULL
            """).collect()
            
            # Validate generated content
            result = self.session.sql("SELECT COUNT(*) as cnt FROM BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENTS WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
            doc_count = result[0]['CNT']
            logger.info(f"Generated {doc_count} compliance documents using Cortex Complete")
        else:
            logger.warning("No prompts generated for compliance documents")
    
    def generate_credit_policy_documents(self) -> None:
        """Generate credit policy documents using Cortex Complete pipeline."""
        logger.info("Generating credit policy documents...")
        
        # Step 1: Generate dynamic prompts for policy documents
        prompts = self._create_policy_document_prompts()
        
        # Step 2: Store prompts in Snowflake table
        if prompts:
            prompts_df = self.session.create_dataframe(prompts)
            prompts_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.CREDIT_POLICY_PROMPTS", mode="overwrite")
            
            # Step 3-5: Generate content using Cortex Complete and save final documents
            self.session.sql("""
                CREATE OR REPLACE TABLE BANK_AI_DEMO.RAW_DATA.CREDIT_POLICY_DOCUMENTS AS
                SELECT 
                    PROMPT_ID AS ID,
                    DOCUMENT_TITLE AS TITLE,
                    SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', PROMPT_TEXT) AS CONTENT,
                    POLICY_SECTION,
                    EFFECTIVE_DATE,
                    VERSION,
                    REGULATORY_FRAMEWORK,
                    LANGUAGE,
                    CREATED_DATE
                FROM BANK_AI_DEMO.RAW_DATA.CREDIT_POLICY_PROMPTS
                WHERE PROMPT_TEXT IS NOT NULL
            """).collect()
            
            # Validate generated content
            result = self.session.sql("SELECT COUNT(*) as cnt FROM BANK_AI_DEMO.RAW_DATA.CREDIT_POLICY_DOCUMENTS WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
            doc_count = result[0]['CNT']
            logger.info(f"Generated {doc_count} credit policy documents using Cortex Complete")
        else:
            logger.warning("No prompts generated for credit policy documents")
    
    def generate_loan_documents(self) -> None:
        """Generate loan documents using Cortex Complete pipeline."""
        logger.info("Generating loan documents...")
        
        # Step 1: Generate dynamic prompts based on loan applications
        applications_df = self.session.table("BANK_AI_DEMO.RAW_DATA.LOAN_APPLICATIONS")
        applications = applications_df.collect()
        
        prompts = []
        
        # Generate business plan prompts for key applications
        for app in applications:
            if app['APPLICANT_NAME'] == 'Innovate GmbH':  # Key demo application
                prompts.extend(self._create_business_plan_prompts(app))
        
        # Step 2: Store prompts in Snowflake table
        if prompts:
            prompts_df = self.session.create_dataframe(prompts)
            prompts_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.LOAN_DOCUMENT_PROMPTS", mode="overwrite")
            
            # Step 3-5: Generate content using Cortex Complete and save final documents
            self.session.sql("""
                CREATE OR REPLACE TABLE BANK_AI_DEMO.RAW_DATA.LOAN_DOCUMENTS AS
                SELECT 
                    PROMPT_ID AS ID,
                    DOCUMENT_TITLE AS TITLE,
                    SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', PROMPT_TEXT) AS CONTENT,
                    APPLICANT_NAME,
                    DOC_TYPE,
                    UPLOAD_DATE,
                    DOCUMENT_SECTION,
                    PROCESSING_STATUS,
                    LANGUAGE,
                    CREATED_DATE
                FROM BANK_AI_DEMO.RAW_DATA.LOAN_DOCUMENT_PROMPTS
                WHERE PROMPT_TEXT IS NOT NULL
            """).collect()
            
            # Validate generated content
            result = self.session.sql("SELECT COUNT(*) as cnt FROM BANK_AI_DEMO.RAW_DATA.LOAN_DOCUMENTS WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
            doc_count = result[0]['CNT']
            logger.info(f"Generated {doc_count} loan documents using Cortex Complete")
        else:
            logger.warning("No prompts generated for loan documents")
    
    def generate_news_and_research(self) -> None:
        """Generate news articles using Cortex Complete pipeline."""
        logger.info("Generating news and research documents...")
        
        # Step 1: Generate dynamic prompts for news articles
        prompts = self._create_news_article_prompts()
        
        # Step 2: Store prompts in Snowflake table
        if prompts:
            prompts_df = self.session.create_dataframe(prompts)
            prompts_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.NEWS_ARTICLE_PROMPTS", mode="overwrite")
            
            # Step 3-5: Generate content using Cortex Complete and save final documents
            self.session.sql("""
                CREATE OR REPLACE TABLE BANK_AI_DEMO.RAW_DATA.NEWS_AND_RESEARCH AS
                SELECT 
                    PROMPT_ID AS ID,
                    DOCUMENT_TITLE AS TITLE,
                    SNOWFLAKE.CORTEX.COMPLETE('llama3.1-70b', PROMPT_TEXT) AS CONTENT,
                    ENTITY_NAME,
                    ARTICLE_TYPE,
                    PUBLISH_DATE,
                    SOURCE,
                    SENTIMENT_SCORE,
                    ESG_RELEVANCE,
                    SUPPLY_CHAIN_RELEVANCE,
                    INFLATION_RELEVANCE,
                    LANGUAGE,
                    CREATED_DATE
                FROM BANK_AI_DEMO.RAW_DATA.NEWS_ARTICLE_PROMPTS
                WHERE PROMPT_TEXT IS NOT NULL
            """).collect()
            
            # Validate generated content
            result = self.session.sql("SELECT COUNT(*) as cnt FROM BANK_AI_DEMO.RAW_DATA.NEWS_AND_RESEARCH WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
            doc_count = result[0]['CNT']
            logger.info(f"Generated {doc_count} news and research documents using Cortex Complete")
        else:
            logger.warning("No prompts generated for news and research documents")
    
    def generate_transactions(self) -> None:
        """Generate transaction history for customers."""
        logger.info("Generating transactions...")
        
        # Get customers
        customers_df = self.session.table("BANK_AI_DEMO.RAW_DATA.CUSTOMERS")
        customers = customers_df.collect()
        
        transactions = []
        
        # Generate transactions for each customer
        for customer in customers:
            customer_transactions = self._generate_customer_transactions(customer)
            transactions.extend(customer_transactions)
        
        # Save to database (in batches for large datasets)
        batch_size = 10000
        for i in range(0, len(transactions), batch_size):
            batch = transactions[i:i + batch_size]
            batch_df = self.session.create_dataframe(batch)
            mode = "overwrite" if i == 0 else "append"
            batch_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.TRANSACTIONS", mode=mode)
        
        logger.info(f"Generated {len(transactions)} transactions")
    
    def _generate_customer_transactions(self, customer: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate transactions for a specific customer."""
        transactions = []
        
        # Generate transaction count based on customer risk
        if customer['RISK_RATING'] == 'HIGH':
            transaction_count = random.randint(80, 120)
        elif customer['RISK_RATING'] == 'MEDIUM':
            transaction_count = random.randint(40, 80)
        else:
            transaction_count = random.randint(20, 40)
        
        for i in range(transaction_count):
            transaction = {
                'TRANSACTION_ID': f'TXN_{customer["CUSTOMER_ID"]}_{i+1:04d}',
                'CUSTOMER_ID': customer['CUSTOMER_ID'],
                'TRANSACTION_DATE': datetime.now() - timedelta(days=random.randint(1, 365)),
                'AMOUNT': random.uniform(1000, 100000),
                'CURRENCY': 'EUR',
                'TRANSACTION_TYPE': random.choice(['CREDIT', 'DEBIT', 'TRANSFER']),
                'COUNTERPARTY_NAME': random.choice(['European Trading Co', 'Nordic Logistics Ltd', 'Baltic Import/Export']),
                'COUNTERPARTY_COUNTRY': random.choice(['DEU', 'FRA', 'NLD', 'BEL']),
                'DESCRIPTION': random.choice(['Trade settlement', 'Service payment', 'Equipment purchase']),
                'RISK_SCORE': random.uniform(0.1, 0.8) if customer['RISK_RATING'] == 'HIGH' else random.uniform(0.1, 0.4),
                'SUSPICIOUS_ACTIVITY_FLAG': random.choice([True, False]) if random.random() < 0.05 else False,
                'CREATED_DATE': datetime.now()
            }
            transactions.append(transaction)
        
        return transactions
    
    def _create_historical_loan(self) -> Dict[str, Any]:
        """Create a single historical loan record."""
        origination_year = random.randint(2019, 2023)
        origination_date = date(origination_year, random.randint(1, 12), random.randint(1, 28))
        
        loan = {
            'LOAN_ID': f'HIST_LOAN_{str(uuid.uuid4())[:8].upper()}',
            'CUSTOMER_ID': None,  # Historical loans may not have current customer IDs
            'APPLICANT_NAME': f'{random.choice(["Tech", "Euro", "Nordic", "Baltic"])} {random.choice(["Solutions", "Industries", "Holdings", "Services"])} {random.choice(["Ltd", "S.A.", "GmbH"])}',
            'ORIGINATION_DATE': origination_date,
            'MATURITY_DATE': origination_date + timedelta(days=random.randint(1095, 2190)),  # 3-6 years
            'ORIGINAL_AMOUNT': random.uniform(500000, 20000000),
            'CURRENCY': 'EUR',
            'INDUSTRY_SECTOR': random.choice(['Software Services', 'Manufacturing', 'Healthcare', 'Financial Services']),
            'DEBT_TO_EQUITY_AT_ORIGINATION': random.uniform(1.0, 5.0),
            'DSCR_AT_ORIGINATION': random.uniform(0.8, 2.5),
            'CURRENT_RATIO_AT_ORIGINATION': random.uniform(0.8, 2.0),
            'CLIENT_CONCENTRATION_AT_ORIGINATION': random.uniform(15, 85),
            'LOAN_STATUS': random.choice(['PERFORMING', 'PERFORMING', 'PERFORMING', 'DEFAULTED']),  # 75% performing
            'DEFAULT_DATE': None,
            'LOSS_AMOUNT': None,
            'CREATED_DATE': datetime.now()
        }
        
        # Set default details for defaulted loans
        if loan['LOAN_STATUS'] == 'DEFAULTED':
            default_days = random.randint(365, 1460)  # Default within 1-4 years
            loan['DEFAULT_DATE'] = loan['ORIGINATION_DATE'] + timedelta(days=default_days)
            loan['LOSS_AMOUNT'] = loan['ORIGINAL_AMOUNT'] * random.uniform(0.2, 0.8)
        
        return loan
    
    def _create_onboarding_prompts(self, entity: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create onboarding document prompts for an entity."""
        prompts = []
        
        if entity['ENTITY_ID'] == 'GTV_SA_001':
            # Special case for Global Trade Ventures with PEP connections
            prompt_text = f"""Create a comprehensive corporate onboarding document for {entity['ENTITY_NAME']}, a Luxembourg-incorporated international trade company.

REQUIREMENTS:
- Document type: Corporate Onboarding Documentation
- Word count: 800-1500 words
- Language: Professional en-GB banking terminology
- Include sections: Corporate Structure, Beneficial Ownership, Business Purpose, Regulatory Status

SPECIFIC CONTENT REQUIREMENTS:
- Legal Name: {entity['ENTITY_NAME']}
- Incorporation: Luxembourg, 15 March 2019
- Registration Number: B-247891
- Business Purpose: International trade facilitation and logistics coordination

BENEFICIAL OWNERSHIP STRUCTURE:
Ultimate Beneficial Owners (>25% ownership):
1. Marcus Weber (German National) - 60% ownership
2. Elena Rossi (Italian National) - 40% ownership
   - PEP Status: Yes (Family member of former Italian Transport Minister)
   - Father: Antonio Rossi (Italian Transport Minister 2015-2018)

RISK ASSESSMENT:
- Overall Risk Rating: Medium
- PEP Risk: Medium (family connection, no direct involvement)

Format as a professional KYC onboarding document with clear sections and regulatory compliance language."""

            prompts.append({
                'PROMPT_ID': f'GTV_ONBOARD_001',
                'DOCUMENT_TITLE': f'{entity["ENTITY_NAME"]} - Corporate Onboarding Documentation',
                'PROMPT_TEXT': prompt_text,
                'ENTITY_NAME': entity['ENTITY_NAME'],
                'DOC_TYPE': 'Onboarding',
                'PUBLISH_DATE': date(2024, 3, 15),
                'RISK_SIGNAL': 'Medium',
                'SOURCE': 'Internal KYC Team',
                'LANGUAGE': 'en-GB',
                'CONFIDENCE_SCORE': 0.95,
                'CREATED_DATE': datetime.now()
            })
        
        return prompts
    
    def _create_adverse_media_prompts(self, entity: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create adverse media prompts for an entity."""
        prompts = []
        
        if entity['ENTITY_ID'] == 'GTV_SA_001':
            # Adverse media for Elena Rossi (UBO of Global Trade Ventures)
            prompt_text = f"""Create a Reuters news article about Italian political corruption investigation affecting Elena Rossi, who is a UBO of {entity['ENTITY_NAME']}.

REQUIREMENTS:
- Document type: Adverse Media / News Article
- Word count: 400-800 words
- Language: Professional journalism en-GB
- Publication: Reuters
- Date: 12 June 2024

SPECIFIC CONTENT REQUIREMENTS:
- Headline: Italian Transport Ministry Contracts Under Parliamentary Scrutiny
- Focus: Parliamentary investigation into Antonio Rossi's tenure as Transport Minister (2015-2018)
- Key allegations: Rossi Logistics Solutions received preferential treatment in contract awards
- Contract value: €2.3M awarded between 2016-2017
- Opposition claims: "clear conflict of interest"
- Current status: Italian Anti-Corruption Authority investigation launched May 2024
- Elena Rossi connection: Daughter of Antonio Rossi, business executive in private sector
- Investigation status: Parliamentary inquiry ongoing, no criminal charges filed to date
- Expected timeline: Preliminary findings by September 2024

Format as a professional Reuters news article with proper journalism structure and objective tone."""

            prompts.append({
                'PROMPT_ID': f'REUTERS_IT_POLITICAL_20240612',
                'DOCUMENT_TITLE': 'Italian Transport Ministry Contracts Under Investigation',
                'PROMPT_TEXT': prompt_text,
                'ENTITY_NAME': 'Elena Rossi',
                'DOC_TYPE': 'Adverse Media',
                'PUBLISH_DATE': date(2024, 6, 12),
                'RISK_SIGNAL': 'Medium',
                'SOURCE': 'Reuters via Snowflake Marketplace',
                'LANGUAGE': 'en-GB',
                'CONFIDENCE_SCORE': 0.88,
                'CREATED_DATE': datetime.now()
            })
        
        return prompts
    
    def _create_policy_document_prompts(self) -> List[Dict[str, Any]]:
        """Create credit policy document prompts."""
        prompts = []
        
        # Policy document with ratio thresholds
        ratio_prompt = """Create a comprehensive Mid-Market Lending Policy document focusing on financial ratio thresholds.

REQUIREMENTS:
- Document type: Credit Policy - Ratio Thresholds
- Word count: 1000-2000 words
- Language: Professional en-GB banking terminology
- Version: v3.2
- Effective Date: 1 January 2024

SPECIFIC CONTENT REQUIREMENTS:
Section 4.1: Financial Ratio Thresholds

4.1.1 Debt-to-Equity Ratio
- Warning Threshold: >3.0
- Breach Threshold: >3.5
- Rationale: Excessive leverage increases default risk

4.1.2 Debt Service Coverage Ratio (DSCR)
- Warning Threshold: <1.25
- Breach Threshold: <1.10
- Rationale: Insufficient cash flow to service debt obligations

4.1.3 Current Ratio
- Warning Threshold: <1.20
- Breach Threshold: <1.10
- Rationale: Liquidity concerns for short-term obligations

Include sections on: Policy Statement, Threshold Definitions, Approval Procedures, Monitoring Requirements, Escalation Procedures, and Review Schedule.

Format as a professional banking policy document with clear structure and regulatory compliance language."""

        prompts.append({
            'PROMPT_ID': 'POLICY_RATIOS_V32',
            'DOCUMENT_TITLE': 'Mid-Market Lending Policy v3.2 - Ratio Thresholds',
            'PROMPT_TEXT': ratio_prompt,
            'POLICY_SECTION': 'Ratio Thresholds',
            'EFFECTIVE_DATE': date(2024, 1, 1),
            'VERSION': 'v3.2',
            'REGULATORY_FRAMEWORK': 'Internal',
            'LANGUAGE': 'en-GB',
            'CREATED_DATE': datetime.now()
        })
        
        # Concentration limits policy
        concentration_prompt = """Create a Commercial Credit Risk Policy document focusing on client concentration limits.

REQUIREMENTS:
- Document type: Credit Risk Policy - Concentration Limits
- Word count: 1000-2000 words
- Language: Professional en-GB banking terminology
- Version: v2.1
- Effective Date: 15 March 2024

SPECIFIC CONTENT REQUIREMENTS:
Section 5.3: Client Concentration Risk

5.3.1 Single Client Concentration
- Warning Threshold: >60% of revenue from single client
- Breach Threshold: >70% of revenue from single client
- Mitigation: Require diversification plan for breaches

Rationale: Over-dependence on single client creates revenue volatility risk.

Include sections on: Policy Statement, Concentration Definitions, Risk Assessment Framework, Mitigation Requirements, Monitoring Procedures, and Reporting Standards.

Authority: Credit Risk Committee
Format as a professional banking policy document with clear structure and risk management focus."""

        prompts.append({
            'PROMPT_ID': 'POLICY_CONCENTRATION_V21',
            'DOCUMENT_TITLE': 'Commercial Credit Risk Policy v2.1 - Concentration Limits',
            'PROMPT_TEXT': concentration_prompt,
            'POLICY_SECTION': 'Concentration Limits',
            'EFFECTIVE_DATE': date(2024, 3, 15),
            'VERSION': 'v2.1',
            'REGULATORY_FRAMEWORK': 'Internal',
            'LANGUAGE': 'en-GB',
            'CREATED_DATE': datetime.now()
        })
        
        return prompts
    
    def _create_business_plan_prompts(self, application: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create business plan document prompts for a loan application."""
        prompts = []
        
        if application['APPLICANT_NAME'] == 'Innovate GmbH':
            prompt_text = f"""Create a comprehensive business plan for {application['APPLICANT_NAME']}, a German software services company applying for a €{application['REQUESTED_AMOUNT']/1000000:.1f}M loan.

REQUIREMENTS:
- Document type: Business Plan 2024-2029
- Word count: 2000-4000 words
- Language: Professional en-GB business terminology
- Application context: {application['LOAN_PURPOSE']}

SPECIFIC CONTENT REQUIREMENTS:
Company Overview:
- Legal Name: {application['APPLICANT_NAME']}
- Industry: {application['INDUSTRY_SECTOR']}
- Annual Revenue: €{application['ANNUAL_REVENUE']/1000000:.1f}M
- Total Assets: €{application['TOTAL_ASSETS']/1000000:.1f}M
- EBITDA: €{application['EBITDA']/1000000:.1f}M

EXECUTIVE SUMMARY:
{application['APPLICANT_NAME']} is a leading {application['INDUSTRY_SECTOR']} company specializing in enterprise solutions for mid-market clients across Germany and Europe.

MARKET STRATEGY:
- Target market: Mid-market enterprises (€10M-€100M revenue)
- Geographic expansion: DACH region focus with selective European expansion
- Service diversification: AI/ML consulting and cloud migration services
- Key differentiator: Industry-specific solutions with rapid deployment

FINANCIAL PROJECTIONS:
- Revenue growth: 25% CAGR 2024-2029
- EBITDA margin target: 18-22%
- Investment required: €{application['REQUESTED_AMOUNT']/1000000:.1f}M for expansion and working capital

RISK FACTORS:
- Client concentration: {application['SINGLE_CLIENT_CONCENTRATION_PCT']:.0f}% revenue from top 3 clients
- Competition from larger consulting firms
- Market volatility in {application['INDUSTRY_SECTOR']} sector
- Dependency on key technical personnel

Include sections: Executive Summary, Market Strategy, Financial Projections, Key Personnel, Risk Factors, Use of Funds.
Format as a professional business plan with clear structure and financial analysis."""

            prompts.append({
                'PROMPT_ID': f'INNOVATE_GMBH_BUSINESS_PLAN_2024',
                'DOCUMENT_TITLE': f'{application["APPLICANT_NAME"]} - Business Plan 2024-2029',
                'PROMPT_TEXT': prompt_text,
                'APPLICANT_NAME': application['APPLICANT_NAME'],
                'DOC_TYPE': 'Business Plan',
                'UPLOAD_DATE': application['APPLICATION_DATE'],
                'DOCUMENT_SECTION': 'Market Strategy',
                'PROCESSING_STATUS': 'PROCESSED',
                'LANGUAGE': 'en-GB',
                'CREATED_DATE': datetime.now()
            })
        
        return prompts
    
    def _create_news_article_prompts(self) -> List[Dict[str, Any]]:
        """Create news article prompts based on market themes."""
        prompts = []
        
        # Supply chain disruption article about Northern Supply Chain Ltd
        supply_chain_prompt = """Create a Reuters news article about European supply chain disruptions affecting technology companies.

REQUIREMENTS:
- Document type: News Article
- Word count: 300-600 words
- Language: Professional journalism en-GB
- Publication: Reuters via Snowflake Marketplace
- Date: 15 August 2024

SPECIFIC CONTENT REQUIREMENTS:
- Headline: European Supply Chain Disruptions Continue to Impact Technology Sector
- Focus: Technology companies adapting to new operational realities
- Key entity: Northern Supply Chain Ltd (key logistics provider for European tech firms)
- Impact: Software services sector particularly affected by supply chain partner reliability issues
- Response: Northern Supply Chain Ltd implementing new risk management protocols
- Timeline: Challenges expected to continue throughout 2024
- Industry context: Operational challenges affecting business planning across technology sectors

Format as a professional Reuters news article with objective journalism tone and proper structure."""

        prompts.append({
            'PROMPT_ID': 'NEWS_SUPPLY_CHAIN_001',
            'DOCUMENT_TITLE': 'European Supply Chain Disruptions Continue to Impact Technology Sector',
            'PROMPT_TEXT': supply_chain_prompt,
            'ENTITY_NAME': 'Northern Supply Chain Ltd',
            'ARTICLE_TYPE': 'News',
            'PUBLISH_DATE': date(2024, 8, 15),
            'SOURCE': 'Reuters via Snowflake Marketplace',
            'SENTIMENT_SCORE': -0.2,
            'ESG_RELEVANCE': False,
            'SUPPLY_CHAIN_RELEVANCE': True,
            'INFLATION_RELEVANCE': False,
            'LANGUAGE': 'en-GB',
            'CREATED_DATE': datetime.now()
        })
        
        return prompts
    
    def generate_external_data_simulation(self) -> None:
        """Generate external data provider simulation tables."""
        logger.info("Generating external data provider simulation...")
        
        # Generate S&P Global financials
        self._generate_sp_global_financials()
        
    def _generate_sp_global_financials(self) -> None:
        """Generate S&P Global financial data simulation."""
        financials = []
        
        companies = ['Global Trade Ventures S.A.', 'Innovate GmbH', 'Northern Supply Chain Ltd']
        
        for company in companies:
            for year in range(2020, 2025):
                financial = {
                    'COMPANY_ID': f'SP_{company.replace(" ", "_").replace(".", "").upper()}',
                    'COMPANY_NAME': company,
                    'TICKER_SYMBOL': f'{company[:3].upper()}{random.randint(100, 999)}',
                    'COUNTRY_CODE': random.choice(['LUX', 'DEU', 'GBR']),
                    'INDUSTRY_CODE': random.randint(1000, 9999),
                    'FISCAL_YEAR': year,
                    'FISCAL_PERIOD': 'FY',
                    'REVENUE': random.uniform(5000000, 50000000),
                    'EBITDA': random.uniform(500000, 5000000),
                    'NET_INCOME': random.uniform(100000, 2000000),
                    'TOTAL_ASSETS': random.uniform(10000000, 100000000),
                    'TOTAL_DEBT': random.uniform(2000000, 20000000),
                    'SHAREHOLDERS_EQUITY': random.uniform(5000000, 30000000),
                    'OPERATING_CASH_FLOW': random.uniform(1000000, 8000000),
                    'CAPEX': random.uniform(500000, 3000000),
                    'CURRENCY': 'EUR',
                    'REPORT_DATE': date(year, 12, 31),
                    'DATA_SOURCE': 'S&P Global Market Intelligence via Snowflake Marketplace',
                    'LAST_UPDATED': datetime.now()
                }
                financials.append(financial)
        
        if financials:
            financials_df = self.session.create_dataframe(financials)
            financials_df.write.save_as_table("BANK_AI_DEMO.RAW_DATA.SP_GLOBAL_COMPANY_FINANCIALS", mode="overwrite")
        
        logger.info("External data provider simulation completed")
    
    def _generate_reuters_news_feed(self) -> None:
        """Generate Reuters news feed simulation."""
        # This is handled by the main news generation pipeline
        pass
    
    def _generate_dj_pep_database(self) -> None:
        """Generate Dow Jones PEP database simulation."""
        # This is handled by the main compliance documents pipeline
        pass
    
    # Helper methods for specific data generation
    
    def _entity_to_dict(self, entity: EntityProfile) -> Dict[str, Any]:
        """Convert EntityProfile to dictionary for DataFrame."""
        return {
            'entity_id': entity.entity_id,
            'entity_name': entity.entity_name,
            'entity_type': entity.entity_type,
            'country_code': entity.country_code,
            'industry_sector': entity.industry_sector,
            'incorporation_date': entity.incorporation_date,
            'regulatory_status': entity.regulatory_status,
            'esg_rating': entity.esg_rating,
            'created_date': datetime.now(),
            'last_updated': datetime.now()
        }
    
    def _generate_incorporation_date(self) -> date:
        """Generate realistic incorporation date."""
        start_date = date(2010, 1, 1)
        end_date = date(2022, 12, 31)
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    def _generate_additional_entities(self, count: int) -> List[EntityProfile]:
        """Generate additional entities beyond key entities."""
        entities = []
        
        countries = ['DEU', 'FRA', 'NLD', 'BEL', 'LUX', 'ITA', 'ESP', 'GBR']
        industries = [
            'Software Services', 'Manufacturing', 'Financial Services',
            'Healthcare', 'Retail', 'Construction', 'Energy', 'Transportation'
        ]
        esg_ratings = ['A+', 'A', 'B+', 'B', 'C+', 'C', 'D']
        
        for i in range(count):
            entity = EntityProfile(
                entity_id=f"ENT_{str(uuid.uuid4())[:8].upper()}",
                entity_name=self._generate_company_name(),
                entity_type='CORPORATE',
                country_code=random.choice(countries),
                industry_sector=random.choice(industries),
                incorporation_date=self._generate_incorporation_date(),
                regulatory_status=random.choice(['ACTIVE', 'UNDER_REVIEW']),
                esg_rating=random.choice(esg_ratings)
            )
            entities.append(entity)
        
        return entities
    
    def _generate_company_name(self) -> str:
        """Generate realistic company names."""
        prefixes = ['Euro', 'Global', 'Advanced', 'Innovative', 'Strategic', 'Dynamic', 'Premier']
        roots = ['Tech', 'Solutions', 'Systems', 'Industries', 'Services', 'Group', 'Holdings']
        suffixes = ['GmbH', 'S.A.', 'Ltd', 'B.V.', 'S.p.A.', 'AG']
        
        return f"{random.choice(prefixes)} {random.choice(roots)} {random.choice(suffixes)}"
    
    def _create_innovate_loan_application(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Create specific loan application for Innovate GmbH with policy breaches."""
        return {
            'application_id': 'INN-DE-2024-003',
            'customer_id': customer['CUSTOMER_ID'],
            'applicant_name': 'Innovate GmbH',
            'application_date': date(2024, 9, 15),
            'requested_amount': 8500000.00,  # €8.5M
            'currency': 'EUR',
            'loan_purpose': 'Business expansion and working capital',
            'term_months': 60,
            'application_status': 'UNDER_REVIEW',
            'industry_sector': 'Software Services',
            'annual_revenue': 12500000.00,  # €12.5M
            'total_assets': 8750000.00,
            'total_liabilities': 6200000.00,
            'ebitda': 1875000.00,
            'debt_service_coverage_ratio': 1.15,  # Below warning threshold (1.25)
            'debt_to_equity_ratio': 3.2,  # Above warning threshold (3.0)
            'current_ratio': 1.18,  # Below warning threshold (1.20)
            'single_client_concentration_pct': 72.0,  # Above breach threshold (70%)
            'created_date': datetime.now()
        }
    
    def _create_loan_application(self, customer: Dict[str, Any]) -> Dict[str, Any]:
        """Create realistic loan application."""
        # Generate realistic financial metrics
        annual_revenue = random.uniform(1000000, 50000000)  # €1M - €50M
        
        return {
            'application_id': f"APP_{str(uuid.uuid4())[:8].upper()}",
            'customer_id': customer['CUSTOMER_ID'],
            'applicant_name': customer['ENTITY_ID'],  # Will be joined with entity name
            'application_date': self._generate_application_date(),
            'requested_amount': random.uniform(500000, 20000000),
            'currency': 'EUR',
            'loan_purpose': random.choice(['Working capital', 'Equipment purchase', 'Business expansion', 'Refinancing']),
            'term_months': random.choice([36, 48, 60, 84]),
                'application_status': random.choice(['SUBMITTED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED']),
            'industry_sector': random.choice(['Manufacturing', 'Services', 'Technology', 'Healthcare']),
            'annual_revenue': annual_revenue,
            'total_assets': annual_revenue * random.uniform(0.5, 1.5),
            'total_liabilities': annual_revenue * random.uniform(0.3, 0.8),
            'ebitda': annual_revenue * random.uniform(0.1, 0.25),
            'debt_service_coverage_ratio': random.uniform(0.8, 2.5),
            'debt_to_equity_ratio': random.uniform(1.0, 4.0),
            'current_ratio': random.uniform(0.8, 2.0),
            'single_client_concentration_pct': random.uniform(10, 80),
            'created_date': datetime.now()
        }
    
    def _generate_key_compliance_documents(self) -> List[Dict[str, Any]]:
        """Generate key compliance documents for demo scenarios."""
        documents = []
        
        # Global Trade Ventures onboarding document
        gtv_onboarding = {
            'id': 'GTV_ONBOARD_001',
            'title': 'Global Trade Ventures S.A. - Corporate Onboarding Documentation',
            'content': self._generate_gtv_onboarding_content(),
            'entity_name': 'Global Trade Ventures S.A.',
            'doc_type': 'Onboarding',
            'publish_date': date(2024, 3, 15),
            'risk_signal': 'Medium',
            'source': 'Internal KYC Team',
            'language': 'en-GB',
            'confidence_score': 0.95,
            'created_date': datetime.now()
        }
        documents.append(gtv_onboarding)
        
        # Elena Rossi adverse media
        elena_adverse = {
            'id': 'REUTERS_IT_POLITICAL_20240612',
            'title': 'Italian Transport Ministry Contracts Under Investigation',
            'content': self._generate_elena_adverse_content(),
            'entity_name': 'Elena Rossi',
            'doc_type': 'Adverse Media',
            'publish_date': date(2024, 6, 12),
            'risk_signal': 'Medium',
            'source': 'Reuters via Snowflake Marketplace',
            'language': 'en-GB',
            'confidence_score': 0.88,
            'created_date': datetime.now()
        }
        documents.append(elena_adverse)
        
        return documents
    
    def _generate_gtv_onboarding_content(self) -> str:
        """Generate realistic onboarding document content for Global Trade Ventures."""
        return """
        CORPORATE ONBOARDING DOCUMENTATION
        Global Trade Ventures S.A.
        
        ENTITY INFORMATION:
        - Legal Name: Global Trade Ventures S.A.
        - Incorporation: Luxembourg, 15 March 2019
        - Registration Number: B-247891
        - Business Purpose: International trade facilitation and logistics coordination
        - Registered Address: 12 Avenue de la Liberté, L-1930 Luxembourg
        
        BENEFICIAL OWNERSHIP STRUCTURE:
        
        Ultimate Beneficial Owners (>25% ownership):
        1. Marcus Weber (German National)
           - Ownership: 60%
           - Date of Birth: 15 April 1975
           - Nationality: German
           - Occupation: Business Executive
           - PEP Status: No
           - Sanctions Check: Clear
        
        2. Elena Rossi (Italian National)
           - Ownership: 40%
           - Date of Birth: 22 September 1980
           - Nationality: Italian
           - Occupation: International Trade Consultant
           - PEP Status: Yes (Family member of former Italian Transport Minister)
           - Father: Antonio Rossi (Italian Transport Minister 2015-2018)
           - Sanctions Check: Clear
        
        BUSINESS ACTIVITIES:
        - Import/export facilitation between EU and non-EU countries
        - Customs clearance and documentation services
        - Supply chain optimization consulting
        - Primary markets: Germany, France, Netherlands, Belgium
        
        REGULATORY STATUS:
        - Luxembourg CSSF registration pending
        - EU AML compliance framework applicable
        - Enhanced due diligence required due to PEP connection
        
        RISK ASSESSMENT:
        - Overall Risk Rating: Medium
        - Geographic Risk: Low (EU operations)
        - Business Risk: Medium (trade finance sector)
        - PEP Risk: Medium (family connection, no direct involvement)
        
        KYC OFFICER: Sarah Mitchell
        REVIEW DATE: 15 March 2024
        NEXT REVIEW: 15 September 2024
        """
    
    def _generate_elena_adverse_content(self) -> str:
        """Generate adverse media content for Elena Rossi."""
        return """
        Italian Transport Ministry Contracts Under Parliamentary Scrutiny
        
        ROME, 12 June 2024 (Reuters) - The Italian Parliament's Anti-Corruption Committee has launched an investigation into procurement practices during Antonio Rossi's tenure as Transport Minister (2015-2018), focusing on contracts awarded to family-connected businesses.
        
        The inquiry centres on €2.3 million in government contracts awarded to Rossi Logistics Solutions, a company with family connections to the former minister. Parliamentary investigators allege the contracts were awarded without proper competitive tender processes.
        
        KEY ALLEGATIONS:
        - Rossi Logistics Solutions received preferential treatment in contract awards
        - Procurement procedures allegedly bypassed standard competitive bidding
        - Contracts totalling €2.3M awarded between 2016-2017
        - Opposition parties claim "clear conflict of interest"
        
        FAMILY RESPONSE:
        A spokesperson for the Rossi family categorically denied any impropriety: "All contracts were awarded based on technical merit and competitive pricing. The family business operated independently of any ministerial influence."
        
        INVESTIGATION STATUS:
        - Italian Anti-Corruption Authority investigation launched May 2024
        - Parliamentary inquiry ongoing
        - No criminal charges filed to date
        - Rossi Logistics Solutions continues normal operations
        
        POLITICAL CONTEXT:
        The investigation comes amid broader scrutiny of procurement practices in Italian infrastructure projects. Opposition leader Marco Bianchi stated: "The timing and scale of contracts awarded to businesses with family connections raises serious questions about procurement integrity."
        
        Former Transport Minister Antonio Rossi, who left office in 2018, has not responded to requests for comment. His daughter Elena Rossi, listed as a director of several international trade companies, was not available for comment.
        
        The Anti-Corruption Authority is expected to publish preliminary findings by September 2024.
        
        (Reporting by Giuseppe Martinelli; Editing by Sarah Chen)
        """
    
    # Additional helper methods would continue here...
    # (Truncated for brevity - the full implementation would include all remaining generation methods)
    
    def _generate_application_date(self) -> date:
        """Generate realistic application date."""
        start_date = date(2024, 1, 1)
        end_date = date(2024, 9, 30)
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    def _generate_onboarding_date(self) -> date:
        """Generate realistic customer onboarding date."""
        start_date = date(2020, 1, 1)
        end_date = date(2024, 8, 31)
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)
    
    def _generate_review_date(self) -> date:
        """Generate last review date."""
        return date.today() - timedelta(days=random.randint(30, 365))
    
    def _generate_next_review_date(self) -> date:
        """Generate next review date."""
        return date.today() + timedelta(days=random.randint(30, 365))
    
    def _generate_rm_name(self) -> str:
        """Generate relationship manager name."""
        first_names = ['James', 'Sarah', 'Michael', 'Emma', 'David', 'Lisa', 'Robert', 'Anna']
        last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis']
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    def _generate_relationship_date(self) -> date:
        """Generate relationship effective date."""
        start_date = date(2020, 1, 1)
        end_date = date(2024, 8, 31)
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randrange(days_between)
        return start_date + timedelta(days=random_days)


def main():
    """Main function for testing data generation."""
    from snowflake.snowpark import Session
    import os
    
    # This would be replaced with actual Snowflake connection
    print("Data generator module loaded successfully")
    print("Use generate_all_data() method to create demo data")


if __name__ == "__main__":
    main()
