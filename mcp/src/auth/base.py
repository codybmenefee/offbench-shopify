"""Base authentication interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class User:
    """User information."""
    id: str
    email: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[Dict] = None


class AuthProvider(ABC):
    """Abstract base class for authentication providers."""

    @abstractmethod
    def validate_request(self, headers: Dict[str, str]) -> Optional[User]:
        """
        Validate an incoming request and return user if authenticated.
        
        Args:
            headers: HTTP request headers
            
        Returns:
            User object if authenticated, None otherwise
        """
        pass

    @abstractmethod
    def get_api_credentials(self) -> Dict[str, str]:
        """
        Get credentials for making authenticated API calls.
        
        Returns:
            Dictionary of credentials (e.g., {"Authorization": "Bearer token"})
        """
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        """
        Check if this auth provider is properly configured.
        
        Returns:
            True if enabled and configured, False otherwise
        """
        pass

