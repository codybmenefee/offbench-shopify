# Developer Guide for Agentic Builders

This document provides essential context for AI agents and developers building the Discovery → Implementation Confidence Tool.

## Core Philosophy

Every implementation is more than "build this feature" — it's solving a business problem for the client.

**Key Beliefs:**

1. **Capture the Why**: If you can capture the why (purpose, outcomes), you increase the value of what and how.

2. **Feedback Loops Matter**: The sooner you detect ambiguity or mis-alignment, the lower the risk downstream.

3. **Engineering Discipline**: Even for discovery tools, clear architecture, defined interfaces (MCP), and good separation of concerns are critical.

4. **Over-Communicate Alignment**: Visibility into "what we know", "what we don't", and "what we're going to do next" builds trust and reduces surprises.

## What's Most Important to Us

When building this tool, always prioritize:

### 1. Clarity & Alignment
- Everyone (client, implementation team, dev) on the same page
- Clear definition of what's being built and why
- Explicit success criteria

### 2. Actionable Output
- Deliver usable deliverables: plans, next-step lists, ambiguity logs
- Not just insights — concrete actions
- Ready for immediate use by PMs and dev teams

### 3. Discovery as Foundation
- Weak discovery = project risk
- Systematic discovery strengthening reduces rework and mis-scope
- Better to find issues now than during implementation

### 4. Augmenting Humans
- NOT replacing discovery leads or PMs
- Amplify their capability
- Surface what they might miss
- Make their jobs smoother

### 5. Maintainability & Scalability
- Add new document types without rewrites
- Add new project templates easily
- Extend with new agents/workflows cleanly

## Key Concepts

### Discovery Artifacts
The raw inputs we work with:
- Email threads between stakeholders
- Call transcripts (sales, discovery, scoping)
- Statements of Work (SOWs)
- Branding guides and design systems
- Technical requirements documents
- Client-provided context documents

### Confidence Scoring
Quantitative measure of implementation readiness:
- **Clarity**: Are requirements unambiguous?
- **Completeness**: Is all necessary information present?
- **Alignment**: Do stakeholders agree on outcomes?
- Scores should be actionable — identify specific gaps to improve

### Gap Detection
What's missing or unclear:
- Missing success criteria
- Ambiguous requirements
- Conflicting stakeholder statements
- Undefined technical constraints
- Unclear scope boundaries

### Ambiguity Surfacing
Making implicit assumptions explicit:
- "The client mentioned 'fast' — what's the actual performance target?"
- "Three stakeholders have different priorities — which wins?"
- "Success metrics weren't defined — what should we track?"

### Continuous Feedback Loop
The iterative improvement cycle:
1. Ingest documents
2. Analyze for gaps/ambiguity
3. Generate plan with confidence score
4. Surface questions/issues to user
5. User provides more context
6. Re-analyze and update plan
7. Confidence score improves
8. Repeat until ready for implementation

## Development Principles

### Engineering Discipline
- **Use MCP interfaces properly**: Clean tool definitions, proper error handling
- **Separation of concerns**: Ingestion ≠ Analysis ≠ Generation ≠ Scoring
- **Testable components**: Each stage should be independently verifiable
- **Clear data models**: Define schemas for artifacts, analysis results, plans, scores

### Template-Driven Approach
- Pre-define project plan templates
- Templates should be configurable and extensible
- Match templates to project types (e-commerce launch, integration, custom app, etc.)
- Allow customization while maintaining structure

### Extensibility
Design for growth:
- New document types: Add parsers without touching core logic
- New project templates: Drop in without system rewrites
- New analysis agents: Compose capabilities modularly
- New output formats: Generate different deliverable types

### Conversational Interface
- Users should ask questions naturally
- System should explain its reasoning
- Make ambiguity discussions productive
- Guide users toward better discovery

## System Components

### 1. Ingestion Pipeline
**Purpose**: Get documents into the system  
**Inputs**: File paths, Drive folder IDs  
**Outputs**: Parsed document objects with metadata  
**Success**: Handle multiple formats, preserve context, extract key info

### 2. Analysis Engine
**Purpose**: Find gaps, inconsistencies, ambiguities  
**Inputs**: Parsed documents  
**Outputs**: Analysis report with flagged issues  
**Success**: Catch what humans miss, prioritize issues by impact

### 3. Plan Generator
**Purpose**: Create implementation deliverables  
**Inputs**: Analyzed documents + template selection  
**Outputs**: Structured implementation plan  
**Success**: Clear, actionable, aligned with discovery findings

### 4. Confidence Scorer
**Purpose**: Quantify readiness for implementation  
**Inputs**: Analysis results + plan  
**Outputs**: Score + improvement recommendations  
**Success**: Accurate assessment, actionable feedback

### 5. Conversational Interface (MCP)
**Purpose**: Enable human-agent collaboration  
**Inputs**: User queries, feedback, additional context  
**Outputs**: Answers, clarifications, updated plans  
**Success**: Natural interaction, productive ambiguity resolution

## Success Criteria

### For Each Component
- **Ingestion**: Parse 95%+ of documents without manual intervention
- **Analysis**: Identify gaps that would cause implementation issues
- **Generation**: Plans are usable by dev teams without major revisions
- **Scoring**: Confidence scores correlate with actual project success
- **Interface**: Users prefer this over manual discovery review

### For the System
- Reduces discovery-to-plan time by 50%+
- Catches critical gaps before implementation starts
- Improves team alignment (measured by stakeholder surveys)
- Plans generated require minimal manual editing
- Used consistently by Lazer implementation teams

## Implementation Notes

### Start Simple, Grow Thoughtfully
- Begin with basic document parsing (text files, PDFs)
- Add complexity as patterns emerge
- Don't over-engineer upfront

### Test with Real Data
- Use actual Lazer project documents
- Validate against known-good and known-problematic projects
- Learn from real discovery failures

### Measure What Matters
- Track confidence score accuracy
- Monitor gap detection hit rate
- Measure time saved vs manual process
- Collect user feedback continuously

### Keep Humans in the Loop
- This augments, doesn't replace
- Surface decisions to humans
- Explain reasoning transparently
- Make override/correction easy

## Questions to Ask Yourself While Building

1. **Will this help a PM sleep better at night?** If not, reconsider.
2. **Would I trust this output for my own project?** Quality bar check.
3. **Can I add a new document type in 30 minutes?** Extensibility check.
4. **Does this reduce ambiguity or just move it?** Value check.
5. **Would this catch the issue that killed the last project?** Relevance check.

## Remember

The goal isn't perfect discovery — it's systematically better discovery. Surface the right questions at the right time. Make implicit assumptions explicit. Help humans do what they do best: make informed decisions.

