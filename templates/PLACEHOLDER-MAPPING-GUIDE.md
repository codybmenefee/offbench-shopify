# Placeholder Mapping Guide

This document maps template placeholders to analysis result fields, helping AI agents fill templates with discovery data.

---

## Analysis Result Structure

When you call `analyze_discovery(project_id)`, you receive:

```json
{
  "analysis": {
    "gaps": [...],
    "ambiguities": [...],
    "conflicts": [...],
    "clarity_score": 85.0,
    "completeness_score": 70.0,
    "alignment_score": 85.0,
    "overall_confidence": 78.5,
    "systems_identified": ["Shopify", "QuickBooks"],
    "client_name": "CozyHome",
    "pain_points": ["spending 3+ hours daily on manual reconciliation"],
    "business_objectives": ["automate order-to-invoice process", "reduce errors"]
  }
}
```

---

## SOW Template Mapping (`client-facing-sow.md`)

### Header Section

| Placeholder | Source | Example | Notes |
|-------------|--------|---------|-------|
| `[PROJECT_NAME]` | `analysis.systems_identified` + "Integration" | "Shopify-QuickBooks Integration" | Join systems with hyphen |
| `[CLIENT_NAME]` | `analysis.client_name` | "CozyHome" | From analysis |
| `[CLIENT_CONTACT_NAME]` | Not in analysis | "Sarah Johnson" | Get from user or leave for manual fill |
| `[CLIENT_CONTACT_TITLE]` | Not in analysis | "Owner" | Get from user or leave for manual fill |
| `[DATE]` | Current date | "October 19, 2025" | Use today's date |

### Section 1: Project Overview

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[BUSINESS_DESCRIPTION]` | `project.project_description` or infer from documents | Brief business description |
| `[CURRENT_PAIN_POINTS]` | `analysis.pain_points[]` | List all pain points found |
| `[OBJECTIVE_1]`, `[OBJECTIVE_2]`, etc. | `analysis.business_objectives[]` | List objectives from analysis |
| `[SUCCESS_METRIC_1]`, etc. | Check gaps for "success_criteria" category | If missing, note as open question |

### Section 2: Technical Scope

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[SYSTEM_A]` | `analysis.systems_identified[0]` | First system |
| `[SYSTEM_B]` | `analysis.systems_identified[1]` | Second system |
| `[SYSTEM_A_ROLE]` | Infer from context | Describe system's role |
| `[SYSTEM_B_ROLE]` | Infer from context | Describe system's role |
| `[HIGH_LEVEL_INTEGRATION_DESCRIPTION]` | Synthesize from documents | 2-3 sentence overview |

**Conditional Sections**: Include based on detected integration type:
- `{{#if accounting}}` - If systems include QuickBooks, Xero, NetSuite
- `{{#if marketing}}` - If systems include Klaviyo, Mailchimp, HubSpot
- `{{#if fulfillment}}` - If systems include ShipStation, ShipBob
- `{{#if inventory}}` - If content mentions "inventory", "stock", "multi-location"
- `{{#if pos}}` - If systems include POS software

| Integration-Specific Placeholder | Source | Notes |
|----------------------------------|--------|-------|
| `[ACCOUNTING_SYSTEM]` | From `systems_identified` | QuickBooks, Xero, etc. |
| `[TAX_HANDLING_APPROACH]` | Check gaps for "tax" | If gap exists, note as TBD |
| `[PAYMENT_SYNC_DETAILS]` | From documents | How payments sync |
| `[MARKETING_PLATFORM]` | From `systems_identified` | Klaviyo, Mailchimp, etc. |
| `[SEGMENTATION_CRITERIA]` | From documents | Customer segmentation rules |
| `[FULFILLMENT_SYSTEM]` | From `systems_identified` | ShipStation, etc. |
| `[RETURNS_HANDLING_APPROACH]` | Check gaps for "return" | If gap exists, note as TBD |

### Section 2.4: Data Synchronization Table

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[DATA_TYPE_1]` | Infer from systems | "Orders", "Invoices", "Customers" |
| `[SOURCE_1]` | From systems | Which system data comes from |
| `[DEST_1]` | From systems | Which system receives data |
| `[FREQ_1]` | Check gaps for "sync frequency" | If ambiguous, note in gaps |

### Section 4: Timeline & Milestones

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[DISCOVERY_DURATION]` | Standard estimate | "1-2 weeks" |
| `[DEV_DURATION]` | Based on complexity | "2-4 weeks" typical |
| `[TEST_DURATION]` | Standard estimate | "1 week" |
| `[TOTAL_TIMELINE]` | Sum of phases | "4-8 weeks" |
| `[*_END_DATE]` | Calculate from start | Add durations to current date |

### Section 5: Investment

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[TOTAL_COST]` | Not in analysis | Leave as `[TBD]` or use standard rates |
| `[MONTHLY_FEE]` | Not in analysis | Leave as `[TBD]` or use standard rates |
| `[SUPPORT_HOURS]` | Not in analysis | Typically "5-10 hours/month" |

### Section 6: Assumptions & Dependencies

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[REVIEW_TIMEFRAME]` | Standard | "3-5 business days" |
| `[ADDITIONAL_CLIENT_RESPONSIBILITIES]` | Infer from context | Add context-specific items |
| `[ADDITIONAL_TECHNICAL_ASSUMPTIONS]` | From gaps | Turn assumptions into list items |

### Section 10: Open Questions

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[OPEN_QUESTIONS]` | `analysis.gaps[]` where `answered=false` | Format as numbered list with priority |
| `[ASSUMPTIONS_TO_VALIDATE]` | `analysis.ambiguities[]` | Format as list |
| `[CONFIDENCE_SCORE]` | `analysis.overall_confidence` | Round to nearest integer |

**Important**: If confidence < 70%, add warning about additional discovery.

---

## Implementation Plan Template Mapping (`internal-implementation-plan.md`)

### Header Section

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[PROJECT_ID]` | `project.project_id` | "scenario-1-cozyhome" |
| `[INTEGRATION_TYPE]` | Detect from systems | "Accounting", "Marketing", etc. |
| `[LEAD_ENGINEER]` | Not in analysis | Leave as `[TBD]` |
| `[PROJECT_MANAGER]` | Not in analysis | Leave as `[TBD]` |
| `[STATUS]` | Default | "Planning" |

### Executive Summary

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[ONE_PARAGRAPH_SUMMARY]` | Synthesize | Combine objectives + pain points + solution |
| `[VOLUME_ESTIMATE]` | From documents | Look for volume mentions |

### Section 1: Project Context

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[CURRENT_STATE_DESCRIPTION]` | `pain_points` + documents | Describe current manual process |
| `[PAIN_POINT_1]`, etc. | `analysis.pain_points[]` | Direct mapping |
| `[BUSINESS_IMPACT_1]`, etc. | `analysis.business_objectives[]` | Reframe as impact statements |
| `[TIME_SAVINGS]` | Calculate from pain points | If "3 hours daily" mentioned, calculate |
| `[APPROACH_RATIONALE]` | Synthesize | Why this technical approach makes sense |

### Section 2: Implementation Phases

**Phase Durations**: Use standard estimates based on confidence score:
- High confidence (>80%): Shorter timelines
- Medium confidence (60-80%): Standard timelines  
- Low confidence (<60%): Add discovery buffer

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[PHASE_*_DURATION]` | Based on confidence | 1-2 weeks per phase |
| `[PHASE_*_STATUS]` | Default | "Not Started" |
| `[WORKFLOW_1]`, etc. | From documents | Key workflows to implement |

**Conditional Sections**: Same as SOW - include based on integration type.

### Section 3: Technical Risks

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[RISK_1]`, etc. | `analysis.gaps[]` + `conflicts[]` | High priority gaps = risks |
| `[RISK_LIKELIHOOD]` | Based on gap priority | HIGH gap = "Medium-High" likelihood |
| `[MITIGATION_STRATEGY]` | For each gap | How to address the risk |

### Section 5: Testing Strategy

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[TEST_SCENARIO_1]`, etc. | Generate from objectives | Cover happy path + edge cases |
| Edge cases | `analysis.gaps[]` for "edge_cases" | If missing, note as TBD |

---

## Technical Specs Template Mapping (`internal-technical-specs.md`)

### Header Section

Same as Implementation Plan header.

### Section 1: System Architecture

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[ARCHITECTURE_PATTERN]` | Infer from requirements | "Event-driven" if real-time, "Scheduled batch" if periodic |
| `[ARCHITECTURE_RATIONALE]` | Based on sync frequency gap | Explain why this pattern |
| `[RUNTIME]`, `[FRAMEWORK]` | Standard choices | Python/FastAPI, Node/Express, etc. |
| `[DATABASE]` | Based on needs | PostgreSQL typical |
| `[HOSTING_PROVIDER]` | Standard | "AWS", "Heroku", etc. |

### Section 2: Data Flow Diagrams

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[FLOW_NAME_1]` | From objectives | "Order Sync", "Customer Sync" |
| `[TRIGGER_DESCRIPTION]` | From documents | "When order is paid", "Nightly at 2am" |
| `[LATENCY_ESTIMATE]` | Based on pattern | Real-time: "< 30 seconds", Batch: "1-5 minutes" |
| `[RETRY_STRATEGY]` | Check gaps | If no error handling gap, use standard strategy |
| `[IDEMPOTENCY_APPROACH]` | Technical decision | Describe approach |

**Conditional Sections**: Include integration-type-specific flows based on detection.

### Section 3: API Integration Details

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[SYSTEM_A_API_VERSION]` | Look in documents | Check for version mentions |
| `[AUTH_METHOD]` | Check gaps for "authentication" | If gap, note as TBD |
| `[BASE_URL]` | Standard for system | Use official docs URL |
| `[RATE_LIMIT]` | Check gaps | If mentioned, use it; else research standard limits |

### Section 4: Data Mapping

This section requires detailed field mapping. Generate tables like:

| Shopify Field | QuickBooks Field | Transformation | Notes |
|---------------|------------------|----------------|-------|
| order.id | Invoice.DocNumber | Direct | Unique identifier |
| order.total_price | Invoice.TotalAmt | Direct | Currency conversion if needed |

**Source**: Infer from common field mappings for these system types.

### Section 5: Business Rules

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[RULE_1]`, etc. | From documents + gaps | Explicit rules + note gaps as TBD |

Check gaps for:
- `business_rules` category - these are missing rules
- `conflicts[]` - these are conflicting rules that need resolution

### Section 6: Error Handling

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[ERROR_TYPE_1]`, etc. | Standard integration errors | Network, validation, rate limit, auth |
| `[ERROR_STRATEGY]` | Check gaps for "error_handling" | If gap exists, use conservative default |

### Section 7: Security

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[SECRET_STORAGE]` | Standard | "AWS Secrets Manager", "Doppler" |
| `[ENCRYPTION]` | Standard | "TLS 1.3", "AES-256" |
| `[COMPLIANCE_REQUIREMENTS]` | From documents | Look for GDPR, CCPA mentions |

### Section 8: Edge Cases

| Placeholder | Source | Notes |
|-------------|--------|-------|
| `[EDGE_CASE_1]`, etc. | `analysis.gaps[]` for "edge_cases" category | If missing, generate common ones |

Common edge cases by integration type:
- **Accounting**: Partial refunds, split payments, multi-currency
- **Marketing**: Unsubscribed users, duplicate emails, GDPR requests
- **Fulfillment**: Partial shipments, address validation, international shipping
- **Inventory**: Negative stock, transfer orders, bundled products

---

## Integration Type Detection

Use this logic to determine which conditional sections to include:

### Accounting Integration
**Detect if**: Systems include QuickBooks, Xero, NetSuite, FreshBooks  
**OR**: Documents mention "invoice", "accounting", "financial", "reconciliation"

### Marketing Integration
**Detect if**: Systems include Klaviyo, Mailchimp, HubSpot, ActiveCampaign  
**OR**: Documents mention "email", "marketing", "campaign", "segmentation"

### Fulfillment Integration
**Detect if**: Systems include ShipStation, ShipBob, Shippo, EasyPost  
**OR**: Documents mention "shipping", "fulfillment", "tracking", "label"

### Inventory Integration
**Detect if**: Documents mention "inventory", "stock", "multi-location", "warehouse"  
**AND**: Primary focus is inventory sync (not just incidental mention)

### POS Integration
**Detect if**: Systems include Square, Clover, Toast, Lightspeed  
**OR**: Documents mention "point of sale", "POS", "retail location"

---

## Handling Missing Data

When data is not available from analysis:

1. **Critical business info** (pricing, timeline, contacts): Leave as `[TBD]` and note in Open Questions
2. **Technical details** (API versions, rate limits): Use industry standard defaults or research
3. **Standard estimates** (timelines, support hours): Use company standards
4. **Inferred data** (integration type, workflows): Make reasonable inferences from context

**Always be transparent**: If you're making assumptions, note them in the "Assumptions to Validate" section.

---

## Quality Checklist

Before outputting a filled template:

- [ ] All critical placeholders filled (no `[UNDEFINED]`)
- [ ] Confidence score included in Open Questions section
- [ ] High priority gaps included in Open Questions
- [ ] Integration type detected correctly
- [ ] Only relevant conditional sections included
- [ ] Business context reflects actual pain points
- [ ] Technical approach aligns with requirements
- [ ] Ambiguities noted in Assumptions section
- [ ] Conflicts highlighted for resolution
- [ ] Timeline realistic based on confidence score

---

## Example Workflow

```python
# 1. Get project analysis
analysis_result = analyze_discovery("scenario-1-cozyhome")

# 2. Get template
template_result = get_template("sow")

# 3. Extract data
client_name = analysis_result["analysis"]["client_name"]
systems = analysis_result["analysis"]["systems_identified"]
confidence = analysis_result["analysis"]["overall_confidence"]
gaps = analysis_result["analysis"]["gaps"]
pain_points = analysis_result["analysis"]["pain_points"]

# 4. Fill placeholders
# Replace [CLIENT_NAME] with client_name
# Replace [SYSTEM_A] with systems[0]
# etc.

# 5. Handle gaps
# For each gap with priority HIGH, add to Open Questions section

# 6. Add confidence score
# Include in Section 10.3

# 7. Output filled template to user
```

---

**Last Updated**: October 2025  
**Version**: 1.0  
**For Use By**: AI agents generating deliverables from discovery analysis

