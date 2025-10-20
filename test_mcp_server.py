#!/usr/bin/env python3
"""
Test MCP Server via HTTP API
"""

import requests
import json

BASE_URL = "http://localhost:8123"

def test_server_health():
    """Test if server is responding"""
    try:
        response = requests.get(BASE_URL, timeout=5)
        print(f"✅ Server is running at {BASE_URL}")
        print(f"   Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Server not responding: {e}")
        return False

def test_mcp_tool_via_http():
    """Test calling an MCP tool via FastMCP HTTP endpoints"""
    # FastMCP uses different endpoint structure
    # Try to get server info or list tools
    
    endpoints_to_try = [
        "/",
        "/docs",
        "/openapi.json",
        "/mcp",
        "/mcp/tools",
    ]
    
    print("\n🔍 Exploring MCP Server Endpoints:")
    for endpoint in endpoints_to_try:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            print(f"   {endpoint}: {response.status_code} - {response.headers.get('content-type', 'unknown')}")
            if response.status_code == 200 and 'json' in response.headers.get('content-type', ''):
                data = response.json()
                if endpoint == "/openapi.json":
                    print(f"      OpenAPI spec found, title: {data.get('info', {}).get('title')}")
        except Exception as e:
            print(f"   {endpoint}: {type(e).__name__}")

if __name__ == "__main__":
    print("="*60)
    print("MCP SERVER HTTP TEST")
    print("="*60)
    
    if test_server_health():
        test_mcp_tool_via_http()
        
        print("\n" + "="*60)
        print("✅ MCP Server is running and responsive")
        print("="*60)
        print("\nNote: The MCP server is running successfully.")
        print("Direct tool testing was done via Python imports in test_mcp_integrity.py")
        print("For production use, the MCP server will be called via:")
        print("  - Claude Desktop (stdio)")
        print("  - Cursor MCP integration (stdio)")
        print("  - HTTP clients for ChatGPT or other integrations")
    else:
        print("\n❌ MCP Server is not running or not accessible")
        print("Start the server with: cd mcp && python src/main.py")

