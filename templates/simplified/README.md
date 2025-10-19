# Simplified Templates - Prototype Testing

These are streamlined versions of the full implementation templates, optimized for **rapid prototyping and testing** of the MCP discovery tool.

---

## What's Different?

### Full Templates (templates/*.md)
- **Length**: 500-900 lines each
- **Detail**: Comprehensive, production-ready
- **Use Case**: Final client deliverables
- **Time to Populate**: 2-3 hours manually

### Simplified Templates (templates/simplified/*.md)
- **Length**: 150-300 lines each
- **Detail**: Core essentials only
- **Use Case**: Prototype testing, rapid iteration
- **Time to Populate**: 30-45 minutes manually

---

## Files in This Directory

1. **`client-facing-sow-simplified.md`** (~150 lines)
   - 9 sections vs. 11 in full version
   - Core SOW elements: overview, scope, timeline, pricing, acceptance
   - Confidence scoring and open questions retained
   - Conditional sections simplified

2. **`internal-implementation-plan-simplified.md`** (~200 lines)
   - 10 sections vs. 11 in full version
   - All 5 phases with essential tasks
   - Team assignments, risks, testing, monitoring
   - Conditional sections for integration types

3. **`internal-technical-specs-simplified.md`** (~250 lines)
   - 12 sections vs. 15 in full version
   - Architecture, data flows, APIs, mappings
   - Error handling, security, monitoring
   - Edge cases and performance targets

---

## What's Preserved

✅ **Placeholder system** - All core placeholders present  
✅ **Conditional logic** - Integration-type conditionals work  
✅ **Confidence scoring** - Gap detection and scoring intact  
✅ **Cross-references** - Documents still link to each other  
✅ **Structure** - Same section flow, less detail per section  

---

## What's Simplified

📉 **Fewer subsections** - Combined related content  
📉 **Shorter examples** - Code snippets condensed  
📉 **Less exposition** - Removed explanatory text  
📉 **Fewer tables rows** - Show structure, fewer examples  
📉 **Compressed formatting** - More concise presentation  

---

## When to Use

### Use Simplified Templates For:
- ✅ Initial MCP prototype development
- ✅ Testing template population logic
- ✅ Validating placeholder replacement
- ✅ Quick confidence scoring demos
- ✅ Iterating on analysis engine
- ✅ User feedback on structure
- ✅ Learning the system

### Use Full Templates For:
- ✅ Production client deliverables
- ✅ Final project documentation
- ✅ Complex enterprise projects
- ✅ When comprehensive detail needed
- ✅ Post-prototype production system

---

## Testing Workflow

### Phase 1: Validate Structure (Week 1)
```bash
# Test with simplified templates
mcp ingest --source ./test-data/scenario-1-cozyhome
mcp analyze --project cozyhome
mcp generate --template simplified-sow --output ./output/
```

**Goal**: Prove placeholder replacement and conditional logic work

---

### Phase 2: Test All Integration Types (Week 2)
```bash
# Test each integration type with simplified templates
mcp generate --project brewcrew --template simplified # marketing
mcp generate --project petpawz --template simplified # fulfillment
mcp generate --project fitfuel --template simplified # inventory
mcp generate --project bloom --template simplified # pos
```

**Goal**: Validate conditional sections adapt correctly

---

### Phase 3: Refine Analysis Engine (Week 3-4)
- Use simplified templates for fast iteration
- Focus on improving gap detection
- Tune confidence scoring algorithm
- Test open question generation

**Goal**: Get analysis engine working accurately

---

### Phase 4: Upgrade to Full Templates (Week 5+)
- Port logic to full templates
- Add detail population
- Test with real projects
- Get team feedback

**Goal**: Production-ready system

---

## Placeholder Quick Reference

### Critical (Required)
- `[PROJECT_NAME]`
- `[CLIENT_NAME]`
- `[SYSTEM_A]` / `[SYSTEM_B]`
- `[INTEGRATION_TYPE]`
- `[CONFIDENCE_SCORE]`

### Discovery-Generated
- `[OPEN_QUESTIONS]`
- `[ASSUMPTIONS_TO_VALIDATE]`
- `[CURRENT_PAIN_POINTS]`
- `[BUSINESS_OBJECTIVES]`

### Timeline & Cost
- `[TOTAL_TIMELINE]`
- `[TOTAL_COST]`
- `[MONTHLY_FEE]`

### Technical
- `[ARCHITECTURE_PATTERN]`
- `[SYNC_FREQUENCY]`
- `[RATE_LIMIT]`

**Full list**: See `../PLACEHOLDER-REFERENCE.md`

---

## Example: CozyHome with Simplified Templates

### Input
- Discovery docs from `test-data/scenario-1-cozyhome/`
- Analysis results (confidence: 68%)

### Output
- `cozyhome-sow-simplified.md` (3 pages)
- `cozyhome-plan-simplified.md` (4 pages)
- `cozyhome-specs-simplified.md` (5 pages)

**vs. Full Templates**: 12 pages instead of 30+ pages

---

## Benefits for Prototyping

### Faster Iteration
- Less content to generate = faster testing
- Quicker to spot issues in logic
- Easier to read and validate

### Focus on Core Logic
- Test placeholder replacement thoroughly
- Validate conditional processing
- Prove confidence scoring concept
- Get gap detection working

### Lower Cognitive Load
- Easier for reviewers to assess
- Faster user feedback cycles
- Less overwhelming for demos

### Easier Debugging
- Fewer moving parts
- Simpler to trace issues
- Faster to regenerate

---

## Migration Path

When ready to move to full templates:

1. **Copy your population logic**
2. **Point to full template files** instead of simplified
3. **Add detail population** for new placeholders
4. **Test with one scenario** (CozyHome)
5. **Validate output quality**
6. **Roll out to all scenarios**

Most logic transfers directly - full templates just have more placeholders to fill.

---

## Testing Checklist

When testing with simplified templates:

- [ ] All critical placeholders replaced
- [ ] Conditional sections process correctly
- [ ] Confidence score displays properly
- [ ] Open questions formatted as list
- [ ] Assumptions section populated
- [ ] Cross-references have correct PROJECT_ID
- [ ] Integration-type conditionals work
- [ ] No stray [PLACEHOLDER] text
- [ ] No unparsed {{#if}} blocks
- [ ] Documents are readable and coherent

---

## File Comparison

| Aspect | Full SOW | Simplified SOW |
|--------|----------|----------------|
| Lines | ~500 | ~150 |
| Sections | 11 | 9 |
| Placeholders | ~50 | ~30 |
| Detail Level | High | Essential |
| Time to Read | 15 min | 5 min |

| Aspect | Full Plan | Simplified Plan |
|--------|-----------|-----------------|
| Lines | ~550 | ~200 |
| Sections | 11 | 10 |
| Placeholders | ~60 | ~40 |
| Tasks/Phase | 10-15 | 5-8 |
| Time to Read | 20 min | 8 min |

| Aspect | Full Specs | Simplified Specs |
|--------|------------|------------------|
| Lines | ~900 | ~250 |
| Sections | 15 | 12 |
| Placeholders | ~80 | ~50 |
| Code Examples | Multiple | Key ones only |
| Time to Read | 30 min | 12 min |

---

## Success Criteria

Simplified templates succeed when:

✅ MCP can generate all three docs from discovery data  
✅ Conditional sections adapt to integration type  
✅ Confidence scoring appears correctly  
✅ Open questions surface from analysis  
✅ Output is coherent and readable  
✅ Team can validate approach quickly  

Then you're ready for full templates.

---

## Tips

1. **Start here** - Don't jump straight to full templates
2. **Test all scenarios** - Ensure works for all integration types
3. **Get user feedback** - Show these to PMs and devs for input
4. **Iterate quickly** - Simplified templates enable fast cycles
5. **Graduate wisely** - Move to full templates when logic is solid

---

## Related Documentation

- **Parent directory**: `../README.md` - Full template guide
- **Placeholder reference**: `../PLACEHOLDER-REFERENCE.md` - Complete catalog
- **Examples**: `../examples/` - See full template examples
- **Quick start**: `../QUICK-START.md` - Getting started guide

---

**Purpose**: Rapid prototyping and testing  
**Status**: Ready for MCP development  
**Next Step**: Build template population logic against these first

