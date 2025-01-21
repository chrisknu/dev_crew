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
        
        # Set up workspace directory
        self.workspace_dir = workspace_dir or os.getenv('DEVCREW_WORKSPACE', os.path.expanduser('~/.devcrew/workspace'))
        os.makedirs(self.workspace_dir, exist_ok=True)
        
        # Set up project directories
        self.project_dir = os.path.join(self.workspace_dir, 'projects', self.project_name)
        self.docs_dir = os.path.join(self.project_dir, 'docs')
        super().__init__()

    def get_docs_dir(self, doc_type: str) -> str:
        """Generate a directory path for documentation"""
        doc_dir = os.path.join(self.docs_dir, doc_type)
        os.makedirs(doc_dir, exist_ok=True)
        return doc_dir

    def get_project_dir(self) -> str:
        """Get the project implementation directory"""
        src_dir = os.path.join(self.project_dir, 'src')
        os.makedirs(src_dir, exist_ok=True)
        return src_dir

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
        output_file = os.path.join(self.get_docs_dir('requirements'), 'project_plan.md')
        return Task(
            description=f"Analyze the following requirements and create a project plan: {self.requirements}",
            expected_output="A detailed project plan with task breakdown and estimates",
            agent=self.project_manager(),
            output_file=output_file
        )

    @task
    def design_architecture(self) -> Task:
        output_file = os.path.join(self.get_docs_dir('architecture'), 'architecture.md')
        return Task(
            description="Based on the project plan from the previous task, create a high-level system architecture",
            expected_output="System architecture document with technology decisions",
            agent=self.architect(),
            context=[self.analyze_requirements()],
            output_file=output_file
        )

    @task
    def create_technical_design(self) -> Task:
        output_file = os.path.join(self.get_docs_dir('technical_design'), 'technical_design.md')
        return Task(
            description="Based on the architecture design, create detailed technical specifications",
            expected_output="Detailed technical design document with implementation specifications",
            agent=self.architect(),
            context=[self.design_architecture()],
            output_file=output_file
        )

    @task
    def implement_solution(self) -> Task:
        output_dir = self.get_project_dir()
        description = """Based on the technical design, implement the solution:

1. Read the framework and setup requirements from the technical design
2. Execute the appropriate setup commands from best_practices.yaml
3. Install required dependencies
4. Set up project structure and configuration
5. Implement core functionality
6. Set up testing infrastructure
7. Configure development tools

Follow these guidelines:
- Use the framework-specific setup commands from best_practices.yaml
- Install only the dependencies required for the chosen framework
- Follow the framework's best practices for project structure
- Implement proper error handling and logging
- Set up appropriate testing infrastructure
- Configure development tools as needed

Save all implementation artifacts in %(dir)s.
Document implementation details in the docs/implementation directory.""" % {'dir': output_dir}

        expected_output = """Successfully implemented solution with:
1. Project scaffolded using specified framework
2. Required dependencies installed
3. Project structure set up according to best practices
4. Testing environment configured
5. Development tools set up

Implementation documentation available in docs/implementation."""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.senior_fullstack_engineer(),
            context=[self.create_technical_design()],
            output_file=os.path.join(self.get_docs_dir('implementation'), 'implementation_summary.md')
        )

    @task
    def test_solution(self) -> Task:
        output_dir = self.get_docs_dir('testing')
        implementation_dir = self.get_project_dir()
        
        description = """Test the implemented application in {}. Create and execute:
1. Unit Tests
2. Integration Tests
3. E2E Tests
4. Test Coverage Analysis

Save all test results and reports in {}.""".format(implementation_dir, output_dir)

        expected_output = """Complete test suite with:
1. Unit test suite with high coverage
2. Integration test suite for all major features
3. E2E tests for critical user journeys
4. Coverage reports meeting minimum requirements
5. Comprehensive test documentation"""

        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.qa_engineer(),
            context=[self.implement_solution()],
            output_file=os.path.join(output_dir, 'test_results.md')
        )

    @task
    def create_documentation(self) -> Task:
        output_file = os.path.join(self.get_docs_dir('documentation'), 'README.md')
        return Task(
            description="Create comprehensive documentation for the solution",
            expected_output="Complete technical documentation",
            agent=self.technical_writer(),
            context=[self.implement_solution(), self.test_solution()],
            output_file=output_file
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