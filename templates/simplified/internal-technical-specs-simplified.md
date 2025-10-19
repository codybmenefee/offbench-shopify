# TECHNICAL SPECIFICATIONS
## [PROJECT_NAME]

**Project ID**: [PROJECT_ID]  
**Integration**: [SYSTEM_A] ↔ [SYSTEM_B]  
**Type**: [INTEGRATION_TYPE]  
**Lead Engineer**: [LEAD_ENGINEER]  
**Version**: [VERSION]

---

## 1. ARCHITECTURE OVERVIEW

**Pattern**: [ARCHITECTURE_PATTERN]

```
[SYSTEM_A] → API Client → Transform → Queue → [SYSTEM_B] API → Status Update
```

**Tech Stack**:
- Runtime: [RUNTIME]
- Hosting: [HOSTING_PROVIDER]
- Database: [DATABASE]
- Monitoring: [MONITORING_TOOL]

---

## 2. DATA FLOWS

### Primary Flow: [FLOW_NAME_1]

```
Trigger: [TRIGGER_DESCRIPTION]
  ↓
1. Receive [SYSTEM_A] webhook/event
2. Validate data
3. Transform to [SYSTEM_B] format
4. Apply business rules
5. POST to [SYSTEM_B] API
6. Handle response and log
```

**Latency Target**: [LATENCY_ESTIMATE]  
**Retry Strategy**: [RETRY_STRATEGY]

{{#if accounting}}
### Accounting Flow: Order → Invoice
```
Shopify Order (Paid) → Validate → Map products → Calculate tax → Create QB Invoice → Link payment
```
{{/if}}

{{#if marketing}}
### Marketing Flow: Customer Sync
```
Shopify Customer → Check opt-in → Fetch history → Calculate metrics → Segment → Sync to [MARKETING_PLATFORM]
```
{{/if}}

### Error Flow
```
Error → Log → Retry (if retryable) → Dead letter queue → Alert → Manual review
```

---

## 3. API INTEGRATION

### [SYSTEM_A] API

**Authentication**: [AUTH_METHOD]  
**Rate Limit**: [RATE_LIMIT]  
**Scopes**: [REQUIRED_SCOPES]

**Key Endpoints**:
1. `[ENDPOINT_1]` - [PURPOSE_1]
2. `[ENDPOINT_2]` - [PURPOSE_2]

**Webhooks**:
- Event: [EVENT_1] → Action: [ACTION_1]
- Event: [EVENT_2] → Action: [ACTION_2]

---

### [SYSTEM_B] API

**Authentication**: [AUTH_METHOD]  
**Rate Limit**: [RATE_LIMIT]  
**Account ID**: [ACCOUNT_ID_HANDLING]

**Key Endpoints**:
1. `[ENDPOINT_1]` - [PURPOSE_1]
2. `[ENDPOINT_2]` - [PURPOSE_2]

---

## 4. DATA MAPPING

### System of Record

| Entity | System of Record | Sync Direction | Conflict Resolution |
|--------|------------------|----------------|---------------------|
| [ENTITY_1] | [SYSTEM_A/B] | [A→B/B→A] | [RESOLUTION_1] |
| [ENTITY_2] | [SYSTEM_A/B] | [A→B/B→A] | [RESOLUTION_2] |

### Field Mapping: [ENTITY_1]

| [SYSTEM_A] Field | [SYSTEM_B] Field | Transformation |
|------------------|------------------|----------------|
| [FIELD_A1] | [FIELD_B1] | [TRANSFORMATION_1] |
| [FIELD_A2] | [FIELD_B2] | [TRANSFORMATION_2] |
| [FIELD_A3] | [FIELD_B3] | [TRANSFORMATION_3] |

**Example**:
```python
def transform_entity(source_data):
    return {
        "[FIELD_B1]": source_data["[FIELD_A1]"],
        "[FIELD_B2]": transform_function(source_data["[FIELD_A2]"]),
    }
```

{{#if accounting}}
### Accounting Mappings
- Order Number → Invoice Number (prefix "SH-")
- Line Items → QB Line Items (array transformation)
- Tax Lines → QB Tax (map by rate)
{{/if}}

---

## 5. SYNC FREQUENCY & TRIGGERS

### Real-Time (Webhooks)

| Event | Trigger | Action | Latency Target |
|-------|---------|--------|----------------|
| [EVENT_1] | [TRIGGER_1] | [ACTION_1] | [LATENCY_1] |
| [EVENT_2] | [TRIGGER_2] | [ACTION_2] | [LATENCY_2] |

### Scheduled Jobs

| Job | Schedule | Purpose |
|-----|----------|---------|
| [JOB_1] | [CRON_1] | [PURPOSE_1] |
| [JOB_2] | [CRON_2] | [PURPOSE_2] |

---

## 6. ERROR HANDLING

### Error Categories

| Type | Retryable | Strategy | Alert |
|------|-----------|----------|-------|
| Network timeout | Yes | Exponential backoff | Low |
| Rate limit (429) | Yes | Wait + backoff | Medium |
| Validation error | No | Log + skip | High |
| System unavailable | Yes | Extended retry | Critical |

### Retry Configuration
```python
MAX_RETRIES = 3
BASE_DELAY = 2  # seconds
EXPONENTIAL_BASE = 2
```

**Dead Letter Queue**: [DLQ_STORAGE] - [DLQ_RETENTION]

---

## 7. SECURITY & PRIVACY

**Authentication**: API keys in [SECRET_MANAGER]  
**Encryption**: TLS 1.2+ in transit, [ENCRYPTION_AT_REST] at rest  
**Key Rotation**: [ROTATION_SCHEDULE]

**Personal Data**:
- [PII_TYPE_1]: [HANDLING_1]
- [PII_TYPE_2]: [HANDLING_2]

{{#if marketing}}
**Compliance**: GDPR, CAN-SPAM - honor opt-outs and deletion requests
{{/if}}

---

## 8. MONITORING & LOGGING

**Metrics Tracked**:
- Sync success rate
- Sync duration (p50, p95)
- Error rate by category
- API response times

**Log Structure** (JSON):
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "event": "sync_completed",
  "sync_id": "uuid",
  "entity_type": "order",
  "duration_ms": 1250
}
```

**Alerts**:
- Sync failure rate >5% → Email + Slack
- API response time >5s → Slack
- System unavailable → PagerDuty

**Health Check**: `/health` - checks API connectivity, database, queue status

---

## 9. EDGE CASES & BUSINESS RULES

### Edge Cases

**1. [EDGE_CASE_1_NAME]**  
**Scenario**: [EDGE_CASE_DESCRIPTION]  
**Handling**: [HANDLING_APPROACH]

**2. [EDGE_CASE_2_NAME]**  
**Scenario**: [EDGE_CASE_DESCRIPTION]  
**Handling**: [HANDLING_APPROACH]

{{#if accounting}}
### Accounting Rules
- **Refunds**: [REFUND_RULE]
- **Partial Payments**: [PARTIAL_PAYMENT_RULE]
- **Tax Conflicts**: [TAX_CONFLICT_RULE]
{{/if}}

{{#if inventory}}
### Inventory Rules
- **Negative Stock**: [NEGATIVE_STOCK_RULE]
- **Multi-Location**: [LOCATION_PRIORITY_RULE]
- **Buffer Stock**: [BUFFER_STOCK_RULE]
{{/if}}

---

## 10. PERFORMANCE TARGETS

| Metric | Target | Maximum |
|--------|--------|---------|
| Sync latency | [TARGET_LATENCY] | [MAX_LATENCY] |
| API response time | [TARGET_RESPONSE] | [MAX_RESPONSE] |
| Throughput | [TARGET_THROUGHPUT] | [MAX_THROUGHPUT] |

**Current Volume**: [CURRENT_VOLUME]  
**Growth Projection**: [GROWTH_PROJECTION]

---

## 11. API QUIRKS & WORKAROUNDS

### [SYSTEM_A] Quirks
- **[QUIRK_1]**: [WORKAROUND_1]
- **[QUIRK_2]**: [WORKAROUND_2]

### [SYSTEM_B] Quirks
- **[QUIRK_1]**: [WORKAROUND_1]

{{#if WEBHOOK_BASED}}
**Webhook Reliability**: [WEBHOOK_ISSUE] → Mitigation: [MITIGATION] + periodic polling backup
{{/if}}

---

## 12. OPEN TECHNICAL QUESTIONS

### Requiring Client Input
[OPEN_QUESTIONS_CLIENT]

### Requiring Research
[OPEN_QUESTIONS_RESEARCH]

### Assumptions to Validate
[TECHNICAL_ASSUMPTIONS]

---

## REFERENCE DOCUMENTATION

- **External APIs**: [SYSTEM_A] docs: [URL], [SYSTEM_B] docs: [URL]
- **Internal**: SOW: `[PROJECT_ID]-sow.md`, Plan: `[PROJECT_ID]-implementation-plan.md`
- **Code Repo**: [REPO_URL]

---

**Version**: [VERSION] | **Last Updated**: [LAST_UPDATED] | **Owner**: [LEAD_ENGINEER]

