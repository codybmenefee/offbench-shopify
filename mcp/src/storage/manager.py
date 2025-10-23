"""Storage provider factory and manager."""

from typing import Optional
from .base import StorageProvider
from .local_provider import LocalStorageProvider
from .gdrive_provider import GoogleDriveProvider


def get_storage_provider(
    provider_type: str = "local",
    **kwargs
) -> StorageProvider:
    """
    Factory function to get appropriate storage provider.
    
    Args:
        provider_type: Type of provider ("local", "google_drive", "merge_api", "integration")
        **kwargs: Provider-specific arguments
        
    Returns:
        Initialized StorageProvider instance
        
    Examples:
        # Local filesystem
        provider = get_storage_provider("local", base_path="/path/to/projects")
        
        # Google Drive (future)
        provider = get_storage_provider(
            "google_drive",
            credentials=creds,
            parent_folder_id="abc123"
        )
        
        # Merge API (future)
        provider = get_storage_provider(
            "merge_api",
            api_key="key",
            account_token="token"
        )
        
        # Integration storage (Convex + Merge)
        provider = get_storage_provider(
            "integration",
            convex_client=convex_client,
            merge_client=merge_client
        )
    """
    if provider_type == "local":
        base_path = kwargs.get("base_path")
        if not base_path:
            raise ValueError("LocalStorageProvider requires 'base_path' parameter")
        return LocalStorageProvider(base_path=base_path)
    
    elif provider_type == "google_drive":
        credentials = kwargs.get("credentials")
        parent_folder_id = kwargs.get("parent_folder_id")
        return GoogleDriveProvider(
            credentials=credentials,
            parent_folder_id=parent_folder_id
        )
    
    elif provider_type == "merge_api":
        api_key = kwargs.get("api_key")
        account_token = kwargs.get("account_token")
        from .gdrive_provider import MergeAPIProvider
        return MergeAPIProvider(
            api_key=api_key,
            account_token=account_token
        )
    
    elif provider_type == "integration":
        convex_client = kwargs.get("convex_client")
        merge_client = kwargs.get("merge_client")
        if not convex_client or not merge_client:
            raise ValueError("IntegrationStorageProvider requires 'convex_client' and 'merge_client' parameters")
        from .integration_provider import IntegrationStorageProvider
        return IntegrationStorageProvider(
            convex_client=convex_client,
            merge_client=merge_client
        )
    
    else:
        raise ValueError(
            f"Unknown storage provider: {provider_type}. "
            f"Supported: 'local', 'google_drive', 'merge_api', 'integration'"
        )


# Global default provider (can be overridden)
_default_provider: Optional[StorageProvider] = None


def set_default_provider(provider: StorageProvider):
    """Set the default storage provider for the application."""
    global _default_provider
    _default_provider = provider


def get_default_provider() -> Optional[StorageProvider]:
    """Get the default storage provider."""
    return _default_provider

