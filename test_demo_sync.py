#!/usr/bin/env python3
"""
Test script to verify demo mode sync works correctly after the fix.
Run this after restarting the MCP server.
"""

import os
import sys

# Ensure we're in demo mode
os.environ["DEMO_MODE"] = "true"

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "mcp", "src"))

from persistence.convex_sync import ConvexSync
from core.state_manager import ProjectStateManager
from config import config

def test_demo_sync():
    """Test that sync works with demo mode."""
    
    print("=" * 80)
    print("DEMO MODE SYNC TEST")
    print("=" * 80)
    
    # Verify demo mode is enabled
    print(f"\n1. Demo Mode Check:")
    print(f"   DEMO_MODE: {config.DEMO_MODE}")
    print(f"   Demo Context: {config.get_demo_context()}")
    
    if not config.DEMO_MODE:
        print("   ❌ ERROR: Demo mode is not enabled!")
        print("   Run: export DEMO_MODE=true")
        return False
    
    # Verify Convex is configured
    print(f"\n2. Convex Configuration:")
    print(f"   Convex Enabled: {config.is_convex_enabled()}")
    print(f"   Deployment URL: {config.CONVEX_DEPLOYMENT_URL[:50]}..." if config.CONVEX_DEPLOYMENT_URL else "   Deployment URL: Not set")
    
    if not config.is_convex_enabled():
        print("   ❌ ERROR: Convex is not configured!")
        return False
    
    # Get project from state manager
    print(f"\n3. Loading Project:")
    state_manager = ProjectStateManager()
    project = state_manager.get_project("scenario-6-enterprise-full")
    
    if not project:
        print("   ❌ ERROR: Project not found!")
        print("   Run: ingest(project_id='scenario-6-enterprise-full', source='local')")
        print("   Then: analyze(project_id='scenario-6-enterprise-full', mode='full')")
        return False
    
    print(f"   ✅ Project loaded: {project.project_name}")
    print(f"   Documents: {len(project.documents)}")
    print(f"   Analysis exists: {project.analysis is not None}")
    
    if project.analysis:
        print(f"   Confidence: {project.analysis.overall_confidence}")
        print(f"   Gaps: {len(project.analysis.gaps)}")
        print(f"   Conflicts: {len(project.analysis.conflicts)}")
        print(f"   Ambiguities: {len(project.analysis.ambiguities)}")
    
    # Test sync
    print(f"\n4. Testing Sync:")
    try:
        sync = ConvexSync()
        
        # Test project creation
        print(f"   Creating/finding project in Convex...")
        convex_project_id = sync.sync_project_metadata(project)
        
        if not convex_project_id:
            print(f"   ❌ ERROR: sync_project_metadata returned None!")
            return False
        
        print(f"   ✅ Project synced successfully!")
        print(f"   Convex Project ID: {convex_project_id}")
        
        # Test full sync
        if project.analysis:
            print(f"\n   Syncing analysis data...")
            results = sync.sync_full_project(project)
            print(f"   ✅ Full sync complete!")
            print(f"   Results: {results}")
        
        sync.close()
        
    except Exception as e:
        print(f"   ❌ ERROR during sync: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED!")
    print("=" * 80)
    print("\nNext steps:")
    print("1. Open Convex Dashboard: https://dashboard.convex.dev")
    print("2. Check projects table for scenarioId='scenario-6-enterprise-full'")
    print("3. Verify orgId='demo-org'")
    print("4. Check conflicts, ambiguities, gaps, documents, questions tables")
    print("5. Open your portal frontend and verify the project appears")
    print("=" * 80)
    
    return True

if __name__ == "__main__":
    success = test_demo_sync()
    sys.exit(0 if success else 1)

