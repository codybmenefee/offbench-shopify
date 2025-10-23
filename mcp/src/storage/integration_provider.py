"""Integration-based storage provider using Convex + Merge API."""

import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

from .base import StorageProvider, FolderType
from models.document import Document, DocumentType
from persistence.convex_client import ConvexClient
from integration.merge_client import MergeClient


class IntegrationStorageProvider(StorageProvider):
    """
    Storage provider that uses Convex + Merge API for Google Drive integration.
    
    Fetches documents from Google Drive via Merge API, stores metadata in Convex,
    and caches content in memory for analysis.
    """
    
    def __init__(self, convex_client: ConvexClient, merge_client: MergeClient):
        """
        Initialize integration storage provider.
        
        Args:
            convex_client: Convex client for database operations
            merge_client: Merge client for Google Drive access
        """
        self.convex_client = convex_client
        self.merge_client = merge_client
        
    def list_projects(self) -> List[Dict]:
        """List all available projects from Convex."""
        try:
            projects = self.convex_client.query("queries/projects:listProjects")
            return [
                {
                    "project_id": p.get("scenarioId", p.get("_id")),
                    "name": p.get("name", "Unknown"),
                    "description": "",
                    "path": f"convex://{p.get('_id')}",
                    "created_at": p.get("created_at"),
                    "has_structure": True  # Integration projects always have structure
                }
                for p in projects
            ]
        except Exception as e:
            print(f"Error listing projects: {e}")
            return []
    
    def get_project(self, project_id: str) -> Optional[Dict]:
        """Get project metadata from Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if project:
                return {
                    "project_id": project_id,
                    "name": project.get("name", "Unknown"),
                    "description": "",
                    "path": f"convex://{project.get('_id')}",
                    "created_at": project.get("created_at"),
                    "has_structure": True
                }
            return None
        except Exception as e:
            print(f"Error getting project {project_id}: {e}")
            return None
    
    def create_project(self, project_id: str, project_name: str,
                      config: Optional[Dict] = None) -> Dict:
        """
        Create new project in Convex.
        
        Note: This creates a project record but doesn't set up Google Drive integration.
        Integration setup is handled by the portal.
        """
        try:
            project_data = {
                "scenarioId": project_id,
                "name": project_name,
                "confidence": 0.0,
                "gapsCount": 0,
                "conflictsCount": 0,
                "ambiguitiesCount": 0,
                "documentsCount": 0,
                "status": "active"
            }
            
            project_convex_id = self.convex_client.mutation(
                "mutations/projects:upsertProject",
                project_data
            )
            
            return {
                "project_id": project_id,
                "name": project_name,
                "description": "",
                "path": f"convex://{project_convex_id}",
                "created_at": datetime.now().isoformat(),
                "has_structure": True
            }
        except Exception as e:
            raise Exception(f"Failed to create project: {str(e)}")
    
    def delete_project(self, project_id: str) -> bool:
        """Delete project from Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if project:
                self.convex_client.mutation(
                    "mutations/projects:deleteProject",
                    {"projectId": project["_id"]}
                )
                return True
            return False
        except Exception as e:
            print(f"Error deleting project {project_id}: {e}")
            return False
    
    def list_documents(self, project_id: str, folder_type: FolderType) -> List[Dict]:
        """List documents for a project from Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if not project:
                return []
            
            documents = self.convex_client.query(
                "queries/documents:listByProject",
                {"projectId": project["_id"]}
            )
            
            return [
                {
                    "filename": doc.get("name", "unknown"),
                    "path": f"convex://{doc.get('_id')}",
                    "size": doc.get("size", 0),
                    "modified": datetime.fromtimestamp(doc.get("uploadDate", 0) / 1000).isoformat(),
                    "external_id": doc.get("externalId"),
                    "source": doc.get("source", "local")
                }
                for doc in documents
            ]
        except Exception as e:
            print(f"Error listing documents for {project_id}: {e}")
            return []
    
    def get_document(self, project_id: str, folder_type: FolderType,
                    filename: str) -> Optional[Dict]:
        """Get a specific document from Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if not project:
                return None
            
            documents = self.convex_client.query(
                "queries/documents:listByProject",
                {"projectId": project["_id"]}
            )
            
            for doc in documents:
                if doc.get("name") == filename:
                    return {
                        "filename": filename,
                        "content": "",  # Content not stored in Convex
                        "metadata": {
                            "path": f"convex://{doc.get('_id')}",
                            "size": doc.get("size", 0),
                            "modified": datetime.fromtimestamp(doc.get("uploadDate", 0) / 1000).isoformat(),
                            "external_id": doc.get("externalId"),
                            "source": doc.get("source", "local")
                        }
                    }
            return None
        except Exception as e:
            print(f"Error getting document {filename} for {project_id}: {e}")
            return None
    
    def add_document(self, project_id: str, folder_type: FolderType,
                    filename: str, content: str, metadata: Optional[Dict] = None):
        """Add a document to Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if not project:
                raise ValueError(f"Project {project_id} not found")
            
            document_data = {
                "projectId": project["_id"],
                "name": filename,
                "type": self._detect_document_type_from_filename(filename),
                "uploadDate": int(datetime.now().timestamp() * 1000),
                "size": len(content.encode('utf-8')),
                "status": "processed",
                "source": "local",
                "metadata": metadata or {}
            }
            
            document_id = self.convex_client.mutation(
                "mutations/documents:createDocument",
                document_data
            )
            
            return document_id
        except Exception as e:
            raise Exception(f"Failed to add document: {str(e)}")
    
    def save_deliverable(self, project_id: str, filename: str,
                        content: str, metadata: Optional[Dict] = None):
        """Save deliverable to Convex."""
        self.add_document(
            project_id=project_id,
            folder_type=FolderType.IMPLEMENTATION,
            filename=filename,
            content=content,
            metadata=metadata
        )
    
    def get_config(self, project_id: str) -> Dict:
        """Get project configuration from Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if project:
                return project.get("config", self._default_config())
            return self._default_config()
        except Exception as e:
            print(f"Error getting config for {project_id}: {e}")
            return self._default_config()
    
    def save_config(self, project_id: str, config: Dict):
        """Save project configuration to Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if project:
                self.convex_client.mutation(
                    "mutations/projects:updateProjectConfig",
                    {"projectId": project["_id"], "config": config}
                )
        except Exception as e:
            print(f"Error saving config for {project_id}: {e}")
    
    def project_exists(self, project_id: str) -> bool:
        """Check if project exists in Convex."""
        try:
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            return project is not None
        except Exception as e:
            print(f"Error checking project existence {project_id}: {e}")
            return False
    
    def sync_documents_from_integration(self, project_id: str) -> List[Document]:
        """
        Sync documents from Google Drive integration.
        
        This is the main method for fetching documents from Google Drive
        and creating Document objects for analysis.
        """
        try:
            # Get project and integration info
            project = self.convex_client.query(
                "queries/projects:getProjectByScenarioId",
                {"scenarioId": project_id}
            )
            if not project:
                raise Exception(f"Project {project_id} not found")
            
            # Get integration info (placeholder for now)
            integration_info = self.convex_client.query(
                "queries/integrations:getProjectIntegration",
                {"projectId": project["_id"]}
            )
            
            if not integration_info:
                raise Exception(f"No integration found for project {project_id}")
            
            folder_info = self.convex_client.query(
                "queries/integrations:getProjectFolder",
                {"projectId": project["_id"]}
            )
            
            if not folder_info:
                raise Exception(f"No folder found for project {project_id}")
            
            # Get account token
            account_token = integration_info.get("accountToken")
            if not account_token:
                raise Exception("No account token available for integration")
            
            # List files in folder
            folder_id = folder_info.get("folderId")
            files = self.merge_client.list_folder_files(folder_id, account_token)
            
            documents = []
            for file_info in files:
                try:
                    # Download file content
                    file_content = self.merge_client.download_file(
                        file_info["id"], account_token
                    )
                    
                    # Decode content (assuming UTF-8)
                    content = file_content.decode('utf-8')
                    
                    # Detect document type
                    doc_type = self._detect_document_type_from_metadata(file_info)
                    
                    # Create document
                    doc = Document(
                        file_path=file_info.get("name", "unknown"),
                        content=content,
                        doc_type=doc_type,
                        metadata={
                            "mime_type": file_info.get("mime_type"),
                            "size": file_info.get("size"),
                            "modified_time": file_info.get("modified_time")
                        },
                        external_id=file_info["id"],
                        external_url=file_info.get("web_view_link"),
                        integration_id=integration_info["id"],
                        source="integration"
                    )
                    
                    # Store metadata in Convex
                    document_data = {
                        "projectId": project["_id"],
                        "name": doc.file_path,
                        "type": doc.doc_type.value,
                        "uploadDate": int(datetime.now().timestamp() * 1000),
                        "size": len(content.encode('utf-8')),
                        "status": "processed",
                        "externalId": doc.external_id,
                        "externalUrl": doc.external_url,
                        "integrationId": doc.integration_id,
                        "source": "integration",
                        "metadata": doc.metadata
                    }
                    
                    convex_doc_id = self.convex_client.mutation(
                        "mutations/documents:createDocument",
                        document_data
                    )
                    
                    doc.convex_document_id = convex_doc_id
                    documents.append(doc)
                    
                except Exception as e:
                    print(f"Error processing file {file_info.get('name', 'unknown')}: {e}")
                    continue
            
            return documents
            
        except Exception as e:
            raise Exception(f"Failed to sync documents from integration: {str(e)}")
    
    def _detect_document_type_from_filename(self, filename: str) -> str:
        """Detect document type from filename."""
        filename_lower = filename.lower()
        
        if "email" in filename_lower:
            return "email"
        elif "transcript" in filename_lower:
            return "transcript"
        elif "sow" in filename_lower:
            return "sow"
        elif "guide" in filename_lower or "brand" in filename_lower:
            return "guide"
        elif "note" in filename_lower:
            return "notes"
        else:
            return "other"
    
    def _detect_document_type_from_metadata(self, file_info: Dict) -> DocumentType:
        """Detect document type from file metadata."""
        filename = file_info.get("name", "").lower()
        mime_type = file_info.get("mime_type", "").lower()
        
        # Check filename patterns first
        if "email" in filename:
            return DocumentType.EMAIL
        elif "transcript" in filename:
            return DocumentType.TRANSCRIPT
        elif "sow" in filename:
            return DocumentType.SOW
        elif "guide" in filename or "brand" in filename:
            return DocumentType.GUIDE
        elif "note" in filename:
            return DocumentType.NOTES
        
        # Check MIME type
        if "text/plain" in mime_type:
            return DocumentType.NOTES
        elif "application/pdf" in mime_type:
            return DocumentType.SOW
        elif "text/html" in mime_type:
            return DocumentType.EMAIL
        
        return DocumentType.OTHER
    
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
