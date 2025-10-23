# Agent Prompt: Scenario B - Ambiguity Clarification

## Prerequisites

**Enable Demo Mode**:
```bash
export DEMO_MODE=true
```

## Copy-Paste This Prompt to Your AI Agent (Cursor/ChatGPT)

```
Analyze the TechStyle Commerce project for ambiguous requirements and their clarifications using the OffBench MCP server.

IMPORTANT: Use ONLY the OffBench MCP tools for this task. Do NOT read files directly.

PROJECT: scenario-6-enterprise-full

TASK: Find ambiguous terms and check if they've been clarified in follow-up documents.

STEPS TO EXECUTE (use OffBench MCP tools):

1. Use the OffBench ingest tool:
   Function: ingest
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - source: "local"

2. Use the OffBench analyze tool:
   Function: analyze
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - mode: "full"

3. Use the OffBench query tool:
   Function: query
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - question: "What ambiguous terms like 'real-time', 'fast', and 'scalable' were found? Were they clarified with specific details?"

4. Use the OffBench sync_to_convex tool:
   Function: sync_to_convex
   Arguments:
   - project_id: "scenario-6-enterprise-full"
   - sync_type: "full"

REPORT REQUIREMENTS:
Create a detailed ambiguity report:

## Ambiguous Terms Analysis

For EACH of these terms found: real-time, fast, quick, scalable, flexible

### Term: [term name]
- **Found in context**: [quote the surrounding text]
- **Document**: [filename]
- **Clarification Status**: CLARIFIED ✅ or NEEDS CLARIFICATION ❌
- **Clarification Details** (if found):
  * Specific definition or measurement
  * Source document for clarification
  * Exact clarifying text

## Summary
- Total ambiguous terms found: X
- Terms with clarification: Y
- Terms needing clarification: Z

## Most Important Finding
[Describe the most impactful clarification found, or most critical missing clarification]

CRITICAL RULES:
1. Only report clarifications that EXPLICITLY exist in documents
2. Look for specific numbers, timelines, or measurements
3. If a term appears but no specific clarification exists, mark as "NEEDS CLARIFICATION"
4. Do not infer or guess what the clarification might be
```

## Expected Outcomes

The agent should find:
- ✅ "real-time" - CLARIFIED as "within 30 seconds"
- ⚠️ "fast" - May or may not find clarification (in performance email but not adjacent to term)
- ⚠️ "scalable" - May or may not find clarification
- ❌ "quick" - NO CLARIFICATION (expected)
- ❌ "flexible" - NO CLARIFICATION (expected)

## Manual Verification Steps

### 1. Check Agent Response
- [ ] Lists all ambiguous terms found
- [ ] Clearly marks which have clarifications
- [ ] Provides exact clarification text (not summary)
- [ ] Correctly identifies terms WITHOUT clarifications

### 2. Verify "real-time" Clarification
```bash
grep -i "30 seconds" test-data/scenario-6-enterprise-full/emails/02-performance-requirements.txt
```
Expected: Should find the clarification text

### 3. Check for False Positives (Hallucination Check)
Pick any clarification the agent reported and verify:
```bash
# Search for the exact text in all documents
grep -r "EXACT_TEXT_FROM_AGENT" test-data/scenario-6-enterprise-full/
```
- [ ] Text exists in source documents
- [ ] Not inferred or made up
- [ ] Context is appropriate

### 4. Check Convex Database
- Navigate to `ambiguities` table
- Find records for `scenario-6-enterprise-full`
- Verify:
  - [ ] "real-time" has `clarification` field populated
  - [ ] Clarification matches what agent reported
  - [ ] Terms without clarifications have `clarification = null`
  - [ ] Status is "clarified" for those with clarifications, "open" for others

### 5. Evaluation Criteria
- [ ] **PASS**: At least 1 clarification found correctly
- [ ] **PASS**: Agent correctly identifies which terms lack clarification
- [ ] **PASS**: No hallucinated clarifications
- [ ] **CONDITIONAL**: Agent finds <50% of clarifications (pattern matching limitation, not bug)
- [ ] **FAIL**: Any made-up clarifications

## Teardown After Testing
```bash
python test_resolution_workflow.py --scenario scenario-6-enterprise-full --wipe-only
```

## Notes for Human Evaluator

**Why some clarifications might be missed:**
- The clarification text may be several sentences away from the ambiguous term
- Current pattern matching has limited context window
- This is a known limitation, not a bug
- Important: Agent should NOT make up clarifications to fill gaps

