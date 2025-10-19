# Cursor MCP Configuration

## Quick Setup

Add this to your Cursor MCP settings:

**Path**: Cursor Settings → Features → MCP Servers

```json
{
  "mcpServers": {
    "discovery-agent": {
      "command": "python3",
      "args": [
        "/Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify/mcp/src/main.py",
        "--stdio"
      ]
    }
  }
}
```

## Testing

After restarting Cursor, you can test with:

```
What projects are available?
```

```
Generate a Statement of Work for CozyHome
```

The MCP tools will appear in the Cursor chat interface!

