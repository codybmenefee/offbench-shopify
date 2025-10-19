"""
Discovery to Implementation Confidence Tool - MCP Server
Autonomous agent tools for processing discovery documents and generating implementation deliverables.
"""

import sys
from fastmcp import FastMCP
from tools.discovery_tools import register_discovery_tools
from tools.template_tools import register_template_tools

# Create FastMCP instance
mcp = FastMCP(
    name="Discovery Agent"
)

# Register discovery tools
register_discovery_tools(mcp)

# Register template tools
register_template_tools(mcp)

if __name__ == "__main__":
    # Support both transports via command line
    # stdio for Cursor/Claude Desktop
    # http for ChatGPT apps
    
    transport = "http"  # default
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        transport = "stdio"
    
    if transport == "stdio":
        # For Cursor and Claude Desktop
        mcp.run(transport="stdio")
    else:
        # For ChatGPT apps
        mcp.run(
            transport="http",
            port=8123
        )
