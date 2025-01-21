from crewai.tools import BaseTool
import subprocess
import os
from typing import Optional
import re

class ShellTool(BaseTool):
    name: str = "Shell Command Executor"
    description: str = """Execute shell commands in the specified directory.
    Commands should be specified in the task description with:
    execute_command: <command>
    working_directory: <directory>
    """

    def _run(self, task_description: str) -> str:
        """Execute commands specified in the task description
        
        Args:
            task_description: Task description containing commands to execute
        
        Returns:
            Combined output from all commands
        """
        # Parse commands from task description using a more robust pattern
        command_pattern = r'execute_command:\s*(.*?)[\n\r]+working_directory:\s*(.*?)(?=[\n\r]+|$)'
        commands = re.findall(command_pattern, task_description, re.MULTILINE | re.DOTALL)
        
        if not commands:
            return f"No commands found in task description. Task description received:\n{task_description}"
            
        outputs = []
        for cmd, working_dir in commands:
            try:
                # Clean up command and working directory
                cmd = cmd.strip()
                working_dir = working_dir.strip()
                
                print(f"Executing command: {cmd}")
                print(f"In directory: {working_dir}")
                
                # Create directory if it doesn't exist
                os.makedirs(working_dir, exist_ok=True)
                
                # Store current directory
                original_dir = os.getcwd()
                
                try:
                    # Change to working directory
                    os.chdir(working_dir)
                    
                    # Execute command
                    result = subprocess.run(
                        cmd,
                        shell=True,
                        check=True,
                        capture_output=True,
                        text=True
                    )
                    
                    outputs.append(f"Command '{cmd}' executed successfully in {working_dir}:\n{result.stdout}")
                    
                finally:
                    # Always change back to original directory
                    os.chdir(original_dir)
                    
            except subprocess.CalledProcessError as e:
                error_msg = f"Command '{cmd}' failed in {working_dir}:\n{e.stderr}"
                outputs.append(error_msg)
                return "\n\n".join(outputs)  # Stop on first error
                
            except Exception as e:
                error_msg = f"Error executing '{cmd}' in {working_dir}: {str(e)}"
                outputs.append(error_msg)
                return "\n\n".join(outputs)  # Stop on first error
                
        return "\n\n".join(outputs) 