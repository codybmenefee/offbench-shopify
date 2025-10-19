# Test Prompts for Discovery Agent MCP

This document contains comprehensive test prompts for validating the Discovery → Implementation Confidence Tool against the 5 test scenarios.

---

## 🎯 Overview

Use these prompts to test the MCP tools through conversational AI agents (Cursor, Claude Desktop, ChatGPT). Prompts are organized by complexity level, from basic single-tool tests to complex end-to-end workflows.

---

## Level 1: Basic Tool Testing (Individual Functions)

These test single tool calls and basic functionality:

### 1. Find Available Projects
```
What projects are available?
```
**Tests**: `find_project_folders()`

### 2. Load Documents
```
Load all documents for scenario-1-cozyhome
```
**Tests**: `ingest_documents()`

### 3. Analyze Project
```
Analyze the CozyHome project
```
**Tests**: `analyze_discovery()`

### 4. Extract Questions
```
What questions should we ask about CozyHome?
```
**Tests**: `extract_open_questions()`

### 5. Get Template
```
Show me the SOW template
```
**Tests**: `get_template()`

---

## Level 2: Intermediate Workflows (Multi-Step Analysis)

These test tool chaining and analysis depth:

### 6. Full Analysis with Readiness Check
```
Analyze CozyHome and tell me if we're ready to start development
```
**Tests**: Ingestion → Analysis → Question extraction → Interpretation

### 7. Cross-Project Comparison
```
Compare the confidence scores across all 5 scenarios
```
**Tests**: Multiple ingestions → Multiple analyses → Comparison logic

### 8. Pattern Detection
```
What are the common gaps across CozyHome, BrewCrew, and PetPawz?
```
**Tests**: Pattern detection across multiple projects

### 9. Quality Assessment
```
Which project has the clearest requirements?
```
**Tests**: Analysis comparison and confidence interpretation

### 10. Conflict Detection
```
Find all conflicts in the Bloom & Co. discovery documents
```
**Tests**: Conflict detection in analysis

---

## Level 3: Iterative Improvement (Feedback Loop)

These test the continuous feedback and improvement cycle:

### 11. CozyHome Context Update
```
For CozyHome: QuickBooks is the source of truth for inventory, sync should happen every 15 minutes, and refunds sync as credit memos within 24 hours
```
**Tests**: `update_project_context()` → `recalculate_confidence()`

### 12. BrewCrew Compliance Addition
```
Add this information to BrewCrew: We need GDPR compliance, customers must opt-in to marketing, and reorder reminders should go out 3 weeks after purchase
```
**Tests**: Context addition → Re-analysis → Confidence improvement

### 13. PetPawz Preorder Handling
```
For PetPawz: Handle preorders by marking them with a special tag in ShipStation and only create shipments when inventory arrives
```
**Tests**: Complex context addition → Gap resolution

### 14. Bloom Technical Specifications
```
Update Bloom's project: The POS system has a REST API with rate limits of 60 requests/minute, and inventory should sync every 5 minutes during business hours only
```
**Tests**: Technical specification addition → Confidence impact

### 15. Target Confidence Achievement
```
Keep adding context to FitFuel until confidence reaches 90%
```
**Tests**: Iterative improvement to target score

---

## Level 4: Deliverable Generation (Template-Based Output)

These test the ability to generate implementation documents.

**For ChatGPT**: Use `prepare_deliverable(project_id, template_type)` to get template + analysis + mapping guide in one call, then generate the filled document for the user to copy.

**For Cursor/Claude Desktop**: Can use either `prepare_deliverable()` or call `get_template()` + `analyze_discovery()` separately.

### 16. Single SOW Generation
```
Generate a Statement of Work for CozyHome
```
**Tests**: SOW generation from analysis  
**Expected**: AI calls `prepare_deliverable("scenario-1-cozyhome", "sow")` then outputs filled SOW

### 17. Complete Package Generation
```
Create a complete implementation package for BrewCrew (SOW, implementation plan, and technical specs)
```
**Tests**: Multiple template generation  
**Expected**: AI calls `prepare_deliverable()` three times (once for each template type), generates all three documents

### 18. Targeted Technical Specs
```
Generate technical specifications for PetPawz focusing on the ShipStation API integration
```
**Tests**: Targeted technical document generation  
**Expected**: AI calls `prepare_deliverable("scenario-3-petpawz", "technical-specs")`, focuses output on ShipStation integration

### 19. Batch Generation with Quality Check
```
Draft an SOW for all 5 scenarios and tell me which ones are complete enough to send to clients
```
**Tests**: Batch generation → Quality assessment  
**Expected**: AI calls `prepare_deliverable()` for each scenario, generates SOWs, assesses based on confidence scores

### 20. Plan with Gap Highlighting
```
Create an implementation plan for Bloom & Co. and highlight what information is still missing
```
**Tests**: Plan generation → Gap identification in output  
**Expected**: AI generates plan with explicit callouts for gaps from analysis

---

## Level 5: Advanced Reasoning (Complex Scenarios)

These test sophisticated analysis and decision-making:

### 21. Conflict Resolution
```
CozyHome's accountant says QuickBooks should be the source of truth, but the store owner wants Shopify to manage inventory. How should we resolve this conflict?
```
**Tests**: Conflict detection → Recommendation generation

### 22. Ambiguity with Constraints
```
BrewCrew wants 'real-time' syncing but mentioned budget constraints. What questions should I ask?
```
**Tests**: Ambiguity detection → Context-aware questioning

### 23. Technical Feasibility Analysis
```
PetPawz ships 100 orders per day. Will ShipStation's API rate limits be an issue? What should we recommend?
```
**Tests**: Technical feasibility analysis → Proactive risk detection

### 24. Strategic Planning
```
Bloom & Co. mentioned future multi-location plans. Should we design for that now or later? What are the tradeoffs?
```
**Tests**: Strategic planning → Scope boundary recommendations

### 25. Risk Assessment
```
Which scenario has the highest technical risk and why?
```
**Tests**: Cross-project risk assessment → Technical analysis

---

## Level 6: Edge Cases & Stress Tests

These test robustness and error handling:

### 26. Non-Existent Project
```
Analyze scenario-99-doesnotexist
```
**Tests**: Error handling for missing projects

### 27. Missing Dependency
```
Generate an SOW for CozyHome without analyzing it first
```
**Tests**: Handling missing dependencies

### 28. Conflicting Information
```
Add conflicting information: Shopify AND QuickBooks should both be the source of truth for inventory
```
**Tests**: Conflict detection in updates

### 29. Invalid State
```
Recalculate confidence for a project that hasn't been ingested yet
```
**Tests**: State validation and error messages

### 30. State Management Chaos
```
Load all documents from BrewCrew, then analyze PetPawz, then try to extract questions for CozyHome
```
**Tests**: State management across multiple projects

---

## Level 7: End-to-End Workflows (Real-World Usage)

These simulate actual PM/developer workflows:

### 31. Pre-Discovery Preparation
```
I just got off a call with a new client who wants to integrate Shopify with QuickBooks. Walk me through using CozyHome as a reference to prepare for our discovery meeting.
```
**Tests**: Full discovery workflow → Actionable outputs

### 32. Client Meeting Prep
```
We're presenting to the BrewCrew client tomorrow. Generate everything I need: analysis summary, SOW, and a list of questions to ask in the meeting.
```
**Tests**: Complete deliverable package for client meeting  
**Expected**: AI calls `analyze_discovery()` for summary, `extract_open_questions()` for questions, and `prepare_deliverable(..., "sow")` to generate SOW

### 33. Email Processing Workflow
```
The PetPawz client just sent me additional context via email: [paste mock email]. Update the project and tell me if we're ready to start development.
```
**Tests**: Email processing → Context update → Readiness assessment

### 34. New Project Onboarding
```
Start a new discovery for FitFuel from scratch. What's the first thing I should do?
```
**Tests**: Onboarding workflow guidance

### 35. Rejection Analysis
```
The Bloom & Co. client rejected our SOW saying it's missing key details. Re-analyze and tell me what we missed.
```
**Tests**: Gap detection in generated deliverables → Root cause analysis

---

## Level 8: Meta-Analysis (System Insights)

These test higher-level pattern recognition:

### 36. Gap Pattern Analysis
```
What are the most common types of gaps across all 5 scenarios?
```
**Tests**: Pattern detection across projects

### 37. Category-Based Ambiguity
```
Which integration type (accounting, marketing, fulfillment) tends to have the most ambiguity?
```
**Tests**: Category-based analysis

### 38. Quality Comparison
```
Show me examples of good vs. bad discovery documents from our test scenarios
```
**Tests**: Quality assessment and learning

### 39. Proactive Discovery Guidance
```
If I'm about to start discovery for a new Shopify + ERP integration, what questions should I ask upfront based on patterns from our scenarios?
```
**Tests**: Proactive guidance from learned patterns

### 40. Complexity Ranking
```
Rank all 5 scenarios by implementation difficulty and explain your reasoning
```
**Tests**: Complexity assessment across projects

---

## 📋 Quick Test Suites

### Suite A: Smoke Test (5 minutes)
Quick validation that basic functionality works:
- **Prompt 1**: What projects are available?
- **Prompt 2**: Load all documents for scenario-1-cozyhome
- **Prompt 3**: Analyze the CozyHome project
- **Prompt 4**: What questions should we ask about CozyHome?
- **Prompt 11**: For CozyHome: QuickBooks is the source of truth...

### Suite B: Full Workflow Test (15 minutes)
Comprehensive workflow testing:
- **Prompt 6**: Analyze CozyHome and tell me if we're ready...
- **Prompt 11**: For CozyHome: QuickBooks is the source of truth...
- **Prompt 12**: Add this information to BrewCrew...
- **Prompt 16**: Generate a Statement of Work for CozyHome
- **Prompt 32**: We're presenting to the BrewCrew client tomorrow...

### Suite C: Edge Case Validation (10 minutes)
Robustness and error handling:
- **Prompt 26**: Analyze scenario-99-doesnotexist
- **Prompt 27**: Generate an SOW for CozyHome without analyzing...
- **Prompt 28**: Add conflicting information...
- **Prompt 29**: Recalculate confidence for a project that hasn't...
- **Prompt 30**: Load all documents from BrewCrew, then analyze...

### Suite D: Real-World Simulation (20 minutes)
Simulate actual usage patterns:
- **Prompt 31**: I just got off a call with a new client...
- **Prompt 32**: We're presenting to the BrewCrew client tomorrow...
- **Prompt 33**: The PetPawz client just sent me additional context...
- **Prompt 35**: The Bloom & Co. client rejected our SOW...
- **Prompt 40**: Rank all 5 scenarios by implementation difficulty...

---

## 🎨 Scenario-Specific Prompts

### CozyHome (Accounting Integration)

**Conflict Analysis:**
```
What's the main conflict in CozyHome's discovery?
```

**Technical Decision:**
```
Should refunds be real-time or batch processed for CozyHome?
```

**Data Mapping:**
```
Generate a data mapping table for CozyHome's Shopify-QuickBooks integration
```

---

### BrewCrew (Marketing Automation)

**Compliance Check:**
```
What GDPR concerns should we address for BrewCrew?
```

**Segmentation Strategy:**
```
How should we segment BrewCrew's customers?
```

**Timing Recommendation:**
```
What's the recommended reorder reminder timing for BrewCrew?
```

---

### PetPawz (Fulfillment)

**Return Workflow:**
```
How do we handle PetPawz's return/exchange workflow?
```

**Rate Limit Analysis:**
```
What are the API rate limit risks for PetPawz?
```

**Integration Pattern:**
```
Should PetPawz use webhooks or polling for order updates?
```

---

### FitFuel (Inventory Management)

**Source of Truth:**
```
Which location should be the source of truth for FitFuel?
```

**Alert System:**
```
How should low-stock alerts work for FitFuel's multi-location setup?
```

**Gap Detection:**
```
What's missing from FitFuel's inventory sync requirements?
```

---

### Bloom & Co. (POS Integration)

**Perishable Inventory:**
```
How should Bloom handle perishable inventory (flowers)?
```

**End-of-Day Process:**
```
What's the end-of-day reconciliation process for Bloom?
```

**System of Record:**
```
Should Bloom's POS or Shopify be the source of truth?
```

---

## 💡 Tips for Effective Testing

### 1. Start Simple
Begin with Level 1-2 prompts to verify basic functionality before moving to complex scenarios.

### 2. Test Iteratively
Use Level 3 prompts to verify the feedback loop works correctly and confidence scores improve appropriately.

### 3. Mix Scenarios
Don't just test one scenario—switch between projects to validate state management.

### 4. Be Specific
When adding context (Level 3), use concrete details rather than vague statements.

### 5. Check State
Test state management by jumping between projects mid-workflow.

### 6. Look for Patterns
Use Level 8 prompts to test cross-project analysis and pattern recognition.

### 7. Verify Error Handling
Level 6 prompts are critical—make sure errors are graceful and informative.

### 8. Simulate Real Usage
Level 7 prompts represent actual PM workflows—these are the most important for UX validation.

---

## 📊 Expected Outcomes

### Confidence Score Ranges (Initial Analysis)

| Scenario | Expected Range | Reason |
|----------|---------------|---------|
| CozyHome | 60-70% | Moderate gaps, 1 major conflict |
| BrewCrew | 60-70% | Marketing complexity, privacy gaps |
| PetPawz | 65-75% | Clearer requirements, rate limit concerns |
| FitFuel | 55-65% | Multi-location ambiguity |
| Bloom & Co. | 50-65% | Most gaps, perishable inventory complexity |

### After Context Updates

After adding missing information via Level 3 prompts, expect confidence scores to increase by 10-20 percentage points.

---

## 🐛 Known Test Issues

Document any issues you encounter:

- [ ] Issue 1: Description
- [ ] Issue 2: Description
- [ ] Issue 3: Description

---

## 📝 Test Results Template

Use this template to document test results:

```
Test Date: [DATE]
Tester: [NAME]
Agent Used: [Cursor / Claude Desktop / ChatGPT]

| Prompt # | Pass/Fail | Notes |
|----------|-----------|-------|
| 1        | ✅        |       |
| 2        | ✅        |       |
| ...      | ...       | ...   |

Issues Found:
- [Issue description]

Improvements Needed:
- [Improvement suggestion]
```

---

## 🚀 Next Steps

1. **Start Testing**: Run Suite A (Smoke Test) first
2. **Document Results**: Use the template above
3. **Report Issues**: Create issues for any failures
4. **Iterate**: Use feedback to improve the tool
5. **Expand**: Add new prompts as you discover edge cases

---

## 📚 Related Documentation

- **[README.md](README.md)** - Project overview
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - How to use the MCP server
- **[SCENARIOS.md](SCENARIOS.md)** - Test scenario details
- **[AGENTS.md](AGENTS.md)** - Development principles

---

**Happy Testing!** 🎉

For questions or issues, refer to the main README or open an issue in the repository.

