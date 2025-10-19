"""MCP tools for discovery analysis."""

from .discovery_tools import register_discovery_tools
from .template_tools import register_template_tools

__all__ = [
    "register_discovery_tools",
    "register_template_tools",
]

