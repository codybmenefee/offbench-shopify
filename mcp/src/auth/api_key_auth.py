"""API Key authentication provider."""

from typing import Optional, Dict
from .base import AuthProvider, User
from config import config


class ApiKeyAuthProvider(AuthProvider):
    """
    Simple API key authentication for MCP server.
    
    Note: Currently not used - Convex functions are publicly accessible.
    Auth will be implemented directly in Convex functions when needed.
    """

    def __init__(self):
        pass

    def validate_request(self, headers: Dict[str, str]) -> Optional[User]:
        """
        Validate API key from Authorization header.
        
        Note: Currently returns None - no auth required for development.
        """
        # No auth required for now
        return None

    def get_api_credentials(self) -> Dict[str, str]:
        """Get credentials for Convex API calls."""
        # No credentials needed for now
        return {}

    def is_enabled(self) -> bool:
        """Check if API key auth is configured."""
        # Auth not enabled for development
        return False

