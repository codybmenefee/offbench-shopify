"""
Railway-specific startup script.
Ensures proper host and port binding for Railway deployment.
"""

import os
import sys
from pathlib import Path

# Ensure we're in the right directory for imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Start the MCP server with Railway-compatible settings."""
    from main import mcp
    
    # Railway provides PORT, default to 8123 for local testing
    port = int(os.getenv("PORT", 8123))
    host = "0.0.0.0"  # Railway requires binding to all interfaces
    
    print(f"🚀 Starting Discovery Agent MCP Server on {host}:{port}")
    print(f"📊 Environment: {'Railway' if 'RAILWAY_' in ''.join(os.environ.keys()) else 'Local'}")
    
    try:
        mcp.run(
            transport="http",
            host=host,
            port=port
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

