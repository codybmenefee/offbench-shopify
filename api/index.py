"""
Vercel serverless function entry point for Discovery Agent MCP.
"""

import sys
import os
from pathlib import Path

# Add mcp/src to path
base_path = Path(__file__).parent.parent
sys.path.insert(0, str(base_path / "mcp" / "src"))

# Import the FastMCP app from main
from main import mcp

# Get the ASGI app from FastMCP
app = mcp.streamable_http_app

# Vercel will use this app as the handler
# The handler signature is what Vercel expects
handler = app

# For debugging
print(f"[VERCEL] Discovery Agent MCP initialized", file=sys.stderr)
print(f"[VERCEL] Base path: {base_path}", file=sys.stderr)
print(f"[VERCEL] App type: {type(app)}", file=sys.stderr)

