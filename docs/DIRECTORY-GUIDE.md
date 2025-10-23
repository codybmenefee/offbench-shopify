# 📂 Documentation Directory Guide

## Complete File Organization

```
offbench-shopify/
│
├── 📄 README.md                      # Main project overview
├── 📄 AGENTS.md                      # Developer principles
├── 📄 DEPLOYMENT.md                  # Deployment guide
│
├── 📚 docs/                          # ALL DOCUMENTATION HERE
│   │
│   ├── 📄 README.md                  # Documentation index (START HERE)
│   ├── 📄 DIRECTORY-GUIDE.md         # This file - visual guide
│   │
│   ├── 📁 evaluation/                # Evaluation Testing Docs
│   │   ├── START-HERE-EVAL.md       ⭐ Main entry point
│   │   ├── EVALUATION-INDEX.md       📋 Navigation guide
│   │   ├── AGENT-EVAL-FRAMEWORK.md   📚 Complete framework (60+ pages)
│   │   └── VALIDATION-TEST-PLAN.md   ✅ Detailed procedures
│   │
│   ├── 📁 demo-mode/                 # Demo Mode Docs
│   │   ├── DEMO-MODE-QUICK-START.md 🚀 Quick setup (2 min)
│   │   ├── DEMO-MODE-GUIDE.md        📖 Comprehensive (15 min)
│   │   └── DEMO-MODE-COMPLETE.md     ✅ Implementation summary
│   │
│   ├── 📁 implementation/            # Technical Implementation
│   │   ├── IMPLEMENTATION-SUMMARY.md 🔧 What was built
│   │   └── DELIVERABLES-MANIFEST.md  📦 Complete file list
│   │
│   └── 📁 testing/                   # Testing Docs
│       ├── README-TESTING.md         📖 Testing overview
│       ├── TEST-QUICK-START.md       ⚡ Quick guide
│       └── TEST-RESULTS-SUMMARY.md   📊 Current results
│
├── 🤖 agent-prompts/                 # AI Agent Prompts (Copy-Paste Ready)
│   ├── README.md                     # Prompt navigation
│   ├── SCENARIO-A-BASIC-CONFLICT.md         # 5 min test
│   ├── SCENARIO-B-AMBIGUITY-CLARIFICATION.md # 5 min test
│   └── SCENARIO-C-USER-RESOLUTION.md         # 10 min test
│
├── 🧪 Test Infrastructure (Root Level for Easy Access)
│   ├── test_resolution_workflow.py   # Automated Python tester
│   ├── run_eval_scenarios.sh         # Batch test runner
│   ├── clean_demo_data.py            # Demo data cleanup
│   └── FINAL-VERIFICATION.sh         # Verify all working
│
├── 📦 test-data/                     # Test Scenarios
│   ├── scenario-6-enterprise-full/   # Comprehensive test (7 docs)
│   │   ├── README.md
│   │   ├── expected-results.json
│   │   ├── emails/ (3 files)
│   │   ├── transcripts/ (2 files)
│   │   └── client-docs/ (2 files)
│   ├── scenario-1-cozyhome/
│   └── scenario-2-brewcrew/
│
├── 💻 mcp/                           # MCP Server Implementation
│   ├── src/                          # Source code
│   │   ├── config.py ✅ (demo mode)
│   │   ├── main.py ✅ (update handler)
│   │   ├── models/analysis.py ✅ (new fields)
│   │   ├── core/analyzer.py ✅ (detection logic)
│   │   └── persistence/convex_sync.py ✅ (sync with demo)
│   │
│   ├── convex/                       # Convex Integration
│   │   ├── schema.ts ✅ (resolution/clarification)
│   │   └── mutations/
│   │       ├── conflicts.ts ✅ (resolution support)
│   │       └── ambiguities.ts ✅ (clarification support)
│   │
│   └── env.example.txt ✅ (demo mode config)
│
└── 📄 templates/                     # Generation Templates
    └── (existing template files)
```

---

## 🎯 How to Navigate

### By Purpose

**Want to test the system?**
→ Start: `docs/evaluation/START-HERE-EVAL.md`
→ Prompts: `agent-prompts/SCENARIO-A-*.md`

**Need demo mode?**
→ Quick: `docs/demo-mode/DEMO-MODE-QUICK-START.md`
→ Detailed: `docs/demo-mode/DEMO-MODE-GUIDE.md`

**Understand implementation?**
→ Summary: `docs/implementation/IMPLEMENTATION-SUMMARY.md`
→ Manifest: `docs/implementation/DELIVERABLES-MANIFEST.md`

**Run tests?**
→ Quick: `docs/testing/TEST-QUICK-START.md`
→ Results: `docs/testing/TEST-RESULTS-SUMMARY.md`

**Find your way around?**
→ Index: `docs/evaluation/EVALUATION-INDEX.md`
→ This guide: `docs/DIRECTORY-GUIDE.md`

---

### By User Type

**New User (Never tested before)**:
1. `docs/README.md` - Documentation index
2. `docs/evaluation/START-HERE-EVAL.md` - Main guide
3. `agent-prompts/SCENARIO-A-BASIC-CONFLICT.md` - First test

**Developer (Understanding code)**:
1. `docs/implementation/IMPLEMENTATION-SUMMARY.md` - What was built
2. `docs/implementation/DELIVERABLES-MANIFEST.md` - Files changed
3. Review actual code in `mcp/src/` and `mcp/convex/`

**QA/Tester (Running evaluations)**:
1. `docs/testing/README-TESTING.md` - Testing overview
2. `docs/evaluation/VALIDATION-TEST-PLAN.md` - Test procedures
3. `agent-prompts/` - All test scenarios

**Demo/Presentation (Preparing demos)**:
1. `docs/demo-mode/DEMO-MODE-QUICK-START.md` - Setup
2. `agent-prompts/` - Run evaluation scenarios
3. `clean_demo_data.py` - Cleanup after demo

---

### By Time Available

**2 minutes**:
- `docs/demo-mode/DEMO-MODE-QUICK-START.md`
- `docs/testing/README-TESTING.md`

**10 minutes**:
- `docs/evaluation/START-HERE-EVAL.md`
- `docs/implementation/IMPLEMENTATION-SUMMARY.md`

**30 minutes**:
- `docs/evaluation/AGENT-EVAL-FRAMEWORK.md`
- Run all 3 agent prompts

**2 hours**:
- Complete `docs/evaluation/VALIDATION-TEST-PLAN.md`
- Run `./run_eval_scenarios.sh`
- Document findings

---

## 📋 File Descriptions

### Evaluation Docs (`docs/evaluation/`)

**START-HERE-EVAL.md** (⭐ Main Entry Point)
- Purpose: Quick start guide for evaluation testing
- When: First time running evaluations
- Time: 10 min read
- Contents: Setup, scenarios, quick test examples

**EVALUATION-INDEX.md** (Navigation Hub)
- Purpose: Complete navigation and file index
- When: Finding specific documentation
- Time: 5 min read
- Contents: File map, learning paths, quick reference

**AGENT-EVAL-FRAMEWORK.md** (Comprehensive Framework)
- Purpose: Complete evaluation methodology
- When: Deep understanding needed
- Time: 30+ min read
- Contents: Scenarios, validation, metrics, theory

**VALIDATION-TEST-PLAN.md** (Detailed Procedures)
- Purpose: Step-by-step test procedures
- When: Running comprehensive validation
- Time: 20 min read, 60+ min execution
- Contents: 6 test suites, checklists, verification

---

### Demo Mode Docs (`docs/demo-mode/`)

**DEMO-MODE-QUICK-START.md** (Quick Reference)
- Purpose: Fast demo mode setup
- When: Need to enable demo mode quickly
- Time: 2 min read
- Contents: 3-step setup, quick commands

**DEMO-MODE-GUIDE.md** (Comprehensive Guide)
- Purpose: Complete demo mode documentation
- When: Understanding demo mode deeply
- Time: 15 min read
- Contents: How it works, integration, troubleshooting

**DEMO-MODE-COMPLETE.md** (Implementation Summary)
- Purpose: What was implemented for demo mode
- When: Technical review of demo mode
- Time: 5 min read
- Contents: Features, test results, validation

---

### Implementation Docs (`docs/implementation/`)

**IMPLEMENTATION-SUMMARY.md** (Technical Overview)
- Purpose: Complete technical implementation details
- When: Understanding what was built
- Time: 10 min read
- Contents: Code changes, data flow, AI rules

**DELIVERABLES-MANIFEST.md** (Complete File List)
- Purpose: Master list of all files modified/created
- When: Need complete audit trail
- Time: 5 min read
- Contents: 8 modified files, 18 created files

---

### Testing Docs (`docs/testing/`)

**README-TESTING.md** (Testing Overview)
- Purpose: High-level testing summary
- When: Quick understanding of testing
- Time: 3 min read
- Contents: What works, quick commands

**TEST-QUICK-START.md** (Quick Test Guide)
- Purpose: Run tests quickly
- When: Need to test fast
- Time: 2 min read
- Contents: Quick commands, validation

**TEST-RESULTS-SUMMARY.md** (Current Results)
- Purpose: Current test status and findings
- When: Reviewing test outcomes
- Time: 5 min read
- Contents: Results, limitations, recommendations

---

### Agent Prompts (`agent-prompts/`)

**README.md**
- Purpose: Prompt navigation and reference
- Contents: Scenario list, quick start, commands

**SCENARIO-A-BASIC-CONFLICT.md** (5 min test)
- Purpose: Test conflict detection and resolution
- When: First agent evaluation
- Contents: Copy-paste prompt, verification steps

**SCENARIO-B-AMBIGUITY-CLARIFICATION.md** (5 min test)
- Purpose: Test clarification detection
- When: Testing ambiguity handling
- Contents: Copy-paste prompt, hallucination checks

**SCENARIO-C-USER-RESOLUTION.md** (10 min test)
- Purpose: Test user workflow
- When: Testing manual resolution input
- Contents: 3-part prompt, full workflow

---

## 🔍 Cross-Reference Guide

### From Root README
- Points to: `docs/README.md` (documentation index)
- Points to: `docs/evaluation/START-HERE-EVAL.md` (testing)
- Points to: `docs/demo-mode/DEMO-MODE-QUICK-START.md` (demo mode)

### From docs/README.md
- Points to: All subdirectories
- Points to: Agent prompts (root level)
- Points to: Test scripts (root level)

### Within Evaluation Docs
- All link to each other
- All link back to docs/README.md
- All link to agent prompts
- All link to demo mode docs

---

## 🎯 Recommended Starting Points

### For First-Time Users
**Start**: `docs/README.md`  
**Then**: `docs/evaluation/START-HERE-EVAL.md`  
**Then**: Run a test

### For Quick Testing
**Start**: `docs/demo-mode/DEMO-MODE-QUICK-START.md`  
**Then**: `python test_resolution_workflow.py --run-full --demo`

### For Agent Evaluation
**Start**: `docs/evaluation/START-HERE-EVAL.md`  
**Then**: `agent-prompts/SCENARIO-A-BASIC-CONFLICT.md`

### For Understanding System
**Start**: `docs/implementation/IMPLEMENTATION-SUMMARY.md`  
**Then**: `docs/evaluation/AGENT-EVAL-FRAMEWORK.md`

---

## ✅ Organization Principles

### Why This Structure?

**docs/** - All documentation in one place
- Easy to find
- Clear categories
- Professional organization

**agent-prompts/** - At root level
- Quick CLI access
- Easy to open
- Frequently used

**Scripts** - At root level
- Easy to execute
- No path confusion
- Standard practice

**test-data/** - At root level
- Logical location
- Consistent with existing structure
- Easy to add new scenarios

### Benefits

1. **Easy Navigation**: Clear folder names
2. **Logical Grouping**: Related docs together
3. **Quick Access**: Important files easy to find
4. **Scalable**: Easy to add more docs
5. **Professional**: Clean, organized structure

---

## 🚀 Common Workflows

### Workflow 1: Run Evaluation Test
```bash
# 1. Read guide
open docs/evaluation/START-HERE-EVAL.md

# 2. Enable demo mode
export DEMO_MODE=true

# 3. Run test
python test_resolution_workflow.py --run-full --demo

# 4. Verify
open https://dashboard.convex.dev
# Filter by: orgId = "demo-org"

# 5. Clean up
python clean_demo_data.py --execute
```

### Workflow 2: Agent Testing
```bash
# 1. Enable demo mode
export DEMO_MODE=true

# 2. Start services
python mcp/src/main.py  # Terminal 1
cd mcp/convex && convex dev  # Terminal 2

# 3. Open prompt
open agent-prompts/SCENARIO-A-BASIC-CONFLICT.md

# 4. Copy to Cursor/ChatGPT

# 5. Verify and clean
python clean_demo_data.py --execute
```

### Workflow 3: Understand System
```bash
# 1. Read implementation
open docs/implementation/IMPLEMENTATION-SUMMARY.md

# 2. Review manifest
open docs/implementation/DELIVERABLES-MANIFEST.md

# 3. Check test results
open docs/testing/TEST-RESULTS-SUMMARY.md
```

---

## 📊 File Count Summary

**Documentation**: 12 files in `docs/`
- Evaluation: 4 files
- Demo Mode: 3 files
- Implementation: 2 files  
- Testing: 3 files

**Agent Prompts**: 4 files in `agent-prompts/`

**Test Scripts**: 4 files at root level

**Test Data**: 9 files in `scenario-6-enterprise-full/`

**Implementation**: 8 modified files in `mcp/`

**Total**: 37 files for complete evaluation framework

---

## 🔗 Quick Links

### Most Used Documents
- [`docs/evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md) ⭐
- [`docs/demo-mode/DEMO-MODE-QUICK-START.md`](demo-mode/DEMO-MODE-QUICK-START.md)
- [`agent-prompts/SCENARIO-A-BASIC-CONFLICT.md`](../agent-prompts/SCENARIO-A-BASIC-CONFLICT.md)

### Reference Documents
- [`docs/README.md`](README.md) - Documentation index
- [`docs/evaluation/EVALUATION-INDEX.md`](evaluation/EVALUATION-INDEX.md) - Navigation
- [`docs/implementation/DELIVERABLES-MANIFEST.md`](implementation/DELIVERABLES-MANIFEST.md) - Files

### Technical Documents
- [`docs/implementation/IMPLEMENTATION-SUMMARY.md`](implementation/IMPLEMENTATION-SUMMARY.md)
- [`docs/testing/TEST-RESULTS-SUMMARY.md`](testing/TEST-RESULTS-SUMMARY.md)
- [`docs/evaluation/AGENT-EVAL-FRAMEWORK.md`](evaluation/AGENT-EVAL-FRAMEWORK.md)

---

## ✅ Quality Checks

### Documentation Standards Met
- [x] Organized by purpose (evaluation, demo, implementation, testing)
- [x] Clear folder structure
- [x] Master index (docs/README.md)
- [x] Cross-references updated
- [x] Quick access to frequently used files
- [x] Professional organization
- [x] Easy to extend

### Usability Verified
- [x] Clear entry points for different user types
- [x] Multiple quick start guides
- [x] Comprehensive references available
- [x] Troubleshooting in all guides
- [x] Examples throughout

---

## 📝 Maintenance Guide

### Adding New Documentation

**Evaluation docs**:
```bash
# Add to docs/evaluation/
touch docs/evaluation/NEW-EVALUATION-DOC.md
# Update docs/evaluation/EVALUATION-INDEX.md
```

**Demo mode docs**:
```bash
# Add to docs/demo-mode/
touch docs/demo-mode/NEW-DEMO-DOC.md
# Update docs/demo-mode/DEMO-MODE-GUIDE.md
```

**Test scenarios**:
```bash
# Add to agent-prompts/
touch agent-prompts/SCENARIO-D-NEW-TEST.md
# Update agent-prompts/README.md
```

### Updating Cross-References

When moving or renaming files:
1. Update `docs/README.md`
2. Update `docs/evaluation/EVALUATION-INDEX.md`
3. Update cross-links in related documents
4. Test all links work

---

## 🎓 Documentation Hierarchy

```
Level 1: Master Indexes
├── README.md (root)
└── docs/README.md

Level 2: Category Indexes
├── docs/evaluation/EVALUATION-INDEX.md
├── docs/evaluation/START-HERE-EVAL.md
├── docs/demo-mode/DEMO-MODE-QUICK-START.md
└── agent-prompts/README.md

Level 3: Detailed Guides
├── All other docs in docs/*/
└── All scenario files in agent-prompts/

Level 4: Technical References
├── docs/implementation/DELIVERABLES-MANIFEST.md
└── Code files in mcp/
```

**Navigation rule**: Start at Level 1, drill down as needed

---

## Summary

**Organization Status**: ✅ COMPLETE & PROFESSIONAL

**Structure**:
- Clear categories (4 doc folders)
- Logical grouping
- Easy navigation
- Scalable design

**Access**:
- Main index: `docs/README.md`
- Quick start: `docs/evaluation/START-HERE-EVAL.md`
- Demo mode: `docs/demo-mode/DEMO-MODE-QUICK-START.md`

**Quality**:
- All files organized
- Cross-references updated
- Professional structure
- Easy to maintain

**Ready for**: Professional use, team collaboration, continuous updates

---

**For complete navigation**: See [`docs/README.md`](README.md)

**To start testing**: See [`docs/evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md)

