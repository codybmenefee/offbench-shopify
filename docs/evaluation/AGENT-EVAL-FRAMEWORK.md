# AI Agent Evaluation Framework
## Discovery Agent MCP - Resolution & Clarification Testing

## Purpose

This framework provides structured scenarios for AI agents (Cursor, ChatGPT) to use MCP tools, with manual verification checkpoints and teardown procedures for repeatable testing.

---

## Test Scenarios Overview

| Scenario | Focus Area | Difficulty | Expected Time |
|----------|-----------|------------|---------------|
| **Scenario A** | Basic conflict with explicit resolution | Easy | 5 min |
| **Scenario B** | Ambiguity with clear clarification | Easy | 5 min |
| **Scenario C** | Multiple conflicts + resolutions | Medium | 10 min |
| **Scenario D** | Complex real-world case (enterprise) | Hard | 15 min |
| **Scenario E** | Edge case: No resolutions present | Medium | 5 min |

---

## Setup Instructions

### Prerequisites
```bash
# Ensure MCP server is running
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
source mcp/venv/bin/activate

# Start the server (if not already running)
python mcp/src/main.py
```

### Verification Tools
```bash
# Check Convex connection
cd mcp/convex
convex dev  # Keep this running in separate terminal

# Python tools for manual verification
python3 -c "
from mcp.src.persistence.convex_client import ConvexClient
client = ConvexClient()
print('✅ Convex connected')
"
```

---

## Scenario A: Basic Conflict Detection & Resolution

### Scenario Context
**Project**: TechStyle Commerce  
**Issue**: Disagreement about inventory system of record  
**Expected Outcome**: Detect conflict, find resolution in decision email

### Agent Prompt Template
```
I need you to analyze discovery documents for a Shopify migration project using the Discovery Agent MCP tools.

PROJECT: scenario-6-enterprise-full

STEPS:
1. Use manage_project to list available projects
2. Use ingest to load documents from scenario-6-enterprise-full
3. Use analyze with mode="full" to analyze all documents
4. Use query to ask: "What conflicts exist about the inventory system?"
5. Report what you find about resolutions

After analysis, tell me:
- How many conflicts were detected?
- Did any conflicts have resolutions?
- What is the resolution text?
- Which document contained the resolution?
```

### Manual Verification Checklist

**Step 1: Verify Analysis Output**
```bash
# Check the agent's response
# Expected findings:
```
- [ ] Conflict detected: "Inventory System of Record"
- [ ] Resolution found: Contains "DECISION: Shopify will be the source of truth"
- [ ] Resolution is NOT hallucinated (appears in actual documents)
- [ ] Source document referenced: `01-inventory-decision.txt`

**Step 2: Verify Convex Data**
```bash
# Open Convex dashboard
# Navigate to: conflicts table
# Filter by: projectId contains "scenario-6-enterprise-full"
```
- [ ] At least 1 conflict record exists
- [ ] `resolution` field is populated (not null)
- [ ] Resolution text matches what agent reported
- [ ] `status` is "resolved"

**Step 3: Check Timeline Events**
```bash
# In Convex: contextEvents table
# Filter by: projectId and eventType = "conflict_resolved"
```
- [ ] Event logged with correct timestamp
- [ ] Event description mentions the conflict
- [ ] Metadata contains conflict details

### Expected Agent Output Format
```json
{
  "conflicts_detected": 1,
  "conflicts_with_resolutions": 1,
  "sample_resolution": {
    "topic": "Inventory System of Record",
    "resolution": "DECISION: Shopify will be the source of truth...",
    "source": "emails/01-inventory-decision.txt",
    "status": "resolved"
  }
}
```

### Teardown Procedure
```bash
# Run teardown script
python3 << 'EOF'
from mcp.src.core.state_manager import ProjectStateManager
from mcp.src.persistence.convex_client import ConvexClient

# Delete local state
state_mgr = ProjectStateManager()
state_mgr.delete_project("scenario-6-enterprise-full")
print("✅ Local state cleared")

# Note: Convex data persists for audit trail
# Manual cleanup if needed via dashboard
print("⚠️  Convex data retained - clear manually if needed")
EOF
```

**Pass Criteria**: All verification checkboxes checked ✅

---

## Scenario B: Ambiguity Clarification Detection

### Scenario Context
**Project**: TechStyle Commerce  
**Issue**: Vague performance requirements ("real-time", "fast")  
**Expected Outcome**: Detect ambiguities, find clarifications where provided

### Agent Prompt Template
```
Analyze the TechStyle Commerce project for ambiguous requirements.

PROJECT: scenario-6-enterprise-full

STEPS:
1. Ingest documents if not already loaded
2. Run analyze with mode="full"
3. Use query to ask: "What ambiguous terms were found and were they clarified?"
4. For each ambiguity, report:
   - The ambiguous term
   - Where it appeared
   - Whether clarification was found
   - The clarification text (if found)

Focus on these terms: "real-time", "fast", "scalable"
```

### Manual Verification Checklist

**Step 1: Review Agent's Findings**
- [ ] Found "real-time" ambiguity
- [ ] Clarification found for "real-time": mentions "30 seconds"
- [ ] Found "fast" ambiguity
- [ ] Found "scalable" ambiguity
- [ ] Agent reports which terms have/don't have clarifications

**Step 2: Verify Convex Data**
```bash
# Convex dashboard: ambiguities table
# Filter: projectId = "scenario-6-enterprise-full"
```
- [ ] Multiple ambiguity records exist (7-9 expected)
- [ ] "real-time" ambiguity has `clarification` field populated
- [ ] Clarification text contains "30 seconds" or similar
- [ ] Other ambiguities have null clarification (not all clarified)
- [ ] Status shows "clarified" for those with clarification, "open" for others

**Step 3: Source Document Verification**
```bash
# Manually check: emails/02-performance-requirements.txt
grep -i "30 seconds" test-data/scenario-6-enterprise-full/emails/02-performance-requirements.txt
```
- [ ] Clarification text exists in source document
- [ ] Text is not inferred or made up
- [ ] Context makes sense

### Expected Agent Output Format
```json
{
  "ambiguities_found": 9,
  "ambiguities_clarified": 1,
  "details": [
    {
      "term": "real-time",
      "context": "Real-time inventory updates across all brands",
      "clarification_found": true,
      "clarification": "Inventory updates must propagate across all brands within 30 seconds maximum",
      "source": "emails/02-performance-requirements.txt"
    },
    {
      "term": "fast",
      "clarification_found": false,
      "reason": "No specific timing found near term in documents"
    }
  ]
}
```

### Teardown
```bash
python test_resolution_workflow.py --wipe-only --scenario scenario-6-enterprise-full
```

**Pass Criteria**: At least 1 clarification found and verified in source ✅

---

## Scenario C: User-Provided Resolution Workflow

### Scenario Context
**Project**: Create new test project  
**Issue**: Agent finds conflict without resolution, user provides one  
**Expected Outcome**: User resolution stored and synced correctly

### Agent Prompt Template (Part 1: Discovery)
```
Create and analyze a new test project.

STEPS:
1. Use manage_project with action="create" to create project_id="eval-test-user-resolution"
2. Copy documents from scenario-6-enterprise-full to this new project (or use ingest)
3. Run analyze with mode="full"
4. Report all conflicts found
5. For the inventory conflict, tell me: does it have a resolution?
```

### Manual Verification Checkpoint 1
- [ ] New project created: "eval-test-user-resolution"
- [ ] Documents ingested successfully
- [ ] Conflicts detected
- [ ] Agent correctly reports if resolution exists or not

### Agent Prompt Template (Part 2: Add Resolution)
```
Now use the update tool to provide a resolution for the inventory conflict.

COMMAND:
update(
    project_id="eval-test-user-resolution",
    type="resolve",
    target_id="inventory",
    content="After consulting with the CTO and CFO, we've decided that Shopify will serve as the source of truth for inventory levels to enable true real-time updates across all sales channels."
)

Report:
1. The response from the update function
2. Whether it succeeded
3. What the new confidence score is
```

### Manual Verification Checkpoint 2

**Step 1: Check Agent Response**
- [ ] Update returned success
- [ ] `resolved_item_type` = "conflict"
- [ ] Confidence score updated

**Step 2: Verify Convex**
```bash
# Convex: conflicts table
# Find record with projectId="eval-test-user-resolution"
```
- [ ] Conflict record exists
- [ ] `resolution` field populated with user-provided text
- [ ] Resolution text matches exactly what was provided
- [ ] `status` = "resolved"

**Step 3: Check Timeline**
```bash
# Convex: contextEvents table
# Filter: projectId="eval-test-user-resolution", eventType="conflict_resolved"
```
- [ ] Event logged
- [ ] Timestamp recent (within last few minutes)
- [ ] Event description includes conflict topic

### Agent Prompt Template (Part 3: Verify)
```
Verify the resolution was stored correctly:

1. Use query to ask: "Show me the resolution for the inventory conflict"
2. Use generate with output_type="analysis_snapshot" to export the current state
3. Report what you find
```

### Manual Verification Checkpoint 3
- [ ] Agent can retrieve the resolution via query
- [ ] Resolution text matches what was provided
- [ ] Analysis snapshot JSON includes resolution

### Teardown
```bash
python3 << 'EOF'
from mcp.src.core.state_manager import ProjectStateManager
state_mgr = ProjectStateManager()
state_mgr.delete_project("eval-test-user-resolution")
print("✅ Test project deleted")
EOF
```

**Pass Criteria**: User resolution stored, synced, and retrievable ✅

---

## Scenario D: Complex Enterprise Case (Full Workflow)

### Scenario Context
**Project**: Complete enterprise migration analysis  
**Expected Outcome**: Comprehensive analysis with multiple conflicts, ambiguities, gaps

### Agent Prompt Template
```
Perform a complete discovery analysis for the TechStyle Commerce enterprise migration.

PROJECT: scenario-6-enterprise-full

WORKFLOW:
1. List projects to confirm scenario-6-enterprise-full exists
2. Ingest all documents from the project
3. Analyze with mode="full"
4. Generate a questions document for client meeting
5. Sync results to Convex

REPORT:
1. Overall confidence score and what it means
2. All conflicts found and which have resolutions
3. All ambiguities found and which have clarifications  
4. Any gaps identified
5. Top 5 questions that need client input
6. Recommendation: Is the project ready for implementation?

Be thorough and specific.
```

### Manual Verification Checklist

**Step 1: Comprehensive Analysis Check**
- [ ] Confidence score between 70-85%
- [ ] At least 1 conflict detected
- [ ] At least 1 resolution found
- [ ] 7-10 ambiguities detected
- [ ] At least 1 clarification found
- [ ] Questions extracted from gaps

**Step 2: Quality Assessment**

**Check for Hallucination**:
```bash
# Pick 3 random resolutions/clarifications the agent reported
# Search for them in source documents

grep -r "TEXT_FROM_AGENT_REPORT" test-data/scenario-6-enterprise-full/
```
- [ ] Resolution 1: Found in source ✅
- [ ] Resolution 2: Found in source ✅
- [ ] Clarification 1: Found in source ✅

**Check for Completeness**:
- [ ] Agent identified the inventory conflict
- [ ] Agent found the resolution email
- [ ] Agent noticed performance requirements clarification
- [ ] Agent generated meaningful questions

**Step 3: Deliverable Quality**
```bash
# Check generated files
ls -la test-data/scenario-6-enterprise-full/implementation/
```
- [ ] Questions document generated
- [ ] Contains specific, actionable questions
- [ ] Questions are relevant to identified gaps

**Step 4: Convex Verification**
```bash
# Dashboard check - all tables
```
- [ ] Project record exists with correct metadata
- [ ] Conflicts table populated
- [ ] Ambiguities table populated
- [ ] Questions table populated (if used)
- [ ] Documents table shows all 7 documents
- [ ] Events timeline shows analysis_completed

**Step 5: Agent Recommendation Verification**
- [ ] Agent provided clear recommendation (ready/not ready)
- [ ] Recommendation aligns with confidence score
- [ ] Justification makes sense based on findings

### Expected Agent Output Structure
```markdown
# TechStyle Commerce - Discovery Analysis Report

## Executive Summary
Confidence Score: 79%
Recommendation: PROCEED WITH CAUTION

## Key Findings

### Conflicts (1 found)
1. **Inventory System of Record**
   - Status: ✅ RESOLVED
   - Resolution: "Shopify will serve as source of truth..."
   - Source: emails/01-inventory-decision.txt

### Ambiguities (9 found, 1 clarified)
1. **"real-time" inventory sync**
   - Status: ✅ CLARIFIED
   - Clarification: "Within 30 seconds maximum"
   - Source: emails/02-performance-requirements.txt

2. **"fast" page loads**
   - Status: ⚠️ NEEDS CLARIFICATION
   - Question: What specific page load time is required?

[... continue for all items ...]

### Gaps Identified
[Agent should ideally identify but current version may not]

### Top 5 Questions for Client
1. What is the specific return/refund policy?
2. Which tax calculation service will be used?
3. How should integration failures be handled?
[... etc ...]

## Recommendation
The project has good clarity on system architecture (inventory conflict resolved) 
and some performance requirements clarified. However, significant gaps remain in:
- Business rules (returns, tax)
- Error handling
- Edge cases

**RECOMMEND**: Schedule follow-up discovery session before proceeding to implementation.
```

### Teardown
```bash
python test_resolution_workflow.py --wipe-only --scenario scenario-6-enterprise-full
rm -f test-data/scenario-6-enterprise-full/implementation/questions_*.md
```

**Pass Criteria**: Comprehensive analysis, no hallucinations, reasonable recommendation ✅

---

## Scenario E: Edge Case - No Resolutions Present

### Scenario Context
**Project**: Use a scenario WITHOUT explicit resolutions  
**Expected Outcome**: Agent correctly reports no resolutions found (no hallucination)

### Setup
```bash
# Use an existing scenario without resolutions
# OR create minimal test data
mkdir -p test-data/eval-no-resolution/{emails,transcripts,client-docs}
```

### Agent Prompt Template
```
Analyze a project that may not have all information resolved yet.

PROJECT: scenario-1-cozyhome

STEPS:
1. Ingest documents from scenario-1-cozyhome
2. Analyze with mode="full"
3. Report:
   - Any conflicts found
   - Whether resolutions exist for conflicts
   - Any ambiguities found
   - Whether clarifications exist

IMPORTANT: Only report resolutions/clarifications if they EXPLICITLY exist in documents.
Do not infer or assume anything.
```

### Manual Verification Checklist

**Critical: No Hallucination Check**
- [ ] Agent reports conflicts (if any exist)
- [ ] Agent states "no resolution found" or similar for unresolved items
- [ ] Agent does NOT make up resolutions
- [ ] Agent does NOT infer clarifications

**Convex Verification**:
```bash
# Check Convex data for scenario-1-cozyhome
```
- [ ] Conflicts have `resolution` = null (if no resolution in docs)
- [ ] Ambiguities have `clarification` = null (if no clarification in docs)
- [ ] Status remains "open" not "resolved"

**Source Document Check**:
- [ ] Manually verify: documents actually don't contain resolutions
- [ ] Agent's assessment is accurate

### Expected Agent Output
```json
{
  "conflicts_found": 2,
  "conflicts_with_resolution": 0,
  "ambiguities_found": 5,
  "ambiguities_with_clarification": 0,
  "note": "No explicit resolutions or clarifications found in documents. Recommend follow-up with client to address these items."
}
```

### Teardown
```bash
python test_resolution_workflow.py --wipe-only --scenario scenario-1-cozyhome
```

**Pass Criteria**: Agent correctly reports absence of resolutions without making them up ✅

---

## Master Evaluation Template

Use this template for each scenario run:

```markdown
# Evaluation Run: [Scenario Name]
Date: _______________
Agent: [ ] Cursor [ ] ChatGPT [ ] Other: __________
Tester: _______________

## Pre-Run Checklist
- [ ] MCP server running
- [ ] Convex connected
- [ ] Test data in place
- [ ] Previous run cleaned up

## Agent Execution
Prompt Used: [paste prompt]
Agent Response: [paste full response]

## Manual Verification Results

### Data Accuracy
- [ ] PASS: No hallucinated resolutions
- [ ] PASS: No hallucinated clarifications  
- [ ] PASS: Source documents referenced correctly
- [ ] PASS: Conflict detection accurate
- [ ] PASS: Ambiguity detection accurate

### Convex Sync
- [ ] PASS: Data synced to Convex
- [ ] PASS: Schema correct
- [ ] PASS: Timeline events logged
- [ ] PASS: Status fields accurate

### Quality Assessment
Confidence Score: _____%
Expected Range: ____% - ____%
Within Range: [ ] YES [ ] NO

Resolutions Found: ___ of ___ expected
Clarifications Found: ___ of ___ expected

### Issues Found
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________

### Overall Result
[ ] PASS - All criteria met
[ ] CONDITIONAL PASS - Minor issues, specify: __________
[ ] FAIL - Major issues, specify: __________

## Post-Run Actions
- [ ] Teardown completed
- [ ] Convex cleaned (if needed)
- [ ] Ready for next run
```

---

## Batch Testing Script

Run all scenarios in sequence:

```bash
#!/bin/bash
# File: run_eval_scenarios.sh

echo "=== Discovery Agent MCP - Evaluation Suite ==="
echo ""

scenarios=("scenario-6-enterprise-full" "scenario-1-cozyhome" "scenario-2-brewcrew")

for scenario in "${scenarios[@]}"; do
    echo "Testing: $scenario"
    echo "-----------------------------------"
    
    # Run test
    python test_resolution_workflow.py --scenario $scenario --run-full
    
    echo ""
    echo "✅ Complete. Press Enter to continue to next scenario..."
    read
    
    # Cleanup
    python test_resolution_workflow.py --scenario $scenario --wipe-only
    
    echo ""
done

echo "=== All scenarios complete ==="
```

---

## Success Metrics

### Per-Scenario Metrics
- **Accuracy**: % of resolutions/clarifications correctly identified
- **Precision**: No hallucinations (false positives)
- **Recall**: All available resolutions/clarifications found
- **Sync Success**: 100% of data synced to Convex

### Overall System Metrics
- **Consistency**: Same scenario produces same results (±5%)
- **Performance**: Each scenario completes in <2 minutes
- **Reliability**: No crashes or data corruption
- **Usability**: Agent can complete workflow with provided prompts

### Quality Thresholds
| Metric | Target | Acceptable | Fail |
|--------|--------|------------|------|
| No Hallucination | 100% | 100% | <100% |
| Resolution Detection | 80%+ | 60%+ | <60% |
| Clarification Detection | 60%+ | 40%+ | <40% |
| Sync Success | 100% | 95%+ | <95% |
| Confidence Accuracy | ±10% | ±20% | >20% off |

---

## Troubleshooting Guide

### Agent Can't Find MCP Tools
```bash
# Verify MCP server is running
ps aux | grep "python.*main.py"

# Check MCP connection in Cursor/ChatGPT settings
# Server URL should be correct
```

### Convex Sync Fails
```bash
# Check Convex is running
cd mcp/convex
convex dev

# Verify environment
cat mcp/.env | grep CONVEX
```

### Inconsistent Results
```bash
# Ensure clean state before each run
python test_resolution_workflow.py --wipe-only --scenario SCENARIO_NAME

# Restart MCP server
pkill -f "python.*main.py"
python mcp/src/main.py
```

### Agent Makes Up Resolutions
**This is a critical failure**
1. Document the hallucinated text
2. Verify it doesn't exist in any source document
3. Report as bug - analyzer needs pattern refinement
4. Do NOT deploy until fixed

---

## Next Steps After Evaluation

### If All Scenarios Pass
1. ✅ Document results
2. ✅ Create baseline metrics
3. ✅ Deploy to production
4. ✅ Monitor first real projects

### If Some Fail
1. Categorize failures (accuracy vs bugs)
2. Fix critical bugs (hallucination, sync failures)
3. Document known limitations
4. Re-run evaluation
5. Decide: deploy with limitations or improve first

### Continuous Improvement
1. Add new scenarios based on real projects
2. Refine patterns based on common misses
3. Update expected results as system improves
4. Build regression test suite

---

## Appendix: Quick Reference Commands

### Project Management
```python
# List projects
manage_project(action="list")

# Create project
manage_project(action="create", project_id="test-1", project_name="Test Project")

# Get project
manage_project(action="get", project_id="test-1")

# Delete project
manage_project(action="delete", project_id="test-1")
```

### Analysis Workflow
```python
# Ingest documents
ingest(project_id="test-1", source="local")

# Analyze
analyze(project_id="test-1", mode="full")

# Query
query(project_id="test-1", question="What conflicts exist?")

# Update/Resolve
update(project_id="test-1", type="resolve", target_id="inventory", content="Decision text")

# Sync to Convex
sync_to_convex(project_id="test-1", sync_type="full")
```

### Cleanup
```bash
# Wipe test data
python test_resolution_workflow.py --wipe-only --scenario SCENARIO_NAME

# Full cleanup
rm -rf test-data/*/working/*
rm -rf test-data/*/implementation/*
```

---

**Estimated Evaluation Time**: 
- Single scenario: 10-15 minutes
- Full suite (5 scenarios): 60-75 minutes
- With documentation: 90-120 minutes

