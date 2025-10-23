# 📋 Evaluation Framework - Complete Index

## 🎯 What You Have

A complete evaluation framework for testing Resolution & Clarification support with AI agents.

---

## 🚀 Start Here

**New to this?** → Read: `START-HERE-EVAL.md`

**Quick test (5 min)?** → Use: `agent-prompts/SCENARIO-A-BASIC-CONFLICT.md`

**Full evaluation (45 min)?** → Run: `./run_eval_scenarios.sh`

---

## 📁 Complete File Structure

```
offbench-shopify/
│
├── START-HERE-EVAL.md               ⭐ START HERE - Quick start guide
├── EVALUATION-INDEX.md              📋 This file - Complete index
│
├── Documentation/
│   ├── AGENT-EVAL-FRAMEWORK.md      📚 Complete framework (comprehensive)
│   ├── VALIDATION-TEST-PLAN.md      ✅ Detailed test plan
│   ├── TEST-RESULTS-SUMMARY.md      📊 Current test results & findings
│   ├── IMPLEMENTATION-SUMMARY.md    🔧 What was built
│   └── TEST-QUICK-START.md          ⚡ Quick testing guide
│
├── Agent Prompts/ (Copy-Paste Ready)
│   ├── agent-prompts/README.md                      📖 Quick reference
│   ├── agent-prompts/SCENARIO-A-BASIC-CONFLICT.md   ✅ Test 1: Conflict detection (5 min)
│   ├── agent-prompts/SCENARIO-B-AMBIGUITY-CLARIFICATION.md  ✅ Test 2: Clarifications (5 min)
│   └── agent-prompts/SCENARIO-C-USER-RESOLUTION.md  ✅ Test 3: User workflow (10 min)
│
├── Test Infrastructure/
│   ├── test_resolution_workflow.py  🐍 Python test runner
│   ├── run_eval_scenarios.sh       🔄 Automated test suite
│   └── test-data/
│       └── scenario-6-enterprise-full/   📦 Test documents (7 files)
│           ├── emails/              ✉️ Decision & clarification emails
│           ├── transcripts/         🎤 Sales & technical calls
│           ├── client-docs/         📄 RFP & brand guidelines
│           └── expected-results.json 🎯 Validation criteria
│
└── Implementation/
    ├── mcp/convex/schema.ts         ✅ Updated schema
    ├── mcp/src/models/analysis.py   ✅ Updated models
    ├── mcp/src/core/analyzer.py     ✅ Detection logic
    └── mcp/src/persistence/convex_sync.py  ✅ Sync operations
```

---

## 🎯 Three Ways to Test

### Method 1: Manual AI Agent Testing (Recommended)
**Best for**: Understanding the system, manual verification

1. Start MCP server
2. Open agent prompt file
3. Copy prompt to AI agent (Cursor/ChatGPT)
4. Watch agent execute
5. Manually verify results
6. Document findings

**Time**: 5-10 min per scenario  
**Files**: `agent-prompts/SCENARIO-*.md`

---

### Method 2: Automated Python Testing
**Best for**: Quick validation, regression testing

```bash
python test_resolution_workflow.py --run-full
```

**Time**: 2 minutes  
**Files**: `test_resolution_workflow.py`

---

### Method 3: Full Automated Suite
**Best for**: Complete evaluation, batch testing

```bash
./run_eval_scenarios.sh
```

**Time**: 30-40 minutes  
**Files**: `run_eval_scenarios.sh`

---

## 📖 Reading Order

### For Quick Start (10 min)
1. `START-HERE-EVAL.md` - Overview
2. `agent-prompts/SCENARIO-A-BASIC-CONFLICT.md` - First test
3. Run the test!

### For Complete Understanding (45 min)
1. `START-HERE-EVAL.md` - Overview
2. `IMPLEMENTATION-SUMMARY.md` - What was built
3. `TEST-RESULTS-SUMMARY.md` - Current state
4. `agent-prompts/README.md` - Test scenarios
5. Run all tests
6. `AGENT-EVAL-FRAMEWORK.md` - Deep dive

### For Comprehensive Testing (2 hours)
1. All of the above
2. `VALIDATION-TEST-PLAN.md` - Detailed test plan
3. Run manual verification for each scenario
4. Document results thoroughly

---

## ✅ What Each Document Does

| Document | Purpose | When to Use |
|----------|---------|-------------|
| `START-HERE-EVAL.md` | Quick start guide | First time setup |
| `EVALUATION-INDEX.md` | Navigation (this file) | Finding your way around |
| `AGENT-EVAL-FRAMEWORK.md` | Complete framework | Deep understanding |
| `VALIDATION-TEST-PLAN.md` | Detailed test procedures | Comprehensive testing |
| `TEST-RESULTS-SUMMARY.md` | Current test results | Understanding status |
| `IMPLEMENTATION-SUMMARY.md` | Technical changes | Understanding code |
| `agent-prompts/README.md` | Prompt quick reference | Running tests |
| `agent-prompts/SCENARIO-*.md` | Copy-paste prompts | Actual testing |

---

## 🎯 Test Scenarios Summary

### Scenario A: Basic Conflict Detection (5 min)
**File**: `agent-prompts/SCENARIO-A-BASIC-CONFLICT.md`

**Tests**:
- ✅ Conflict detection
- ✅ Resolution finding
- ✅ No hallucination
- ✅ Source tracking

**Expected**: Finds inventory conflict with resolution

---

### Scenario B: Ambiguity Clarification (5 min)
**File**: `agent-prompts/SCENARIO-B-AMBIGUITY-CLARIFICATION.md`

**Tests**:
- ✅ Ambiguity detection
- ✅ Clarification finding
- ✅ Handles missing clarifications
- ✅ No hallucination

**Expected**: Finds "real-time" clarification (30 seconds)

---

### Scenario C: User Resolution Workflow (10 min)
**File**: `agent-prompts/SCENARIO-C-USER-RESOLUTION.md`

**Tests**:
- ✅ User can add resolutions
- ✅ Data persists to Convex
- ✅ Resolutions retrievable
- ✅ Timeline events logged

**Expected**: User resolution stored and synced

---

## 🛠️ Quick Commands Reference

### Start Services
```bash
# Terminal 1: MCP Server
python mcp/src/main.py

# Terminal 2: Convex
cd mcp/convex && convex dev
```

### Run Tests
```bash
# Single automated test
python test_resolution_workflow.py --run-full

# Full suite with checkpoints
./run_eval_scenarios.sh

# Specific scenario
python test_resolution_workflow.py --scenario scenario-6-enterprise-full --run-full
```

### Teardown
```bash
# Clean specific scenario
python test_resolution_workflow.py --scenario SCENARIO_NAME --wipe-only

# Clean all
rm -rf test-data/*/working/* test-data/*/implementation/*
```

### Verify
```bash
# Check for hallucination
grep -r "REPORTED_TEXT" test-data/scenario-6-enterprise-full/

# Check Convex
open https://dashboard.convex.dev

# Check MCP server running
ps aux | grep main.py
```

---

## 📊 Success Criteria

### Must Pass (Blocking)
- [ ] No hallucinations (resolutions/clarifications exist in docs)
- [ ] Convex sync works
- [ ] User updates work
- [ ] No data corruption

### Should Pass (Important)
- [ ] AI finds at least 1 resolution
- [ ] AI finds at least 1 clarification
- [ ] Timeline events logged
- [ ] Source tracking accurate

### Nice to Have
- [ ] 60%+ clarification detection accuracy
- [ ] Gap detection works
- [ ] Confidence scores accurate

---

## 🚨 Red Flags

**Stop and fix if you see:**
- ❌ Hallucinated resolutions/clarifications
- ❌ Data not syncing to Convex
- ❌ Data corruption or loss
- ❌ System crashes

**Warning signs (investigate):**
- ⚠️ Very low accuracy (<30%)
- ⚠️ Missing timeline events
- ⚠️ Wrong source documents

---

## 💡 Pro Tips

1. **Always start with Scenario A** - simplest test, validates core
2. **Check Convex after each test** - verify data is there
3. **Search for reported text in docs** - catch hallucinations
4. **Clean between runs** - ensures consistent results
5. **Document everything** - you'll want the baseline later

---

## 📞 Next Steps

### After First Test
- [ ] Read test results
- [ ] Check Convex dashboard
- [ ] Verify no hallucinations
- [ ] Document findings

### After All Tests
- [ ] Review success criteria
- [ ] Categorize any failures
- [ ] Decide: Deploy, Improve, or Iterate
- [ ] Update baseline metrics

### For Production
- [ ] All tests pass
- [ ] Documentation complete
- [ ] Baseline metrics established
- [ ] Monitoring plan ready

---

## 🎓 Learning Path

**Beginner** (30 min):
1. Read `START-HERE-EVAL.md`
2. Run Scenario A
3. Verify results manually

**Intermediate** (90 min):
1. All beginner steps
2. Run all 3 scenarios
3. Read `TEST-RESULTS-SUMMARY.md`
4. Document findings

**Advanced** (3+ hours):
1. All intermediate steps
2. Read `AGENT-EVAL-FRAMEWORK.md`
3. Run automated suite
4. Create custom scenarios
5. Performance testing

---

## 📚 Additional Resources

**Technical Deep Dive**:
- `mcp/convex/schema.ts` - Database schema
- `mcp/src/models/analysis.py` - Data models
- `mcp/src/core/analyzer.py` - Detection logic

**Test Data**:
- `test-data/scenario-6-enterprise-full/` - Documents
- `test-data/scenario-6-enterprise-full/expected-results.json` - Criteria

**Configuration**:
- `mcp/.env` - Environment variables
- `mcp/convex/convex.json` - Convex config

---

## ✨ You're All Set!

Everything you need to validate the Resolution & Clarification implementation is ready.

**Quick Start**:
```bash
# 1. Open the guide
open START-HERE-EVAL.md

# 2. Pick a scenario
open agent-prompts/SCENARIO-A-BASIC-CONFLICT.md

# 3. Start testing!
```

---

**Questions?** Check the relevant documentation file above.

**Ready to test?** Start with `START-HERE-EVAL.md`

**Good luck! 🚀**
