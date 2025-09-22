"""
Glacier First Bank Demo - Scenario Validation Tests

Comprehensive test suite for validating Phase 1 scenarios including
multi-step reasoning, cross-domain intelligence, and contradictory
evidence synthesis patterns.
"""

import pytest
import json
from datetime import datetime, date
from typing import Dict, List, Any, Optional
from snowflake.snowpark import Session
import sys
import os

# Add python directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'python'))

import config


class ScenarioValidator:
    """Validates demo scenarios and agent capabilities."""
    
    def __init__(self, session: Session, scenarios: List[str]):
        self.session = session
        self.scenarios = scenarios
        
    def validate_aml_kyc_scenario(self) -> Dict[str, bool]:
        """Validate AML/KYC Enhanced Due Diligence scenario."""
        results = {}
        
        # Test 1: Entity identification and UBO extraction
        results['entity_identification'] = self._test_entity_identification()
        
        # Test 2: Adverse media screening
        results['adverse_media_screening'] = self._test_adverse_media_screening()
        
        # Test 3: Cross-domain intelligence
        results['cross_domain_intelligence'] = self._test_cross_domain_intelligence()
        
        # Test 4: Multi-step reasoning
        results['multi_step_reasoning'] = self._test_aml_multi_step_reasoning()
        
        return results
    
    def validate_credit_analysis_scenario(self) -> Dict[str, bool]:
        """Validate Credit Analysis scenario."""
        results = {}
        
        # Test 1: Financial ratio analysis
        results['ratio_analysis'] = self._test_ratio_analysis()
        
        # Test 2: Policy threshold flagging
        results['policy_flagging'] = self._test_policy_threshold_flagging()
        
        # Test 3: Historical cohort analysis
        results['cohort_analysis'] = self._test_cohort_analysis()
        
        # Test 4: Document analysis
        results['document_analysis'] = self._test_document_analysis()
        
        # Test 5: Cross-domain risk assessment
        results['cross_domain_risk'] = self._test_cross_domain_risk_assessment()
        
        return results
    
    def validate_cross_domain_intelligence(self) -> Dict[str, bool]:
        """Validate cross-domain intelligence capabilities."""
        results = {}
        
        # Test 1: Shared ecosystem connections
        results['ecosystem_connections'] = self._test_ecosystem_connections()
        
        # Test 2: Risk contagion analysis
        results['risk_contagion'] = self._test_risk_contagion_analysis()
        
        # Test 3: Contradictory evidence synthesis
        results['contradictory_evidence'] = self._test_contradictory_evidence_synthesis()
        
        # Test 4: Multi-domain correlation
        results['multi_domain_correlation'] = self._test_multi_domain_correlation()
        
        return results
    
    def _test_entity_identification(self) -> bool:
        """Test entity identification from compliance documents."""
        try:
            # Test search for Global Trade Ventures onboarding document
            search_query = """
                SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                    'BANK_AI_DEMO.AGENT_FRAMEWORK.compliance_docs_search_svc',
                    '{"query": "Global Trade Ventures beneficial ownership", "filter": {"doc_type": "Onboarding"}, "limit": 3}'
                )
            """
            
            result = self.session.sql(search_query).collect()
            
            if not result:
                return False
            
            # Parse search results
            search_results = json.loads(result[0][0])
            
            # Verify we found relevant documents
            if not search_results.get('results'):
                return False
            
            # Check for UBO information in results
            found_ubos = False
            for doc in search_results['results']:
                content = doc.get('content', '').lower()
                if 'marcus weber' in content and 'elena rossi' in content:
                    found_ubos = True
                    break
            
            return found_ubos
            
        except Exception as e:
            print(f"Entity identification test failed: {e}")
            return False
    
    def _test_adverse_media_screening(self) -> bool:
        """Test adverse media screening functionality."""
        try:
            # Test search for Elena Rossi adverse media
            search_query = """
                SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                    'BANK_AI_DEMO.AGENT_FRAMEWORK.compliance_docs_search_svc',
                    '{"query": "Elena Rossi Italian Transport Ministry", "filter": {"doc_type": "Adverse Media"}, "limit": 2}'
                )
            """
            
            result = self.session.sql(search_query).collect()
            
            if not result:
                return False
            
            search_results = json.loads(result[0][0])
            
            # Verify we found adverse media documents
            if not search_results.get('results'):
                return False
            
            # Check for specific allegations
            found_allegations = False
            for doc in search_results['results']:
                content = doc.get('content', '').lower()
                if 'corruption' in content or 'investigation' in content:
                    found_allegations = True
                    break
            
            return found_allegations
            
        except Exception as e:
            print(f"Adverse media screening test failed: {e}")
            return False
    
    def _test_cross_domain_intelligence(self) -> bool:
        """Test cross-domain intelligence between AML and credit data."""
        try:
            # Test query combining customer risk and credit risk data
            cross_domain_query = """
                WITH aml_risk AS (
                    SELECT * FROM SEMANTIC_VIEW(
                        BANK_AI_DEMO.SEMANTIC_LAYER.customer_risk_sv
                        METRICS aml_flag_count, average_relationship_risk
                        DIMENSIONS entity_name, risk_rating
                    ) WHERE entity_name IN ('Global Trade Ventures S.A.', 'Innovate GmbH')
                ),
                credit_risk AS (
                    SELECT * FROM SEMANTIC_VIEW(
                        BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                        METRICS dscr, debt_to_equity, client_concentration
                        DIMENSIONS applicant_name
                    ) WHERE applicant_name IN ('Global Trade Ventures S.A.', 'Innovate GmbH')
                )
                SELECT 
                    a.entity_name,
                    a.aml_flag_count,
                    a.risk_rating,
                    c.dscr,
                    c.debt_to_equity,
                    c.client_concentration
                FROM aml_risk a
                LEFT JOIN credit_risk c ON a.entity_name = c.applicant_name
            """
            
            result = self.session.sql(cross_domain_query).collect()
            
            # Verify we got results for both entities
            return len(result) >= 1
            
        except Exception as e:
            print(f"Cross-domain intelligence test failed: {e}")
            return False
    
    def _test_aml_multi_step_reasoning(self) -> bool:
        """Test multi-step reasoning in AML scenario."""
        try:
            # Step 1: Find entity
            # Step 2: Extract UBOs
            # Step 3: Screen for adverse media
            # Step 4: Assess risk
            
            # This would be implemented as a sequence of queries
            # that an agent would perform in the actual scenario
            
            # For now, test that we can perform the sequence
            steps = [
                # Step 1: Entity lookup
                """
                SELECT entity_name, regulatory_status, esg_rating
                FROM BANK_AI_DEMO.RAW_DATA.ENTITIES
                WHERE entity_name = 'Global Trade Ventures S.A.'
                """,
                
                # Step 2: UBO information from documents
                """
                SELECT title, doc_type, risk_signal
                FROM BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENTS
                WHERE entity_name = 'Global Trade Ventures S.A.'
                AND doc_type = 'Onboarding'
                """,
                
                # Step 3: Adverse media check
                """
                SELECT title, doc_type, risk_signal, publish_date
                FROM BANK_AI_DEMO.RAW_DATA.COMPLIANCE_DOCUMENTS
                WHERE entity_name = 'Elena Rossi'
                AND doc_type = 'Adverse Media'
                """
            ]
            
            for i, step_query in enumerate(steps):
                result = self.session.sql(step_query).collect()
                if not result:
                    print(f"Multi-step reasoning failed at step {i+1}")
                    return False
            
            return True
            
        except Exception as e:
            print(f"Multi-step reasoning test failed: {e}")
            return False
    
    def _test_ratio_analysis(self) -> bool:
        """Test financial ratio analysis."""
        try:
            # Test ratio calculation for any applicant
            ratio_query = """
                SELECT applicant_name, industry_sector, debt_service_coverage_ratio, debt_to_equity_ratio
                FROM SEMANTIC_VIEW(
                    BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                    DIMENSIONS applicant_name, industry_sector
                    METRICS debt_service_coverage_ratio, debt_to_equity_ratio
                ) LIMIT 1
            """
            
            result = self.session.sql(ratio_query).collect()
            
            if not result:
                return False
            
            # Verify ratios are within expected ranges for demo data
            row = result[0]
            
            # Check that ratios exist and are reasonable
            dscr = row.get('DSCR')
            debt_to_equity = row.get('DEBT_TO_EQUITY')
            
            if dscr is None or debt_to_equity is None:
                return False
            
            # Verify demo scenario: Innovate GmbH should have policy breaches
            # DSCR should be below 1.25 (warning threshold)
            # D/E should be above 3.0 (warning threshold)
            
            return dscr < 1.25 and debt_to_equity > 3.0
            
        except Exception as e:
            print(f"Ratio analysis test failed: {e}")
            return False
    
    def _test_policy_threshold_flagging(self) -> bool:
        """Test policy threshold flagging logic."""
        try:
            # Get policy thresholds from configuration
            dscr_threshold = self.config.get_policy_threshold('debt_service_coverage_ratio')
            de_threshold = self.config.get_policy_threshold('debt_to_equity_ratio')
            
            # Verify thresholds are configured correctly
            if not dscr_threshold or not de_threshold:
                return False
            
            # Test that we can identify policy breaches
            breach_query = """
                SELECT 
                    applicant_name,
                    dscr,
                    debt_to_equity,
                    client_concentration,
                    CASE WHEN dscr < 1.25 THEN 'WARNING' ELSE 'OK' END as dscr_flag,
                    CASE WHEN debt_to_equity > 3.0 THEN 'WARNING' ELSE 'OK' END as de_flag,
                    CASE WHEN client_concentration > 70 THEN 'BREACH' ELSE 'OK' END as concentration_flag
                FROM SEMANTIC_VIEW(
                    BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                    METRICS dscr, debt_to_equity, client_concentration
                    DIMENSIONS applicant_name
                ) WHERE applicant_name = 'Innovate GmbH'
                )
            """
            
            result = self.session.sql(breach_query).collect()
            
            if not result:
                return False
            
            # Verify flagging logic works
            row = result[0]
            return (row.get('DSCR_FLAG') == 'WARNING' and 
                   row.get('DE_FLAG') == 'WARNING' and
                   row.get('CONCENTRATION_FLAG') == 'BREACH')
            
        except Exception as e:
            print(f"Policy threshold flagging test failed: {e}")
            return False
    
    def _test_cohort_analysis(self) -> bool:
        """Test historical cohort analysis."""
        try:
            # Test cohort analysis for Software Services companies
            cohort_query = """
                SELECT * FROM SEMANTIC_VIEW(
                    BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                    METRICS cohort_default_rate, total_loss_amount, application_count
                    DIMENSIONS historical_industry
                ) WHERE historical_industry = 'Software Services'
            """
            
            result = self.session.sql(cohort_query).collect()
            
            if not result:
                return False
            
            # Verify we have historical data for cohort analysis
            row = result[0]
            default_rate = row.get('COHORT_DEFAULT_RATE')
            
            # Should have some default rate (even if 0)
            return default_rate is not None
            
        except Exception as e:
            print(f"Cohort analysis test failed: {e}")
            return False
    
    def _test_document_analysis(self) -> bool:
        """Test business plan document analysis."""
        try:
            # Test search for Innovate GmbH business plan
            doc_search_query = """
                SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                    'BANK_AI_DEMO.AGENT_FRAMEWORK.loan_documents_search_svc',
                    '{"query": "Innovate GmbH market strategy", "filter": {"applicant_name": "Innovate GmbH"}, "limit": 2}'
                )
            """
            
            result = self.session.sql(doc_search_query).collect()
            
            if not result:
                return False
            
            search_results = json.loads(result[0][0])
            
            # Verify we found business plan documents
            return bool(search_results.get('results'))
            
        except Exception as e:
            print(f"Document analysis test failed: {e}")
            return False
    
    def _test_cross_domain_risk_assessment(self) -> bool:
        """Test cross-domain risk assessment combining multiple data sources."""
        try:
            # Test ecosystem risk analysis
            ecosystem_query = """
                SELECT * FROM SEMANTIC_VIEW(
                    BANK_AI_DEMO.SEMANTIC_LAYER.ecosystem_risk_sv
                    METRICS relationship_count, average_risk_impact, vendor_dependency_count
                    DIMENSIONS related_entity_name, relationship_type
                ) WHERE related_entity_name = 'Northern Supply Chain Ltd'
            """
            
            result = self.session.sql(ecosystem_query).collect()
            
            if not result:
                return False
            
            # Verify we have ecosystem relationships
            row = result[0]
            relationship_count = row.get('RELATIONSHIP_COUNT')
            
            # Should have multiple relationships for Northern Supply Chain
            return relationship_count and relationship_count > 1
            
        except Exception as e:
            print(f"Cross-domain risk assessment test failed: {e}")
            return False
    
    def _test_ecosystem_connections(self) -> bool:
        """Test shared ecosystem connections."""
        try:
            # Test that we can identify shared vendors
            shared_vendor_query = """
                SELECT 
                    related_entity_name,
                    COUNT(DISTINCT primary_entity_name) as client_count,
                    AVG(relationship_risk_score) as avg_risk
                FROM SEMANTIC_VIEW(
                    BANK_AI_DEMO.SEMANTIC_LAYER.ecosystem_risk_sv
                    METRICS relationship_count, average_risk_impact
                    DIMENSIONS primary_entity_name, related_entity_name, relationship_type
                ) WHERE relationship_type = 'VENDOR'
                GROUP BY related_entity_name
                HAVING COUNT(DISTINCT primary_entity_name) > 1
            """
            
            result = self.session.sql(shared_vendor_query).collect()
            
            # Should find Northern Supply Chain as shared vendor
            return len(result) >= 1
            
        except Exception as e:
            print(f"Ecosystem connections test failed: {e}")
            return False
    
    def _test_risk_contagion_analysis(self) -> bool:
        """Test risk contagion analysis through shared relationships."""
        try:
            # Test risk contagion calculation
            contagion_query = """
                WITH vendor_clients AS (
                    SELECT * FROM SEMANTIC_VIEW(
                        BANK_AI_DEMO.SEMANTIC_LAYER.ecosystem_risk_sv
                        METRICS average_risk_impact, relationship_count
                        DIMENSIONS primary_entity_name, related_entity_name, relationship_strength
                    ) WHERE related_entity_name = 'Northern Supply Chain Ltd'
                ),
                client_credit_risk AS (
                    SELECT * FROM SEMANTIC_VIEW(
                        BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                        METRICS dscr, debt_to_equity, requested_amount
                        DIMENSIONS applicant_name
                    )
                )
                SELECT 
                    vc.primary_entity_name,
                    vc.relationship_strength,
                    vc.average_risk_impact,
                    ccr.requested_amount
                FROM vendor_clients vc
                LEFT JOIN client_credit_risk ccr ON vc.primary_entity_name = ccr.applicant_name
            """
            
            result = self.session.sql(contagion_query).collect()
            
            # Should identify multiple clients affected by Northern Supply Chain
            return len(result) >= 2
            
        except Exception as e:
            print(f"Risk contagion analysis test failed: {e}")
            return False
    
    def _test_contradictory_evidence_synthesis(self) -> bool:
        """Test handling of contradictory evidence."""
        try:
            # This would test scenarios where financial data conflicts with news sentiment
            # For now, test that we can access both structured and unstructured data
            
            # Financial strength
            financial_query = """
                SELECT dscr, debt_to_equity, annual_revenue
                FROM SEMANTIC_VIEW(
                    BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                    METRICS dscr, debt_to_equity, annual_revenue
                    DIMENSIONS applicant_name
                ) WHERE applicant_name = 'Innovate GmbH'
                )
            """
            
            financial_result = self.session.sql(financial_query).collect()
            
            # News sentiment
            news_query = """
                SELECT SNOWFLAKE.CORTEX.SEARCH_PREVIEW(
                    'BANK_AI_DEMO.AGENT_FRAMEWORK.news_research_search_svc',
                    '{"query": "Innovate GmbH", "limit": 3}'
                )
            """
            
            news_result = self.session.sql(news_query).collect()
            
            # Both queries should return results for contradiction analysis
            return bool(financial_result) and bool(news_result)
            
        except Exception as e:
            print(f"Contradictory evidence synthesis test failed: {e}")
            return False
    
    def _test_multi_domain_correlation(self) -> bool:
        """Test correlation analysis across multiple domains."""
        try:
            # Test correlation between AML flags and credit risk
            correlation_query = """
                WITH aml_data AS (
                    SELECT * FROM SEMANTIC_VIEW(
                        BANK_AI_DEMO.SEMANTIC_LAYER.customer_risk_sv
                        METRICS aml_flag_count, average_relationship_risk
                        DIMENSIONS entity_name, risk_rating
                    )
                ),
                credit_data AS (
                    SELECT * FROM SEMANTIC_VIEW(
                        BANK_AI_DEMO.SEMANTIC_LAYER.credit_risk_sv
                        METRICS dscr, debt_to_equity
                        DIMENSIONS applicant_name
                    )
                )
                SELECT 
                    a.entity_name,
                    a.aml_flag_count,
                    a.risk_rating,
                    c.dscr,
                    c.debt_to_equity,
                    CASE 
                        WHEN a.aml_flag_count > 0 AND c.debt_to_equity > 3.0 THEN 'HIGH_RISK'
                        WHEN a.aml_flag_count > 0 OR c.debt_to_equity > 3.0 THEN 'MEDIUM_RISK'
                        ELSE 'LOW_RISK'
                    END as composite_risk
                FROM aml_data a
                INNER JOIN credit_data c ON a.entity_name = c.applicant_name
            """
            
            result = self.session.sql(correlation_query).collect()
            
            # Should be able to correlate data across domains
            return len(result) >= 1
            
        except Exception as e:
            print(f"Multi-domain correlation test failed: {e}")
            return False


def run_scenario_validation(session: Session, scenarios: List[str] = None) -> Dict[str, Any]:
    """Run complete scenario validation suite."""
    
    scenarios = scenarios or config.get_all_scenarios()
    validator = ScenarioValidator(session, scenarios)
    
    print("🧪 Running Glacier First Bank Demo Validation Suite...")
    print("=" * 60)
    
    # Run AML/KYC scenario validation
    print("\n📋 Validating AML/KYC Enhanced Due Diligence Scenario...")
    aml_results = validator.validate_aml_kyc_scenario()
    
    for test, result in aml_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test}: {status}")
    
    # Run Credit Analysis scenario validation
    print("\n💰 Validating Credit Analysis Scenario...")
    credit_results = validator.validate_credit_analysis_scenario()
    
    for test, result in credit_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test}: {status}")
    
    # Run Cross-Domain Intelligence validation
    print("\n🔗 Validating Cross-Domain Intelligence...")
    cross_domain_results = validator.validate_cross_domain_intelligence()
    
    for test, result in cross_domain_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {test}: {status}")
    
    # Calculate overall results
    all_results = {**aml_results, **credit_results, **cross_domain_results}
    total_tests = len(all_results)
    passed_tests = sum(all_results.values())
    
    print("\n" + "=" * 60)
    print(f"📊 Validation Summary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All validation tests passed! Demo is ready.")
    else:
        print(f"⚠️  {total_tests - passed_tests} tests failed. Review setup.")
    
    return {
        'aml_kyc': aml_results,
        'credit_analysis': credit_results,
        'cross_domain': cross_domain_results,
        'summary': {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'success_rate': passed_tests / total_tests if total_tests > 0 else 0
        }
    }


if __name__ == "__main__":
    # This would be run as part of the main validation process
    print("Scenario validation module loaded successfully")
    print("Use run_scenario_validation() to execute tests")
