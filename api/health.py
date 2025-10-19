"""
Simple health check endpoint for debugging Vercel deployment.
"""

from http.server import BaseHTTPRequestHandler
import json
import sys
from pathlib import Path

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            # Add mcp/src to path
            base_path = Path(__file__).parent.parent
            mcp_src_path = base_path / "mcp" / "src"
            sys.path.insert(0, str(mcp_src_path))
            
            # Try to import main
            try:
                import main
                mcp_status = "✅ MCP module loaded"
                has_mcp = True
            except Exception as e:
                mcp_status = f"❌ MCP module failed: {str(e)}"
                has_mcp = False
            
            # Check paths
            paths_info = {
                "base_path": str(base_path),
                "mcp_src_path": str(mcp_src_path),
                "mcp_src_exists": mcp_src_path.exists(),
                "main_py_exists": (mcp_src_path / "main.py").exists(),
            }
            
            response = {
                "status": "healthy" if has_mcp else "error",
                "mcp_status": mcp_status,
                "paths": paths_info,
                "python_version": sys.version,
                "sys_path": sys.path[:5]
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response, indent=2).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            error_response = {
                "error": str(e),
                "type": type(e).__name__
            }
            self.wfile.write(json.dumps(error_response, indent=2).encode())

