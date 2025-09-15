"""
Glacier First Bank Demo Configuration Manager

Unified configuration management system supporting all phases of the demo
with scalable data generation, configurable market themes, and external
data provider simulation.
"""

import yaml
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class GlacierDemoConfig:
    """Unified configuration manager for Glacier First Bank demo."""
    
    def __init__(self, config_path: str = None, 
                 connection_name: str = None):
        self.config_path = config_path or "config/glacier_demo_config.yaml"
        self.connection_name = connection_name or os.getenv('CONNECTION_NAME')
        self.config = self._load_config()
        self._validate_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with parameter substitution."""
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Parameter substitution
            if self.connection_name:
                config['global']['snowflake']['connection_name'] = self.connection_name
            else:
                config['global']['snowflake']['connection_name'] = config['global']['snowflake']['connection_fallback']
            
            logger.info(f"Configuration loaded from {self.config_path}")
            return config
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in configuration file: {e}")
    
    def get_scale_config(self, scale: str = None) -> Dict[str, int]:
        """Get data generation scale configuration."""
        scale = scale or self.config['data_generation']['default_scale']
        if scale not in self.config['data_generation']['scales']:
            raise ValueError(f"Scale '{scale}' not found in configuration")
        return self.config['data_generation']['scales'][scale]
    
    def get_entity_config(self, entity_key: str) -> Dict[str, Any]:
        """Get specific entity configuration."""
        if entity_key not in self.config['data_generation']['key_entities']:
            raise ValueError(f"Entity key '{entity_key}' not found in configuration")
        return self.config['data_generation']['key_entities'][entity_key]
    
    def get_policy_threshold(self, metric: str) -> Dict[str, Any]:
        """Get policy threshold configuration for specific metric."""
        for category, thresholds in self.config['policy_thresholds'].items():
            if metric in thresholds:
                return thresholds[metric]
        raise ValueError(f"Policy threshold not found for metric: {metric}")
    
    def get_market_themes(self) -> List[Dict[str, Any]]:
        """Get current market themes configuration."""
        return self.config['market_themes']['current_themes']
    
    def get_external_provider(self, provider_type: str) -> Dict[str, Any]:
        """Get external data provider configuration."""
        if provider_type not in self.config['external_data_providers']:
            raise ValueError(f"External provider '{provider_type}' not found in configuration")
        return self.config['external_data_providers'][provider_type]
    
    def get_document_config(self, doc_category: str, doc_type: str) -> Dict[str, Any]:
        """Get document generation configuration."""
        try:
            return self.config['document_generation']['types'][doc_category][doc_type]
        except KeyError:
            raise ValueError(f"Document configuration not found for {doc_category}.{doc_type}")
    
    def get_snowflake_config(self) -> Dict[str, str]:
        """Get Snowflake connection configuration."""
        return self.config['global']['snowflake']
    
    def get_agent_template(self, template_type: str) -> str:
        """Get agent instruction template."""
        if template_type not in self.config['agent_templates']:
            raise ValueError(f"Agent template '{template_type}' not found")
        return self.config['agent_templates'][template_type]
    
    def get_current_phase_config(self) -> Dict[str, Any]:
        """Get configuration for current phase."""
        current_phase = self.config['phases']['current_phase']
        phase_key = f"phase_{current_phase}"
        return self.config['phases'][phase_key]
    
    def get_deployment_config(self, environment: str = "demo") -> Dict[str, Any]:
        """Get deployment configuration for specified environment."""
        if environment not in self.config['deployment']['environments']:
            raise ValueError(f"Environment '{environment}' not found in deployment configuration")
        return self.config['deployment']['environments'][environment]
    
    def _validate_config(self):
        """Validate configuration consistency and completeness."""
        required_sections = [
            'global', 'phases', 'data_generation', 'market_themes',
            'external_data_providers', 'policy_thresholds'
        ]
        
        for section in required_sections:
            if section not in self.config:
                raise ValueError(f"Missing required configuration section: {section}")
        
        # Validate current phase exists
        current_phase = self.config['phases']['current_phase']
        phase_key = f"phase_{current_phase}"
        if phase_key not in self.config['phases']:
            raise ValueError(f"Current phase {current_phase} not defined in configuration")
        
        # Validate default scale exists
        default_scale = self.config['data_generation']['default_scale']
        if default_scale not in self.config['data_generation']['scales']:
            raise ValueError(f"Default scale {default_scale} not defined in scales")
        
        logger.info("Configuration validation completed successfully")


class ConfigValidator:
    """Validates configuration consistency and data generation requirements."""
    
    def __init__(self, config: GlacierDemoConfig):
        self.config = config
        
    def validate_phase_requirements(self, phase: int) -> List[str]:
        """Validate that configuration supports specified phase requirements."""
        errors = []
        
        try:
            phase_config = self.config.config['phases'][f'phase_{phase}']
            
            # Validate scenario support
            for scenario in phase_config['scenarios']:
                if not self._validate_scenario_config(scenario):
                    errors.append(f"Scenario {scenario} missing required configuration")
            
            # Validate data dependencies
            if not self._validate_data_dependencies(phase):
                errors.append(f"Phase {phase} data dependencies not satisfied")
                
        except KeyError:
            errors.append(f"Phase {phase} configuration not found")
            
        return errors
    
    def validate_agent_configuration(self, agent_name: str) -> List[str]:
        """Validate agent configuration completeness."""
        errors = []
        
        # Check semantic view dependencies
        if not self._check_semantic_view_dependencies(agent_name):
            errors.append(f"Agent {agent_name} semantic view dependencies not met")
        
        # Check search service dependencies
        if not self._check_search_service_dependencies(agent_name):
            errors.append(f"Agent {agent_name} search service dependencies not met")
            
        return errors
    
    def validate_policy_thresholds(self) -> List[str]:
        """Validate policy threshold consistency."""
        errors = []
        
        thresholds = self.config.config['policy_thresholds']
        
        for category, metrics in thresholds.items():
            for metric, config in metrics.items():
                if not self._validate_threshold_config(metric, config):
                    errors.append(f"Invalid threshold configuration for {category}.{metric}")
                    
        return errors
    
    def _validate_scenario_config(self, scenario: str) -> bool:
        """Validate scenario has required configuration elements."""
        # This would check for required document types, entity configurations, etc.
        # Implementation depends on specific scenario requirements
        return True
    
    def _validate_data_dependencies(self, phase: int) -> bool:
        """Validate data dependencies for phase."""
        # This would check for required entities, relationships, etc.
        return True
    
    def _check_semantic_view_dependencies(self, agent_name: str) -> bool:
        """Check if required semantic views exist for agent."""
        # This would validate semantic view availability
        return True
    
    def _check_search_service_dependencies(self, agent_name: str) -> bool:
        """Check if required search services exist for agent."""
        # This would validate search service availability
        return True
    
    def _validate_threshold_config(self, metric: str, config: Dict[str, Any]) -> bool:
        """Validate individual threshold configuration."""
        required_fields = ['warning_threshold', 'breach_threshold', 'direction', 'policy_reference']
        return all(field in config for field in required_fields)


def load_config(config_path: str = None, connection_name: str = None) -> GlacierDemoConfig:
    """Convenience function to load configuration."""
    config_path = config_path or "config/glacier_demo_config.yaml"
    return GlacierDemoConfig(config_path, connection_name)


if __name__ == "__main__":
    # Test configuration loading
    try:
        config = load_config()
        print("✅ Configuration loaded successfully")
        print(f"Institution: {config.config['global']['institution_name']}")
        print(f"Current Phase: {config.config['phases']['current_phase']}")
        print(f"Default Scale: {config.get_scale_config()}")
        
        # Test validation
        validator = ConfigValidator(config)
        phase_errors = validator.validate_phase_requirements(1)
        if phase_errors:
            print(f"❌ Phase 1 validation errors: {phase_errors}")
        else:
            print("✅ Phase 1 configuration valid")
            
    except Exception as e:
        print(f"❌ Configuration error: {e}")
