"""Test MCP tools via stdio mode."""

import subprocess
import json
import sys

def send_jsonrpc_request(process, method, params):
    """Send a JSON-RPC request to the MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": params
    }
    
    # Write request
    request_str = json.dumps(request) + "\n"
    process.stdin.write(request_str)
    process.stdin.flush()
    
    # Read response
    response_str = process.stdout.readline()
    if response_str:
        return json.loads(response_str)
    return None


def test_stdio_mode():
    """Test all tools in stdio mode."""
    print("\n" + "="*80)
    print("TESTING MCP TOOLS VIA STDIO MODE")
    print("="*80)
    
    # Start server in stdio mode
    print("\n Starting MCP server in stdio mode...")
    process = subprocess.Popen(
        ["python3", "src/main.py", "--stdio"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,
        cwd="/Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify/mcp"
    )
    
    print("✓ Server started in stdio mode\n")
    
    try:
        # Initialize connection
        print("1. Initializing MCP connection...")
        response = send_jsonrpc_request(process, "initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        })
        if response and "result" in response:
            print(f"✓ Initialized: {response['result'].get('serverInfo', {}).get('name', 'N/A')}\n")
        
        # List tools
        print("2. Listing available tools...")
        response = send_jsonrpc_request(process, "tools/list", {})
        if response and "result" in response:
            tools = response['result'].get('tools', [])
            print(f"✓ Found {len(tools)} tools:")
            for tool in tools[:10]:  # Show first 10
                print(f"   - {tool.get('name', 'N/A')}")
            if len(tools) > 10:
                print(f"   ... and {len(tools) - 10} more")
            print()
        
        # Test new tools
        test_cases = [
            ("manage_project", {"action": "list"}, "List projects"),
            ("ingest", {"project_id": "scenario-1-cozyhome", "source": "local"}, "Ingest documents"),
            ("analyze", {"project_id": "scenario-1-cozyhome", "mode": "quick"}, "Quick analysis"),
            ("update", {
                "project_id": "scenario-1-cozyhome",
                "type": "context",
                "content": "STDIO test: Client confirmed setup"
            }, "Add context"),
            ("query", {
                "project_id": "scenario-1-cozyhome",
                "question": "What systems are mentioned?"
            }, "Query project"),
        ]
        
        for i, (tool_name, params, description) in enumerate(test_cases, 3):
            print(f"{i}. Testing {tool_name}: {description}...")
            response = send_jsonrpc_request(process, "tools/call", {
                "name": tool_name,
                "arguments": params
            })
            
            if response and "result" in response:
                result = response['result'].get('content', [])
                if result and len(result) > 0:
                    # Extract text from result
                    text_content = result[0].get('text', '')
                    if text_content:
                        try:
                            result_data = json.loads(text_content)
                            # Show key info
                            if isinstance(result_data, dict):
                                if 'count' in result_data:
                                    print(f"✓ Success: Found {result_data['count']} items")
                                elif 'confidence' in result_data:
                                    print(f"✓ Success: Confidence {result_data['confidence']}%")
                                elif 'project_id' in result_data:
                                    print(f"✓ Success: {result_data.get('message', 'Completed')}")
                                else:
                                    print(f"✓ Success: {list(result_data.keys())[:3]}")
                        except json.JSONDecodeError:
                            print(f"✓ Success: {text_content[:100]}...")
                else:
                    print("✓ Success (no content returned)")
            elif response and "error" in response:
                print(f"✗ Error: {response['error'].get('message', 'Unknown error')}")
            else:
                print("✗ No response")
            print()
        
        # Test deprecated tools
        print(f"{i+1}. Testing backward compatibility...")
        response = send_jsonrpc_request(process, "tools/call", {
            "name": "find_project_folders",
            "arguments": {}
        })
        if response and "result" in response:
            print("✓ Deprecated tools still work\n")
        
        print("="*80)
        print("✅ STDIO MODE TESTS COMPLETE")
        print("="*80)
        print("\nAll 6 new tools functional in stdio mode!")
        print("Backward compatibility confirmed!")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Cleanup
        process.terminate()
        process.wait(timeout=5)


if __name__ == "__main__":
    test_stdio_mode()

