# Convex Integration Overview for Admin Portal Team

## System Architecture

The Discovery Agent system has **two entry points** to the Convex database:

1. **MCP Server** (Python) - Analyzes discovery documents and syncs findings to Convex
2. **Admin Portal** (Your Frontend) - Web interface for managing projects and viewing analysis

Both systems connect to the **same Convex backend** and coordinate data updates.

```
┌─────────────────┐    ┌─────────────────┐
│   ChatGPT/MCP   │    │  Admin Portal   │
│   Clients       │    │  (Frontend)    │
└─────────┬───────┘    └─────────┬───────┘
          │                      │
          │                      │
          ▼                      ▼
    ┌─────────────────────────────────────┐
    │         Convex Database              │
    │  (Shared Backend for Both Systems)  │
    └─────────────────────────────────────┘
```

## Database Schema

Convex has **8 main tables** defined in `mcp/convex/schema.ts`:

### 1. **projects** (Main Entity)
**Purpose**: Core project metadata and summary statistics

| Field | Type | Description |
|-------|------|-------------|
| `scenarioId` | string | Unique identifier from MCP (e.g., "scenario-1-cozyhome") |
| `name` | string | Project display name |
| `confidence` | number | Overall confidence score (0-100) |
| `gapsCount` | number | Number of open gaps |
| `conflictsCount` | number | Number of unresolved conflicts |
| `ambiguitiesCount` | number | Number of unclear requirements |
| `documentsCount` | number | Number of ingested documents |
| `lastUpdated` | number | Timestamp in milliseconds |
| `status` | union | "active" \| "archived" \| "draft" |

**Indexes**: `by_scenarioId`, `by_status`, `by_lastUpdated`

### 2. **gaps** (Missing Information)
**Purpose**: Track missing or unclear requirements

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | id | References projects table |
| `category` | string | e.g., "business_rules", "technical_constraints" |
| `description` | string | What's missing |
| `impact` | union | "high" \| "medium" \| "low" |
| `priority` | union | "high" \| "medium" \| "low" |
| `status` | union | "open" \| "in-progress" \| "resolved" |
| `identifiedDate` | number | Timestamp when gap was found |
| `suggestedQuestion` | string? | Clarifying question to ask |

**Indexes**: `by_project`, `by_status`, `by_priority`, `by_project_status`

### 3. **conflicts** (Contradictions)
**Purpose**: Track conflicting statements from different sources

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | id | References projects table |
| `category` | string | Conflict category |
| `description` | string | What's conflicting |
| `impact` | union | "high" \| "medium" \| "low" |
| `priority` | union | "high" \| "medium" \| "low" |
| `status` | union | "open" \| "in-progress" \| "resolved" |
| `identifiedDate` | number | Timestamp when conflict was found |
| `conflictingStatements` | string[] | The contradicting statements |
| `sources` | string[] | Where they came from |

**Indexes**: `by_project`, `by_status`, `by_priority`, `by_project_status`

### 4. **ambiguities** (Unclear Requirements)
**Purpose**: Track ambiguous terms that need clarification

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | id | References projects table |
| `category` | string | Ambiguity category |
| `description` | string | The ambiguous term |
| `impact` | union | "high" \| "medium" \| "low" |
| `clarificationNeeded` | string | What needs to be clarified |
| `status` | union | "open" \| "clarified" \| "resolved" |
| `identifiedDate` | number | Timestamp when ambiguity was found |
| `context` | string | Where it was found |

**Indexes**: `by_project`, `by_status`, `by_project_status`

### 5. **questions** (Questions Needing Answers)
**Purpose**: Track questions extracted from analysis

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | id | References projects table |
| `question` | string | The question text |
| `category` | string | Question category |
| `priority` | union | "high" \| "medium" \| "low" |
| `status` | union | "open" \| "answered" \| "deferred" |
| `askedDate` | number | When question was created |
| `answer` | string? | Answer text (if answered) |
| `answeredDate` | number? | When it was answered |
| `whyItMatters` | string? | Why this question is important |

**Indexes**: `by_project`, `by_status`, `by_priority`, `by_project_status`

### 6. **documents** (Ingested Files)
**Purpose**: Track uploaded/processed documents

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | id | References projects table |
| `name` | string | Filename |
| `type` | string | e.g., "email", "transcript", "sow" |
| `uploadDate` | number | When document was processed |
| `size` | string | Human-readable size (e.g., "2.5 MB") |
| `status` | union | "processed" \| "processing" \| "pending" |
| `sourceLink` | string? | URL to original file |
| `metadata` | any? | Additional context |

**Indexes**: `by_project`, `by_status`, `by_type`

### 7. **contextEvents** (Activity Timeline)
**Purpose**: Track all project activity for timeline view

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | id | References projects table |
| `eventType` | union | See event types below |
| `description` | string | Human-readable description |
| `timestamp` | number | When event occurred |
| `metadata` | any? | Additional event data |

**Event Types**: `document_added`, `gap_identified`, `conflict_resolved`, `question_answered`, `confidence_updated`, `ambiguity_clarified`, `project_created`, `analysis_completed`

**Indexes**: `by_project`, `by_timestamp`, `by_project_timestamp`, `by_eventType`

### 8. **deliverables** (Generated Outputs)
**Purpose**: Track generated documents (SOWs, plans, etc.)

| Field | Type | Description |
|-------|------|-------------|
| `projectId` | id | References projects table |
| `name` | string | Deliverable name |
| `type` | union | See types below |
| `generatedDate` | number | When it was created |
| `status` | union | "draft" \| "final" \| "archived" |
| `fileType` | string | e.g., "markdown", "pdf" |
| `downloadUrl` | string? | Link to download |

**Types**: `implementation_plan`, `requirements_document`, `technical_specification`, `gap_analysis_report`, `risk_assessment`, `sow`

**Indexes**: `by_project`, `by_status`, `by_type`

## Data Sync Patterns

### How MCP Syncs to Convex

The MCP server uses the `sync_to_convex()` tool with these patterns:

#### 1. **Project Creation/Update** (`upsertProject`)
```python
# MCP calls this whenever analyzing a project
project_data = {
    "scenarioId": "scenario-1-cozyhome",
    "name": "CozyHome Integration",
    "confidence": 78.5,
    "gapsCount": 5,
    "conflictsCount": 2,
    "ambiguitiesCount": 3,
    "documentsCount": 4,
    "status": "active"
}

# Returns Convex project ID for subsequent operations
project_id = convex_sync.sync_project_metadata(project)
```

#### 2. **Analysis Results** (Bulk Insert)
```python
# MCP sends arrays of findings
convex_sync.sync_gaps(project_id, gaps_list)
convex_sync.sync_conflicts(project_id, conflicts_list)
convex_sync.sync_ambiguities(project_id, ambiguities_list)
convex_sync.sync_questions(project_id, questions_list)
```

#### 3. **Document Metadata**
```python
# MCP sends document info (not file contents)
convex_sync.sync_documents(project_id, documents_list)
```

#### 4. **Event Logging**
```python
# MCP logs timeline events
convex_sync.log_event(
    project_id,
    "analysis_completed",
    "Analysis completed with 78% confidence",
    {"confidence": 78.5}
)
```

### Important Sync Behaviors

1. **Project Identification**: MCP uses `scenarioId` to find existing projects, Convex returns internal `_id`
2. **Bulk Operations**: MCP sends arrays of items, creates multiple records at once
3. **Timestamp Format**: All timestamps are in milliseconds (`Date.now()`)
4. **Denormalized Counts**: Projects store counts (gapsCount, etc.) for performance

## Update Rules

### Who Updates What

| Entity | MCP Updates | Admin Portal Updates | Notes |
|--------|-------------|----------------------|-------|
| **Project confidence** | ✅ After analysis | ❌ No | Calculated from analysis |
| **Project counts** | ✅ After sync | ✅ After user actions | Both should recalculate |
| **Gap status** | ✅ When resolved by new docs | ✅ User-driven | Both can resolve |
| **Conflict status** | ✅ When resolved by new docs | ✅ User-driven | Both can resolve |
| **Ambiguity status** | ✅ When clarified | ✅ User-driven | Both can clarify |
| **Question status** | ⚠️ Partial | ✅ Primary | Both can answer |
| **Project status** | ❌ No | ✅ User-driven | "active" → "archived" |
| **Timeline events** | ✅ Analysis events | ✅ User action events | Both add events |

### Bidirectional Updates

**Key Insight**: MCP can update existing findings when new information resolves them:

```python
# Example: New document resolves a conflict
update(project_id="cozyhome", 
       type="context", 
       content="Meeting notes confirm QuickBooks is source of truth")

# MCP re-analyzes and updates Convex:
# - Marks conflict as "resolved"
# - Updates confidence score
# - Logs resolution event
```

## API Reference

### Queries (Read Operations)

#### `listProjects`
```typescript
// Get all projects
const projects = await ctx.db
  .query("projects")
  .withIndex("by_lastUpdated")
  .order("desc")
  .collect();

// Filter by status
const activeProjects = await ctx.db
  .query("projects")
  .withIndex("by_status", q => q.eq("status", "active"))
  .collect();
```

#### `getProjectDetails`
```typescript
// Get project with all related data
const project = await ctx.db.get(projectId);

const gaps = await ctx.db
  .query("gaps")
  .withIndex("by_project", q => q.eq("projectId", projectId))
  .collect();

const conflicts = await ctx.db
  .query("conflicts")
  .withIndex("by_project", q => q.eq("projectId", projectId))
  .collect();

// ... similar for ambiguities, questions, documents
```

#### `getProjectByScenarioId`
```typescript
// Find project by MCP scenario ID
const project = await ctx.db
  .query("projects")
  .withIndex("by_scenarioId", q => q.eq("scenarioId", "scenario-1-cozyhome"))
  .first();
```

#### `getProjectTimeline`
```typescript
// Get activity timeline
const events = await ctx.db
  .query("contextEvents")
  .withIndex("by_project_timestamp", q => q.eq("projectId", projectId))
  .order("desc")
  .collect();
```

### Mutations (Write Operations)

#### Project Mutations
```typescript
// Create/update project (called by MCP)
await ctx.db.patch(projectId, {
  confidence: 85.0,
  gapsCount: 3,
  lastUpdated: Date.now()
});

// Update project status (called by Admin Portal)
await ctx.db.patch(projectId, {
  status: "archived",
  lastUpdated: Date.now()
});

// Delete project (cascades to all related data)
await deleteProject({ projectId });
```

#### Gap Mutations
```typescript
// Bulk insert gaps (called by MCP)
await ctx.db.insert("gaps", {
  projectId,
  category: "business_rules",
  description: "Missing refund policy",
  impact: "high",
  priority: "high",
  status: "open",
  identifiedDate: Date.now(),
  suggestedQuestion: "How should refunds be handled?"
});

// Update gap status (called by Admin Portal)
await ctx.db.patch(gapId, {
  status: "resolved"
});
```

#### Question Mutations
```typescript
// Answer question (called by Admin Portal)
await ctx.db.patch(questionId, {
  answer: "Refunds are processed daily via QuickBooks",
  answeredDate: Date.now(),
  status: "answered"
});
```

#### Event Logging
```typescript
// Log user action (called by Admin Portal)
await ctx.db.insert("contextEvents", {
  projectId,
  eventType: "question_answered",
  description: "Question answered: How are refunds handled?",
  timestamp: Date.now(),
  metadata: { answeredBy: "user" }
});
```

## Frontend Integration Patterns

### 1. **Project Dashboard**
```typescript
// Display project list with confidence scores
const useProjects = () => {
  return useQuery(api.queries.projects.listProjects, {
    status: "active"
  });
};

// Component
const ProjectCard = ({ project }) => (
  <div>
    <h3>{project.name}</h3>
    <div>Confidence: {project.confidence}%</div>
    <div>Gaps: {project.gapsCount}</div>
    <div>Conflicts: {project.conflictsCount}</div>
  </div>
);
```

### 2. **Project Detail View**
```typescript
// Get full project data
const useProjectDetails = (projectId) => {
  return useQuery(api.queries.projects.getProjectDetails, { projectId });
};

// Filter by status
const openGaps = gaps.filter(g => g.status === "open");
const highPriorityGaps = gaps.filter(g => g.priority === "high");
```

### 3. **Status Updates** (User Actions)
```typescript
// Mark gap as resolved
const markGapResolved = useMutation(api.mutations.gaps.updateGapStatus);

const handleResolveGap = async (gapId) => {
  await markGapResolved({
    gapId,
    status: "resolved"
  });
  
  // Recalculate project counts
  await recalculateProjectCounts(projectId);
  
  // Log event
  await logEvent({
    projectId,
    eventType: "gap_identified", // or custom type
    description: "Gap marked as resolved by user"
  });
};
```

### 4. **Timeline View**
```typescript
// Display activity timeline
const useTimeline = (projectId) => {
  return useQuery(api.queries.projects.getProjectTimeline, { projectId });
};

// Group events by date
const eventsByDate = groupBy(events, event => 
  new Date(event.timestamp).toDateString()
);
```

### 5. **Real-time Updates**
```typescript
// Subscribe to project changes
const useProjectSubscription = (projectId) => {
  return useQuery(api.queries.projects.getProjectDetails, { projectId });
};

// Component automatically re-renders when MCP updates data
const ProjectView = ({ projectId }) => {
  const project = useProjectSubscription(projectId);
  // Component updates automatically when MCP syncs new analysis
};
```

## Data Consistency Guidelines

### 1. **Count Synchronization**
Projects store denormalized counts that can get out of sync:

```typescript
// Always recalculate after mutations
const recalculateCounts = async (projectId) => {
  const gaps = await ctx.db.query("gaps")
    .withIndex("by_project", q => q.eq("projectId", projectId))
    .collect();
    
  const conflicts = await ctx.db.query("conflicts")
    .withIndex("by_project", q => q.eq("projectId", projectId))
    .collect();
    
  await ctx.db.patch(projectId, {
    gapsCount: gaps.length,
    conflictsCount: conflicts.length,
    lastUpdated: Date.now()
  });
};
```

### 2. **Prevent Duplicate Analysis Items**
When MCP re-runs analysis, it may create duplicates:

**Option A: Clear old analysis first** (Recommended)
```typescript
// Add mutation to clear old analysis
export const clearProjectAnalysis = mutation({
  args: { projectId: v.id("projects") },
  handler: async (ctx, args) => {
    // Delete old gaps, conflicts, ambiguities
    const gaps = await ctx.db.query("gaps")
      .withIndex("by_project", q => q.eq("projectId", args.projectId))
      .collect();
    for (const gap of gaps) await ctx.db.delete(gap._id);
    
    // Similar for conflicts, ambiguities
  }
});
```

**Option B: Upsert with unique keys** (Requires schema change)
```typescript
// Add unique index on (projectId, description)
gaps: defineTable({...})
  .index("by_project_description", ["projectId", "description"])
```

### 3. **Handle Race Conditions**
If both MCP and Admin Portal update simultaneously:

- **MCP updates**: confidence, counts (from analysis)
- **Admin Portal updates**: status, user actions

These rarely conflict because they update different fields. If they do:
- Convex transactions are atomic
- Last write wins (based on `lastUpdated`)
- Use optimistic updates in frontend

### 4. **Soft vs Hard Deletes**
**Soft delete** (recommended):
```typescript
await ctx.db.patch(projectId, { 
  status: "archived",
  lastUpdated: Date.now()
});
```

**Hard delete** (cascades to all related data):
```typescript
await deleteProject({ projectId });
```

## Example Workflows

### Workflow 1: User Analyzes Project via ChatGPT

1. **User**: "Analyze the CozyHome project"
2. **ChatGPT** → **MCP**: 
   ```
   ingest(project_id="scenario-1-cozyhome", source="local")
   analyze(project_id="scenario-1-cozyhome", mode="full")
   ```
3. **MCP**: Loads documents, runs analysis, detects 5 gaps, 2 conflicts, 3 ambiguities, confidence: 78%
4. **MCP** → **Convex** (if user calls `sync_to_convex()`):
   ```
   upsertProject({ scenarioId: "scenario-1-cozyhome", confidence: 78, ... })
   → Returns projectId: "k_abc123"
   
   syncGaps({ projectId: "k_abc123", gaps: [...5 items...] })
   syncConflicts({ projectId: "k_abc123", conflicts: [...2 items...] })
   syncAmbiguities({ projectId: "k_abc123", ambiguities: [...3 items...] })
   
   logEvent({ projectId: "k_abc123", eventType: "analysis_completed", ... })
   ```
5. **Convex Database**: Now has complete project state
6. **Admin Portal**: Automatically sees new data via subscriptions
7. **PM**: Marks 2 gaps as resolved
8. **Admin Portal**: Updates gap status, recalculates counts, logs events

### Workflow 2: MCP Resolves Conflict with New Documents

1. **Initial State**: Conflict exists - "Email says inventory in QuickBooks, SOW says Shopify"
2. **User**: Provides new meeting notes via MCP
3. **MCP**: Re-analyzes, detects conflict is resolved
4. **MCP** → **Convex**: Updates conflict status to "resolved"
5. **MCP**: Recalculates confidence (78% → 82%)
6. **MCP** → **Convex**: Updates project confidence
7. **Admin Portal**: Shows updated confidence, resolved conflict in timeline

### Workflow 3: Admin Portal User Actions

1. **PM**: Views project dashboard, sees 5 open gaps
2. **PM**: Clicks on gap "Missing refund policy"
3. **PM**: Provides answer: "Refunds processed daily via QuickBooks"
4. **Admin Portal**: 
   ```
   updateGapStatus({ gapId: "k_gap1", status: "resolved" })
   recalculateProjectCounts({ projectId: "k_abc123" })
   logEvent({ projectId: "k_abc123", eventType: "gap_identified", ... })
   ```
5. **Admin Portal**: Shows updated counts (5 → 4 gaps), logs timeline event

## Security Considerations

### Current State
- **No authentication** implemented
- **No authorization** (role-based access)
- **No rate limiting** on mutations
- **Basic validation** via Convex schema

### Recommendations
1. **Add authentication** to mutations
2. **Implement user roles** (admin, PM, viewer)
3. **Add rate limiting** to prevent abuse
4. **Add business logic validation** (e.g., confidence 0-100)

## Environment Configuration

### MCP Environment Variables
```bash
# Required for Convex sync
CONVEX_DEPLOYMENT_URL=https://your-deployment.convex.cloud

# Optional auto-sync flags
AUTO_SYNC_ON_ANALYZE=false  # Auto-sync after analysis
AUTO_SYNC_ON_UPDATE=false   # Auto-sync after update
AUTO_SYNC_ON_CREATE=false   # Auto-sync on project create
```

### Admin Portal Environment
```bash
CONVEX_URL=https://your-deployment.convex.cloud
# Add auth credentials as needed
```

## Implementation Phases

### Phase 1: Read-Only Dashboard
1. Implement `listProjects` query
2. Display projects with confidence scores
3. Implement `getProjectDetails` query
4. Show gaps, conflicts, ambiguities, questions

### Phase 2: User Actions
5. Add "Mark as Resolved" for gaps/conflicts
6. Add "Answer Question" functionality
7. Implement status updates (active → archived)
8. Add timeline view with events

### Phase 3: Data Management
9. Add "Refresh Analysis" button (clears old, triggers MCP re-sync)
10. Implement count recalculation
11. Add duplicate detection
12. Add audit logging

### Phase 4: Polish
13. Add real-time subscriptions for live updates
14. Implement optimistic updates for better UX
15. Add data visualization (confidence trends)
16. Export functionality for deliverables

## Key Questions for Your Team

1. **Auto-sync**: Should MCP auto-sync after every analysis, or only when explicitly called?

2. **Duplicate handling**: When re-running analysis, should we clear old gaps/conflicts first?

3. **Authentication**: Do you need API key auth or other security measures?

4. **Admin portal capabilities**: Should it trigger MCP operations, or is it read-only with manual MCP invocation?

5. **Delete behavior**: Should "archiving" a project hide it or permanently delete it?

---

This overview provides everything your admin portal team needs to build against the Convex backend. The system is designed for bidirectional updates between MCP and Admin Portal, with clear patterns for maintaining data consistency.
