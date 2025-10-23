# Demo Mode - Quick Start Guide

## What is Demo Mode?

Demo mode tags all data with special IDs (`demo-user`, `demo-org`) so it appears in your portal's demo environment and can be easily cleaned up after testing.

**Perfect for**:
- Testing with AI agents and seeing results in portal
- Evaluation sessions without polluting production data
- Repeatable testing (test → verify → clean → repeat)
- Demo/presentation preparation

---

## 🚀 Quick Start (3 Steps)

### Step 1: Enable Demo Mode
```bash
export DEMO_MODE=true
```

### Step 2: Run Test
```bash
# Option A: Automated test with demo tagging
python test_resolution_workflow.py --run-full --demo

# Option B: Start MCP server in demo mode and use agent prompts
python mcp/src/main.py  # Picks up DEMO_MODE env var
```

### Step 3: Clean Up
```bash
# Clean demo data from Convex
python clean_demo_data.py --execute

# Clean local state
python test_resolution_workflow.py --wipe-only
```

**That's it!** ✅

---

## How Demo Mode Works

### With Environment Variable
```bash
# Set before starting MCP server
export DEMO_MODE=true
export DEMO_USER_ID=demo-user  # Optional
export DEMO_ORG_ID=demo-org    # Optional

# Start server
python mcp/src/main.py

# All data synced to Convex will be tagged:
# {
#   "userId": "demo-user",
#   "orgId": "demo-org", 
#   "isDemo": true
# }
```

### With Test Script Flag
```bash
# Use --demo flag
python test_resolution_workflow.py --run-full --demo

# Automatically sets DEMO_MODE=true for that run
```

### With .env File
```bash
# Edit mcp/.env
DEMO_MODE=true
DEMO_USER_ID=demo-user
DEMO_ORG_ID=demo-org

# Restart MCP server to pick up changes
```

---

## Complete Workflow Example

### Testing Session with Demo Mode

```bash
# ============================================
# SETUP
# ============================================

# 1. Enable demo mode
export DEMO_MODE=true

# 2. Start services
# Terminal 1: MCP Server
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
source mcp/venv/bin/activate
python mcp/src/main.py

# Terminal 2: Convex
cd mcp/convex
convex dev

# ============================================
# RUN TESTS
# ============================================

# 3. Run automated test
python test_resolution_workflow.py --run-full --demo

# 4. Or use AI agent with prompts
# Open: agent-prompts/SCENARIO-A-BASIC-CONFLICT.md
# Copy prompt to Cursor/ChatGPT
# Agent executes with demo tagging

# ============================================
# VERIFY
# ============================================

# 5. Check portal (if available)
# Open portal
# Filter by: orgId = "demo-org"
# See your test data!

# 6. Check Convex dashboard
# Open: https://dashboard.convex.dev
# Go to Data tab
# Filter projects by: orgId = "demo-org"
# See demo data tagged properly

# ============================================
# CLEANUP
# ============================================

# 7. Clean demo data from Convex
python clean_demo_data.py --execute

# 8. Clean local state
python test_resolution_workflow.py --wipe-only

# 9. Verify cleanup
python clean_demo_data.py
# Should show: "No demo data found"

# ============================================
# REPEAT
# ============================================

# Now you can run tests again with clean state!
python test_resolution_workflow.py --run-full --demo
```

---

## Verification: Is Demo Mode Working?

### Check 1: Configuration
```bash
python3 << 'EOF'
import sys, os
os.environ["DEMO_MODE"] = "true"
sys.path.insert(0, "mcp/src")
from config import config

print(f"Demo Mode: {config.is_demo_mode()}")
print(f"Demo Context: {config.get_demo_context()}")
EOF
```

**Expected Output**:
```
Demo Mode: True
Demo Context: {'userId': 'demo-user', 'orgId': 'demo-org', 'isDemo': True}
```

### Check 2: Data Tagging
After running a test in demo mode:

```bash
# Open Convex dashboard
# Navigate to 'projects' table
# Look at any recent record

# Should see:
{
  "_id": "...",
  "name": "Enterprise Shopify Plus Migration",
  "scenarioId": "scenario-6-enterprise-full",
  "userId": "demo-user",      ← Demo tag!
  "orgId": "demo-org",        ← Demo tag!
  ...
}
```

### Check 3: Portal Display
- Open portal
- Add filter: `orgId = "demo-org"`
- Should see test projects
- Demo badge/indicator should show (if portal supports it)

---

## Cleaning Demo Data

### Automatic Cleanup
```bash
# Preview what will be deleted
python clean_demo_data.py

# Actually delete
python clean_demo_data.py --execute
```

### Manual Cleanup via Convex Dashboard

**Step-by-Step**:

1. **Open Dashboard**: https://dashboard.convex.dev
2. **Navigate to Data tab**
3. **For each table** (in order):

**Order matters** (delete in this sequence):
```
1. deliverables
2. contextEvents  
3. documents
4. questions
5. gaps
6. ambiguities
7. conflicts
8. projects
```

**For each table**:
- Click on table name
- Add filter: `orgId` equals `demo-org`
- Select all matching records
- Click "Delete" button
- Confirm deletion

### Quick Manual Cleanup Script
```bash
# Open Convex dashboard and run in browser console:
// Not implemented yet - use manual method above
```

---

## Custom Demo IDs for Different Tests

### Use Case: Multiple Concurrent Tests

```bash
# Test A
export DEMO_ORG_ID=demo-scenario-a
python test_resolution_workflow.py --run-full --demo

# Test B (different data set)
export DEMO_ORG_ID=demo-scenario-b
python test_resolution_workflow.py --scenario scenario-1-cozyhome --run-full --demo

# Clean specific test
python clean_demo_data.py --demo-org demo-scenario-a --execute
```

### Use Case: Team Testing

```bash
# Tester 1
export DEMO_USER_ID=demo-alice
export DEMO_ORG_ID=demo-team
python test_resolution_workflow.py --run-full --demo

# Tester 2
export DEMO_USER_ID=demo-bob
export DEMO_ORG_ID=demo-team
python test_resolution_workflow.py --run-full --demo

# Both visible in portal under "demo-team" org
```

---

## Integration with Evaluation Framework

Demo mode works with all evaluation tools:

### With Automated Tests
```bash
python test_resolution_workflow.py --run-full --demo
./run_eval_scenarios.sh  # Uses DEMO_MODE env var
```

### With Agent Prompts
```bash
# Enable demo mode first
export DEMO_MODE=true

# Use any agent prompt - data gets tagged automatically
# See: agent-prompts/SCENARIO-*.md
```

### With Manual MCP Tools
All MCP tool calls automatically use demo context when enabled:
- `manage_project()` - Creates demo-tagged projects
- `ingest()` - Tags ingested documents
- `analyze()` - Tags analysis results
- `sync_to_convex()` - Syncs with demo tags
- `update()` - Updates with demo context

---

## Troubleshooting

### Demo Mode Not Working

**Symptom**: Data doesn't have demo tags in Convex

**Checks**:
```bash
# 1. Verify env var is set
echo $DEMO_MODE
# Should print: true

# 2. Check config loaded it
python3 -c "import sys; sys.path.insert(0, 'mcp/src'); from config import config; print(config.DEMO_MODE)"
# Should print: True

# 3. Check MCP server was started AFTER setting env var
# Restart server if env var was set after server started
```

**Fix**:
- Set env var before starting MCP server
- Or restart MCP server after setting env var
- Or use --demo flag with test script

### Can't Find Demo Data

**Symptom**: Convex dashboard shows no demo data

**Possible Causes**:
1. Demo mode wasn't enabled
2. Sync failed (check terminal output)
3. Wrong demo IDs used for search

**Check Sync Output**:
```bash
python test_resolution_workflow.py --run-full --demo
# Look for: "🎭 Demo mode enabled: {..."
# Look for: "✅ Sync complete"
```

### Demo Data Cleanup Fails

**Symptom**: Can't delete demo data

**Current Status**:
- Automated cleanup requires additional Convex mutations
- Use manual cleanup via dashboard for now

**Manual Steps**: See "Manual Cleanup via Convex Dashboard" above

---

## Best Practices

### DO ✅
- Always enable demo mode for evaluation testing
- Use consistent demo IDs for related tests
- Clean demo data between test runs
- Verify data is tagged in Convex dashboard
- Document which demo IDs are for which tests

### DON'T ❌
- Don't use demo mode in production
- Don't forget to clean demo data
- Don't mix demo and real data
- Don't reuse demo IDs for unrelated tests
- Don't leave demo data in production Convex

---

## Quick Reference

### Enable Demo Mode
```bash
export DEMO_MODE=true
# or
python script.py --demo
```

### Run Test with Demo
```bash
python test_resolution_workflow.py --run-full --demo
```

### Verify Demo Tagging
```bash
# Check config
python3 -c "import sys; sys.path.insert(0, 'mcp/src'); from config import config; print(config.get_demo_context())"

# Check Convex dashboard
# Filter by: orgId = "demo-org"
```

### Clean Demo Data
```bash
# Preview
python clean_demo_data.py

# Execute
python clean_demo_data.py --execute

# Manual via dashboard
# Filter each table by orgId = "demo-org" and delete
```

---

## Environment Variables Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `DEMO_MODE` | `false` | Enable/disable demo mode |
| `DEMO_USER_ID` | `demo-user` | Demo user identifier |
| `DEMO_ORG_ID` | `demo-org` | Demo organization identifier |

Set in:
- Shell: `export DEMO_MODE=true`
- File: `mcp/.env`
- Script: `os.environ["DEMO_MODE"] = "true"`

---

## Summary

**Demo mode makes testing easy**:

1. ✅ **Enable**: `export DEMO_MODE=true`
2. ✅ **Test**: Run any test or agent prompt
3. ✅ **Verify**: Check portal/Convex (filter by demo-org)
4. ✅ **Clean**: `python clean_demo_data.py --execute`
5. ✅ **Repeat**: Fresh state for next test

**Benefits**:
- Isolated demo data
- Easy cleanup
- Safe testing
- Portal integration
- Repeatable tests

For detailed demo mode documentation, see: `DEMO-MODE-GUIDE.md`

For evaluation framework, see: `START-HERE-EVAL.md`

---

**Ready to test?** Enable demo mode and run your first evaluation! 🚀

