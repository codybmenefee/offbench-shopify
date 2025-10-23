#!/bin/bash
# Discovery Agent MCP - Evaluation Suite Runner
# Run all test scenarios in sequence with manual verification checkpoints

set -e  # Exit on error

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Discovery Agent MCP - Evaluation Suite                  ║"
echo "║   Resolution & Clarification Testing                      ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source mcp/venv/bin/activate

# Check if Convex is running
echo "🔍 Checking Convex connection..."
if ! python3 -c "from mcp.src.persistence.convex_client import ConvexClient; ConvexClient()" 2>/dev/null; then
    echo "⚠️  WARNING: Convex connection failed"
    echo "    Tests will continue but sync may fail"
    echo "    Start Convex: cd mcp/convex && convex dev"
    echo ""
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Convex connected"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo ""

# Define scenarios
declare -a scenarios=(
    "scenario-6-enterprise-full:Complex Enterprise:Hard"
    "scenario-1-cozyhome:Basic E-commerce:Easy"
    "scenario-2-brewcrew:Mid-size Business:Medium"
)

total_scenarios=${#scenarios[@]}
current=0

for scenario_info in "${scenarios[@]}"; do
    current=$((current + 1))
    
    # Parse scenario info
    IFS=':' read -r scenario_id scenario_name difficulty <<< "$scenario_info"
    
    echo "┌────────────────────────────────────────────────────────┐"
    echo "│ Scenario $current/$total_scenarios: $scenario_name"
    echo "│ ID: $scenario_id"
    echo "│ Difficulty: $difficulty"
    echo "└────────────────────────────────────────────────────────┘"
    echo ""
    
    # Clean any previous run
    echo "🗑️  Cleaning previous test data..."
    python test_resolution_workflow.py --scenario $scenario_id --wipe-only 2>/dev/null || true
    
    echo ""
    echo "▶️  Running analysis..."
    echo "───────────────────────────────────────────────────────────"
    
    # Run the test
    if python test_resolution_workflow.py --scenario $scenario_id --run-full; then
        echo ""
        echo "✅ Scenario completed successfully"
    else
        echo ""
        echo "❌ Scenario failed - check output above"
    fi
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "📋 MANUAL VERIFICATION CHECKPOINT"
    echo ""
    echo "Please verify the following:"
    echo "  1. Check Convex dashboard for $scenario_id"
    echo "  2. Verify resolution/clarification fields populated"
    echo "  3. Confirm no hallucinated text"
    echo "  4. Review confidence score"
    echo ""
    echo "Convex Dashboard: https://dashboard.convex.dev"
    echo ""
    
    if [ $current -lt $total_scenarios ]; then
        read -p "Press Enter to continue to next scenario (or Ctrl+C to stop)..."
        echo ""
        
        # Cleanup for next run
        echo "🧹 Cleaning up for next scenario..."
        python test_resolution_workflow.py --scenario $scenario_id --wipe-only
        echo ""
    fi
done

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   Evaluation Suite Complete!                              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "📊 Summary:"
echo "   Total scenarios tested: $total_scenarios"
echo "   Review evaluation template for detailed results"
echo ""
echo "📝 Next Steps:"
echo "   1. Review AGENT-EVAL-FRAMEWORK.md"
echo "   2. Document results in evaluation template"
echo "   3. Check for any hallucinations in Convex data"
echo "   4. Decide: Deploy, Improve, or Iterate"
echo ""

