from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TaskContext:
    """Context manager for task execution and optimization"""
    task_id: str
    task_type: str
    parent_task: Optional[str] = None
    subtasks: List[str] = field(default_factory=list)
    context: Dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    # Track dependencies and artifacts
    dependencies: List[str] = field(default_factory=list)
    artifacts: Dict[str, str] = field(default_factory=dict)
    
    # Track research queries to avoid duplication
    research_queries: Dict[str, dict] = field(default_factory=dict)
    
    def add_research_query(self, query: str, result: dict) -> None:
        """Track research queries to avoid duplicates"""
        self.research_queries[query] = result
    
    def has_research_query(self, query: str) -> bool:
        """Check if a query has already been performed"""
        return query in self.research_queries
    
    def get_research_result(self, query: str) -> Optional[dict]:
        """Get cached research result"""
        return self.research_queries.get(query)
    
    def add_artifact(self, name: str, path: str) -> None:
        """Track generated artifacts"""
        self.artifacts[name] = path
    
    def add_dependency(self, task_id: str) -> None:
        """Track task dependencies"""
        if task_id not in self.dependencies:
            self.dependencies.append(task_id)
    
    def add_subtask(self, task_id: str) -> None:
        """Track subtasks"""
        if task_id not in self.subtasks:
            self.subtasks.append(task_id)

@dataclass
class ProjectContext:
    """Project-level context manager"""
    project_id: str
    tasks: Dict[str, TaskContext] = field(default_factory=dict)
    global_context: Dict = field(default_factory=dict)
    
    def create_task(self, task_type: str, parent_task: Optional[str] = None) -> TaskContext:
        """Create a new task context"""
        task_id = f"{task_type}_{len(self.tasks)}"
        task = TaskContext(task_id=task_id, task_type=task_type, parent_task=parent_task)
        self.tasks[task_id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[TaskContext]:
        """Get task context by ID"""
        return self.tasks.get(task_id)
    
    def get_tasks_by_type(self, task_type: str) -> List[TaskContext]:
        """Get all tasks of a specific type"""
        return [task for task in self.tasks.values() if task.task_type == task_type]
    
    def get_task_chain(self, task_id: str) -> List[TaskContext]:
        """Get the chain of tasks leading to this task"""
        chain = []
        task = self.get_task(task_id)
        while task:
            chain.append(task)
            task = self.get_task(task.parent_task) if task.parent_task else None
        return list(reversed(chain))
    
    def update_global_context(self, updates: Dict) -> None:
        """Update global project context"""
        self.global_context.update(updates)
    
    def get_relevant_context(self, task_id: str) -> Dict:
        """Get relevant context for a task including parent context"""
        context = self.global_context.copy()
        for task in self.get_task_chain(task_id):
            context.update(task.context)
        return context 