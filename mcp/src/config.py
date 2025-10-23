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
    
    # Optional multi-tenant context passed on writes
    MCP_USER_ID: Optional[str] = os.getenv("MCP_USER_ID")
    MCP_ORG_ID: Optional[str] = os.getenv("MCP_ORG_ID")
    
    # Demo mode - tags data for portal demo purposes
    DEMO_MODE: bool = os.getenv("DEMO_MODE", "false").lower() == "true"
    DEMO_USER_ID: str = os.getenv("DEMO_USER_ID", "demo-user")
    DEMO_ORG_ID: str = os.getenv("DEMO_ORG_ID", "demo-org")
    
    # Integration Storage configuration
    MERGE_API_KEY: Optional[str] = os.getenv("MERGE_API_KEY")
    MERGE_API_BASE_URL: str = os.getenv("MERGE_API_BASE_URL", "https://api.merge.dev/api/filestorage/v1")
    USE_INTEGRATION_STORAGE: bool = os.getenv("USE_INTEGRATION_STORAGE", "false").lower() == "true"
    
    # Sync behavior
    AUTO_SYNC_ON_ANALYZE: bool = os.getenv("AUTO_SYNC_ON_ANALYZE", "false").lower() == "true"
    AUTO_SYNC_ON_UPDATE: bool = os.getenv("AUTO_SYNC_ON_UPDATE", "false").lower() == "true"
    AUTO_SYNC_ON_CREATE: bool = os.getenv("AUTO_SYNC_ON_CREATE", "false").lower() == "true"
    
    @classmethod
    def is_convex_enabled(cls) -> bool:
        """Check if Convex is properly configured."""
        return bool(cls.CONVEX_DEPLOYMENT_URL)
    
    @classmethod
    def is_demo_mode(cls) -> bool:
        """Check if demo mode is enabled."""
        return cls.DEMO_MODE
    
    @classmethod
    def get_demo_context(cls) -> dict:
        """Get demo user/org context for data tagging."""
        if cls.DEMO_MODE:
            return {
                "userId": cls.DEMO_USER_ID,
                "orgId": cls.DEMO_ORG_ID,
                "isDemo": True
            }
        return {}


# Singleton config instance
config = Config()
