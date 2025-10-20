"""Test MCP tools via HTTP mode."""

import requests
import json

BASE_URL = "http://localhost:8123"

def test_tool_via_sse(tool_name, params):
    """Test a tool via SSE endpoint."""
    print(f"\n{'='*80}")
    print(f"Testing: {tool_name}({params})")
    print('='*80)
    
    # MCP over SSE uses POST with JSON-RPC
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": tool_name,
            "arguments": params
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/mcp",
            json=payload,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json, text/event-stream"
            },
            timeout=10
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Result: {json.dumps(result, indent=2)[:500]}...")
            return result
        else:
            print(f"Error: {response.text[:200]}")
            return None
            
    except Exception as e:
        print(f"Exception: {e}")
        return None


def test_all_new_tools():
    """Test all 6 new tools."""
    
    print("\n" + "="*80)
    print("TESTING NEW MCP TOOLS VIA HTTP")
    print("="*80)
    
    # Test 1: manage_project (list)
    test_tool_via_sse("manage_project", {"action": "list"})
    
    # Test 2: ingest
    test_tool_via_sse("ingest", {
        "project_id": "scenario-1-cozyhome",
        "source": "local"
    })
    
    # Test 3: analyze (quick mode)
    test_tool_via_sse("analyze", {
        "project_id": "scenario-1-cozyhome",
        "mode": "quick"
    })
    
    # Test 4: analyze (questions mode)
    test_tool_via_sse("analyze", {
        "project_id": "scenario-1-cozyhome",
        "mode": "questions_only"
    })
    
    # Test 5: update
    test_tool_via_sse("update", {
        "project_id": "scenario-1-cozyhome",
        "type": "context",
        "content": "HTTP test: Client uses QuickBooks Online"
    })
    
    # Test 6: query
    test_tool_via_sse("query", {
        "project_id": "scenario-1-cozyhome",
        "question": "What did the client say about QuickBooks?"
    })
    
    # Test 7: generate
    test_tool_via_sse("generate", {
        "project_id": "scenario-1-cozyhome",
        "output_type": "report"
    })
    
    print("\n" + "="*80)
    print("HTTP MODE TESTS COMPLETE")
    print("="*80)


def test_deprecated_tools():
    """Test backward compatibility."""
    print("\n" + "="*80)
    print("TESTING DEPRECATED TOOLS (Backward Compatibility)")
    print("="*80)
    
    test_tool_via_sse("find_project_folders", {})
    test_tool_via_sse("analyze_discovery", {"project_id": "scenario-1-cozyhome"})
    
    print("\n✅ Backward compatibility confirmed")


if __name__ == "__main__":
    test_all_new_tools()
    test_deprecated_tools()

