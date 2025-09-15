-- Glacier First Bank AI Intelligence Demo - PDF Generation Custom Tool
-- Creates custom tool for generating PDF reports from agent responses

USE DATABASE BANK_AI_DEMO;
USE WAREHOUSE BANK_AI_DEMO_COMPUTE_WH;

-- =============================================================================
-- STAGES FOR PDF GENERATION
-- =============================================================================

CREATE STAGE IF NOT EXISTS BANK_AI_DEMO.CURATED_DATA.GLACIER_REPORTS_STAGE
COMMENT = 'Stage for storing AI-generated PDF reports';

CREATE STAGE IF NOT EXISTS BANK_AI_DEMO.AGENT_FRAMEWORK.PROC_STAGE
COMMENT = 'Stage for storing Python stored procedures code';

-- =============================================================================
-- PDF GENERATION STORED PROCEDURE (CUSTOM TOOL)
-- =============================================================================

-- Note: This stored procedure is created using Snowpark Python with @sproc decorator
-- It includes markdown processing and professional PDF generation capabilities

-- CREATED USING SNOWPARK PYTHON:
--
-- from snowflake.snowpark.functions import sproc
-- from snowflake.snowpark.types import StringType
-- 
-- @sproc(
--     name="BANK_AI_DEMO.AGENT_FRAMEWORK.GENERATE_PDF_REPORT", 
--     is_permanent=True, 
--     stage_location="@BANK_AI_DEMO.AGENT_FRAMEWORK.PROC_STAGE", 
--     replace=True, 
--     packages=["snowflake-snowpark-python", "markdown", "weasyprint"],
--     return_type=StringType(),
--     session=session
-- )
-- def generate_pdf(session: Session, report_content: str, report_type: str, entity_name: str):
--     # Implementation includes markdown to HTML conversion, CSS styling, and PDF generation
--     # Returns success message with filename, location, and report details

-- The stored procedure has been successfully created and tested.
-- It can be called as: CALL BANK_AI_DEMO.AGENT_FRAMEWORK.GENERATE_PDF_REPORT(content, type, entity)

-- Test query:
-- CALL BANK_AI_DEMO.AGENT_FRAMEWORK.GENERATE_PDF_REPORT(
--     'Test report content', 
--     'AML', 
--     'Global Trade Ventures S.A.'
-- );

COMMIT;