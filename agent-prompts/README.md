# Agent Evaluation Prompts - Quick Reference

## Overview

This directory contains ready-to-use prompts for testing the **OffBench MCP server** with AI agents (Cursor, ChatGPT, etc.).

Each prompt is designed to be **copy-pasted directly** to an AI agent with access to the OffBench MCP tools.

**Important**: All prompts instruct the agent to use **ONLY OffBench MCP tools** to ensure proper testing of the MCP functionality.

## Available Scenarios

| Scenario | File | Focus | Difficulty | Time |
|----------|------|-------|------------|------|
| **A** | `SCENARIO-A-BASIC-CONFLICT.md` | Conflict detection & resolution | Easy | 5 min |
| **B** | `SCENARIO-B-AMBIGUITY-CLARIFICATION.md` | Ambiguity detection & clarification | Easy | 5 min |
| **C** | `SCENARIO-C-USER-RESOLUTION.md` | User-provided resolution workflow | Medium | 10 min |

## Quick Start

### 1. Prerequisites

**Start OffBench MCP Server:**
```bash
# Terminal 1: OffBench MCP Server
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
source mcp/venv/bin/activate
python mcp/src/main.py  # Keep running - this is the OffBench MCP server

# Terminal 2: Convex
cd mcp/convex
convex dev  # Keep running
```

**Verify OffBench MCP is Available:**
- In Cursor: Check Settings → MCP → Should see "OffBench" server
- In ChatGPT: Verify MCP connection shows OffBench tools

### 2. Run a Scenario

1. Open one of the scenario files (e.g., `SCENARIO-A-BASIC-CONFLICT.md`)
2. Copy the prompt from the "Copy-Paste This Prompt" section
3. Paste it to your AI agent (Cursor AI, ChatGPT with MCP access)
4. Let the agent execute
5. Follow the manual verification steps in the scenario file
6. Document results
7. Run teardown command

### 3. Run All Scenarios (Automated)
```bash
# From project root
./run_eval_scenarios.sh
```

This will run all scenarios in sequence with manual verification checkpoints.

## What Each Scenario Tests

### Scenario A: Basic Conflict & Resolution
**Tests:**
- ✅ Agent uses OffBench MCP tools (not direct file access)
- ✅ AI can detect conflicts in documents
- ✅ AI can find explicit resolutions
- ✅ Resolutions are accurately extracted (no hallucination)
- ✅ Source documents are correctly referenced
- ✅ Data syncs to Convex properly

**Success Criteria:**
- Agent uses OffBench MCP tools only
- Finds inventory conflict
- Finds resolution in decision email
- Resolution text matches source document verbatim

---

### Scenario B: Ambiguity & Clarification
**Tests:**
- ✅ AI detects ambiguous terms (real-time, fast, scalable, etc.)
- ✅ AI finds clarifications where they exist
- ✅ AI correctly reports when clarifications don't exist
- ✅ No made-up clarifications (hallucination check)

**Success Criteria:**
- Finds "real-time" clarification (30 seconds)
- Correctly identifies terms without clarifications
- No inferred or assumed clarifications

---

### Scenario C: User Resolution Workflow
**Tests:**
- ✅ User can create projects
- ✅ User can provide resolutions via update()
- ✅ Resolutions are stored and persisted
- ✅ Resolutions sync to Convex
- ✅ Resolutions retrievable via query
- ✅ Timeline events logged

**Success Criteria:**
- User resolution stored correctly
- Text not truncated or corrupted
- Sync successful
- Retrievable in subsequent queries

---

## Evaluation Process

For each scenario:

1. **Run** - Execute the agent prompt
2. **Observe** - Watch agent's tool usage and responses
3. **Verify** - Follow manual verification steps
4. **Document** - Record results in evaluation template
5. **Teardown** - Clean up for next run

## Common Verification Steps

### Check for Hallucination
```bash
# Agent reported a resolution - verify it exists:
grep -r "EXACT_RESOLUTION_TEXT" test-data/scenario-6-enterprise-full/

# If found → PASS
# If not found → FAIL (hallucination)
```

### Check Convex Data
```bash
# Open: https://dashboard.convex.dev
# Navigate to your deployment
# Check tables: conflicts, ambiguities, contextEvents
```

Verify:
- [ ] Records exist for test project
- [ ] resolution/clarification fields populated when found
- [ ] Fields are null when not found (not made up)
- [ ] Status fields accurate
- [ ] Timeline events logged

### Check Source References
For each finding the agent reports:
- [ ] Can you find the exact text in source documents?
- [ ] Is the source document name correct?
- [ ] Is the context appropriate?

## Results Template

Use this to document each scenario run:

```markdown
## Scenario [A/B/C] Results

**Date**: ___________
**Agent**: [ ] Cursor [ ] ChatGPT [ ] Other: _____
**Tester**: ___________

### Agent Execution
- [ ] PASS: Agent completed all steps
- [ ] PASS: No errors or crashes
- [ ] PASS: Provided clear report

### Accuracy
- [ ] PASS: Conflicts detected correctly
- [ ] PASS: Resolutions accurate (no hallucination)
- [ ] PASS: Ambiguities detected correctly
- [ ] PASS: Clarifications accurate (no hallucination)
- [ ] PASS: Source documents referenced correctly

### Convex Sync
- [ ] PASS: Data synced successfully
- [ ] PASS: All fields populated correctly
- [ ] PASS: Timeline events logged
- [ ] PASS: Status fields accurate

### Issues Found
1. _______________________________________
2. _______________________________________

### Overall Result
[ ] PASS | [ ] CONDITIONAL PASS | [ ] FAIL

**Notes**: _____________________________________
```

## Troubleshooting

### Agent Can't Access MCP Tools
**Problem**: Agent says "I don't have access to those tools"

**Solution**:
- Verify MCP server is running: `ps aux | grep main.py`
- Check agent's MCP configuration
- In Cursor: Settings → MCP → Verify server URL
- In ChatGPT: Check GPT configuration has MCP enabled

### Convex Sync Fails
**Problem**: "Convex connection failed" errors

**Solution**:
```bash
# Check Convex is running
cd mcp/convex
convex dev

# Verify environment
cat ../. env | grep CONVEX_DEPLOYMENT_URL

# Test connection
python3 -c "from mcp.src.persistence.convex_client import ConvexClient; ConvexClient()"
```

### Documents Not Found
**Problem**: Agent can't ingest documents

**Solution**:
```bash
# Verify test data exists
ls -la test-data/scenario-6-enterprise-full/

# Check folder structure
ls -la test-data/scenario-6-enterprise-full/emails/
ls -la test-data/scenario-6-enterprise-full/transcripts/
ls -la test-data/scenario-6-enterprise-full/client-docs/
```

### Inconsistent Results
**Problem**: Same scenario produces different results

**Solution**:
```bash
# Always wipe before re-running
python test_resolution_workflow.py --scenario SCENARIO_NAME --wipe-only

# Restart MCP server
pkill -f "python.*main.py"
python mcp/src/main.py
```

## Success Metrics

### Per-Scenario
- **Accuracy**: Findings match source documents
- **Precision**: No hallucinations (100% requirement)
- **Completeness**: Found available resolutions/clarifications
- **Sync Success**: 100% of data synced to Convex

### Overall System
- **Consistency**: Same scenario → same results (±5%)
- **Performance**: Each scenario < 2 minutes
- **Reliability**: No crashes or data corruption
- **Usability**: Agent completes with provided prompts

## Next Steps After Testing

### If All Scenarios Pass ✅
1. System is production-ready
2. Document baseline metrics
3. Deploy to production
4. Monitor first real projects

### If Some Fail ⚠️
1. Categorize failures:
   - **Critical**: Hallucination, data loss, sync failure
   - **Important**: Low accuracy, missing features
   - **Nice-to-have**: Pattern matching improvements

2. Fix critical issues first
3. Document known limitations
4. Re-run evaluation
5. Decide: deploy with limitations or improve first

### Continuous Improvement
1. Add new scenarios from real projects
2. Refine patterns based on common misses
3. Update expected results as system improves
4. Build regression test suite

## Quick Reference Commands

### OffBench MCP Tools Reference

**Project Management** (from OffBench MCP):
```python
manage_project(action="list")
manage_project(action="create", project_id="test-1", project_name="Test")
manage_project(action="delete", project_id="test-1")
```

**Analysis Workflow** (from OffBench MCP):
```python
ingest(project_id="test-1", source="local")
analyze(project_id="test-1", mode="full")
query(project_id="test-1", question="What conflicts exist?")
update(project_id="test-1", type="resolve", target_id="inventory", content="Resolution text")
sync_to_convex(project_id="test-1", sync_type="full")
```

All these tools come from the **OffBench MCP server**. Agents should use these instead of direct file access.

### Cleanup
```bash
# Single scenario
python test_resolution_workflow.py --scenario SCENARIO_NAME --wipe-only

# All working files
rm -rf test-data/*/working/*
rm -rf test-data/*/implementation/*
```

---

## Contact & Support

For questions or issues:
1. Review `AGENT-EVAL-FRAMEWORK.md` for detailed documentation
2. Check `VALIDATION-TEST-PLAN.md` for comprehensive testing guide
3. Review `TEST-RESULTS-SUMMARY.md` for known limitations

---

**Happy Testing! 🚀**

