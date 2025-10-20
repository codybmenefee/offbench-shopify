"""Clerk authentication provider (stub for future implementation)."""

from typing import Optional, Dict
from .base import AuthProvider, User
from config import config


class ClerkAuthProvider(AuthProvider):
    """
    Clerk authentication provider.
    
    TODO: Implement Clerk authentication when ready.
    - Validate JWT tokens from Clerk
    - Fetch user info from Clerk API
    - Handle session management
    """

    def __init__(self):
        self.publishable_key = config.CLERK_PUBLISHABLE_KEY
        self.secret_key = config.CLERK_SECRET_KEY

    def validate_request(self, headers: Dict[str, str]) -> Optional[User]:
        """
        Validate Clerk JWT token.
        
        TODO: Implement JWT validation using Clerk SDK
        """
        raise NotImplementedError("Clerk authentication not yet implemented")

    def get_api_credentials(self) -> Dict[str, str]:
        """Get Clerk credentials for API calls."""
        if self.secret_key:
            return {"Authorization": f"Bearer {self.secret_key}"}
        return {}

    def is_enabled(self) -> bool:
        """Check if Clerk is configured."""
        return bool(self.publishable_key and self.secret_key)

