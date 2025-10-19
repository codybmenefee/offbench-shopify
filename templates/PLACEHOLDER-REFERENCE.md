# Template Placeholder Quick Reference

This document provides a quick lookup for all placeholders used in the implementation templates. Use this when building MCP template population logic.

---

## Core Placeholders (All Templates)

| Placeholder | Type | Source | Example Value | Required |
|-------------|------|--------|---------------|----------|
| `[PROJECT_NAME]` | String | User input or generated | "CozyHome Shopify-QuickBooks Integration" | Yes |
| `[PROJECT_ID]` | String | Generated (slug format) | "cozyhome-qb-integration" | Yes |
| `[CLIENT_NAME]` | String | Discovery docs | "CozyHome LLC" | Yes |
| `[CLIENT_CONTACT_NAME]` | String | Discovery docs | "Sarah Chen" | Yes |
| `[CLIENT_CONTACT_TITLE]` | String | Discovery docs | "Owner" | Yes |
| `[DATE]` | Date | Current date | "January 17, 2024" | Yes |
| `[INTEGRATION_TYPE]` | Enum | Analysis or user input | accounting/marketing/fulfillment/inventory/pos | Yes |
| `[SYSTEM_A]` | String | Discovery docs | "Shopify" | Yes |
| `[SYSTEM_B]` | String | Discovery docs | "QuickBooks Online" | Yes |
| `[CONFIDENCE_SCORE]` | Integer (0-100) | Analysis engine | 68 | Yes |
| `[VERSION]` | String | Document versioning | "1.0" or "1.1 (Draft)" | Yes |

---

## Discovery-Generated Content Placeholders

These are populated by the analysis engine:

| Placeholder | Type | Source | Format | Example |
|-------------|------|--------|--------|---------|
| `[OPEN_QUESTIONS]` | List | Gap detection | Numbered list | "1. How should refunds be handled?\n2. Which system is inventory SOR?" |
| `[ASSUMPTIONS_TO_VALIDATE]` | List | Analysis engine | Numbered list | "1. All orders use standard checkout\n2. No multi-currency" |
| `[CURRENT_PAIN_POINTS]` | List | Discovery docs | Bullet list | "- 3 hours/day manual entry\n- Accounting errors" |
| `[BUSINESS_OBJECTIVES]` | List | Discovery docs | Bullet list | "- Eliminate manual entry\n- Improve accuracy" |
| `[SUCCESS_METRICS]` | List | Discovery docs | Bullet list | "- Zero manual entry\n- >95% inventory accuracy" |

---

## Business Context Placeholders

| Placeholder | Type | Source | Example |
|-------------|------|--------|---------|
| `[BUSINESS_DESCRIPTION]` | String | Discovery docs | "a small home décor retailer selling online through Shopify" |
| `[CURRENT_STATE_DESCRIPTION]` | String | Discovery docs | "manually copying order information from Shopify into QuickBooks" |
| `[HIGH_LEVEL_INTEGRATION_DESCRIPTION]` | String | Generated | "automatically synchronizes order data from Shopify to QuickBooks" |
| `[APPROACH_RATIONALE]` | String | Generated | "webhook-based real-time sync provides immediate visibility while batch inventory sync reduces API load" |

---

## System Details Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[SYSTEM_A_ROLE]` | String | "E-commerce platform, order management" |
| `[SYSTEM_A_USAGE_DETAILS]` | String | "~200 orders/week, 250 product SKUs" |
| `[SYSTEM_B_ROLE]` | String | "Accounting system of record" |
| `[SYSTEM_B_USAGE_DETAILS]` | String | "Manual invoice entry, financial reporting" |

---

## Timeline & Cost Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[TOTAL_TIMELINE]` | String | "6 weeks from contract signing" |
| `[DISCOVERY_DURATION]` | String | "1 week" |
| `[DISCOVERY_END_DATE]` | Date | "Jan 25, 2024" |
| `[DEV_DURATION]` | String | "2 weeks" |
| `[DEV_END_DATE]` | Date | "Feb 8, 2024" |
| `[TEST_DURATION]` | String | "1 week" |
| `[TEST_END_DATE]` | Date | "Feb 15, 2024" |
| `[DEPLOY_DURATION]` | String | "3 days" |
| `[DEPLOY_DATE]` | Date | "Feb 18, 2024" |
| `[SUPPORT_DURATION]` | String | "2 weeks" |
| `[SUPPORT_END_DATE]` | Date | "Mar 3, 2024" |
| `[TOTAL_COST]` | Currency | "$12,500" |
| `[MONTHLY_FEE]` | Currency | "$350" |
| `[PAYMENT_1_AMOUNT]` | Currency | "$6,250" |
| `[PAYMENT_2_AMOUNT]` | Currency | "$3,750" |
| `[PAYMENT_3_AMOUNT]` | Currency | "$2,500" |
| `[PERCENTAGE_1]` | Integer | 50 |
| `[PERCENTAGE_2]` | Integer | 30 |
| `[PERCENTAGE_3]` | Integer | 20 |

---

## Technical Architecture Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[ARCHITECTURE_PATTERN]` | String | "Event-driven webhook-based with scheduled batch jobs" |
| `[RUNTIME]` | String | "Node.js" or "Python" |
| `[FRAMEWORK]` | String | "Express.js" or "FastAPI" |
| `[DATABASE]` | String | "PostgreSQL" or "MongoDB" |
| `[QUEUE_SYSTEM]` | String | "AWS SQS" or "Redis Queue" |
| `[HOSTING_PROVIDER]` | String | "AWS" or "Google Cloud" |
| `[MONITORING_TOOL]` | String | "DataDog" or "New Relic" |

---

## API & Integration Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[AUTH_METHOD]` | String | "OAuth 2.0" or "API Key" |
| `[REQUIRED_SCOPES]` | String | "read_orders, write_customers, read_products" |
| `[RATE_LIMIT]` | String | "40 requests/second" or "2 requests/second" |
| `[SYNC_FREQUENCY]` | String | "Real-time via webhooks" or "Hourly" |
| `[TARGET_LATENCY]` | String | "< 15 seconds" or "< 5 minutes" |
| `[WEBHOOK_URL]` | String | "https://integration.example.com/webhooks/shopify" |

---

## Data Mapping Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[DATA_TYPE_1]` | String | "Orders (Paid)" |
| `[SOURCE_1]` | String | "Shopify" |
| `[DEST_1]` | String | "QuickBooks" |
| `[FREQ_1]` | String | "Real-time (webhook)" |
| `[NOTES_1]` | String | "Creates invoice in QB" |
| `[FIELD_A1]` | String | "order_number" |
| `[FIELD_B1]` | String | "invoice_number" |
| `[TRANSFORMATION]` | String | "Prefix with 'SH-'" or "Direct mapping" |

---

## Team & Responsibility Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[LEAD_ENGINEER]` | String | "Alex Rodriguez" |
| `[PROJECT_MANAGER]` | String | "Jamie Sullivan" |
| `[PM_NAME]` | String | "Jamie Sullivan" |
| `[LEAD_NAME]` | String | "Alex Rodriguez" |
| `[DEV_NAME]` | String | "Morgan Chen" |
| `[QA_NAME]` | String | "Taylor Kim" |
| `[DEVOPS_NAME]` | String | "Jordan Lee" |
| `[CLIENT_POC]` | String | "Sarah Chen" |

---

## Risk & Error Handling Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[RISK_1]` | String | "API rate limit exceeded during high volume" |
| `[MITIGATION_1]` | String | "Implement exponential backoff and request queuing" |
| `[ERROR_HANDLING]` | String | "Exponential backoff with max 3 retries" |
| `[RETRY_STRATEGY]` | String | "3 attempts with exponential backoff (2s, 4s, 8s)" |
| `[DLQ_RETENTION_PERIOD]` | String | "7 days" |

---

## Monitoring & Performance Placeholders

| Placeholder | Type | Example |
|-------------|------|---------|
| `[TARGET_RATE]` | Percentage | "99.5" |
| `[TARGET_DURATION]` | String | "< 10 seconds" |
| `[TARGET_ERROR_RATE]` | Percentage | "0.5" |
| `[DASHBOARD_URL]` | URL | "https://monitoring.example.com/cozyhome-integration" |
| `[ALERT_DESTINATION]` | String | "ops-team@example.com, #alerts-slack" |

---

## Conditional Section Flags

These determine which conditional sections to include:

| Flag | Type | Trigger Condition | Sections Affected |
|------|------|------------------|-------------------|
| `{{#if accounting}}` | Boolean | integration_type == "accounting" | Tax handling, reconciliation, invoice flows |
| `{{#if marketing}}` | Boolean | integration_type == "marketing" | Customer sync, segmentation, privacy compliance |
| `{{#if fulfillment}}` | Boolean | integration_type == "fulfillment" | Order routing, shipping, tracking, returns |
| `{{#if inventory}}` | Boolean | integration_type == "inventory" | Multi-location, stock sync, reconciliation |
| `{{#if pos}}` | Boolean | integration_type == "pos" | Hardware, offline mode, end-of-day sync |
| `{{#if HAS_FUTURE_PHASES}}` | Boolean | future enhancements exist | Future enhancement opportunities |
| `{{#if HAS_DATA_MIGRATION}}` | Boolean | historical data needed | Data migration requirements |
| `{{#if BATCH_PROCESSING}}` | Boolean | batch sync required | Batch processing logic |
| `{{#if HIGH_VOLUME}}` | Boolean | volume > threshold | High-volume optimizations |
| `{{#if WEBHOOK_BASED}}` | Boolean | uses webhooks | Webhook reliability issues |
| `{{#if CONFIDENCE_SCORE < 70}}` | Boolean | confidence < 70 | Warning recommendation |

---

## Integration-Specific Placeholders

### Accounting Integrations

| Placeholder | Example |
|-------------|---------|
| `[ACCOUNTING_SYSTEM]` | "QuickBooks Online" |
| `[TAX_HANDLING_APPROACH]` | "Tax lines mapped by rate matching to QB tax codes" |
| `[PAYMENT_SYNC_DETAILS]` | "Payment method recorded on invoice" |
| `[REFUND_RULE]` | "Refunds create QB credit memos for manual review" |
| `[CURRENCY_RULE]` | "All transactions in USD, multi-currency out of scope" |

### Marketing Integrations

| Placeholder | Example |
|-------------|---------|
| `[MARKETING_PLATFORM]` | "Klaviyo" |
| `[SEGMENTATION_CRITERIA]` | "purchase history, lifetime value, engagement score" |
| `[EMAIL_TRIGGER_DESCRIPTION]` | "Welcome series for new customers, re-engagement for lapsed" |
| `[RETENTION_POLICY]` | "Customer data retained per GDPR (request deletion honored)" |

### Fulfillment Integrations

| Placeholder | Example |
|-------------|---------|
| `[FULFILLMENT_SYSTEM]` | "ShipStation" |
| `[LABEL_GENERATION_APPROACH]` | "Automatic label creation via ShipStation API" |
| `[RETURNS_HANDLING_APPROACH]` | "Return labels generated on-demand via customer portal" |
| `[CARRIER_FAILOVER_RULE]` | "If USPS unavailable, auto-switch to FedEx" |

### Inventory Integrations

| Placeholder | Example |
|-------------|---------|
| `[LOCATION_HANDLING_DETAILS]` | "3 locations supported: Warehouse, Store A, Store B" |
| `[SYNC_DIRECTION]` | "Bidirectional" or "QB → Shopify" |
| `[ALERT_MECHANISM]` | "Email alert when stock < 10 units" |
| `[RECONCILIATION_APPROACH]` | "Daily reconciliation report comparing both systems" |

### POS Integrations

| Placeholder | Example |
|-------------|---------|
| `[POS_SYNC_DETAILS]` | "End-of-day sales total and transaction count" |
| `[INVENTORY_COORDINATION_APPROACH]` | "Real-time sync prevents overselling" |
| `[HARDWARE_DETAILS]` | "Compatible with Square Reader, iPad POS" |
| `[OFFLINE_HANDLING]` | "Queue transactions locally, sync when connection restored" |

---

## Placeholder Population Priority

### Critical (Block document generation if missing)
1. `[PROJECT_NAME]`
2. `[CLIENT_NAME]`
3. `[SYSTEM_A]`
4. `[SYSTEM_B]`
5. `[INTEGRATION_TYPE]`

### High (Required for quality output)
6. `[CLIENT_CONTACT_NAME]`
7. `[CONFIDENCE_SCORE]`
8. `[OPEN_QUESTIONS]`
9. `[BUSINESS_OBJECTIVES]`
10. `[TOTAL_TIMELINE]`

### Medium (Improve usability)
11. `[TOTAL_COST]`
12. `[CURRENT_PAIN_POINTS]`
13. `[ARCHITECTURE_PATTERN]`
14. `[SYNC_FREQUENCY]`

### Low (Nice to have)
15. `[LEAD_ENGINEER]`
16. `[MONITORING_TOOL]`
17. `[DASHBOARD_URL]`

---

## Placeholder Data Types & Validation

| Type | Validation Rule | Example |
|------|----------------|---------|
| String | Non-empty | "CozyHome" |
| Date | Valid ISO or readable format | "2024-01-17" or "January 17, 2024" |
| Currency | Format: $X,XXX | "$12,500" |
| Percentage | 0-100 | "68" (not "68%") |
| Integer | Numeric | "250" |
| Enum | One of allowed values | "accounting" not "Accounting" |
| List | Newline or bullet separated | "- Item 1\n- Item 2" |
| Boolean | true/false for conditional | true (not "yes" or "1") |

---

## Template Population Algorithm (Suggested)

```python
def populate_template(template_path, discovery_data, analysis_results):
    """
    Populate a template with discovery data and analysis results.
    """
    # 1. Load template
    template_content = read_file(template_path)
    
    # 2. Determine integration type
    integration_type = determine_integration_type(discovery_data)
    
    # 3. Replace core placeholders
    content = replace_placeholders(template_content, {
        'PROJECT_NAME': discovery_data.project_name,
        'CLIENT_NAME': discovery_data.client_name,
        'SYSTEM_A': discovery_data.system_a,
        'SYSTEM_B': discovery_data.system_b,
        'CONFIDENCE_SCORE': analysis_results.confidence_score,
        # ... all other placeholders
    })
    
    # 4. Process conditional sections
    content = process_conditionals(content, {
        'accounting': integration_type == 'accounting',
        'marketing': integration_type == 'marketing',
        'fulfillment': integration_type == 'fulfillment',
        'inventory': integration_type == 'inventory',
        'pos': integration_type == 'pos',
        'CONFIDENCE_SCORE < 70': analysis_results.confidence_score < 70,
        # ... other conditionals
    })
    
    # 5. Populate discovery-generated content
    content = populate_discovery_content(content, {
        'OPEN_QUESTIONS': format_list(analysis_results.open_questions),
        'ASSUMPTIONS_TO_VALIDATE': format_list(analysis_results.assumptions),
        'CURRENT_PAIN_POINTS': format_list(discovery_data.pain_points),
        # ... other generated content
    })
    
    # 6. Validate no placeholders remain (optional)
    validate_no_placeholders(content)
    
    return content
```

---

## Testing Checklist

When implementing template population:

- [ ] All critical placeholders replaced
- [ ] Conditional sections processed correctly based on integration type
- [ ] Confidence score appears in correct format
- [ ] Open questions formatted as numbered list
- [ ] Dates in consistent format
- [ ] Currency values properly formatted
- [ ] No stray `[PLACEHOLDER]` text remains
- [ ] No unparsed `{{#if}}` blocks remain
- [ ] Cross-references point to correct document names
- [ ] Generated content readable and grammatically correct

---

## Example Placeholder Mapping (CozyHome)

```json
{
  "PROJECT_NAME": "CozyHome Shopify-QuickBooks Integration",
  "PROJECT_ID": "cozyhome-qb-integration",
  "CLIENT_NAME": "CozyHome LLC",
  "CLIENT_CONTACT_NAME": "Sarah Chen",
  "CLIENT_CONTACT_TITLE": "Owner",
  "DATE": "January 17, 2024",
  "INTEGRATION_TYPE": "accounting",
  "SYSTEM_A": "Shopify",
  "SYSTEM_B": "QuickBooks Online",
  "CONFIDENCE_SCORE": 68,
  "OPEN_QUESTIONS": [
    "How should refunds be handled?",
    "Which system is the inventory system of record?",
    "What is the precise definition of 'real-time' sync?",
    "How to handle orders with multiple tax jurisdictions?",
    "Should architecture account for future POS integration?",
    "Which QuickBooks Online edition is in use?"
  ],
  "CURRENT_PAIN_POINTS": [
    "3+ hours per day manual data entry",
    "Accounting errors and reconciliation issues",
    "Inventory overselling between systems"
  ],
  "BUSINESS_OBJECTIVES": [
    "Eliminate manual data entry",
    "Reduce accounting errors",
    "Improve inventory accuracy",
    "Enable real-time financial visibility"
  ],
  "TOTAL_COST": "$12,500",
  "MONTHLY_FEE": "$350"
}
```

---

## Tips for MCP Developers

1. **Start with required placeholders**: Ensure all critical placeholders are populated before attempting optional ones

2. **Use fallback values**: For optional placeholders, provide sensible defaults (e.g., "[TO BE DETERMINED]")

3. **Validate integration type early**: This drives conditional section logic

4. **Format lists consistently**: Use numbered lists for questions, bullet lists for features

5. **Generate dates intelligently**: Calculate milestone dates based on total timeline and phase durations

6. **Cross-reference validation**: Ensure PROJECT_ID is consistent across all three generated documents

7. **Preserve markdown formatting**: Don't break tables or code blocks when replacing placeholders

8. **Test with all integration types**: Validate that conditional sections work for accounting, marketing, fulfillment, inventory, and POS

9. **Handle missing data gracefully**: Leave placeholder or insert "[REQUIRES CLARIFICATION]" rather than crashing

10. **Keep human in loop**: Some placeholders are better filled by humans (team names, specific tool choices)

---

**Last Updated**: January 2024  
**For**: MCP Template Population Development  
**Related**: templates/README.md, templates/IMPLEMENTATION-SUMMARY.md

