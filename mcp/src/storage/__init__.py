"""Storage abstraction layer for multi-provider support."""

from .base import StorageProvider, FolderType
from .manager import get_storage_provider

__all__ = ["StorageProvider", "FolderType", "get_storage_provider"]

