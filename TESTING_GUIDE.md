# MCP Server Testing Guide

Quick reference for testing the Discovery Agent MCP server.

## Quick Test Commands

### Run Full Integrity Test (Recommended)
```bash
cd /Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify
python3 test_mcp_integrity.py
```

Expected output: `✅ ALL TESTS PASSED! MCP Server integrity verified.`

### Check Server Health
```bash
python3 test_mcp_server.py
```

### Start MCP Server
```bash
cd mcp
python src/main.py  # HTTP mode (port 8123)
# or
python src/main.py --stdio  # stdio mode (for Claude/Cursor)
```

---

## What Gets Tested

### Core MCP Tools (13 tests)
- ✅ `manage_project` - Project listing and retrieval
- ✅ `ingest` - Document loading (4 docs, multiple types)
- ✅ `analyze` - Full analysis, confidence scoring, system detection
- ✅ `update` - Context addition and reanalysis
- ✅ `generate` - Template loading and validation
- ✅ `query` - Document search and retrieval

### Convex Integration (11 tests)
- ✅ `ConvexClient` - HTTP connection and queries
- ✅ `ConvexSync` - Project metadata, gaps, conflicts, ambiguities
- ✅ Document sync
- ✅ Question extraction and sync
- ✅ Event logging
- ✅ Data verification and consistency

### Error Handling (6 tests)
- ✅ Non-existent projects
- ✅ Empty document sets
- ✅ Invalid file paths
- ✅ Baseline confidence behavior

---

## Test Scenarios

### scenario-1-cozyhome (Primary Test Data)
Used for deep testing:
- 4 documents (2 emails, 1 SOW, 1 catalog)
- 81% expected confidence
- 3 systems (Shopify, QuickBooks, PayPal)
- 2 gaps, 4 ambiguities, 1 conflict

### Other Scenarios (Available)
- scenario-2-brewcrew
- scenario-3-petpawz
- scenario-4-fitfuel
- scenario-5-bloom

---

## Expected Results

### Confidence Scores
- **CozyHome**: ~81%
- **Empty Project**: 68% (baseline)
- **Range**: 0-100%

### Systems Detected
- Shopify, QuickBooks, PayPal (CozyHome)

### Convex Data
- Projects synced with matching confidence
- All gaps/conflicts/ambiguities persisted
- Documents count matches local state
- Events logged correctly

---

## Troubleshooting

### Test Failures

**If Convex tests fail:**
```bash
# Check Convex URL is set
echo $CONVEX_DEPLOYMENT_URL

# If not set, create .env file in mcp/ directory:
cd mcp
echo "CONVEX_DEPLOYMENT_URL=https://your-deployment.convex.cloud" > .env
```

**If document loading fails:**
```bash
# Verify test data exists
ls -la test-data/scenario-1-cozyhome/
```

**If server not responding:**
```bash
# Check if server is running
lsof -i :8123

# Kill and restart
pkill -f "python.*main.py"
cd mcp && python src/main.py &
```

### Common Issues

1. **Port 8123 already in use**
   ```bash
   lsof -i :8123
   kill <PID>
   ```

2. **Import errors**
   ```bash
   cd mcp
   pip install -r ../requirements.txt
   ```

3. **Convex connection timeout**
   - Check internet connection
   - Verify CONVEX_DEPLOYMENT_URL is correct
   - Check Convex deployment status

---

## Adding New Tests

To add tests to `test_mcp_integrity.py`:

```python
# Add to appropriate phase section
print("\n→ Testing new_feature()...")
result = test_new_feature()
results.test(
    "Feature name - test description",
    result is not None and result.success,
    f"Details: {result.message}"
)
```

---

## Test Data Management

### Creating New Test Scenarios

```bash
cd test-data
mkdir scenario-6-newclient
cd scenario-6-newclient

# Create folder structure
mkdir -p emails transcripts client-docs

# Add test documents...
```

### Required Document Types
- At least 1 email or transcript
- Optional: SOW draft, guides, notes
- Format: .txt files with standard headers

---

## CI/CD Integration

For automated testing:

```bash
#!/bin/bash
# Start server in background
cd mcp && python src/main.py &
SERVER_PID=$!

# Wait for server to start
sleep 3

# Run tests
python3 test_mcp_integrity.py
TEST_RESULT=$?

# Cleanup
kill $SERVER_PID

exit $TEST_RESULT
```

---

## Performance Benchmarks

Expected performance (MacBook Pro, M1):
- Document loading: < 1 second
- Full analysis: < 2 seconds  
- Convex sync: < 3 seconds
- Total test suite: < 15 seconds

---

## Test Output Files

Tests create no output files (non-destructive).

However, the MCP server may create:
- `mcp/implementation/` - Generated deliverables
- `mcp/working/` - Context updates

These are temporary and can be deleted.

---

## Manual Testing via Cursor

1. Start server: `cd mcp && python src/main.py --stdio`
2. In Cursor chat: "Call manage_project with action='list'"
3. Verify tools are accessible and working

---

## Support

For issues or questions:
1. Check TEST_RESULTS.md for detailed test output
2. Check TROUBLESHOOTING.md for common issues
3. Review mcp/README.md for tool documentation

---

**Last Updated**: October 20, 2025  
**Test Suite Version**: 1.0  
**Status**: All tests passing ✅

