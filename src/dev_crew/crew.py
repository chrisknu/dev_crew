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
    
    def __init__(self, requirements: str, project_name: str = None):
        """Initialize the crew with requirements and optional project name"""
        self.requirements = requirements
        self.project_name = project_name or f"project_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.project_dir = os.path.join('projects', self.project_name)
        super().__init__()

    def get_task_dir(self, task_name: str) -> str:
        """Generate a directory path for a task"""
        task_dir = os.path.join(self.project_dir, task_name)
        os.makedirs(task_dir, exist_ok=True)
        return task_dir

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
            backstory="Experienced full stack developer with expertise in Next.js, React, and TypeScript",
            verbose=True,
            allow_delegation=True,
            allow_code_execution=True,
            tools=[serper_tool, file_read_tool, file_writer_tool, shell_tool]
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
        output_file = os.path.join(self.get_task_dir('requirements'), 'project_plan.md')
        return Task(
            description=f"Analyze the following requirements and create a project plan: {self.requirements}",
            expected_output="A detailed project plan with task breakdown and estimates",
            agent=self.project_manager(),
            output_file=output_file
        )

    @task
    def design_architecture(self) -> Task:
        output_file = os.path.join(self.get_task_dir('architecture'), 'architecture.md')
        return Task(
            description="Based on the project plan from the previous task, create a high-level system architecture",
            expected_output="System architecture document with technology decisions",
            agent=self.architect(),
            context=[self.analyze_requirements()],
            output_file=output_file
        )

    @task
    def create_technical_design(self) -> Task:
        output_file = os.path.join(self.get_task_dir('technical_design'), 'technical_design.md')
        return Task(
            description="Based on the architecture design, create detailed technical specifications",
            expected_output="Detailed technical design document with implementation specifications",
            agent=self.architect(),
            context=[self.design_architecture()],
            output_file=output_file
        )

    @task
    def implement_solution(self) -> Task:
        output_dir = self.get_task_dir('implementation')
        description = """Execute these commands in sequence to set up the Next.js application:

# Command 1: Initialize Next.js project
execute_command: pnpm dlx create-next-app@latest . --ts --tailwind --eslint --app --src-dir --import-alias "@/*" --use-pnpm --yes
working_directory: %(dir)s

# Command 2: Install core dependencies
execute_command: pnpm add @supabase/supabase-js @supabase/auth-helpers-nextjs drizzle-orm @neondatabase/serverless --yes
working_directory: %(dir)s

# Command 3: Install dev dependencies
execute_command: pnpm add -D drizzle-kit @graphql-codegen/cli @graphql-codegen/typescript --yes
working_directory: %(dir)s

# Command 4: Install GraphQL dependencies
execute_command: pnpm add @graphql-yoga/node graphql --yes
working_directory: %(dir)s

# Command 5: Install and setup UI components
execute_command: pnpm add @shadcn/ui --yes && pnpm dlx shadcn@latest init --yes
working_directory: %(dir)s

# Command 6: Add common UI components
execute_command: pnpm dlx shadcn@latest add button card form input --yes
working_directory: %(dir)s

# Command 7: Setup testing dependencies
execute_command: pnpm add -D jest @testing-library/react @testing-library/jest-dom @types/jest jest-environment-jsdom --yes
working_directory: %(dir)s

# Command 8: Create test directory structure
execute_command: mkdir -p src/__tests__/components src/__tests__/lib src/__tests__/app
working_directory: %(dir)s

# Command 9: Create Jest config
execute_command: echo 'const nextJest = require("next/jest");const createJestConfig = nextJest({dir: "./"});const customJestConfig = {testEnvironment: "jest-environment-jsdom",setupFilesAfterEnv: ["<rootDir>/jest.setup.js"],testMatch: ["**/__tests__/**/*.test.ts?(x)"]};module.exports = createJestConfig(customJestConfig);' > jest.config.js
working_directory: %(dir)s

# Command 10: Create Jest setup
execute_command: echo 'import "@testing-library/jest-dom";' > jest.setup.js
working_directory: %(dir)s

# Command 11: Create example component test
execute_command: echo 'import { render, screen } from "@testing-library/react";import { Button } from "@/components/ui/button";describe("Button", () => {it("renders correctly", () => {render(<Button>Test Button</Button>);expect(screen.getByText("Test Button")).toBeInTheDocument();});});' > src/__tests__/components/button.test.tsx
working_directory: %(dir)s

# Command 12: Create example page test
execute_command: echo 'import { render, screen } from "@testing-library/react";import Page from "@/app/page";describe("Home Page", () => {it("renders correctly", () => {render(<Page />);expect(screen.getByRole("main")).toBeInTheDocument();});});' > src/__tests__/app/page.test.tsx
working_directory: %(dir)s

# Command 13: Add test scripts to package.json
execute_command: npm pkg set scripts.test="jest" scripts.test:watch="jest --watch" scripts.test:coverage="jest --coverage"
working_directory: %(dir)s

After each command completes successfully, proceed to the next one.
If any command fails, report the error and stop execution.

After all commands complete successfully:
1. Configure Supabase and environment variables
2. Set up GraphQL schema and resolvers
3. Create Drizzle schema and migrations
4. Implement auth middleware and components
5. Set up server-side components and routes""" % {'dir': output_dir}

        expected_output = """Successfully created Next.js application in %(dir)s with:
1. Project scaffolded using create-next-app
2. All dependencies installed
3. UI components set up with shadcn/ui
4. Testing environment configured with example tests in src/__tests__/

Verify each command's output in the implementation directory.""" % {'dir': output_dir}

        return Task(
            description=description,
            expected_output=expected_output,
            agent=self.senior_fullstack_engineer(),
            context=[self.create_technical_design()],
            output_file=os.path.join(output_dir, 'implementation_summary.md')
        )

    @task
    def test_solution(self) -> Task:
        output_dir = self.get_task_dir('testing')
        implementation_dir = self.get_task_dir('implementation')
        
        description = """Test the implemented Next.js application in {}. Create and execute:
1. Unit Tests:
- Component tests using React Testing Library
- API route handler tests
- Utility function tests
- Authentication flow tests
- Database operation tests
2. Integration Tests:
- API endpoint integration tests
- Database integration tests
- Authentication flow integration
- Component integration tests
3. E2E Tests:
- User journey tests
- Authentication flows
- Critical business flows
- Error handling scenarios
4. Test Coverage:
- Generate and analyze coverage reports
- Ensure minimum 80% coverage
- Document areas needing additional coverage
Save all test results and reports in {}. Ensure all tests are:
- Properly typed with TypeScript
- Following testing best practices
- Using appropriate mocking strategies
- Including proper error case coverage
Create a comprehensive test report documenting:
- Test strategy and approach
- Test results and metrics
- Coverage analysis
- Identified issues
- Recommendations for improvements""".format(implementation_dir, output_dir)

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
            output_file=os.path.join(output_dir, 'test_results.md'),
            tools=[file_read_tool, file_writer_tool]
        )

    @task
    def create_documentation(self) -> Task:
        output_file = os.path.join(self.get_task_dir('documentation'), 'documentation.md')
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
        
        # Create project directory structure
        os.makedirs(self.project_dir, exist_ok=True)
        
        # Create a project metadata file
        metadata = {
            'project_name': self.project_name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'requirements': self.requirements
        }
        
        with open(os.path.join(self.project_dir, 'project_metadata.md'), 'w') as f:
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