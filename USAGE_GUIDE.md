# Discovery Agent MCP - Usage Guide

## Quick Start (5 Minutes)

### Step 1: Choose Your Transport

The MCP server supports **two transports**:

**For Cursor / Claude Desktop** (stdio):
```bash
cd mcp
python3 src/main.py --stdio
```

**For ChatGPT Apps** (HTTP):
```bash
cd mcp
python3 src/main.py
```
You should see: `Uvicorn running on http://0.0.0.0:8123`

---

### Step 2: Connect an AI Agent

#### Option A: Use Cursor (This IDE)

**1. Configure Cursor MCP Settings:**

Go to: **Cursor Settings → Features → MCP Servers**

Add this configuration:
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

**3. Test it:**
- In Cursor chat, say: "Call find_project_folders"
- I'll execute it and show you the results

#### Option B: Use Claude Desktop

1. **Install Claude Desktop** (if not already): https://claude.ai/download

2. **Configure MCP in Claude Desktop**:

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "discovery-agent": {
      "command": "python3",
      "args": [
        "/Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify/mcp/src/main.py",
        "--stdio"
      ],
      "env": {}
    }
  }
}
```

3. **Restart Claude Desktop**

4. **Verify**: Look for 🔨 icon in Claude chat - it indicates MCP tools are available

#### Option C: Use ChatGPT Desktop (Future - HTTP Transport)

**For deploying to ChatGPT apps**, use HTTP mode:

1. Start server in HTTP mode:
```bash
cd mcp
python3 src/main.py  # defaults to HTTP on port 8123
```

2. Configure ChatGPT to connect to `http://localhost:8123`

(See ChatGPT MCP documentation for app-specific setup)

#### Option D: Use MCP Inspector (Testing/Debugging)

For **HTTP mode testing**:
```bash
# Start server in HTTP mode
cd mcp
python3 src/main.py

# In another terminal, install and run inspector
npm install -g @modelcontextprotocol/inspector
mcp-inspector http://localhost:8123
```

Opens a web UI where you can test each tool manually.

---

## Using the Agent (Conversational Interface)

Once connected, you interact **naturally** - the agent calls tools autonomously.

### Example 1: Analyze a Project

**You say:**
```
"Help me prepare the CozyHome project for implementation"
```

**Agent does (autonomously):**
1. Calls `find_project_folders()` → sees available scenarios
2. Calls `ingest_documents("scenario-1-cozyhome")` → loads 4 docs
3. Calls `analyze_discovery("scenario-1-cozyhome")` → analyzes
4. Calls `extract_open_questions("scenario-1-cozyhome")` → generates questions
5. Calls `prepare_deliverable("scenario-1-cozyhome", "sow")` → gets template + data, generates SOW

**Agent responds:**
```
I've analyzed CozyHome's discovery documents:

📊 **Analysis Summary**
- Documents: 4 (2 emails, 1 draft SOW, 1 product catalog)
- Confidence Score: 81%
  - Clarity: 80% (4 ambiguous terms found)
  - Completeness: 80% (2 gaps detected)
  - Alignment: 85% (1 conflict identified)

🎯 **Systems Identified**
- Shopify (e-commerce)
- QuickBooks Online (accounting)
- PayPal (payments)

⚠️ **Critical Issues**
1. CONFLICT: Sarah manages inventory in Shopify, but David (accountant) 
   says QuickBooks should be source of truth
2. GAP: No discussion of refund/return handling
3. AMBIGUITY: "Real-time sync" mentioned without specific timing

📄 **Generated Deliverable**
I've created a draft Statement of Work (89% complete):
- Business objectives captured
- Systems and data flows outlined
- 13 items need clarification

❓ **Questions for You**
1. [HIGH] Which system should be the source of truth for inventory?
2. [MEDIUM] "Real-time sync" - what's the acceptable delay?
3. [MEDIUM] How should refunds and returns be handled?
...
```

---

### Example 2: Iterative Improvement

**You say:**
```
"QuickBooks is the source of truth for inventory. 
Sync frequency should be every 15 minutes. 
Refunds should sync as credit memos within 24 hours."
```

**Agent does (autonomously):**
1. Calls `update_project_context("scenario-1-cozyhome", "...")`
2. Calls `recalculate_confidence("scenario-1-cozyhome")`
3. Calls `prepare_deliverable("scenario-1-cozyhome", "sow")` → regenerates SOW with new context

**Agent responds:**
```
Great! I've updated the project context.

📈 **Confidence Improved**
- Previous: 81%
- New: 85%
- Improvement: +4%

✅ **Resolved**
- Inventory source of truth clarified (QuickBooks)
- Sync frequency defined (every 15 minutes)
- Refund handling specified (credit memos, 24hr sync)

📄 **SOW Updated**
The Statement of Work has been updated with your answers.
93% complete (was 89%).

❓ **Remaining Questions** (2)
1. What are the API rate limits for Shopify and QuickBooks?
2. How should edge cases be handled (partial refunds, split payments)?
```

---

### Example 3: Generate Multiple Deliverables

**You say:**
```
"Generate the implementation plan and technical specs too"
```

**Agent does:**
1. Calls `prepare_deliverable("scenario-1-cozyhome", "implementation-plan")` → generates plan
2. Calls `prepare_deliverable("scenario-1-cozyhome", "technical-specs")` → generates specs

**Agent responds:**
```
I've generated both documents:

📄 **Implementation Plan** (internal-implementation-plan.md)
- 5 phases: Discovery, Development, Testing, Deployment, Support
- Timeline estimates based on complexity
- Team assignments (needs actual names)
- Risk assessment included

📄 **Technical Specifications** (internal-technical-specs.md)
- API integration details
- Data mapping tables
- Error handling workflows
- Security considerations

Both documents are 85%+ complete. The remaining items need:
- Specific team member names
- Exact timeline dates
- Budget/cost details
```

---

## Available Commands (Natural Language)

You don't need to memorize tool names - just talk naturally:

### Discovery & Analysis
- ✅ "What projects are available?"
- ✅ "Analyze the CozyHome discovery documents"
- ✅ "What's the confidence score?"
- ✅ "Show me the gaps in the discovery"
- ✅ "What questions should I ask the client?"

### Deliverable Generation
- ✅ "Generate a Statement of Work"
- ✅ "Create an implementation plan"
- ✅ "Draft the technical specifications"
- ✅ "Show me what's been generated"

### Iterative Improvement
- ✅ "Update: refunds should sync daily"
- ✅ "Add this information: [paste client email]"
- ✅ "Recalculate the confidence score"
- ✅ "Has the confidence improved?"

### Exploration
- ✅ "What systems did you identify?"
- ✅ "Summarize the pain points"
- ✅ "What are the business objectives?"
- ✅ "Show me the conflicts you found"

---

## Testing the MCP (Without AI Agent)

Use the included test script:

```bash
cd mcp
python3 test_tools.py
```

This runs a full workflow simulation and shows you what the agent would do:
```
✓ Document Parsing
✓ Project Ingestion (4 documents)
✓ Analysis (81% confidence)
✓ Template Filling (89% complete)
✓ Context Update & Recalculation
```

---

## Available Test Scenarios

```
scenario-1-cozyhome     → Shopify + QuickBooks (accounting)
scenario-2-brewcrew     → Shopify + Klaviyo (marketing)
scenario-3-petpawz      → Shopify + ShipStation (fulfillment)
scenario-4-fitfuel      → Shopify + Stocky (inventory)
scenario-5-bloom        → Shopify + Local POS
```

**Try different scenarios:**
```
"Analyze the BrewCrew project"
"What's different about PetPawz vs CozyHome?"
"Generate SOWs for all 5 scenarios"
```

---

## Troubleshooting

### "Connection refused" or "Cannot connect to MCP"

**Fix:** Make sure the MCP server is running
```bash
cd mcp
python3 src/main.py
```

### "Project not found"

**Fix:** Use exact folder names
```
✅ Correct: "scenario-1-cozyhome"
❌ Wrong: "cozyhome" or "scenario 1"
```

Or just say: "What projects are available?"

### "No analysis found"

**Fix:** Run analysis before generating deliverables
```
1. First: "Analyze scenario-1-cozyhome"
2. Then: "Generate the SOW"
```

### Server crashed or acting weird

**Fix:** Restart for clean state
```bash
# Ctrl+C to stop
python3 src/main.py  # Start fresh
```

---

## Pro Tips

### 1. Chain Operations Naturally

**Instead of:**
```
"Ingest documents"
[wait]
"Analyze"
[wait]
"Generate SOW"
```

**Just say:**
```
"Prepare a full implementation package for CozyHome"
```

The agent will chain all necessary tools automatically.

### 2. Provide Context Conversationally

**Instead of:**
```
"Call update_project_context with: refunds sync daily"
```

**Just say:**
```
"By the way, refunds should sync daily to QuickBooks"
```

The agent understands and calls the right tool.

### 3. Ask for Summaries

```
"Summarize all 5 scenarios and their confidence scores"
"Which project is most ready for implementation?"
"What are the common gaps across all projects?"
```

### 4. Iterate Rapidly

```
"What if we make QuickBooks the source of truth instead?"
"Recalculate assuming daily sync instead of real-time"
"How does that change the confidence score?"
```

---

## Demo Workflow (30 seconds)

Perfect for showing stakeholders:

```
You: "Analyze CozyHome and tell me if we're ready to start development"

Agent: [Analyzes 4 documents]
       "Confidence is 81%. Found 1 conflict and 2 gaps. 
        Not quite ready - here are 6 questions we need answered first..."

You: "QuickBooks is source of truth, refunds sync daily, 
      use 15-minute polling"

Agent: [Updates and recalculates]
       "Confidence now 85%. Generated SOW and implementation plan.
        2 minor questions remain but we can start development."

You: "Show me the SOW"

Agent: [Displays generated SOW]
       "Here's the 93% complete SOW. Missing items are just 
        team assignments and specific dates."
```

**Total time: 30 seconds. Zero manual work.** 🚀

---

## Next Steps

1. ✅ **Start the MCP server** (python3 src/main.py)
2. ✅ **Connect your AI agent** (Cursor, Claude Desktop, or Inspector)
3. ✅ **Try the demo workflow** above
4. ✅ **Test all 5 scenarios**
5. ✅ **Iterate on gap detection** as you find patterns

---

## Need Help?

- **Check server is running**: Look for "Uvicorn running on http://0.0.0.0:8123"
- **Test tools directly**: Run `python3 test_tools.py`
- **Read tool documentation**: See `mcp/README.md`
- **Check implementation**: See `IMPLEMENTATION_SUMMARY.md`

---

**You're ready to go!** 🎉

Start the server and say: *"Show me what projects are available"*

