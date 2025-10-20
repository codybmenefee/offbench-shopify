"""Local filesystem storage provider."""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from .base import StorageProvider, FolderType
from models.document import Document, DocumentType


class LocalStorageProvider(StorageProvider):
    """
    Local filesystem storage provider.
    
    Maintains backward compatibility with existing test-data structure
    while supporting three-folder structure for new projects.
    """
    
    def __init__(self, base_path: str):
        """
        Initialize local storage provider.
        
        Args:
            base_path: Base directory for all projects (e.g., /path/to/test-data)
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def list_projects(self) -> List[Dict]:
        """List all available projects in base directory."""
        projects = []
        
        if not self.base_path.exists():
            return projects
        
        for folder in self.base_path.iterdir():
            if folder.is_dir() and not folder.name.startswith('.'):
                project_info = self._get_project_metadata(folder)
                if project_info:
                    projects.append(project_info)
        
        return projects
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """Get project metadata."""
        project_path = self.base_path / project_id
        
        if not project_path.exists():
            return None
        
        return self._get_project_metadata(project_path)
    
    def create_project(self, project_id: str, project_name: str,
                      config: Optional[Dict] = None) -> Dict:
        """
        Create new project with three-folder structure.
        
        Creates:
        - project_id/
          - discovery/
          - implementation/
          - working/
          - .project.json (metadata and config)
        """
        project_path = self.base_path / project_id
        
        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)
        
        # Create three subfolders
        (project_path / "discovery").mkdir(exist_ok=True)
        (project_path / "implementation").mkdir(exist_ok=True)
        (project_path / "working").mkdir(exist_ok=True)
        
        # Create project config
        project_config = {
            "project_id": project_id,
            "project_name": project_name,
            "created_at": datetime.now().isoformat(),
            "config": config or self._default_config()
        }
        
        config_path = project_path / ".project.json"
        with open(config_path, 'w') as f:
            json.dump(project_config, f, indent=2)
        
        return self._get_project_metadata(project_path)
    
    def delete_project(self, project_id: str) -> bool:
        """Delete a project directory."""
        project_path = self.base_path / project_id
        
        if not project_path.exists():
            return False
        
        # Remove directory recursively
        import shutil
        shutil.rmtree(project_path)
        return True
    
    def list_documents(self, project_id: str, folder_type: FolderType) -> List[Dict]:
        """List documents in a specific folder."""
        folder_path = self._get_folder_path(project_id, folder_type)
        
        if not folder_path or not folder_path.exists():
            return []
        
        documents = []
        for file_path in folder_path.rglob("*.txt"):
            doc_info = {
                "filename": file_path.name,
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
            documents.append(doc_info)
        
        return documents
    
    def get_document(self, project_id: str, folder_type: FolderType,
                    filename: str) -> Optional[Dict]:
        """Get a specific document."""
        folder_path = self._get_folder_path(project_id, folder_type)
        
        if not folder_path:
            return None
        
        file_path = folder_path / filename
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "filename": filename,
            "content": content,
            "metadata": {
                "path": str(file_path),
                "size": file_path.stat().st_size,
                "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
            }
        }
    
    def add_document(self, project_id: str, folder_type: FolderType,
                    filename: str, content: str, metadata: Optional[Dict] = None):
        """Add a document to project folder."""
        folder_path = self._get_folder_path(project_id, folder_type)
        
        if not folder_path:
            raise ValueError(f"Project {project_id} not found")
        
        file_path = folder_path / filename
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Optionally save metadata
        if metadata:
            meta_path = folder_path / f".{filename}.meta.json"
            with open(meta_path, 'w') as f:
                json.dump(metadata, f, indent=2)
    
    def save_deliverable(self, project_id: str, filename: str,
                        content: str, metadata: Optional[Dict] = None):
        """Save deliverable to implementation folder."""
        self.add_document(
            project_id=project_id,
            folder_type=FolderType.IMPLEMENTATION,
            filename=filename,
            content=content,
            metadata=metadata
        )
    
    def get_config(self, project_id: str) -> Dict:
        """Get project configuration."""
        project_path = self.base_path / project_id
        config_path = project_path / ".project.json"
        
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                return data.get("config", self._default_config())
        
        return self._default_config()
    
    def save_config(self, project_id: str, config: Dict):
        """Save project configuration."""
        project_path = self.base_path / project_id
        config_path = project_path / ".project.json"
        
        # Load existing or create new
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
        else:
            data = {
                "project_id": project_id,
                "created_at": datetime.now().isoformat()
            }
        
        data["config"] = config
        data["updated_at"] = datetime.now().isoformat()
        
        with open(config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def project_exists(self, project_id: str) -> bool:
        """Check if project exists."""
        return (self.base_path / project_id).exists()
    
    # Helper methods
    
    def _get_folder_path(self, project_id: str, folder_type: FolderType) -> Optional[Path]:
        """Get path to specific folder, handling legacy structure."""
        project_path = self.base_path / project_id
        
        if not project_path.exists():
            return None
        
        # Check if new structure (has three subfolders)
        new_structure_path = project_path / folder_type.value
        if new_structure_path.exists():
            return new_structure_path
        
        # Legacy structure compatibility
        if folder_type == FolderType.DISCOVERY:
            # Legacy: emails/, transcripts/, client-docs/ at root
            # Return project root for backward compatibility
            return project_path
        elif folder_type == FolderType.IMPLEMENTATION:
            # Legacy: no implementation folder
            impl_path = project_path / "implementation"
            impl_path.mkdir(exist_ok=True)
            return impl_path
        elif folder_type == FolderType.WORKING:
            # Legacy: no working folder
            working_path = project_path / "working"
            working_path.mkdir(exist_ok=True)
            return working_path
        
        return project_path
    
    def _get_project_metadata(self, project_path: Path) -> Dict:
        """Extract project metadata from directory."""
        project_id = project_path.name
        
        # Try to load from .project.json
        config_path = project_path / ".project.json"
        if config_path.exists():
            with open(config_path, 'r') as f:
                data = json.load(f)
                return {
                    "project_id": project_id,
                    "name": data.get("project_name", self._format_name(project_id)),
                    "description": data.get("description", ""),
                    "path": str(project_path),
                    "created_at": data.get("created_at"),
                    "has_structure": self._check_new_structure(project_path)
                }
        
        # Legacy: try to read README
        readme_path = project_path / "README.md"
        description = ""
        if readme_path.exists():
            with open(readme_path, 'r') as f:
                content = f.read()
                # Extract business context
                match = re.search(r'## Business Context\s+(.+?)(?=\n##|\Z)', 
                                content, re.DOTALL)
                if match:
                    description = match.group(1).strip()
        
        return {
            "project_id": project_id,
            "name": self._format_name(project_id),
            "description": description,
            "path": str(project_path),
            "has_structure": self._check_new_structure(project_path)
        }
    
    def _check_new_structure(self, project_path: Path) -> bool:
        """Check if project has new three-folder structure."""
        return (
            (project_path / "discovery").exists() and
            (project_path / "implementation").exists() and
            (project_path / "working").exists()
        )
    
    def _format_name(self, project_id: str) -> str:
        """Format project ID into human-readable name."""
        return project_id.replace("scenario-", "").replace("-", " ").title()
    
    def _default_config(self) -> Dict:
        """Return default project configuration."""
        return {
            "confidence_threshold": 80.0,
            "custom_gap_patterns": [],
            "priority_weights": {
                "business_rules": 1.0,
                "technical_constraints": 1.0,
                "edge_cases": 0.5,
                "success_criteria": 1.0,
                "error_handling": 1.0
            },
            "auto_reanalyze": True
        }
    
    def get_all_discovery_documents(self, project_id: str) -> List[Path]:
        """
        Get all discovery documents from project (handles legacy structure).
        
        Returns:
            List of file paths for all discovery documents
        """
        project_path = self.base_path / project_id
        
        if not project_path.exists():
            return []
        
        documents = []
        
        # Check new structure
        discovery_path = project_path / "discovery"
        if discovery_path.exists():
            documents.extend(discovery_path.rglob("*.txt"))
        else:
            # Legacy structure: scan emails, transcripts, client-docs
            for subfolder in ["emails", "transcripts", "client-docs"]:
                subfolder_path = project_path / subfolder
                if subfolder_path.exists():
                    # Use rglob for nested files
                    documents.extend(subfolder_path.rglob("*.txt"))
        
        # Sort for consistent ordering
        return sorted(documents)

