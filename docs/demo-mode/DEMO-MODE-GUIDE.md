# Demo Mode Testing Guide

## Overview

Demo Mode allows you to run evaluation tests with data properly tagged for the portal demo environment. This makes it easy to:
- Test with AI agents and see results in portal
- Identify demo data in Convex database
- Clean up demo data for fresh testing
- Avoid mixing demo data with real projects

---

## Enabling Demo Mode

### Method 1: Environment Variable

```bash
# Set in your shell
export DEMO_MODE=true
export DEMO_USER_ID=demo-user  # Optional, defaults to "demo-user"
export DEMO_ORG_ID=demo-org    # Optional, defaults to "demo-org"

# Run tests
python test_resolution_workflow.py --run-full
```

### Method 2: .env File

```bash
# Edit mcp/.env
cat >> mcp/.env << 'EOF'

# Demo Mode Configuration
DEMO_MODE=true
DEMO_USER_ID=demo-user
DEMO_ORG_ID=demo-org
EOF
```

### Method 3: Command Line Flag

```bash
# Use --demo flag with test script
python test_resolution_workflow.py --run-full --demo
```

---

## What Demo Mode Does

When demo mode is enabled:

1. **Data Tagging**: All data synced to Convex includes:
   ```json
   {
     "userId": "demo-user",
     "orgId": "demo-org",
     "isDemo": true
   }
   ```

2. **Portal Filtering**: Portal can filter to show only demo data

3. **Easy Cleanup**: All demo data can be identified and cleaned

4. **Isolation**: Demo data doesn't mix with real projects

---

## Running Demo Mode Tests

### Quick Demo Test (2 min)
```bash
# Run with demo mode enabled
python test_resolution_workflow.py --run-full --demo
```

### Full Agent Evaluation with Demo Data (20 min)

1. **Enable Demo Mode**
```bash
export DEMO_MODE=true
```

2. **Start Services**
```bash
# Terminal 1: MCP Server
python mcp/src/main.py

# Terminal 2: Convex
cd mcp/convex && convex dev
```

3. **Run Agent Test**
```bash
# Use any agent prompt from agent-prompts/
# Copy prompt to Cursor/ChatGPT
# Agent will process documents with demo tagging
```

4. **Verify in Portal**
- Open portal
- Filter by demo org: `demo-org`
- See evaluation results

5. **Clean Up Demo Data**
```bash
# Preview what will be deleted
python clean_demo_data.py

# Actually delete demo data
python clean_demo_data.py --execute
```

### Automated Demo Suite (45 min)
```bash
# Set demo mode
export DEMO_MODE=true

# Run full evaluation suite
./run_eval_scenarios.sh

# Clean up after
python clean_demo_data.py --execute
```

---

## Verifying Demo Mode

### Check Configuration
```bash
python3 << 'EOF'
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd() / "mcp" / "src"))

from config import config

print(f"Demo Mode: {config.is_demo_mode()}")
print(f"Demo Context: {config.get_demo_context()}")
EOF
```

Expected output:
```
Demo Mode: True
Demo Context: {'userId': 'demo-user', 'orgId': 'demo-org', 'isDemo': True}
```

### Check Convex Data
1. Open Convex dashboard: https://dashboard.convex.dev
2. Navigate to your deployment
3. Check any table (e.g., `projects`)
4. Look for records with:
   - `orgId` = "demo-org"
   - `userId` = "demo-user"
   - `isDemo` = true (if field exists)

---

## Cleaning Demo Data

### Preview Before Cleaning
```bash
# See what demo data exists
python clean_demo_data.py
```

Output:
```
🔍 Searching for demo data...
   Demo User ID: demo-user
   Demo Org ID: demo-org

⚠️  Note: For manual cleanup, use Convex dashboard
   Filter by: orgId = 'demo-org' or userId = 'demo-user'
```

### Manual Cleanup via Convex Dashboard

1. Open Convex Dashboard
2. Go to "Data" tab
3. For each table:
   - Add filter: `orgId` equals `demo-org`
   - Select all matching records
   - Delete selected records
4. Repeat for all tables

**Tables to Clean** (in order):
1. `deliverables`
2. `contextEvents`
3. `documents`
4. `questions`
5. `gaps`
6. `ambiguities`
7. `conflicts`
8. `projects`

### Automated Cleanup (Future)

The `clean_demo_data.py` script provides structure for automated cleanup. To enable:

1. Add Convex query functions to find demo records
2. Add Convex delete mutations
3. Update script to call these functions

---

## Custom Demo IDs

Use custom demo IDs for different testing scenarios:

```bash
# Scenario A demo
export DEMO_ORG_ID=demo-scenario-a
python test_resolution_workflow.py --run-full --demo

# Scenario B demo  
export DEMO_ORG_ID=demo-scenario-b
python test_resolution_workflow.py --run-full --demo

# Clean specific scenario
python clean_demo_data.py --demo-org demo-scenario-a --execute
```

---

## Integration with Agent Prompts

When using demo mode with AI agents, the agents don't need to know about it. Simply:

1. Enable demo mode before running agent
2. Use normal agent prompts
3. Data automatically gets tagged

**Example Workflow**:
```bash
# 1. Enable demo mode
export DEMO_MODE=true

# 2. Start MCP server (picks up env var)
python mcp/src/main.py

# 3. Use agent prompt normally
# Open agent-prompts/SCENARIO-A-BASIC-CONFLICT.md
# Copy prompt to Cursor/ChatGPT
# Agent executes, data gets demo tags automatically

# 4. Verify in portal
# Filter by demo-org

# 5. Clean up
python clean_demo_data.py --execute
```

---

## Best Practices

### DO ✅
- Always enable demo mode for evaluation testing
- Clean demo data between test runs
- Use custom demo IDs for different test scenarios
- Verify demo tagging in Convex dashboard
- Document which demo IDs are for which tests

### DON'T ❌
- Don't use demo mode for production data
- Don't mix demo and production data
- Don't forget to clean up demo data
- Don't reuse demo IDs across unrelated tests
- Don't enable demo mode in production environment

---

## Portal Integration

### Filtering Demo Data in Portal

If your portal supports filtering, add a demo mode toggle:

```typescript
// Example portal filter
const isDemoMode = searchParams.get('demo') === 'true';

const projects = isDemoMode 
  ? allProjects.filter(p => p.orgId === 'demo-org')
  : allProjects.filter(p => p.orgId !== 'demo-org');
```

### Demo Data Badge

Show visual indicator for demo data:

```typescript
{project.isDemo && (
  <Badge variant="warning">DEMO</Badge>
)}
```

---

## Troubleshooting

### Demo Mode Not Working

**Problem**: Data not tagged with demo IDs

**Check**:
```bash
# 1. Verify environment
echo $DEMO_MODE

# 2. Check config
python3 -c "import sys; sys.path.insert(0, 'mcp/src'); from config import config; print(config.DEMO_MODE)"

# 3. Check Convex data
# Look for orgId/userId in Convex dashboard
```

**Fix**:
- Ensure env var is set before starting MCP server
- Restart MCP server after setting env var
- Use --demo flag with test script

### Can't Find Demo Data

**Problem**: No demo data in Convex

**Possible Causes**:
1. Demo mode wasn't enabled
2. Convex sync failed
3. Wrong demo IDs used

**Solution**:
```bash
# Verify sync worked
python test_resolution_workflow.py --run-full --demo

# Check terminal output for:
# "🎭 Demo mode enabled: {...}"
# "✅ Sync complete"
```

### Demo Data Mixing with Real Data

**Problem**: Demo data appearing in production

**Prevention**:
- Always use dedicated demo org/user IDs
- Never use demo mode in production
- Clean demo data regularly
- Filter demo data in portal queries

**Fix**:
```bash
# Clean all demo data immediately
python clean_demo_data.py --execute

# Verify in Convex dashboard
```

---

## Example: Complete Demo Testing Session

```bash
# 1. Setup
export DEMO_MODE=true
export DEMO_ORG_ID=eval-session-$(date +%Y%m%d)

# 2. Start services
python mcp/src/main.py &  # Terminal 1
cd mcp/convex && convex dev &  # Terminal 2

# 3. Run Scenario A
python test_resolution_workflow.py --scenario scenario-6-enterprise-full --run-full --demo

# 4. Verify in portal
# Open portal, filter by demo org
# Check conflicts, resolutions, clarifications

# 5. Document results
cat > test-results-$(date +%Y%m%d).md << EOF
# Demo Test Session $(date)

## Scenario A Results
- Conflicts detected: X
- Resolutions found: Y
- Demo Org ID: $DEMO_ORG_ID

[... document findings ...]
EOF

# 6. Clean up
python clean_demo_data.py --demo-org $DEMO_ORG_ID --execute

# 7. Verify cleanup
python clean_demo_data.py --demo-org $DEMO_ORG_ID
# Should show: "No demo data found"
```

---

## Configuration Reference

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `DEMO_MODE` | `false` | Enable/disable demo mode |
| `DEMO_USER_ID` | `demo-user` | Demo user identifier |
| `DEMO_ORG_ID` | `demo-org` | Demo org identifier |

### Config Methods

```python
from config import config

# Check if demo mode enabled
config.is_demo_mode()  # Returns bool

# Get demo context
config.get_demo_context()  # Returns dict with userId, orgId, isDemo

# Get individual IDs
config.DEMO_USER_ID  # String
config.DEMO_ORG_ID   # String
```

---

## Integration with Evaluation Framework

Demo mode works seamlessly with the evaluation framework:

### With Test Scripts
```bash
# All support --demo flag
python test_resolution_workflow.py --run-full --demo
./run_eval_scenarios.sh  # Uses DEMO_MODE env var if set
```

### With Agent Prompts
```bash
# Enable before running agents
export DEMO_MODE=true

# Use normal prompts
# Data gets demo tags automatically
```

### With Manual MCP Tools
```python
# Demo mode picked up automatically
manage_project(action="create", project_id="test-1", project_name="Test")
ingest(project_id="test-1", source="local")
analyze(project_id="test-1", mode="full")
sync_to_convex(project_id="test-1", sync_type="full")

# All data tagged with demo context
```

---

## Summary

**Enable Demo Mode**:
```bash
export DEMO_MODE=true
# or
python test_resolution_workflow.py --demo
```

**Run Tests**:
- Data automatically tagged
- Visible in portal with demo filter
- Easy to identify in Convex

**Clean Up**:
```bash
python clean_demo_data.py --execute
```

**Benefits**:
- ✅ Isolated demo data
- ✅ Easy cleanup
- ✅ Safe testing
- ✅ Portal integration
- ✅ Repeatable tests

---

For more information, see:
- `START-HERE-EVAL.md` - Evaluation testing guide
- `AGENT-EVAL-FRAMEWORK.md` - Complete framework
- `agent-prompts/` - Ready-to-use prompts

