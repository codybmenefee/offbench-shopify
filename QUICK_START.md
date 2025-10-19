# Quick Start Guide

## TL;DR - Get Running in 2 Minutes ⚡

### For Cursor Testing (Right Now!)

**1. Add MCP Server to Cursor:**

Go to: **Cursor Settings → Features → MCP Servers**

Paste this:
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

**2. Restart Cursor**

**3. Test in chat:**
```
"Call find_project_folders to show what scenarios are available"
```

Done! ✅

---

### For ChatGPT Apps (Later)

**1. Start HTTP server:**
```bash
cd mcp
python3 src/main.py
```

**2. Configure ChatGPT to connect to `http://localhost:8123`**

---

## Available Commands (After Setup)

Just talk naturally in Cursor chat:

```
"What projects are available?"
"Analyze scenario-1-cozyhome"
"What's the confidence score?"
"Generate a Statement of Work"
"What questions should I ask the client?"
```

The agent (me!) will call the MCP tools autonomously.

---

## Test Without MCP

Run the included test script:
```bash
cd mcp
python3 test_tools.py
```

This simulates a full workflow without needing MCP configured.

---

## Transport Modes

| Mode | Command | Use Case |
|------|---------|----------|
| **stdio** | `python3 src/main.py --stdio` | Cursor, Claude Desktop |
| **HTTP** | `python3 src/main.py` | ChatGPT Apps, Web APIs |

**Both modes use the exact same tools** - just different connection methods.

---

## Troubleshooting

**"MCP server not found"**
- Make sure you restarted Cursor after adding the config
- Check the path in the config is correct

**"Command not found: python3"**
- Try `python` instead of `python3`

**"Want to test but MCP not working"**
- Use `python3 test_tools.py` - works without MCP

---

See **USAGE_GUIDE.md** for full documentation.

