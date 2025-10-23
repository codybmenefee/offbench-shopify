# Agent Prompt: Scenario C - User-Provided Resolution

## Prerequisites

**Enable Demo Mode**:
```bash
export DEMO_MODE=true
```

## Copy-Paste This Prompt to Your AI Agent (Cursor/ChatGPT)

## Part 1: Create Project and Identify Issues

```
Create a new test project and identify conflicts that need resolution using the OffBench MCP server.

IMPORTANT: Use ONLY the OffBench MCP tools for this task.

TASK: Set up a new project and analyze it to find unresolved issues.

STEPS (use OffBench MCP tools):

1. Use the OffBench manage_project tool:
   Function: manage_project
   Arguments:
   - action: "create"
   - project_id: "eval-user-resolution-test"
   - project_name: "User Resolution Eval Test"

2. Use the OffBench ingest tool:
   Function: ingest
   Arguments:
   - project_id: "eval-user-resolution-test"
   - source: "local"
   - location: "" (will use default path)
   Note: This will copy from scenario-6-enterprise-full

3. Use the OffBench analyze tool:
   Function: analyze
   Arguments:
   - project_id: "eval-user-resolution-test"
   - mode: "full"

4. Use the OffBench query tool:
   Function: query
   Arguments:
   - project_id: "eval-user-resolution-test"
   - question: "List all conflicts found. For each conflict, tell me if it has a resolution or not."

REPORT:
List each conflict with:
- Conflict description
- Resolution status (HAS RESOLUTION / NO RESOLUTION)
- If no resolution: Brief description of what needs to be decided

After reporting, STOP and wait for next instructions.
```

## Manual Verification Checkpoint 1
- [ ] Project created successfully
- [ ] Documents ingested
- [ ] Analysis completed
- [ ] Agent correctly identifies conflicts and their resolution status

---

## Part 2: Add User-Provided Resolution

**After verifying Part 1 worked, give the agent this prompt:**

```
Now I'll provide a resolution for one of the unresolved conflicts using OffBench MCP.

IMPORTANT: Use OffBench MCP tools only.

TASK: Add a user-provided resolution to the inventory conflict.

STEPS (use OffBench MCP tools):

1. Use the OffBench update tool:
   Function: update
   Arguments:
   - project_id: "eval-user-resolution-test"
   - type: "resolve"
   - target_id: "inventory"
   - content: "After extensive discussion with the technical team and executive stakeholders, we have made the final decision that Shopify will serve as the authoritative source of truth for all inventory levels. This decision is based on the need for true real-time inventory updates across all sales channels, Shopify's superior webhook infrastructure for instant notifications, and the native integration capabilities with our warehouse management system. SAP will receive hourly inventory snapshots for financial reporting purposes but will not manage inventory levels."

2. Use the OffBench query tool to verify:
   Function: query
   Arguments:
   - project_id: "eval-user-resolution-test"
   - question: "Show me the resolution for the inventory conflict"

3. Use the OffBench sync_to_convex tool:
   Function: sync_to_convex
   Arguments:
   - project_id: "eval-user-resolution-test"
   - sync_type: "full"

REPORT:
1. Update function response
2. Whether the resolution is now visible in the project
3. New confidence score (if available)
4. Confirmation that sync completed
```

## Manual Verification Checkpoint 2

### 1. Check Agent Response
- [ ] Update function returned success
- [ ] `resolved_item_type` indicated "conflict"
- [ ] Agent confirmed resolution is stored
- [ ] Sync completed successfully

### 2. Verify Convex Database
```bash
# Open Convex dashboard
# Navigate to: conflicts table
# Filter: projectId = "eval-user-resolution-test"
```

Check:
- [ ] Conflict record exists
- [ ] `resolution` field populated with exact text provided
- [ ] `status` = "resolved"
- [ ] Resolution text is complete (not truncated)

### 3. Check Timeline Events
```bash
# Convex dashboard: contextEvents table
# Filter: projectId = "eval-user-resolution-test"
# Filter: eventType = "conflict_resolved"
```

Verify:
- [ ] Event logged
- [ ] Timestamp is recent (within last few minutes)
- [ ] Event description mentions inventory conflict
- [ ] Metadata includes relevant details

---

## Part 3: Verification and Cleanup

**After verifying Part 2, give the agent this prompt:**

```
Verify the resolution was stored correctly and clean up using OffBench MCP tools.

STEPS (use OffBench MCP tools):

1. Use the OffBench generate tool:
   Function: generate
   Arguments:
   - project_id: "eval-user-resolution-test"
   - output_type: "analysis_snapshot"
   - format: "json"

2. Use the OffBench query tool:
   Function: query
   Arguments:
   - project_id: "eval-user-resolution-test"
   - question: "Give me a complete summary of the inventory conflict including its resolution and who resolved it (user vs AI detection)"

3. Report what you find about the resolution storage

After reporting, acknowledge that you're ready for cleanup.
```

## Manual Verification Checkpoint 3
- [ ] Analysis snapshot includes resolution in JSON
- [ ] Query returns the resolution correctly
- [ ] Agent can identify this was user-provided (not AI-detected)

## Teardown
```bash
python3 << 'EOF'
from mcp.src.core.state_manager import ProjectStateManager
state_mgr = ProjectStateManager()
state_mgr.delete_project("eval-user-resolution-test")
print("✅ Test project deleted")
EOF
```

Or use the test script:
```bash
python test_resolution_workflow.py --scenario eval-user-resolution-test --wipe-only
```

## Evaluation Criteria

### Must Pass
- [ ] User resolution stored in project state
- [ ] Resolution synced to Convex
- [ ] Resolution retrievable via query
- [ ] Timeline event logged
- [ ] No data loss or corruption

### Quality Checks
- [ ] Resolution text matches exactly what was provided
- [ ] No truncation of long resolution text
- [ ] Status correctly updated to "resolved"
- [ ] Confidence score improved (if calculated)

### Overall Result
- [ ] **PASS**: All must-pass criteria met
- [ ] **FAIL**: Any data loss, corruption, or sync failure

## Notes

This scenario tests the complete user workflow:
1. User identifies a gap in automated detection
2. User provides additional context/resolution
3. System stores and persists the information
4. System makes it available for queries and reports

This is a critical workflow for augmenting AI detection with human expertise.

