# Discovery → Implementation Confidence Tool

**For Lazer Technologies (Shopify Systems-Integrator)**

## Purpose

Empower Lazer's projects by automating and elevating the discovery-to-plan workflow. We capture, process, and convert unstructured discovery artifacts (emails, call transcripts, SOWs, branding guides, etc.) into structured implementation deliverables — and then continuously drive clarity, alignment, and confidence across sales, implementation, and dev teams.

## Core Value Proposition

Transform weak, scattered discovery into systematic, high-confidence implementation plans. Reduce project risk, rework, and mis-scope by strengthening the foundation before a single line of code is written.

## Key Features

### 1. **Document Ingestion & Parsing**
- Configurable sources: Google Drive folders or local directories
- Support for multiple document types (emails, transcripts, SOWs, brand guides, etc.)
- Automated extraction of key information

### 2. **Analysis Engine**
- Reviews documents for gaps, inconsistencies, and ambiguities
- Detects missing critical information
- Identifies alignment issues between stakeholders

### 3. **Plan Generation**
- Uses pre-defined templates tailored to project scope
- Incorporates success criteria and user context
- Produces actionable implementation deliverables

### 4. **Confidence Scoring**
- Quantifies project readiness for implementation
- Based on clarity, completeness, and alignment metrics
- Tracks improvement over time

### 5. **Agentic Interaction**
- Conversational interface via MCP + ChatGPT App SDK
- Ask questions, review drafts, surface ambiguity
- Prepare for client and practice meetings

### 6. **Continuous Feedback Loop**
- Identifies missing information
- Prompts further discovery activities
- Updates plans and improves confidence scores iteratively

### 7. **Admin Portal Integration (Convex)**
- Persistent storage for project observability
- Real-time dashboard for tracking all projects
- View gaps, questions, conflicts across teams
- Timeline of project activities and changes
- Seamless data sync from MCP to admin portal

## What's Most Important

### 1. Clarity & Alignment
Everyone (client, implementation team, dev) must be on the same page about what's being built, why it's being built, and how success will be measured.

### 2. Actionable Output
The tool must deliver usable deliverables (plans, next-step lists, ambiguity logs) — not just insights.

### 3. Discovery as Foundation
Weak discovery leads to project risk. By strengthening discovery and making it systematic, we reduce rework, mis-scope, and mismatch.

### 4. Augmenting Humans
This is not about replacing discovery leads or PMs — it's about amplifying their capability, surfacing things they might miss, making their job smoother.

### 5. Maintainability & Scalability
Architect the system so we can add new document types, new project templates, new agents/workflows without large rewrites.

## Architecture Overview

```
Discovery Artifacts → Ingestion → Analysis → Plan Generation → Confidence Scoring
                                      ↓
                              Agentic Interface (MCP)
                                      ↓
                              Feedback & Iteration
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Access to discovery document sources (Google Drive or local files)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd offbench-shopify
   ```

2. **Set up Python environment:**
   ```bash
   cd mcp
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Start the MCP server:**
   ```bash
   python src/main.py
   ```

4. **Connect to ChatGPT:**
   - Open ChatGPT
   - Go to Settings → Apps → Add App
   - Enter your server URL (use ngrok for local development)
   - Start your discovery analysis!

## Project Structure

```
offbench-shopify/
├── README.md                 # Project overview (this file)
├── AGENTS.md                # Developer context and principles
├── templates/               # Implementation document templates
│   ├── README.md            # Template usage guide
│   ├── client-facing-sow.md           # Statement of Work template
│   ├── internal-implementation-plan.md # Implementation plan template
│   ├── internal-technical-specs.md    # Technical specifications template
│   └── examples/            # Populated template examples
├── test-data/               # Discovery document test scenarios
└── mcp/                     # MCP server implementation
    ├── src/
    │   ├── main.py          # Main server entry point
    │   └── tools/           # Tool implementations
    └── requirements.txt     # Python dependencies
```

## Development Status

✅ **Latest Update** - Resolution & Clarification Support + Demo Mode Evaluation Framework
- ✅ Document ingestion pipeline
- ✅ Analysis engine for gap detection
- ✅ Confidence scoring algorithm
- ✅ Template-based plan generation
- ✅ Convex integration for admin portal observability
- ✅ **Resolution & clarification field support**
- ✅ **Demo mode for testing**
- ✅ **Comprehensive evaluation framework**

## Convex Integration (Admin Portal)

The MCP now includes Convex integration to enable a separate admin portal for project observability.

### Quick Start

1. **Set up Convex** (see `mcp/convex/README.md` for detailed guide):
   ```bash
   cd mcp/convex
   npm install
   convex dev
   ```

2. **Configure environment**:
   ```bash
   cd mcp
   cp .env.example .env
   # Edit .env with your Convex credentials
   ```

3. **Use the sync tool**:
   ```python
   # After running analysis
   analyze(project_id="cozyhome", mode="full")
   sync_to_convex(project_id="cozyhome", sync_type="full")
   ```

The admin portal (separate repo) reads from Convex to display:
- All projects with confidence scores
- Gaps, conflicts, and ambiguities
- Open questions across projects
- Document metadata with links
- Activity timeline

See `mcp/convex/README.md` for complete setup instructions.

## Evaluation & Testing

### Resolution & Clarification Testing
New features added to support resolution of conflicts and clarification of ambiguities, with comprehensive evaluation framework:

**Quick Start**: [`docs/evaluation/START-HERE-EVAL.md`](docs/evaluation/START-HERE-EVAL.md)  
**Demo Mode**: [`docs/demo-mode/DEMO-MODE-QUICK-START.md`](docs/demo-mode/DEMO-MODE-QUICK-START.md)  
**Complete Docs**: [`docs/README.md`](docs/README.md)

### Quick Test
```bash
# Enable demo mode
export DEMO_MODE=true

# Run automated test
python test_resolution_workflow.py --run-full --demo

# Or use AI agent prompts
open agent-prompts/SCENARIO-A-BASIC-CONFLICT.md
```

See [`docs/`](docs/) for complete documentation organized by purpose.

## For Developers

See `AGENTS.md` for detailed development principles, core concepts, and system component guidance.

See [`docs/implementation/`](docs/implementation/) for technical implementation details and deliverables manifest.

## License

Proprietary - Lazer Technologies