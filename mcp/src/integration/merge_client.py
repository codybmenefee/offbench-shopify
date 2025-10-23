"""Merge API client for Google Drive integration."""

import httpx
import time
from typing import Dict, List, Optional, Any
from config import config


class MergeClient:
    """
    Client for Merge API to access Google Drive documents.
    
    Handles authentication, file listing, and file download with rate limiting
    and error handling.
    """
    
    def __init__(self, api_key: str):
        """
        Initialize Merge API client.
        
        Args:
            api_key: Merge API key for authentication
        """
        self.api_key = api_key
        self.base_url = config.MERGE_API_BASE_URL
        self.client = httpx.Client(timeout=30.0)
        
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Merge API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "X-Account-Token": "",  # Will be set per request
        }
    
    def _make_request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        account_token: Optional[str] = None,
        retries: int = 3
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Merge API with retry logic.
        
        Args:
            method: HTTP method (GET, POST, etc.)
            path: API path
            data: Request body data
            account_token: Account token for the request
            retries: Number of retry attempts
            
        Returns:
            Response data as dictionary
            
        Raises:
            Exception on failure after all retries
        """
        url = f"{self.base_url}{path}"
        headers = self._get_headers()
        
        if account_token:
            headers["X-Account-Token"] = account_token
        
        last_error = None
        for attempt in range(retries):
            try:
                if method == "GET":
                    response = self.client.get(url, headers=headers)
                elif method == "POST":
                    response = self.client.post(url, json=data, headers=headers)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code == 429:  # Rate limited
                    if attempt < retries - 1:
                        time.sleep(2 ** attempt)  # Exponential backoff
                        continue
                elif e.response.status_code >= 500 and attempt < retries - 1:
                    # Retry on server errors
                    time.sleep(2 ** attempt)
                    continue
                raise
            
            except httpx.RequestError as e:
                last_error = e
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
        
        raise last_error or Exception("Request failed after all retries")
    
    def get_integration_token(self, integration_id: str) -> str:
        """
        Get account token for an integration.
        
        Args:
            integration_id: Integration ID
            
        Returns:
            Account token for the integration
            
        Raises:
            Exception if integration not found or token unavailable
        """
        # This would query the portal's integrations table
        # For now, return a placeholder
        # TODO: Implement when portal tables are available
        raise NotImplementedError("Integration token retrieval not yet implemented")
    
    def list_folder_files(self, folder_id: str, account_token: str) -> List[Dict]:
        """
        List files in a Google Drive folder.
        
        Args:
            folder_id: Google Drive folder ID
            account_token: Account token for authentication
            
        Returns:
            List of file metadata dictionaries
        """
        try:
            response = self._make_request(
                "GET",
                f"/files?folder_id={folder_id}",
                account_token=account_token
            )
            return response.get("results", [])
        except Exception as e:
            raise Exception(f"Failed to list folder files: {str(e)}")
    
    def download_file(self, file_id: str, account_token: str) -> bytes:
        """
        Download file content from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            account_token: Account token for authentication
            
        Returns:
            File content as bytes
            
        Raises:
            Exception if download fails
        """
        try:
            # First get file metadata to get download URL
            file_info = self._make_request(
                "GET",
                f"/files/{file_id}",
                account_token=account_token
            )
            
            # Get download URL from file info
            download_url = file_info.get("download_url")
            if not download_url:
                raise Exception("No download URL available for file")
            
            # Download file content
            headers = self._get_headers()
            headers["X-Account-Token"] = account_token
            
            response = self.client.get(download_url, headers=headers)
            response.raise_for_status()
            
            return response.content
            
        except Exception as e:
            raise Exception(f"Failed to download file {file_id}: {str(e)}")
    
    def get_file_metadata(self, file_id: str, account_token: str) -> Dict:
        """
        Get file metadata from Google Drive.
        
        Args:
            file_id: Google Drive file ID
            account_token: Account token for authentication
            
        Returns:
            File metadata dictionary
        """
        try:
            return self._make_request(
                "GET",
                f"/files/{file_id}",
                account_token=account_token
            )
        except Exception as e:
            raise Exception(f"Failed to get file metadata: {str(e)}")
    
    def close(self):
        """Close the HTTP client."""
        self.client.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()