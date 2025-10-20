# Storage Provider Documentation

## Overview

The storage abstraction layer provides a clean interface for storing and retrieving project data across multiple storage platforms. This enables seamless migration from local filesystem to Google Drive, OneDrive, Notion, or any other storage backend.

## Architecture

```
┌─────────────────┐
│   MCP Tools     │
│ (main.py)       │
└────────┬────────┘
         │
         v
┌─────────────────┐
│ Storage Manager │
│  (manager.py)   │
└────────┬────────┘
         │
         v
┌─────────────────┐
│Storage Provider │
│   Interface     │
│   (base.py)     │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬────────────┐
    v         v          v            v
┌───────┐ ┌────────┐ ┌──────┐ ┌───────────┐
│ Local │ │GDrive  │ │Merge │ │  Future   │
│       │ │        │ │ API  │ │ Providers │
└───────┘ └────────┘ └──────┘ └───────────┘
```

## Project Structure

All storage providers implement a consistent three-folder structure:

```
project-root/
├── discovery/          # Discovery documents (emails, transcripts, SOWs)
├── implementation/     # Generated deliverables (SOWs, plans, specs)
├── working/            # Agent notes, drafts, context additions
└── .project.json       # Project metadata and configuration
```

## Using Storage Providers

### Local Filesystem (Current)

```python
from storage import get_storage_provider

# Initialize local storage
storage = get_storage_provider("local", base_path="/path/to/projects")

# Create project
storage.create_project(
    project_id="cozyhome",
    project_name="CozyHome Integration",
    config={"confidence_threshold": 85.0}
)

# Add document
storage.add_document(
    project_id="cozyhome",
    folder_type=FolderType.DISCOVERY,
    filename="initial-email.txt",
    content="Client wants Shopify + QuickBooks integration...",
    metadata={"from": "client@cozyhome.com"}
)

# Save deliverable
storage.save_deliverable(
    project_id="cozyhome",
    filename="sow-v1.md",
    content="# Statement of Work...",
    metadata={"confidence": 85.0}
)
```

### Google Drive (Coming Soon)

```python
from storage import get_storage_provider
from google.oauth2 import service_account

# Initialize Google Drive storage
credentials = service_account.Credentials.from_service_account_file(
    'path/to/credentials.json'
)

storage = get_storage_provider(
    "google_drive",
    credentials=credentials,
    parent_folder_id="1234567890abcdef"  # Parent folder in Drive
)

# Rest of API is identical to local storage
storage.create_project(...)
```

### Merge API (Future)

```python
from storage import get_storage_provider

# Unified API for multiple platforms
storage = get_storage_provider(
    "merge_api",
    api_key="your_merge_api_key",
    account_token="user_account_token"
)

# Works with Google Drive, OneDrive, Dropbox, Box, etc.
# Same API across all platforms
```

## Implementing a New Storage Provider

To add support for a new storage platform:

### 1. Create Provider Class

```python
# storage/my_provider.py
from .base import StorageProvider, FolderType

class MyStorageProvider(StorageProvider):
    def __init__(self, **kwargs):
        # Initialize your storage client
        pass
    
    def list_projects(self) -> List[Dict]:
        # Query your storage platform for projects
        pass
    
    def create_project(self, project_id: str, project_name: str,
                      config: Optional[Dict] = None) -> Dict:
        # Create project folder structure
        pass
    
    # Implement all other abstract methods...
```

### 2. Register in Manager

```python
# storage/manager.py
from .my_provider import MyStorageProvider

def get_storage_provider(provider_type: str = "local", **kwargs):
    if provider_type == "my_storage":
        return MyStorageProvider(**kwargs)
    # ...
```

### 3. Test Implementation

```python
# test_my_provider.py
def test_my_provider():
    storage = get_storage_provider("my_storage", api_key="test")
    
    # Test project creation
    storage.create_project("test-proj", "Test Project")
    
    # Test document operations
    storage.add_document("test-proj", FolderType.DISCOVERY, "test.txt", "content")
    
    # Test retrieval
    doc = storage.get_document("test-proj", FolderType.DISCOVERY, "test.txt")
    assert doc["content"] == "content"
```

## Storage Provider Interface

### Core Methods

#### `list_projects() -> List[Dict]`
List all available projects.

**Returns**:
```python
[
    {
        "project_id": "cozyhome",
        "name": "CozyHome Integration",
        "description": "...",
        "path": "/path/to/project",
        "created_at": "2025-10-20T10:00:00Z"
    }
]
```

#### `create_project(project_id, project_name, config) -> Dict`
Create new project with three-folder structure.

**Creates**:
- discovery/ folder
- implementation/ folder
- working/ folder
- .project.json file

**Returns**: Project metadata dict

#### `add_document(project_id, folder_type, filename, content, metadata)`
Add document to specific folder.

**Args**:
- `folder_type`: FolderType.DISCOVERY, IMPLEMENTATION, or WORKING

#### `save_deliverable(project_id, filename, content, metadata)`
Save generated deliverable to implementation folder.

**Metadata can include**:
- confidence score at generation
- template used
- generation timestamp

#### `get_config(project_id) -> Dict`
Get project configuration.

**Default config**:
```python
{
    "confidence_threshold": 80.0,
    "custom_gap_patterns": [],
    "priority_weights": {...},
    "auto_reanalyze": True
}
```

## Google Drive Setup Guide

### Prerequisites

1. Google Cloud Project with Drive API enabled
2. Service Account or OAuth2 credentials
3. Parent folder in Google Drive for all projects

### Setup Steps

1. **Enable Drive API**
   ```bash
   gcloud services enable drive.googleapis.com
   ```

2. **Create Service Account**
   ```bash
   gcloud iam service-accounts create discovery-agent \
       --display-name="Discovery Agent"
   ```

3. **Generate Credentials**
   ```bash
   gcloud iam service-accounts keys create credentials.json \
       --iam-account=discovery-agent@PROJECT_ID.iam.gserviceaccount.com
   ```

4. **Share Parent Folder**
   - Create a folder in Google Drive
   - Share with service account email (editor access)
   - Get folder ID from URL

5. **Use in Code**
   ```python
   storage = get_storage_provider(
       "google_drive",
       credentials="path/to/credentials.json",
       parent_folder_id="FOLDER_ID_FROM_URL"
   )
   ```

### Folder Structure in Drive

```
Parent Folder/
├── cozyhome/
│   ├── discovery/
│   │   ├── email-01.txt
│   │   └── transcript-sales-call.txt
│   ├── implementation/
│   │   ├── sow-20251020.md
│   │   └── implementation-plan-20251020.md
│   ├── working/
│   │   ├── context-notes.txt
│   │   └── questions-draft.md
│   └── .project.json
└── brewcrew/
    └── ...
```

## Merge API Integration Guide

### What is Merge API?

Merge API provides a unified interface to multiple storage platforms:
- Google Drive
- Microsoft OneDrive
- Dropbox
- Box
- Notion (via File Storage API)

### Setup

1. **Sign up at merge.dev**
2. **Get API Key**
3. **Link User Account** (per customer)
4. **Use Unified API**

```python
storage = get_storage_provider(
    "merge_api",
    api_key="your_api_key",
    account_token="customer_account_token"
)

# Same API works across all platforms
# Merge handles platform-specific differences
```

## Migration Guide

### From Local to Google Drive

1. **Export Projects**
   ```python
   # Save all projects as JSON
   for project in local_storage.list_projects():
       snapshot = generate(project["project_id"], "analysis_snapshot")
       # Save snapshot
   ```

2. **Create Drive Projects**
   ```python
   drive_storage = get_storage_provider("google_drive", ...)
   
   for project in snapshots:
       drive_storage.create_project(project["project_id"], project["name"])
   ```

3. **Upload Documents**
   ```python
   for doc in project["documents"]:
       drive_storage.add_document(
           project_id,
           determine_folder_type(doc),
           doc["filename"],
           doc["content"]
       )
   ```

4. **Update MCP Configuration**
   ```python
   # In main.py, change default storage
   storage = get_storage_provider("google_drive", ...)
   ```

### Zero-Downtime Migration

Use a "migration mode" where writes go to both providers:

```python
class DualStorageProvider(StorageProvider):
    def __init__(self, primary, secondary):
        self.primary = primary
        self.secondary = secondary
    
    def add_document(self, *args, **kwargs):
        self.primary.add_document(*args, **kwargs)
        self.secondary.add_document(*args, **kwargs)  # Async/background
```

## Best Practices

### 1. Always Use Storage Abstraction

❌ **Don't**:
```python
# Direct file operations
with open(f"{project_id}/discovery/email.txt", "w") as f:
    f.write(content)
```

✅ **Do**:
```python
# Use storage provider
storage.add_document(project_id, FolderType.DISCOVERY, "email.txt", content)
```

### 2. Handle Errors Gracefully

```python
try:
    storage.add_document(...)
except Exception as e:
    logger.error(f"Failed to save document: {e}")
    # Fallback or retry logic
```

### 3. Use Metadata

```python
storage.add_document(
    project_id="cozyhome",
    folder_type=FolderType.DISCOVERY,
    filename="email.txt",
    content=content,
    metadata={
        "from": "client@example.com",
        "date": "2025-10-20",
        "importance": "high"
    }
)
```

### 4. Version Deliverables

```python
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"sow_{timestamp}.md"

storage.save_deliverable(
    project_id="cozyhome",
    filename=filename,
    content=sow_content,
    metadata={
        "confidence": 85.0,
        "template": "simplified",
        "version": "1.2"
    }
)
```

## Troubleshooting

### Local Provider Issues

**Problem**: Project not found  
**Solution**: Check base_path is correct and project folder exists

**Problem**: Permission denied  
**Solution**: Ensure write permissions on base_path directory

### Google Drive Issues (Future)

**Problem**: Authentication failed  
**Solution**: Verify credentials.json is valid and not expired

**Problem**: Folder not found  
**Solution**: Ensure parent_folder_id is correct and shared with service account

**Problem**: Quota exceeded  
**Solution**: Check Google Drive API quota limits

## Performance Considerations

### Local Storage
- Fast reads/writes
- No network latency
- Limited by disk I/O

### Google Drive
- Network latency (100-500ms per operation)
- Consider batching operations
- Use caching for frequently accessed documents

### Optimization Tips

```python
# Bad: Multiple individual calls
for doc in documents:
    storage.add_document(project_id, folder, doc.name, doc.content)

# Good: Batch upload (when supported)
storage.batch_add_documents(project_id, folder, documents)
```

## Future Enhancements

- **Caching layer**: Cache frequently accessed documents
- **Batch operations**: Upload/download multiple files at once
- **Sync status**: Track sync state for offline-first capability
- **Conflict resolution**: Handle concurrent edits
- **Version control**: Built-in versioning for deliverables
- **Search indexing**: Full-text search across all documents

## Support

For issues or questions:
- Check existing provider implementations in `storage/`
- Review test cases in `test_storage.py`
- Refer to platform-specific documentation (Google Drive API, Merge API docs)

