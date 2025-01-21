from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os

class FileReadInput(BaseModel):
    """Input schema for FileReadTool."""
    file_path: str = Field(..., description="Path to the file relative to workspace")

class FileWriteInput(BaseModel):
    """Input schema for FileWriteTool."""
    file_path: str = Field(..., description="Path to the file relative to workspace")
    content: str = Field(..., description="Content to write to the file")

class FileTools:
    @staticmethod
    def get_workspace_dir() -> str:
        """Get the current workspace directory"""
        workspace = os.getenv('DEVCREW_WORKSPACE')
        if workspace:
            return os.path.abspath(workspace)
        return os.getcwd()

    @staticmethod
    def normalize_path(file_path: str) -> str:
        """Normalize a file path to be relative to workspace"""
        # Remove any leading slashes
        file_path = file_path.lstrip('/')
        # Remove any ./ or ../ from the beginning
        while file_path.startswith('./') or file_path.startswith('../'):
            file_path = file_path[2:] if file_path.startswith('./') else file_path[3:]
        return file_path

class FileReadTool(BaseTool):
    name: str = "Read File"
    description: str = "Read content from a file relative to workspace"
    args_schema: Type[BaseModel] = FileReadInput

    def _run(self, file_path: str) -> str:
        try:
            # Normalize the path to be relative to workspace
            file_path = FileTools.normalize_path(file_path)
            # Get absolute path by joining with workspace
            full_path = os.path.join(FileTools.get_workspace_dir(), file_path)
            
            if not os.path.exists(full_path):
                return f"Error: File not found at path: {file_path}"
                
            with open(full_path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file {file_path}: {str(e)}"

class FileWriteTool(BaseTool):
    name: str = "Write File"
    description: str = "Write content to a file relative to workspace"
    args_schema: Type[BaseModel] = FileWriteInput

    def _run(self, file_path: str, content: str) -> str:
        try:
            # Normalize the path to be relative to workspace
            file_path = FileTools.normalize_path(file_path)
            # Get absolute path by joining with workspace
            full_path = os.path.join(FileTools.get_workspace_dir(), file_path)
            
            # Create directories if they don't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            with open(full_path, 'w') as f:
                f.write(content)
            return f"Successfully wrote to {file_path}"
        except Exception as e:
            return f"Error writing to file {file_path}: {str(e)}" 