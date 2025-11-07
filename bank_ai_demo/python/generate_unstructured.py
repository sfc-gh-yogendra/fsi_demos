"""
Glacier First Bank Demo - Unstructured Data Generator

Generates realistic unstructured documents using Snowflake Cortex Complete.
Includes compliance documents, credit policies, loan documents, and news articles.
"""

from datetime import datetime, date, timedelta
from typing import Dict, List, Any
import logging
import random
from snowflake.snowpark import Session

import config

logger = logging.getLogger(__name__)


def generate_all_unstructured_data(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate all unstructured data for Phase 1 and Phase 2."""
    logger.info("Starting unstructured data generation...")
    
    # Determine which phases to generate based on scenarios
    phase_2_scenarios = ['corp_relationship_manager', 'wealth_advisor']
    include_phase_2 = scenarios and any(s in phase_2_scenarios for s in scenarios) if scenarios != ["all"] else False
    
    # Phase 1 unstructured documents using Cortex Complete pipeline
    generate_compliance_documents(session, scale, scenarios)
    generate_credit_policy_documents(session, scale, scenarios)
    generate_loan_documents(session, scale, scenarios)
    generate_news_and_research(session, scale, scenarios)
    
    # Always generate document templates as they're used by agent framework
    generate_document_templates(session, scale, scenarios)
    
    # Phase 2 unstructured documents (if Phase 2 scenarios requested or "all")
    if include_phase_2 or scenarios == ["all"] or not scenarios:
        logger.info("Generating Phase 2 unstructured data...")
        generate_client_documents(session, scale, scenarios)
        generate_wealth_meeting_notes(session, scale, scenarios)
    
    logger.info("Unstructured data generation completed successfully")


def generate_compliance_documents(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate compliance documents using Cortex Complete pipeline."""
    logger.info("Generating compliance documents...")
    
    # Step 1: Generate dynamic prompts based on structured data
    prompts = []
    
    # Get entities for document generation
    entities_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES")
    entities = entities_df.collect()
    
    # Generate prompts for key entities
    key_entities = ['GTV_SA_001', 'INN_DE_001', 'NSC_UK_001']
    for entity in entities:
        if entity['ENTITY_ID'] in key_entities:
            prompts.extend(_create_onboarding_prompts(entity))
            prompts.extend(_create_adverse_media_prompts(entity))
    
    # Step 2: Store prompts in Snowflake table
    if prompts:
        prompts_df = session.create_dataframe(prompts)
        prompts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.COMPLIANCE_DOCUMENT_PROMPTS", mode="overwrite")
        
        # Step 3-5: Generate content using Cortex Complete and save final documents
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.COMPLIANCE_DOCUMENTS AS
            SELECT 
                PROMPT_ID AS ID,
                DOCUMENT_TITLE AS TITLE,
                SNOWFLAKE.CORTEX.COMPLETE('{config.LLM_MODEL}', PROMPT_TEXT) AS CONTENT,
                ENTITY_NAME,
                DOC_TYPE,
                PUBLISH_DATE,
                RISK_SIGNAL,
                SOURCE,
                LANGUAGE,
                CONFIDENCE_SCORE,
                CREATED_DATE
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.COMPLIANCE_DOCUMENT_PROMPTS
            WHERE PROMPT_TEXT IS NOT NULL
        """).collect()
        
        # Validate generated content
        result = session.sql(f"SELECT COUNT(*) as cnt FROM {config.SNOWFLAKE['database']}.RAW_DATA.COMPLIANCE_DOCUMENTS WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
        doc_count = result[0]['CNT']
        logger.info(f"Generated {doc_count} compliance documents using Cortex Complete")
    else:
        logger.warning("No prompts generated for compliance documents")


def generate_credit_policy_documents(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate credit policy documents using Cortex Complete pipeline."""
    logger.info("Generating credit policy documents...")
    
    # Step 1: Generate dynamic prompts for policy documents
    prompts = _create_policy_document_prompts()
    
    # Step 2: Store prompts in Snowflake table
    if prompts:
        prompts_df = session.create_dataframe(prompts)
        prompts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CREDIT_POLICY_PROMPTS", mode="overwrite")
        
        # Step 3-5: Generate content using Cortex Complete and save final documents
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.CREDIT_POLICY_DOCUMENTS AS
            SELECT 
                PROMPT_ID AS ID,
                DOCUMENT_TITLE AS TITLE,
                SNOWFLAKE.CORTEX.COMPLETE('{config.LLM_MODEL}', PROMPT_TEXT) AS CONTENT,
                POLICY_SECTION,
                EFFECTIVE_DATE,
                VERSION,
                REGULATORY_FRAMEWORK,
                LANGUAGE,
                CREATED_DATE
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.CREDIT_POLICY_PROMPTS
            WHERE PROMPT_TEXT IS NOT NULL
        """).collect()
        
        # Validate generated content
        result = session.sql(f"SELECT COUNT(*) as cnt FROM {config.SNOWFLAKE['database']}.RAW_DATA.CREDIT_POLICY_DOCUMENTS WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
        doc_count = result[0]['CNT']
        logger.info(f"Generated {doc_count} credit policy documents using Cortex Complete")
    else:
        logger.warning("No prompts generated for credit policy documents")


def generate_loan_documents(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate loan documents using Cortex Complete pipeline."""
    logger.info("Generating loan documents...")
    
    # Step 1: Generate dynamic prompts based on loan applications
    applications_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.LOAN_APPLICATIONS")
    applications = applications_df.collect()
    
    prompts = []
    
    # Generate business plan prompts for key applications
    # Use GTV_SA_001 which has both entity and customer records (and loan applications)
    key_applicant_id = config.KEY_ENTITIES['primary_aml_subject']['entity_id']  # GTV_SA_001
    for app in applications:
        if app['APPLICANT_NAME'] == key_applicant_id:  # Key demo application
            prompts.extend(_create_business_plan_prompts(app))
    
    # Step 2: Store prompts in Snowflake table
    if prompts:
        prompts_df = session.create_dataframe(prompts)
        prompts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.LOAN_DOCUMENT_PROMPTS", mode="overwrite")
        
        # Step 3-5: Generate content using Cortex Complete and save final documents
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.LOAN_DOCUMENTS AS
            SELECT 
                PROMPT_ID AS ID,
                DOCUMENT_TITLE AS TITLE,
                SNOWFLAKE.CORTEX.COMPLETE('{config.LLM_MODEL}', PROMPT_TEXT) AS CONTENT,
                APPLICANT_NAME,
                DOC_TYPE,
                UPLOAD_DATE,
                DOCUMENT_SECTION,
                PROCESSING_STATUS,
                LANGUAGE,
                CREATED_DATE
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.LOAN_DOCUMENT_PROMPTS
            WHERE PROMPT_TEXT IS NOT NULL
        """).collect()
        
        # Validate generated content
        result = session.sql(f"SELECT COUNT(*) as cnt FROM {config.SNOWFLAKE['database']}.RAW_DATA.LOAN_DOCUMENTS WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
        doc_count = result[0]['CNT']
        logger.info(f"Generated {doc_count} loan documents using Cortex Complete")
    else:
        logger.warning("No prompts generated for loan documents")


def generate_news_and_research(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate news articles using Cortex Complete pipeline."""
    logger.info("Generating news and research documents...")
    
    # Step 1: Generate dynamic prompts for news articles
    prompts = _create_news_article_prompts()
    
    # Step 2: Store prompts in Snowflake table
    if prompts:
        prompts_df = session.create_dataframe(prompts)
        prompts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.NEWS_ARTICLE_PROMPTS", mode="overwrite")
        
        # Step 3-5: Generate content using Cortex Complete and save final documents
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.NEWS_AND_RESEARCH AS
            SELECT 
                PROMPT_ID AS ID,
                DOCUMENT_TITLE AS TITLE,
                SNOWFLAKE.CORTEX.COMPLETE('{config.LLM_MODEL}', PROMPT_TEXT) AS CONTENT,
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
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.NEWS_ARTICLE_PROMPTS
            WHERE PROMPT_TEXT IS NOT NULL
        """).collect()
        
        # Validate generated content
        result = session.sql(f"SELECT COUNT(*) as cnt FROM {config.SNOWFLAKE['database']}.RAW_DATA.NEWS_AND_RESEARCH WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
        doc_count = result[0]['CNT']
        logger.info(f"Generated {doc_count} news and research documents using Cortex Complete")
    else:
        logger.warning("No prompts generated for news and research documents")


def generate_document_templates(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate document templates for agent framework using Cortex Complete pipeline."""
    logger.info("Generating document templates...")
    
    # Step 1: Create template prompts for different template types
    prompts = []
    
    # Generate RFI templates
    prompts.extend(_create_rfi_template_prompts())
    
    # Generate SAR templates
    prompts.extend(_create_sar_template_prompts())
    
    # Generate credit memo templates
    prompts.extend(_create_credit_memo_template_prompts())
    
    # Generate compliance report templates
    prompts.extend(_create_compliance_report_template_prompts())
    
    # Step 2: Store prompts in Snowflake table
    if prompts:
        prompts_df = session.create_dataframe(prompts)
        prompts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.DOCUMENT_TEMPLATE_PROMPTS", mode="overwrite")
        
        # Step 3-5: Generate content using Cortex Complete and save final templates
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.DOCUMENT_TEMPLATES AS
            SELECT 
                PROMPT_ID AS TEMPLATE_ID,
                TEMPLATE_NAME,
                SNOWFLAKE.CORTEX.COMPLETE('{config.LLM_MODEL}', PROMPT_TEXT) AS TEMPLATE_CONTENT,
                TEMPLATE_TYPE,
                SCENARIO,
                USE_CASE,
                REGULATORY_FRAMEWORK,
                REQUIRED_VARIABLES,
                LANGUAGE,
                CREATED_DATE
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.DOCUMENT_TEMPLATE_PROMPTS
            WHERE PROMPT_TEXT IS NOT NULL
        """).collect()
        
        # Validate generated content
        result = session.sql(f"SELECT COUNT(*) as cnt FROM {config.SNOWFLAKE['database']}.RAW_DATA.DOCUMENT_TEMPLATES WHERE TEMPLATE_CONTENT IS NOT NULL AND LENGTH(TEMPLATE_CONTENT) > 100").collect()
        template_count = result[0]['CNT']
        logger.info(f"Generated {template_count} document templates using Cortex Complete")
    else:
        logger.warning("No prompts generated for document templates")


# =============================================================================
# PROMPT GENERATION FUNCTIONS
# =============================================================================

def _create_onboarding_prompts(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create onboarding document prompts for an entity."""
    prompts = []
    
    if entity['ENTITY_ID'] == 'GTV_SA_001':
        # Special case for Global Trade Ventures with PEP connections
        prompt_text = f"""Create a comprehensive corporate onboarding document for {entity['ENTITY_NAME']}, a Luxembourg-incorporated international trade company.

REQUIREMENTS:
- Document type: Corporate Onboarding Documentation
- Word count: 800-1500 words
- Language: Professional {config.LANGUAGE} banking terminology
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
            'LANGUAGE': f'{config.LANGUAGE}',
            'CONFIDENCE_SCORE': 0.95,
            'CREATED_DATE': datetime.now()
        })
    
    return prompts


def _create_adverse_media_prompts(entity: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create adverse media prompts for an entity."""
    prompts = []
    
    if entity['ENTITY_ID'] == 'GTV_SA_001':
        # Adverse media for Elena Rossi (UBO of Global Trade Ventures)
        prompt_text = f"""Create a Reuters news article about Italian political corruption investigation affecting Elena Rossi, who is a UBO of {entity['ENTITY_NAME']}.

REQUIREMENTS:
- Document type: Adverse Media / News Article
- Word count: 400-800 words
- Language: Professional journalism {config.LANGUAGE}
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
            'LANGUAGE': f'{config.LANGUAGE}',
            'CONFIDENCE_SCORE': 0.88,
            'CREATED_DATE': datetime.now()
        })
    
    return prompts


def _create_policy_document_prompts() -> List[Dict[str, Any]]:
    """Create credit policy document prompts."""
    prompts = []
    
    # Policy document with ratio thresholds
    ratio_prompt = """Create a comprehensive Mid-Market Lending Policy document focusing on financial ratio thresholds.

REQUIREMENTS:
- Document type: Credit Policy - Ratio Thresholds
- Word count: 1000-2000 words
- Language: Professional {config.LANGUAGE} banking terminology
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
        'LANGUAGE': f'{config.LANGUAGE}',
        'CREATED_DATE': datetime.now()
    })
    
    # Concentration limits policy
    concentration_prompt = """Create a Commercial Credit Risk Policy document focusing on client concentration limits.

REQUIREMENTS:
- Document type: Credit Risk Policy - Concentration Limits
- Word count: 1000-2000 words
- Language: Professional {config.LANGUAGE} banking terminology
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
        'LANGUAGE': f'{config.LANGUAGE}',
        'CREATED_DATE': datetime.now()
    })
    
    return prompts


def _create_business_plan_prompts(application: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Create business plan document prompts for a loan application."""
    prompts = []
    
    if application['APPLICANT_NAME'] == config.KEY_ENTITIES['primary_aml_subject']['entity_id']:  # GTV_SA_001
        prompt_text = f"""Create a comprehensive business plan for {config.KEY_ENTITIES['primary_aml_subject']['name']}, a Luxembourg international trade company applying for a €{application['REQUESTED_AMOUNT']/1000000:.1f}M loan.

REQUIREMENTS:
- Document type: Business Plan 2024-2029
- Word count: 2000-4000 words
- Language: Professional {config.LANGUAGE} business terminology
- Application context: {application['LOAN_PURPOSE']}

SPECIFIC CONTENT REQUIREMENTS:
Company Overview:
- Legal Name: {application['APPLICANT_NAME']}
- Industry: {application['INDUSTRY_SECTOR']}
- Annual Revenue: €{application['ANNUAL_REVENUE']/1000000:.1f}M
- Total Assets: €{application['TOTAL_ASSETS']/1000000:.1f}M
- EBITDA: €{application['EBITDA']/1000000:.1f}M

EXECUTIVE SUMMARY:
{config.KEY_ENTITIES['primary_aml_subject']['name']} is a leading {config.KEY_ENTITIES['primary_aml_subject']['industry']} company specializing in cross-border trade facilitation and logistics solutions across Europe, Asia, and emerging markets.

MARKET STRATEGY:
- Target market: Mid-market importers/exporters (€5M-€50M annual trade volume)
- Geographic expansion: Eastern European and Asian market penetration
- Service diversification: Digital trade finance and customs automation
- Key differentiator: Comprehensive supply chain solutions with regulatory expertise

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
            'PROMPT_ID': f'GTV_SA_BUSINESS_PLAN_2024',
            'DOCUMENT_TITLE': f'{config.KEY_ENTITIES["primary_aml_subject"]["name"]} - Business Plan 2024-2029',
            'PROMPT_TEXT': prompt_text,
            'APPLICANT_NAME': application['APPLICANT_NAME'],
            'DOC_TYPE': 'Business Plan',
            'UPLOAD_DATE': application['APPLICATION_DATE'],
            'DOCUMENT_SECTION': 'Market Strategy',
            'PROCESSING_STATUS': 'PROCESSED',
            'LANGUAGE': f'{config.LANGUAGE}',
            'CREATED_DATE': datetime.now()
        })
    
    return prompts


def _create_news_article_prompts() -> List[Dict[str, Any]]:
    """Create news article prompts based on market themes."""
    prompts = []
    
    # Supply chain disruption article about Northern Supply Chain Ltd
    supply_chain_prompt = """Create a Reuters news article about European supply chain disruptions affecting technology companies.

REQUIREMENTS:
- Document type: News Article
- Word count: 300-600 words
- Language: Professional journalism {config.LANGUAGE}
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
        'LANGUAGE': f'{config.LANGUAGE}',
        'CREATED_DATE': datetime.now()
    })
    
    return prompts


def _create_rfi_template_prompts() -> List[Dict[str, Any]]:
    """Create RFI (Request for Information) template prompts."""
    prompts = []
    
    # RFI for PEP investigations
    prompts.append({
        'PROMPT_ID': 'RFI_PEP_001',
        'TEMPLATE_NAME': 'PEP Investigation Request for Information',
        'PROMPT_TEXT': f"""Create a professional Request for Information template for PEP (Politically Exposed Person) investigations.

REQUIREMENTS:
- Professional {config.LANGUAGE} banking tone following {config.REGULATORY_FRAMEWORK} guidelines
- Institution: {config.INSTITUTION_NAME}
- Template for requesting additional documentation regarding PEP status
- Include placeholders for: {{CLIENT_NAME}}, {{ENTITY_NAME}}, {{PEP_PERSON_NAME}}, {{RELATIONSHIP_TYPE}}, {{ALLEGATIONS_SUMMARY}}
- Request source of funds clarification
- Specify documentation required (bank statements, declarations, etc.)
- Include compliance deadlines
- Professional closing with contact information

The template should be ready for customization with case-specific details.""",
        'TEMPLATE_TYPE': 'RFI',
        'SCENARIO': 'AML',
        'USE_CASE': 'PEP Investigation',
        'REGULATORY_FRAMEWORK': config.REGULATORY_FRAMEWORK,
        'REQUIRED_VARIABLES': 'CLIENT_NAME,ENTITY_NAME,PEP_PERSON_NAME,RELATIONSHIP_TYPE,ALLEGATIONS_SUMMARY',
        'LANGUAGE': config.LANGUAGE,
        'CREATED_DATE': datetime.now()
    })
    
    # RFI for source of funds
    prompts.append({
        'PROMPT_ID': 'RFI_SOF_001',
        'TEMPLATE_NAME': 'Source of Funds Request for Information',
        'PROMPT_TEXT': f"""Create a professional Request for Information template for source of funds investigations.

REQUIREMENTS:
- Professional {config.LANGUAGE} banking tone following {config.REGULATORY_FRAMEWORK} guidelines
- Institution: {config.INSTITUTION_NAME}
- Template for requesting source of funds documentation
- Include placeholders for: {{CLIENT_NAME}}, {{ENTITY_NAME}}, {{AMOUNT}}, {{TRANSACTION_DATE}}, {{TRANSACTION_DETAILS}}
- Request specific documentation (contracts, invoices, etc.)
- Include compliance deadlines
- Professional closing

The template should be ready for customization with transaction-specific details.""",
        'TEMPLATE_TYPE': 'RFI',
        'SCENARIO': 'AML',
        'USE_CASE': 'Source of Funds',
        'REGULATORY_FRAMEWORK': config.REGULATORY_FRAMEWORK,
        'REQUIRED_VARIABLES': 'CLIENT_NAME,ENTITY_NAME,AMOUNT,TRANSACTION_DATE,TRANSACTION_DETAILS',
        'LANGUAGE': config.LANGUAGE,
        'CREATED_DATE': datetime.now()
    })
    
    return prompts


def _create_sar_template_prompts() -> List[Dict[str, Any]]:
    """Create SAR (Suspicious Activity Report) template prompts."""
    prompts = []
    
    prompts.append({
        'PROMPT_ID': 'SAR_001',
        'TEMPLATE_NAME': 'Suspicious Activity Report Template',
        'PROMPT_TEXT': f"""Create a professional Suspicious Activity Report template.

REQUIREMENTS:
- Professional {config.LANGUAGE} compliance tone following {config.REGULATORY_FRAMEWORK} guidelines
- Institution: {config.INSTITUTION_NAME}
- Template for reporting suspicious activities to authorities
- Include placeholders for: {{CLIENT_NAME}}, {{ENTITY_NAME}}, {{SUSPICIOUS_ACTIVITY}}, {{TIMEFRAME}}, {{AMOUNTS}}, {{INVESTIGATION_SUMMARY}}
- Include all required regulatory sections
- Professional format suitable for submission to financial intelligence unit

The template should be ready for customization with case-specific investigation details.""",
        'TEMPLATE_TYPE': 'SAR',
        'SCENARIO': 'AML',
        'USE_CASE': 'Suspicious Activity Reporting',
        'REGULATORY_FRAMEWORK': config.REGULATORY_FRAMEWORK,
        'REQUIRED_VARIABLES': 'CLIENT_NAME,ENTITY_NAME,SUSPICIOUS_ACTIVITY,TIMEFRAME,AMOUNTS,INVESTIGATION_SUMMARY',
        'LANGUAGE': config.LANGUAGE,
        'CREATED_DATE': datetime.now()
    })
    
    return prompts


def _create_credit_memo_template_prompts() -> List[Dict[str, Any]]:
    """Create credit memo template prompts."""
    prompts = []
    
    # Credit approval memo
    prompts.append({
        'PROMPT_ID': 'CREDIT_MEMO_APPROVAL_001',
        'TEMPLATE_NAME': 'Credit Approval Memorandum',
        'PROMPT_TEXT': f"""Create a professional credit approval memorandum template.

REQUIREMENTS:
- Professional {config.LANGUAGE} banking tone following {config.REGULATORY_FRAMEWORK} guidelines
- Institution: {config.INSTITUTION_NAME}
- Template for credit approval recommendations
- Include placeholders for: {{APPLICANT_NAME}}, {{REQUESTED_AMOUNT}}, {{CURRENCY}}, {{FINANCIAL_SUMMARY}}, {{RISK_ASSESSMENT}}, {{RECOMMENDATION}}
- Include financial ratio analysis section
- Include risk mitigation measures
- Professional format for credit committee

The template should be ready for customization with application-specific details.""",
        'TEMPLATE_TYPE': 'Credit Memo',
        'SCENARIO': 'CREDIT',
        'USE_CASE': 'Credit Approval',
        'REGULATORY_FRAMEWORK': config.REGULATORY_FRAMEWORK,
        'REQUIRED_VARIABLES': 'APPLICANT_NAME,REQUESTED_AMOUNT,CURRENCY,FINANCIAL_SUMMARY,RISK_ASSESSMENT,RECOMMENDATION',
        'LANGUAGE': config.LANGUAGE,
        'CREATED_DATE': datetime.now()
    })
    
    # Credit decline letter
    prompts.append({
        'PROMPT_ID': 'CREDIT_DECLINE_001',
        'TEMPLATE_NAME': 'Credit Application Decline Letter',
        'PROMPT_TEXT': f"""Create a professional credit application decline letter template.

REQUIREMENTS:
- Professional {config.LANGUAGE} banking tone following {config.REGULATORY_FRAMEWORK} guidelines
- Institution: {config.INSTITUTION_NAME}
- Template for declining credit applications
- Include placeholders for: {{APPLICANT_NAME}}, {{APPLICATION_DATE}}, {{DECLINE_REASONS}}, {{NEXT_STEPS}}
- Professional but empathetic tone
- Include information about appeal process
- Professional closing

The template should be ready for customization with application-specific details.""",
        'TEMPLATE_TYPE': 'Decline Letter',
        'SCENARIO': 'CREDIT',
        'USE_CASE': 'Credit Decline',
        'REGULATORY_FRAMEWORK': config.REGULATORY_FRAMEWORK,
        'REQUIRED_VARIABLES': 'APPLICANT_NAME,APPLICATION_DATE,DECLINE_REASONS,NEXT_STEPS',
        'LANGUAGE': config.LANGUAGE,
        'CREATED_DATE': datetime.now()
    })
    
    return prompts


def _create_compliance_report_template_prompts() -> List[Dict[str, Any]]:
    """Create compliance report template prompts."""
    prompts = []
    
    prompts.append({
        'PROMPT_ID': 'COMPLIANCE_REPORT_001',
        'TEMPLATE_NAME': 'Enhanced Due Diligence Report',
        'PROMPT_TEXT': f"""Create a professional Enhanced Due Diligence report template.

REQUIREMENTS:
- Professional {config.LANGUAGE} compliance tone following {config.REGULATORY_FRAMEWORK} guidelines
- Institution: {config.INSTITUTION_NAME}
- Template for EDD investigation reports
- Include placeholders for: {{CLIENT_NAME}}, {{ENTITY_NAME}}, {{INVESTIGATION_PERIOD}}, {{FINDINGS_SUMMARY}}, {{RISK_RATING}}, {{RECOMMENDATIONS}}
- Include sections for: Entity background, UBO analysis, Adverse media findings, Risk assessment, Recommendations
- Professional format suitable for risk committee presentation

The template should be ready for customization with investigation-specific findings.""",
        'TEMPLATE_TYPE': 'Compliance Report',
        'SCENARIO': 'AML',
        'USE_CASE': 'EDD Report',
        'REGULATORY_FRAMEWORK': config.REGULATORY_FRAMEWORK,
        'REQUIRED_VARIABLES': 'CLIENT_NAME,ENTITY_NAME,INVESTIGATION_PERIOD,FINDINGS_SUMMARY,RISK_RATING,RECOMMENDATIONS',
        'LANGUAGE': config.LANGUAGE,
        'CREATED_DATE': datetime.now()
    })
    
    return prompts


# =============================================================================
# PHASE 2 UNSTRUCTURED DATA GENERATION FUNCTIONS
# =============================================================================

def generate_client_documents(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate client documents (call notes, emails, news) for relationship manager scenario."""
    logger.info("Generating client documents...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('client_documents', 0)
    
    if target_count == 0:
        logger.info("Skipping client documents generation (not in scale config)")
        return
    
    # Get CRM records and opportunities for context
    try:
        crm_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_CRM")
        crm_records = crm_df.collect()
        
        opportunities_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_OPPORTUNITIES")
        opportunities = opportunities_df.collect()
    except:
        logger.warning("No CRM data found, skipping client documents generation")
        return
    
    # Get entity names for realistic references
    try:
        entities_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.ENTITIES")
        entities = entities_df.select("ENTITY_ID", "ENTITY_NAME", "INDUSTRY_SECTOR").collect()
        entity_map = {e['ENTITY_ID']: {'name': e['ENTITY_NAME'], 'industry': e['INDUSTRY_SECTOR']} for e in entities}
    except:
        entity_map = {}
    
    # Generate prompts for different document types
    prompts = []
    doc_types = config.PHASE_2_DOCUMENT_TYPES['client_documents']
    
    # Distribute documents across types based on weights
    for doc_type_info in doc_types:
        doc_type = doc_type_info['type']
        weight = doc_type_info['weight']
        type_count = int(target_count * weight)
        
        for i in range(type_count):
            crm_record = crm_records[i % len(crm_records)]
            customer_id = crm_record['CUSTOMER_ID']
            entity_info = entity_map.get(customer_id, {'name': f'Customer {customer_id}', 'industry': 'Various'})
            
            # Find related opportunities for this customer
            customer_opps = [o for o in opportunities if o['CUSTOMER_ID'] == customer_id]
            
            if doc_type == 'call_note':
                prompt_data = _create_call_note_prompt(customer_id, entity_info, crm_record, customer_opps)
            elif doc_type == 'internal_email':
                prompt_data = _create_internal_email_prompt(customer_id, entity_info, crm_record, customer_opps)
            elif doc_type == 'client_news':
                prompt_data = _create_client_news_prompt(customer_id, entity_info)
            else:
                continue
            
            prompts.append(prompt_data)
    
    # Store prompts and generate content
    if prompts:
        prompts_df = session.create_dataframe(prompts)
        prompts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_DOCUMENT_PROMPTS", mode="overwrite")
        
        # Generate content using Cortex Complete
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_DOCUMENTS AS
            SELECT 
                PROMPT_ID AS ID,
                DOCUMENT_TITLE AS TITLE,
                SNOWFLAKE.CORTEX.COMPLETE('{config.LLM_MODEL}', PROMPT_TEXT) AS CONTENT,
                CUSTOMER_ID AS CLIENT_NAME,
                SOURCE_TYPE,
                PUBLISH_DATE,
                CREATED_DATE
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_DOCUMENT_PROMPTS
            WHERE PROMPT_TEXT IS NOT NULL
        """).collect()
        
        # Validate
        result = session.sql(f"SELECT COUNT(*) as cnt FROM {config.SNOWFLAKE['database']}.RAW_DATA.CLIENT_DOCUMENTS WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
        doc_count = result[0]['CNT']
        logger.info(f"Generated {doc_count} client documents using Cortex Complete")
    else:
        logger.warning("No prompts generated for client documents")


def generate_wealth_meeting_notes(session: Session, scale: str = "demo", scenarios: List[str] = None) -> None:
    """Generate wealth advisor meeting notes."""
    logger.info("Generating wealth meeting notes...")
    
    scale_config = config.get_scale_config(scale)
    target_count = scale_config.get('wealth_meeting_notes', 0)
    
    if target_count == 0:
        logger.info("Skipping wealth meeting notes generation (not in scale config)")
        return
    
    # Get wealth client profiles for context
    try:
        profiles_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_CLIENT_PROFILES")
        profiles = profiles_df.collect()
        
        # Get model portfolio info
        portfolios_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.MODEL_PORTFOLIOS")
        portfolios = portfolios_df.collect()
        portfolio_map = {p['MODEL_ID']: p for p in portfolios}
        
        # Get holdings for context
        holdings_df = session.table(f"{config.SNOWFLAKE['database']}.RAW_DATA.HOLDINGS")
        all_holdings = holdings_df.collect()
    except:
        logger.warning("No wealth data found, skipping meeting notes generation")
        return
    
    # Generate prompts for meeting notes
    prompts = []
    note_types = config.PHASE_2_DOCUMENT_TYPES['wealth_meeting_notes']
    
    for note_type_info in note_types:
        note_type = note_type_info['type']
        weight = note_type_info['weight']
        type_count = int(target_count * weight)
        
        for i in range(type_count):
            profile = profiles[i % len(profiles)]
            customer_id = profile['CUSTOMER_ID']
            
            # Get customer holdings
            customer_holdings = [h for h in all_holdings if h['CUSTOMER_ID'] == customer_id]
            
            # Get model portfolio info
            model_portfolio = portfolio_map.get(profile['MODEL_PORTFOLIO_ID'], {})
            
            if note_type == 'portfolio_review':
                prompt_data = _create_portfolio_review_prompt(profile, model_portfolio, customer_holdings)
            elif note_type == 'investment_strategy':
                prompt_data = _create_investment_strategy_prompt(profile, model_portfolio)
            elif note_type == 'rebalancing_decision':
                prompt_data = _create_rebalancing_decision_prompt(profile, model_portfolio, customer_holdings)
            else:
                continue
            
            prompts.append(prompt_data)
    
    # Store prompts and generate content
    if prompts:
        prompts_df = session.create_dataframe(prompts)
        prompts_df.write.save_as_table(f"{config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_MEETING_NOTE_PROMPTS", mode="overwrite")
        
        # Generate content using Cortex Complete
        session.sql(f"""
            CREATE OR REPLACE TABLE {config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_MEETING_NOTES AS
            SELECT 
                PROMPT_ID AS ID,
                DOCUMENT_TITLE AS TITLE,
                SNOWFLAKE.CORTEX.COMPLETE('{config.LLM_MODEL}', PROMPT_TEXT) AS CONTENT,
                CUSTOMER_ID AS CLIENT_NAME,
                ADVISOR_NAME,
                MEETING_DATE,
                CREATED_DATE
            FROM {config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_MEETING_NOTE_PROMPTS
            WHERE PROMPT_TEXT IS NOT NULL
        """).collect()
        
        # Validate
        result = session.sql(f"SELECT COUNT(*) as cnt FROM {config.SNOWFLAKE['database']}.RAW_DATA.WEALTH_MEETING_NOTES WHERE CONTENT IS NOT NULL AND LENGTH(CONTENT) > 100").collect()
        doc_count = result[0]['CNT']
        logger.info(f"Generated {doc_count} wealth meeting notes using Cortex Complete")
    else:
        logger.warning("No prompts generated for wealth meeting notes")


# =============================================================================
# PHASE 2 PROMPT GENERATION HELPER FUNCTIONS
# =============================================================================

def _create_call_note_prompt(customer_id: str, entity_info: Dict, crm_record: Dict, opportunities: List[Dict]) -> Dict[str, Any]:
    """Create prompt for relationship manager call note."""
    entity_name = entity_info['name']
    industry = entity_info['industry']
    rm_name = crm_record['RELATIONSHIP_MANAGER']
    
    # Select opportunity to discuss if available
    opp_context = ""
    if opportunities:
        opp = opportunities[0]
        opp_context = f"Discussed opportunity: {opp['OPPORTUNITY_DESCRIPTION']} (potential value: €{opp['POTENTIAL_VALUE']:,.0f})"
    
    prompt = f"""Write a professional relationship manager call note for {entity_name}, a {industry} client.

Context:
- Relationship Manager: {rm_name}
- Account Status: {crm_record['ACCOUNT_STATUS']}
- Account Tier: {crm_record['ACCOUNT_TIER']}
{opp_context}

Generate a 200-300 word call note covering:
1. Purpose of the call and key discussion topics
2. Client's current business situation and any concerns raised
3. Opportunities or risks identified during the conversation
4. Action items and next steps
5. Overall client sentiment

Use professional banking language with European tone. Include specific details that would be useful for future client interactions."""
    
    return {
        'PROMPT_ID': f"CLN_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'DOCUMENT_TITLE': f"Call Note: {entity_name} - {rm_name}",
        'PROMPT_TEXT': prompt,
        'CUSTOMER_ID': customer_id,
        'SOURCE_TYPE': 'call_note',
        'PUBLISH_DATE': date.today() - timedelta(days=random.randint(1, 60)),
        'CREATED_DATE': datetime.now()
    }


def _create_internal_email_prompt(customer_id: str, entity_info: Dict, crm_record: Dict, opportunities: List[Dict]) -> Dict[str, Any]:
    """Create prompt for internal email about client strategy."""
    entity_name = entity_info['name']
    industry = entity_info['industry']
    rm_name = crm_record['RELATIONSHIP_MANAGER']
    
    # Determine email focus
    if crm_record['ACCOUNT_TIER'] == 'PREMIUM':
        focus = "strategic expansion opportunities and revenue growth"
    elif crm_record['ACCOUNT_STATUS'] == 'PROSPECT':
        focus = "onboarding strategy and initial product suite"
    else:
        focus = "risk mitigation and relationship deepening"
    
    prompt = f"""Write an internal email from {rm_name} to the Commercial Banking team regarding {entity_name}, a {industry} client.

Context:
- Account Tier: {crm_record['ACCOUNT_TIER']}
- Account Status: {crm_record['ACCOUNT_STATUS']}
- Email Focus: {focus}

Generate a 200-250 word professional email with:
1. Subject line
2. Brief situation summary
3. Strategic recommendation with specific products/services
4. Risk considerations or potential challenges
5. Request for team input or approval

Use internal banking communication style. Include actionable recommendations."""
    
    return {
        'PROMPT_ID': f"EML_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'DOCUMENT_TITLE': f"Internal Email: {entity_name} Strategy",
        'PROMPT_TEXT': prompt,
        'CUSTOMER_ID': customer_id,
        'SOURCE_TYPE': 'internal_email',
        'PUBLISH_DATE': date.today() - timedelta(days=random.randint(1, 45)),
        'CREATED_DATE': datetime.now()
    }


def _create_client_news_prompt(customer_id: str, entity_info: Dict) -> Dict[str, Any]:
    """Create prompt for news article about client company."""
    entity_name = entity_info['name']
    industry = entity_info['industry']
    
    # Select news topic based on industry
    topics = {
        'Automotive Manufacturing': 'announces new electric vehicle production facility',
        'Software Services': 'secures major enterprise software contract',
        'Logistics & Transportation': 'expands European distribution network',
        'Renewable Energy': 'wins government contract for solar energy project',
        'International Trade': 'expands into Asian markets',
        'Private Investment': 'announces new fund focused on sustainable infrastructure'
    }
    
    topic = topics.get(industry, 'announces strategic business expansion')
    
    prompt = f"""Write a neutral business news article about {entity_name}, a {industry} company.

Headline: "{entity_name} {topic}"

Generate a 250-300 word news article with:
1. Lead paragraph summarizing the key announcement
2. Financial or operational details of the initiative
3. Quote from company leadership
4. Market context and industry implications
5. Future outlook

Use neutral journalism style appropriate for European financial press. Include specific numbers and timelines."""
    
    return {
        'PROMPT_ID': f"NWS_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'DOCUMENT_TITLE': f"News: {entity_name} {topic[:50]}...",
        'PROMPT_TEXT': prompt,
        'CUSTOMER_ID': customer_id,
        'SOURCE_TYPE': 'client_news',
        'PUBLISH_DATE': date.today() - timedelta(days=random.randint(1, 90)),
        'CREATED_DATE': datetime.now()
    }


def _create_portfolio_review_prompt(profile: Dict, model_portfolio: Dict, holdings: List[Dict]) -> Dict[str, Any]:
    """Create prompt for quarterly portfolio review meeting note."""
    customer_id = profile['CUSTOMER_ID']
    advisor = profile['WEALTH_ADVISOR']
    total_aum = profile['TOTAL_AUM']
    risk_tolerance = profile['RISK_TOLERANCE']
    
    # Calculate current allocation
    equity_holdings = [h for h in holdings if h['ASSET_TYPE'] == 'EQUITY']
    bond_holdings = [h for h in holdings if h['ASSET_TYPE'] == 'BOND']
    
    equity_value = sum(h['CURRENT_VALUE'] for h in equity_holdings) if equity_holdings else 0
    bond_value = sum(h['CURRENT_VALUE'] for h in bond_holdings) if bond_holdings else 0
    total_value = sum(h['CURRENT_VALUE'] for h in holdings) if holdings else total_aum
    
    equity_pct = (equity_value / total_value * 100) if total_value > 0 else 0
    bond_pct = (bond_value / total_value * 100) if total_value > 0 else 0
    
    target_equity = model_portfolio.get('TARGET_EQUITY_PCT', 50)
    target_bond = model_portfolio.get('TARGET_BOND_PCT', 40)
    
    prompt = f"""Write a quarterly portfolio review meeting note for a wealth management client.

Meeting Details:
- Wealth Advisor: {advisor}
- Client Risk Tolerance: {risk_tolerance}
- Total AUM: €{total_aum:,.0f}

Portfolio Performance:
- Current Equity Allocation: {equity_pct:.1f}% (Target: {target_equity:.1f}%)
- Current Bond Allocation: {bond_pct:.1f}% (Target: {target_bond:.1f}%)
- Model Portfolio: {model_portfolio.get('MODEL_NAME', 'Balanced')}

Generate a 300-350 word meeting note with:
1. Portfolio performance summary vs. benchmarks
2. Current allocation vs. target allocation analysis
3. Market environment discussion and outlook
4. Client questions or concerns addressed
5. Recommendations and agreed action items

Use professional wealth advisory tone. Include specific performance figures and actionable recommendations."""
    
    return {
        'PROMPT_ID': f"PFR_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'DOCUMENT_TITLE': f"Quarterly Portfolio Review - {customer_id}",
        'PROMPT_TEXT': prompt,
        'CUSTOMER_ID': customer_id,
        'ADVISOR_NAME': advisor,
        'MEETING_DATE': date.today() - timedelta(days=random.randint(1, 90)),
        'CREATED_DATE': datetime.now()
    }


def _create_investment_strategy_prompt(profile: Dict, model_portfolio: Dict) -> Dict[str, Any]:
    """Create prompt for investment strategy discussion note."""
    customer_id = profile['CUSTOMER_ID']
    advisor = profile['WEALTH_ADVISOR']
    investment_objectives = profile['INVESTMENT_OBJECTIVES']
    risk_tolerance = profile['RISK_TOLERANCE']
    
    prompt = f"""Write an investment strategy discussion meeting note for a wealth management client.

Client Profile:
- Wealth Advisor: {advisor}
- Investment Objectives: {investment_objectives}
- Risk Tolerance: {risk_tolerance}
- Current Model: {model_portfolio.get('MODEL_NAME', 'Balanced Portfolio')}
- Expected Return: {model_portfolio.get('EXPECTED_ANNUAL_RETURN_PCT', 6.5):.1f}%

Generate a 250-300 word meeting note with:
1. Discussion of client's long-term financial goals
2. Review of investment time horizon and liquidity needs
3. Tax optimization strategies discussed
4. Asset allocation philosophy and diversification approach
5. Agreement on investment guidelines and rebalancing triggers

Use consultative wealth advisory language. Focus on strategic planning and long-term objectives."""
    
    return {
        'PROMPT_ID': f"INV_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'DOCUMENT_TITLE': f"Investment Strategy Discussion - {customer_id}",
        'PROMPT_TEXT': prompt,
        'CUSTOMER_ID': customer_id,
        'ADVISOR_NAME': advisor,
        'MEETING_DATE': date.today() - timedelta(days=random.randint(30, 180)),
        'CREATED_DATE': datetime.now()
    }


def _create_rebalancing_decision_prompt(profile: Dict, model_portfolio: Dict, holdings: List[Dict]) -> Dict[str, Any]:
    """Create prompt for portfolio rebalancing decision note."""
    customer_id = profile['CUSTOMER_ID']
    advisor = profile['WEALTH_ADVISOR']
    
    # Calculate drift from target
    total_value = sum(h['CURRENT_VALUE'] for h in holdings) if holdings else profile['TOTAL_AUM']
    
    equity_value = sum(h['CURRENT_VALUE'] for h in holdings if h['ASSET_TYPE'] == 'EQUITY')
    current_equity_pct = (equity_value / total_value * 100) if total_value > 0 else 0
    target_equity_pct = model_portfolio.get('TARGET_EQUITY_PCT', 50)
    equity_drift = current_equity_pct - target_equity_pct
    
    prompt = f"""Write a portfolio rebalancing decision meeting note for a wealth management client.

Rebalancing Context:
- Wealth Advisor: {advisor}
- Total Portfolio Value: €{total_value:,.0f}
- Model Portfolio: {model_portfolio.get('MODEL_NAME', 'Balanced')}
- Current Equity: {current_equity_pct:.1f}% (Target: {target_equity_pct:.1f}%)
- Drift: {equity_drift:+.1f}%
- Rebalancing Trigger: {profile.get('REBALANCE_TRIGGER_PCT', 10.0):.0f}%

Generate a 250-300 word rebalancing decision note with:
1. Trigger for rebalancing (threshold exceeded or calendar-based)
2. Specific trades recommended to restore target allocation
3. Tax considerations and wash sale rules
4. Expected transaction costs
5. Client approval and execution timeline

Use decisive, action-oriented wealth advisory language. Include specific trade recommendations."""
    
    return {
        'PROMPT_ID': f"REB_{customer_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        'DOCUMENT_TITLE': f"Rebalancing Decision - {customer_id}",
        'PROMPT_TEXT': prompt,
        'CUSTOMER_ID': customer_id,
        'ADVISOR_NAME': advisor,
        'MEETING_DATE': date.today() - timedelta(days=random.randint(1, 60)),
        'CREATED_DATE': datetime.now()
    }


def main():
    """Main function for testing unstructured data generation."""
    print("Unstructured data generator module loaded successfully")
    print("Use generate_all_unstructured_data() method to create unstructured demo data")


if __name__ == "__main__":
    main()
