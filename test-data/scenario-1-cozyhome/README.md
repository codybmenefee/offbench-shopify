# Scenario 1: CozyHome - Shopify + QuickBooks Integration

## Business Context
CozyHome is a small home décor retailer that sells online through Shopify. They currently use QuickBooks Online for accounting and are spending 3+ hours daily manually reconciling orders and inventory.

## Integration Objective
Automate the sync between Shopify and QuickBooks to eliminate manual data entry and reduce accounting errors.

## Discovery Documents in This Scenario

### Email-Heavy Discovery with SOW Draft
1. **emails/01-initial-inquiry.txt** - Initial outreach from store owner
2. **emails/02-accountant-thread.txt** - Follow-up discussion with accountant joining
3. **client-docs/draft-sow.txt** - Partially completed Statement of Work
4. **client-docs/product-catalog.txt** - Product SKU structure and categories

## Intentional Gaps for Testing
- No mention of refund/return handling
- Conflicting information on inventory system of record
- "Real-time sync" mentioned without defining frequency
- Tax handling not discussed
- No error handling or retry logic mentioned
- Budget/timeline vague

## Expected Tool Outputs
- Gap detection: Missing refund workflow, unclear sync frequency, undefined tax handling
- Ambiguity surfacing: Which system is source of truth for inventory?
- Confidence score: Should be moderate (60-70%) due to gaps
- Generated questions: 3-4 clarifying questions about edge cases

