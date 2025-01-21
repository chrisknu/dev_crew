from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import uuid
import asyncio
from datetime import datetime
import os
import logging
from ..crew import DevCrew

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="DevCrew API",
    description="API for automated software development lifecycle management",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store project status and tasks
projects = {}
running_tasks = {}

class ProjectRequest(BaseModel):
    requirements: str
    project_name: Optional[str] = None
    timeout: Optional[int] = 3600  # Default 1 hour timeout

class ProjectStatus(BaseModel):
    project_id: str
    status: str
    current_task: Optional[str] = None
    progress: Optional[float] = None
    artifacts_path: Optional[str] = None
    error: Optional[str] = None
    tasks_completed: Optional[List[str]] = None
    created_at: str
    updated_at: str

async def update_project_status(project_id: str, updates: Dict[str, Any]):
    """Update project status with timestamp"""
    if project_id in projects:
        projects[project_id].update({
            **updates,
            "updated_at": datetime.now().isoformat()
        })

async def run_crew_task(project_id: str, requirements: str, project_name: Optional[str] = None, timeout: int = 3600):
    try:
        await update_project_status(project_id, {
            "status": "running",
            "tasks_completed": []
        })
        
        # Initialize the crew
        crew = DevCrew(requirements=requirements, project_name=project_name)
        
        # Store task reference for potential cancellation
        running_tasks[project_id] = asyncio.current_task()
        
        try:
            # Run with timeout
            result = await asyncio.wait_for(
                asyncio.to_thread(crew.crew().kickoff),
                timeout=timeout
            )
            
            # Update project status with results
            await update_project_status(project_id, {
                "status": "completed",
                "artifacts_path": crew.project_dir,
                "result": result,
                "progress": 100
            })
            
        except asyncio.TimeoutError:
            await update_project_status(project_id, {
                "status": "timeout",
                "error": f"Task exceeded timeout of {timeout} seconds"
            })
            logger.error(f"Project {project_id} timed out")
            
    except Exception as e:
        error_msg = str(e)
        logger.error(f"Error in project {project_id}: {error_msg}", exc_info=True)
        await update_project_status(project_id, {
            "status": "failed",
            "error": error_msg
        })
    finally:
        if project_id in running_tasks:
            del running_tasks[project_id]

@app.post("/projects/", response_model=ProjectStatus)
async def create_project(
    project_request: ProjectRequest,
    background_tasks: BackgroundTasks
):
    project_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    
    # Initialize project status
    projects[project_id] = {
        "status": "initialized",
        "created_at": timestamp,
        "updated_at": timestamp,
        "progress": 0,
        "tasks_completed": []
    }
    
    # Start the crew in the background
    background_tasks.add_task(
        run_crew_task,
        project_id,
        project_request.requirements,
        project_request.project_name,
        project_request.timeout
    )
    
    return {
        "project_id": project_id,
        **projects[project_id]
    }

@app.post("/projects/{project_id}/cancel")
async def cancel_project(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if project_id in running_tasks:
        task = running_tasks[project_id]
        task.cancel()
        await update_project_status(project_id, {
            "status": "cancelled",
            "error": "Project cancelled by user"
        })
        return {"status": "cancelled"}
    
    return {"status": projects[project_id]["status"]}

@app.get("/projects/{project_id}", response_model=ProjectStatus)
async def get_project_status(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return {
        "project_id": project_id,
        **projects[project_id]
    }

@app.get("/projects/{project_id}/artifacts/{artifact_path:path}")
async def get_project_artifact(project_id: str, artifact_path: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    if project["status"] != "completed":
        raise HTTPException(status_code=400, detail="Project artifacts not ready")
    
    # Try project artifacts first
    full_path = os.path.join(project["artifacts_path"], artifact_path)
    if not os.path.exists(full_path):
        # Try docs directory
        docs_path = os.path.join('docs', project_id, artifact_path)
        if os.path.exists(docs_path):
            full_path = docs_path
        else:
            raise HTTPException(status_code=404, detail="Artifact not found")
    
    try:
        with open(full_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        logger.error(f"Error reading artifact {full_path}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error reading artifact")

@app.get("/projects/{project_id}/docs/{doc_path:path}")
async def get_project_docs(project_id: str, doc_path: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    if project["status"] != "completed":
        raise HTTPException(status_code=400, detail="Project documentation not ready")
    
    docs_path = os.path.join(project["artifacts_path"], 'docs', doc_path)
    if not os.path.exists(docs_path):
        raise HTTPException(status_code=404, detail="Documentation not found")
    
    try:
        with open(docs_path, 'r') as f:
            content = f.read()
        return {"content": content}
    except Exception as e:
        logger.error(f"Error reading documentation {docs_path}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error reading documentation")

@app.get("/projects/{project_id}/docs")
async def list_project_docs(project_id: str):
    if project_id not in projects:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects[project_id]
    if project["status"] != "completed":
        raise HTTPException(status_code=400, detail="Project documentation not ready")
    
    docs_dir = os.path.join(project["artifacts_path"], 'docs')
    if not os.path.exists(docs_dir):
        return {"docs": []}
    
    try:
        docs = []
        for root, _, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md'):
                    rel_path = os.path.relpath(os.path.join(root, file), docs_dir)
                    docs.append({
                        "path": rel_path,
                        "type": os.path.basename(os.path.dirname(os.path.join(root, file)))
                    })
        return {"docs": docs}
    except Exception as e:
        logger.error(f"Error listing documentation for project {project_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error listing documentation")

@app.get("/projects/")
async def list_projects():
    return {
        project_id: {
            "status": data["status"],
            "created_at": data["created_at"],
            "updated_at": data["updated_at"],
            "progress": data.get("progress", 0),
            "current_task": data.get("current_task"),
            "error": data.get("error")
        }
        for project_id, data in projects.items()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    } 