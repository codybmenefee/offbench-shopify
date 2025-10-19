# STATEMENT OF WORK

**Project**: CozyHome Shopify-QuickBooks Integration  
**Client**: CozyHome LLC  
**Date**: January 17, 2024  
**Prepared by**: Lazer Technologies

---

## 1. PROJECT OVERVIEW

### Business Context
CozyHome LLC is a small home décor retailer selling online through Shopify with 250 SKUs and 150-200 orders/week. Currently facing: 3+ hours daily manual data entry, accounting errors, and inventory discrepancies between systems.

### Business Objectives
- Eliminate 3+ hours per day of manual order entry
- Reduce accounting errors and improve financial data accuracy
- Enable real-time financial visibility into online sales
- Improve inventory accuracy between Shopify and QuickBooks

### Success Metrics
- Zero manual data entry for standard orders
- >95% inventory accuracy between systems
- Orders sync within 15 minutes

---

## 2. TECHNICAL SCOPE

### Systems Integration
**Shopify** → **QuickBooks Online**

Automated integration that synchronizes order data from Shopify to QuickBooks Online and maintains inventory consistency. When customers place paid orders on Shopify, invoices are automatically created in QuickBooks with proper product mapping and tax calculation.

**Financial Data**: Orders sync to invoices, tax handling: Tax lines mapped by rate to QuickBooks tax codes

### What Will Sync

| Data Type | Source | Destination | Frequency |
|-----------|--------|-------------|-----------|
| Orders (Paid) | Shopify | QuickBooks | Real-time (webhook) |
| Customer Info | Shopify | QuickBooks | With order |
| Inventory Levels | QuickBooks | Shopify | Hourly |
| Daily Sales Summary | Shopify | QuickBooks | Daily at 11:59 PM |

---

## 3. DELIVERABLES

1. **Integration Application** - Automated sync between Shopify and QuickBooks Online
2. **Configuration** - Data mapping (250 SKUs), authentication, monitoring
3. **Documentation** - User guide and support procedures
4. **Training** - 60-minute onboarding session

---

## 4. TIMELINE & INVESTMENT

### Timeline
- **Discovery**: 1 week
- **Development**: 2 weeks
- **Testing**: 1 week
- **Launch**: Feb 18, 2024

**Total**: 6 weeks from contract signing

### Investment
**Project Cost**: $12,500  
**Monthly Support**: $350

**Payment Schedule**:
- 50% upon signing: $6,250
- 30% at development completion: $3,750
- 20% at launch: $2,500

---

## 5. KEY ASSUMPTIONS

- Client provides API credentials within 3 business days
- Both systems support API integration
- No historical data migration (future transactions only)
- Current product naming is consistent between systems
- All orders use standard Shopify checkout (no POS initially)

---

## 6. OUT OF SCOPE

- Historical data migration
- Custom reporting beyond specified
- Automated refund/return processing
- Integration with future retail location
- Draft orders or unpaid orders

---

## 7. ACCEPTANCE CRITERIA

Project complete when:
- ✓ All data types syncing as specified
- ✓ Paid Shopify orders create QuickBooks invoices within 15 minutes
- ✓ 250 SKUs mapped and syncing correctly
- ✓ 5 days of stable operation
- ✓ Team trained and documentation delivered

---

## 8. OPEN QUESTIONS & DISCOVERY STATUS

### Questions Requiring Clarification

1. **Refund Handling**: How should refunds issued in Shopify be handled in QuickBooks? Create credit memos automatically or require manual review?

2. **Inventory System of Record**: Sarah manages inventory in Shopify, but David (accountant) mentioned QuickBooks should be source of truth. Which system drives inventory quantities?

3. **Sync Frequency Definition**: What is acceptable latency for "real-time"? Is 15 minutes acceptable, or is immediate webhook-based sync required?

4. **Tax Edge Cases**: How to handle orders with multiple tax jurisdictions or tax exemptions?

5. **Future Architecture**: Should integration architecture account for planned physical retail location and future POS integration?

6. **QuickBooks Edition**: Need confirmation of exact QuickBooks Online subscription level to verify API capabilities.

### Assumptions to Validate

1. All orders will use standard Shopify checkout (no draft orders or POS initially) - **Confirm with Sarah**

2. Customer payment method from Shopify is sufficient for QuickBooks tracking - **Confirm with David**

3. Current product naming in both systems is consistent for mapping - **Review during discovery call**

4. No multi-currency orders (all USD currently and in future) - **Confirm current and future plans**

### Implementation Readiness
**Confidence Score**: 68%

⚠️ **Recommendation**: Additional discovery needed before proceeding. See questions above.

**Breakdown**:
- **Clarity**: 65% (ambiguous requirements around inventory and refunds)
- **Completeness**: 70% (core requirements clear, edge cases need definition)
- **Alignment**: 70% (stakeholder conflict on inventory system of record)

---

## 9. AGREEMENT

**Client**: ___________________________ Date: _______  
**Lazer Technologies**: ___________________________ Date: _______

---

**Version**: 1.1 (Draft - Post Initial Discovery)  
**Status**: DRAFT - Pending Discovery Call (Jan 18, 2pm)  
**Internal Reference**: `cozyhome-qb-implementation-plan.md`, `cozyhome-qb-technical-specs.md`

