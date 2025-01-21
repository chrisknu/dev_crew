from typing import List, Dict, Optional
from dataclasses import dataclass
from .task_context import TaskContext, ProjectContext

@dataclass
class SubTask:
    name: str
    description: str
    dependencies: List[str]
    expected_output: str

class TaskDecomposer:
    """Helper class to break down complex tasks into smaller, manageable pieces"""
    
    @staticmethod
    def decompose_research_task(query: str, context: TaskContext) -> List[SubTask]:
        """Break down research tasks to avoid redundant queries"""
        # Check if we already have related research
        if context.has_research_query(query):
            return []
            
        # Break down broad queries into specific aspects
        subtasks = []
        if "Next.js" in query:
            subtasks.extend([
                SubTask(
                    name="core_features",
                    description="Research core features and changes",
                    dependencies=[],
                    expected_output="List of core features and changes"
                ),
                SubTask(
                    name="migration_guide",
                    description="Research migration requirements and steps",
                    dependencies=["core_features"],
                    expected_output="Migration guide and requirements"
                )
            ])
        
        if "authentication" in query.lower():
            subtasks.extend([
                SubTask(
                    name="auth_providers",
                    description="Research available authentication providers",
                    dependencies=[],
                    expected_output="List of supported providers"
                ),
                SubTask(
                    name="auth_implementation",
                    description="Research implementation patterns",
                    dependencies=["auth_providers"],
                    expected_output="Implementation guide"
                )
            ])
            
        return subtasks

    @staticmethod
    def decompose_implementation_task(task: str, context: TaskContext) -> List[SubTask]:
        """Break down implementation tasks into smaller units"""
        subtasks = []
        
        if "API" in task:
            subtasks.extend([
                SubTask(
                    name="api_routes",
                    description="Define API routes and endpoints",
                    dependencies=[],
                    expected_output="API route definitions"
                ),
                SubTask(
                    name="data_models",
                    description="Define data models and schemas",
                    dependencies=[],
                    expected_output="Data model definitions"
                ),
                SubTask(
                    name="controllers",
                    description="Implement API controllers",
                    dependencies=["api_routes", "data_models"],
                    expected_output="Controller implementations"
                )
            ])
            
        if "database" in task.lower():
            subtasks.extend([
                SubTask(
                    name="schema_design",
                    description="Design database schema",
                    dependencies=[],
                    expected_output="Database schema"
                ),
                SubTask(
                    name="migrations",
                    description="Create database migrations",
                    dependencies=["schema_design"],
                    expected_output="Migration files"
                )
            ])
            
        return subtasks

    @staticmethod
    def get_task_dependencies(project_context: ProjectContext, task_type: str) -> Dict:
        """Get relevant dependencies and context for a task type"""
        dependencies = {}
        
        if task_type == "implementation":
            # Get architecture decisions
            arch_tasks = project_context.get_tasks_by_type("architecture")
            if arch_tasks:
                dependencies["architecture"] = arch_tasks[-1].artifacts
            
            # Get technical design
            design_tasks = project_context.get_tasks_by_type("technical_design")
            if design_tasks:
                dependencies["design"] = design_tasks[-1].artifacts
                
        elif task_type == "technical_design":
            # Get architecture decisions
            arch_tasks = project_context.get_tasks_by_type("architecture")
            if arch_tasks:
                dependencies["architecture"] = arch_tasks[-1].artifacts
        
        return dependencies 