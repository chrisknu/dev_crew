from crewai.tools import BaseTool
from typing import Type, Dict, Any, List
from pydantic import BaseModel, Field
import yaml
import os
import subprocess
from pathlib import Path

class FrameworkSetupInput(BaseModel):
    """Input schema for FrameworkSetup tool."""
    project_dir: str = Field(..., description="Directory where the project should be set up")
    config_path: str = Field(..., description="Path to the best practices config file")

class FrameworkTool(BaseTool):
    name: str = "Framework Setup Tool"
    description: str = (
        "Tool for setting up Next.js projects based on best practices configuration. "
        "Executes setup commands and configures the development environment."
    )
    args_schema: Type[BaseModel] = FrameworkSetupInput

    def _execute_command(self, command: str, cwd: str) -> Dict[str, Any]:
        """Execute a shell command and return the result"""
        try:
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                check=True,
                capture_output=True,
                text=True
            )
            return {
                'status': 'success',
                'output': result.stdout,
                'command': command
            }
        except subprocess.CalledProcessError as e:
            return {
                'status': 'error',
                'error': str(e),
                'output': e.stdout if e.stdout else e.stderr,
                'command': command
            }

    def _setup_nextjs(self, project_dir: str) -> List[Dict[str, Any]]:
        """Set up a Next.js project with all required configurations"""
        results = []
        
        try:
            # Ensure we're using absolute paths
            abs_project_dir = os.path.abspath(project_dir)
            print(f"Setting up Next.js project in: {abs_project_dir}")
            
            # Ensure we're in the project directory
            os.makedirs(abs_project_dir, exist_ok=True)
            
            # Initialize Next.js project with interactive mode disabled
            init_cmd = "npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias '@/*' --no-git --use-npm"
            print(f"Executing command: {init_cmd}")
            results.append(self._execute_command(init_cmd, abs_project_dir))
            
            if results[-1]['status'] == 'error':
                print(f"Error during Next.js initialization: {results[-1]['output']}")
                return results
            
            print("Next.js project initialized successfully")
            
            # Install core dependencies
            core_deps = "@radix-ui/react-icons @radix-ui/themes class-variance-authority clsx tailwind-merge"
            print(f"Installing core dependencies: {core_deps}")
            results.append(self._execute_command(f"npm install {core_deps}", abs_project_dir))
            
            # Install development dependencies
            dev_deps = "@types/node @types/react @types/react-dom @typescript-eslint/eslint-plugin @typescript-eslint/parser prettier prettier-plugin-tailwindcss"
            print(f"Installing dev dependencies: {dev_deps}")
            results.append(self._execute_command(f"npm install -D {dev_deps}", abs_project_dir))
            
            # Install testing dependencies
            test_deps = "jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom"
            print(f"Installing test dependencies: {test_deps}")
            results.append(self._execute_command(f"npm install -D {test_deps}", abs_project_dir))
            
            # Create test setup
            print("Setting up Jest configuration")
            jest_config = """module.exports = {
    testEnvironment: 'jest-environment-jsdom',
    setupFilesAfterEnv: ['<rootDir>/jest.setup.js'],
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/src/$1',
    },
}"""
            
            jest_setup = """import '@testing-library/jest-dom'"""
            
            with open(os.path.join(abs_project_dir, 'jest.config.js'), 'w') as f:
                f.write(jest_config)
                
            with open(os.path.join(abs_project_dir, 'jest.setup.js'), 'w') as f:
                f.write(jest_setup)
            
            # Update package.json scripts
            print("Updating package.json scripts")
            results.append(self._execute_command(
                """npm pkg set scripts.test="jest" scripts.coverage="jest --coverage" """,
                abs_project_dir
            ))
            
            print("Next.js setup completed successfully")
            return results
            
        except Exception as e:
            print(f"Error during Next.js setup: {str(e)}")
            results.append({
                'status': 'error',
                'error': str(e),
                'output': str(e)
            })
            return results

    def _run(self, project_dir: str, config_path: str) -> Dict[str, Any]:
        """
        Set up a Next.js project with all configurations and dependencies.
        
        Args:
            project_dir: Directory where the project should be set up
            config_path: Path to the best practices config file
            
        Returns:
            Dictionary containing setup results
        """
        try:
            print(f"\n=== Starting Next.js Project Setup ===")
            print(f"Project Directory: {project_dir}")
            print(f"Config Path: {config_path}")
            
            results = self._setup_nextjs(project_dir)
            
            # Check if any step failed
            failed_steps = [r for r in results if r['status'] == 'error']
            if failed_steps:
                print("\n=== Setup Failed ===")
                for step in failed_steps:
                    print(f"Error in command: {step['command']}")
                    print(f"Error output: {step['output']}")
                return {
                    'status': 'failed',
                    'error': 'Some setup steps failed',
                    'failed_steps': failed_steps
                }
            
            print("\n=== Setup Completed Successfully ===")
            return {
                'status': 'success',
                'message': 'Next.js project setup completed successfully',
                'steps': results
            }
            
        except Exception as e:
            print(f"\n=== Setup Failed with Exception ===")
            print(f"Error: {str(e)}")
            return {
                'status': 'failed',
                'error': str(e)
            } 