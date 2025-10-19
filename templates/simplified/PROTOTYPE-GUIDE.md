# Prototype Testing Guide - Simplified Templates

Quick guide to get you testing the MCP discovery tool immediately with simplified templates.

---

## 🚀 Quick Start (5 Minutes)

### 1. Pick a Test Scenario
```bash
cd test-data/scenario-1-cozyhome
```

### 2. Manual Test First (Validate Structure)
```bash
# Copy simplified template
cp templates/simplified/client-facing-sow-simplified.md \
   output/test-sow.md

# Replace placeholders manually (search for [PROJECT_NAME], etc.)
# Takes ~10 minutes
```

### 3. Validate Output
- Check all `[PLACEHOLDERS]` replaced
- Verify conditional sections removed/kept appropriately
- Ensure readable and coherent

✅ **If manual works, MCP logic will work**

---

## 📋 Test Checklist

### Phase 1: Basic Population (Day 1)
- [ ] Extract PROJECT_NAME from discovery docs
- [ ] Extract CLIENT_NAME from discovery docs
- [ ] Extract SYSTEM_A and SYSTEM_B
- [ ] Determine INTEGRATION_TYPE
- [ ] Replace all critical placeholders
- [ ] Generate readable document

**Success**: Document has no [PLACEHOLDER] text remaining

---

### Phase 2: Conditional Logic (Day 2)
- [ ] Detect integration type (accounting/marketing/fulfillment/inventory/pos)
- [ ] Process `{{#if accounting}}` blocks correctly
- [ ] Remove non-matching conditional blocks
- [ ] Keep matching conditional content
- [ ] Test with all 5 integration types

**Success**: Accounting project has accounting sections, not marketing sections

---

### Phase 3: Discovery Analysis (Day 3-4)
- [ ] Detect gaps in discovery docs
- [ ] Generate OPEN_QUESTIONS list
- [ ] Generate ASSUMPTIONS_TO_VALIDATE list
- [ ] Calculate CONFIDENCE_SCORE
- [ ] Populate CURRENT_PAIN_POINTS
- [ ] Populate BUSINESS_OBJECTIVES

**Success**: Open questions match real gaps in discovery docs

---

### Phase 4: All Three Documents (Day 5)
- [ ] Generate SOW from discovery docs
- [ ] Generate Implementation Plan
- [ ] Generate Technical Specs
- [ ] Ensure PROJECT_ID consistent across all three
- [ ] Validate cross-references work

**Success**: Three coherent documents that reference each other

---

### Phase 5: All Scenarios (Week 2)
- [ ] Test with CozyHome (accounting)
- [ ] Test with BrewCrew (marketing)
- [ ] Test with PetPawz (fulfillment)
- [ ] Test with FitFuel (inventory)
- [ ] Test with Bloom (POS)

**Success**: Conditional sections adapt correctly for each type

---

## 🧪 Test Cases

### Test Case 1: Placeholder Replacement
**Input**: Discovery docs with client name "CozyHome LLC"  
**Expected**: `[CLIENT_NAME]` → "CozyHome LLC" in all documents  
**Validation**: Search output for "[CLIENT" - should find nothing

---

### Test Case 2: Conditional Processing
**Input**: Integration type = "accounting"  
**Expected**: `{{#if accounting}}` content included, other conditionals removed  
**Validation**: SOW should have tax handling, not email automation

---

### Test Case 3: Confidence Scoring
**Input**: Discovery docs with 6 open questions  
**Expected**: Confidence score 60-75%, warning displayed if <70%  
**Validation**: Check Open Questions section populated correctly

---

### Test Case 4: Gap Detection
**Input**: Discovery docs missing refund handling discussion  
**Expected**: "How should refunds be handled?" in OPEN_QUESTIONS  
**Validation**: Gap detection catches what humans would ask

---

### Test Case 5: All Integration Types
**Input**: 5 different scenarios  
**Expected**: Each gets appropriate conditional content  
**Validation**: Marketing gets GDPR, fulfillment gets shipping, etc.

---

## 📊 Validation Metrics

Track these to measure success:

### Quality Metrics
- **Placeholder coverage**: 100% of critical placeholders filled
- **Conditional accuracy**: 100% correct conditional selection
- **Readability score**: 90%+ (human review)
- **Gap detection rate**: Catches 80%+ of real gaps

### Performance Metrics
- **Generation time**: <15 seconds for all 3 docs
- **File size**: ~40 KB total (simplified)
- **Memory usage**: <100 MB during generation

### Iteration Metrics
- **Time to fix bug**: <30 minutes (simplified makes debugging easier)
- **Time to add feature**: <1 hour
- **Test cycle time**: <5 minutes

---

## 🐛 Common Issues & Solutions

### Issue: Placeholders Not Replaced
**Symptom**: "[PROJECT_NAME]" still in output  
**Cause**: Placeholder not in replacement dictionary  
**Fix**: Add to placeholder map, ensure exact bracket format

---

### Issue: Conditional Blocks Not Processed
**Symptom**: "{{#if accounting}}" text in output  
**Cause**: Conditional parser not running  
**Fix**: Implement conditional processor, test regex/parser

---

### Issue: Generated Text Not Readable
**Symptom**: Grammatical errors, missing context  
**Cause**: Insufficient data extraction from discovery docs  
**Fix**: Improve extraction logic, add more context preservation

---

### Issue: Confidence Score Always Same
**Symptom**: Every project scores 75%  
**Cause**: Scoring algorithm not considering gaps  
**Fix**: Enhance gap detection, weight missing vs. present info

---

### Issue: Cross-References Broken
**Symptom**: Links point to wrong file names  
**Cause**: PROJECT_ID inconsistent across documents  
**Fix**: Generate PROJECT_ID once, reuse everywhere

---

## 📈 Progression Path

### Week 1: Foundation
- Day 1: Basic placeholder replacement
- Day 2: Conditional processing
- Day 3: Discovery extraction
- Day 4: Gap detection
- Day 5: All three documents

**Milestone**: Generate CozyHome docs successfully

---

### Week 2: All Integration Types
- Day 1: Marketing (BrewCrew)
- Day 2: Fulfillment (PetPawz)
- Day 3: Inventory (FitFuel)
- Day 4: POS (Bloom)
- Day 5: Refinement & bug fixes

**Milestone**: All 5 scenarios generate correctly

---

### Week 3-4: Analysis Engine
- Improve gap detection accuracy
- Enhance confidence scoring algorithm
- Better business objective extraction
- Refine open question generation
- Add assumption detection

**Milestone**: Confidence scores correlate with real readiness

---

### Week 5: Validation
- Generate both simplified AND full templates
- Compare quality
- Get team feedback
- Measure time savings
- Validate against real projects

**Milestone**: Team approves approach

---

### Week 6+: Production
- Port to full templates
- Add detail population
- Deploy to team
- Collect usage data
- Iterate based on feedback

**Milestone**: Production deployment

---

## 🎯 Success Criteria

### Prototype Succeeds When:

✅ **Generates all 3 docs** from discovery artifacts  
✅ **<15% manual editing** needed for coherence  
✅ **Conditional sections** adapt to integration type  
✅ **Confidence score** reflects actual readiness  
✅ **Gap detection** catches 80%+ of missing info  
✅ **Team feedback** is positive on structure  
✅ **Ready to upgrade** to full templates

---

## 💡 Tips for Success

### 1. Start Simple
- Test one placeholder at a time
- Validate each step before moving on
- Use print statements liberally

### 2. Use CozyHome First
- Most complete test data
- Has known gaps to detect
- Good balance of complexity

### 3. Manual Baseline
- Populate one template manually first
- Use as reference for automated output
- Helps catch subtle issues

### 4. Iterate Fast
- Simplified templates enable 5-minute test cycles
- Fix bugs immediately
- Don't over-engineer initially

### 5. Get Feedback Early
- Show output to PMs/devs after Week 1
- Adjust structure based on input
- Validate gap detection with real users

---

## 📝 Sample Test Script

```python
# Pseudocode for prototype testing

def test_simplified_template_generation():
    # Phase 1: Setup
    discovery_docs = ingest("test-data/scenario-1-cozyhome")
    
    # Phase 2: Analysis
    analysis = analyze_discovery(discovery_docs)
    assert analysis.confidence_score < 75  # CozyHome has gaps
    assert len(analysis.open_questions) >= 4
    
    # Phase 3: Generation
    sow = generate_from_template(
        "templates/simplified/client-facing-sow-simplified.md",
        discovery_docs,
        analysis
    )
    
    # Phase 4: Validation
    assert "[PROJECT_NAME]" not in sow
    assert "[CLIENT_NAME]" not in sow
    assert "{{#if" not in sow  # Conditionals processed
    assert "accounting" in sow.lower()  # Type detected
    assert analysis.open_questions[0] in sow  # Questions included
    
    # Phase 5: Quality
    assert is_readable(sow)
    assert has_valid_cross_references(sow)
    
    print("✅ Test passed!")

# Run for all scenarios
for scenario in ["cozyhome", "brewcrew", "petpawz", "fitfuel", "bloom"]:
    test_simplified_template_generation(scenario)
```

---

## 🔗 Quick Links

### Documentation
- **This Guide**: Start here for testing
- **README.md**: Simplified template overview
- **COMPARISON.md**: Full vs. simplified comparison
- **../PLACEHOLDER-REFERENCE.md**: Complete placeholder list

### Templates
- **SOW**: `client-facing-sow-simplified.md` (150 lines)
- **Plan**: `internal-implementation-plan-simplified.md` (200 lines)
- **Specs**: `internal-technical-specs-simplified.md` (250 lines)

### Examples
- **Populated SOW**: `examples/cozyhome-sow-simplified-example.md`
- **Full version**: `../examples/cozyhome-sow-example.md` (for comparison)

### Test Data
- **CozyHome**: `../../test-data/scenario-1-cozyhome/`
- **All Scenarios**: `../../test-data/scenario-*/`

---

## ❓ FAQ

**Q: Should I use simplified or full templates for prototype?**  
A: Simplified. 70% faster iteration, easier debugging.

**Q: Will my logic work with full templates?**  
A: Yes. 80% transfers directly, just add more placeholders.

**Q: How long to build prototype with simplified templates?**  
A: ~2 weeks for basic functionality, 4 weeks for refined.

**Q: Can I test analysis engine with simplified templates?**  
A: Yes. Perfect for testing gap detection and confidence scoring.

**Q: When should I upgrade to full templates?**  
A: After validating approach with all 5 scenarios (Week 5+).

**Q: What's the migration effort to full templates?**  
A: ~20% code changes, mostly adding placeholders. Low risk.

---

**Status**: Ready for prototype testing  
**Estimated time to first working prototype**: 1 week  
**Start here**: Test manual population with CozyHome

