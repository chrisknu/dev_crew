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

    def _setup_nextjs(self, project_dir: str) -> bool:
        """Set up Next.js project with best practices"""
        try:
            abs_project_dir = os.path.abspath(project_dir)
            print(f"Setting up Next.js project in: {abs_project_dir}")
            
            # Create .gitignore first
            gitignore_content = """
# dependencies
/node_modules
/.pnp
.pnp.js
.yarn/install-state.gz

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
"""
            with open(os.path.join(abs_project_dir, '.gitignore'), 'w') as f:
                f.write(gitignore_content.strip())

            # Clean up existing files but preserve docs
            if os.path.exists(abs_project_dir):
                print("Cleaning up existing directory...")
                for item in os.listdir(abs_project_dir):
                    if item not in ['docs', '.gitignore']:
                        item_path = os.path.join(abs_project_dir, item)
                        if os.path.isfile(item_path):
                            os.remove(item_path)
                        elif os.path.isdir(item_path):
                            import shutil
                            shutil.rmtree(item_path)

            # Initialize Next.js project with all flags to prevent prompts
            init_cmd = (
                "npx create-next-app@latest . "
                "--yes "  # Must be first to skip all prompts
                "--typescript "
                "--tailwind "
                "--eslint "
                "--app "
                "--src-dir "
                "--import-alias '@/*' "
                "--no-git "
                "--use-npm "
                "--js false "
                "--ts true "
                "--tailwind true "
                "--eslint true "
                "--app true "
                "--src-dir true "
                "--import-alias '@/*' "
                "--use-npm true "
                "--no-git true "
                "--experimental-app=false "
                "--template=default "
                "--no-tailwind=false "
                "--customize=false"
            )
            
            # Execute in project directory
            os.chdir(abs_project_dir)
            print("Initializing Next.js project...")
            result = subprocess.run(init_cmd, shell=True, check=True, capture_output=True, text=True)
            print(result.stdout)
            
            # Wait for npm install to complete
            print("Installing dependencies...")
            subprocess.run("npm install", shell=True, check=True, cwd=abs_project_dir)
            
            # Create required directories
            print("Creating project structure...")
            src_dir = os.path.join(abs_project_dir, 'src')
            os.makedirs(os.path.join(src_dir, 'components'), exist_ok=True)
            os.makedirs(os.path.join(src_dir, 'lib'), exist_ok=True)
            os.makedirs(os.path.join(src_dir, 'styles'), exist_ok=True)
            
            # Create best practices file
            print("Creating best practices configuration...")
            best_practices = """
# Next.js 15 Best Practices and Setup Commands

setup_commands:
  - name: "Create Next.js Project"
    command: "npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --import-alias '@/*'"
    description: "Initialize a new Next.js 15 project with TypeScript, Tailwind CSS, ESLint, and App Router"

  - name: "Install Core Dependencies"
    command: "npm install @radix-ui/react-icons @radix-ui/themes class-variance-authority clsx tailwind-merge"
    description: "Install essential UI and utility libraries"

  - name: "Install Development Dependencies"
    command: "npm install -D @types/node @types/react @types/react-dom @typescript-eslint/eslint-plugin @typescript-eslint/parser prettier prettier-plugin-tailwindcss"
    description: "Install development and type dependencies"

coding_standards:
  typescript:
    - "Use strict TypeScript configuration"
    - "Enable all strict type checking options"
    - "Use interface for object types"
    - "Use type for union types and primitives"
    - "Always specify return types for functions"

  react:
    - "Use functional components with hooks"
    - "Implement proper error boundaries"
    - "Use React.Suspense for code splitting"
    - "Implement proper loading states"
    - "Use proper state management patterns"

  nextjs:
    - "Use App Router for routing"
    - "Implement proper metadata"
    - "Use Server Components by default"
    - "Use Client Components when needed"
    - "Implement proper caching strategies"

  tailwind:
    - "Use consistent color palette"
    - "Implement proper responsive design"
    - "Use proper component composition"
    - "Follow utility-first approach"
    - "Use proper theme configuration"

testing:
  setup:
    - name: "Install Testing Dependencies"
      command: "npm install -D jest @testing-library/react @testing-library/jest-dom @testing-library/user-event jest-environment-jsdom"
      description: "Install testing framework and utilities"

  configuration:
    - "Configure Jest for TypeScript"
    - "Set up testing environment"
    - "Configure test coverage thresholds"
    - "Set up test utilities"
    - "Configure test runners"

deployment:
  vercel:
    - "Configure Vercel deployment"
    - "Set up environment variables"
    - "Configure build settings"
    - "Set up preview deployments"
    - "Configure custom domains"

  github:
    - "Set up GitHub Actions"
    - "Configure CI/CD pipeline"
    - "Set up automated testing"
    - "Configure deployment triggers"
    - "Set up security scanning"
"""
            with open(os.path.join(abs_project_dir, 'best_practices.yaml'), 'w') as f:
                f.write(best_practices.strip())
            
            # Verify required files exist
            required_files = [
                'next.config.js',
                '.eslintrc.json',
                'tailwind.config.js',
                'postcss.config.js'
            ]
            
            missing_files = []
            for file in required_files:
                if not os.path.exists(os.path.join(abs_project_dir, file)):
                    missing_files.append(file)
            
            if missing_files:
                print(f"Warning: Missing required files: {', '.join(missing_files)}")
                # Create missing configuration files if needed
                if 'next.config.js' in missing_files:
                    with open(os.path.join(abs_project_dir, 'next.config.js'), 'w') as f:
                        f.write('/** @type {import("next").NextConfig} */\nconst nextConfig = {};\nmodule.exports = nextConfig;\n')
                
                if '.eslintrc.json' in missing_files:
                    with open(os.path.join(abs_project_dir, '.eslintrc.json'), 'w') as f:
                        f.write('{\n  "extends": "next/core-web-vitals"\n}\n')
                
                if 'tailwind.config.js' in missing_files:
                    with open(os.path.join(abs_project_dir, 'tailwind.config.js'), 'w') as f:
                        f.write('/** @type {import("tailwindcss").Config} */\nmodule.exports = {\n  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],\n  theme: {\n    extend: {},\n  },\n  plugins: [],\n};\n')
                
                if 'postcss.config.js' in missing_files:
                    with open(os.path.join(abs_project_dir, 'postcss.config.js'), 'w') as f:
                        f.write('module.exports = {\n  plugins: {\n    tailwindcss: {},\n    autoprefixer: {},\n  },\n};\n')
            
            print("Next.js setup completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"Error setting up Next.js project: {e.stderr}")
            return False
        except Exception as e:
            print(f"Error: {str(e)}")
            return False

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