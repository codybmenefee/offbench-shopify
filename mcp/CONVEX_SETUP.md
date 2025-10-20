# Convex Integration Setup Guide

This guide walks through setting up Convex for the Discovery Agent MCP to enable the admin portal observability features.

## Overview

The MCP server uses Convex as a persistence layer to store project data for the admin portal. The architecture is:

```
Agent → MCP Tools → In-Memory State (during operations)
                  ↓ (explicit sync)
                  Convex Database
                  ↓ (read-only)
                  Admin Portal (separate repo)
```

## Prerequisites

- Node.js 18+ (for Convex CLI)
- Python 3.9+ (for MCP server)
- A Convex account (free at https://convex.dev)

## Step 1: Install Convex CLI

```bash
npm install -g convex
```

## Step 2: Create Convex Project

1. Go to https://dashboard.convex.dev
2. Create a new project (e.g., "discovery-agent")
3. Note your deployment URL (e.g., `https://happy-animal-123.convex.cloud`)

## Step 3: Deploy Convex Functions

From the MCP repository root:

```bash
cd mcp/convex
npm install
convex dev
```

This will:
- Install Convex dependencies
- Generate TypeScript types
- Deploy your schema and functions
- Start watching for changes

For production deployment:

```bash
convex deploy --prod
```

## Step 4: Get Admin API Key

1. In Convex dashboard, go to Settings → API Keys
2. Create a new API key with admin access
3. Copy the key (starts with `prod:...` or `dev:...`)

## Step 5: Configure MCP Server

Create a `.env` file in the `mcp/` directory:

```bash
cp .env.example .env
```

Edit `.env` and add your Convex credentials:

```env
CONVEX_DEPLOYMENT_URL=https://happy-animal-123.convex.cloud
CONVEX_ADMIN_KEY=prod:happy-animal-123|abcd1234...
```

## Step 6: Test the Integration

Start your MCP server:

```bash
cd mcp
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python src/main.py
```

Test syncing a project to Convex:

```python
# In your MCP client/agent:

# 1. Create and analyze a project
manage_project(action="create", project_id="test-project", project_name="Test Project")
ingest(project_id="test-project", source="local")
analyze(project_id="test-project", mode="full")

# 2. Sync to Convex
sync_to_convex(project_id="test-project", sync_type="full")

# Result should show:
# {
#   "project_id": "test-project",
#   "convex_project_id": "j57...",
#   "synced_components": ["metadata", "analysis", "documents", "questions"],
#   "gaps_synced": 3,
#   "conflicts_synced": 1,
#   ...
# }
```

## Step 7: Verify in Convex Dashboard

1. Go to your Convex dashboard
2. Navigate to Data → Tables
3. You should see tables populated:
   - `projects` - Your test project
   - `gaps` - Identified gaps
   - `questions` - Extracted questions
   - `documents` - Document metadata
   - `contextEvents` - Activity timeline

## Using Convex with MCP Tools

### Manual Sync (Recommended)

The agent explicitly decides when to sync:

```python
# After analysis
analyze(project_id="cozyhome", mode="full")
sync_to_convex(project_id="cozyhome", sync_type="full")

# Update just questions
sync_to_convex(project_id="cozyhome", sync_type="questions")

# Partial sync
sync_to_convex(project_id="cozyhome", sync_type="full", 
              components=["metadata", "questions"])
```

### Sync Types

- **`full`**: Sync everything (metadata, analysis, documents, questions)
- **`metadata`**: Only project info and counts
- **`analysis`**: Only gaps, conflicts, ambiguities
- **`questions`**: Only extracted questions
- **`documents`**: Only document metadata

### Auto-Sync (Optional)

Set environment variables to enable automatic syncing:

```env
AUTO_SYNC_ON_ANALYZE=true
AUTO_SYNC_ON_UPDATE=true
AUTO_SYNC_ON_CREATE=true
```

⚠️ **Note**: Auto-sync adds latency to operations. Recommended for production but disable during rapid development/testing.

## Admin Portal Setup

Once Convex is set up and data is syncing, you can:

1. Set up the admin portal (separate Next.js repo)
2. Configure it to read from the same Convex deployment
3. Use the Convex React hooks to display projects, gaps, questions, etc.

The admin portal queries Convex directly (read-only) and doesn't call the MCP server.

## Authentication (Future)

Currently using simple API key authentication. When ready to add user auth:

### Option 1: Clerk

```env
CONVEX_AUTH_ENABLED=true
CLERK_PUBLISHABLE_KEY=pk_test_...
CLERK_SECRET_KEY=sk_test_...
```

Convex + Clerk integration guide: https://docs.convex.dev/auth/clerk

### Option 2: WorkOS

```env
CONVEX_AUTH_ENABLED=true
WORKOS_API_KEY=sk_...
WORKOS_CLIENT_ID=client_...
```

WorkOS integration: https://workos.com/docs

## Troubleshooting

### "Convex not configured" error

Make sure `.env` file exists and contains:
```env
CONVEX_DEPLOYMENT_URL=https://...
CONVEX_ADMIN_KEY=...
```

### Schema mismatch errors

Redeploy your schema:
```bash
cd mcp/convex
convex deploy --prod
```

### API authentication failures

1. Check that your API key is correct
2. Verify it has admin permissions in Convex dashboard
3. Ensure no extra whitespace in `.env` file

### Sync fails with "Project not found"

Make sure the project exists in MCP memory:
```python
manage_project(action="get", project_id="your-project")
```

## Data Schema

See `mcp/convex/schema.ts` for the complete schema definition.

Key tables:
- **projects**: Main project entities
- **gaps**: Missing information
- **conflicts**: Contradictions
- **ambiguities**: Unclear requirements
- **questions**: Questions needing answers
- **documents**: Document metadata
- **contextEvents**: Activity timeline
- **deliverables**: Generated outputs

All tables match the frontend data structures exactly.

## Next Steps

1. ✅ Set up Convex deployment
2. ✅ Configure environment variables
3. ✅ Test sync operations
4. ⏳ Build admin portal
5. ⏳ Add Clerk or WorkOS authentication
6. ⏳ Add Google Drive integration

## Support

For issues or questions:
- Convex docs: https://docs.convex.dev
- MCP server issues: [GitHub repo]
- Team Slack: [channel link]

