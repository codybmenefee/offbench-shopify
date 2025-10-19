# Quick Start Guide - Implementation Templates

## What You Got

✅ **3 Professional Templates** ready for MCP population  
✅ **Complete documentation** on how to use them  
✅ **Working example** based on CozyHome scenario  
✅ **Developer reference** for building MCP logic  

---

## Files Created

```
templates/
├── README.md                           # Complete usage guide (main doc)
├── QUICK-START.md                      # This file - quick overview
├── IMPLEMENTATION-SUMMARY.md           # Detailed summary of what was built
├── PLACEHOLDER-REFERENCE.md            # Developer reference for MCP builders
│
├── client-facing-sow.md                # Template: Statement of Work
├── internal-implementation-plan.md     # Template: Implementation Plan  
├── internal-technical-specs.md         # Template: Technical Specifications
│
└── examples/
    └── cozyhome-sow-example.md         # Fully populated SOW example
```

---

## The Three Templates

### 1. Statement of Work (SOW) - `client-facing-sow.md`
**For**: Client signature, legal/contractual  
**Tone**: Professional, non-technical  
**Length**: ~500 lines  
**Key Sections**: Project overview, scope, timeline, pricing, terms, acceptance  

### 2. Implementation Plan - `internal-implementation-plan.md`
**For**: Dev team execution, project management  
**Tone**: Action-oriented, practical  
**Length**: ~550 lines  
**Key Sections**: Phases, tasks, risks, testing, deployment, monitoring  

### 3. Technical Specifications - `internal-technical-specs.md`
**For**: Engineers, detailed technical blueprint  
**Tone**: Technical, detailed  
**Length**: ~900 lines  
**Key Sections**: Architecture, APIs, data mappings, error handling, security  

---

## How to Use

### Option 1: Manual (Right Now)

1. **Copy template** to your project folder
2. **Search** for `[PLACEHOLDERS]` in brackets
3. **Replace** with your project values
4. **Delete** conditional sections that don't apply (like `{{#if marketing}}`)
5. **Review** and polish

**Time**: 2-3 hours per project

---

### Option 2: MCP-Powered (After MCP Implementation)

```bash
# Future workflow when MCP is complete:

# 1. Ingest discovery documents
mcp ingest --source ./test-data/scenario-1-cozyhome

# 2. Analyze for gaps
mcp analyze --project cozyhome

# 3. Generate all three documents
mcp generate --project cozyhome --output ./output/

# Result: Three populated documents ready for review
```

**Time**: ~15 minutes per project (mostly review)

---

## Key Features

### ✨ Adaptive to Integration Type
Templates automatically adjust based on project type:
- **Accounting** (QuickBooks, Xero) - tax handling, reconciliation
- **Marketing** (Klaviyo, Mailchimp) - privacy, segmentation  
- **Fulfillment** (ShipStation) - shipping, tracking, returns
- **Inventory** (Stocky) - multi-location, stock sync
- **POS** - hardware, offline mode, end-of-day

### ✨ Built-in Confidence Scoring
Templates include sections for:
- Confidence score (0-100%)
- Open questions requiring answers
- Assumptions needing validation
- Warnings when clarity is too low

### ✨ Professional Quality
- Industry-standard SOW format
- Comprehensive technical coverage
- Real-world tested structure
- Ready for client presentation

---

## Example: See It In Action

Check out `examples/cozyhome-sow-example.md` to see a fully populated Statement of Work.

**Shows**:
- How placeholders get replaced
- How conditional sections work (accounting-specific content)
- How confidence scoring appears (68% with improvement recommendations)
- How gaps are surfaced (6 open questions, 4 assumptions)
- Real discovery conflicts identified (inventory system of record)

---

## For MCP Developers

### Building Template Population Logic

1. **Read**: `PLACEHOLDER-REFERENCE.md` - complete placeholder catalog
2. **Reference**: Sample population algorithm included
3. **Test**: Use CozyHome scenario data to validate
4. **Extend**: Add new placeholders as needed

### Priority Order

**Phase 1**: Populate critical placeholders (project name, systems, client)  
**Phase 2**: Add analysis results (confidence, gaps, questions)  
**Phase 3**: Process conditional sections  
**Phase 4**: Add optional details (team names, specific tools)  

---

## Next Steps

### Immediate (Manual Use)
1. Open `README.md` for complete usage guide
2. Copy a template for your next project
3. Use placeholder reference to fill it out
4. Review CozyHome example for guidance

### Near-Term (MCP Development)
1. Build document ingestion tools
2. Build analysis engine (gap detection, confidence scoring)
3. Build template population logic
4. Test with all 5 scenario types

### Long-Term (Production Use)
1. Integrate into Lazer workflow
2. Collect feedback from team
3. Refine templates based on real usage
4. Extend with new integration types

---

## Quick Reference

### Most Important Placeholders

| Placeholder | Example | Where to Find |
|-------------|---------|---------------|
| `[PROJECT_NAME]` | "CozyHome Shopify-QuickBooks" | User input |
| `[CLIENT_NAME]` | "CozyHome LLC" | Discovery docs |
| `[SYSTEM_A]` | "Shopify" | Discovery docs |
| `[SYSTEM_B]` | "QuickBooks Online" | Discovery docs |
| `[INTEGRATION_TYPE]` | "accounting" | Analysis or user |
| `[CONFIDENCE_SCORE]` | 68 | Analysis engine |
| `[OPEN_QUESTIONS]` | List of gaps | Gap detection |

### Integration Type Values
- `accounting` - QuickBooks, Xero, NetSuite
- `marketing` - Klaviyo, Mailchimp, HubSpot
- `fulfillment` - ShipStation, ShipBob
- `inventory` - Stocky, inventory management
- `pos` - Point-of-sale systems

### Conditional Syntax
```
{{#if accounting}}
  ... accounting-specific content ...
{{/if}}

{{#if CONFIDENCE_SCORE < 70}}
  ⚠️ Additional discovery recommended
{{/if}}
```

---

## Quality Checklist

Before delivering documents:

**SOW**:
- [ ] All `[PLACEHOLDERS]` replaced
- [ ] Conditional sections handled
- [ ] Professional tone maintained
- [ ] Pricing and terms clear
- [ ] Ready for client signature

**Implementation Plan**:
- [ ] All phases have tasks
- [ ] Tasks have owners
- [ ] Timeline is realistic
- [ ] Risks identified
- [ ] Exit criteria clear

**Technical Specs**:
- [ ] APIs documented
- [ ] Data mappings complete
- [ ] Error handling specified
- [ ] Security addressed
- [ ] Code examples included

---

## Support

### Documentation
- **Main Guide**: `README.md` (start here)
- **Summary**: `IMPLEMENTATION-SUMMARY.md` (what was built)
- **Developer Ref**: `PLACEHOLDER-REFERENCE.md` (for MCP builders)
- **This File**: `QUICK-START.md` (quick overview)

### Questions?
- Review the CozyHome example
- Check troubleshooting in README.md
- Contact Lazer dev tools team

---

## Success Metrics

These templates succeed when:

✅ Documents are usable with <15% manual editing  
✅ Confidence scores correlate with project success  
✅ Gaps are caught before implementation  
✅ Team prefers templates over starting from scratch  
✅ Discovery-to-plan time reduced by 50%+  

---

## Remember

> "The goal isn't perfect discovery — it's systematically better discovery. Surface the right questions at the right time. Make implicit assumptions explicit. Help humans do what they do best: make informed decisions."
> 
> — From AGENTS.md

These templates embody this philosophy by:
- Making gaps visible through confidence scoring
- Surfacing questions that need answers
- Capturing assumptions that need validation
- Guiding teams toward better outcomes

---

**Created**: January 2024  
**Version**: 1.0  
**Ready to Use**: Yes - start with manual population, build MCP next  
**Questions**: See README.md or contact dev tools team

