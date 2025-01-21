#!/usr/bin/env python
import sys
import warnings


from dev_crew.crew import DevCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def main():
    # Get requirements from command line argument or use default web app requirements
    requirements = (sys.argv[1] if len(sys.argv) > 1 else
                  """Create a modern web application with the following features:
    - Next.js 15 with App Router using server-first approach
    - Authentication using Supabase Auth
    - PostgreSQL database with Supabase and Drizzle ORM for models/migrations
    - GraphQL API with REST fallback where appropriate
    - TailwindCSS for styling with shadcn/ui components
    - TypeScript throughout with strict type checking
    - Unit and integration tests
    - CI/CD pipeline
    - Server Components as default
    - Edge Runtime where possible
    """)

    # Initialize the development crew with the requirements
    dev_crew = DevCrew(requirements=requirements)

    # Start the SDLC process
    result = dev_crew.crew().kickoff()

    print("\nSDLC Process Results:")
    print("====================")
    for task_result in result:
        print(f"\nTask: {task_result.task.description}")
        print(f"Status: {'Success' if task_result.success else 'Failed'}")
        if not task_result.success:
            print(f"Error: {task_result.error}")

def run():
    """
    Run the SDLC crew with default requirements.
    """
    # Default requirements for a web application project
    requirements = """Create a modern web application with the following features:
    - Next.js 15 with App Router using server-first approach
    - Authentication using Supabase Auth
    - PostgreSQL database with Supabase and Drizzle ORM for models/migrations
    - GraphQL API with REST fallback where appropriate
    - TailwindCSS for styling with shadcn/ui components
    - TypeScript throughout with strict type checking
    - Unit and integration tests
    - CI/CD pipeline
    - Server Components as default
    - Edge Runtime where possible
    """
    
    # Initialize and run the SDLC crew
    dev_crew = DevCrew(
        requirements=requirements,
        project_name="web_app_project"
    )
    
    # Start the SDLC process
    result = dev_crew.crew().kickoff()

    print("\nSDLC Process Results:")
    print("====================")
    for task_result in result:
        print(f"\nTask: {task_result.task.description}")
        print(f"Status: {'Success' if task_result.success else 'Failed'}")
        if not task_result.success:
            print(f"Error: {task_result.error}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    requirements = "Training run for web application development"
    try:
        DevCrew(requirements=requirements).crew().train(
            n_iterations=int(sys.argv[1]), 
            filename=sys.argv[2]
        )

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    requirements = "Replay run for web application development"
    try:
        DevCrew(requirements=requirements).crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    requirements = "Test run for web application development"
    try:
        DevCrew(requirements=requirements).crew().test(
            n_iterations=int(sys.argv[1]), 
            openai_model_name=sys.argv[2]
        )

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    main()
