# Validation Test Plan - Resolution & Clarification Support

## Prerequisites

### 1. Environment Setup
```bash
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
source mcp/venv/bin/activate
```

### 2. Convex Setup (Required for Full Testing)
```bash
cd mcp/convex
npm install
convex dev  # Or convex deploy for production
```

### 3. Verify Environment Variables
```bash
# Check .env file exists in mcp/ directory
cat mcp/.env | grep CONVEX_DEPLOYMENT_URL
```

---

## Test Suite 1: Automated Testing (15 minutes)

### Test 1.1: Run Comprehensive Test Scenario
**Objective**: Validate AI detection of resolutions and clarifications

```bash
# From project root
python test_resolution_workflow.py --run-full
```

**Expected Results**:
- ✅ Ingests 5-7 documents successfully
- ✅ Detects inventory conflict (SAP vs Shopify)
- ✅ Finds resolution in decision email
- ✅ Finds at least 1 clarification (real-time)
- ✅ Syncs to Convex without errors
- ✅ Confidence score between 55-85%

**Pass Criteria**:
- [ ] Test completes without errors
- [ ] At least 1 conflict detected
- [ ] At least 1 resolution found (not None)
- [ ] At least 1 clarification found (not None)
- [ ] Convex sync succeeds (if configured)

**Document Results**:
```
Conflicts found: ____
Resolutions found: ____
Ambiguities found: ____
Clarifications found: ____
Confidence score: ____%
```

---

### Test 1.2: Validate Against Expected Results
**Objective**: Ensure output matches expectations

```bash
python test_resolution_workflow.py --validate
```

**Pass Criteria**:
- [ ] Validation runs without crashes
- [ ] At least 50% of validations pass
- [ ] No hallucinated resolutions/clarifications

**What to Check**:
- Resolution text appears verbatim in source documents ✅
- Clarification text appears verbatim in source documents ✅
- No made-up or inferred text ✅

---

### Test 1.3: Data Cleanup and Re-test
**Objective**: Verify repeatable testing

```bash
# Wipe data
python test_resolution_workflow.py --wipe-only

# Re-run test
python test_resolution_workflow.py --run-full
```

**Pass Criteria**:
- [ ] Wipe completes successfully
- [ ] Second run produces same results (±5% confidence)
- [ ] No data corruption or carry-over

---

## Test Suite 2: Manual Portal Validation (20 minutes)

### Test 2.1: Verify Convex Data Structure
**Objective**: Confirm schema changes deployed correctly

**Steps**:
1. Open Convex dashboard: https://dashboard.convex.dev
2. Navigate to your deployment
3. Go to "Data" tab
4. Select `conflicts` table

**Verify**:
- [ ] `resolution` column exists (optional string)
- [ ] At least 1 conflict record visible
- [ ] Resolution field populated for resolved conflicts
- [ ] Resolution text matches source document

**Check `ambiguities` table**:
- [ ] `clarification` column exists (optional string)
- [ ] At least 1 ambiguity record visible
- [ ] Clarification field populated when found
- [ ] Clarification text matches source document

**Screenshot Evidence**: Take screenshots of Convex data tables

---

### Test 2.2: Portal Display Verification
**Objective**: Ensure portal correctly displays new fields

**Open Portal** (if available):
1. Navigate to project detail page
2. View conflicts section

**Verify Conflict Display**:
- [ ] Conflict card shows "Inventory System of Record"
- [ ] Resolution section visible
- [ ] Resolution text displays correctly
- [ ] Resolution badge/indicator shows "Resolved" status

**Verify Ambiguity Display**:
- [ ] Ambiguity card shows ambiguous terms
- [ ] Clarification section visible when populated
- [ ] Clarification text displays correctly
- [ ] Clarification badge/indicator shows "Clarified" status

**Verify Empty States**:
- [ ] Conflicts without resolution show "Needs Resolution" or similar
- [ ] Ambiguities without clarification show "Needs Clarification"

---

### Test 2.3: Timeline/Events Verification
**Objective**: Confirm event logging works

**In Portal or Convex Dashboard**:
1. Navigate to `contextEvents` table or project timeline
2. Filter by project: `scenario-6-enterprise-full`

**Verify Events**:
- [ ] `conflict_resolved` event logged when resolution added
- [ ] `ambiguity_clarified` event logged when clarification added
- [ ] Event timestamps are correct
- [ ] Event metadata contains relevant IDs

---

## Test Suite 3: User Update Workflow (10 minutes)

### Test 3.1: User-Provided Resolution
**Objective**: Test manual resolution via update() function

**Setup Test Project**:
```bash
# In Python/MCP environment
from main import manage_project, ingest, analyze, update

# Create test project
manage_project(action="create", project_id="test-resolution", project_name="Resolution Test")

# Ingest a simple scenario
ingest(project_id="test-resolution", source="local")

# Analyze to create conflicts
analyze(project_id="test-resolution", mode="full")
```

**Add Resolution**:
```python
# Provide resolution for a conflict
result = update(
    project_id="test-resolution",
    type="resolve",
    target_id="inventory",  # or partial match from conflict
    content="After team discussion, we decided Shopify will be the inventory master for real-time accuracy."
)

print(result)
```

**Verify**:
- [ ] Update returns success message
- [ ] `resolved_item_type` is "conflict" or "ambiguity"
- [ ] Check Convex - resolution field updated
- [ ] Timeline event logged
- [ ] Confidence score updated

**Check Portal**:
- [ ] Conflict shows as resolved
- [ ] Resolution text displays
- [ ] Timeline shows resolution event

---

### Test 3.2: User-Provided Clarification
**Objective**: Test manual clarification via update() function

```python
result = update(
    project_id="test-resolution",
    type="resolve",
    target_id="real-time",  # Match ambiguity term
    content="Real-time means inventory updates propagate within 30 seconds maximum via webhook triggers."
)

print(result)
```

**Verify**:
- [ ] Update returns success message
- [ ] `resolved_item_type` is "ambiguity"
- [ ] Check Convex - clarification field updated
- [ ] Timeline event logged
- [ ] Ambiguity status changes to "clarified"

---

## Test Suite 4: Edge Cases & Error Handling (10 minutes)

### Test 4.1: No Resolution Found
**Objective**: Verify system doesn't hallucinate

**Create Test Scenario**:
```bash
# Use scenario-1-cozyhome (existing test data without resolutions)
python test_resolution_workflow.py --scenario scenario-1-cozyhome --run-full
```

**Verify**:
- [ ] Conflicts detected (if any)
- [ ] Resolution field is `null` or empty
- [ ] No fake/inferred resolution text
- [ ] Status remains "open" not "resolved"

---

### Test 4.2: Partial Clarification Match
**Objective**: Test pattern matching robustness

**Check Analysis Results**:
- [ ] Some ambiguities have clarifications, some don't
- [ ] Only explicit clarifications are populated
- [ ] Ambiguous clarifications are left empty (conservative approach)

---

### Test 4.3: Multiple Conflicts/Resolutions
**Objective**: Handle multiple items correctly

**Verify in Comprehensive Test**:
- [ ] All conflicts detected
- [ ] Each conflict tracked separately
- [ ] Resolutions mapped to correct conflicts
- [ ] No cross-contamination of data

---

### Test 4.4: Convex Connection Failure
**Objective**: Graceful degradation

**Simulate Failure**:
```bash
# Stop Convex dev server or set invalid URL
export CONVEX_DEPLOYMENT_URL="invalid"

# Run test
python test_resolution_workflow.py --run-full
```

**Verify**:
- [ ] Test continues despite Convex failure
- [ ] Warning message displayed
- [ ] Local analysis still works
- [ ] No crash or data loss

---

## Test Suite 5: Data Integrity (10 minutes)

### Test 5.1: Resolution Text Validation
**Objective**: Ensure no data corruption or truncation

**For Each Resolution Found**:
1. Copy resolution text from portal/Convex
2. Search in source documents (Ctrl+F)

**Verify**:
- [ ] Resolution text exists verbatim in source document
- [ ] No truncation (text is complete)
- [ ] No corruption (special characters preserved)
- [ ] Source attribution is correct

---

### Test 5.2: Clarification Text Validation
**Objective**: Ensure accurate extraction

**For Each Clarification Found**:
1. Copy clarification text from portal/Convex
2. Search in source documents

**Verify**:
- [ ] Clarification text exists in source document
- [ ] Context is appropriate (not out of context)
- [ ] Numeric values are accurate (if any)
- [ ] No inference or assumption

---

### Test 5.3: Concurrent Updates
**Objective**: Test race conditions (if applicable)

**If Multiple Users/Processes**:
1. Have two sessions update same project simultaneously
2. Check for data conflicts

**Verify**:
- [ ] Last write wins (expected behavior)
- [ ] No data corruption
- [ ] Both updates logged in timeline

---

## Test Suite 6: Performance & Scale (5 minutes)

### Test 6.1: Large Document Set
**Objective**: Ensure performance with realistic data volume

**Test with Multiple Scenarios**:
```bash
# Run all scenarios
for scenario in scenario-1-cozyhome scenario-2-brewcrew scenario-6-enterprise-full; do
    echo "Testing $scenario..."
    python test_resolution_workflow.py --scenario $scenario --run-full
done
```

**Verify**:
- [ ] All tests complete in reasonable time (<2 min each)
- [ ] No memory issues
- [ ] Convex sync completes successfully
- [ ] Analysis quality consistent across scenarios

---

### Test 6.2: Stress Test (Optional)
**Objective**: Test limits

```bash
# Run 10 iterations
python test_resolution_workflow.py --iterations 10
```

**Verify**:
- [ ] All iterations complete
- [ ] Consistent results (±5% variation acceptable)
- [ ] No memory leaks
- [ ] No database errors

---

## Validation Checklist

### Core Functionality
- [ ] Convex schema includes `resolution` and `clarification` fields
- [ ] Python models correctly handle new fields
- [ ] Analyzer detects resolutions in documents
- [ ] Analyzer detects clarifications in documents
- [ ] Sync operations pass new fields to Convex
- [ ] Mutations accept and store new fields
- [ ] User updates sync resolutions/clarifications
- [ ] Event logging works correctly

### Quality Assurance
- [ ] No hallucinated resolutions (only real text from docs)
- [ ] No hallucinated clarifications (only real text from docs)
- [ ] Source documents correctly referenced
- [ ] Timeline events accurate
- [ ] Confidence scores update appropriately

### User Experience
- [ ] Portal displays resolutions correctly
- [ ] Portal displays clarifications correctly
- [ ] "Needs resolution" state visible
- [ ] "Needs clarification" state visible
- [ ] Timeline shows resolution/clarification events

### Error Handling
- [ ] Graceful handling of missing Convex
- [ ] Appropriate warnings for missing data
- [ ] No crashes on edge cases
- [ ] Clear error messages

---

## Pass/Fail Criteria

### Must Pass (Blocking Issues)
- ✅ Test Suite 1: Automated tests run without errors
- ✅ Test Suite 2.1: Convex schema correct
- ✅ Test Suite 3: User updates work correctly
- ✅ Test Suite 5: No hallucinated data

### Should Pass (Important but not blocking)
- ⚠️ Test Suite 2.2: Portal display (if portal available)
- ⚠️ Test Suite 4: Edge cases handled gracefully
- ⚠️ Test Suite 6: Performance acceptable

### Nice to Have
- ℹ️ AI detection catches 50%+ of clarifications
- ℹ️ Gap detection works correctly
- ℹ️ Confidence scores in expected range

---

## Test Execution Log Template

```
Date: _______________
Tester: _______________
Environment: [ ] Local Dev [ ] Staging [ ] Production

AUTOMATED TESTS
[ ] Test 1.1: Comprehensive scenario - PASS/FAIL
    Notes: _______________________________
    
[ ] Test 1.2: Validation - PASS/FAIL
    Notes: _______________________________
    
[ ] Test 1.3: Re-test - PASS/FAIL
    Notes: _______________________________

PORTAL VALIDATION
[ ] Test 2.1: Schema verification - PASS/FAIL
    Screenshot: _______________________________
    
[ ] Test 2.2: Display verification - PASS/FAIL
    Screenshot: _______________________________
    
[ ] Test 2.3: Timeline events - PASS/FAIL
    Notes: _______________________________

USER WORKFLOWS
[ ] Test 3.1: User resolution - PASS/FAIL
    Notes: _______________________________
    
[ ] Test 3.2: User clarification - PASS/FAIL
    Notes: _______________________________

EDGE CASES
[ ] Test 4.1: No hallucination - PASS/FAIL
[ ] Test 4.2: Partial matches - PASS/FAIL
[ ] Test 4.3: Multiple items - PASS/FAIL
[ ] Test 4.4: Error handling - PASS/FAIL

DATA INTEGRITY
[ ] Test 5.1: Resolution accuracy - PASS/FAIL
[ ] Test 5.2: Clarification accuracy - PASS/FAIL

OVERALL RESULT: [ ] PASS [ ] FAIL [ ] CONDITIONAL PASS

Blockers: _______________________________
Issues Found: _______________________________
Recommendations: _______________________________
```

---

## Quick Start (5-Minute Smoke Test)

If you're short on time, run this minimal validation:

```bash
# 1. Run automated test
python test_resolution_workflow.py --run-full

# 2. Check key results
# ✅ Conflict detected
# ✅ Resolution found (not None)
# ✅ Sync succeeded

# 3. Check Convex dashboard
# ✅ conflicts table has resolution column
# ✅ At least 1 resolution populated

# 4. Test user update
# (Use Test 3.1 steps)

# If all 4 pass → System is working ✅
```

---

## Troubleshooting Guide

### Issue: Documents not loading
```bash
# Check file structure
ls -la test-data/scenario-6-enterprise-full/

# Verify all folders exist
ls -la test-data/scenario-6-enterprise-full/emails/
ls -la test-data/scenario-6-enterprise-full/transcripts/
ls -la test-data/scenario-6-enterprise-full/client-docs/
```

### Issue: Convex sync fails
```bash
# Check Convex connection
cd mcp/convex
convex dev  # Should be running

# Verify env vars
cat ../. env | grep CONVEX
```

### Issue: No resolutions found
**Expected**: AI detection is conservative. This is correct behavior if:
- Documents don't contain explicit decision statements
- Resolution keywords not present
- This means system is NOT hallucinating ✅

### Issue: Test validation fails
**Review**: Check expected-results.json - may need adjustment based on actual document content

---

## Success Criteria Summary

**Minimum Viable**: 
- ✅ Tests run without errors
- ✅ Schema deployed correctly
- ✅ User updates work
- ✅ No hallucinated data

**Production Ready**:
- ✅ All minimum viable criteria
- ✅ Portal displays correctly
- ✅ AI detection finds at least some resolutions/clarifications
- ✅ Event logging works

**Optimal**:
- ✅ All production ready criteria
- ✅ AI detection >50% accuracy
- ✅ Gap detection works
- ✅ Performance excellent

---

## Next Steps After Validation

### If All Tests Pass ✅
1. Deploy Convex schema: `cd mcp/convex && convex deploy`
2. Deploy MCP server to Railway/production
3. Update portal to latest version
4. Monitor first real projects

### If Some Tests Fail ⚠️
1. Document specific failures
2. Prioritize blockers vs nice-to-haves
3. Fix critical issues
4. Re-run validation

### If Tests Pass with Notes 📝
1. Document pattern matching improvements needed
2. Plan future enhancements
3. Deploy with known limitations
4. Iterate based on real usage

---

**Estimated Total Time**: 60-75 minutes for complete validation
**Minimum Time**: 5 minutes for smoke test

