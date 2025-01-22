from crewai import Agent, Crew, Task
from crewai_tools import SerperDevTool, FileReadTool, FileWriterTool
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize tools
serper_tool = SerperDevTool()
file_read_tool = FileReadTool()
file_writer_tool = FileWriterTool()

# Create agents
architect = Agent(
    role='Software Architect',
    goal='Design a robust and scalable system architecture',
    backstory='Experienced software architect with expertise in modern web technologies',
    tools=[serper_tool],
    verbose=True
)

senior_engineer = Agent(
    role='Senior Software Engineer',
    goal='Implement high-quality code following best practices',
    backstory='Senior developer with deep expertise in React and Next.js',
    tools=[serper_tool, file_read_tool, file_writer_tool],
    verbose=True
)

# Create tasks
design_task = Task(
    description='Design the system architecture for a modern web application using Next.js, React, and TailwindCSS',
    expected_output='A detailed system architecture document outlining the components, data flow, and technical decisions',
    agent=architect
)

implementation_task = Task(
    description='Implement the core features of the web application following the architectural design',
    expected_output='Working implementation of the core features with clean, well-documented code',
    agent=senior_engineer
)

# Create crew
crew = Crew(
    agents=[architect, senior_engineer],
    tasks=[design_task, implementation_task],
    verbose=True
)

# Start the crew
result = crew.kickoff()
print("\nResults:")
print(result) 