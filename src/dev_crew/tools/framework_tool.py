from crewai.tools import BaseTool
from typing import Type, Dict, Any
from pydantic import BaseModel, Field
import yaml
import os
from pathlib import Path

class FrameworkSetupInput(BaseModel):
    """Input schema for FrameworkSetup tool."""
    framework: str = Field(..., description="Name of the framework to set up (e.g., 'nextjs', 'fastapi')")
    config_path: str = Field(default="src/dev_crew/config/best_practices.yaml", description="Path to the best practices config file")

class FrameworkTool(BaseTool):
    name: str = "Framework Setup Tool"
    description: str = (
        "Tool for setting up project frameworks based on best practices configuration. "
        "Uses the best_practices.yaml file to determine setup steps and dependencies."
    )
    args_schema: Type[BaseModel] = FrameworkSetupInput

    def _resolve_config_path(self, config_path: str) -> str:
        """
        Resolve the configuration file path.
        Tries multiple possible locations to find the config file.
        """
        possible_paths = [
            config_path,  # Try direct path first
            os.path.join(os.getcwd(), config_path),  # Try from current working directory
            os.path.join(os.path.dirname(__file__), '..', 'config', 'best_practices.yaml'),  # Try relative to tool location
            os.path.join(os.path.dirname(__file__), '../../..', config_path)  # Try from project root
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        raise FileNotFoundError(f"Could not find configuration file in any of: {possible_paths}")

    def _run(self, framework: str, config_path: str = "config/best_practices.yaml") -> Dict[Any, Any]:
        """
        Get framework-specific setup instructions and configuration.
        
        Args:
            framework: Name of the framework to set up
            config_path: Path to the best practices config file
            
        Returns:
            Dictionary containing setup instructions and configuration
        """
        try:
            # Resolve the actual config file path
            resolved_path = self._resolve_config_path(config_path)
            
            # Load best practices configuration
            with open(resolved_path, 'r') as f:
                config = yaml.safe_load(f)
            
            # Get framework-specific configuration
            if framework not in config.get('frameworks', {}):
                raise ValueError(f"Framework '{framework}' not found in configuration")
            
            framework_config = config['frameworks'][framework]
            
            # Add general patterns and best practices
            framework_config.update({
                'patterns': config.get('patterns', {}),
                'security': config.get('security', [])
            })
            
            return framework_config
            
        except Exception as e:
            return {
                'error': str(e),
                'status': 'failed',
                'attempted_path': config_path,
                'resolved_path': resolved_path if 'resolved_path' in locals() else None
            } 