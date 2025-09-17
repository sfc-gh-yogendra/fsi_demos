I am a Sales Engineer at Snowflake and my goal is to build a compelling demo of  Snowflake AI, [https://docs.snowflake.com/en/guides-overview-ai-features](https://docs.snowflake.com/en/guides-overview-ai-features),  for my wealth management customers.

I have attached 1 document, wam\_ai\_research, that all contain research around AI for Wealth Management and how Snowflake can be a part of the identified use cases in the document. 

You have three tasks.     
1\) Review the info I give you, including reading the attached document wam\_ai\_research, and search the internet for further info that would help.    
2). Ask me 10 to 20 good questions that will help you finish a great design for a demo.  
3). After I respond to those, you will then create a functional requirements document,a high level technical design and a high level project plan (do not think of time, resources but the phases needed) for implementing all the use cases identified in wam\_ai\_research. When creating those documents have in mind that they will be used by [Cursor.ai](http://Cursor.ai) for helping me generate the code..

These are my requirements on the demo:

The demo needs to cover all identified use cases. Each use case workflow should be translated into multiple steps where a user starts with an initial question to the Agent and then based on the Agent response continue with follow up questions, so each workflow should have 3-4 user questions. For each question there should be an expected response from the agent, what tools it would use and what data it will access.

Focus is to generate the data needed both structured and unstructured and also how to set up the Agents, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence\#create-an-agent, and to create the needed tools, Cortex Analyst and Cortex Search. The data that is generated need also cover data that would come from various data providers and public sources.

The data generation should use Python and Snowflake Snowpark for Python Dataframes  as much as possible. 

The generation of unstructured data should be done using Snowflake Cortex Complete function,[https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete](https://docs.snowflake.com/en/developer-guide/snowpark-ml/reference/latest/api/cortex/snowflake.cortex.complete), using llama3.1-70b as the model, and should mimic realistic data. The logic for generating the unstructured data should be:  
 1\. Generate dynamic prompts first based needed generated structured data etc  
 2\. Store those in a Snowflake table  
 3\. Create a Snowpark DataFrame on the prompt table  
 4\.  Use with\_column to create a new column with the generated content using complete(), with model name as the model parameter, lit(model name) and the column with the prompt as the prompt parameter.  
5\. Save it in a Snowflake table. 

It should use Python and Snowflake Snowpark for Python Dataframes  as much as possible.

Each demo scenario will have one Agent that can use any combination of Cortex Analyst, https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence\#create-an-agent-that-uses-a-semantic-view-in-cortex-analyst, and Cortex Search, [https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence\#create-an-agent-that-uses-the-cortex-search-service](https://docs.snowflake.com/en/user-guide/snowflake-cortex/snowflake-intelligence#create-an-agent-that-uses-the-cortex-search-service). Part of the demo build is to create the instructions to configure an Agent, when doing that it should always split into Response Instructions (how to respond) and Planning Instructions (tool selection), each tool will also need a description that makes it easy for the Agent to understand what and when to use the tool. 

For Cortex Analyst we will always use SEMANTIC VIEWS, [https://docs.snowflake.com/en/user-guide/views-semantic/overview](https://docs.snowflake.com/en/user-guide/views-semantic/overview), and pay attention to how a SEMANTIC VIEW is created with SQL [https://docs.snowflake.com/en/user-guide/views-semantic/sql](https://docs.snowflake.com/en/user-guide/views-semantic/sql) and use proper TABLES (https://docs.snowflake.com/en/user-guide/views-semantic/sql\#defining-the-logical-tables), RELATIONSHIPS (https://docs.snowflake.com/en/user-guide/views-semantic/sql\#label-semantic-views-create-relationships), FACTS, DIMENSIONS, METRICS (https://docs.snowflake.com/en/user-guide/views-semantic/sql\#defining-facts-dimensions-and-metrics) structure. Also always include COMMENT and WITH SYNONYMS for all supported elements. This is an example of how to create a Semantic View with SQL https://docs.snowflake.com/en/user-guide/views-semantic/example\#creating-the-semantic-view

 A SEMANTIC VIEW can also be queried using SQL, https://docs.snowflake.com/en/user-guide/views-semantic/querying\#basic-examples

For Cortex Search we will always create the service with SQL, https://docs.snowflake.com/sql-reference/sql/create-cortex-search\#example,and see the examples at and we can test it using SQL function SEARCH\_PREVIEW, [https://docs.snowflake.com/sql-reference/functions/search\_preview-snowflake-cortex\#examples](https://docs.snowflake.com/sql-reference/functions/search_preview-snowflake-cortex#examples)

The demo will use an existing Snowflake demo account.

When connecting to the account Snowpark will be used and using connection\_name ie Session.builder.config("connection\_name", "myconnection").create(). The actual connection\_name value should be provided as a parameter when running the creation of the data, if no name is provided the sfseeurope-mstellwall-aws-us-west3 should be used.

Control of data volumes, date range etc should be managed by a configuration file. It should also be able to configure which model to use for complete(), where llama3.1-70b should be used as default value.

For getting assets that can be used as part of portfolios etc the following SQL can be used:

```sql
with
Enriched_Securities AS (
    -- This CTE joins the main security index with geography, company characteristics, and aggregated exchange codes.
    SELECT
        osi.TOP_LEVEL_OPENFIGI_ID,
        osi.SECURITY_NAME,
        osi.ASSET_CLASS,
        osi.SECURITY_TYPE,
        osi.SECURITY_SUBTYPE,
        osi.PRIMARY_TICKER,
        ci.PRIMARY_EXCHANGE_CODE,
        ci.PRIMARY_EXCHANGE_NAME,
        --osi.GLOBAL_TICKERS,
        osi.EXCHANGE_CODES,
        ci.COMPANY_NAME AS ISSUER_NAME,
        -- Extract Country of Domicile from company characteristics
        MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'business_address_country' THEN char.VALUE END) AS COUNTRY_OF_DOMICILE,
        -- Use SIC Description as a proxy for industry, as GICS is not in this base dataset
        MAX(CASE WHEN char.RELATIONSHIP_TYPE = 'sic_description' THEN char.VALUE END) AS INDUSTRY_SECTOR
    FROM
        FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN.OPENFIGI_SECURITY_INDEX AS osi
    LEFT JOIN
        FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN.COMPANY_SECURITY_RELATIONSHIPS AS rship 
            ON osi.TOP_LEVEL_OPENFIGI_ID = rship.SECURITY_ID AND osi.TOP_LEVEL_OPENFIGI_ID_TYPE = rship.security_id_type
    LEFT JOIN
        FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN.COMPANY_INDEX AS ci ON rship.COMPANY_ID = ci.COMPANY_ID
    LEFT JOIN
        FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN.COMPANY_CHARACTERISTICS AS char ON rship.COMPANY_ID = char.COMPANY_ID,
    WHERE
        NOT (ARRAY_CONTAINS('CEDEAR'::variant, osi.SECURITY_TYPE) 
            OR ARRAY_CONTAINS('PRIV PLACEMENT'::variant, osi.SECURITY_TYPE)
            OR ARRAY_CONTAINS('Crypto'::variant, osi.SECURITY_TYPE))
    GROUP BY
        osi.TOP_LEVEL_OPENFIGI_ID,
        osi.SECURITY_NAME,
        osi.ASSET_CLASS,
        osi.SECURITY_TYPE,
        osi.SECURITY_SUBTYPE,
        osi.PRIMARY_TICKER,
        ci.PRIMARY_EXCHANGE_CODE,
        ci.PRIMARY_EXCHANGE_NAME,
        osi.EXCHANGE_CODES,
        ci.COMPANY_NAME
),
Categorized_Securities AS (
    -- This CTE applies the asset class and market region logic to each security.
    SELECT
        es.TOP_LEVEL_OPENFIGI_ID,
        es.SECURITY_NAME,
        es.ISSUER_NAME,
        es.PRIMARY_TICKER,
        es.PRIMARY_EXCHANGE_CODE,
        IFNULL(es.PRIMARY_EXCHANGE_NAME, es.EXCHANGE_CODES[0]::varchar) AS PRIMARY_EXCHANGE_NAME,
        es.EXCHANGE_CODES,
        es.INDUSTRY_SECTOR,
        es.COUNTRY_OF_DOMICILE,
        -- Asset Category Classification Logic (Expanded to include more bond types)
        CASE
            WHEN es.ASSET_CLASS = 'Corp' THEN 'Corporate Bond'
            WHEN es.ASSET_CLASS = 'Govt' THEN 'Government Bond'
            WHEN es.ASSET_CLASS = 'Muni' THEN 'Municipal Bond'
            WHEN es.ASSET_CLASS = 'Mtge' THEN 'Mortgage-Backed Security'
            WHEN es.ASSET_CLASS = 'Equity' AND (
                ARRAY_CONTAINS('ETF'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Exchange Traded Fund'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('ETN'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('ETP'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Unit Trust'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('UIT'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Closed-End Fund'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Open-End Fund'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Fund of Funds'::variant, es.SECURITY_TYPE) OR
                ARRAY_CONTAINS('Mutual Fund'::variant, es.SECURITY_SUBTYPE)
            ) THEN 'ETF'
            WHEN es.ASSET_CLASS = 'Equity' THEN 'Equity'
            ELSE NULL
        END AS ASSET_CATEGORY,
        -- Market Region Classification Logic
        CASE
            WHEN es.COUNTRY_OF_DOMICILE = 'US' THEN 'USA'
            WHEN es.COUNTRY_OF_DOMICILE IN (
                'AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR',
                'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK',
                'SI', 'ES', 'SE'
            ) THEN 'EU'
            WHEN es.COUNTRY_OF_DOMICILE IN (
                'AF', 'AU', 'BD', 'BT', 'BR', 'BN', 'KH', 'CL', 'CN', 'CO', 'CK', 'CZ',
                'KP', 'EG', 'FJ', 'GR', 'HK', 'HU', 'IN', 'ID', 'JP', 'KI', 'KW', 'LA',
                'MY', 'MV', 'MH', 'MX', 'FM', 'MN', 'MM', 'NR', 'NP', 'NZ', 'PK', 'PW',
                'PG', 'PE', 'PH', 'PL', 'QA', 'KR', 'WS', 'SA', 'SG', 'SB', 'ZA', 'LK',
                'TW', 'TH', 'TL', 'TO', 'TR', 'TV', 'AE', 'VU', 'VN'
            ) THEN 'APAC/EM'
            ELSE 'Other'
        END AS MARKET_REGION
    FROM
        Enriched_Securities AS es
)
-- Final SELECT Statement
-- This query selects the categorized and filtered data, returning the final list with all requested columns.
SELECT
    cs.MARKET_REGION,
    cs.ASSET_CATEGORY,
    cs.ISSUER_NAME,
    cs.INDUSTRY_SECTOR,
    cs.TOP_LEVEL_OPENFIGI_ID,
    cs.SECURITY_NAME,
    cs.PRIMARY_TICKER,
    cs.PRIMARY_EXCHANGE_CODE,
    cs.PRIMARY_EXCHANGE_NAME,
    cs.COUNTRY_OF_DOMICILE,
    cs.EXCHANGE_CODES,
FROM
    Categorized_Securities cs
WHERE
    cs.ASSET_CATEGORY IS NOT NULL
ORDER BY
    cs.MARKET_REGION,
    cs.ASSET_CATEGORY,
    cs.ISSUER_NAME,
    cs.SECURITY_NAME;
```

For getting real market values for some of the assets the following SQL can be used

```sql
SELECT 
        TICKER,
        DATE,
        PRIMARY_EXCHANGE_CODE,
        PRIMARY_EXCHANGE_NAME,
        MAX(CASE WHEN VARIABLE = 'pre-market_open' THEN VALUE END) as OPEN_PRICE,
        MAX(CASE WHEN VARIABLE = 'all-day_high' THEN VALUE END) as HIGH_PRICE,
        MAX(CASE WHEN VARIABLE = 'all-day_low' THEN VALUE END) as LOW_PRICE,
        MAX(CASE WHEN VARIABLE = 'post-market_close' THEN VALUE END) as CLOSE_PRICE,
        MAX(CASE WHEN VARIABLE = 'nasdaq_volume' THEN VALUE END) as VOLUME
    FROM FINANCIALS_ECONOMICS_ENTERPRISE.CYBERSYN.STOCK_PRICE_TIMESERIES
    WHERE TICKER IN ({ticker_list})
    GROUP BY TICKER, DATE, PRIMARY_EXCHANGE_CODE, PRIMARY_EXCHANGE_NAME
    HAVING 
        CLOSE_PRICE IS NOT NULL  -- Only require close price
    ORDER BY TICKER, DATE;
```

If anything is unclear, do ask me questions. I want to help.

Gemini Response:

# **Snowflake AI for Wealth Management: A Technical Blueprint for Demonstration**

## **Part I: Functional Requirements Specification**

### **1.0 Demo Personas and Narrative Framework**

This document specifies the functional and technical requirements for a comprehensive demonstration of Snowflake's AI capabilities tailored for the wealth management industry. The demonstration is structured around three core personas, each representing a critical function within a modern wealth management firm. The narrative framework is designed to showcase not only the individual value of Snowflake AI for each role but also the synergistic, platform-level benefits that arise when data and AI-driven insights are shared across the enterprise on a single, governed platform.1

#### **1.1 The Augmented Wealth Manager: "Sarah"**

* **Description:** Sarah is a senior Wealth Manager responsible for a significant book of high-net-worth clients. Her role is a dynamic blend of financial planning, client servicing, and business development.2 Her primary operational challenge is the severe fragmentation of client information. Critical data points are scattered across disconnected systems, including the firm's CRM, email archives, call transcripts, and portfolio management tools. This fragmentation forces her to spend hours manually collating information to prepare for client meetings, which detracts from time that could be spent on high-value strategic advisory. The objective is to transform Sarah's role from a reactive "data gatherer" into a proactive "strategic advisor" who can anticipate client needs at scale by leveraging AI to synthesize a holistic client view.2

#### **1.2 The Data-Driven Portfolio Manager: "David"**

* **Description:** David is a Portfolio Manager tasked with constructing and managing several discretionary model portfolios to meet specific client objectives and risk mandates.2 His daily routine is characterized by the intense consumption and synthesis of vast quantities of market data and research. His single greatest challenge is information overload; actionable signals are often buried within thousands of pages of unstructured documents like broker research reports, earnings call transcripts, and regulatory filings.2 The goal is to democratize quantitative analysis, enabling David to rapidly process unstructured data, correlate it with structured market data, and accelerate his research process from weeks to hours, thereby enhancing his ability to generate alpha.2

#### **1.3 The Proactive Compliance Officer: "Maria"**

* **Description:** Maria is a Compliance Officer responsible for ensuring the firm operates within all legal and ethical standards set by regulatory bodies such as FINRA and the SEC.2 Her primary challenge is the overwhelming volume of communications and transactional data that must be supervised. Traditional compliance processes, which rely on manual, random sampling, are reactive, inefficient, and expose the firm to significant regulatory and reputational risk.2 The objective is to leverage AI to shift the compliance paradigm from a reactive, forensic approach to a proactive, preventative posture. This involves monitoring 100% of communications in near real-time to automatically flag potential violations for investigation, dramatically improving both efficiency and the firm's overall risk management framework.2

#### **1.4 Interconnected Demo Narrative**

The demonstration's narrative is designed to illustrate a cohesive "Intelligent Wealth Platform" where data and insights flow seamlessly between roles, creating a compounding effect of value.2 This interconnected story moves beyond siloed feature demonstrations to showcase a virtuous cycle of data enrichment and collaborative intelligence, which is a core value proposition of the Snowflake AI Data Cloud.1

The narrative unfolds as follows:

1. **Market Event Trigger:** A significant geopolitical event occurs, impacting the global semiconductor supply chain. This event is captured in real-time news feeds ingested into Snowflake.  
2. **Portfolio Manager's Analysis (David):** David, the Portfolio Manager, uses his AI agent, "AnalystAI," to assess the impact. He asks the agent to synthesize all recent broker research and news related to the event and identify companies with high supply chain exposure. AnalystAI uses Cortex Search over the firm's research corpus and news feeds to provide a summary and a list of affected companies.2 David then uses Cortex Analyst to quantify the firm's portfolio-wide exposure to these specific companies. This AI-augmented research process allows him to quickly formulate a new investment thesis and adjust his model portfolios.  
3. **Wealth Manager's Proactive Outreach (Sarah):** The system flags that one of Sarah's key clients, "Sarah Jones," has a concentrated position in one of the affected semiconductor stocks. Sarah's AI agent, "AdvisorAI," proactively alerts her to this risk. AdvisorAI synthesizes the client's portfolio data, the research summary generated by David's agent, and recent communications with the client. Armed with this comprehensive, 360-degree view, Sarah initiates a call with Sarah Jones to discuss the situation and propose a strategic rebalancing, referencing the firm's latest research.  
4. **Compliance Officer's Oversight (Maria):** All electronic communications between Sarah and her client, including the email summary of their call, are ingested into Snowflake. Maria's AI agent, "GuardianAI," continuously monitors this data stream. It uses AI functions to classify the communication, confirming that no promissory language was used and that all risk disclosures were appropriate, ensuring adherence to FINRA Rule 2210\.5 This provides a complete, auditable record of the interaction, demonstrating a proactive and comprehensive compliance posture.

This narrative effectively demonstrates how a single platform enables the Portfolio Manager's analytical work to directly empower the Wealth Manager's client relationship activities, all under the watchful eye of an automated, intelligent compliance function.

### **2.0 Wealth Manager ("Sarah") Use Cases: Enhancing Client Relationships**

The following scenarios detail the step-by-step conversational workflows for the Wealth Manager, Sarah, interacting with her Cortex Agent, "AdvisorAI." Each workflow is designed to have 3-4 steps, showcasing a natural, evolving conversation that solves a specific business problem.

#### **2.1 Scenario: Hyper-Personalized Client Meeting Preparation**

This use case demonstrates how the agent can drastically reduce meeting preparation time from hours to minutes by synthesizing all relevant client information from both structured and unstructured sources.2

* **Step 1: Initial Briefing Request**  
  * **User (Sarah):** "I have a meeting with my client, Sarah Jones, in 30 minutes. Please prepare a full briefing."  
  * **Agent (AdvisorAI) Expected Response:**

```

**Meeting Briefing: Sarah Jones**

**Portfolio Summary:**
*   **Total AUM:** $5.2M
*   **YTD Performance:** +8.5%
*   **Asset Allocation:** 65% Equities, 30% Fixed Income, 5% Alternatives

**Recent Activity & Sentiment (Last 90 Days):**
*   **Overall Sentiment:** Positive.
*   **Key Topics:** Sarah expressed interest in increasing her allocation to sustainable investments (ESG) in an email on May 15th. She also mentioned her daughter, Emily, has just been accepted to university in a call last week.
*   **Action Items:** We have not yet followed up on her ESG inquiry.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Queries the CLIENT\_FINANCIALS\_SV Semantic View to retrieve AUM, performance, and allocation metrics.  
    * **Cortex Search:** Queries the indexed COMMUNICATIONS table to find recent emails and call transcripts for "Sarah Jones," extracting key topics and sentiment.  
* **Step 2: Deeper Dive into Holdings and Market Context**  
  * **User (Sarah):** "That's very helpful. What are her top 5 holdings and have there been any significant news events related to them recently?"  
  * **Agent (AdvisorAI) Expected Response:**

```

**Top 5 Holdings & Related News:**
1.  **AAPL:** Recent product announcements have been met with positive analyst ratings.
2.  **MSFT:** Announced a new multi-billion dollar investment in AI infrastructure.
3.  **NVDA:** Reported earnings that beat expectations, citing strong demand for their AI chips.
4.  **JPM:** CEO commented on macroeconomic uncertainty in a recent conference.
5.  **VGT:** No significant fund-specific news; performance is closely tracking the tech sector.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Queries the CLIENT\_FINANCIALS\_SV Semantic View to retrieve the top 5 holdings by market value.  
    * **Cortex Search:** The agent takes the tickers of the top 5 holdings and executes a search against the indexed NEWS\_FEEDS table (containing data from providers like LSEG or FactSet) to find relevant news from the last 7 days.2  
* **Step 3: Actionable Recommendations and Opportunity Identification**  
  * **User (Sarah):** "Based on her interest in ESG and the mention of her daughter, what should be my key talking points?"  
  * **Agent (AdvisorAI) Expected Response:**

```

**Recommended Talking Points:**
1.  **Acknowledge Tech Performance:** Discuss the strong performance of her tech holdings, particularly NVDA, and its contribution to her YTD returns.
2.  **Address ESG Interest:** Propose a follow-up discussion on her ESG inquiry. Mention that you have identified two highly-rated ESG funds, 'Global Sustainable Leaders Fund (GSLF)' and 'Future Impact Equity Fund (FIEF)', that align with her risk profile.
3.  **Review Education Savings:** The mention of her daughter's university acceptance is an excellent opportunity to review her 529 education savings plan and discuss if contributions should be adjusted.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Queries a PRODUCT\_CATALOG table to find approved ESG funds and cross-references the client's ACCOUNTS table to check for an existing 529 plan.  
    * **Cortex Search:** Queries the RESEARCH\_CORPUS to find internal fact sheets or summaries on the suggested ESG funds.

#### **2.2 Scenario: Proactive Opportunity and Risk Identification**

This use case shows the agent acting as a continuous monitor, surfacing actionable insights based on market events and client data.2

* **Step 1: Proactive Agent Alert**  
  * **User (Sarah):** "Any new opportunities or risks in my book of business today?"  
  * **Agent (AdvisorAI) Expected Response:**

```

**Today's Key Insights:**
*   **Opportunity:** The 'Global Tech Innovators ETF (GTI)' held by 4 of your clients, including James Miller, has dropped 7% this week. This may present a tax-loss harvesting opportunity.
*   **Risk:** A new analyst report has downgraded the 'Energy Select Sector SPDR Fund (XLE)' from 'Buy' to 'Hold'. Your client, Susan Garcia, has a 15% allocation to this fund, which is above her target model's allocation of 10%.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Runs a pre-defined query against the CLIENT\_FINANCIALS\_SV to identify holdings with significant negative price movement (for tax-loss harvesting) and positions that have deviated from their target models.  
    * **Cortex Search:** Scans the indexed RESEARCH\_CORPUS for new analyst reports and cross-references the mentioned securities with client holdings.  
* **Step 2: Investigating the Opportunity**  
  * **User (Sarah):** "Tell me more about the tax-loss harvesting opportunity for James Miller."  
  * **Agent (AdvisorAI) Expected Response:**

```

**Tax-Loss Harvesting Analysis: James Miller**
*   **Holding:** Global Tech Innovators ETF (GTI)
*   **Current Position:** 500 shares
*   **Estimated Unrealized Loss:** -$12,500
*   **Wash Sale Rule:** No purchases of GTI have been made in the last 30 days.
*   **Suggested Replacement:** The 'Future of Technology ETF (FTEC)' is a highly correlated (0.95) replacement ETF that would maintain market exposure.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Queries the CLIENT\_FINANCIALS\_SV to calculate the unrealized gain/loss for the specific position and checks the TRANSACTIONS table for recent purchases to verify wash sale rule compliance. It also queries a SECURITIES\_MASTER table for correlated replacement securities.  
* **Step 3: Drafting Client Communication**  
  * **User (Sarah):** "Draft a brief email to James explaining this opportunity."  
  * **Agent (AdvisorAI) Expected Response:**

```

**Subject: A potential strategy regarding your portfolio**

Hi James,

I hope you're well.

I'm monitoring the recent volatility in the tech sector and noticed an opportunity in your portfolio. The Global Tech Innovators ETF (GTI) has seen a downturn, which may allow us to realize a tax loss of approximately $12,500 to offset potential gains elsewhere.

We could then reinvest the proceeds into a similar fund to maintain your market exposure.

Would you be open to a brief call tomorrow to discuss this strategy?

Best,
Sarah

```

  *   
  * **Tools & Data Accessed:** The agent uses its underlying LLM, fed with the context from the previous steps, to generate a compliant and professional email draft.

#### **2.3 Scenario: Streamlined Onboarding & Suitability**

This use case highlights the use of Document AI to automate the extraction and analysis of data from client onboarding documents.2

* **Step 1: Document Ingestion and Extraction**  
  * **User (Sarah):** "I have a new client questionnaire for John Smith. Please process it and create a client profile." (User uploads a PDF document).  
  * **Agent (AdvisorAI) Expected Response:**

```

Processing the document for John Smith...

**Extracted Information:**
*   **Name:** John Smith
*   **Date of Birth:** 1975-08-20
*   **Stated Risk Tolerance:** Moderate Growth
*   **Investment Horizon:** 20+ years
*   **Primary Goals:** Retirement Savings, Child's Education
*   **Stated Net Worth:** $2.5M

```

  *   
  * **Tools & Data Accessed:** The agent uses a custom tool that calls the AI\_PARSE\_DOCUMENT function to extract text and AI\_EXTRACT with a predefined schema to pull out specific entities from the uploaded PDF.  
* **Step 2: Suitability Analysis**  
  * **User (Sarah):** "Based on his profile, what is the recommended model portfolio?"  
  * **Agent (AdvisorAI) Expected Response:**

```

Based on John Smith's 'Moderate Growth' risk tolerance and long-term investment horizon, the recommended model is the **'Balanced Growth Model'**.

**Asset Allocation:**
*   60% Global Equities
*   35% Fixed Income
*   5% Alternatives

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Takes the extracted risk tolerance and investment horizon as inputs to query a SUITABILITY\_RULES table, which maps client attributes to the firm's approved model portfolios.  
* **Step 3: Identifying Missing Information**  
  * **User (Sarah):** "Is any information missing for full onboarding?"  
  * **Agent (AdvisorAI) Expected Response:**

```

**Onboarding Checklist:**
*   Client Questionnaire: **COMPLETE**
*   Risk Profile Analysis: **COMPLETE**
*   KYC Documentation (Passport/Driver's License): **PENDING**
*   Signed Advisory Agreement: **PENDING**

A request for the pending KYC documents has been drafted and is ready to be sent to John Smith.

```

  *   
  * **Tools & Data Accessed:** The agent compares the extracted information against a required fields list in a CLIENT\_ONBOARDING\_CHECKLIST table and identifies missing items. It then uses its LLM to generate a follow-up communication draft.

### **3.0 Portfolio Manager ("David") Use Cases: Generating Alpha with AI**

These scenarios focus on David, the Portfolio Manager, using his agent, "AnalystAI," to accelerate research and enhance risk analysis by interacting with vast amounts of unstructured data.

#### **3.1 Scenario: AI-Augmented Investment Thesis Generation**

This workflow demonstrates how to compress a multi-week research effort into a matter of hours by automating the analysis and synthesis of a large corpus of research documents.2

* **Step 1: High-Level Theme Discovery**  
  * **User (David):** "I'm building a thesis on AI in healthcare. What are the primary sub-themes identified in our research corpus?"  
  * **Agent (AnalystAI) Expected Response:**

```

Based on an analysis of 2,500+ research documents, the primary sub-themes in AI Healthcare are:

1.  AI-Powered Drug Discovery & Development (Highest frequency)
2.  Predictive Diagnostics & Imaging Analysis
3.  Robotic-Assisted Surgery
4.  Personalized Treatment Plans
5.  Hospital Operations Optimization

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Search:** Queries the metadata of the indexed RESEARCH\_CORPUS. This query does not search the text itself but performs an aggregation on the classification tags (generated during a pre-processing step using AI\_CLASSIFY) that are associated with the query "AI in healthcare."  
* **Step 2: Deeper Dive into a Sub-Theme**  
  * **User (David):** "Interesting. For 'AI-Powered Drug Discovery', summarize the consensus view and identify the top 3 most frequently mentioned public companies."  
  * **Agent (AnalystAI) Expected Response:**

```

**Consensus View on AI in Drug Discovery:** The consensus is highly positive, with most analysts believing AI can drastically reduce drug development timelines and costs. Key challenges cited include data quality for model training and navigating complex regulatory approvals.

**Top 3 Mentioned Companies:**
1.  Recursion Pharmaceuticals (RXRX)
2.  Schrödinger (SDGR)
3.  AbCellera Biologics (ABCL)

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Search:** The agent performs a two-part action. First, it sends a query to find all text chunks in the RESEARCH\_CORPUS tagged with 'Drug Discovery' and passes them to the LLM for summarization. Concurrently, it queries the extracted entity metadata (generated by AI\_EXTRACT) to count the company names that appear most frequently within that same set of text chunks.  
* **Step 3: Pivot from Unstructured to Structured Data**  
  * **User (David):** "Compare the revenue growth and R\&D spend as a percentage of revenue for those three companies over the last 8 quarters."  
  * **Agent (AnalystAI) Expected Response:** The agent generates a table or chart visualizing the requested financial metrics for RXRX, SDGR, and ABCL.  
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Uses the company tickers identified in the previous step to query a FUNDAMENTALS\_DATA table (sourced from a provider like Cybersyn or FactSet) to retrieve the necessary financial statement data and perform the calculations. This demonstrates a seamless pivot from unstructured text analysis to structured quantitative analysis.  
* **Step 4: Document-Specific Extraction**  
  * **User (David):** "Pull the latest earnings call transcript for RXRX and highlight any management commentary on their clinical trial progress."  
  * **Agent (AnalystAI) Expected Response:**

```

**From the RXRX Q2 2025 Transcript:**
*   (Page 4) CEO Chris Gibson: "...we are pleased to announce positive topline data from our Phase 1 study..."
*   (Page 6) CSO: "...our pipeline now has five programs advancing towards Phase 2 trials, a direct result of our AI-driven discovery platform..."

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Search:** Locates the specific document in the RESEARCH\_CORPUS by its title and metadata. Instead of returning the full text, it applies a second LLM prompt to the document's content, instructing it to extract only sentences containing keywords like "clinical trial," "Phase 1," "Phase 2," or "FDA."

#### **3.2 Scenario: Dynamic Risk & Exposure Analysis**

This workflow shows how to query portfolio-wide exposure to complex, non-standard risk factors described in natural language.2

* **Step 1: Natural Language Risk Query**  
  * **User (David):** "What is our firm's total portfolio exposure to companies with significant supply chain dependencies in Southeast Asia, according to recent geopolitical risk reports?"  
  * **Agent (AnalystAI) Expected Response:**

```

Analyzing geopolitical risk reports and cross-referencing with portfolio holdings...

I have identified 12 companies mentioned as having high supply chain risk in Southeast Asia. Our firm's total exposure to these companies across all portfolios is **$127.4M**.

The top 3 holdings by exposure are:
1.  **Company A (TICK):** $35.2M
2.  **Company B (TICK):** $21.8M
3.  **Company C (TICK):** $15.1M

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Search:** First, it queries the indexed RESEARCH\_CORPUS (specifically filtering for documents tagged as 'Geopolitical Risk') to find reports mentioning "Southeast Asia" and "supply chain." It then uses AI\_EXTRACT within the search context to pull out all company names from these documents.  
    * **Cortex Analyst:** The agent then takes the list of extracted company names and uses them as a filter in a query against the CLIENT\_FINANCIALS\_SV to aggregate the total market value of those holdings across all client portfolios.  
* **Step 2: Drill Down into Specific Risk Factors**  
  * **User (David):** "For those 12 companies, summarize the specific risks mentioned in the reports."  
  * **Agent (AnalystAI) Expected Response:**

```

**Summary of Mentioned Risks:**
*   **Company A:** Cited for dependency on a single-source semiconductor fabricator in the region.
*   **Company B:** Mentioned in relation to potential shipping lane disruptions.
*   **Company C:** Highlighted for reliance on raw material suppliers in politically unstable areas.

```

  *   
* ...  
  \`\`\`  
  * **Tools & Data Accessed:**  
    * **Cortex Search:** Re-queries the relevant text chunks from the previous step and uses the LLM to summarize the context surrounding each company's name.  
* **Step 3: Portfolio-Level Impact**  
  * **User (David):** "Which of my model portfolios has the highest concentration in these high-risk companies?"  
  * **Agent (AnalystAI) Expected Response:**

```

The **'Global Technology Leaders'** model portfolio has the highest concentration, with 18.5% of its assets invested in the identified high-risk companies. The 'Global Growth' model is second at 11.2%.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Queries the CLIENT\_FINANCIALS\_SV, filtering for the identified companies and grouping the results by MODEL\_PORTFOLIO\_NAME to calculate the concentration percentage for each.

#### **3.3 Scenario: Automated ESG & Thematic Screening**

This workflow demonstrates screening the investment universe against ESG criteria derived from unstructured company reports.2

* **Step 1: Screening with Unstructured Criteria**  
  * **User (David):** "Screen all companies in the S\&P 500 and identify the top 5 with the most positive sentiment in their latest sustainability reports regarding their carbon neutrality goals."  
  * **Agent (AnalystAI) Expected Response:**

```

Screening S&P 500 sustainability reports...

**Top 5 Companies by Positive Sentiment on Carbon Neutrality:**
1.  Microsoft (MSFT)
2.  Alphabet (GOOGL)
3.  Salesforce (CRM)
4.  Apple (AAPL)
5.  Schneider Electric (SU.PA)

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Search:** The agent searches the indexed RESEARCH\_CORPUS (filtering for document type 'Sustainability Report' and a list of S\&P 500 companies). Within the search, it looks for sections mentioning "carbon neutral" or "net zero." The AI\_SENTIMENT function is applied to these sections, and the results are ranked by the highest positive sentiment score.  
* **Step 2: Extracting Specific Commitments**  
  * **User (David):** "For Microsoft, extract their stated target year for becoming carbon negative."  
  * **Agent (AnalystAI) Expected Response:**

```

According to their latest Corporate Sustainability Report, Microsoft's stated goal is to be **carbon negative by 2030**.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Search:** The agent locates the Microsoft sustainability report and uses AI\_EXTRACT with a specific prompt to find the target year associated with the phrase "carbon negative."  
* **Step 3: Creating a Thematic Watchlist**  
  * **User (David):** "Create a new thematic watchlist named 'Carbon Negative Leaders' with these 5 companies and track their performance against the S\&P 500."  
  * **Agent (AnalystAI) Expected Response:**

```

The 'Carbon Negative Leaders' watchlist has been created. I will begin tracking its performance. You can now ask me for updates on this watchlist at any time.

```

  *   
  * **Tools & Data Accessed:** The agent uses a custom tool (e.g., a stored procedure) to insert the five company tickers into a WATCHLISTS table in the database, associating them with David's user ID.

### **4.0 Compliance Officer ("Maria") Use Cases: Shifting from Reactive to Proactive**

These scenarios detail the workflows for Maria, the Compliance Officer, using her agent, "GuardianAI," to achieve comprehensive surveillance and automate regulatory analysis.

#### **4.1 Scenario: Intelligent Communications Surveillance**

This workflow automates the review of all electronic communications, accurately flagging potential violations of FINRA and SEC rules for human review.2

* **Step 1: Daily High-Risk Review**  
  * **User (Maria):** "Show me all high-risk communications flagged in the last 24 hours."  
  * **Agent (GuardianAI) Expected Response:**

```

**High-Risk Communications (Last 24 Hours):**
*   **Sender:** John Doe (Advisor) | **Recipient:** Client A | **Category:** Promising_Returns
    *   **Snippet:** "...with this investment, you're practically guaranteed to see a 20% return this year..."
*   **Sender:** Jane Smith (Advisor) | **Recipient:** Client B | **Category:** Client_Complaint
    *   **Snippet:** "...I am extremely unhappy with the performance and the fees you have charged me..."
*   **Sender:** Bob Richards (Advisor) | **Recipient:** Prospect C | **Category:** PII_Sharing
    *   **Snippet:** "...here is the social security number for my other client you asked about..."

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Queries the COMMUNICATIONS table. This table is continuously enriched by a background Snowflake task that applies AI\_CLASSIFY (against a custom lexicon of compliance risks like 'Promising\_Returns', 'PII\_Sharing', 'Client\_Complaint') and AI\_SENTIMENT to all new communications, setting a REVIEW\_FLAG \= TRUE on high-risk items.  
* **Step 2: Deep-Dive Investigation**  
  * **User (Maria):** "This is serious. For the communication from Bob Richards, pull up his full communication history with Prospect C and show me his compliance training record for the PII module."  
  * **Agent (GuardianAI) Expected Response:**

```

**Investigation: Bob Richards**

**Conversation History with Prospect C:**
*   [Full transcript or summary of the conversation thread is displayed here]

**Training Record:**
*   **Module:** PII Handling and Data Privacy
*   **Status:** **INCOMPLETE**. Last assigned on March 1st, 2025. Multiple reminders sent.

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Analyst:** Queries the COMMUNICATIONS table for the full conversation history between the two parties.  
    * **Cortex Search:** Queries the indexed HR\_TRAINING\_RECORDS table (a separate data source) to find the specific training module status for "Bob Richards." This demonstrates the agent's ability to orchestrate across different data domains to build a complete picture.  
* **Step 3: Action and Documentation**  
  * **User (Maria):** "Based on this, what is the recommended action, and can you draft a case report?"  
  * **Agent (GuardianAI) Expected Response:**

```

**Recommendation:** Immediate escalation to the Chief Compliance Officer is recommended due to the combination of a direct policy violation (PII sharing) and a failure to complete mandatory training.

**Case Report Draft:**
*   **Case ID:** 2025-00123
*   **Advisor:** Bob Richards
*   **Issue:** Unauthorized sharing of Personally Identifiable Information (PII) in electronic communication.
*   **Violation:** Potential breach of SEC Regulation S-P and firm policy.
*   **Evidence:** Communication log attached.
*   **Aggravating Factor:** Advisor is delinquent on mandatory 'PII Handling' training.

```

  *   
  * **Tools & Data Accessed:** The agent uses its underlying LLM to synthesize the information from the previous steps into a structured report. It may also use Cortex Search to query an indexed INTERNAL\_POLICIES document to reference the specific policy violated.

#### **4.2 Scenario: Automated Regulatory Change Analysis**

This workflow shows the agent helping Maria stay ahead of the constantly changing regulatory landscape.2

* **Step 1: Identifying Impact of New Regulations**  
  * **User (Maria):** "A new FINRA notice on social media communications was just released. Summarize the key changes and identify all our internal policy documents that might be affected."  
  * **Agent (GuardianAI) Expected Response:**

```

**Summary of New FINRA Notice 25-11:**
*   The notice introduces stricter requirements for the supervision of interactive, real-time communications on platforms like X and LinkedIn.
*   It mandates that firms must now capture and review 'likes' and 'shares' of business-related content by associated persons.
*   New guidance is provided on the use of emojis and hyperlinks, which may be considered promissory or misleading.

**Potentially Affected Internal Policies:**
1.  'Social Media Policy for Advisors' (Last updated: 2023)
2.  'Electronic Communications Supervision Procedures' (Last updated: 2022)
3.  'Annual Compliance Training Module'

```

  *   
  * **Tools & Data Accessed:**  
    * **Cortex Search:** The agent first queries the indexed REGULATORY\_FEEDS to find and summarize the new FINRA notice. It then uses keywords from the summary (e.g., "social media," "electronic communications") to search the indexed INTERNAL\_POLICIES corpus to find relevant documents.  
* **Step 2: Redlining and Comparison**  
  * **User (Maria):** "Show me a side-by-side comparison of the old and new guidance on hyperlinks."  
  * **Agent (GuardianAI) Expected Response:** The agent displays a two-column view showing the text from the previous regulatory notice and the new notice, highlighting the changed sentences.  
  * **Tools & Data Accessed:**  
    * **Cortex Search:** Retrieves the relevant sections from both the old and new regulatory documents.  
    * **LLM:** The agent's underlying LLM performs a "diff" on the two text blocks to identify and format the changes for easy comparison.  
* **Step 3: Drafting Policy Updates**  
  * **User (Maria):** "Draft an update to our 'Social Media Policy for Advisors' to incorporate the new guidance on 'likes' and 'shares'."  
  * **Agent (GuardianAI) Expected Response:**

```

**Draft Policy Update (Section 4.5):**

**Current:** "All business-related posts by advisors on approved social media platforms must be pre-approved by a designated principal."

**Suggested Addition:** "Furthermore, any 'like,' 'share,' or 'repost' of content related to financial products or services by an advisor will be considered an endorsement and is subject to the same supervision and record-keeping requirements as original posts. Advisors must submit such interactions for review within 24 hours."

```

  *   
  * **Tools & Data Accessed:** The agent uses the content of the new FINRA notice and the existing policy document as context for its underlying LLM to generate a precise and relevant policy update draft.

## **Part II: High-Level Technical Design**

### **5.0 Unified Data Architecture**

This section provides the foundational data blueprint for the demonstration. The architecture is designed to support all persona workflows with a set of interconnected tables containing both synthetically generated and real-world market data.

#### **5.1 Logical Data Model**

The data model is centered around the CLIENTS entity. A client can have multiple ACCOUNTS, and each account has HOLDINGS and a history of TRANSACTIONS. Advisors and clients interact through COMMUNICATIONS. The firm's investment decisions are informed by RESEARCH\_REPORTS and NEWS\_FEEDS. Compliance is managed by monitoring communications against REGULATORY\_DOCUMENTS and ensuring advisors complete their HR\_TRAINING\_RECORDS.

#### **5.2 Physical Table Schemas (SQL DDL)**

The following CREATE TABLE statements define the physical schema for the demonstration. These should be executed in a dedicated database and schema (e.g., WEALTH\_DEMO.RAW).

SQL

```

-- Core Client and Financial Data (Structured)
CREATE OR REPLACE TABLE CLIENTS (
    CLIENT_ID INT,
    ADVISOR_ID INT,
    FIRST_NAME VARCHAR,
    LAST_NAME VARCHAR,
    EMAIL VARCHAR,
    PHONE VARCHAR,
    ADDRESS VARCHAR,
    CITY VARCHAR,
    STATE VARCHAR,
    ZIP_CODE VARCHAR,
    DATE_OF_BIRTH DATE,
    RISK_TOLERANCE VARCHAR, -- e.g., 'Conservative', 'Moderate', 'Aggressive'
    INVESTMENT_HORIZON VARCHAR, -- e.g., 'Short-term', 'Medium-term', 'Long-term'
    ONBOARDING_DATE DATE
);

CREATE OR REPLACE TABLE ADVISORS (
    ADVISOR_ID INT,
    FIRST_NAME VARCHAR,
    LAST_NAME VARCHAR,
    EMAIL VARCHAR,
    TEAM VARCHAR
);

CREATE OR REPLACE TABLE ACCOUNTS (
    ACCOUNT_ID VARCHAR,
    CLIENT_ID INT,
    ACCOUNT_TYPE VARCHAR, -- e.g., 'Brokerage', 'IRA', '529 Plan'
    MODEL_PORTFOLIO_NAME VARCHAR,
    OPEN_DATE DATE
);

CREATE OR REPLACE TABLE HOLDINGS (
    HOLDING_ID INT,
    ACCOUNT_ID VARCHAR,
    SNAPSHOT_DATE DATE,
    TOP_LEVEL_OPENFIGI_ID VARCHAR,
    TICKER VARCHAR,
    SECURITY_NAME VARCHAR,
    ASSET_CATEGORY VARCHAR,
    QUANTITY NUMBER(38, 5),
    COST_BASIS NUMBER(38, 5),
    MARKET_VALUE NUMBER(38, 5)
);

CREATE OR REPLACE TABLE TRANSACTIONS (
    TRANSACTION_ID VARCHAR,
    ACCOUNT_ID VARCHAR,
    TRANSACTION_DATE TIMESTAMP_NTZ,
    TOP_LEVEL_OPENFIGI_ID VARCHAR,
    TICKER VARCHAR,
    TRANSACTION_TYPE VARCHAR, -- 'Buy', 'Sell'
    QUANTITY NUMBER(38, 5),
    PRICE NUMBER(38, 5),
    TOTAL_AMOUNT NUMBER(38, 5)
);

-- Unstructured and Semi-Structured Data
CREATE OR REPLACE TABLE COMMUNICATIONS (
    COMMUNICATION_ID VARCHAR,
    CLIENT_ID INT,
    ADVISOR_ID INT,
    TIMESTAMP TIMESTAMP_NTZ,
    CHANNEL VARCHAR, -- 'Email', 'Call Transcript', 'SMS'
    SUBJECT VARCHAR, -- For emails
    CONTENT TEXT,
    SENTIMENT NUMBER(3,2),
    REVIEW_FLAG BOOLEAN,
    COMPLIANCE_CATEGORY VARCHAR
);

CREATE OR REPLACE TABLE RESEARCH_CORPUS (
    DOCUMENT_ID VARCHAR,
    DOCUMENT_TITLE VARCHAR,
    SOURCE VARCHAR, -- 'Internal', 'FactSet', 'LSEG'
    PUBLISH_DATE DATE,
    DOCUMENT_TYPE VARCHAR, -- 'Broker Research', 'Earnings Transcript', 'Sustainability Report', 'Geopolitical Risk'
    CONTENT TEXT,
    TAGS ARRAY -- e.g.,
);

CREATE OR REPLACE TABLE NEWS_FEEDS (
    NEWS_ID VARCHAR,
    TICKER VARCHAR,
    PUBLISH_TIMESTAMP TIMESTAMP_NTZ,
    SOURCE VARCHAR, -- 'Reuters', 'Bloomberg', 'FactSet'
    HEADLINE VARCHAR,
    SUMMARY TEXT,
    URL VARCHAR
);

-- Supporting and Reference Data
CREATE OR REPLACE TABLE HR_TRAINING_RECORDS (
    RECORD_ID INT,
    ADVISOR_ID INT,
    MODULE_NAME VARCHAR,
    ASSIGNED_DATE DATE,
    COMPLETION_DATE DATE,
    STATUS VARCHAR -- 'COMPLETE', 'INCOMPLETE'
);

CREATE OR REPLACE TABLE REGULATORY_DOCUMENTS (
    DOC_ID VARCHAR,
    REGULATOR VARCHAR, -- 'FINRA', 'SEC'
    RULE_ID VARCHAR, -- e.g., '2210'
    TITLE VARCHAR,
    PUBLISH_DATE DATE,
    CONTENT TEXT
);

CREATE OR REPLACE TABLE SECURITIES_MASTER (
    TOP_LEVEL_OPENFIGI_ID VARCHAR,
    SECURITY_NAME VARCHAR,
    ISSUER_NAME VARCHAR,
    PRIMARY_TICKER VARCHAR,
    PRIMARY_EXCHANGE_CODE VARCHAR,
    INDUSTRY_SECTOR VARCHAR,
    COUNTRY_OF_DOMICILE VARCHAR,
    ASSET_CATEGORY VARCHAR,
    MARKET_REGION VARCHAR,
    ESG_RATING VARCHAR
);

CREATE OR REPLACE TABLE MARKET_PRICES_DAILY (
    TICKER VARCHAR,
    PRICE_DATE DATE,
    OPEN_PRICE NUMBER(38, 5),
    HIGH_PRICE NUMBER(38, 5),
    LOW_PRICE NUMBER(38, 5),
    CLOSE_PRICE NUMBER(38, 5),
    VOLUME NUMBER(38, 0)
);

CREATE OR REPLACE TABLE SUITABILITY_RULES (
    RULE_ID INT,
    RISK_TOLERANCE VARCHAR,
    INVESTMENT_HORIZON VARCHAR,
    RECOMMENDED_MODEL_PORTFOLIO VARCHAR
);

CREATE OR REPLACE TABLE PRODUCT_CATALOG (
    PRODUCT_ID VARCHAR,
    PRODUCT_NAME VARCHAR,
    TICKER VARCHAR,
    ASSET_CLASS VARCHAR,
    ESG_RATING VARCHAR,
    IS_APPROVED BOOLEAN
);

```

#### **Data Schema Summary**

To provide a clear overview of the data landscape, the following table summarizes the purpose and origin of each key table in the schema. This serves as a quick reference map for understanding the relationships and data flows within the demo environment.

| TABLE\_NAME | DESCRIPTION | KEY\_COLUMNS | DATA\_SOURCE\_TYPE | GENERATION\_METHOD |
| :---- | :---- | :---- | :---- | :---- |
| CLIENTS | Stores profile information for synthetic clients. | CLIENT\_ID, ADVISOR\_ID | Synthetic Structured | Snowpark/Faker |
| ADVISORS | Stores profile information for synthetic advisors. | ADVISOR\_ID | Synthetic Structured | Snowpark/Faker |
| ACCOUNTS | Links clients to their financial accounts. | ACCOUNT\_ID, CLIENT\_ID | Synthetic Structured | Snowpark |
| HOLDINGS | Stores daily portfolio positions for each account. | ACCOUNT\_ID, SNAPSHOT\_DATE | Synthetic Structured | Snowpark/Cybersyn |
| TRANSACTIONS | A log of all buy/sell transactions. | TRANSACTION\_ID, ACCOUNT\_ID | Synthetic Structured | Snowpark |
| COMMUNICATIONS | Stores all client-advisor interactions. | COMMUNICATION\_ID | Synthetic Unstructured | Cortex complete() |
| RESEARCH\_CORPUS | A repository of research documents. | DOCUMENT\_ID | Synthetic Unstructured | Cortex complete() |
| NEWS\_FEEDS | Stores real-time news articles. | NEWS\_ID, TICKER | Synthetic Unstructured | Cortex complete() |
| HR\_TRAINING\_RECORDS | Tracks compliance training for advisors. | ADVISOR\_ID, MODULE\_NAME | Synthetic Structured | Snowpark |
| REGULATORY\_DOCUMENTS | Stores text of FINRA/SEC rules. | DOC\_ID, RULE\_ID | External Unstructured | Manual Upload |
| SECURITIES\_MASTER | Master list of investable securities. | TOP\_LEVEL\_OPENFIGI\_ID | Marketplace | Cybersyn SQL |
| MARKET\_PRICES\_DAILY | Daily historical prices for securities. | TICKER, PRICE\_DATE | Marketplace | Cybersyn SQL |

### **6.0 Synthetic Data Generation Engine**

The success of this demonstration hinges on a rich, realistic, and interconnected dataset. This section details the engine for generating this data, using a configuration-driven approach with Snowpark for Python and Snowflake Cortex.

#### **6.1 Master Configuration File Specification**

A central YAML file, config.yml, will control all data generation parameters. This allows for easy modification of data volumes, date ranges, and model selection without altering the core Python code.

YAML

```

# config.yml
# --- General Parameters ---
num_clients: 100
num_advisors: 5
date_range_start: "2023-01-01"
date_range_end: "2025-06-30"
connection_name: "sfseeurope-mstellwall-aws-us-west3" # Default connection name

# --- Data Generation Specifics ---
avg_accounts_per_client: 2
avg_holdings_per_account: 15
avg_transactions_per_month: 4
avg_communications_per_client: 25

# --- Cortex LLM Configuration ---
cortex_model_name: "llama3.1-70b"
cortex_max_tokens: 4096
cortex_temperature: 0.7

```

#### **6.2 Structured Data Generation: Snowpark Python Logic**

The generation of structured data will be orchestrated by a main Python script (generate\_structured\_data.py) that uses Snowpark DataFrames.

1. **Session Establishment:** The script will establish a Snowpark session using the connection\_name from the config file.  
2. **Securities & Market Data Population:**  
   * The script will first execute the provided Cybersyn SQL queries to populate the SECURITIES\_MASTER and MARKET\_PRICES\_DAILY tables. The list of tickers for the market price query will be derived from a random sample of securities selected for the portfolios.  
3. **Client and Advisor Generation:**  
   * Using the Faker library, generate realistic names, addresses, and contact details for the number of clients and advisors specified in the config file. Create Snowpark DataFrames and save them to the CLIENTS and ADVISORS tables.  
4. **Account and Portfolio Generation:**  
   * Iterate through each client and create a random number of accounts.  
   * For each account, assign a model portfolio (e.g., 'Balanced Growth').  
   * Randomly select securities from SECURITIES\_MASTER to populate the initial holdings for each account as of date\_range\_start.  
5. **Transaction Simulation:**  
   * Simulate a time-series of transactions (buys/sells) for each account from the start date to the end date.  
   * Use the historical price data in MARKET\_PRICES\_DAILY to calculate transaction costs.  
   * Update the holdings table based on these transactions to create a daily snapshot of market value.  
6. **Supporting Data:** Generate simple records for HR\_TRAINING\_RECORDS, SUITABILITY\_RULES, and PRODUCT\_CATALOG.

#### **6.3 Unstructured Data Generation: The Cortex complete Pipeline**

Generating realistic, context-aware unstructured data is the most critical and complex part of the data generation process. It will be handled by a separate script (generate\_unstructured\_data.py) that strictly follows the user-requested 5-step pipeline.

##### **6.3.1 Dynamic Prompt Engineering Framework**

The core of this process is the dynamic creation of prompts that are contextually grounded in the previously generated structured data. This ensures, for example, that an email from a client mentions a stock they actually own.

**Prompt Template Example for Client Email:**

Python

```

def create_client_email_prompt(client, advisor, holdings):
    # Select a random holding and a random communication theme
    random_holding = random.choice(holdings)
    theme = random.choice()
    
    prompt = f"""
    You are an AI assistant generating a realistic email communication for a wealth management demo.
    
    **Instructions:**
    - Write an email from the client to their financial advisor.
    - The email should be consistent with the persona and context provided below.
    - The tone should be natural and reflect the specified sentiment.
    - Do not use placeholders like '[Client Name]'. Use the actual names provided.

    **Context:**
    - **Client Name:** {client} {client}
    - **Advisor Name:** {advisor} {advisor}
    - **Client Persona:** A high-net-worth individual, moderately knowledgeable about finance.
    - **Email Theme:** {theme}
    - **Key Security to Mention:** {random_holding} ({random_holding})
    - **Desired Sentiment:** Neutral to slightly concerned.

    **Email Content:**
    """
    return prompt

```

##### **6.3.2 Snowpark Python Implementation**

The script will implement the following logic:

1. **Generate Dynamic Prompts:**  
   * Read the generated CLIENTS, ADVISORS, and HOLDINGS tables into Snowpark DataFrames.  
   * For each client, loop avg\_communications\_per\_client times.  
   * In each loop, call a prompt generation function (like the one above) to create a unique, context-aware prompt for an email, call transcript, or research report summary.  
   * Create a new Snowpark DataFrame containing columns COMMUNICATION\_ID and PROMPT\_TEXT.  
2. **Store Prompts in a Table:**  
   * Save this DataFrame to a temporary Snowflake table, e.g., TEMP\_PROMPTS.  
3. **Create Snowpark DataFrame on Prompt Table:**  
   * prompts\_df \= session.table('TEMP\_PROMPTS')  
4. **Generate Content with with\_column:**  
   * Use the with\_column method to invoke snowflake.cortex.complete for each row. This parallelizes the LLM calls efficiently within Snowflake.  
5. Python

```

from snowflake.snowpark.functions import col, lit
from snowflake.cortex import Complete

generated_content_df = prompts_df.with_column(
    'GENERATED_CONTENT',
    Complete(
        lit(config['cortex_model_name']), # Model name from config
        col('PROMPT_TEXT')
    )
)

```

8.   
9. **Save to Final Table:**  
   * Select the COMMUNICATION\_ID and the GENERATED\_CONTENT from the resulting DataFrame.  
   * Perform any necessary post-processing (e.g., extracting subject lines).  
   * Join back with the original client/advisor data and save the final, enriched records to the COMMUNICATIONS table.

This same 5-step process will be repeated for generating content for the RESEARCH\_CORPUS and NEWS\_FEEDS tables, using different dynamic prompt templates tailored to those content types.

### **7.0 Snowflake AI Service Configuration**

This section provides the complete, ready-to-execute SQL DDL for all Snowflake AI services required for the demonstration.

#### **7.1 Cortex Analyst Semantic Views (Complete SQL DDL)**

A single, comprehensive Semantic View, CLIENT\_FINANCIALS\_SV, will serve as the primary tool for Cortex Analyst. This view is meticulously crafted to expose complex financial data in simple, business-friendly terms, maximizing the agent's accuracy and reliability.11

SQL

```

CREATE OR REPLACE SEMANTIC VIEW CLIENT_FINANCIALS_SV
    COMMENT='A unified view of client financial data, including profiles, accounts, holdings, and transactions for natural language querying.'
    TABLES(
        LOGICAL_TABLE CLIENTS_LT(SOURCE_TABLE => 'CLIENTS'),
        LOGICAL_TABLE ADVISORS_LT(SOURCE_TABLE => 'ADVISORS'),
        LOGICAL_TABLE ACCOUNTS_LT(SOURCE_TABLE => 'ACCOUNTS'),
        LOGICAL_TABLE HOLDINGS_LT(SOURCE_TABLE => 'HOLDINGS'),
        LOGICAL_TABLE TRANSACTIONS_LT(SOURCE_TABLE => 'TRANSACTIONS'),
        LOGICAL_TABLE SECURITIES_LT(SOURCE_TABLE => 'SECURITIES_MASTER')
    )
    RELATIONSHIPS(
        RELATIONSHIP(TABLES => (ACCOUNTS_LT, CLIENTS_LT) ON ACCOUNTS_LT.CLIENT_ID = CLIENTS_LT.CLIENT_ID),
        RELATIONSHIP(TABLES => (CLIENTS_LT, ADVISORS_LT) ON CLIENTS_LT.ADVISOR_ID = ADVISORS_LT.ADVISOR_ID),
        RELATIONSHIP(TABLES => (HOLDINGS_LT, ACCOUNTS_LT) ON HOLDINGS_LT.ACCOUNT_ID = ACCOUNTS_LT.ACCOUNT_ID),
        RELATIONSHIP(TABLES => (TRANSACTIONS_LT, ACCOUNTS_LT) ON TRANSACTIONS_LT.ACCOUNT_ID = ACCOUNTS_LT.ACCOUNT_ID),
        RELATIONSHIP(TABLES => (HOLDINGS_LT, SECURITIES_LT) ON HOLDINGS_LT.TOP_LEVEL_OPENFIGI_ID = SECURITIES_LT.TOP_LEVEL_OPENFIGI_ID)
    )
    FACTS(
        FACT HOLDINGS_FACTS(
            DIMENSIONS(
                DIMENSION CLIENT_NAME(
                    SOURCE_COLUMN => CLIENTS_LT.FIRST_NAME |

| ' ' |
| CLIENTS_LT.LAST_NAME,
                    COMMENT => 'The full name of the client.',
                    SYNONYMS => ('client', 'customer name', 'investor')
                ),
                DIMENSION CLIENT_ID(
                    SOURCE_COLUMN => CLIENTS_LT.CLIENT_ID,
                    COMMENT => 'Unique identifier for a client.'
                ),
                DIMENSION ADVISOR_NAME(
                    SOURCE_COLUMN => ADVISORS_LT.FIRST_NAME |

| ' ' |
| ADVISORS_LT.LAST_NAME,
                    COMMENT => 'The full name of the financial advisor.',
                    SYNONYMS => ('advisor', 'wealth manager', 'relationship manager')
                ),
                DIMENSION ACCOUNT_TYPE(
                    SOURCE_COLUMN => ACCOUNTS_LT.ACCOUNT_TYPE,
                    COMMENT => 'The type of financial account, such as Brokerage or IRA.',
                    SYNONYMS => ('account type', 'plan type')
                ),
                DIMENSION SECURITY_NAME(
                    SOURCE_COLUMN => HOLDINGS_LT.SECURITY_NAME,
                    COMMENT => 'The name of the security or investment.',
                    SYNONYMS => ('holding', 'investment', 'stock', 'asset name')
                ),
                DIMENSION TICKER(
                    SOURCE_COLUMN => HOLDINGS_LT.TICKER,
                    COMMENT => 'The stock market ticker symbol for the security.',
                    SYNONYMS => ('symbol', 'stock symbol')
                ),
                DIMENSION ASSET_CATEGORY(
                    SOURCE_COLUMN => HOLDINGS_LT.ASSET_CATEGORY,
                    COMMENT => 'The category of the asset, such as Equity, Fixed Income, or ETF.',
                    SYNONYMS => ('asset class', 'investment type')
                ),
                DIMENSION SNAPSHOT_DATE(
                    SOURCE_COLUMN => HOLDINGS_LT.SNAPSHOT_DATE,
                    COMMENT => 'The date for which the holding information is valid.',
                    SYNONYMS => ('date', 'as of date')
                )
            )
            METRICS(
                METRIC TOTAL_AUM(
                    AGGREGATION => SUM(HOLDINGS_LT.MARKET_VALUE),
                    COMMENT => 'Total Assets Under Management, representing the total market value of all holdings.',
                    SYNONYMS => ('AUM', 'assets under management', 'total assets', 'total value', 'portfolio value')
                ),
                METRIC TOTAL_QUANTITY(
                    AGGREGATION => SUM(HOLDINGS_LT.QUANTITY),
                    COMMENT => 'The total number of shares or units held.',
                    SYNONYMS => ('quantity', 'number of shares', 'position size')
                ),
                METRIC NUMBER_OF_CLIENTS(
                    AGGREGATION => COUNT(DISTINCT CLIENTS_LT.CLIENT_ID),
                    COMMENT => 'The total count of unique clients.',
                    SYNONYMS => ('client count', 'number of customers')
                ),
                METRIC NUMBER_OF_HOLDINGS(
                    AGGREGATION => COUNT(DISTINCT HOLDINGS_LT.TICKER),
                    COMMENT => 'The total count of unique securities held.',
                    SYNONYMS => ('holding count', 'number of positions')
                )
            )
        )
    );

```

#### **7.2 Cortex Search Services (Complete SQL DDL)**

Three distinct Cortex Search services will be created, one for each major corpus of unstructured data. This separation allows for more targeted and efficient searching.13

SQL

```

-- Search service for client communications
CREATE OR REPLACE CORTEX SEARCH SERVICE COMMUNICATIONS_SEARCH_SERVICE
    ON CONTENT
    ATTRIBUTES CONTENT_ID, CONTENT_TITLE, ...
    TARGET_LAG = '5 minutes'
    WAREHOUSE = 'DEMO_WH'
AS
(
  SELECT CONTENT, CONTENT_ID, CONTENT_TITLE, ...
  FROM COMMUNICATIONS
)
;

-- Search service for the research corpus
CREATE OR REPLACE CORTEX SEARCH SERVICE RESEARCH_SEARCH_SERVICE
    ON CONTENT
    ATTRIBUTES = DOCUMENT_TITLE, DOCUMENT_SOURCE, PUBLISH_DATE, DOCUMENT_TYPE, DOCUMENT_TAGS
    TARGET_LAG = '5 minutes'
    WAREHOUSE = 'DEMO_WH'
AS
( SELECT DOCUMENT_TITLE, DOCUMENT_SOURCE, PUBLISH_DATE, DOCUMENT_TYPE, DOCUMENT_TAGS, CONTENT ...
  FROM RESEARCH_CORPUS
)
;

-- Search service for regulatory documents
CREATE OR REPLACE CORTEX SEARCH SERVICE REGULATORY_SEARCH_SERVICE
    ON CONTENT
    ATTRIBUTES = REGULATOR, RULE_ID, TITLE, ...
    TARGET_LAG = '5 minutes'
    WAREHOUSE = 'DEMO_WH'
AS 
(
  SELECT REGULATOR, RULE_ID, TITLE, CONTENT, ...
  FROM REGULATORY_DOCUMENTS
)
;

```

#### **7.3 Cortex Agent Definitions**

This section provides the configuration for the three persona-specific agents. The separation of response and planning instructions, along with clear tool descriptions, is critical for effective and predictable agent behavior.14

#### **Cortex Agent Configuration Summary**

| AGENT\_NAME | TARGET\_PERSONA | PRIMARY\_OBJECTIVE | TOOLS\_CONFIGURED |
| :---- | :---- | :---- | :---- |
| AdvisorAI | Wealth Manager | Enhance client engagement and streamline daily workflows. | Cortex Analyst: CLIENT\_FINANCIALS\_SV, Cortex Search: COMMUNICATIONS\_SEARCH\_SERVICE, RESEARCH\_SEARCH\_SERVICE |
| AnalystAI | Portfolio Manager | Accelerate investment research and risk analysis. | Cortex Analyst: CLIENT\_FINANCIALS\_SV, Cortex Search: RESEARCH\_SEARCH\_SERVICE, NEWS\_FEEDS (via custom tool) |
| GuardianAI | Compliance Officer | Automate surveillance and regulatory analysis. | Cortex Analyst: CLIENT\_FINANCIALS\_SV, Cortex Search: COMMUNICATIONS\_SEARCH\_SERVICE, REGULATORY\_SEARCH\_SERVICE, HR\_TRAINING\_RECORDS |

---

**Agent 1: AdvisorAI**

* **Response Instructions:** "You are 'AdvisorAI', a professional and helpful assistant for a Wealth Manager. Your responses should be concise, data-driven, and presented in a clear, easy-to-read format (use markdown like lists and bolding). Never provide financial advice or make promissory statements. Always refer to the data as being 'according to our records.' If you synthesize information from multiple sources, state that clearly."  
* **Planning Instructions:** "When a user asks a question, first determine the type of information required. If the question is about quantitative client data (like AUM, performance, holdings, transactions), you MUST use the 'Cortex\_Analyst\_Client\_Financials' tool. If the question is about unstructured information (like emails, call notes, research reports, or news), you MUST use the appropriate 'Cortex\_Search' tool. For complex questions, you may need to use multiple tools in sequence. For example, first use Cortex Analyst to find a client's holdings, then use Cortex Search to find news about those holdings."  
* **Tool Descriptions:**  
  * **Cortex\_Analyst\_Client\_Financials:** "Use this tool to answer quantitative questions about client financials. It can retrieve data on portfolio value (AUM), performance, asset allocation, top holdings, and transaction history."  
  * **Cortex\_Search\_Communications:** "Use this tool to search the content of past client communications, including emails and call transcripts. It is useful for finding key topics, expressed client interests, or concerns."  
  * **Cortex\_Search\_Research:** "Use this tool to search the firm's internal and third-party research library. It can find analyst reports, fact sheets, and whitepapers on specific securities or investment themes like ESG."

---

**Agent 2: AnalystAI**

* **Response Instructions:** "You are 'AnalystAI', an assistant for a Portfolio Manager. Your responses must be analytical, precise, and objective. When presenting data, use tables where appropriate. Summarize research findings without adding personal opinions. Cite the source of information (e.g., 'According to the Q2 earnings transcript...')."  
* **Planning Instructions:** "Your primary function is to analyze data. For questions about portfolio exposure, holdings, or financial metrics, use the 'Cortex\_Analyst\_Client\_Financials' tool. For questions requiring synthesis of research reports, earnings calls, or news, use the 'Cortex\_Search\_Research' tool. If a user asks a question that requires both, first use the search tool to identify entities (like company names) and then use the analyst tool to query structured data about those entities."  
* **Tool Descriptions:**  
  * **Cortex\_Analyst\_Client\_Financials:** "Use this tool for quantitative analysis of portfolio data. It can calculate firm-wide exposure to specific securities, industries, or regions, and retrieve fundamental financial data for companies."  
  * **Cortex\_Search\_Research:** "Use this tool to perform deep analysis on a large corpus of unstructured documents, including broker research, sustainability reports, and earnings call transcripts. It can be used to identify themes, summarize consensus views, and extract specific data points."

---

**Agent 3: GuardianAI**

* **Response Instructions:** "You are 'GuardianAI', a compliance monitoring assistant. Your tone must be formal and factual. Present findings clearly and without ambiguity. When identifying potential issues, state the facts and reference the potential policy or rule violation. Always recommend review by a human compliance officer."  
* **Planning Instructions:** "Your goal is to surface potential compliance risks. Use the 'Cortex\_Search\_Communications' tool to scan communications for keywords and themes defined in your risk lexicon. Use the 'Cortex\_Search\_Regulatory' tool to find specific rules and regulations. Use the 'Cortex\_Search\_HR' tool to check employee training records. Use the 'Cortex\_Analyst\_Client\_Financials' tool to investigate transaction patterns or account histories related to a flagged communication."  
* **Tool Descriptions:**  
  * **Cortex\_Search\_Communications:** "Use this tool to search and analyze all electronic communications for potential compliance violations, such as promising returns, sharing PII, or client complaints."  
  * **Cortex\_Search\_Regulatory:** "Use this tool to search a knowledge base of FINRA and SEC regulations to find specific rules relevant to an investigation."  
  * **Cortex\_Search\_HR:** "Use this tool to look up the status of an advisor's mandatory compliance training records."  
  * **Cortex\_Analyst\_Client\_Financials:** "Use this tool to retrieve transaction histories or account details to provide context for a compliance investigation."

## **Part III: High-Level Implementation Plan**

This section outlines a logical, phased approach for constructing the demonstration environment, from foundational data setup to final agent testing.

### **8.0 Phase 1: Foundational Environment and Data Population**

This phase focuses on creating the necessary Snowflake objects and populating them with the complete, interconnected dataset.

* **8.1 Snowflake Object and Security Setup:**  
  1. Create a new database: WEALTH\_DEMO.  
  2. Create schemas: RAW for data tables, ANALYTICS for Semantic Views, and AI for Cortex services and agents.  
  3. Create a virtual warehouse: DEMO\_WH, sized appropriately for the data generation workload.  
  4. Create roles: DEMO\_ADMIN (for setup), WEALTH\_MANAGER\_ROLE, PORTFOLIO\_MANAGER\_ROLE, COMPLIANCE\_OFFICER\_ROLE (for demo users). Grant necessary privileges on the objects to these roles.  
* **8.2 Data Generation Script Execution:**  
  1. Configure the config.yml file with the desired data volumes and parameters.  
  2. Set up a Python environment with Snowpark and other required libraries (e.g., Faker).  
  3. Execute the generate\_structured\_data.py script to populate all structured tables, including pulling data from the Cybersyn Marketplace.  
  4. Execute the generate\_unstructured\_data.py script. This will orchestrate the 5-step process of dynamic prompt generation, storage, and execution via snowflake.cortex.complete to populate the COMMUNICATIONS, RESEARCH\_CORPUS, and NEWS\_FEEDS tables.  
* **8.3 Foundational Data Validation:**  
  1. Run COUNT(\*) queries on all tables to ensure they are populated.  
  2. Execute join queries between key tables (e.g., CLIENTS and ACCOUNTS, HOLDINGS and SECURITIES\_MASTER) to verify that relationships are correctly established.  
  3. Select a few sample records from COMMUNICATIONS to manually verify that the generated text is contextually consistent with the structured data for that client.

### **9.0 Phase 2: AI Service and Semantic Layer Deployment**

With the data in place, this phase focuses on deploying the AI and semantic layers that will power the agents.

* **9.1 Cortex Search Service Indexing:**  
  1. Execute the CREATE CORTEX SEARCH SERVICE DDL statements provided in Section 7.2 for all three search services.  
  2. Monitor the indexing status. The initial indexing may take some time depending on the volume of unstructured data.  
  3. Run a test query using the SEARCH\_PREVIEW function for each service to ensure they are returning results (e.g., SELECT snowflake.cortex.search\_preview('COMMUNICATIONS\_SEARCH\_SERVICE', 'ESG')).  
* **9.2 Semantic View Creation and Validation:**  
  1. Execute the CREATE OR REPLACE SEMANTIC VIEW DDL for CLIENT\_FINANCIALS\_SV from Section 7.1.  
  2. Run a test query against the semantic view to validate its structure and relationships, for example: SELECT \* FROM SEMANTIC\_VIEW('CLIENT\_FINANCIALS\_SV') WHERE client\_name \= 'Sarah Jones'.

### **10.0 Phase 3: Agent Configuration and End-to-End Testing**

This final phase involves creating the agents and conducting a full walkthrough of every demonstration scenario.

* **10.1 Agent Creation and Tool Integration:**  
  1. Execute the CREATE AGENT DDL for AdvisorAI, AnalystAI, and GuardianAI, including their response/planning instructions and tool configurations as specified in Section 7.3.  
* **10.2 Full-Scenario Walkthrough and Refinement:**  
  1. Systematically execute every user prompt for every step of all seven scenarios detailed in Sections 2.0, 3.0, and 4.0.  
  2. For each step, verify that the agent's response matches the expected output and that it correctly utilizes the intended tools (Cortex Analyst or Cortex Search).  
  3. If responses are suboptimal, refine the agent's instructions (e.g., make planning instructions more explicit, add synonyms to the Semantic View) and re-test. This iterative refinement is crucial for a polished demonstration.  
* **10.3 Demo Script and Asset Finalization:**  
  1. Once all scenarios are validated, finalize the talking points and narrative script for the live demonstration.  
  2. Prepare any supporting presentation slides or visuals that will accompany the live interaction with the agents. The demonstration is now ready for delivery to wealth management customers.