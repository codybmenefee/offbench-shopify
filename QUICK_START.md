# Discovery Agent - Quick Start Guide

## 🎉 Recent Fixes (January 2025)

### ✅ Local File Support - WORKING
Auto-loading of documents from `test-data/` folder is now active. No need to manually call `ingest()` before `analyze()`.

### ✅ FunctionTool Error - FIXED
The "'FunctionTool' object is not callable" error has been resolved. All tools now work correctly through the MCP protocol.

---

## Getting Started

### 1. Start the MCP Server

**For Railway/Production:**
```bash
python mcp/src/railway_start.py
```

**For Local Development:**
```bash
cd mcp/src
python main.py
```

The server will start on `http://0.0.0.0:8123` by default.

### 2. Test with Available Projects

Five test scenarios are available in `test-data/`:
- `scenario-1-cozyhome` - Shopify + QuickBooks (Low-Med complexity)
- `scenario-2-brewcrew` - Shopify + Klaviyo (Medium complexity)
- `scenario-3-petpawz` - Shopify + ShipStation (Medium complexity)
- `scenario-4-fitfuel` - Shopify + Stocky (High complexity)
- `scenario-5-bloom` - Shopify + POS (Med-High complexity)

### 3. Run Your First Analysis

Through your MCP client (Claude Desktop, Cursor, etc.), try these commands:

```
List all available projects
```

```
Run a quick confidence check on scenario-1-cozyhome
```

```
Analyze scenario-1-cozyhome in full mode. What gaps and ambiguities do you find?
```

---

## Test Prompts by Complexity

### 🟢 Level 1: Basic (Start Here)
- "List all available projects in the test data"
- "Run a quick confidence check on scenario-1-cozyhome"
- "Show me the details of the scenario-2-brewcrew project"

### 🟡 Level 2: Document Analysis
- "Analyze scenario-1-cozyhome in full mode"
- "What gaps exist in scenario-3-petpawz?"
- "Generate prioritized questions for scenario-4-fitfuel"

### 🟠 Level 3: Information Retrieval
- "What did the client say about refunds in scenario-1-cozyhome?"
- "Which systems are mentioned in scenario-2-brewcrew?"
- "What are the main pain points in scenario-3-petpawz?"

### 🔴 Level 4: Feedback Loop
- "Add context: Client uses QuickBooks Online for scenario-1-cozyhome"
- "Answer the refund handling gap with: Refunds create credit memos"
- "Resolve the 'real-time' ambiguity: means within 5 minutes"

### 🟣 Level 5: Deliverables
- "Generate a questions document for scenario-1-cozyhome"
- "Create an analysis report for scenario-2-brewcrew"
- "Generate a simplified SOW for scenario-3-petpawz"

**Full test prompt list**: See `TEST_PROMPTS.md` for 40+ test cases

---

## Common Workflows

### Workflow 1: Quick Project Assessment
```
1. "Run a quick confidence check on scenario-1-cozyhome"
2. "What are the top 3 gaps?"
3. "Generate questions for the client"
```

### Workflow 2: Full Discovery Analysis
```
1. "Analyze scenario-2-brewcrew in full mode"
2. "What systems are identified?"
3. "Generate an analysis report"
4. "Create a simplified SOW"
```

### Workflow 3: Iterative Improvement
```
1. "Get initial confidence score for scenario-1-cozyhome"
2. "Add context: <new information>"
3. "Check new confidence score"
4. "Repeat until confidence > 80%"
5. "Generate implementation plan"
```

---

## Key Features

### ✅ Auto-Loading Documents
No need to manually ingest - just analyze!
```
analyze(project_id="scenario-1-cozyhome", mode="full")
```
The system automatically loads all `.txt` files from the project folder.

### ✅ Confidence Scoring
Get quantitative readiness metrics:
- **Overall Confidence**: 0-100%
- **Clarity**: How clear are the requirements?
- **Completeness**: Is all needed info present?
- **Alignment**: Do stakeholders agree?

### ✅ Gap Detection
Automatically identifies missing information:
- Business rules (refunds, taxes, etc.)
- Technical constraints (rate limits, auth, etc.)
- Error handling
- Success criteria
- Edge cases

### ✅ Ambiguity Surfacing
Flags vague terms that need clarification:
- "real-time", "fast", "quick"
- "scalable", "robust", "flexible"
- "soon", "later", "eventually"

### ✅ Feedback Loop
Iteratively improve confidence:
- Add general context
- Answer specific gaps
- Override incorrect findings
- Resolve ambiguities
- Auto-reanalysis on updates

### ✅ Deliverable Generation
Create client-ready documents:
- Statements of Work (SOW)
- Implementation plans
- Technical specifications
- Questions documents
- Analysis reports

---

## Tool Reference

### Core Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `manage_project` | List, create, configure projects | List all projects |
| `ingest` | Load documents (auto in analyze) | Ingest from local folder |
| `analyze` | Run discovery analysis | Analyze with auto-loading |
| `update` | Add context, answer gaps | Add context about QB Online |
| `generate` | Create deliverables | Generate SOW |
| `query` | Ask questions about docs | What did client say about X? |
| `sync_to_convex` | Sync to admin portal | Sync for observability |

### Analysis Modes

- `full` - Complete analysis with all findings
- `quick` - Confidence scores only (fast)
- `gaps_only` - Just gap detection
- `questions_only` - Prioritized questions list
- `confidence_only` - Score without details
- `compare` - Compare two projects

---

## Troubleshooting

### Issue: "Project not found"
**Solution**: Use exact folder names from `test-data/`:
```
# ✅ Correct
analyze(project_id="scenario-1-cozyhome")

# ❌ Wrong
analyze(project_id="cozyhome")
```

### Issue: "No documents found"
**Solution**: Check that `.txt` files exist in project subfolders:
- `emails/`
- `transcripts/`
- `client-docs/`

### Issue: FunctionTool error
**Solution**: Already fixed! If you see this, ensure you're using the latest code (January 2025 update).

---

## File Structure

```
offbench-shopify/
├── mcp/
│   └── src/
│       ├── main.py              # MCP server & tools
│       ├── core/
│       │   ├── analyzer.py      # Analysis engine
│       │   └── state_manager.py # Project state
│       ├── storage/
│       │   ├── local_provider.py # Local file handling
│       │   └── manager.py        # Storage factory
│       └── models/              # Data models
├── test-data/
│   ├── scenario-1-cozyhome/    # Test project 1
│   ├── scenario-2-brewcrew/    # Test project 2
│   └── ...                      # More scenarios
├── templates/                   # Deliverable templates
├── TEST_PROMPTS.md             # 40+ test cases
├── FUNCTIONTOOL_FIX.md         # Fix documentation
└── QUICK_START.md              # This file
```

---

## Next Steps

1. **Start the server** (if not already running)
2. **Try Level 1 test prompts** from `TEST_PROMPTS.md`
3. **Run a full analysis** on scenario-1-cozyhome
4. **Generate a deliverable** (questions doc or SOW)
5. **Test the feedback loop** by adding context and measuring confidence improvement

---

## Additional Resources

- **Test Prompts**: `TEST_PROMPTS.md` - 40+ organized test cases
- **Architecture**: `AGENTS.md` - System design and principles
- **Fix Details**: `FUNCTIONTOOL_FIX.md` - Recent bug fix documentation
- **Templates**: `templates/` - SOW and plan templates

---

**Status**: All systems operational ✅  
**Last Updated**: January 2025  
**Ready for Testing**: Yes 🚀

