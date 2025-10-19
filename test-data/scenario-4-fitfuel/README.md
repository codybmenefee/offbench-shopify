# Scenario 4: FitFuel - Shopify + Stocky Integration

## Business Context
FitFuel is a small fitness brand with two retail stores and an online store. They need unified inventory tracking across all three channels using Shopify and the Stocky inventory app. Currently suffering from frequent inventory mismatches.

## Integration Objective
Sync inventory across online store and two physical retail locations, generate low-stock alerts, and centralize purchase order management using Stocky.

## Discovery Documents in This Scenario

### Multi-Stakeholder Chat Logs with Technical Documentation
1. **transcripts/team-chat-export.txt** - 30+ message Slack/Teams thread about inventory issues
2. **client-docs/inventory-spreadsheet-notes.txt** - Documentation of current Excel-based tracking system
3. **client-docs/technical-requirements.txt** - IT person's list of API access, credentials, system constraints
4. **client-docs/meeting-minutes.txt** - Notes from internal FitFuel planning meeting

## Intentional Gaps for Testing
- Which location is source of truth? (conflicting answers from different stakeholders)
- Low-stock threshold not clearly defined
- Purchase order approval workflow unclear
- Seasonal inventory patterns not mentioned
- No discussion of transfer orders between locations
- Product variants (sizes, colors) handling vague

## Expected Tool Outputs
- Gap detection: Missing source of truth definition, undefined thresholds, unclear approval process
- Ambiguity surfacing: Conflicting stakeholder opinions on system of record, vague "real-time" requirements
- Confidence score: Should be low-moderate (50-60%) due to multi-location complexity
- Generated questions: 7-8 questions about multi-location logic, approval workflows, variant handling, seasonal planning

