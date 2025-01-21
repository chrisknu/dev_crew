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
    def implement_solution(self) -> Task:
        output_file = 'implementation_summary.md'
        input_file = os.path.join(self.project_name, 'docs/technical_design/technical_design.md')
        output_path = os.path.join(self.get_docs_dir('implementation'), output_file)
        return Task(
            description=f"""First, read and analyze the technical design document from: {input_file}

Then, implement the solution following these steps:

1. Project Setup
   - Initialize the Next.js project with TypeScript and TailwindCSS
   - Set up the project structure according to the technical design
   - Configure development tools and linters

2. Core Implementation
   - Implement the frontend components and pages
   - Set up the API routes and services
   - Configure database connections and models
   - Implement authentication and authorization
   - Set up state management

3. Testing Setup
   - Configure Jest and Testing Library
   - Set up test environment
   - Create initial test suites

4. Build and Deployment
   - Configure build process
   - Set up CI/CD pipeline
   - Configure deployment environments

Save all implementation artifacts in: {os.path.join(self.project_name, 'src')}
Document the implementation details in: {os.path.join(self.project_name, 'docs/implementation', output_file)}""",
            expected_output="""Implementation completed with:
1. Project structure and configuration
2. Core functionality implementation
3. Testing infrastructure
4. Build and deployment setup
5. Implementation documentation""",
            agent=self.senior_fullstack_engineer(),
            context=[{
                "description": "Technical design to implement",
                "expected_output": "Implementation summary",
                "file": input_file
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

    @crew
    def crew(self) -> Crew:
        """Creates the SDLC crew"""
        return Crew(
            agents=self.agents,
            tasks=[
                self.analyze_requirements(),
                self.design_architecture(),
                self.create_technical_design(),
                self.implement_solution(),
                self.test_solution(),
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
        """Clean up after the crew has finished"""
        print("SDLC process completed for project: " + str(self.project_name))
        print("Project artifacts available at: " + str(self.project_dir))