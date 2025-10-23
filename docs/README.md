# 📚 Discovery Agent Documentation

Complete documentation for Resolution & Clarification support and evaluation framework.

---

## 🚀 Quick Start

**New to testing?** → Start here: [`evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md)

**Need demo mode?** → Quick guide: [`demo-mode/DEMO-MODE-QUICK-START.md`](demo-mode/DEMO-MODE-QUICK-START.md)

**Want to understand the system?** → Implementation: [`implementation/IMPLEMENTATION-SUMMARY.md`](implementation/IMPLEMENTATION-SUMMARY.md)

---

## 📁 Documentation Structure

```
docs/
├── README.md (this file)             # Master documentation index
│
├── evaluation/                       # Evaluation Testing
│   ├── START-HERE-EVAL.md           ⭐ Main entry point
│   ├── EVALUATION-INDEX.md           📋 Complete navigation
│   ├── AGENT-EVAL-FRAMEWORK.md       📚 60+ page framework
│   └── VALIDATION-TEST-PLAN.md       ✅ Detailed procedures
│
├── demo-mode/                        # Demo Mode Documentation
│   ├── DEMO-MODE-QUICK-START.md     🚀 Quick setup guide
│   ├── DEMO-MODE-GUIDE.md           📖 Comprehensive guide
│   └── DEMO-MODE-COMPLETE.md        ✅ Implementation summary
│
├── implementation/                   # Technical Implementation
│   ├── IMPLEMENTATION-SUMMARY.md    🔧 What was built
│   └── DELIVERABLES-MANIFEST.md     📦 Complete file list
│
└── testing/                          # Testing Documentation
    ├── README-TESTING.md            📖 Testing overview
    ├── TEST-QUICK-START.md          ⚡ Quick test guide
    └── TEST-RESULTS-SUMMARY.md      📊 Current results
```

---

## 🎯 Documentation by Purpose

### Want to... → Go to...

| Purpose | Document | Time |
|---------|----------|------|
| **Start evaluation testing** | [`evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md) | 5 min |
| **Set up demo mode** | [`demo-mode/DEMO-MODE-QUICK-START.md`](demo-mode/DEMO-MODE-QUICK-START.md) | 2 min |
| **Understand what was built** | [`implementation/IMPLEMENTATION-SUMMARY.md`](implementation/IMPLEMENTATION-SUMMARY.md) | 10 min |
| **Run quick test** | [`testing/TEST-QUICK-START.md`](testing/TEST-QUICK-START.md) | 2 min |
| **Get complete framework** | [`evaluation/AGENT-EVAL-FRAMEWORK.md`](evaluation/AGENT-EVAL-FRAMEWORK.md) | 30 min |
| **See current test results** | [`testing/TEST-RESULTS-SUMMARY.md`](testing/TEST-RESULTS-SUMMARY.md) | 5 min |
| **Navigate everything** | [`evaluation/EVALUATION-INDEX.md`](evaluation/EVALUATION-INDEX.md) | 5 min |
| **Demo mode details** | [`demo-mode/DEMO-MODE-GUIDE.md`](demo-mode/DEMO-MODE-GUIDE.md) | 15 min |
| **Detailed test procedures** | [`evaluation/VALIDATION-TEST-PLAN.md`](evaluation/VALIDATION-TEST-PLAN.md) | 20 min |
| **See all files created** | [`implementation/DELIVERABLES-MANIFEST.md`](implementation/DELIVERABLES-MANIFEST.md) | 5 min |

---

## 📂 Complete Repository Structure

```
offbench-shopify/
│
├── README.md                         # Project overview
├── AGENTS.md                         # Developer principles
│
├── docs/                             # 📚 All documentation
│   ├── README.md                     # This file - documentation index
│   ├── evaluation/                   # Evaluation testing
│   ├── demo-mode/                    # Demo mode guides
│   ├── implementation/               # Technical details
│   └── testing/                      # Test documentation
│
├── agent-prompts/                    # 🤖 Copy-paste prompts
│   ├── README.md
│   ├── SCENARIO-A-BASIC-CONFLICT.md
│   ├── SCENARIO-B-AMBIGUITY-CLARIFICATION.md
│   └── SCENARIO-C-USER-RESOLUTION.md
│
├── test-data/                        # 📦 Test scenarios
│   ├── scenario-6-enterprise-full/   # Comprehensive test
│   ├── scenario-1-cozyhome/          # Basic test
│   └── scenario-2-brewcrew/          # Mid-size test
│
├── test_resolution_workflow.py       # 🐍 Automated tester
├── run_eval_scenarios.sh            # 🔄 Batch runner
├── clean_demo_data.py               # 🧹 Cleanup utility
├── FINAL-VERIFICATION.sh            # ✅ Verify all working
│
├── mcp/                              # 💻 MCP server implementation
│   ├── src/                          # Source code (8 files modified)
│   ├── convex/                       # Convex integration (2 files modified)
│   └── .env.example                  # Configuration template
│
└── templates/                        # 📄 Generation templates
```

---

## 🎓 Learning Paths

### Beginner (30 minutes)
1. Read: [`evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md)
2. Read: [`demo-mode/DEMO-MODE-QUICK-START.md`](demo-mode/DEMO-MODE-QUICK-START.md)
3. Run: `python test_resolution_workflow.py --run-full --demo`
4. Verify results

### Intermediate (90 minutes)
1. All beginner steps
2. Read: [`implementation/IMPLEMENTATION-SUMMARY.md`](implementation/IMPLEMENTATION-SUMMARY.md)
3. Run: All 3 agent prompts in `agent-prompts/`
4. Review: [`testing/TEST-RESULTS-SUMMARY.md`](testing/TEST-RESULTS-SUMMARY.md)
5. Document findings

### Advanced (3+ hours)
1. All intermediate steps
2. Read: [`evaluation/AGENT-EVAL-FRAMEWORK.md`](evaluation/AGENT-EVAL-FRAMEWORK.md)
3. Read: [`evaluation/VALIDATION-TEST-PLAN.md`](evaluation/VALIDATION-TEST-PLAN.md)
4. Run: `./run_eval_scenarios.sh` (full suite)
5. Create custom test scenarios
6. Performance testing

---

## 📖 Documentation Categories

### Evaluation Testing
**Location**: `docs/evaluation/`

Documents for setting up and running AI agent evaluation:
- **START-HERE-EVAL.md** - Main entry point, quick start
- **EVALUATION-INDEX.md** - Navigation guide
- **AGENT-EVAL-FRAMEWORK.md** - Complete framework (60+ pages)
- **VALIDATION-TEST-PLAN.md** - Detailed test procedures

**Use when**: Running evaluation tests with AI agents

---

### Demo Mode
**Location**: `docs/demo-mode/`

Documents for demo mode testing and data management:
- **DEMO-MODE-QUICK-START.md** - Quick setup (2 min read)
- **DEMO-MODE-GUIDE.md** - Comprehensive guide (15 min read)
- **DEMO-MODE-COMPLETE.md** - Implementation summary

**Use when**: Setting up demo mode for testing or portal demos

---

### Implementation
**Location**: `docs/implementation/`

Technical documentation about what was built:
- **IMPLEMENTATION-SUMMARY.md** - Complete technical details
- **DELIVERABLES-MANIFEST.md** - All files modified/created

**Use when**: Understanding the codebase or deployment

---

### Testing
**Location**: `docs/testing/`

Testing guides and results:
- **README-TESTING.md** - Testing overview
- **TEST-QUICK-START.md** - Quick test guide
- **TEST-RESULTS-SUMMARY.md** - Current test results

**Use when**: Running tests or reviewing results

---

## 🤖 Agent Prompts

**Location**: `agent-prompts/` (root level for easy access)

Ready-to-use prompts for AI agents:
- **README.md** - Prompt navigation
- **SCENARIO-A-BASIC-CONFLICT.md** - Conflict detection (5 min)
- **SCENARIO-B-AMBIGUITY-CLARIFICATION.md** - Clarification detection (5 min)
- **SCENARIO-C-USER-RESOLUTION.md** - User workflow (10 min)

**Use when**: Testing with Cursor or ChatGPT

---

## 🔧 Scripts & Tools

**Location**: Root level (for easy CLI access)

- `test_resolution_workflow.py` - Automated test runner
- `run_eval_scenarios.sh` - Batch test suite
- `clean_demo_data.py` - Demo data cleanup
- `FINAL-VERIFICATION.sh` - Verify implementation

**Use when**: Running automated tests

---

## ⭐ Recommended Reading Order

### First Time Setup (15 min)
1. [`evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md)
2. [`demo-mode/DEMO-MODE-QUICK-START.md`](demo-mode/DEMO-MODE-QUICK-START.md)
3. Run a test

### Before Agent Testing (10 min)
1. [`agent-prompts/README.md`](../agent-prompts/README.md)
2. [`agent-prompts/SCENARIO-A-BASIC-CONFLICT.md`](../agent-prompts/SCENARIO-A-BASIC-CONFLICT.md)
3. Run the prompt

### For Deep Understanding (60 min)
1. [`implementation/IMPLEMENTATION-SUMMARY.md`](implementation/IMPLEMENTATION-SUMMARY.md)
2. [`evaluation/AGENT-EVAL-FRAMEWORK.md`](evaluation/AGENT-EVAL-FRAMEWORK.md)
3. [`evaluation/VALIDATION-TEST-PLAN.md`](evaluation/VALIDATION-TEST-PLAN.md)

### For Complete Mastery (2+ hours)
1. All of the above
2. [`demo-mode/DEMO-MODE-GUIDE.md`](demo-mode/DEMO-MODE-GUIDE.md)
3. [`implementation/DELIVERABLES-MANIFEST.md`](implementation/DELIVERABLES-MANIFEST.md)
4. Review all agent prompts
5. Run full test suite

---

## 🔍 Finding What You Need

### By Topic

**Evaluation Testing**:
- Quick start → [`evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md)
- Complete framework → [`evaluation/AGENT-EVAL-FRAMEWORK.md`](evaluation/AGENT-EVAL-FRAMEWORK.md)
- Test procedures → [`evaluation/VALIDATION-TEST-PLAN.md`](evaluation/VALIDATION-TEST-PLAN.md)
- Navigation → [`evaluation/EVALUATION-INDEX.md`](evaluation/EVALUATION-INDEX.md)

**Demo Mode**:
- Quick setup → [`demo-mode/DEMO-MODE-QUICK-START.md`](demo-mode/DEMO-MODE-QUICK-START.md)
- Complete guide → [`demo-mode/DEMO-MODE-GUIDE.md`](demo-mode/DEMO-MODE-GUIDE.md)
- Implementation → [`demo-mode/DEMO-MODE-COMPLETE.md`](demo-mode/DEMO-MODE-COMPLETE.md)

**Testing**:
- Overview → [`testing/README-TESTING.md`](testing/README-TESTING.md)
- Quick start → [`testing/TEST-QUICK-START.md`](testing/TEST-QUICK-START.md)
- Results → [`testing/TEST-RESULTS-SUMMARY.md`](testing/TEST-RESULTS-SUMMARY.md)

**Implementation**:
- Technical summary → [`implementation/IMPLEMENTATION-SUMMARY.md`](implementation/IMPLEMENTATION-SUMMARY.md)
- Complete manifest → [`implementation/DELIVERABLES-MANIFEST.md`](implementation/DELIVERABLES-MANIFEST.md)

### By Time Available

**2 minutes**:
- [`testing/README-TESTING.md`](testing/README-TESTING.md)
- [`demo-mode/DEMO-MODE-QUICK-START.md`](demo-mode/DEMO-MODE-QUICK-START.md)

**10 minutes**:
- [`evaluation/START-HERE-EVAL.md`](evaluation/START-HERE-EVAL.md)
- [`implementation/IMPLEMENTATION-SUMMARY.md`](implementation/IMPLEMENTATION-SUMMARY.md)

**30 minutes**:
- [`evaluation/AGENT-EVAL-FRAMEWORK.md`](evaluation/AGENT-EVAL-FRAMEWORK.md)
- [`demo-mode/DEMO-MODE-GUIDE.md`](demo-mode/DEMO-MODE-GUIDE.md)

**60 minutes**:
- [`evaluation/VALIDATION-TEST-PLAN.md`](evaluation/VALIDATION-TEST-PLAN.md)
- All agent prompts

---

## 🎯 Quick Reference

### Enable Demo Mode
```bash
export DEMO_MODE=true
```

### Run Tests
```bash
# Quick automated test
python test_resolution_workflow.py --run-full --demo

# Full evaluation suite
./run_eval_scenarios.sh

# Verify implementation
./FINAL-VERIFICATION.sh
```

### Clean Up
```bash
# Demo data from Convex
python clean_demo_data.py --execute

# Local state
python test_resolution_workflow.py --wipe-only
```

### Access Agent Prompts
```bash
# View available prompts
ls agent-prompts/

# Open a scenario
open agent-prompts/SCENARIO-A-BASIC-CONFLICT.md
```

---

## ✅ What's Implemented

- ✅ **Resolution Support**: AI finds + users provide
- ✅ **Clarification Support**: AI finds + users provide
- ✅ **Demo Mode**: Automatic data tagging
- ✅ **No Hallucination**: Conservative AI detection
- ✅ **Convex Integration**: Full database sync
- ✅ **Evaluation Framework**: Comprehensive testing
- ✅ **Agent Prompts**: 3 ready-to-use scenarios
- ✅ **Test Infrastructure**: Automated + manual testing
- ✅ **Documentation**: Complete guides

---

## 📊 Current Status

**Implementation**: ✅ COMPLETE  
**Testing**: ✅ VERIFIED  
**Demo Mode**: ✅ WORKING  
**Documentation**: ✅ ORGANIZED  

**Ready for**: Evaluation testing and production deployment

---

## 🎬 Your Next Step

Choose your path:

**Path 1: Quick Test (2 min)**
```bash
export DEMO_MODE=true
python test_resolution_workflow.py --run-full --demo
```

**Path 2: Agent Evaluation (20 min)**
```bash
open evaluation/START-HERE-EVAL.md
# Follow the guide
```

**Path 3: Understand First (10 min)**
```bash
open implementation/IMPLEMENTATION-SUMMARY.md
# Learn what was built
```

---

## 📞 Support

**Questions about**:
- **Evaluation testing** → See `evaluation/` docs
- **Demo mode** → See `demo-mode/` docs
- **Implementation** → See `implementation/` docs
- **Test results** → See `testing/` docs
- **Agent prompts** → See `agent-prompts/` (root level)

**Can't find something?** → Check [`evaluation/EVALUATION-INDEX.md`](evaluation/EVALUATION-INDEX.md)

---

## 🎓 Documentation Standards

### Structure
- **Organized by purpose** (evaluation, demo, implementation, testing)
- **Easy navigation** (clear folder names, READMEs)
- **Cross-references** (links between related docs)
- **Quick access** (important files at root level)

### Content
- **Quick starts** for time-pressed users
- **Comprehensive guides** for deep understanding
- **Step-by-step procedures** for execution
- **Troubleshooting** in every guide
- **Examples** throughout

---

## 🚀 Get Started

```bash
# Navigate to this directory
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify

# Read main evaluation guide
open docs/evaluation/START-HERE-EVAL.md

# Or jump straight to testing
export DEMO_MODE=true
python test_resolution_workflow.py --run-full --demo
```

---

**Everything is organized and ready!** 🎉

For questions, check the appropriate docs folder above.  
For evaluation testing, start with `evaluation/START-HERE-EVAL.md`.  
For demo mode, start with `demo-mode/DEMO-MODE-QUICK-START.md`.

