# Test Data - Discovery Documents

This directory contains **realistic, imperfect mock discovery documents** for testing the Discovery → Implementation Confidence Tool.

## Purpose

These documents are designed to:
- **Test document ingestion** across multiple formats (emails, transcripts, spreadsheet notes, technical docs)
- **Validate gap detection** by including intentional ambiguities and missing information
- **Exercise confidence scoring** with varying levels of completeness (50-70% ready for implementation)
- **Demonstrate ambiguity surfacing** through conflicting stakeholder statements and vague requirements

## Scenarios Overview

### Scenario 1: CozyHome (Shopify + QuickBooks)
**Document Type Focus**: Email-heavy discovery with SOW draft  
**Complexity**: Low-Medium  
**Confidence Target**: 60-70%

**Documents**: 4 files
- 2 email threads
- 1 draft Statement of Work
- 1 product catalog document

**Key Gaps**:
- No refund/return handling defined
- Conflicting info on inventory system of record
- Sync frequency undefined ("real-time" mentioned but not specified)
- Tax handling not discussed

---

### Scenario 2: BrewCrew Coffee (Shopify + Klaviyo)
**Document Type Focus**: Call transcripts with brand documentation  
**Complexity**: Medium  
**Confidence Target**: 60-70%

**Documents**: 4 files
- 2 call transcripts (sales call + discovery session)
- 1 brand voice guide
- 1 email from founder

**Key Gaps**:
- Data privacy/GDPR compliance vaguely mentioned
- Segmentation criteria not clearly defined
- Reorder reminder timing not specified
- Guest checkout handling not discussed
- Historical data migration not addressed

---

### Scenario 3: PetPawz (Shopify + ShipStation)
**Document Type Focus**: Operational notes and informal documentation  
**Complexity**: Medium  
**Confidence Target**: 55-65%

**Documents**: 4 files
- 1 operations notes (bullet points)
- 1 customer support notes
- 1 shipping process document (wiki-style)
- 1 Slack conversation export

**Key Gaps**:
- International shipping not mentioned
- Return process mentioned but not detailed
- Peak volume (holidays) not discussed
- Multiple carriers mentioned without prioritization
- No error handling for failed shipments

---

### Scenario 4: FitFuel (Shopify + Stocky)
**Document Type Focus**: Multi-stakeholder chat logs with technical documentation  
**Complexity**: High  
**Confidence Target**: 50-60%

**Documents**: 4 files
- 1 team chat export (30+ messages)
- 1 inventory spreadsheet notes
- 1 technical requirements document
- 1 meeting minutes

**Key Gaps**:
- Which location is source of truth? (conflicting answers)
- Low-stock threshold not clearly defined
- Purchase order approval workflow unclear
- Seasonal inventory patterns not mentioned
- Transfer order logic undefined
- Product variant handling vague

---

### Scenario 5: Bloom & Co. (Shopify + POS)
**Document Type Focus**: Field notes with vendor correspondence  
**Complexity**: Medium-High  
**Confidence Target**: 50-65%

**Documents**: 4 files
- 1 discovery field notes (consultant's informal notes)
- 1 three-way call transcript
- 1 end-of-day process document
- 1 email from POS vendor (technical specs)

**Key Gaps**:
- Tax reconciliation not addressed
- Perishable inventory (flowers) handling not discussed
- Same-day pickup orders not mentioned
- POS API capabilities unclear/vague
- Multi-location future plans hinted but undefined

---

## Document Authenticity Features

All documents include realistic imperfections:

### Natural Language
- Conversational tone, contractions, informal speech
- People ramble, repeat themselves, use jargon inconsistently
- Typos and grammatical quirks (minimal but present)

### Ambiguous Requirements
- "Fast", "real-time", "easy to use", "scalable" without definitions
- "ASAP", "soon", "eventually" without specific dates
- Assumptions stated as facts

### Conflicting Information
- Different stakeholders say different things
- Owner wants X, accountant wants Y
- Technical constraints contradict business requirements

### Missing Critical Details
- No error handling discussed
- Performance requirements undefined
- Budget constraints vague
- Success metrics not specified

### Scope Creep Hints
- "While we're at it, could we also..."
- "It would be nice if..."
- Future plans mentioned without clear scoping

---

## Testing Strategy

### Document Ingestion Testing
Each scenario uses a **unique document mix** to test parsing capabilities:
- **Scenario 1**: Formal documents (emails, SOW, catalog)
- **Scenario 2**: Calls + brand docs (transcripts, brand guide)
- **Scenario 3**: Operational docs (notes, wiki, chat)
- **Scenario 4**: Technical docs (requirements, spreadsheet notes, meeting minutes)
- **Scenario 5**: Field notes (consultant notes, vendor email, process docs)

### Gap Detection Testing
Scenarios contain **2-3 major gaps** and **3-5 ambiguities** each:
- Missing success criteria
- Undefined system of record
- Conflicting stakeholder statements
- Unclear data ownership
- Undefined edge cases
- Vague performance requirements

### Confidence Scoring Testing
Documents provide **60-70% of needed information**:
- Enough to understand the project
- Not enough to implement without clarification
- Clear opportunities for improvement
- Measurable increase as gaps are filled

### Ambiguity Surfacing Testing
Each scenario includes **1-2 inconsistencies**:
- Stakeholder A says one thing, Stakeholder B contradicts it
- Requirements imply one approach, constraints require another
- Timing expectations don't align with resource availability

---

## Usage

### Running Tests
```bash
# Ingest all scenarios
python mcp/src/tools/ingest_documents.py --path test-data/

# Ingest specific scenario
python mcp/src/tools/ingest_documents.py --path test-data/scenario-1-cozyhome/

# Analyze and generate report
python mcp/src/tools/analyze_discovery.py --scenario scenario-1-cozyhome
```

### Expected Outputs

For each scenario, the tool should produce:

1. **Analysis Report**
   - Identified gaps with severity
   - Detected ambiguities with context
   - Conflicting statements highlighted
   - Missing information catalog

2. **Implementation Plan**
   - Structured project plan
   - Clear scope definition
   - Technical approach
   - Integration architecture

3. **Confidence Score**
   - Overall readiness score (0-100)
   - Breakdown by dimension (clarity, completeness, alignment)
   - Improvement recommendations
   - Priority questions to ask client

4. **Question List**
   - 3-7 clarifying questions per scenario
   - Prioritized by impact
   - Specific enough to be actionable
   - Tied to gaps in discovery

---

## Document Statistics

| Scenario | Files | Total Words | Completeness | Complexity |
|----------|-------|-------------|--------------|------------|
| CozyHome | 4 | ~3,500 | 65% | Low-Med |
| BrewCrew | 4 | ~5,200 | 65% | Medium |
| PetPawz | 4 | ~4,800 | 60% | Medium |
| FitFuel | 4 | ~6,500 | 55% | High |
| Bloom & Co. | 4 | ~5,800 | 55% | Med-High |
| **Total** | **20** | **~25,800** | **60%** | **Varied** |

---

## Maintenance

### Adding New Scenarios
When adding new test scenarios:
1. Create new directory: `scenario-X-clientname/`
2. Include README.md with scenario context
3. Organize into subdirectories: `emails/`, `transcripts/`, `client-docs/`
4. Ensure unique document mix (don't duplicate scenario patterns)
5. Include 2-3 major gaps and 3-5 ambiguities
6. Target 60-70% completeness
7. Update this README with new scenario details

### Updating Existing Scenarios
- Keep documents realistic and imperfect
- Don't "fix" ambiguities - they're intentional
- Add complexity carefully (don't over-engineer)
- Test changes against actual tool capabilities

---

## Success Criteria

These test documents are successful if they:

✓ **Enable tool testing** across all major features  
✓ **Feel authentic** (anyone reading believes they're real)  
✓ **Surface gaps** the tool is designed to catch  
✓ **Provide learning data** for improving the tool  
✓ **Scale to production** (patterns apply to real client docs)

---

## Questions?

For questions about test data or to report issues:
- Check `SCENARIOS.md` for scenario descriptions
- Review `AGENTS.md` for development principles
- See `README.md` (root) for project overview

---

Last Updated: January 2024  
Maintained by: Lazer Technologies Implementation Team

