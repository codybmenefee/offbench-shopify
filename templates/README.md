# Implementation Document Templates

This directory contains standardized templates for generating implementation documentation from discovery artifacts. These templates are designed to be populated by the MCP discovery analysis tool or manually filled for projects.

---

## Template Overview

### 1. Client-Facing Statement of Work (`client-facing-sow.md`)

**Purpose**: Formal contract document for client signature  
**Audience**: Client stakeholders, legal/procurement teams  
**Tone**: Professional, clear, non-technical  

**When to Use**: 
- For all client-facing contracts
- Before project kick-off (after discovery)
- When formalizing scope and pricing

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

**When to Use**:
- To guide development team through implementation
- For project tracking and progress monitoring
- To coordinate cross-functional activities

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

**When to Use**:
- As the source of truth for technical implementation
- During development for reference
- For onboarding new engineers to the project

**Key Sections**:
- System architecture and data flows
- API endpoints and authentication
- Field-level data mappings
- Error handling and security
- Edge cases and business rules

---

## How to Use These Templates

### Option 1: MCP-Powered Generation (Recommended)

The MCP discovery tool will automatically populate these templates:

1. **Ingest discovery documents** (emails, transcripts, SOWs, etc.)
2. **Run analysis** to detect gaps and ambiguities
3. **Generate documents** from templates with confidence scoring
4. **Iterate** by answering open questions and regenerating

```bash
# Example MCP workflow (when implemented)
mcp ingest --source ./test-data/scenario-1-cozyhome
mcp analyze --project cozyhome
mcp generate --template sow --output ./output/cozyhome-sow.md
mcp generate --template implementation-plan --output ./output/cozyhome-plan.md
mcp generate --template technical-specs --output ./output/cozyhome-specs.md
```

### Option 2: Manual Population

If filling manually:

1. **Copy the template** to your project directory
2. **Search and replace** placeholder values (see Placeholder Reference below)
3. **Remove conditional sections** that don't apply
4. **Fill in blanks** with project-specific details
5. **Review and validate** with stakeholders

---

## Placeholder System

### Standard Placeholders

All templates use these common placeholders:

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `[PROJECT_NAME]` | Full project name | "CozyHome Shopify-QuickBooks Integration" |
| `[PROJECT_ID]` | Short project identifier | "cozyhome-qb-integration" |
| `[CLIENT_NAME]` | Client company name | "CozyHome LLC" |
| `[CLIENT_CONTACT_NAME]` | Primary client contact | "Sarah Chen" |
| `[CLIENT_CONTACT_TITLE]` | Contact's job title | "Owner" |
| `[DATE]` | Document date | "January 17, 2024" |
| `[INTEGRATION_TYPE]` | Integration category | "accounting" / "marketing" / "fulfillment" / "inventory" / "pos" |
| `[SYSTEM_A]` | First system in integration | "Shopify" |
| `[SYSTEM_B]` | Second system in integration | "QuickBooks Online" |
| `[CONFIDENCE_SCORE]` | Implementation readiness (0-100) | "72" |

### Discovery-Generated Placeholders

These are auto-populated by the MCP analysis engine:

| Placeholder | Source | Description |
|-------------|--------|-------------|
| `[OPEN_QUESTIONS]` | Gap detection | List of questions requiring clarification |
| `[ASSUMPTIONS_TO_VALIDATE]` | Analysis engine | Assumptions that should be confirmed |
| `[CURRENT_PAIN_POINTS]` | Discovery docs | Client's current challenges |
| `[BUSINESS_OBJECTIVES]` | Discovery docs | Project goals extracted from conversations |

### Technical Placeholders

Used primarily in technical specs:

| Placeholder | Example Value |
|-------------|---------------|
| `[API_ENDPOINT]` | "https://api.shopify.com/admin/orders.json" |
| `[AUTH_METHOD]` | "OAuth 2.0" |
| `[RATE_LIMIT]` | "40 requests/second" |
| `[SYNC_FREQUENCY]` | "Real-time via webhooks" |
| `[ERROR_HANDLING]` | "Exponential backoff with max 3 retries" |

---

## Conditional Sections

Templates include conditional sections that adapt to project type. These use Handlebars-style syntax:

```
{{#if accounting}}
### Accounting-Specific Content
...
{{/if}}
```

### Integration Type Conditions

- `{{#if accounting}}` - For QuickBooks, Xero, NetSuite integrations
- `{{#if marketing}}` - For Klaviyo, Mailchimp, HubSpot integrations
- `{{#if fulfillment}}` - For ShipStation, ShipBob integrations
- `{{#if inventory}}` - For Stocky, inventory management integrations
- `{{#if pos}}` - For Point-of-sale system integrations

### Manual Use of Conditionals

If filling manually:
1. **Determine your integration type**
2. **Keep relevant conditional sections**, remove the markers
3. **Delete irrelevant sections**

**Example**: For an accounting integration, keep everything inside `{{#if accounting}}` blocks and delete marketing/fulfillment/inventory/pos blocks.

---

## Document Cross-References

The three templates are designed to work together:

### Client-Facing SOW References:
- Points to internal docs at bottom (for team use only)
- References implementation plan for technical details
- Links to technical specs for architecture

### Implementation Plan References:
- References SOW for contractual obligations
- Links to specific sections of technical specs
- Points to test cases and deployment runbooks

### Technical Specs References:
- References SOW section numbers for traceability
- Links back to implementation plan phases
- Points to external API documentation

**Best Practice**: Use consistent `[PROJECT_ID]` across all documents for easy cross-referencing.

---

## Template Maintenance & Extension

### Adding New Conditional Sections

To add support for a new integration type:

1. **Define the condition** (e.g., `{{#if crm}}`)
2. **Add conditional sections** to all three templates where relevant
3. **Update this README** with the new condition type
4. **Test** with a real project scenario

### Adding New Placeholders

When adding new placeholders:

1. **Use bracket notation**: `[PLACEHOLDER_NAME]`
2. **Document in this README**
3. **Update MCP generation logic** to populate the placeholder
4. **Provide example values**

### Extending Templates

To add new sections:

1. **Identify which template** needs the section
2. **Add to the appropriate location** (maintain logical flow)
3. **Use placeholders** for variable content
4. **Add conditional logic** if section is type-specific
5. **Update this README**

---

## Confidence Score Integration

The templates include built-in **Confidence Score** sections that integrate with the MCP analysis engine:

### What is the Confidence Score?

A quantitative measure (0-100%) of implementation readiness based on:
- **Clarity**: Are requirements unambiguous?
- **Completeness**: Is all necessary information present?
- **Alignment**: Do stakeholders agree?

### How It's Used in Templates

**In SOW (Section 10.3)**:
```markdown
**Current Implementation Readiness**: [CONFIDENCE_SCORE]%

{{#if CONFIDENCE_SCORE < 70}}
⚠️ **Recommendation**: Additional discovery recommended
{{/if}}
```

**In Implementation Plan (Executive Summary)**:
```markdown
**Confidence Score**: [CONFIDENCE_SCORE]%
```

### Score Ranges & Interpretation

| Score | Interpretation | Recommendation |
|-------|---------------|----------------|
| 90-100% | Excellent clarity | Proceed to development |
| 75-89% | Good, minor gaps | Clarify open questions first |
| 60-74% | Moderate gaps | Additional discovery recommended |
| <60% | Significant gaps | Do not proceed without more discovery |

---

## Example: CozyHome Scenario

Using the `scenario-1-cozyhome` test data:

### Key Values
- **Project Name**: "CozyHome Shopify-QuickBooks Integration"
- **Integration Type**: "accounting"
- **System A**: "Shopify"
- **System B**: "QuickBooks Online"
- **Client**: "CozyHome LLC"
- **Contact**: "Sarah Chen, Owner"

### Generated Documents
1. `cozyhome-qb-sow.md` - Client signs this
2. `cozyhome-qb-implementation-plan.md` - Dev team uses this
3. `cozyhome-qb-technical-specs.md` - Engineers reference this

### Conditional Sections Used
- Accounting-specific sections (tax handling, reconciliation)
- Order-to-invoice mapping
- Financial data flows

---

## Quality Checklist

Before considering a generated document complete:

### For All Documents
- [ ] All `[PLACEHOLDERS]` replaced with real values
- [ ] No `{{#if}}` conditional markers remain
- [ ] Cross-references point to correct document names
- [ ] Dates and version numbers are current
- [ ] Grammar and spelling checked

### For Client-Facing SOW
- [ ] Professional tone maintained throughout
- [ ] Technical jargon minimized or explained
- [ ] Pricing and payment terms clear
- [ ] Legal sections reviewed (assumptions, out of scope)
- [ ] Signature block ready

### For Implementation Plan
- [ ] All tasks have owners assigned
- [ ] Timeline is realistic and achievable
- [ ] Exit criteria clearly defined for each phase
- [ ] Risk assessment complete
- [ ] Success criteria measurable

### For Technical Specs
- [ ] API endpoints documented with examples
- [ ] Data mappings complete at field level
- [ ] Error handling clearly specified
- [ ] Security requirements addressed
- [ ] Performance targets defined

---

## Best Practices

### 1. Start with Discovery
Don't try to fill templates without adequate discovery. Garbage in = garbage out.

### 2. Iterate on Confidence
Use the confidence score to guide further discovery. If score is low, answer open questions and regenerate.

### 3. Keep Documents Synchronized
When you update one document (e.g., add a field to technical specs), update references in the other documents.

### 4. Version Control
- Use version numbers on all documents
- Track changes in the change log section
- Keep old versions for reference

### 5. Review with Stakeholders
- **SOW**: Review with client and legal
- **Implementation Plan**: Review with PM and dev team
- **Technical Specs**: Review with lead engineer and architects

### 6. Don't Over-Engineer
Simple projects need simple docs. Don't fill every section if it's not relevant. Remove unnecessary complexity.

---

## Troubleshooting

### Problem: Too many open questions after generation
**Solution**: Run more discovery activities. Schedule calls to clarify ambiguities.

### Problem: Conditional sections don't match project type
**Solution**: Review integration type selection. Manually adjust conditional sections if needed.

### Problem: Client finds SOW too technical
**Solution**: Simplify Section 2 (Technical Scope). Move details to technical specs.

### Problem: Dev team says specs aren't detailed enough
**Solution**: Add more detail to data mapping tables and API endpoint sections. Include code examples.

### Problem: Documents don't stay synchronized
**Solution**: Use a single source of truth (technical specs) and reference it from other docs rather than duplicating content.

---

## Support & Feedback

For questions or improvements to these templates:

1. **Internal**: Contact the Lazer dev tools team
2. **Issues**: Document in project issue tracker
3. **Improvements**: Submit PR with template updates
4. **New Use Cases**: Share your scenario so we can extend templates

---

## Related Documentation

- **AGENTS.md** - Developer guide for building the discovery tool
- **README.md** - Project overview
- **SCENARIOS.md** - Test scenarios for validation
- **test-data/** - Example discovery documents

---

**Last Updated**: January 2024  
**Version**: 1.0  
**Maintained By**: Lazer Technologies Dev Tools Team

