"""Abstract base class for storage providers."""

from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from enum import Enum
from pathlib import Path


class FolderType(Enum):
    """Types of folders in project structure."""
    DISCOVERY = "discovery"
    IMPLEMENTATION = "implementation"
    WORKING = "working"


class StorageProvider(ABC):
    """Abstract interface for storage providers (local, Google Drive, etc.)."""
    
    @abstractmethod
    def list_projects(self) -> List[Dict]:
        """
        List all available projects.
        
        Returns:
            List of project metadata dicts with keys: project_id, name, description, path
        """
        pass
    
    @abstractmethod
    def get_project(self, project_id: str) -> Optional[Dict]:
        """
        Get project metadata and configuration.
        
        Args:
            project_id: Unique project identifier
            
        Returns:
            Project metadata dict or None if not found
        """
        pass
    
    @abstractmethod
    def create_project(self, project_id: str, project_name: str, 
                      config: Optional[Dict] = None) -> Dict:
        """
        Create a new project with folder structure.
        
        Args:
            project_id: Unique project identifier
            project_name: Human-readable project name
            config: Optional project configuration
            
        Returns:
            Project metadata dict
        """
        pass
    
    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if deleted, False if not found
        """
        pass
    
    @abstractmethod
    def list_documents(self, project_id: str, folder_type: FolderType) -> List[Dict]:
        """
        List documents in a specific folder.
        
        Args:
            project_id: Project identifier
            folder_type: Which folder to list (discovery, implementation, working)
            
        Returns:
            List of document metadata dicts
        """
        pass
    
    @abstractmethod
    def get_document(self, project_id: str, folder_type: FolderType, 
                    filename: str) -> Optional[Dict]:
        """
        Get a specific document.
        
        Args:
            project_id: Project identifier
            folder_type: Which folder the document is in
            filename: Document filename
            
        Returns:
            Document dict with 'content' and 'metadata' keys, or None
        """
        pass
    
    @abstractmethod
    def add_document(self, project_id: str, folder_type: FolderType,
                    filename: str, content: str, metadata: Optional[Dict] = None):
        """
        Add a document to a project folder.
        
        Args:
            project_id: Project identifier
            folder_type: Which folder to add to
            filename: Document filename
            content: Document content
            metadata: Optional metadata dict
        """
        pass
    
    @abstractmethod
    def save_deliverable(self, project_id: str, filename: str, 
                        content: str, metadata: Optional[Dict] = None):
        """
        Save a generated deliverable to implementation folder.
        
        Args:
            project_id: Project identifier
            filename: Deliverable filename
            content: Deliverable content
            metadata: Optional metadata (confidence score, generation time, etc.)
        """
        pass
    
    @abstractmethod
    def get_config(self, project_id: str) -> Dict:
        """
        Get project configuration.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Configuration dict
        """
        pass
    
    @abstractmethod
    def save_config(self, project_id: str, config: Dict):
        """
        Save project configuration.
        
        Args:
            project_id: Project identifier
            config: Configuration dict to save
        """
        pass
    
    @abstractmethod
    def project_exists(self, project_id: str) -> bool:
        """
        Check if project exists.
        
        Args:
            project_id: Project identifier
            
        Returns:
            True if exists, False otherwise
        """
        pass

