# FunctionTool Callable Error - FIXED ✅

## Problem

When calling MCP tools through the OffBench environment, you were getting:
```
TypeError: 'FunctionTool' object is not callable
```

This occurred specifically when:
- Running `analyze()` on projects with local test data
- The `analyze()` tool tried to auto-load documents by calling `ingest()` internally
- FastMCP-decorated tools (`@mcp.tool()`) cannot call other FastMCP-decorated tools directly

## Root Cause

**FastMCP Limitation**: Tools decorated with `@mcp.tool()` are wrapped in a `FunctionTool` object that's only callable through the MCP protocol, NOT directly from Python code.

When we implemented auto-loading in `analyze()`, it tried to call `ingest()` directly:
```python
@mcp.tool()
def analyze(...):
    # This FAILS because ingest is a FunctionTool, not a regular function
    result = ingest(project_id=project_id, ...)  # ❌ Error!
```

## Solution

**Extract business logic into internal helper functions** that can be called by both MCP tools and other internal functions.

### Architecture Pattern

```python
# Internal helper function (plain Python - callable)
def _ingest_documents(...) -> Dict:
    """Internal function with all the business logic"""
    # All the actual ingestion code here
    return result

# Public MCP tool (FastMCP wrapper - only callable via MCP)
@mcp.tool()
def ingest(...) -> Dict:
    """Public API exposed to MCP clients"""
    return _ingest_documents(...)

# Other tools can now call the internal function
@mcp.tool()
def analyze(...):
    # This WORKS because _ingest_documents is plain Python
    result = _ingest_documents(...)  # ✅ Success!
```

## Changes Made

### 1. Refactored `ingest()` Tool
- Created `_ingest_documents()` - internal helper with all business logic
- `ingest()` MCP tool now just wraps the internal function
- **File**: `mcp/src/main.py` lines 199-353

### 2. Refactored `analyze()` Tool
- Created `_analyze_project()` - internal helper with all business logic
- `analyze()` MCP tool handles batch mode and delegates to internal function
- **File**: `mcp/src/main.py` lines 356-566

### 3. Updated Internal Cross-Tool Calls
- `analyze()` now calls `_ingest_documents()` for auto-loading
- `update()` now calls `_analyze_project()` for auto-reanalysis
- Batch mode in `analyze()` calls `_analyze_project()` for each project

## Test Results

✅ **All tests passing**:
- Internal functions are callable
- Auto-loading works correctly
- No 'FunctionTool' errors
- Analysis runs successfully:
  - **Confidence**: 81% on scenario-1-cozyhome
  - **Documents loaded**: 4 files automatically
  - **Full analysis**: Completed without errors

## How to Use

### Through MCP Protocol (Normal Usage)

When using the MCP server through Claude Desktop, Cursor, or other MCP clients:

```
# These work through the MCP protocol
analyze project_id="scenario-1-cozyhome" mode="quick"
ingest project_id="scenario-2-brewcrew" source="local"
```

The server will handle the auto-loading automatically now!

### Direct Python Testing (Development)

For local development and testing:

```python
from main import _analyze_project, _ingest_documents

# Use internal functions for testing
result = _analyze_project(project_id="scenario-1-cozyhome", mode="full")
docs = _ingest_documents(project_id="scenario-2-brewcrew", source="local")
```

## Verification

Run the verification script:
```bash
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
python3 verify_fix.py
```

Expected output:
```
✓ Internal functions are callable
✓ Analysis successful!
  - Confidence: 81.0%
  - Clarity: 80%
  - Completeness: 80%
✓ No 'FunctionTool' errors in internal function calls!
```

## Testing with Test Prompts

Now you can use the test prompts from `TEST_PROMPTS.md`:

### Level 1: Basic Operations ✅
```
Run a quick confidence check on scenario-1-cozyhome
```

### Level 2: Document Analysis ✅
```
Analyze scenario-1-cozyhome in full mode. What gaps and ambiguities do you find?
```

### Level 4: Feedback Loop ✅
```
For scenario-1-cozyhome, add this context: "Client uses QuickBooks Online..."
```

All these should now work without the FunctionTool error!

## Key Takeaways

1. **FastMCP tools are NOT directly callable** - they're only callable through the MCP protocol
2. **Internal cross-tool communication requires helper functions** - extract business logic into plain Python functions
3. **Pattern**: `@mcp.tool()` wrapper → internal `_function_name()` with logic
4. **This is a common FastMCP pattern** for complex multi-tool workflows

## Related Files

- **Main implementation**: `mcp/src/main.py`
- **Test script**: `verify_fix.py`
- **Test prompts**: `TEST_PROMPTS.md`
- **Local file support**: Already implemented and working

## Next Steps

1. ✅ FunctionTool error fixed
2. ✅ Local file auto-loading working
3. ✅ Test prompts ready to use
4. 🚀 Start testing with the MCP server through your preferred client

---

**Status**: FIXED ✅  
**Tested**: January 2025  
**Verified**: All tests passing

