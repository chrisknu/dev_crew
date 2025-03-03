# src/dev_crew/crew.py
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from crewai_tools import (
    SerperDevTool,
    FileReadTool,
    FileWriterTool
)
from crewai import Agent, LLM
from dotenv import load_dotenv
import os
from datetime import datetime
from .tools.shell_tool import ShellTool
from .tools.framework_tool import FrameworkTool

# Load environment variables
load_dotenv()

# Initialize LLM
llm = LLM(api_key=os.getenv('OPENAI_API_KEY'), model='gpt-4o-mini')

# Initialize tools - using them directly as they are already BaseTool instances
serper_tool = SerperDevTool()
file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()
shell_tool = ShellTool()

@CrewBase
class DevCrew():
    """Software Development Lifecycle Crew"""
    
    def __init__(self, requirements: str, project_name: str = None, workspace_dir: str = None):
        """Initialize the crew with requirements and optional project name"""
        self.requirements = requirements
        self.project_name = project_name or f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Set up workspace directory (always absolute)
        if workspace_dir:
            self.workspace_dir = os.path.abspath(workspace_dir)
        else:
            default_workspace = os.getenv('DEVCREW_WORKSPACE')
            if default_workspace:
                self.workspace_dir = os.path.abspath(default_workspace)
            else:
                self.workspace_dir = os.path.abspath(os.path.join(os.getcwd(), 'workspace'))
        
        # Ensure workspace exists
        os.makedirs(self.workspace_dir, exist_ok=True)
        print(f"Using workspace directory: {self.workspace_dir}")
        
        # Set up project directories (relative to workspace)
        self.project_name = project_name or f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.project_dir = os.path.join(self.project_name)
        self.docs_dir = os.path.join(self.project_dir, 'docs')
        self.src_dir = os.path.join(self.project_dir, 'src')
        
        # Create core directories (using absolute paths)
        os.makedirs(os.path.join(self.workspace_dir, self.project_dir), exist_ok=True)
        os.makedirs(os.path.join(self.workspace_dir, self.docs_dir), exist_ok=True)
        os.makedirs(os.path.join(self.workspace_dir, self.src_dir), exist_ok=True)
        
        # Change to workspace directory
        os.chdir(self.workspace_dir)
        
        super().__init__()

    def get_docs_dir(self, doc_type: str) -> str:
        """Generate a directory path for documentation relative to workspace"""
        doc_dir = os.path.join(self.docs_dir, doc_type)
        os.makedirs(doc_dir, exist_ok=True)
        return doc_dir

    def get_project_dir(self) -> str:
        """Get the project implementation directory relative to workspace"""
        return self.src_dir

    def get_absolute_path(self, relative_path: str) -> str:
        """Convert a workspace-relative path to absolute path"""
        return os.path.join(self.workspace_dir, relative_path)

    def get_relative_path(self, absolute_path: str) -> str:
        """Convert an absolute path to workspace-relative path"""
        return os.path.relpath(absolute_path, self.workspace_dir)

    @agent
    def project_manager(self) -> Agent:
        """Project manager agent focused on planning and coordination"""
        return Agent(
            role="Project Manager",
            goal="Ensure project success through effective planning and coordination",
            backstory="Experienced technical project manager with strong background in Agile methodologies",
            verbose=True,
            allow_delegation=True,
            tools=[serper_tool, file_read_tool]
        )

    @agent
    def architect(self) -> Agent:
        """Software architect focused on system design"""
        return Agent(
            role="Software Architect",
            goal="Design scalable and maintainable system architecture with emphasis on simplicity",
            backstory="Senior architect with expertise in modern web architectures and best practices",
            verbose=True,
            allow_delegation=True,
            tools=[serper_tool, file_read_tool]
        )

    @agent
    def senior_fullstack_engineer(self) -> Agent:
        """Senior engineer responsible for implementation"""
        return Agent(
            role="Senior Full Stack Engineer",
            goal="Implement high-quality, production-ready code following best practices",
            backstory="Experienced full stack developer with expertise in modern web development",
            verbose=True,
            allow_delegation=True,
            allow_code_execution=True,
            tools=[
                serper_tool,
                file_read_tool,
                file_writer_tool,
                shell_tool,
                FrameworkTool()
            ]
        )

    @agent
    def qa_engineer(self) -> Agent:
        """QA engineer focused on testing and quality"""
        return Agent(
            role="QA Engineer",
            goal="Ensure code quality through comprehensive testing",
            backstory="Expert in testing methodologies with strong experience in Jest and Testing Library",
            verbose=True,
            allow_delegation=True,
            allow_code_execution=True,
            tools=[file_read_tool, file_writer_tool]
        )

    @agent
    def technical_writer(self) -> Agent:
        """Technical writer focused on documentation"""
        return Agent(
            role="Technical Writer",
            goal="Create clear and comprehensive documentation",
            backstory="Experienced technical writer with strong background in software documentation",
            verbose=True,
            allow_delegation=False,
            tools=[file_read_tool, file_writer_tool, serper_tool]
        )

    @task
    def analyze_requirements(self) -> Task:
        output_file = 'project_plan.md'
        output_path = os.path.join(self.get_docs_dir('requirements'), output_file)
        return Task(
            description=f"Analyze the following requirements and create a project plan: {self.requirements}",
            expected_output="A detailed project plan with task breakdown and estimates",
            agent=self.project_manager(),
            output_file=output_path,
            context=[{
                "description": "Initial project requirements to analyze",
                "expected_output": "Project plan document",
                "content": self.requirements,
                "output_path": os.path.join(self.project_name, 'docs/requirements', output_file)
            }]
        )

    @task
    def design_architecture(self) -> Task:
        output_file = 'architecture.md'
        input_file = os.path.join(self.project_name, 'docs/requirements/project_plan.md')
        output_path = os.path.join(self.get_docs_dir('architecture'), output_file)
        return Task(
            description=f"""First, read and analyze the project plan from: {input_file}

Then, based on the project plan requirements, create a comprehensive system architecture that includes:

1. System Overview
   - High-level architecture diagram
   - Key components and their responsibilities
   - System boundaries and external interfaces

2. Technology Stack
   - Detailed justification for each technology choice
   - Version requirements and compatibility considerations
   - Alternative technologies considered and why they were not chosen

3. Component Architecture
   - Frontend architecture (React/Next.js structure)
   - Backend services and APIs
   - Database design and data models
   - Authentication and authorization flow
   - External service integrations

4. Data Flow
   - Request/response patterns
   - Data processing pipelines
   - State management approach
   - Caching strategy

5. Non-Functional Requirements
   - Scalability approach
   - Performance considerations
   - Security measures
   - Monitoring and observability
   - Disaster recovery strategy

6. Infrastructure
   - Deployment architecture
   - CI/CD pipeline
   - Environment configuration
   - Resource requirements

Follow these guidelines:
- Use clear diagrams (Mermaid.js format) for visual representation
- Provide rationale for architectural decisions
- Address security considerations for each component
- Include error handling and fallback strategies
- Consider future scalability and maintenance

Save the architecture document to: {os.path.join(self.project_name, 'docs/architecture', output_file)}""",
            expected_output="""A comprehensive architecture document that includes:
1. System architecture diagrams
2. Detailed component specifications
3. Technology stack decisions with justifications
4. Security and scalability considerations
5. Infrastructure requirements""",
            agent=self.architect(),
            context=[{
                "description": "Project plan to base architecture on",
                "expected_output": "Architecture design document",
                "file": input_file
            }],
            output_file=output_path
        )

    @task
    def create_technical_design(self) -> Task:
        output_file = 'technical_design.md'
        input_file = os.path.join(self.project_name, 'docs/architecture/architecture.md')
        output_path = os.path.join(self.get_docs_dir('technical_design'), output_file)
        return Task(
            description=f"""First, read and analyze the architecture document from: {input_file}

Then, create a detailed technical design that specifies:

1. Component Implementation Details
   - Frontend component hierarchy and state management
   - API endpoint specifications
   - Database schema and migrations
   - Authentication implementation details
   - Service integration specifications

2. Development Standards
   - Coding conventions
   - Testing requirements
   - Documentation standards
   - Error handling patterns
   - Logging standards

3. Technical Requirements
   - Development environment setup
   - Required dependencies and versions
   - Build and deployment procedures
   - Testing framework configuration
   - CI/CD pipeline specifications

Save the technical design document to: {os.path.join(self.project_name, 'docs/technical_design', output_file)}""",
            expected_output="""A detailed technical design document that includes:
1. Component implementation specifications
2. Development standards and patterns
3. Technical requirements and configurations
4. Testing and deployment procedures""",
            agent=self.architect(),
            context=[{
                "description": "Architecture design to base technical design on",
                "expected_output": "Technical design document",
                "file": input_file
            }],
            output_file=output_path
        )

    @task
    def setup_framework(self) -> Task:
        """Set up the base framework following best practices"""
        best_practices_file = os.path.join(self.project_name, 'best_practices.yaml')
        project_dir = os.path.join(self.workspace_dir, self.project_name)
        
        return Task(
            description=f"""Set up the base framework environment:

1. Initialize Framework
   Use the FrameworkTool to set up the project:
   ```python
   framework_tool = FrameworkTool()
   result = framework_tool._run(
       project_dir="{project_dir}",
       config_path="{best_practices_file}"
   )
   ```

2. Verify Setup
   - Confirm all configuration files are present
   - Verify development dependencies are installed
   - Check testing infrastructure
   - Ensure proper directory structure""",
            expected_output="""Framework setup completed with:
1. Project structure initialized
2. Dependencies installed
3. Development environment configured
4. Testing infrastructure ready""",
            agent=self.senior_fullstack_engineer(),
            context=[{
                "description": "Framework setup",
                "expected_output": "Setup verification",
                "best_practices": self.get_absolute_path(best_practices_file),
                "project_dir": project_dir,
                "framework_setup": {
                    "tool": "FrameworkTool",
                    "args": {
                        "project_dir": project_dir,
                        "config_path": best_practices_file
                    }
                }
            }]
        )

    @task
    def implement_requirements(self) -> Task:
        """Implement the actual project requirements"""
        output_file = 'implementation_summary.md'
        project_plan = os.path.join(self.project_name, 'docs/requirements/project_plan.md')
        tech_design = os.path.join(self.project_name, 'docs/technical_design/technical_design.md')
        architecture = os.path.join(self.project_name, 'docs/architecture/architecture.md')
        output_path = os.path.join(self.get_docs_dir('implementation'), output_file)
        project_dir = os.path.join(self.workspace_dir, self.project_name)
        
        return Task(
            description=f"""Implement the project requirements based on the provided documentation:

1. Review Requirements and Design
   - Project Plan: {project_plan}
   - Technical Design: {tech_design}
   - Architecture: {architecture}

2. Implementation Steps
   a. For each feature in the project plan:
      - Review the technical design for implementation details
      - Follow the architectural patterns specified
      - Implement the feature following best practices
      - Add appropriate tests
      - Document the implementation

   b. Follow these guidelines for each component:
      - Use TypeScript with strict type checking
      - Implement proper error handling
      - Add loading states and feedback
      - Follow the component patterns from technical design
      - Ensure responsive design
      - Add accessibility features
      - Include proper documentation

   c. Integration Requirements:
      - Implement API integrations as specified
      - Set up authentication flows
      - Configure state management
      - Add proper validation
      - Handle edge cases

3. Quality Checks
   - Ensure code follows best practices
   - Add comprehensive test coverage
   - Include error boundaries
   - Implement proper logging
   - Add performance monitoring

4. Documentation
   - Document all implemented features
   - Add inline code documentation
   - Update API documentation
   - Include usage examples
   - Document any deviations from design

Save the implementation summary to: {output_path}

The implementation should match exactly what was specified in the project plan and follow the patterns in the technical design.""",
            expected_output="""Implementation completed with:
1. All features from project plan implemented
2. Components follow technical design
3. Architecture patterns properly applied
4. Tests added for all features
5. Documentation updated""",
            agent=self.senior_fullstack_engineer(),
            context=[{
                "description": "Project implementation",
                "expected_output": "Implementation summary",
                "files": {
                    "project_plan": self.get_absolute_path(project_plan),
                    "technical_design": self.get_absolute_path(tech_design),
                    "architecture": self.get_absolute_path(architecture)
                },
                "project_dir": project_dir,
                "components_dir": os.path.join(project_dir, 'src/components'),
                "lib_dir": os.path.join(project_dir, 'src/lib'),
                "styles_dir": os.path.join(project_dir, 'src/styles')
            }],
            output_file=output_path
        )

    @task
    def test_solution(self) -> Task:
        output_file = 'test_results.md'
        input_dir = os.path.join(self.project_name, 'src')
        input_docs = os.path.join(self.project_name, 'docs/implementation/implementation_summary.md')
        output_path = os.path.join(self.get_docs_dir('testing'), output_file)
        
        return Task(
            description=f"""First, review the implementation details from: {input_docs}
Then, test the implemented application in: {input_dir}

Create and execute the following test suites:

1. Unit Tests
   - Component tests
   - Utility function tests
   - API endpoint tests
   - Database operation tests

2. Integration Tests
   - API integration tests
   - Database integration tests
   - Authentication flow tests
   - State management tests

3. End-to-End Tests
   - Critical user journeys
   - Error handling scenarios
   - Edge cases

4. Performance Tests
   - Load testing
   - API response times
   - Client-side performance

Generate test coverage reports and save all test results in: {os.path.join(self.project_name, 'docs/testing', output_file)}""",
            expected_output="""Complete test suite with:
1. Unit test results
2. Integration test results
3. E2E test results
4. Performance test results
5. Coverage reports""",
            agent=self.qa_engineer(),
            context=[{
                "description": "Implementation to test",
                "expected_output": "Test results and coverage report",
                "src_dir": input_dir,
                "implementation_docs": input_docs
            }],
            output_file=output_path
        )

    @task
    def create_documentation(self) -> Task:
        output_file = 'README.md'
        output_path = os.path.join(self.get_docs_dir('documentation'), output_file)
        input_files = {
            "project_plan": os.path.join(self.project_name, 'docs/requirements/project_plan.md'),
            "architecture": os.path.join(self.project_name, 'docs/architecture/architecture.md'),
            "technical_design": os.path.join(self.project_name, 'docs/technical_design/technical_design.md'),
            "implementation": os.path.join(self.project_name, 'docs/implementation/implementation_summary.md'),
            "test_results": os.path.join(self.project_name, 'docs/testing/test_results.md')
        }
        return Task(
            description=f"""Create comprehensive documentation by reviewing and synthesizing:

1. Project Overview
   - Project Plan: {input_files['project_plan']}
   - Key Features and Requirements
   - Project Timeline and Milestones

2. Technical Documentation
   - Architecture Overview: {input_files['architecture']}
   - Technical Design Details: {input_files['technical_design']}
   - Implementation Notes: {input_files['implementation']}
   - Test Results and Coverage: {input_files['test_results']}

3. User Documentation
   - Installation Instructions
   - Configuration Guide
   - Usage Examples
   - API Documentation

4. Development Guide
   - Setup Instructions
   - Development Workflow
   - Testing Procedures
   - Deployment Process

5. Maintenance Guide
   - Troubleshooting
   - Monitoring
   - Backup and Recovery
   - Security Considerations

Save the complete documentation to: {os.path.join(self.project_name, 'docs/documentation', output_file)}""",
            expected_output="""Complete documentation including:
1. Project overview and requirements
2. Technical architecture and design
3. Implementation details
4. Testing results
5. User and developer guides
6. Maintenance procedures""",
            agent=self.technical_writer(),
            context=[{
                "description": "Project documentation to compile",
                "expected_output": "Complete README documentation",
                "files": input_files
            }],
            output_file=output_path
        )

    def validate_file_exists(self, file_path: str, description: str) -> bool:
        """Validate that a required file exists"""
        full_path = os.path.join(self.workspace_dir, file_path)
        exists = os.path.exists(full_path)
        if not exists:
            print(f"❌ Validation Failed: {description} not found at {file_path}")
        return exists

    def validate_directory_structure(self, directory: str, required_files: list, description: str) -> bool:
        """Validate that a directory contains required files/structure"""
        full_path = os.path.join(self.workspace_dir, directory)
        if not os.path.exists(full_path):
            print(f"❌ Validation Failed: {description} directory not found at {directory}")
            return False
            
        missing_files = []
        for file in required_files:
            if not os.path.exists(os.path.join(full_path, file)):
                missing_files.append(file)
        
        if missing_files:
            print(f"❌ Validation Failed: {description} missing required files: {', '.join(missing_files)}")
            return False
            
        return True

    def validate_project_setup(self) -> bool:
        """Validate the complete project setup"""
        # Define directories to ignore
        ignore_dirs = {'node_modules', '.next', '.git', '__pycache__', '.vscode'}
        
        validations = [
            # Documentation structure
            self.validate_directory_structure(
                os.path.join(self.project_name, 'docs'),
                ['requirements', 'architecture', 'technical_design', 'implementation', 'testing'],
                "Documentation"
            ),
            
            # Project files
            self.validate_file_exists(
                os.path.join(self.project_name, 'best_practices.yaml'),
                "Best practices configuration"
            ),
            
            # Next.js project structure
            self.validate_directory_structure(
                os.path.join(self.project_name, 'src'),
                ['app', 'components', 'lib', 'styles'],
                "Next.js project"
            ),
            
            # Configuration files
            self.validate_directory_structure(
                self.project_name,
                [
                    'package.json',
                    'tsconfig.json',
                    'next.config.js',
                    '.eslintrc.json',
                    'tailwind.config.js',
                    'postcss.config.js'
                ],
                "Project configuration"
            )
        ]
        
        return all(validations)

    @task
    def validate_implementation(self) -> Task:
        """Task to validate the implementation"""
        return Task(
            description=f"""Validate the project implementation in {self.project_name}:

1. Check Project Structure
   - Verify Next.js app directory structure
   - Validate presence of all configuration files
   - Check for required components and utilities

2. Validate Dependencies
   - Verify package.json contains required dependencies
   - Check for proper TypeScript configuration
   - Validate ESLint and Prettier setup

3. Test Configuration
   - Verify Jest setup
   - Check test file structure
   - Validate coverage configuration

4. Documentation Check
   - Verify all documentation sections exist
   - Check for required diagrams
   - Validate API documentation

Report any missing or incorrect items.""",
            expected_output="Validation report detailing any issues found",
            agent=self.qa_engineer(),
            context=[{
                "description": "Project validation",
                "expected_output": "Validation report",
                "project_dir": self.project_name
            }]
        )

    @task
    def review_implementation(self) -> Task:
        """Task to review and provide feedback on implementation"""
        output_file = 'implementation_review.md'
        output_path = os.path.join(self.get_docs_dir('reviews'), output_file)
        
        return Task(
            description=f"""Review the current implementation and provide feedback:

1. Architecture Review
   - Verify alignment with architectural decisions
   - Check component interactions
   - Validate technical patterns

2. Code Quality Review
   - Review code organization
   - Check coding standards compliance
   - Verify error handling
   - Assess performance considerations

3. Implementation Feedback
   - Identify potential improvements
   - Suggest optimizations
   - Note any missing requirements

4. Documentation Review
   - Check documentation completeness
   - Verify API documentation
   - Review code comments

Save the review feedback to: {output_path}""",
            expected_output="""Comprehensive review including:
1. Architecture alignment check
2. Code quality assessment
3. Implementation feedback
4. Documentation review""",
            agent=self.architect(),
            context=[{
                "description": "Implementation review",
                "expected_output": "Review feedback",
                "project_dir": self.project_name
            }],
            output_file=output_path
        )

    @crew
    def crew(self) -> Crew:
        """Creates the SDLC crew with validation and feedback steps"""
        return Crew(
            agents=self.agents,
            tasks=[
                self.analyze_requirements(),
                self.design_architecture(),
                self.create_technical_design(),
                self.setup_framework(),      # Phase 1: Framework Setup
                self.validate_implementation(),
                self.implement_requirements(),# Phase 2: Requirements Implementation
                self.review_implementation(), # New: Implementation Review
                self.test_solution(),
                self.validate_implementation(),
                self.create_documentation()
            ],
            process=Process.sequential,
            verbose=True
        )

    @before_kickoff
    def before_kickoff(self, crew) -> None:
        """Prepare the project environment before starting the crew"""
        print("Starting SDLC process for project: " + str(self.project_name))
        print("Requirements: " + str(self.requirements))
        
        # Create project and docs directory structure
        os.makedirs(self.project_dir, exist_ok=True)
        os.makedirs(self.docs_dir, exist_ok=True)
        
        # Create best practices file
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
        
        # Write best practices file
        with open(os.path.join(self.project_dir, 'best_practices.yaml'), 'w') as f:
            f.write(best_practices)
        
        # Create a project metadata file
        metadata = {
            'project_name': self.project_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'requirements': self.requirements
        }
        
        with open(os.path.join(self.docs_dir, 'metadata.md'), 'w') as f:
            f.write("# Project Metadata\n\n")
            for key, value in metadata.items():
                title = key.replace('_', ' ').title()
                f.write("## " + title + "\n")
                f.write(str(value) + "\n\n")

    @after_kickoff
    def after_kickoff(self, crew) -> None:
        """Clean up and validate after the crew has finished"""
        print("\n=== Validating Project Setup ===")
        if self.validate_project_setup():
            print("✅ Project setup validation passed")
        else:
            print("❌ Project setup validation failed")
            
        print("\n=== SDLC Process Summary ===")
        print("Project: " + str(self.project_name))
        print("Location: " + str(self.project_dir))
        
        # List all generated artifacts (excluding node_modules and other build directories)
        ignore_dirs = {'node_modules', '.next', '.git', '__pycache__', '.vscode'}
        print("\nGenerated Artifacts:")
        for root, dirs, files in os.walk(os.path.join(self.workspace_dir, self.project_name)):
            # Remove ignored directories from dirs list to prevent walking into them
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            
            level = root.replace(os.path.join(self.workspace_dir, self.project_name), '').count(os.sep)
            indent = ' ' * 4 * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print(f"{subindent}{f}")