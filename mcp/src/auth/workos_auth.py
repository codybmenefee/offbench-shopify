"""WorkOS authentication provider (stub for future implementation)."""

from typing import Optional, Dict
from .base import AuthProvider, User
from config import config


class WorkOSAuthProvider(AuthProvider):
    """
    WorkOS authentication provider.
    
    TODO: Implement WorkOS authentication when ready.
    - Validate WorkOS sessions
    - Handle SSO integration
    - Fetch user info from WorkOS API
    """

    def __init__(self):
        self.api_key = config.WORKOS_API_KEY
        self.client_id = config.WORKOS_CLIENT_ID

    def validate_request(self, headers: Dict[str, str]) -> Optional[User]:
        """
        Validate WorkOS session.
        
        TODO: Implement WorkOS session validation
        """
        raise NotImplementedError("WorkOS authentication not yet implemented")

    def get_api_credentials(self) -> Dict[str, str]:
        """Get WorkOS credentials for API calls."""
        if self.api_key:
            return {"Authorization": f"Bearer {self.api_key}"}
        return {}

    def is_enabled(self) -> bool:
        """Check if WorkOS is configured."""
        return bool(self.api_key and self.client_id)

