# Implementation Document Templates

This directory contains **reference templates** that serve as examples for AI agents generating implementation documentation from discovery artifacts.

---

## Philosophy: Templates as Reference, Not Forms

**OLD APPROACH** (rigid): Fill placeholders like `[PROJECT_NAME]`, `[CLIENT_NAME]` mechanically  
**NEW APPROACH** (flexible): AI agents use templates as reference examples to write contextual, natural documents

### How It Works

1. **AI agent calls** `get_template(template_type)` to see the example structure
2. **AI agent calls** `analyze_discovery(project_id)` to get project data and analysis
3. **AI agent writes** its own version, guided by template structure but with full creative flexibility
4. **Result**: Natural, contextual documents that adapt to the specific project context

This approach enables:
- ✅ More natural, contextual writing
- ✅ Better adaptation to unique project needs
- ✅ Flexibility in tone and detail level
- ✅ Intelligent summarization and synthesis
- ✅ No rigid placeholder mapping

---

## Template Overview

### 1. Client-Facing Statement of Work (`client-facing-sow.md`)

**Purpose**: Formal contract document for client signature  
**Audience**: Client stakeholders, legal/procurement teams  
**Tone**: Professional, clear, non-technical  

**Key Sections**:
- Project overview and business objectives
- High-level technical scope
- Deliverables and success criteria
- Timeline and pricing
- Legal terms (assumptions, out of scope, acceptance)

---

### 2. Internal Implementation Plan (`internal-implementation-plan.md`)

**Purpose**: Action-oriented guide for dev team execution  
**Audience**: Project managers, development team, QA engineers  
**Tone**: Practical, action-oriented, clear  

**Key Sections**:
- Executive summary and business context
- Phase-by-phase implementation tasks
- Team assignments and responsibilities
- Risk assessment and testing strategy
- Deployment and monitoring plans

---

### 3. Internal Technical Specifications (`internal-technical-specs.md`)

**Purpose**: Detailed technical blueprint for developers  
**Audience**: Software engineers, DevOps, architects  
**Tone**: Technical, detailed, precise  

**Key Sections**:
- System architecture and data flows
- API endpoints and authentication
- Field-level data mappings
- Error handling and security
- Edge cases and business rules

---

## Using These Templates

### As an AI Agent

```
1. Load template: get_template("sow")
2. Get project data: analyze_discovery("scenario-1-cozyhome")
3. Synthesize information and write contextual document
4. Use template structure as guide, but adapt to context
5. Include relevant sections, skip irrelevant ones
6. Write naturally, not mechanically
```

### As a Human

These templates provide examples of:
- What sections to include
- Appropriate level of detail
- Professional tone and structure
- How to organize information
- Integration type-specific considerations

**Copy the structure, not the exact content.** Adapt to your specific project needs.

---

## Template Features

### Conditional Sections by Integration Type

Templates include examples for different integration types:
- **Accounting** - Order-to-invoice sync, tax handling, reconciliation
- **Marketing** - Customer sync, segmentation, email automation
- **Fulfillment** - Order routing, shipping labels, tracking
- **Inventory** - Multi-location sync, stock alerts, reconciliation
- **POS** - Daily sales sync, cross-channel inventory

**For AI agents**: Include sections relevant to the detected integration type, skip others.

### Confidence Score Integration

Templates demonstrate how to integrate confidence scores from the discovery analysis:
- Show confidence score prominently
- Recommend additional discovery if confidence is low (<70%)
- Link confidence to open questions that need clarification

---

## Example: CozyHome Scenario

Using `scenario-1-cozyhome` test data:

**Input**:
- Discovery documents: 2 emails, 1 draft SOW, 1 product catalog
- Analysis result: 81% confidence, 2 gaps, 4 ambiguities, 1 conflict
- Systems identified: Shopify, QuickBooks Online
- Integration type: Accounting

**Template Usage**:
- Load `client-facing-sow.md` as reference
- Write SOW incorporating:
  - CozyHome business context (home décor retailer)
  - Pain points (3+ hours/day manual reconciliation)
  - Shopify-QuickBooks integration scope
  - Accounting-specific sections (order-to-invoice, tax handling)
  - Open questions section (inventory source of truth conflict)
  - 81% confidence score with recommendation to clarify gaps

See `templates/examples/cozyhome-sow-example.md` for the result.

---

## Quality Checklist

### For All Documents
- [ ] Written naturally, not mechanically filled
- [ ] Appropriate detail level for audience
- [ ] Clear and professional tone
- [ ] All critical information included
- [ ] No placeholder markers remain

### For Client-Facing SOW
- [ ] Business context clearly explained
- [ ] Non-technical language used
- [ ] Pricing and timeline included
- [ ] Open questions highlighted
- [ ] Ready for client signature

### For Implementation Plan
- [ ] Clear action items and owners
- [ ] Realistic timeline
- [ ] Risk assessment included
- [ ] Exit criteria defined
- [ ] Testing strategy outlined

### For Technical Specs
- [ ] API endpoints documented
- [ ] Data mappings specified
- [ ] Error handling defined
- [ ] Security addressed
- [ ] Edge cases covered

---

## Best Practices

### 1. Use Discovery Data as Source of Truth
Don't invent information. Base documents on actual discovery artifacts and analysis results.

### 2. Adapt to Context
Simple projects need simple docs. Complex projects need more detail. Match the complexity.

### 3. Highlight Gaps Explicitly
Use the "Open Questions" section to call out areas needing clarification. This builds trust.

### 4. Include Confidence Scores
Show confidence scores to set expectations. If confidence is low, recommend more discovery.

### 5. Write for the Audience
- **SOW**: Client-friendly, professional, clear value proposition
- **Implementation Plan**: Action-oriented, practical, team-focused
- **Technical Specs**: Detailed, precise, engineer-friendly

### 6. Cross-Reference Appropriately
Link documents together so stakeholders can find related information easily.

---

## Template Maintenance

### Adding New Integration Types
To support a new integration category:
1. Add example sections to relevant templates
2. Document the integration type here
3. Test with real project scenario

### Extending Templates
To add new sections:
1. Add to appropriate template(s)
2. Provide clear example content
3. Document in this README
4. Test with AI agent generation

### Feedback & Improvements
Templates evolve based on:
- Real project usage
- Stakeholder feedback
- New integration patterns
- Lessons learned

Submit improvements via PR with rationale and examples.

---

## Related Documentation

- **AGENTS.md** - Developer guide for building the discovery tool
- **README.md** - Project overview
- **SCENARIOS.md** - Test scenarios for validation
- **test-data/** - Example discovery documents
- **templates/examples/** - Example generated documents

---

**Last Updated**: January 2024  
**Version**: 2.0 (Reference-based approach)  
**Maintained By**: Lazer Technologies Dev Tools Team
