#!/bin/bash
# Final Verification - Check all components working

echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Final Verification - Resolution & Clarification        ║"
echo "║   + Demo Mode Evaluation Framework                      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Activate venv
source mcp/venv/bin/activate

echo "✅ Checking Implementation..."
echo "───────────────────────────────────────────────────────────"

# Check 1: Convex schema
echo -n "1. Convex schema has resolution/clarification fields... "
if grep -q "resolution: v.optional(v.string())" mcp/convex/schema.ts && \
   grep -q "clarification: v.optional(v.string())" mcp/convex/schema.ts; then
    echo "✅"
else
    echo "❌"
fi

# Check 2: Python models
echo -n "2. Python models support new fields... "
if grep -q "resolution: Optional\[str\]" mcp/src/models/analysis.py && \
   grep -q "clarification: Optional\[str\]" mcp/src/models/analysis.py; then
    echo "✅"
else
    echo "❌"
fi

# Check 3: Demo mode config
echo -n "3. Demo mode configuration present... "
if grep -q "DEMO_MODE" mcp/src/config.py; then
    echo "✅"
else
    echo "❌"
fi

# Check 4: Test documents exist
echo -n "4. Test documents created (7 files)... "
doc_count=$(find test-data/scenario-6-enterprise-full/ -name "*.txt" | wc -l | tr -d ' ')
if [ "$doc_count" -ge 7 ]; then
    echo "✅ ($doc_count files)"
else
    echo "❌ ($doc_count files, expected 7+)"
fi

# Check 5: Agent prompts exist
echo -n "5. Agent prompts ready... "
if [ -f "agent-prompts/SCENARIO-A-BASIC-CONFLICT.md" ] && \
   [ -f "agent-prompts/SCENARIO-B-AMBIGUITY-CLARIFICATION.md" ] && \
   [ -f "agent-prompts/SCENARIO-C-USER-RESOLUTION.md" ]; then
    echo "✅ (3 scenarios)"
else
    echo "❌"
fi

# Check 6: Test scripts executable
echo -n "6. Test scripts ready... "
if [ -x "test_resolution_workflow.py" ] && \
   [ -x "run_eval_scenarios.sh" ] && \
   [ -x "clean_demo_data.py" ]; then
    echo "✅"
else
    echo "❌"
fi

echo ""
echo "✅ Running Demo Mode Test..."
echo "───────────────────────────────────────────────────────────"

# Check 7: Demo mode test
python test_resolution_workflow.py --run-full --demo 2>&1 | head -30

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║   Verification Complete!                                 ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo "   1. Review test output above"
echo "   2. Check for: 🎭 Demo mode enabled"
echo "   3. Check for: ✅ RESOLUTION FOUND"
echo "   4. Check for: ✅ CLARIFICATION FOUND"
echo ""
echo "📖 Documentation:"
echo "   • START-HERE-EVAL.md - Evaluation testing"
echo "   • DEMO-MODE-QUICK-START.md - Demo mode guide"
echo "   • agent-prompts/ - Ready-to-use prompts"
echo ""
echo "🚀 Ready to start evaluation testing!"
echo ""
