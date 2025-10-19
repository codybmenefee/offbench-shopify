# Scenario 5: Bloom & Co. - Shopify + Local POS Integration

## Business Context
Bloom & Co. is a flower shop with both online (Shopify) and in-store (POS) sales. They struggle with inventory sync between systems and need unified daily sales visibility for accurate reporting.

## Integration Objective
Synchronize daily sales totals and shared product inventory between their POS system and Shopify to prevent overselling and generate combined end-of-day reports.

## Discovery Documents in This Scenario

### Field Notes with Vendor Correspondence
1. **client-docs/discovery-field-notes.txt** - Consultant's informal notes from site visit
2. **transcripts/three-way-call.txt** - Technical discussion between owner, manager, and POS vendor
3. **client-docs/eod-process.txt** - Step-by-step current closing procedure
4. **emails/pos-vendor-specs.txt** - Email from POS vendor about API capabilities

## Intentional Gaps for Testing
- Tax reconciliation not addressed
- Perishable inventory (flowers) handling not discussed
- Same-day online orders for in-store pickup not mentioned
- POS system API capabilities unclear/vague
- No mention of seasonal inventory patterns
- Multi-location future plans hinted but not detailed

## Expected Tool Outputs
- Gap detection: Missing tax handling, perishable inventory logic undefined, pickup order workflow missing
- Ambiguity surfacing: Which system is source of truth for inventory? How often should sync happen?
- Confidence score: Should be moderate-low (50-65%) due to retail complexity gaps
- Generated questions: 6-7 questions about inventory management, tax reconciliation, pickup orders, perishability

