"""Configuration management for MCP server."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


class Config:
    """Application configuration."""

    # Convex configuration
    CONVEX_DEPLOYMENT_URL: Optional[str] = os.getenv("CONVEX_DEPLOYMENT_URL")
    CONVEX_AUTH_ENABLED: bool = os.getenv("CONVEX_AUTH_ENABLED", "false").lower() == "true"
    
    # Future auth providers
    CLERK_PUBLISHABLE_KEY: Optional[str] = os.getenv("CLERK_PUBLISHABLE_KEY")
    CLERK_SECRET_KEY: Optional[str] = os.getenv("CLERK_SECRET_KEY")
    WORKOS_API_KEY: Optional[str] = os.getenv("WORKOS_API_KEY")
    WORKOS_CLIENT_ID: Optional[str] = os.getenv("WORKOS_CLIENT_ID")
    
    # Sync behavior
    AUTO_SYNC_ON_ANALYZE: bool = os.getenv("AUTO_SYNC_ON_ANALYZE", "false").lower() == "true"
    AUTO_SYNC_ON_UPDATE: bool = os.getenv("AUTO_SYNC_ON_UPDATE", "false").lower() == "true"
    AUTO_SYNC_ON_CREATE: bool = os.getenv("AUTO_SYNC_ON_CREATE", "false").lower() == "true"
    
    @classmethod
    def is_convex_enabled(cls) -> bool:
        """Check if Convex is properly configured."""
        return bool(cls.CONVEX_DEPLOYMENT_URL)
    
    @classmethod
    def get_auth_mode(cls) -> str:
        """Get current authentication mode."""
        if cls.CLERK_SECRET_KEY:
            return "clerk"
        elif cls.WORKOS_API_KEY:
            return "workos"
        else:
            return "api_key"


# Singleton config instance
config = Config()

