# 🎯 Start Here: Evaluation Testing Guide

## Quick Overview

You now have a complete evaluation framework to test the Resolution & Clarification implementation with AI agents (Cursor, ChatGPT, etc.).

**What's Ready:**
- ✅ 3 ready-to-use agent prompts
- ✅ Automated test runner
- ✅ Manual verification checklists
- ✅ Teardown procedures
- ✅ Comprehensive documentation

---

## 🚀 Quick Start (10 Minutes)

### Option 1: Single Scenario Test (Recommended First)

1. **Enable Demo Mode** (tags data for portal demo)
```bash
export DEMO_MODE=true
```

2. **Start Services**
```bash
# Terminal 1: MCP Server
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
source mcp/venv/bin/activate
python mcp/src/main.py

# Terminal 2: Convex
cd mcp/convex
convex dev
```

2. **Open Agent Prompt**
```bash
# View the prompt
cat agent-prompts/SCENARIO-A-BASIC-CONFLICT.md
```

3. **Copy & Paste to AI Agent**
- Open Cursor AI or ChatGPT (with MCP access)
- Copy the prompt from the "Copy-Paste This Prompt" section
- Paste and let it run

4. **Manual Verification**
- Follow the verification steps in the scenario file
- Check Convex dashboard: https://dashboard.convex.dev
- Verify no hallucinations

5. **Teardown**
```bash
# Clean local state
python test_resolution_workflow.py --scenario scenario-6-enterprise-full --wipe-only

# Clean demo data from Convex
python clean_demo_data.py --execute
```

**Time**: ~5-10 minutes  
**Success**: Agent finds conflict and resolution without hallucinating

---

### Option 2: Automated Full Suite (Recommended After Single Test)

```bash
# Run all scenarios with manual verification checkpoints
./run_eval_scenarios.sh
```

**Time**: ~30-40 minutes  
**Success**: All scenarios pass verification

---

## 📁 What's Included

### Documentation
```
├── AGENT-EVAL-FRAMEWORK.md      # Complete framework (60+ pages)
├── VALIDATION-TEST-PLAN.md      # Detailed test plan
├── TEST-RESULTS-SUMMARY.md      # Current test results
├── START-HERE-EVAL.md          # This file
```

### Agent Prompts (Copy-Paste Ready)
```
├── agent-prompts/
│   ├── README.md                       # Quick reference
│   ├── SCENARIO-A-BASIC-CONFLICT.md    # Conflict detection
│   ├── SCENARIO-B-AMBIGUITY-CLARIFICATION.md  # Ambiguity detection
│   └── SCENARIO-C-USER-RESOLUTION.md   # User workflow
```

### Test Infrastructure
```
├── test_resolution_workflow.py  # Python test runner
├── run_eval_scenarios.sh       # Bash automated runner
├── test-data/
│   └── scenario-6-enterprise-full/    # Test documents
```

---

## 🎓 Scenarios Explained

### Scenario A: Basic Conflict (5 min) 
**Tests**: Can AI find a conflict and its resolution?

**Expected**:
- ✅ Finds "Inventory System of Record" conflict
- ✅ Finds resolution in decision email
- ✅ No hallucination

**Use When**: First test, validating core functionality

---

### Scenario B: Ambiguity Clarification (5 min)
**Tests**: Can AI detect vague terms and find clarifications?

**Expected**:
- ✅ Finds "real-time" and clarification (30 seconds)
- ⚠️ May miss some clarifications (pattern limitation, not bug)
- ✅ Doesn't make up clarifications

**Use When**: Testing ambiguity detection, checking for hallucinations

---

### Scenario C: User Resolution (10 min)
**Tests**: Can users add their own resolutions?

**Expected**:
- ✅ User can provide resolution via update()
- ✅ Resolution stored and synced
- ✅ Resolution retrievable later

**Use When**: Testing the augmented workflow (AI + human)

---

## ✅ What to Check

### Critical (Must Pass)
- [ ] **No Hallucination**: Every resolution/clarification exists in source docs
- [ ] **Sync Works**: Data appears in Convex
- [ ] **Source Tracking**: Documents correctly referenced
- [ ] **User Updates**: Manual resolutions work

### Important (Should Pass)
- [ ] **AI Detection**: Finds at least some resolutions/clarifications
- [ ] **Timeline Events**: Logged correctly
- [ ] **Status Fields**: Accurate (open/resolved/clarified)

### Nice-to-Have
- [ ] **High Accuracy**: Finds 80%+ of available clarifications
- [ ] **Gap Detection**: Identifies missing information
- [ ] **Confidence Scores**: In expected range

---

## 🔍 How to Verify Results

### 1. Check Agent Response
- Did it find conflicts/ambiguities?
- Did it report resolutions/clarifications?
- Are source documents referenced?

### 2. Verify in Source Documents
```bash
# Search for reported text
grep -r "TEXT_FROM_AGENT" test-data/scenario-6-enterprise-full/

# If found → PASS
# If not found → FAIL (hallucination)
```

### 3. Check Convex Dashboard
1. Open: https://dashboard.convex.dev
2. Go to your deployment
3. Check tables:
   - `conflicts` - Has resolution field?
   - `ambiguities` - Has clarification field?
   - `contextEvents` - Events logged?

### 4. Verify Data Quality
- [ ] Resolution text matches source exactly
- [ ] No truncation
- [ ] No corruption
- [ ] Status fields correct

---

## 🧹 Teardown Procedures

### After Each Test
```bash
# Clean specific scenario
python test_resolution_workflow.py --scenario SCENARIO_NAME --wipe-only
```

### Clean All Test Data
```bash
# Remove all working files
rm -rf test-data/*/working/*
rm -rf test-data/*/implementation/*

# Restart with clean state
pkill -f "python.*main.py"
python mcp/src/main.py
```

### Reset Convex (If Needed)
- Manual: Use Convex dashboard to delete records
- Or: Let data accumulate (it's just test data)

---

## 📊 Document Your Results

Use this template for each test run:

```markdown
# Test Run: [Date]

## Scenario: [A/B/C]
**Agent**: [ ] Cursor [ ] ChatGPT
**Tester**: __________

### Results
- [ ] PASS: No hallucinations
- [ ] PASS: Sync successful
- [ ] PASS: Data accurate

### Metrics
- Conflicts found: ____ / ____ expected
- Resolutions found: ____ / ____ expected
- Ambiguities found: ____ / ____ expected
- Clarifications found: ____ / ____ expected

### Issues
1. ________________________________
2. ________________________________

### Overall
[ ] PASS | [ ] CONDITIONAL PASS | [ ] FAIL

**Notes**: ______________________________
```

---

## 🎯 Success Criteria

### Minimum Viable (Block Deployment if Fail)
- ✅ No hallucinations (100% required)
- ✅ Sync works (data reaches Convex)
- ✅ User updates work
- ✅ Source tracking works

### Production Ready (Should Pass)
- ✅ AI finds at least 1 resolution correctly
- ✅ AI finds at least 1 clarification correctly
- ✅ Timeline events logged
- ✅ No data corruption

### Optimal (Nice to Have)
- ✅ AI finds 60%+ of available clarifications
- ✅ Gap detection works
- ✅ Confidence scores accurate

---

## 🚨 Red Flags (Stop and Fix)

### Critical Issues
- ❌ **Hallucination**: Agent makes up resolutions not in documents
- ❌ **Data Loss**: Information not saved or corrupted
- ❌ **Sync Failure**: Data doesn't reach Convex
- ❌ **Crash**: System fails during execution

### Warning Signs
- ⚠️ **Low Accuracy**: Finds <30% of available clarifications
- ⚠️ **Missing Events**: Timeline not logging
- ⚠️ **Wrong Sources**: Documents misreferenced

---

## 📚 Documentation Map

**For Running Tests**:
1. This file (`START-HERE-EVAL.md`)
2. `agent-prompts/README.md` - Quick reference
3. Individual scenario files in `agent-prompts/`

**For Understanding System**:
1. `IMPLEMENTATION-SUMMARY.md` - What was built
2. `TEST-RESULTS-SUMMARY.md` - Current state
3. `AGENT-EVAL-FRAMEWORK.md` - Complete framework

**For Detailed Testing**:
1. `VALIDATION-TEST-PLAN.md` - Comprehensive test plan
2. `AGENT-EVAL-FRAMEWORK.md` - All scenarios + theory

---

## 🤝 Next Steps

### After Running Tests

**If All Pass** ✅
1. Document baseline metrics
2. Deploy to production
3. Monitor first real projects
4. Iterate on patterns

**If Some Fail** ⚠️
1. Categorize: Critical vs Nice-to-Have
2. Fix critical issues
3. Document limitations
4. Re-run tests
5. Decide: Deploy or improve first

**If Major Failures** ❌
1. Don't deploy
2. Debug issues
3. Fix root causes
4. Re-run full evaluation

---

## 💡 Tips for Success

1. **Start Small**: Run Scenario A first, understand the flow
2. **Verify Everything**: Don't trust AI output blindly
3. **Check Sources**: Always verify against original documents
4. **Document Issues**: Record what fails and why
5. **Clean Between Tests**: Always teardown before re-running
6. **Be Patient**: First run takes longer as you learn the flow

---

## ❓ Need Help?

### Common Questions

**Q: Agent can't find MCP tools**  
A: Verify MCP server is running and agent has correct configuration

**Q: Convex sync fails**  
A: Check `convex dev` is running and `.env` is configured

**Q: Different results each time**  
A: Always run teardown between tests for clean state

**Q: Agent makes up resolutions**  
A: This is a **critical failure** - don't deploy, needs fixing

### Where to Look

- **Error Logs**: Check MCP server terminal output
- **Convex Dashboard**: https://dashboard.convex.dev
- **Test Output**: `test_resolution_workflow.py` output
- **Documentation**: All markdown files in this directory

---

## 🎬 Ready to Start?

```bash
# 1. Start services (2 terminals)
# Terminal 1:
python mcp/src/main.py

# Terminal 2:
cd mcp/convex && convex dev

# 2. Run first test
cat agent-prompts/SCENARIO-A-BASIC-CONFLICT.md
# Copy prompt to AI agent

# 3. Verify results
# Follow checklist in scenario file

# 4. Celebrate! 🎉
```

---

**Good luck with testing!** 🚀

Remember: The goal is to validate that resolutions and clarifications are detected and stored WITHOUT HALLUCINATION. If you find the AI making things up, that's a critical issue to address before deployment.

