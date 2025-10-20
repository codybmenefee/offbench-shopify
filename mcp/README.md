# Discovery Agent MCP Server

Autonomous agent tools for processing discovery documents and generating implementation deliverables.

## Overview

This MCP server provides **6 general-purpose tools** with storage abstraction for seamless Google Drive integration. An AI agent can chain these tools to:

1. Manage projects and configurations
2. Ingest documents from any source (local, Drive, text input)
3. Analyze with multiple modes (full, quick, compare, etc.)
4. Update context and answer questions
5. Generate any deliverable type
6. Query project information conversationally

### Key Features

- **Storage Abstraction**: Ready for Google Drive, OneDrive, Notion via unified interface
- **Flexible Tools**: Each tool supports multiple modes/actions
- **Batch Operations**: Analyze or ingest multiple projects at once
- **Configuration Management**: Per-project settings for thresholds and patterns
- **Backward Compatible**: Old tool names still work (deprecated)

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

### 1. `manage_project()` - Project Management

Unified tool for all project operations.

**Actions**:
- `list`: Show all available projects
- `create`: Create new project with folder structure (discovery/, implementation/, working/)
- `get`: Retrieve project metadata and status
- `delete`: Remove project
- `configure`: Update project settings

**Examples**:
```python
# List all projects
manage_project(action="list")

# Create new project
manage_project(action="create", project_id="cozyhome", project_name="CozyHome Integration")

# Get project status
manage_project(action="get", project_id="cozyhome")

# Configure project
manage_project(action="configure", project_id="cozyhome", config={
    "confidence_threshold": 85.0,
    "auto_reanalyze": True
})
```

### 2. `ingest()` - Universal Document Ingestion

Flexible document ingestion from any source.

**Sources**:
- `local`: Local filesystem (current/legacy structure)
- `text`: Direct text input (for notes, context)
- `google_drive`: Google Drive folder (coming soon)
- `url`: Web URL (coming soon)

**Examples**:
```python
# Ingest from local folder
ingest(project_id="cozyhome", source="local", location="/path/to/docs")

# Add text note
ingest(project_id="cozyhome", source="text", location="Client confirmed refunds...", doc_type="note")

# Replace all documents
ingest(project_id="cozyhome", source="local", location="/new/path", append=False)
```

### 3. `analyze()` - Comprehensive Analysis Engine

Multi-mode analysis tool.

**Modes**:
- `full`: Complete analysis with all findings
- `quick`: Confidence score only
- `gaps_only`: Just gap detection
- `questions_only`: Prioritized clarifying questions
- `confidence_only`: Score without detailed findings
- `compare`: Compare this project to another

**Supports batch operations**: Pass list of project IDs

**Examples**:
```python
# Full analysis
analyze(project_id="cozyhome", mode="full")

# Quick confidence check
analyze(project_id="cozyhome", mode="quick")

# Just questions for meeting
analyze(project_id="cozyhome", mode="questions_only")

# Compare projects
analyze(project_id="cozyhome", mode="compare", compare_to="brewcrew")

# Batch analyze
analyze(project_id=["proj1", "proj2", "proj3"], mode="quick")
```

**Scoring Algorithm**:
- **Clarity** (40%): Fewer ambiguous terms = higher score
- **Completeness** (40%): Fewer gaps = higher score
- **Alignment** (20%): Fewer conflicts = higher score

### 4. `update()` - Context and Override Management

Add information, answer questions, override findings.

**Types**:
- `context`: Add general information
- `answer`: Answer specific gap/question by ID
- `override`: Correct wrong analysis finding
- `resolve`: Mark ambiguity/gap as resolved

**Features**:
- Saves updates to working/ folder for traceability
- Auto-reanalyzes if configured
- Returns new confidence score

**Examples**:
```python
# Add context
update(project_id="cozyhome", type="context", content="Client uses QB Online")

# Answer specific gap
update(project_id="cozyhome", type="answer", content="Refunds create credit memos", target_id="gap_refund")

# Override incorrect finding
update(project_id="cozyhome", type="override", content="Klaviyo not involved", target_id="system_klaviyo")
```

### 5. `generate()` - Deliverable Generation

Generate any deliverable type with multiple formats.

**Output Types**:
- `sow`: Client-facing Statement of Work
- `implementation_plan`: Internal implementation plan
- `tech_specs`: Technical specifications
- `questions_doc`: Formatted questions for meetings
- `report`: Analysis summary with trends
- `analysis_snapshot`: JSON export of full state

**Formats**: markdown, json, pdf, html

**Templates**: standard, simplified, custom

**Examples**:
```python
# Generate SOW
generate(project_id="cozyhome", output_type="sow", template="simplified")

# Generate questions doc
generate(project_id="cozyhome", output_type="questions_doc", format="pdf")

# Export analysis
generate(project_id="cozyhome", output_type="analysis_snapshot", format="json")
```

**Automatically saves** to implementation/ folder

### 6. `query()` - Conversational Project Exploration

Answer questions about project documents and analysis.

**Examples**:
```python
# Search documents
query(project_id="cozyhome", question="What did the client say about refunds?")

# Find mentions
query(project_id="cozyhome", question="Which documents mention QuickBooks?")

# Get insights
query(project_id="cozyhome", question="What are the main pain points?")
query(project_id="cozyhome", question="Who are the stakeholders?")
```

**Returns**: Relevant excerpts from documents + analysis insights

---

## Deprecated Tools (Still Work)

Old tool names are deprecated but still functional for backward compatibility:

- `find_project_folders()` → use `manage_project(action="list")`
- `ingest_documents(project_id)` → use `ingest(project_id, source="local")`
- `analyze_discovery(project_id)` → use `analyze(project_id, mode="full")`
- `extract_open_questions(project_id)` → use `analyze(project_id, mode="questions_only")`
- `update_project_context(project_id, info)` → use `update(project_id, type="context", content=info)`
- `recalculate_confidence(project_id)` → use `analyze(project_id, mode="quick")`
- `get_template(type)` → use `generate(project_id, output_type=type)`
- `prepare_deliverable(project_id, type)` → use `generate(project_id, output_type=type)`

## Example Agent Workflow (New Tools)

```
User: "Help me prepare the CozyHome implementation"

Agent autonomously:
1. manage_project(action="list")
   → Sees scenario-1-cozyhome available

2. ingest(project_id="scenario-1-cozyhome", source="local")
   → Loads 4 documents (2 emails, 1 SOW draft, 1 product catalog)

3. analyze(project_id="scenario-1-cozyhome", mode="full")
   → Confidence: 81%
   → Found 2 gaps, 4 ambiguities, 1 conflict
   → Returns prioritized questions

4. generate(project_id="scenario-1-cozyhome", output_type="sow", template="simplified")
   → Generates SOW draft, saves to implementation/

Agent responds to user:
"I've analyzed CozyHome's discovery documents. Current confidence: 81%.
I've drafted an initial SOW (saved to implementation folder). 
There are 6 critical questions:
1. How should refunds and returns be handled?
2. Which system is the source of truth for inventory?
..."

User: "Inventory source of truth is QuickBooks. Refunds sync daily."

Agent autonomously:
5. update(project_id="scenario-1-cozyhome", type="context", 
         content="Inventory source: QuickBooks. Refunds sync daily.")
   → Stores answers to working/ folder
   → Auto-reanalyzes: Confidence: 81% → 85% (improved 4%)

6. generate(project_id="scenario-1-cozyhome", output_type="sow", template="simplified")
   → Regenerates SOW with new context

Agent: "Great! Confidence improved to 85%. Updated the SOW. 4 questions remain..."
```

### New Features in Action

**Query for specific information**:
```
User: "What did the accountant say about invoice handling?"

Agent:
query(project_id="scenario-1-cozyhome", question="accountant invoice handling")
→ Returns relevant excerpts from email thread

Agent: "The accountant mentioned in email-02 that invoices should..."
```

**Compare projects**:
```
User: "How does CozyHome compare to BrewCrew?"

Agent:
analyze(project_id="scenario-1-cozyhome", mode="compare", compare_to="scenario-2-brewcrew")

Agent: "CozyHome has 85% confidence vs BrewCrew's 72%. 
       CozyHome is better defined but both have gaps in error handling..."
```

**Batch operations**:
```
User: "Give me a quick status on all projects"

Agent:
analyze(project_id=["scenario-1-cozyhome", "scenario-2-brewcrew", "scenario-3-petpawz"], mode="quick")

Agent: "Project statuses:
       - CozyHome: 85% confidence
       - BrewCrew: 72% confidence  
       - PetPawz: 68% confidence"
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

