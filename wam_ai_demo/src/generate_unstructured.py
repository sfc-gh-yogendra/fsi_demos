"""
WAM AI Demo - Unstructured Data Generation
Generates realistic unstructured data using Snowflake Cortex Complete
"""

from snowflake.snowpark import Session
from snowflake.snowpark.functions import col, lit
from snowflake.cortex import Complete
import config
import random
from datetime import datetime, timedelta

def generate_unstructured_data(session: Session, test_mode: bool = False):
    """Generate all unstructured data using Cortex Complete"""
    
    print("  → Generating unstructured data...")
    
    # Generate communications corpus
    generate_communications_corpus(session, test_mode)
    
    # Generate research corpus
    generate_research_corpus(session, test_mode)
    
    # Generate regulatory corpus
    generate_regulatory_corpus(session, test_mode)
    
    # Generate planning corpus
    generate_planning_corpus(session, test_mode)
    
    # Generate departure corpus for benchmarking
    generate_departure_corpus(session, test_mode)
    
    # Create client interactions view
    create_client_interactions_view(session)
    
    print("  ✅ Unstructured data generation complete")


def generate_communications_corpus(session: Session, test_mode: bool = False):
    """Generate communications using the 5-step Cortex Complete pipeline"""
    print("    → Generating communications corpus...")
    
    # Step 1: Generate dynamic prompts
    prompts_data = create_communications_prompts(session, test_mode)
    
    # Step 2: Store prompts in Snowflake table
    prompts_df = session.create_dataframe(prompts_data)
    prompts_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_COMMUNICATIONS_PROMPTS", )
    
    # Step 3: Create Snowpark DataFrame on prompt table
    prompts_table_df = session.table(f"{config.DATABASE_NAME}.RAW.TEMP_COMMUNICATIONS_PROMPTS")
    
    # Step 4: Use with_column to generate content using complete()
    generated_df = prompts_table_df.with_column(
        'GENERATED_CONTENT',
        Complete(
            lit(config.MODEL_BY_CORPUS['communications']),
            col('PROMPT_TEXT')
        )
    )
    
    # Step 5: Save to final table with post-processing and risk detection
    final_communications = generated_df.select(
        col('COMMUNICATION_ID'),
        col('CLIENT_ID'),
        col('ADVISOR_ID'),
        col('TIMESTAMP'),
        col('CHANNEL'),
        col('SUBJECT'),
        col('GENERATED_CONTENT').alias('CONTENT'),
        col('SENTIMENT_SCORE'),
        lit(None).cast('string').alias('RISKCATEGORY'),
        lit(None).cast('string').alias('RISKSEVERITY'),
        lit(0).alias('RISKFLAGS')
    )
    
    final_communications.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS", )
    
    # Add risk flags using post-processing
    add_risk_flags_to_communications(session)
    
    # Clean up temp table
    session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_COMMUNICATIONS_PROMPTS").collect()
    
    print(f"    ✅ Generated communications corpus with risk flags")

def create_communications_prompts(session: Session, test_mode: bool = False) -> list:
    """Create dynamic prompts for communications generation"""
    
    # Get clients and their holdings for context
    clients_query = f"""
        SELECT 
            c.ClientID,
            c.AdvisorID,
            c.FirstName,
            c.LastName,
            c.RiskTolerance,
            a.FirstName as AdvisorFirstName,
            a.LastName as AdvisorLastName
        FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT c
        JOIN {config.DATABASE_NAME}.CURATED.DIM_ADVISOR a ON c.AdvisorID = a.AdvisorID
        WHERE c.IsActive = TRUE
    """
    
    clients = session.sql(clients_query).collect()
    
    # Get securities for reference
    securities = session.table(f"{config.DATABASE_NAME}.CURATED.DIM_SECURITY").collect()
    tickers = [s['PRIMARYTICKER'] for s in securities if s['PRIMARYTICKER']]
    
    prompts_data = []
    comm_id = 1
    
    # Determine volume based on test mode
    volume_per_client = 10 if test_mode else config.COMMS_PER_CLIENT
    
    for client in clients:
        client_id = client['CLIENTID']
        advisor_id = client['ADVISORID']
        
        # Track used dates to prevent duplicate meetings on same day
        used_communication_dates = set()
        
        for i in range(volume_per_client):
            # Determine communication type based on mix
            comm_type = get_communication_type()
            
            # Create timestamp within client lifespan, ensuring no duplicate meetings on same day
            attempts = 0
            while attempts < 20:  # Prevent infinite loops
                base_date = config.get_history_start_date() + timedelta(days=random.randint(0, 365))
                
                # For meetings, ensure no duplicates on same day for this client
                if comm_type == 'Meeting':
                    date_key = (client_id, base_date)  # base_date is already a date object
                    if date_key in used_communication_dates:
                        attempts += 1
                        continue
                    used_communication_dates.add(date_key)
                
                timestamp = datetime.combine(base_date, datetime.min.time()) + timedelta(
                    hours=random.randint(9, 17),
                    minutes=random.randint(0, 59)
                )
                break
            else:
                # Fallback if we can't find a unique date - still create the communication
                base_date = config.get_history_start_date() + timedelta(days=random.randint(0, 365))
                timestamp = datetime.combine(base_date, datetime.min.time()) + timedelta(
                    hours=random.randint(9, 17),
                    minutes=random.randint(0, 59)
                )
            
            # Select a ticker to reference (with some noise)
            referenced_ticker = random.choice(tickers) if random.random() > config.CONTROLLED_NOISE_RATE else "UNKNOWN"
            
            # Determine sentiment
            sentiment_type = get_sentiment_type()
            sentiment_score = get_sentiment_score(sentiment_type)
            
            # Create prompt based on communication type
            prompt = create_communication_prompt(
                client, comm_type, referenced_ticker, sentiment_type
            )
            
            # Create subject based on type
            subject = create_communication_subject(comm_type, referenced_ticker, sentiment_type)
            
            prompts_data.append({
                'COMMUNICATION_ID': f'COMM_{comm_id:06d}',
                'CLIENT_ID': client_id,
                'ADVISOR_ID': advisor_id,
                'TIMESTAMP': timestamp,
                'CHANNEL': comm_type,
                'SUBJECT': subject,
                'PROMPT_TEXT': prompt,
                'SENTIMENT_SCORE': sentiment_score
            })
            
            comm_id += 1
    
    return prompts_data

def get_communication_type() -> str:
    """Get communication type based on configured mix"""
    rand = random.random()
    if rand < config.COMMUNICATIONS_MIX['emails']:
        return 'Email'
    elif rand < config.COMMUNICATIONS_MIX['emails'] + config.COMMUNICATIONS_MIX['phone_transcripts']:
        return 'Phone'
    else:
        return 'Meeting'

def get_sentiment_type() -> str:
    """Get sentiment type based on configured distribution"""
    rand = random.random()
    if rand < config.SENTIMENT_DISTRIBUTION['neutral']:
        return 'neutral'
    elif rand < config.SENTIMENT_DISTRIBUTION['neutral'] + config.SENTIMENT_DISTRIBUTION['positive']:
        return 'positive'
    else:
        return 'negative'

def get_sentiment_score(sentiment_type: str) -> float:
    """Get numerical sentiment score based on type"""
    if sentiment_type == 'positive':
        return round(random.uniform(0.6, 1.0), 2)
    elif sentiment_type == 'negative':
        return round(random.uniform(-1.0, -0.6), 2)
    else:
        return round(random.uniform(-0.3, 0.3), 2)

def create_communication_prompt(client, comm_type: str, ticker: str, sentiment: str) -> str:
    """Create a dynamic prompt for communication generation"""
    
    client_name = f"{client['FIRSTNAME']} {client['LASTNAME']}"
    advisor_name = f"{client['ADVISORFIRSTNAME']} {client['ADVISORLASTNAME']}"
    risk_tolerance = client['RISKTOLERANCE']
    
    base_prompt = f"""
You are generating a realistic {comm_type.lower()} communication for a wealth management demo.

Context:
- Client: {client_name}
- Advisor: {advisor_name}
- Client Risk Tolerance: {risk_tolerance}
- Referenced Security: {ticker}
- Communication Sentiment: {sentiment}
- Communication Type: {comm_type}

Instructions:
- Write a natural, professional {comm_type.lower()} between the client and advisor
- Reference the security {ticker} naturally in the conversation
- Maintain {sentiment} sentiment throughout
- Keep it realistic for wealth management context
- Length: 150-300 words for emails, 200-400 words for calls/meetings
"""
    
    if comm_type == 'Email':
        base_prompt += f"""
- Format as an email with natural flow
- Include context about portfolio performance or market concerns
- Client may ask questions about {ticker} or market conditions
"""
    elif comm_type == 'Phone':
        base_prompt += f"""
- Format as a phone call transcript with [Client] and [Advisor] labels
- Include natural conversation flow about portfolio review
- Discussion should cover {ticker} and overall portfolio performance
- Duration: 15-45 minutes worth of content
"""
    else:  # Meeting
        base_prompt += f"""
- Format as a meeting transcript with [Client] and [Advisor] labels
- Include comprehensive portfolio review discussion
- Cover {ticker} performance and strategic planning
- Duration: 15-45 minutes worth of content
"""
    
    base_prompt += f"\n\nGenerate the {comm_type.lower()} content:"
    
    return base_prompt

def create_communication_subject(comm_type: str, ticker: str, sentiment: str) -> str:
    """Create appropriate subject line for communication"""
    
    if comm_type == 'Email':
        if sentiment == 'positive':
            subjects = [
                f"Great performance update on {ticker}",
                f"Positive developments in your portfolio",
                f"Strong returns - {ticker} update",
                "Portfolio performance review - good news"
            ]
        elif sentiment == 'negative':
            subjects = [
                f"Market volatility affecting {ticker}",
                f"Portfolio adjustment recommendations",
                f"Concerns about {ticker} position",
                "Market update and strategy discussion"
            ]
        else:
            subjects = [
                f"Monthly portfolio review - {ticker}",
                "Portfolio update and market outlook",
                f"Investment strategy discussion",
                "Quarterly portfolio check-in"
            ]
        return random.choice(subjects)
    
    elif comm_type == 'Phone':
        return f"Phone call - Portfolio review and {ticker} discussion"
    
    else:  # Meeting
        return f"Client meeting - Comprehensive portfolio review"

def generate_research_corpus(session: Session, test_mode: bool = False):
    """Generate research corpus using Cortex Complete"""
    print("    → Generating research corpus...")
    
    # Get securities for research coverage
    securities = session.table(f"{config.DATABASE_NAME}.CURATED.DIM_SECURITY").collect()
    
    prompts_data = []
    doc_id = 1
    
    # Determine volume based on test mode
    docs_per_ticker = 5 if test_mode else config.UNSTRUCTURED_DOCS_PER_TICKER
    
    for security in securities:
        ticker = security['PRIMARYTICKER']
        description = security['DESCRIPTION']
        
        for i in range(docs_per_ticker):
            # Create different types of research documents
            doc_types = ['Analyst Report', 'Earnings Analysis', 'ESG Assessment', 'Market Commentary', 'Investment Thesis']
            doc_type = random.choice(doc_types)
            
            # Create publication date within history range
            pub_date = config.get_history_start_date() + timedelta(days=random.randint(0, 365))
            
            # Create research prompt
            prompt = create_research_prompt(ticker, description, doc_type)
            
            prompts_data.append({
                'DOCUMENT_ID': f'RES_{doc_id:06d}',
                'DOCUMENT_TITLE': f'{doc_type}: {description} ({ticker})',
                'DOCUMENT_TYPE': doc_type,
                'TICKER': ticker,
                'PUBLISH_DATE': pub_date,
                'SOURCE': random.choice(['Internal Research', 'Goldman Sachs', 'Morgan Stanley', 'J.P. Morgan']),
                'LANGUAGE': 'en',
                'PROMPT_TEXT': prompt
            })
            
            doc_id += 1
    
    # Use the same 5-step pipeline for research
    prompts_df = session.create_dataframe(prompts_data)
    prompts_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_RESEARCH_PROMPTS", )
    
    prompts_table_df = session.table(f"{config.DATABASE_NAME}.RAW.TEMP_RESEARCH_PROMPTS")
    
    generated_df = prompts_table_df.with_column(
        'GENERATED_CONTENT',
        Complete(
            lit(config.MODEL_BY_CORPUS['research']),
            col('PROMPT_TEXT')
        )
    )
    
    final_research = generated_df.select(
        col('DOCUMENT_ID'),
        col('DOCUMENT_TITLE'),
        col('DOCUMENT_TYPE'),
        col('TICKER'),
        col('PUBLISH_DATE'),
        col('SOURCE'),
        col('LANGUAGE'),
        col('GENERATED_CONTENT').alias('DOCUMENT_TEXT')
    )
    
    final_research.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS", )
    
    # Clean up temp table
    session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_RESEARCH_PROMPTS").collect()
    
    print(f"    ✅ Generated research corpus")

def create_research_prompt(ticker: str, description: str, doc_type: str) -> str:
    """Create dynamic prompt for research document generation"""
    
    base_prompt = f"""
You are generating a realistic {doc_type.lower()} for a wealth management research database.

Context:
- Company: {description}
- Ticker: {ticker}
- Document Type: {doc_type}

Instructions:
- Write professional investment research content
- Include specific analysis relevant to {ticker}
- Maintain objective, analytical tone
- Include financial metrics and market context
- Length: 300-500 words
"""
    
    if doc_type == 'ESG Assessment':
        base_prompt += """
- Focus on Environmental, Social, and Governance factors
- Include carbon neutrality goals and sustainability initiatives
- Assess ESG risks and opportunities
- Provide ESG rating rationale
"""
    elif doc_type == 'Analyst Report':
        base_prompt += """
- Include investment recommendation (Buy/Hold/Sell)
- Provide price target and rationale
- Analyze financial performance and outlook
- Discuss key risks and opportunities
"""
    elif doc_type == 'Earnings Analysis':
        base_prompt += """
- Analyze recent quarterly earnings results
- Compare actual vs. expected performance
- Discuss management guidance and outlook
- Highlight key financial metrics
"""
    
    base_prompt += f"\n\nGenerate the {doc_type.lower()} content for {ticker}:"
    
    return base_prompt

def generate_regulatory_corpus(session: Session, test_mode: bool = False):
    """Generate regulatory corpus using Cortex Complete"""
    print("    → Generating regulatory corpus...")
    
    # Create regulatory documents relevant to wealth management
    regulatory_topics = [
        {'regulator': 'FINRA', 'rule_id': '2210', 'title': 'Communications with the Public'},
        {'regulator': 'FINRA', 'rule_id': '3110', 'title': 'Books and Records'},
        {'regulator': 'SEC', 'rule_id': 'Reg S-P', 'title': 'Privacy of Consumer Financial Information'},
        {'regulator': 'FINRA', 'rule_id': '4512', 'title': 'Customer Account Information'},
        {'regulator': 'SEC', 'rule_id': '206(4)-7', 'title': 'Compliance Procedures and Practices'}
    ]
    
    prompts_data = []
    doc_id = 1
    
    for topic in regulatory_topics:
        # Create publication date
        pub_date = config.get_history_start_date() + timedelta(days=random.randint(0, 200))
        
        # Create regulatory prompt
        prompt = create_regulatory_prompt(topic)
        
        prompts_data.append({
            'DOCUMENT_ID': f'REG_{doc_id:06d}',
            'REGULATOR': topic['regulator'],
            'RULE_ID': topic['rule_id'],
            'TITLE': topic['title'],
            'PUBLISH_DATE': pub_date,
            'PROMPT_TEXT': prompt
        })
        
        doc_id += 1
    
    # Use the same 5-step pipeline for regulatory content
    prompts_df = session.create_dataframe(prompts_data)
    prompts_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_REGULATORY_PROMPTS", )
    
    prompts_table_df = session.table(f"{config.DATABASE_NAME}.RAW.TEMP_REGULATORY_PROMPTS")
    
    generated_df = prompts_table_df.with_column(
        'GENERATED_CONTENT',
        Complete(
            lit(config.MODEL_BY_CORPUS['regulatory']),
            col('PROMPT_TEXT')
        )
    )
    
    final_regulatory = generated_df.select(
        col('DOCUMENT_ID'),
        col('REGULATOR'),
        col('RULE_ID'),
        col('TITLE'),
        col('PUBLISH_DATE'),
        col('GENERATED_CONTENT').alias('CONTENT')
    )
    
    final_regulatory.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.REGULATORY_CORPUS", )
    
    # Clean up temp table
    session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_REGULATORY_PROMPTS").collect()
    
    print(f"    ✅ Generated regulatory corpus")

def create_regulatory_prompt(topic: dict) -> str:
    """Create dynamic prompt for regulatory document generation"""
    
    prompt = f"""
You are generating realistic regulatory guidance content for a financial services compliance database.

Context:
- Regulator: {topic['regulator']}
- Rule ID: {topic['rule_id']}
- Title: {topic['title']}

Instructions:
- Write professional regulatory guidance content
- Include specific compliance requirements and procedures
- Maintain formal, authoritative tone appropriate for regulatory documents
- Include practical implementation guidance for financial firms
- Length: 400-600 words
- Focus on wealth management and investment advisory context

Generate the regulatory guidance content for {topic['rule_id']} - {topic['title']}:
"""
    
    return prompt

def create_client_interactions_view(session: Session):
    """Create client interactions view for CLIENT_INTERACTIONS_SV"""
    session.sql(f"""
        CREATE OR REPLACE VIEW {config.DATABASE_NAME}.CURATED.VW_CLIENT_INTERACTIONS AS
        SELECT 
            CLIENT_ID,
            ADVISOR_ID,
            CHANNEL,
            DATE(TIMESTAMP) as INTERACTION_DATE,
            COUNT(*) as COUNT_COMMUNICATIONS,
            AVG(CASE 
                WHEN CHANNEL IN ('Phone', 'Meeting') THEN 30 
                ELSE 5 
            END) as AVG_LENGTH_MINUTES,
            MAX(TIMESTAMP) as LAST_CONTACT_DATE
        FROM {config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS
        GROUP BY CLIENT_ID, ADVISOR_ID, CHANNEL, DATE(TIMESTAMP)
    """).collect()

# ======================================================
# ESG RESEARCH CONTENT CREATION
# ======================================================

def enhance_esg_content(session: Session):
    """Create ESG research content for the research corpus"""
    
    # Ensure database context
    session.sql(f"USE DATABASE {config.DATABASE_NAME}").collect()
    
    # Create enhanced ESG research content
    create_esg_research_content(session)
    
    # Create carbon neutrality research
    create_carbon_neutrality_research(session)
    
    # Create sustainability reports
    create_sustainability_reports(session)

def create_esg_research_content(session: Session):
    """Create enhanced ESG research using Cortex Complete"""
    
    print("    → Creating enhanced ESG research...")
    
    # ESG research prompts for golden tickers
    esg_prompts = []
    doc_id_start = 1000  # Start with high ID to avoid conflicts
    
    esg_research_topics = [
        {
            'ticker': 'MSFT',
            'company': 'Microsoft Corporation', 
            'theme': 'Carbon Negative Leadership',
            'focus': 'Microsoft\'s commitment to being carbon negative by 2030, AI for sustainability initiatives, and comprehensive climate action plan'
        },
        {
            'ticker': 'AAPL',
            'company': 'Apple Inc.',
            'theme': 'Circular Economy Innovation', 
            'focus': 'Apple\'s closed-loop supply chain, renewable energy transition, and product lifecycle sustainability'
        },
        {
            'ticker': 'NVDA',
            'company': 'NVIDIA Corporation',
            'theme': 'AI for Climate Solutions',
            'focus': 'NVIDIA\'s AI applications for climate modeling, energy efficiency, and sustainable computing'
        },
        {
            'ticker': 'SAP',
            'company': 'SAP SE',
            'theme': 'Sustainability Software Leadership',
            'focus': 'SAP\'s sustainability management software, carbon accounting solutions, and European ESG compliance'
        }
    ]
    
    for i, topic in enumerate(esg_research_topics):
        prompt = f"""
You are generating professional ESG research content for an investment management firm.

Context:
- Company: {topic['company']} ({topic['ticker']})
- ESG Theme: {topic['theme']}
- Research Focus: {topic['focus']}

Instructions:
- Write a comprehensive ESG analysis report
- Include specific environmental initiatives and measurable goals
- Discuss social impact programs and governance practices
- Provide investment implications and ESG scoring rationale
- Include carbon neutrality commitments and timeline
- Maintain professional investment research tone
- Length: 400-600 words

Generate the ESG research report:
"""
        
        esg_prompts.append({
            'DOCUMENT_ID': f'ESG_{doc_id_start + i:03d}',
            'DOCUMENT_TITLE': f'ESG Leadership Analysis: {topic["company"]} - {topic["theme"]}',
            'DOCUMENT_TYPE': 'ESG Research',
            'TICKER': topic['ticker'],
            'PUBLISH_DATE': config.get_history_end_date(),
            'SOURCE': 'Internal ESG Research Team',
            'LANGUAGE': 'en',
            'PROMPT_TEXT': prompt
        })
    
    # Use Cortex Complete to generate content
    if esg_prompts:
        prompts_df = session.create_dataframe(esg_prompts)
        prompts_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_ESG_PROMPTS")
        
        prompts_table_df = session.table(f"{config.DATABASE_NAME}.RAW.TEMP_ESG_PROMPTS")
        
        generated_df = prompts_table_df.with_column(
            'GENERATED_CONTENT',
            Complete(
                lit(config.MODEL_BY_CORPUS['research']),
                col('PROMPT_TEXT')
            )
        )
        
        # Insert into research corpus
        final_esg = generated_df.select(
            col('DOCUMENT_ID'),
            col('DOCUMENT_TITLE'),
            col('DOCUMENT_TYPE'),
            col('TICKER'),
            col('PUBLISH_DATE'),
            col('SOURCE'),
            col('LANGUAGE'),
            col('GENERATED_CONTENT').alias('DOCUMENT_TEXT')
        )
        
        # Append to existing research corpus
        final_esg.write.mode("append").save_as_table(f"{config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS")
        
        # Clean up temp table
        session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_ESG_PROMPTS").collect()
        
        print(f"    ✅ Generated {len(esg_prompts)} enhanced ESG research documents")

def create_carbon_neutrality_research(session: Session):
    """Create specific carbon neutrality research content"""
    
    print("    → Creating carbon neutrality research...")
    
    # Carbon neutrality specific content
    carbon_content = [
        {
            'id': 'CARBON_001',
            'title': 'Corporate Carbon Neutrality Commitments: Technology Sector Leadership',
            'ticker': 'MSFT',
            'content': 'Microsoft leads the technology sector with its ambitious carbon negative commitment by 2030. The company has invested over $1 billion in climate innovation and developed comprehensive carbon accounting methodologies. Key initiatives include renewable energy procurement, carbon capture technologies, and AI-powered sustainability solutions. Investment implications suggest strong ESG positioning for long-term value creation and regulatory compliance preparedness.'
        },
        {
            'id': 'CARBON_002', 
            'title': 'Apple\'s Carbon Neutral Supply Chain: Circular Economy Innovation',
            'ticker': 'AAPL',
            'content': 'Apple has committed to achieving carbon neutrality across its entire supply chain by 2030. The company\'s innovative approach includes transitioning to recycled materials, renewable energy partnerships, and closed-loop manufacturing processes. Apple\'s environmental leadership creates competitive advantages in ESG-conscious markets while reducing operational risks from climate regulations and resource scarcity.'
        },
        {
            'id': 'CARBON_003',
            'title': 'AI-Powered Climate Solutions: Technology\'s Role in Carbon Reduction',
            'ticker': 'NVDA', 
            'content': 'NVIDIA\'s AI platforms are enabling breakthrough climate solutions including weather prediction, renewable energy optimization, and carbon footprint modeling. The company\'s GPUs power climate research and energy efficiency applications while its own operations focus on sustainable computing. This positions NVIDIA as both a climate solution provider and responsible technology leader.'
        }
    ]
    
    # Insert carbon neutrality research directly
    for content in carbon_content:
        # Escape single quotes
        escaped_content = content['content'].replace("'", "''")
        escaped_title = content['title'].replace("'", "''")
        
        session.sql(f"""
            INSERT INTO {config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS
            (DOCUMENT_ID, DOCUMENT_TITLE, DOCUMENT_TYPE, TICKER, PUBLISH_DATE, SOURCE, LANGUAGE, DOCUMENT_TEXT)
            VALUES
            ('{content['id']}', '{escaped_title}', 'Carbon Neutrality Research', '{content['ticker']}',
             '{config.get_history_end_date()}', 'ESG Research Team', 'en', '{escaped_content}')
        """).collect()
    
    print(f"    ✅ Generated {len(carbon_content)} carbon neutrality research documents")

def create_sustainability_reports(session: Session):
    """Create sustainability report summaries"""
    
    print("    → Creating sustainability report summaries...")
    
    sustainability_reports = [
        {
            'id': 'SUSTAIN_001',
            'title': 'Microsoft 2025 Sustainability Report: Carbon Negative Progress',
            'ticker': 'MSFT',
            'content': 'Microsoft reports significant progress toward its carbon negative goal, achieving 30% reduction in emissions since 2020. Key achievements include 100% renewable energy for global operations, $1.3B in climate innovation investments, and AI-powered sustainability solutions for customers. The company\'s comprehensive approach includes Scope 1, 2, and 3 emissions with transparent reporting and science-based targets.'
        },
        {
            'id': 'SUSTAIN_002',
            'title': 'Apple Environmental Progress Report: Supply Chain Transformation',
            'ticker': 'AAPL', 
            'content': 'Apple\'s latest environmental report demonstrates substantial progress in supply chain decarbonization with 75% of manufacturing partners committed to renewable energy. The company achieved carbon neutrality for corporate operations and is on track for complete carbon neutrality by 2030. Innovation highlights include recycled materials comprising 40% of product components and breakthrough battery recycling technologies.'
        }
    ]
    
    # Insert sustainability reports
    for report in sustainability_reports:
        escaped_content = report['content'].replace("'", "''")
        escaped_title = report['title'].replace("'", "''")
        
        session.sql(f"""
            INSERT INTO {config.DATABASE_NAME}.CURATED.RESEARCH_CORPUS
            (DOCUMENT_ID, DOCUMENT_TITLE, DOCUMENT_TYPE, TICKER, PUBLISH_DATE, SOURCE, LANGUAGE, DOCUMENT_TEXT)
            VALUES
            ('{report['id']}', '{escaped_title}', 'Sustainability Report', '{report['ticker']}',
             '{config.get_history_end_date()}', 'Corporate Sustainability Team', 'en', '{escaped_content}')
        """).collect()
    
    print(f"    ✅ Generated {len(sustainability_reports)} sustainability reports")

# ======================================================
# FINANCIAL PLANNING DOCUMENTS GENERATION
# ======================================================

def generate_planning_corpus(session: Session, test_mode: bool = False):
    """Generate financial planning documents using Cortex Complete"""
    print("    → Generating planning corpus...")
    
    # Get clients for planning document generation
    clients_query = f"""
        SELECT 
            c.ClientID,
            c.AdvisorID,
            c.FirstName,
            c.LastName,
            c.RiskTolerance,
            c.InvestmentHorizon,
            c.OnboardingDate,
            a.FirstName as AdvisorFirstName,
            a.LastName as AdvisorLastName
        FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT c
        JOIN {config.DATABASE_NAME}.CURATED.DIM_ADVISOR a ON c.AdvisorID = a.AdvisorID
        WHERE c.IsActive = TRUE
    """
    
    clients = session.sql(clients_query).collect()
    
    prompts_data = []
    doc_id = 1
    
    # Determine volume based on test mode - 3-5 planning documents per client
    docs_per_client = 3 if test_mode else 5
    
    for client in clients:
        client_id = client['CLIENTID']
        advisor_id = client['ADVISORID']
        
        # Generate different types of planning documents
        planning_doc_types = [
            'Comprehensive Financial Plan',
            'Investment Policy Statement',
            'Retirement Planning Analysis', 
            'Education Funding Plan',
            'Estate Planning Strategy'
        ]
        
        # Select document types based on volume
        selected_types = planning_doc_types[:docs_per_client]
        
        # Track document dates to avoid duplicates and create version history
        used_dates = set()
        
        for doc_type in selected_types:
            # For Education Funding Plans, create multiple versions with different dates
            versions_to_create = 3 if doc_type == 'Education Funding Plan' else 1
            
            for version in range(versions_to_create):
                # Create document date within client relationship, ensuring no duplicates
                attempts = 0
                while attempts < 10:  # Prevent infinite loops
                    days_offset = random.randint(30, 365) + (version * 90)  # Spread versions across time
                    doc_date = client['ONBOARDINGDATE'] + timedelta(days=days_offset)
                    # Ensure we have a date object for the key
                    if hasattr(doc_date, 'date'):
                        date_part = doc_date.date()
                    else:
                        date_part = doc_date
                    date_key = (client_id, date_part)
                    if date_key not in used_dates:
                        used_dates.add(date_key)
                        break
                    attempts += 1
                else:
                    # Fallback if we can't find a unique date
                    doc_date = client['ONBOARDINGDATE'] + timedelta(days=random.randint(30, 365))
                
                # Determine goal category
                goal_category = get_goal_category(doc_type)
                
                # Create planning document prompt
                prompt = create_planning_document_prompt(client, doc_type, goal_category)
                
                # Create document title with version/date if multiple
                if versions_to_create > 1:
                    version_suffix = f" - {doc_date.strftime('%B %Y')} Update" if version > 0 else " - Initial Plan"
                    title = f"{doc_type} - {client['FIRSTNAME']} {client['LASTNAME']}{version_suffix}"
                else:
                    title = f"{doc_type} - {client['FIRSTNAME']} {client['LASTNAME']}"
                
                prompts_data.append({
                    'DOCUMENT_ID': f'PLAN_{doc_id:06d}',
                    'PLAN_TITLE': title,
                    'PLAN_TYPE': doc_type,
                    'CLIENT_ID': client_id,
                    'ADVISOR_ID': advisor_id,
                    'CREATED_DATE': doc_date,
                    'GOAL_CATEGORY': goal_category,
                    'PROMPT_TEXT': prompt
                })
                
                doc_id += 1
    
    # Use the same 5-step pipeline for planning documents
    prompts_df = session.create_dataframe(prompts_data)
    prompts_df.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.RAW.TEMP_PLANNING_PROMPTS")
    
    prompts_table_df = session.table(f"{config.DATABASE_NAME}.RAW.TEMP_PLANNING_PROMPTS")
    
    generated_df = prompts_table_df.with_column(
        'GENERATED_CONTENT',
        Complete(
            lit(config.MODEL_BY_CORPUS['research']),  # Use research model for planning docs
            col('PROMPT_TEXT')
        )
    )
    
    final_planning = generated_df.select(
        col('DOCUMENT_ID'),
        col('PLAN_TITLE'),
        col('PLAN_TYPE'),
        col('CLIENT_ID'),
        col('ADVISOR_ID'),
        col('CREATED_DATE'),
        col('GOAL_CATEGORY'),
        col('GENERATED_CONTENT').alias('DOCUMENT_TEXT')
    )
    
    final_planning.write.mode("overwrite").save_as_table(f"{config.DATABASE_NAME}.CURATED.PLANNING_CORPUS")
    
    # Clean up temp table
    session.sql(f"DROP TABLE IF EXISTS {config.DATABASE_NAME}.RAW.TEMP_PLANNING_PROMPTS").collect()
    
    print(f"    ✅ Generated planning corpus")

def get_goal_category(doc_type: str) -> str:
    """Map document type to goal category"""
    goal_mapping = {
        'Comprehensive Financial Plan': 'Comprehensive',
        'Investment Policy Statement': 'Investment Strategy',
        'Retirement Planning Analysis': 'Retirement',
        'Education Funding Plan': 'Education',
        'Estate Planning Strategy': 'Estate Planning'
    }
    return goal_mapping.get(doc_type, 'General Planning')

def create_planning_document_prompt(client, doc_type: str, goal_category: str) -> str:
    """Create dynamic prompt for planning document generation"""
    
    client_name = f"{client['FIRSTNAME']} {client['LASTNAME']}"
    advisor_name = f"{client['ADVISORFIRSTNAME']} {client['ADVISORLASTNAME']}"
    risk_tolerance = client['RISKTOLERANCE']
    investment_horizon = client['INVESTMENTHORIZON']
    
    base_prompt = f"""
You are generating a realistic {doc_type.lower()} for a wealth management planning database.

Context:
- Client: {client_name}
- Advisor: {advisor_name}
- Risk Tolerance: {risk_tolerance}
- Investment Horizon: {investment_horizon}
- Document Type: {doc_type}
- Goal Category: {goal_category}

Instructions:
- Write professional financial planning content appropriate for wealth management
- Include specific, measurable goals and timelines
- Maintain objective, advisory tone suitable for client presentation
- Include quantitative targets and strategic recommendations
- Reference appropriate asset allocation and risk management strategies
- Length: 400-700 words
"""
    
    if doc_type == 'Comprehensive Financial Plan':
        base_prompt += """
- Include executive summary of client's overall financial situation
- Define primary financial goals with specific timelines and amounts
- Outline recommended investment strategy and asset allocation
- Address risk management and insurance needs
- Discuss tax planning strategies
- Include action items and review schedule
"""
    elif doc_type == 'Investment Policy Statement':
        base_prompt += """
- Define investment objectives and return expectations
- Specify asset allocation targets and ranges
- Outline investment constraints and restrictions
- Define rebalancing guidelines and review procedures
- Include benchmark specifications
- Address ESG preferences if applicable
"""
    elif doc_type == 'Retirement Planning Analysis':
        base_prompt += """
- Analyze current retirement savings and projected needs
- Calculate required savings rate to meet retirement goals
- Recommend retirement account strategies (401k, IRA, etc.)
- Include Social Security planning considerations
- Discuss retirement income distribution strategies
- Address healthcare and long-term care planning
"""
    elif doc_type == 'Education Funding Plan':
        base_prompt += """
- Estimate education costs for children with inflation adjustments
- Recommend 529 plan or other education savings strategies
- Calculate required monthly savings to meet education goals
- Discuss tax-advantaged education savings options
- Include timeline for education expenses and semester payment schedules
- Address potential financial aid implications
- Include specific action items for implementation (e.g., 529 distributions, account transfers)
- Consider university billing deadlines and payment processing times
- Address contingency funding options if education costs exceed projections
"""
    elif doc_type == 'Estate Planning Strategy':
        base_prompt += """
- Review current estate planning documents and needs
- Recommend estate tax minimization strategies
- Discuss trust structures and beneficiary planning
- Include life insurance needs analysis
- Address charitable giving strategies if applicable
- Outline action items for estate planning implementation
"""
    
    base_prompt += f"\n\nGenerate the {doc_type.lower()} content for {client_name}:"
    
    return base_prompt

def add_risk_flags_to_communications(session: Session):
    """Add risk flags to communications corpus using keyword detection and random assignment"""
    print("      → Adding risk flags to communications...")
    
    # Risk detection patterns for each category
    risk_patterns = {
        'PERFORMANCE_GUARANTEE': [
            'guarantee', 'promised return', 'assured profit', 'certain return',
            'guaranteed performance', 'will definitely', 'promise you will'
        ],
        'SUITABILITY_MISMATCH': [
            'aggressive for conservative', 'high risk for low tolerance', 
            'unsuitable investment', 'doesn\'t match profile', 'mismatch'
        ],
        'UNDOCUMENTED_REC': [
            'verbal recommendation', 'phone call only', 'undocumented advice',
            'off the record', 'informal suggestion'
        ],
        'PII_BREACH': [
            'social security', 'SSN', 'full credit card', 'bank account number',
            'password', 'personal information shared'
        ],
        'ESG_GREENWASHING': [
            'green but not really', 'ESG washing', 'fake sustainability',
            'misleading environmental', 'false ESG claims'
        ]
    }
    
    # Get all communications
    comms = session.sql(f"""
        SELECT COMMUNICATION_ID, CONTENT
        FROM {config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS
    """).collect()
    
    # Process each communication for risk detection
    import random
    risk_updates = []
    
    for comm in comms:
        content = comm['CONTENT'].lower() if comm['CONTENT'] else ''
        comm_id = comm['COMMUNICATION_ID']
        detected_risks = []
        
        # Check for pattern matches
        for category, patterns in risk_patterns.items():
            if any(pattern in content for pattern in patterns):
                detected_risks.append(category)
        
        # Add random risk flags based on configuration rate
        if not detected_risks and random.random() < config.RISK_FLAG_RATE:
            detected_risks.append(random.choice(config.RISK_CATEGORIES))
        
        # Update record if risks detected
        if detected_risks:
            primary_risk = detected_risks[0]
            severity = random.choices(['LOW', 'MEDIUM', 'HIGH'], weights=[0.6, 0.3, 0.1])[0]
            
            session.sql(f"""
                UPDATE {config.DATABASE_NAME}.CURATED.COMMUNICATIONS_CORPUS
                SET RISKCATEGORY = '{primary_risk}',
                    RISKSEVERITY = '{severity}',
                    RISKFLAGS = {len(detected_risks)}
                WHERE COMMUNICATION_ID = '{comm_id}'
            """).collect()
    
    print(f"      ✅ Risk flags added to communications")

def generate_departure_corpus(session: Session, test_mode: bool = False):
    """Generate departure documents for clients who have left"""
    print("    → Generating departure corpus...")
    
    # Get departed clients
    departed_clients = session.sql(f"""
        SELECT ClientID, FirstName || ' ' || LastName as ClientName,
               AdvisorID, DepartureReason, EndDate
        FROM {config.DATABASE_NAME}.CURATED.DIM_CLIENT
        WHERE EndDate IS NOT NULL
    """).collect()
    
    if not departed_clients:
        print("      → No departed clients found, skipping departure corpus")
        return
    
    # Get advisor names for context
    advisors = session.sql(f"""
        SELECT AdvisorID, FirstName || ' ' || LastName as AdvisorName
        FROM {config.DATABASE_NAME}.CURATED.DIM_ADVISOR
    """).collect()
    advisor_lookup = {a['ADVISORID']: a['ADVISORNAME'] for a in advisors}
    
    # Generate departure documents
    departure_data = []
    
    for client in departed_clients:
        client_id = client['CLIENTID']
        client_name = client['CLIENTNAME']
        advisor_id = client['ADVISORID']
        advisor_name = advisor_lookup.get(advisor_id, 'Unknown Advisor')
        departure_reason = client['DEPARTUREREASON']
        end_date = client['ENDDATE']
        
        # Generate exit questionnaire
        questionnaire_prompt = f"""
        Generate a realistic client exit questionnaire response for {client_name} who left due to {departure_reason}.
        Include:
        - Overall satisfaction rating (1-10)
        - Specific feedback about advisor service
        - Reasons for leaving
        - Communication frequency satisfaction
        - Investment performance concerns if applicable
        - Fee structure feedback
        - Likelihood to recommend (1-10)
        - Additional comments
        
        Make it authentic and vary the tone based on departure reason.
        """
        
        # For demo purposes, create simplified content rather than using Cortex Complete
        questionnaire_content = generate_departure_content(client_name, departure_reason, 'questionnaire')
        
        departure_data.append({
            'DOCUMENTID': f'EXIT_QUEST_{client_id}_{end_date.strftime("%Y%m%d")}',
            'CLIENTID': client_id,
            'CLIENTNAME': client_name,
            'ADVISORID': advisor_id,
            'ADVISORNAME': advisor_name,
            'DOCUMENTTYPE': 'EXIT_QUESTIONNAIRE',
            'DOCUMENTDATE': end_date,
            'TITLE': f'Exit Questionnaire - {client_name}',
            'DOCUMENTTEXT': questionnaire_content,
            'DEPARTUREREASON': departure_reason
        })
        
        # Generate exit interview notes (50% chance)
        if random.random() < 0.5:
            interview_content = generate_departure_content(client_name, departure_reason, 'interview')
            
            departure_data.append({
                'DOCUMENTID': f'EXIT_INTERVIEW_{client_id}_{end_date.strftime("%Y%m%d")}',
                'CLIENTID': client_id,
                'CLIENTNAME': client_name,
                'ADVISORID': advisor_id,
                'ADVISORNAME': advisor_name,
                'DOCUMENTTYPE': 'EXIT_INTERVIEW',
                'DOCUMENTDATE': end_date,
                'TITLE': f'Exit Interview Notes - {client_name}',
                'DOCUMENTTEXT': interview_content,
                'DEPARTUREREASON': departure_reason
            })
    
    # Save to departure corpus table
    if departure_data:
        import pandas as pd
        departure_df = pd.DataFrame(departure_data)
        session.write_pandas(departure_df, "CURATED.DEPARTURE_CORPUS", overwrite=True, quote_identifiers=False)
        print(f"      ✅ Generated {len(departure_data)} departure documents")
    else:
        print("      → No departure documents to generate")

def generate_departure_content(client_name: str, departure_reason: str, doc_type: str) -> str:
    """Generate realistic departure document content"""
    
    if doc_type == 'questionnaire':
        if departure_reason == 'Performance Dissatisfaction':
            return f"""
EXIT QUESTIONNAIRE - {client_name}

1. Overall satisfaction with advisory services (1-10): 4
2. Communication frequency: Adequate but concerning when performance was poor
3. Investment performance satisfaction: Very unsatisfied - portfolio underperformed market by significant margin
4. Fee structure feedback: Fees seemed high given poor performance
5. Advisor responsiveness: Good initially, but less responsive when issues arose
6. Likelihood to recommend (1-10): 2
7. Primary reason for leaving: Investment performance consistently below expectations
8. Additional comments: Expected better risk management and performance monitoring. Disappointed with lack of proactive communication during market downturns.

Date: {datetime.now().strftime('%Y-%m-%d')}
"""
        elif departure_reason == 'Fee Concerns':
            return f"""
EXIT QUESTIONNAIRE - {client_name}

1. Overall satisfaction with advisory services (1-10): 6
2. Communication frequency: Good
3. Investment performance satisfaction: Acceptable
4. Fee structure feedback: Too expensive compared to alternatives available
5. Advisor responsiveness: Very good
6. Likelihood to recommend (1-10): 5
7. Primary reason for leaving: Found lower-cost alternatives with similar services
8. Additional comments: Service quality was good but fees became prohibitive. Found robo-advisor with lower fees for similar portfolio management.

Date: {datetime.now().strftime('%Y-%m-%d')}
"""
        else:  # Other reasons
            return f"""
EXIT QUESTIONNAIRE - {client_name}

1. Overall satisfaction with advisory services (1-10): 7
2. Communication frequency: Good
3. Investment performance satisfaction: Satisfactory
4. Fee structure feedback: Fair
5. Advisor responsiveness: Good
6. Likelihood to recommend (1-10): 7
7. Primary reason for leaving: {departure_reason}
8. Additional comments: No major issues with service. Departure due to personal circumstances.

Date: {datetime.now().strftime('%Y-%m-%d')}
"""
    
    else:  # interview
        return f"""
EXIT INTERVIEW NOTES - {client_name}

Date: {datetime.now().strftime('%Y-%m-%d')}
Departure Reason: {departure_reason}

Client expressed overall satisfaction with relationship but {departure_reason.lower()} became primary concern.
Key themes from discussion:
- Service quality generally met expectations
- Communication style was appropriate for client needs
- Departure primarily driven by {departure_reason.lower()}

Action items for team:
- Review similar client situations
- Consider process improvements where applicable
- Follow up in 6 months if appropriate

Interview conducted by: Regional Manager
"""
