# MCP Discovery Agent - Test Prompts

A comprehensive list of test prompts organized by complexity level to validate the Discovery Agent's functionality with local test data.

---

## Level 1: Basic Operations (Getting Started)

### Test 1.1: List Available Projects
```
List all available projects in the test data
```

**Expected Result**: Shows all 5 scenario projects with their names and metadata.

---

### Test 1.2: Quick Confidence Check
```
Run a quick confidence check on scenario-1-cozyhome
```

**Expected Result**: Returns confidence scores (clarity, completeness, alignment) around 60-70%.

---

### Test 1.3: View Project Details
```
Show me the details of the scenario-2-brewcrew project
```

**Expected Result**: Project metadata, document count, and status.

---

## Level 2: Document Analysis (Core Features)

### Test 2.1: Full Analysis - CozyHome
```
Analyze scenario-1-cozyhome in full mode. What gaps and ambiguities do you find?
```

**Expected Result**: 
- Gaps: refund handling, tax handling, error handling, sync frequency
- Ambiguities: "real-time" mentioned without definition
- Confidence: ~65%

---

### Test 2.2: Full Analysis - BrewCrew
```
Run a complete analysis on scenario-2-brewcrew. What are the main concerns?
```

**Expected Result**:
- Gaps: GDPR compliance, segmentation criteria, guest checkout handling
- Systems identified: Shopify, Klaviyo
- Confidence: ~65%

---

### Test 2.3: Gaps Only Mode
```
What gaps exist in scenario-3-petpawz? Show only the gaps.
```

**Expected Result**: List of gaps without full analysis details.

---

### Test 2.4: Questions Only Mode
```
Generate prioritized questions for scenario-4-fitfuel
```

**Expected Result**: 3-7 questions prioritized by impact, ready for client meeting.

---

## Level 3: Querying & Information Retrieval

### Test 3.1: Specific Information Query
```
What did the client say about refunds in scenario-1-cozyhome?
```

**Expected Result**: Relevant excerpts from documents mentioning refunds (may be limited).

---

### Test 3.2: System Identification
```
Which systems are mentioned in scenario-2-brewcrew?
```

**Expected Result**: Shopify, Klaviyo identified from documents.

---

### Test 3.3: Pain Points Extraction
```
What are the main pain points mentioned in scenario-3-petpawz?
```

**Expected Result**: Manual shipping process, tracking errors, customer complaints.

---

### Test 3.4: Stakeholder Identification
```
Who are the stakeholders involved in scenario-4-fitfuel?
```

**Expected Result**: Names extracted from emails/transcripts/chat logs.

---

## Level 4: Feedback Loop & Context Addition

### Test 4.1: Add General Context
```
For scenario-1-cozyhome, add this context: "Client uses QuickBooks Online, not Desktop version. They need real-time sync within 5 minutes of order placement."
```

**Expected Result**: Context added, auto-reanalysis triggered, confidence improves.

---

### Test 4.2: Answer Specific Gap
```
For scenario-1-cozyhome, answer the refund handling gap: "Refunds should create credit memos in QuickBooks. Partial refunds are supported. Credit memos should be dated same as refund date."
```

**Expected Result**: Gap marked as answered, confidence score improves.

---

### Test 4.3: Override Incorrect Finding
```
For scenario-2-brewcrew, override the system detection: "Klaviyo is not being used. Client switched to Mailchimp last month."
```

**Expected Result**: Override recorded, systems list updated.

---

### Test 4.4: Resolve Ambiguity
```
For scenario-1-cozyhome, resolve the "real-time" ambiguity: "Real-time means within 5 minutes via polling, not webhooks."
```

**Expected Result**: Ambiguity removed from list, clarity score improves.

---

## Level 5: Deliverable Generation

### Test 5.1: Generate Questions Document
```
Generate a questions document for scenario-1-cozyhome
```

**Expected Result**: Formatted markdown document with prioritized questions ready for client meeting.

---

### Test 5.2: Generate Analysis Report
```
Create an analysis report for scenario-2-brewcrew
```

**Expected Result**: Comprehensive report with confidence scores, gaps, systems, findings summary.

---

### Test 5.3: Generate SOW (Standard Template)
```
Generate a statement of work for scenario-1-cozyhome using the standard template
```

**Expected Result**: SOW template filled with analysis data, ready for customization.

---

### Test 5.4: Generate SOW (Simplified Template)
```
Generate a simplified statement of work for scenario-3-petpawz
```

**Expected Result**: Simplified SOW template with analysis data.

---

### Test 5.5: Generate Implementation Plan
```
Create an internal implementation plan for scenario-4-fitfuel
```

**Expected Result**: Structured implementation plan with phases, tasks, technical approach.

---

### Test 5.6: Generate Technical Specs
```
Generate technical specifications for scenario-5-bloom
```

**Expected Result**: Technical specs document with API details, data models, error handling.

---

### Test 5.7: Export Analysis Snapshot
```
Export a complete analysis snapshot for scenario-1-cozyhome in JSON format
```

**Expected Result**: Full JSON export of project state, analysis, documents metadata.

---

## Level 6: Comparison & Batch Operations

### Test 6.1: Compare Two Projects
```
Compare scenario-1-cozyhome with scenario-2-brewcrew. Which has better discovery documentation?
```

**Expected Result**: Side-by-side comparison with confidence scores, gaps, better project identified.

---

### Test 6.2: Batch Analysis (Quick Mode)
```
Run quick confidence checks on all 5 scenarios
```

**Expected Result**: Confidence scores for all projects in batch.

---

### Test 6.3: Identify Best/Worst Project
```
Which scenario has the highest confidence score? Which has the lowest?
```

**Expected Result**: Ranking of projects by confidence with explanations.

---

## Level 7: Complex Multi-Step Workflows

### Test 7.1: Full Discovery to Implementation Flow
```
For scenario-1-cozyhome:
1. Analyze the project
2. Identify the top 3 gaps
3. Add context to fill those gaps
4. Re-analyze to measure improvement
5. Generate a questions document for remaining issues
6. Generate a simplified SOW
```

**Expected Result**: Complete workflow with measurable confidence improvement.

---

### Test 7.2: Iterative Improvement Workflow
```
For scenario-2-brewcrew:
1. Get initial confidence score
2. Add context about GDPR compliance requirements
3. Answer the segmentation criteria gap
4. Resolve the "scalable" ambiguity
5. Check new confidence score
6. Generate implementation plan
```

**Expected Result**: Step-by-step improvement with confidence tracking.

---

### Test 7.3: Gap-Driven Question Generation
```
For scenario-4-fitfuel:
1. Find all HIGH priority gaps
2. For each gap, generate a specific question
3. Create a questions document prioritized by impact
4. Save to implementation folder
```

**Expected Result**: Targeted questions document focusing on critical gaps.

---

### Test 7.4: Multi-Project Analysis & Comparison
```
Analyze all e-commerce scenarios (1, 2, 3) and identify:
1. Common gaps across all projects
2. Which project is most ready for implementation
3. Common ambiguous terms used
4. Systems most frequently mentioned
```

**Expected Result**: Cross-project insights and patterns.

---

## Level 8: Edge Cases & Error Handling

### Test 8.1: Non-Existent Project
```
Analyze scenario-99-doesnotexist
```

**Expected Result**: Helpful error message with list of available projects.

---

### Test 8.2: Project with No Documents
```
Create a new project called test-empty and try to analyze it
```

**Expected Result**: Error indicating no documents found, instructions to add documents.

---

### Test 8.3: Invalid Analysis Mode
```
Analyze scenario-1-cozyhome in "super-detailed" mode
```

**Expected Result**: Error listing valid modes (full, quick, gaps_only, questions_only, etc.).

---

### Test 8.4: Typo in Project Name
```
Analyze senario-1-cozyhome (note the typo)
```

**Expected Result**: Error with suggestion for correct project name.

---

## Level 9: Advanced Scenarios

### Test 9.1: Confidence Threshold Check
```
For scenario-1-cozyhome, determine what additional information is needed to reach 85% confidence
```

**Expected Result**: Analysis of remaining gaps and specific improvements needed.

---

### Test 9.2: Pre-Implementation Checklist
```
Is scenario-2-brewcrew ready for implementation? Generate a go/no-go checklist.
```

**Expected Result**: Checklist with readiness criteria, blockers, confidence assessment.

---

### Test 9.3: Risk Assessment
```
What are the biggest risks if we start implementing scenario-4-fitfuel without more discovery?
```

**Expected Result**: Risk analysis based on gaps and ambiguities, prioritized by impact.

---

### Test 9.4: Scope Definition
```
Generate a clear scope statement for scenario-5-bloom based on the discovery documents
```

**Expected Result**: In-scope/out-of-scope lists, assumptions, constraints.

---

## Level 10: Real-World Scenarios

### Test 10.1: Client Meeting Preparation
```
I have a meeting with the CozyHome client tomorrow. Prepare:
1. Top 5 questions to ask
2. Current confidence level with justification
3. What we know vs. what we don't know summary
```

**Expected Result**: Meeting-ready package with clear questions and status.

---

### Test 10.2: Technical Lead Briefing
```
Brief a technical lead on scenario-3-petpawz. What do they need to know before scoping work?
```

**Expected Result**: Technical summary with systems, constraints, unknowns, and concerns.

---

### Test 10.3: Project Manager Handoff
```
Create a handoff document for scenario-4-fitfuel for a PM taking over the project
```

**Expected Result**: Comprehensive status, next steps, risks, and recommendations.

---

### Test 10.4: Stakeholder Alignment Check
```
For scenario-5-bloom, are there any conflicting requirements between stakeholders?
```

**Expected Result**: Conflict detection with sources and resolution recommendations.

---

## Test Success Criteria

For each test level, track:
- ✅ **Pass**: Feature works as expected
- ⚠️ **Partial**: Feature works but with issues
- ❌ **Fail**: Feature doesn't work or errors

### Passing Thresholds by Level:
- **Level 1-3**: 100% pass (basic functionality)
- **Level 4-6**: 90%+ pass (core features)
- **Level 7-8**: 80%+ pass (advanced features)
- **Level 9-10**: 70%+ pass (edge cases and complex scenarios)

---

## Notes for Testers

1. **Auto-Loading**: All tests should work without explicit `ingest()` calls (implemented in latest update)
2. **Project IDs**: Use exact folder names (e.g., `scenario-1-cozyhome`, not `cozyhome`)
3. **Confidence Targets**: Test data is designed for 50-70% confidence initially
4. **Feedback Loop**: Tests 4.x should show measurable confidence improvement
5. **Error Messages**: Tests 8.x should provide helpful guidance, not just fail

---

## Running Tests

### Via Python Test Script
```bash
python test_local_file_support.py
```

### Via MCP Client (Claude Desktop, etc.)
Use the prompts directly in conversation with the MCP server enabled.

### Via Direct Tool Calls
```python
from main import analyze, ingest, manage_project, update, generate

# Example
result = analyze(project_id="scenario-1-cozyhome", mode="full")
print(result)
```

---

## Test Data Reference

| Project ID | Business | Integration | Complexity | Target Confidence |
|------------|----------|-------------|------------|-------------------|
| scenario-1-cozyhome | Home Goods | Shopify + QB | Low-Med | 65% |
| scenario-2-brewcrew | Coffee | Shopify + Klaviyo | Medium | 65% |
| scenario-3-petpawz | Pet Supplies | Shopify + ShipStation | Medium | 60% |
| scenario-4-fitfuel | Supplements | Shopify + Stocky | High | 55% |
| scenario-5-bloom | Florist | Shopify + POS | Med-High | 55% |

---

## Extending the Test Suite

To add new tests:
1. Identify the feature/capability to test
2. Write a clear natural language prompt
3. Define expected result
4. Assign appropriate complexity level
5. Add to this document
6. Run and validate

---

Last Updated: January 2025  
Maintained by: Lazer Technologies Implementation Team

