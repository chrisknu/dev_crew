from typing import Dict, List, Optional
from crewai.tools import BaseTool
from ..utils.task_context import ProjectContext, TaskContext
from ..utils.task_decomposer import TaskDecomposer, SubTask

class TaskManagementTool(BaseTool):
    """Tool for managing and decomposing tasks"""
    
    def __init__(self, project_context: ProjectContext):
        self.project_context = project_context
        self.decomposer = TaskDecomposer()
        
    def name(self) -> str:
        return "Task Management Tool"
        
    def description(self) -> str:
        return """
        A tool for managing and decomposing tasks. Use this to:
        - Break down complex tasks into smaller subtasks
        - Check for existing research or work
        - Get relevant context from previous tasks
        - Track task dependencies and artifacts
        """
        
    def decompose_task(self, task_type: str, description: str) -> List[SubTask]:
        """Break down a task into smaller subtasks"""
        task_context = self.project_context.create_task(task_type)
        
        if task_type == "research":
            return self.decomposer.decompose_research_task(description, task_context)
        elif task_type == "implementation":
            return self.decomposer.decompose_implementation_task(description, task_context)
        
        return []
        
    def get_task_context(self, task_id: str) -> Dict:
        """Get relevant context for a task"""
        return self.project_context.get_relevant_context(task_id)
        
    def check_existing_research(self, query: str) -> Optional[Dict]:
        """Check if research has already been done"""
        for task in self.project_context.tasks.values():
            if result := task.get_research_result(query):
                return result
        return None
        
    def track_research_result(self, query: str, result: Dict, task_id: str) -> None:
        """Track research results for future reference"""
        task = self.project_context.get_task(task_id)
        if task:
            task.add_research_query(query, result)
            
    def add_artifact(self, task_id: str, name: str, path: str) -> None:
        """Track task artifacts"""
        task = self.project_context.get_task(task_id)
        if task:
            task.add_artifact(name, path)
            
    def get_dependencies(self, task_type: str) -> Dict:
        """Get relevant dependencies for a task type"""
        return self.decomposer.get_task_dependencies(self.project_context, task_type) 