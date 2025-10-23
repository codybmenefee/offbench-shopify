# Convex Demo Sync Fix - Testing Instructions

## What Was Fixed

**Bug**: `sync_to_convex()` was returning `convex_project_id: null` because the Convex `projects:create` mutation requires a `confidence` field, but the code wasn't providing it.

**Fix**: Added `confidence: 0` to the project creation arguments in `mcp/src/persistence/convex_sync.py` line 76.

## How to Test the Fix

### Step 1: Restart the MCP Server

The MCP server needs to be restarted to load the updated code.

**Option A: If using Cursor with MCP**
1. Close Cursor completely
2. Reopen Cursor
3. The MCP server will restart automatically

**Option B: If running MCP server manually**
```bash
# Stop the current server (Ctrl+C)
# Then restart it:
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
export DEMO_MODE=true
cd mcp
source venv/bin/activate
python src/main.py
```

### Step 2: Run the Test Script

```bash
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
export DEMO_MODE=true
python test_demo_sync.py
```

This will:
- ✅ Verify demo mode is enabled
- ✅ Verify Convex is configured
- ✅ Load the project from local state
- ✅ Test sync_project_metadata (should return valid ID now)
- ✅ Perform full sync of all components

### Step 3: Verify in Convex Dashboard

1. Open https://dashboard.convex.dev
2. Navigate to your deployment (animated-scorpion-19)
3. Go to Data tab
4. Check these tables:

**projects table:**
- Look for `scenarioId = "scenario-6-enterprise-full"`
- Verify `orgId = "demo-org"`
- Verify `confidence = 79.0` (or similar)
- Verify counts populated

**conflicts table:**
- Filter by project
- Should see 1 conflict about "Inventory System of Record"
- Should have `resolution` field populated
- Should have `orgId = "demo-org"`

**ambiguities table:**
- Should see 9 entries
- All should have `orgId = "demo-org"`

**documents table:**
- Should see 7 documents
- All should have `orgId = "demo-org"`

**questions table:**
- Should see extracted questions
- All should have `orgId = "demo-org"`

### Step 4: Test via MCP Tools

Alternatively, use the MCP tools directly in Cursor:

```
1. Ensure DEMO_MODE=true is set in your environment
2. Restart the MCP server (restart Cursor)
3. Run these MCP commands:

# Ingest and analyze (if not already done)
mcp_OffBench_ingest(project_id="scenario-6-enterprise-full", source="local")
mcp_OffBench_analyze(project_id="scenario-6-enterprise-full", mode="full")

# Sync to Convex
mcp_OffBench_sync_to_convex(project_id="scenario-6-enterprise-full", sync_type="full")

# Should now return:
# {
#   "project_id": "scenario-6-enterprise-full",
#   "sync_type": "full",
#   "convex_project_id": "k17xxxx..." (actual Convex ID),
#   "synced_components": ["metadata", "analysis", "documents", "questions"],
#   "gaps_synced": 0,
#   "conflicts_synced": 1,
#   "ambiguities_synced": 9,
#   "documents_synced": 7,
#   "questions_synced": 3,
#   "message": "Successfully synced 4 component(s) to Convex"
# }
```

### Step 5: Verify in Portal Frontend

1. Open your portal frontend URL
2. Navigate to Projects page
3. Look for "6 Enterprise Full" project
4. Click into it
5. Verify you can see:
   - Project details with 79% confidence
   - 1 conflict with resolution visible
   - 9 ambiguities listed
   - 7 documents
   - Questions tab populated

## Expected Results

✅ **Before fix**: `convex_project_id: null`, only metadata synced
✅ **After fix**: Valid Convex project ID returned, all components synced

## Troubleshooting

### If sync still returns null:

1. **Check if server restarted**: 
   ```bash
   # The server should show this on startup:
   # "🏠 Local environment detected - using test-data folder"
   ```

2. **Verify DEMO_MODE is set**:
   ```bash
   echo $DEMO_MODE
   # Should output: true
   ```

3. **Check Convex logs in dashboard** for any mutation errors

4. **Manually test the fix**:
   ```bash
   cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
   export DEMO_MODE=true
   python test_demo_sync.py
   ```

### If you see "Project not found" error:

Run ingestion and analysis first:
```bash
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
export DEMO_MODE=true
python test_resolution_workflow.py --scenario scenario-6-enterprise-full --run-full --demo
```

## Summary

The fix is complete and committed. The only remaining step is to restart the MCP server and re-run the sync. The sync should now successfully create the project in Convex with `orgId="demo-org"` and sync all analysis data (conflicts, ambiguities, gaps, documents, questions).

