"""Project state management singleton."""

from typing import Dict, Optional
from models.project_state import ProjectState


class ProjectStateManager:
    """Singleton manager for project states across tool calls."""
    
    _instance = None
    _projects: Dict[str, ProjectState] = {}
    
    def __new__(cls):
        """Ensure only one instance exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def get_project(self, project_id: str) -> Optional[ProjectState]:
        """Get project state by ID."""
        return self._projects.get(project_id)
    
    def create_project(self, project_id: str, project_name: str, 
                      project_description: str = "") -> ProjectState:
        """Create a new project state."""
        if project_id in self._projects:
            return self._projects[project_id]
        
        project = ProjectState(
            project_id=project_id,
            project_name=project_name,
            project_description=project_description
        )
        self._projects[project_id] = project
        return project
    
    def update_project(self, project: ProjectState):
        """Update an existing project state."""
        self._projects[project.project_id] = project
    
    def clear_project(self, project_id: str) -> bool:
        """Clear a project from memory."""
        if project_id in self._projects:
            del self._projects[project_id]
            return True
        return False
    
    def list_projects(self) -> list:
        """List all project IDs."""
        return list(self._projects.keys())
    
    def get_or_create(self, project_id: str, project_name: str = "",
                     project_description: str = "") -> ProjectState:
        """Get existing project or create new one."""
        project = self.get_project(project_id)
        if project is None:
            project = self.create_project(project_id, project_name, project_description)
        return project

