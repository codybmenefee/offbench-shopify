"""
Vercel serverless function entry point for Discovery Agent MCP.
"""

import sys
from pathlib import Path

# Add mcp/src to path
base_path = Path(__file__).parent.parent
mcp_src_path = base_path / "mcp" / "src"
sys.path.insert(0, str(mcp_src_path))

try:
    # Import the FastMCP app from main
    from main import mcp
    
    # Get the ASGI app from FastMCP
    app = mcp.streamable_http_app
    
    # Export for Vercel
    # Vercel expects either 'app' or 'handler'
    handler = app
    
except Exception as e:
    import traceback
    print(f"[VERCEL ERROR] Failed to initialize: {e}", file=sys.stderr)
    traceback.print_exc()
    raise

