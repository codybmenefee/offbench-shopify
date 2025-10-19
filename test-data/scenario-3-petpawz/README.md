# Scenario 3: PetPawz - Shopify + ShipStation Integration

## Business Context
PetPawz is a pet accessories startup that ships approximately 100 orders per day. They currently print shipping labels manually from ShipStation and are struggling to keep up with order volume.

## Integration Objective
Automate shipment creation and tracking synchronization between Shopify and ShipStation to eliminate manual label printing and improve customer experience.

## Discovery Documents in This Scenario

### Operational Notes and Informal Documentation
1. **client-docs/operations-notes.txt** - Bullet-point pain points from ops lead
2. **client-docs/customer-support-notes.txt** - CS manager's notes about shipping complaints
3. **client-docs/shipping-process.txt** - Internal wiki-style workflow documentation
4. **transcripts/slack-conversation.txt** - Chat export between ops and CS teams

## Intentional Gaps for Testing
- International shipping not mentioned
- Return process mentioned but not detailed
- Peak volume (holidays) not discussed
- Multiple carriers mentioned without prioritization
- No error handling for failed shipments
- Tracking notification timing unclear

## Expected Tool Outputs
- Gap detection: Missing international shipping requirements, return workflow undefined, peak capacity not addressed
- Ambiguity surfacing: Which carrier for which order types? What happens when ShipStation API fails?
- Confidence score: Should be moderate-low (55-65%) due to operational gaps
- Generated questions: 4-5 questions about edge cases and carrier routing logic

