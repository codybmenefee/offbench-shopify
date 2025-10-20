"""
Simple Convex HTTP client - direct HTTP calls, no CLI needed.
For prototyping and simple CRUD operations.
"""

import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime


class ConvexHTTPClient:
    """Simple HTTP client for Convex - no deployment needed."""
    
    def __init__(self, deployment_url: str):
        """
        Initialize with your Convex deployment URL.
        
        Args:
            deployment_url: Your Convex URL (e.g., https://animated-scorpion-19.convex.cloud)
        """
        self.deployment_url = deployment_url.rstrip('/')
        self.client = httpx.Client(timeout=30.0)
    
    def insert(self, table: str, document: Dict[str, Any]) -> Optional[str]:
        """
        Insert a document into a table.
        
        Args:
            table: Table name (e.g., "projects")
            document: Document data as dict
            
        Returns:
            Document ID if successful, None otherwise
        """
        try:
            response = self.client.post(
                f"{self.deployment_url}/api/insert",
                json={
                    "table": table,
                    "document": document
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("_id")
            else:
                print(f"Insert failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"Insert error: {e}")
            return None
    
    def query(self, table: str, filter: Optional[Dict] = None, limit: int = 100) -> List[Dict]:
        """
        Query documents from a table.
        
        Args:
            table: Table name
            filter: Optional filter dict
            limit: Max results to return
            
        Returns:
            List of documents
        """
        try:
            response = self.client.post(
                f"{self.deployment_url}/api/query",
                json={
                    "table": table,
                    "filter": filter or {},
                    "limit": limit
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("documents", [])
            else:
                print(f"Query failed: {response.status_code} - {response.text}")
                return []
                
        except Exception as e:
            print(f"Query error: {e}")
            return []
    
    def update(self, table: str, id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a document.
        
        Args:
            table: Table name
            id: Document ID
            updates: Fields to update
            
        Returns:
            True if successful
        """
        try:
            response = self.client.post(
                f"{self.deployment_url}/api/update",
                json={
                    "table": table,
                    "id": id,
                    "updates": updates
                }
            )
            
            return response.status_code == 200
                
        except Exception as e:
            print(f"Update error: {e}")
            return False
    
    def delete(self, table: str, id: str) -> bool:
        """
        Delete a document.
        
        Args:
            table: Table name
            id: Document ID
            
        Returns:
            True if successful
        """
        try:
            response = self.client.post(
                f"{self.deployment_url}/api/delete",
                json={
                    "table": table,
                    "id": id
                }
            )
            
            return response.status_code == 200
                
        except Exception as e:
            print(f"Delete error: {e}")
            return False
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()


# Helper functions for common operations
def save_project(client: ConvexHTTPClient, project_data: Dict) -> Optional[str]:
    """Save a project to Convex."""
    return client.insert("projects", {
        **project_data,
        "lastUpdated": int(datetime.now().timestamp() * 1000)
    })


def get_projects(client: ConvexHTTPClient) -> List[Dict]:
    """Get all projects from Convex."""
    return client.query("projects")


def save_gap(client: ConvexHTTPClient, project_id: str, gap_data: Dict) -> Optional[str]:
    """Save a gap to Convex."""
    return client.insert("gaps", {
        "projectId": project_id,
        **gap_data,
        "identifiedDate": int(datetime.now().timestamp() * 1000)
    })


def save_question(client: ConvexHTTPClient, project_id: str, question_data: Dict) -> Optional[str]:
    """Save a question to Convex."""
    return client.insert("questions", {
        "projectId": project_id,
        **question_data,
        "askedDate": int(datetime.now().timestamp() * 1000)
    })


# Example usage
if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    url = os.getenv("CONVEX_DEPLOYMENT_URL")
    
    if not url:
        print("Error: CONVEX_DEPLOYMENT_URL not set in .env")
        exit(1)
    
    client = ConvexHTTPClient(url)
    
    # Test: Insert a project
    print("Testing Convex HTTP API...")
    project_id = save_project(client, {
        "name": "Test Project",
        "scenarioId": "test-123",
        "confidence": 75.5,
        "gapsCount": 3,
        "conflictsCount": 1,
        "ambiguitiesCount": 2,
        "documentsCount": 5,
        "status": "active"
    })
    
    if project_id:
        print(f"✅ Project created: {project_id}")
        
        # Get all projects
        projects = get_projects(client)
        print(f"✅ Retrieved {len(projects)} project(s)")
    else:
        print("❌ Failed to create project")
    
    client.close()

