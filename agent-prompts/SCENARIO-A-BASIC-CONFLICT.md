# Agent Prompt: Scenario A - Basic Conflict Detection

## Prerequisites

**Enable Demo Mode** (so data appears in portal demo environment):
```bash
export DEMO_MODE=true
```

Or run test with `--demo` flag:
```bash
python test_resolution_workflow.py --run-full --demo
```

## Copy-Paste This Prompt to Your AI Agent (Cursor/ChatGPT)

```
I need you to analyze discovery documents for a Shopify migration project using the OffBench MCP server.

IMPORTANT: Use ONLY the OffBench MCP tools for this task. The tools you need are:
- manage_project (from OffBench MCP)
- ingest (from OffBench MCP)
- analyze (from OffBench MCP)
- query (from OffBench MCP)
- sync_to_convex (from OffBench MCP)

Do NOT use any other tools or methods to read files or analyze data.

PROJECT: scenario-6-enterprise-full

TASK: Analyze documents to find conflicts and their resolutions.

STEPS TO EXECUTE (use OffBench MCP tools):

1. Use the OffBench manage_project tool:
   Function: manage_project
   Arguments:
   - action: "list"
   
2. Use the OffBench ingest tool to load documents:
   Function: ingest
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - source: "local"
   
3. Use the OffBench analyze tool:
   Function: analyze
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - mode: "full"
   
4. Use the OffBench query tool:
   Function: query
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - question: "What conflicts exist about the inventory system?"

5. Use the OffBench sync_to_convex tool:
   Function: sync_to_convex
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - sync_type: "full"

REPORT REQUIREMENTS:
After analysis, provide a structured report with:

1. **Conflicts Detected**
   - Total number of conflicts
   - List each conflict with:
     * Topic/description
     * Conflicting statements
     * Source documents

2. **Resolutions Found**
   - How many conflicts have resolutions?
   - For each resolution:
     * Complete resolution text
     * Source document name
     * Confidence that this is a legitimate resolution (not inferred)

3. **Key Insight**
   - What was the main conflict?
   - How was it resolved?
   - What document contained the resolution?

FORMAT: Use clear headings and bullet points. Be specific about source documents.

CRITICAL: Only report resolutions that explicitly exist in the documents. Do not infer or assume. If no resolution exists, say "NO RESOLUTION FOUND".
```

## Expected Outcome

The agent should find:
- ✅ 1 conflict about "Inventory System of Record"
- ✅ Resolution found in `emails/01-inventory-decision.txt`
- ✅ Resolution text contains: "DECISION: Shopify will be the source of truth"

## Manual Verification Steps

### 1. Check Agent Response
- [ ] Conflict clearly identified
- [ ] Resolution text quoted (not paraphrased)
- [ ] Source document correctly referenced
- [ ] No made-up or inferred content

### 2. Verify in Source Document
```bash
grep -A 10 "DECISION" test-data/scenario-6-enterprise-full/emails/01-inventory-decision.txt
```
Expected: Should see the resolution text that agent reported

### 3. Check Convex Database
Open: https://dashboard.convex.dev
- Navigate to `conflicts` table
- Find record for `scenario-6-enterprise-full`
- Verify `resolution` field populated
- Verify text matches agent's report

### 4. Evaluation Criteria
- [ ] **PASS**: Resolution found and accurate
- [ ] **PASS**: Source document correct
- [ ] **PASS**: No hallucination
- [ ] **FAIL**: If any made-up content

## Teardown After Testing

### Clean Local State
```bash
python test_resolution_workflow.py --scenario scenario-6-enterprise-full --wipe-only
```

### Clean Demo Data from Convex
```bash
# Preview what will be deleted
python clean_demo_data.py

# Execute deletion
python clean_demo_data.py --execute
```

### Manual Convex Cleanup
1. Open Convex Dashboard: https://dashboard.convex.dev
2. Go to "Data" tab
3. For each table, filter by: `orgId = 'demo-org'`
4. Select all and delete

**Tables to clean** (in order):
- deliverables → contextEvents → documents → questions → gaps → ambiguities → conflicts → projects

