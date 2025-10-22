"""Convex HTTP API client wrapper."""

import httpx
import os
import time
from typing import Dict, Any, Optional, List
from config import config


class ConvexClient:
    """
    Wrapper around Convex HTTP API for Python.
    Handles authentication, retries, and error handling.
    """

    def __init__(
        self,
        deployment_url: Optional[str] = None
    ):
        self.deployment_url = deployment_url or config.CONVEX_DEPLOYMENT_URL
        
        if not self.deployment_url:
            raise ValueError("CONVEX_DEPLOYMENT_URL not configured")
        
        # HTTP client with timeout
        self.client = httpx.Client(timeout=30.0)

    def _get_headers(self) -> Dict[str, str]:
        """Get headers for Convex API requests."""
        headers = {
            "Content-Type": "application/json",
        }
        
        # Optional auth header (if portal requires it). Use CONVEX_ADMIN_KEY if provided.
        admin_key = os.getenv("CONVEX_ADMIN_KEY")
        if admin_key:
            headers["Authorization"] = f"Bearer {admin_key}"
        
        return headers

    def _make_request(
        self,
        method: str,
        path: str,
        data: Optional[Dict[str, Any]] = None,
        retries: int = 3
    ) -> Dict[str, Any]:
        """
        Make HTTP request to Convex API with retry logic.
        
        Args:
            method: HTTP method (POST, GET, etc.)
            path: API path (e.g., "/api/mutation")
            data: Request body data
            retries: Number of retry attempts
            
        Returns:
            Response data as dictionary
            
        Raises:
            Exception on failure after all retries
        """
        url = f"{self.deployment_url}{path}"
        headers = self._get_headers()
        
        last_error = None
        for attempt in range(retries):
            try:
                if method == "POST":
                    response = self.client.post(url, json=data, headers=headers)
                elif method == "GET":
                    response = self.client.get(url, headers=headers)
                else:
                    raise ValueError(f"Unsupported method: {method}")
                
                response.raise_for_status()
                return response.json()
            
            except httpx.HTTPStatusError as e:
                last_error = e
                if e.response.status_code >= 500 and attempt < retries - 1:
                    # Retry on server errors
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise
            
            except httpx.RequestError as e:
                last_error = e
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise
        
        raise last_error or Exception("Request failed after all retries")

    def mutation(self, function_name: str, args: Dict[str, Any]) -> Any:
        """
        Call a Convex mutation (write operation).
        
        Args:
            function_name: Mutation name (e.g., "mutations/projects:upsertProject")
            args: Mutation arguments
            
        Returns:
            Mutation result
        """
        data = {
            "path": function_name,
            "args": args,
        }
        
        result = self._make_request("POST", "/api/mutation", data)
        
        if "error" in result:
            raise Exception(f"Convex mutation error: {result['error']}")
        
        return result.get("value")

    def query(self, function_name: str, args: Optional[Dict[str, Any]] = None) -> Any:
        """
        Call a Convex query (read operation).
        
        Args:
            function_name: Query name (e.g., "queries/projects:listProjects")
            args: Query arguments
            
        Returns:
            Query result
        """
        data = {
            "path": function_name,
            "args": args or {},
        }
        
        result = self._make_request("POST", "/api/query", data)
        
        if "error" in result:
            raise Exception(f"Convex query error: {result['error']}")
        
        return result.get("value")

    def batch_mutations(self, mutations: List[Dict[str, Any]]) -> List[Any]:
        """
        Execute multiple mutations in sequence.
        
        Args:
            mutations: List of {function_name, args} dicts
            
        Returns:
            List of mutation results
        """
        results = []
        for mutation in mutations:
            result = self.mutation(
                mutation["function_name"],
                mutation["args"]
            )
            results.append(result)
        return results

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
