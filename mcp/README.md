# Discovery Agent MCP Server

Autonomous agent tools for processing discovery documents and generating implementation deliverables.

## Overview

This MCP server provides 8 composable tools that work together to enable autonomous discovery-to-implementation workflows. An AI agent can chain these tools to:

1. Find and ingest discovery documents (emails, transcripts, SOWs)
2. Analyze for gaps, ambiguities, and conflicts
3. Calculate confidence scores
4. Generate implementation deliverables (SOW, implementation plans)
5. Extract clarifying questions
6. Accept answers and iteratively improve confidence

## Quick Start

### Installation

```bash
cd mcp
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the MCP Server

```bash
python src/main.py
```

The server will start on `http://localhost:8123`

### Test the Implementation

```bash
python test_tools.py
```

This validates all tools using the CozyHome test scenario.

## Available Tools

### 1. `find_project_folders()`

Scans the test-data directory for available project scenarios.

**Returns**: List of projects with metadata

**Example Agent Flow**:
```
Agent sees: "scenario-1-cozyhome", "scenario-2-brewcrew", etc.
```

### 2. `ingest_documents(project_id: str)`

Loads and parses all discovery documents from a project folder.

**Args**:
- `project_id`: e.g., "scenario-1-cozyhome"

**Returns**: Document count and summary

**What it does**:
- Recursively scans emails/, transcripts/, client-docs/
- Extracts metadata (dates, participants, subjects)
- Classifies document types
- Stores in ProjectState

### 3. `analyze_discovery(project_id: str)`

Analyzes documents for gaps, ambiguities, and conflicts. Calculates confidence score.

**Args**:
- `project_id`: Project identifier

**Returns**: Analysis results with confidence score (0-100%)

**Scoring Algorithm**:
- **Clarity** (40%): Fewer ambiguous terms = higher score
- **Completeness** (40%): Fewer gaps = higher score
- **Alignment** (20%): Fewer conflicts = higher score

**Gap Detection**:
- Missing refund/return handling
- Undefined tax logic
- No error handling defined
- Vague sync frequency
- Missing success criteria
- Undefined API rate limits
- Authentication not specified

**Ambiguity Detection**:
- "real-time" without specific timing
- "fast" without metrics
- "simple" without definition
- Other vague terms

**Conflict Detection**:
- Stakeholders disagree on system of record
- Contradicting requirements

### 4. `get_template(template_type: str)`

Loads a template from the templates directory.

**Args**:
- `template_type`: "sow", "implementation-plan", or "technical-specs"

**Returns**: Template content

### 5. `prepare_deliverable(project_id: str, template_type: str)`

Prepares all information needed to generate a deliverable document. Returns template, analysis data, and mapping guidance in one call.

**Args**:
- `project_id`: Project identifier
- `template_type`: "sow", "implementation-plan", or "technical-specs"

**Returns**: Complete package with:
- Template content with placeholders
- Project analysis data
- Integration type detection
- Mapping guide for filling placeholders
- Instructions for AI agent

**For AI Agents**:
- **ChatGPT/HTTP clients**: Use this to get everything needed, then generate the filled document
- **Cursor/Claude**: Can use this or call `get_template()` + `analyze_discovery()` separately

### 6. `extract_open_questions(project_id: str)`

Generates prioritized clarifying questions from analysis.

**Args**:
- `project_id`: Project identifier

**Returns**: List of 5-10 questions with priority and context

**Question Categories**:
- Business rules
- Technical constraints
- Edge cases
- Success criteria

### 7. `update_project_context(project_id: str, new_information: str)`

Adds new information or answers to project context.

**Args**:
- `project_id`: Project identifier
- `new_information`: Additional context or answers

**Returns**: Confirmation

**What it does**:
- Stores new context
- Marks related gaps as answered
- Prepares for re-analysis

### 8. `recalculate_confidence(project_id: str)`

Re-runs analysis with updated context and recalculates confidence score.

**Args**:
- `project_id`: Project identifier

**Returns**: New confidence score and improvement metrics

**Tracks**:
- Previous vs new confidence
- Delta improvement
- Remaining gaps/ambiguities/conflicts

## Example Agent Workflow

```
User: "Help me prepare the CozyHome implementation"

Agent autonomously:
1. find_project_folders()
   → Sees scenario-1-cozyhome available

2. ingest_documents("scenario-1-cozyhome")
   → Loads 4 documents (2 emails, 1 SOW draft, 1 product catalog)

3. analyze_discovery("scenario-1-cozyhome")
   → Confidence: 81%
   → Found 2 gaps, 4 ambiguities, 1 conflict

4. extract_open_questions("scenario-1-cozyhome")
   → Generates 6 prioritized questions

5. prepare_deliverable("scenario-1-cozyhome", "sow")
   → Gets template + analysis + mapping guide, generates SOW draft

Agent responds to user:
"I've analyzed CozyHome's discovery documents. Current confidence: 81%.
I've drafted an initial SOW, but there are 6 critical questions:
1. How should refunds and returns be handled?
2. Which system is the source of truth for inventory?
..."

User: "Inventory source of truth is QuickBooks. Refunds sync daily."

Agent autonomously:
7. update_project_context("scenario-1-cozyhome", "...")
   → Stores answers

8. recalculate_confidence("scenario-1-cozyhome")
   → Confidence: 81% → 85% (improved 4%)
   → 2 gaps resolved, 4 remain

9. prepare_deliverable("scenario-1-cozyhome", "sow")
   → Regenerates SOW with new context included

Agent: "Great! Confidence improved to 85%. Updated the SOW. 4 questions remain..."
```

## State Management

The server maintains in-memory state via `ProjectStateManager` singleton:

- **Projects**: Dictionary of `project_id → ProjectState`
- **Persistence**: Across tool calls within agent session
- **History**: Tracks confidence improvements over time

**ProjectState includes**:
- Documents loaded
- Analysis results
- Additional context from user
- Confidence history
- Generated deliverables

## Architecture

```
mcp/src/
├── main.py                  # MCP server entry point
├── models/                  # Data models
│   ├── document.py          # Document schema
│   ├── analysis.py          # Analysis results
│   └── project_state.py     # Project state
├── core/                    # Core logic
│   ├── state_manager.py     # State persistence
│   ├── analyzer.py          # Gap/ambiguity detection
│   └── template_filler.py   # Template population
└── tools/                   # MCP tools
    ├── discovery_tools.py   # Tools 1,2,6,7,8
    └── template_tools.py    # Tools 4,5
```

## Testing

The test suite validates:

1. ✓ Document parsing (emails, transcripts, docs)
2. ✓ Project ingestion (scanning folders, loading files)
3. ✓ Analysis (gap detection, confidence scoring)
4. ✓ Template filling (placeholder replacement)
5. ✓ Context updates (answer integration)
6. ✓ Confidence recalculation (improvement tracking)

**Test Results** (scenario-1-cozyhome):
- Documents loaded: 4
- Initial confidence: 81%
- Systems identified: Shopify, QuickBooks, PayPal
- Gaps detected: 2 (medium/low priority)
- Ambiguities: 4 (real-time, fast, quick)
- Conflicts: 1 (inventory system of record)
- Template fill rate: 89% (105/118 placeholders)

## Development

### Adding New Gap Patterns

Edit `core/analyzer.py`:

```python
gap_checks = [
    {
        "keywords": ["new_topic"],
        "category": GapCategory.BUSINESS_RULES,
        "description": "New gap description",
        "impact": "Why this matters",
        "question": "Clarifying question",
        "priority": Priority.HIGH
    }
]
```

### Adding New Document Types

Edit `tools/discovery_tools.py`:

```python
def _parse_new_type(file_path: Path) -> Document:
    # Custom parsing logic
    return Document(...)
```

### Customizing Templates

Edit templates in `/templates/`:
- `client-facing-sow.md`
- `internal-implementation-plan.md`
- `internal-technical-specs.md`

Use placeholders like `[CLIENT_NAME]`, `[SYSTEM_A]`, etc.

## Next Steps

- Add more test scenarios (BrewCrew, PetPawz, etc.)
- Enhance gap detection patterns
- Improve confidence scoring algorithm
- Add support for more document types (PDFs, Google Docs)
- Build visualization for confidence trends
- Add export functionality for generated deliverables

## License

Proprietary - Lazer Technologies

