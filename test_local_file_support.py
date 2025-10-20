#!/usr/bin/env python3
"""
Test script to verify local file support is working correctly.
Tests the auto-loading functionality implemented in the MCP server.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "mcp" / "src"))

from storage import get_storage_provider
from core.state_manager import ProjectStateManager
from main import analyze, ingest, manage_project

# Setup
BASE_PATH = Path(__file__).parent / "test-data"
print(f"Testing with base path: {BASE_PATH}")
print("-" * 60)

# Test 1: List available projects
print("\n[TEST 1] Listing available projects...")
result = manage_project(action="list")
print(f"✓ Found {result['count']} projects:")
for project in result['projects']:
    print(f"  - {project['project_id']}: {project.get('name', 'N/A')}")

# Test 2: Auto-load and analyze without explicit ingest
print("\n[TEST 2] Auto-loading documents via analyze()...")
project_id = "scenario-1-cozyhome"
result = analyze(project_id=project_id, mode="quick")

if "error" in result:
    print(f"✗ FAILED: {result['error']}")
    sys.exit(1)
else:
    print(f"✓ SUCCESS: Analyzed {project_id}")
    print(f"  - Confidence: {result['confidence']}%")
    print(f"  - Clarity: {result['clarity']}%")
    print(f"  - Completeness: {result['completeness']}%")
    print(f"  - Alignment: {result['alignment']}%")

# Test 3: Full analysis with document details
print("\n[TEST 3] Running full analysis...")
result = analyze(project_id=project_id, mode="full")

if "error" in result:
    print(f"✗ FAILED: {result['error']}")
    sys.exit(1)
else:
    print(f"✓ SUCCESS: Full analysis complete")
    print(f"  - Documents analyzed: {len(result['analysis']['systems_identified'])} systems identified")
    print(f"  - Gaps found: {len(result['analysis']['gaps'])}")
    print(f"  - Ambiguities found: {len(result['analysis']['ambiguities'])}")
    print(f"  - Conflicts found: {len(result['analysis']['conflicts'])}")
    print(f"  - Questions generated: {len(result['questions'])}")

# Test 4: Verify documents were loaded
print("\n[TEST 4] Verifying documents were loaded...")
state_manager = ProjectStateManager()
project = state_manager.get_project(project_id)

if project and project.documents:
    print(f"✓ SUCCESS: {len(project.documents)} documents loaded")
    for doc in project.documents[:3]:  # Show first 3
        print(f"  - {Path(doc.file_path).name} ({doc.doc_type.value})")
    if len(project.documents) > 3:
        print(f"  ... and {len(project.documents) - 3} more")
else:
    print("✗ FAILED: No documents found in project state")
    sys.exit(1)

# Test 5: Test error handling for non-existent project
print("\n[TEST 5] Testing error messages for invalid project...")
result = analyze(project_id="non-existent-project", mode="quick")

if "error" in result and "Available projects" in result["error"]:
    print(f"✓ SUCCESS: Got helpful error message")
    print(f"  Error: {result['error'][:100]}...")
else:
    print(f"✗ FAILED: Expected error with available projects list")
    print(f"  Got: {result}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED!")
print("=" * 60)
print("\nLocal file support is working correctly.")
print("You can now use analyze() directly without calling ingest() first.")

