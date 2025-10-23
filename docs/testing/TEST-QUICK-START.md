# Resolution & Clarification Testing - Quick Start Guide

## Prerequisites

```bash
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
source mcp/venv/bin/activate
```

## Run Your First Test

```bash
# Run complete test cycle
python test_resolution_workflow.py --run-full
```

This will:
1. ✅ Ingest 8 discovery documents from `scenario-6-enterprise-full`
2. ✅ Analyze documents for conflicts, ambiguities, and gaps
3. ✅ Detect resolutions and clarifications where they exist
4. ✅ Sync results to Convex (if configured)
5. ✅ Validate against expected results
6. ✅ Display detailed report

## Expected Output

```
============================================================
🧪 Running Full Test: scenario-6-enterprise-full
============================================================

📥 Step 1: Ingesting documents...
   ✅ Ingested 8 documents

🔍 Step 2: Analyzing documents...
   ✅ Analysis complete
      Confidence: 62.5%
      Conflicts: 1
      Ambiguities: 3
      Gaps: 5

☁️  Step 3: Syncing to Convex...
   ✅ Sync complete

============================================================
📊 ANALYSIS RESULTS
============================================================

🔴 CONFLICTS:

   1. Inventory System of Record
      Priority: high
      Statements: 2
      ✅ RESOLUTION FOUND: DECISION: Shopify will be the source of truth...

🟡 AMBIGUITIES:

   1. 'real-time' in context: inventory sync...
      Clarification needed: Please specify exact sync timing...
      ✅ CLARIFICATION FOUND: within 30 seconds maximum...

   2. 'fast' in context: page load performance...
      Clarification needed: What is the specific performance requirement...
      ✅ CLARIFICATION FOUND: under 2 seconds for full page load...

   3. 'scalable' in context: future growth...
      Clarification needed: What volume needs to be supported...
      ✅ CLARIFICATION FOUND: 250,000 orders/month by year 3...

🔵 GAPS:

   1. Return and refund handling not discussed
      Category: business_rules
      Priority: high
      Impact: Returns could fail to sync

   2. Tax handling not specified
      Category: business_rules
      Priority: high
      Impact: Tax calculations could be incorrect

   [... more gaps ...]

============================================================
Overall Confidence: 62.5%
Client: TechStyle
Systems: Shopify, SAP, Salesforce, Klaviyo, ShipStation, Stripe, PayPal
============================================================

============================================================
✅ VALIDATING RESULTS
============================================================

Validating conflicts...
   ✅ Conflict resolution found for 'Inventory System of Record'

Validating ambiguities...
   ✅ Clarification found for 'real-time'
   ✅ Clarification found for 'fast'
   ✅ Clarification found for 'scalable'

Validating gaps...
   ✅ Gap count acceptable: 5 (expected ~5)

Validating confidence score...
   ✅ Confidence score in range: 62.5% (55-70%)

============================================================
✅ ALL VALIDATIONS PASSED
============================================================
```

## Other Test Commands

### Validate Only (without re-running)
```bash
python test_resolution_workflow.py --validate
```

### Clean Data for Fresh Run
```bash
python test_resolution_workflow.py --wipe-only
```

### Run Multiple Iterations (Regression Testing)
```bash
python test_resolution_workflow.py --iterations 3
```

### Test Different Scenario
```bash
python test_resolution_workflow.py --scenario scenario-1-cozyhome --run-full
```

## What to Look For

### ✅ Good Results
- Conflicts have resolutions when they exist in documents
- Ambiguities have clarifications when they exist in documents
- NO resolutions/clarifications when they DON'T exist (no hallucination)
- Confidence score in expected range
- All expected gaps identified

### ❌ Problems to Watch For
- Resolution text that doesn't appear in any document (HALLUCINATION)
- Clarification text that's inferred rather than quoted (HALLUCINATION)
- Missing resolutions that clearly exist in documents
- Missing clarifications that clearly exist in documents
- Confidence score way off from expected range

## Next Steps After Testing

1. **Review Results**: Check if AI correctly found resolutions/clarifications
2. **Check Portal**: View results in Convex-connected portal
3. **Adjust Patterns**: If needed, enhance pattern matching in `analyzer.py`
4. **Add More Test Cases**: Create additional scenarios in `test-data/`
5. **Deploy**: Push changes to production

## Troubleshooting

### Test Fails to Run
```bash
# Make sure you're in the right directory
pwd
# Should show: .../offbench-shopify

# Make sure venv is activated
which python
# Should show: .../offbench-shopify/mcp/venv/bin/python

# Install dependencies if needed
pip install -r requirements.txt
```

### Convex Sync Fails
- Check `mcp/.env` has correct `CONVEX_DEPLOYMENT_URL`
- Verify Convex is running: `cd mcp/convex && convex dev`
- Test will continue without Convex if not configured

### No Resolutions/Clarifications Found
- Check `analyzer.py` pattern matching
- Verify test documents actually contain resolution/clarification text
- Review `expected-results.json` to ensure expectations match document content

## Files Reference

- **Test Script**: `test_resolution_workflow.py`
- **Test Data**: `test-data/scenario-6-enterprise-full/`
- **Expected Results**: `test-data/scenario-6-enterprise-full/expected-results.json`
- **Analyzer Logic**: `mcp/src/core/analyzer.py`
- **Sync Logic**: `mcp/src/persistence/convex_sync.py`

## Questions?

See `IMPLEMENTATION-SUMMARY.md` for complete technical details.

