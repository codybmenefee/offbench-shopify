"""
Integration tests for Convex sync functionality.

Run these tests after setting up Convex and configuring environment variables.
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from datetime import datetime
from models.project_state import ProjectState
from models.document import Document, DocumentType
from models.analysis import AnalysisResult, Gap, Ambiguity, Conflict, GapCategory, Priority
from persistence import ConvexSync, ConvexClient
from config import config


def test_convex_connection():
    """Test basic Convex connection."""
    print("\n=== Testing Convex Connection ===")
    
    if not config.is_convex_enabled():
        print("❌ Convex not configured. Set CONVEX_DEPLOYMENT_URL and CONVEX_ADMIN_KEY")
        return False
    
    try:
        client = ConvexClient()
        print(f"✅ Connected to Convex: {config.CONVEX_DEPLOYMENT_URL}")
        client.close()
        return True
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False


def test_project_sync():
    """Test syncing project metadata."""
    print("\n=== Testing Project Metadata Sync ===")
    
    try:
        sync = ConvexSync()
        
        # Create test project
        project = ProjectState(
            project_id="test-integration-project",
            project_name="Integration Test Project",
            project_description="Test project for Convex integration"
        )
        
        # Add mock analysis
        analysis = AnalysisResult()
        analysis.overall_confidence = 75.5
        analysis.clarity_score = 80.0
        analysis.completeness_score = 70.0
        analysis.alignment_score = 76.5
        analysis.client_name = "Test Client"
        project.update_analysis(analysis)
        
        # Sync to Convex
        convex_id = sync.sync_project_metadata(project)
        print(f"✅ Project synced. Convex ID: {convex_id}")
        
        sync.close()
        return True
    except Exception as e:
        print(f"❌ Project sync failed: {e}")
        return False


def test_analysis_sync():
    """Test syncing analysis results (gaps, conflicts, ambiguities)."""
    print("\n=== Testing Analysis Sync ===")
    
    try:
        sync = ConvexSync()
        
        # Create test project
        project = ProjectState(
            project_id="test-analysis-project",
            project_name="Analysis Test Project"
        )
        
        # Create mock analysis with gaps, conflicts, ambiguities
        analysis = AnalysisResult()
        
        # Add gaps
        gap1 = Gap(
            category=GapCategory.BUSINESS_RULES,
            description="Missing refund policy details",
            impact="Could lead to customer disputes",
            priority=Priority.HIGH,
            suggested_question="What is the refund policy for returns after 30 days?"
        )
        gap2 = Gap(
            category=GapCategory.TECHNICAL_CONSTRAINTS,
            description="No performance requirements specified",
            impact="Could result in slow system",
            priority=Priority.MEDIUM,
            suggested_question="What are the expected response time requirements?"
        )
        analysis.gaps = [gap1, gap2]
        
        # Add conflicts
        conflict1 = Conflict(
            topic="Payment Processing",
            conflicting_statements=[
                "We need to support PayPal",
                "We only want credit card processing"
            ],
            sources=["email-01", "call-transcript-02"],
            resolution_needed="Clarify which payment methods to support",
            priority=Priority.HIGH
        )
        analysis.conflicts = [conflict1]
        
        # Add ambiguities
        ambiguity1 = Ambiguity(
            term="fast checkout",
            context="Client mentioned wanting 'fast checkout' multiple times",
            clarification_needed="What does 'fast' mean? 2 clicks? Under 30 seconds?",
            priority=Priority.MEDIUM
        )
        analysis.ambiguities = [ambiguity1]
        
        analysis.calculate_confidence()
        project.update_analysis(analysis)
        
        # Sync project first
        convex_id = sync.sync_project_metadata(project)
        print(f"✅ Project created: {convex_id}")
        
        # Sync analysis
        gap_ids = sync.sync_gaps(convex_id, analysis.gaps)
        print(f"✅ Synced {len(gap_ids)} gaps")
        
        conflict_ids = sync.sync_conflicts(convex_id, analysis.conflicts)
        print(f"✅ Synced {len(conflict_ids)} conflicts")
        
        ambiguity_ids = sync.sync_ambiguities(convex_id, analysis.ambiguities)
        print(f"✅ Synced {len(ambiguity_ids)} ambiguities")
        
        sync.close()
        return True
    except Exception as e:
        print(f"❌ Analysis sync failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_document_sync():
    """Test syncing document metadata."""
    print("\n=== Testing Document Sync ===")
    
    try:
        sync = ConvexSync()
        
        # Create test project with documents
        project = ProjectState(
            project_id="test-docs-project",
            project_name="Documents Test Project"
        )
        
        # Add mock documents
        doc1 = Document(
            file_path="emails/inquiry.txt",
            content="Sample email content",
            doc_type=DocumentType.EMAIL,
            metadata={"from": "client@example.com"},
            date=datetime.now()
        )
        doc2 = Document(
            file_path="transcripts/discovery-call.txt",
            content="Sample transcript",
            doc_type=DocumentType.TRANSCRIPT,
            metadata={"duration": "45 minutes"},
            date=datetime.now()
        )
        project.add_document(doc1)
        project.add_document(doc2)
        
        # Add minimal analysis for project creation
        analysis = AnalysisResult()
        analysis.calculate_confidence()
        project.update_analysis(analysis)
        
        # Sync to Convex
        convex_id = sync.sync_project_metadata(project)
        doc_ids = sync.sync_documents(convex_id, project)
        
        print(f"✅ Synced {len(doc_ids)} documents")
        
        sync.close()
        return True
    except Exception as e:
        print(f"❌ Document sync failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_project_sync():
    """Test full project sync with all components."""
    print("\n=== Testing Full Project Sync ===")
    
    try:
        sync = ConvexSync()
        
        # Create complete test project
        project = ProjectState(
            project_id="test-full-project",
            project_name="Complete Test Project",
            project_description="Full integration test"
        )
        
        # Add documents
        doc = Document(
            file_path="test.txt",
            content="Test content",
            doc_type=DocumentType.NOTES,
            date=datetime.now()
        )
        project.add_document(doc)
        
        # Add complete analysis
        analysis = AnalysisResult()
        analysis.gaps = [
            Gap(
                category=GapCategory.SUCCESS_CRITERIA,
                description="Missing success metrics",
                impact="Can't measure project success",
                priority=Priority.HIGH
            )
        ]
        analysis.conflicts = [
            Conflict(
                topic="Timeline",
                conflicting_statements=["Need it in 2 weeks", "Standard is 6 weeks"],
                sources=["email", "contract"],
                resolution_needed="Agree on realistic timeline",
                priority=Priority.HIGH
            )
        ]
        analysis.ambiguities = [
            Ambiguity(
                term="scalable",
                context="Client wants a scalable solution",
                clarification_needed="How many users? What growth rate?",
                priority=Priority.MEDIUM
            )
        ]
        analysis.calculate_confidence()
        project.update_analysis(analysis)
        
        # Use full sync method
        results = sync.sync_full_project(project)
        
        print(f"✅ Full sync completed:")
        print(f"   - Project ID: {results['project_id']}")
        print(f"   - Gaps: {len(results.get('gaps', []))}")
        print(f"   - Conflicts: {len(results.get('conflicts', []))}")
        print(f"   - Ambiguities: {len(results.get('ambiguities', []))}")
        print(f"   - Documents: {len(results.get('documents', []))}")
        
        sync.close()
        return True
    except Exception as e:
        print(f"❌ Full sync failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_event_logging():
    """Test logging context events."""
    print("\n=== Testing Event Logging ===")
    
    try:
        sync = ConvexSync()
        
        # Create test project
        project = ProjectState(
            project_id="test-events-project",
            project_name="Events Test Project"
        )
        analysis = AnalysisResult()
        analysis.calculate_confidence()
        project.update_analysis(analysis)
        
        convex_id = sync.sync_project_metadata(project)
        
        # Log test event
        event_id = sync.log_event(
            convex_id,
            "analysis_completed",
            "Test analysis completed successfully",
            {"test": True, "confidence": 85.5}
        )
        
        print(f"✅ Event logged: {event_id}")
        
        sync.close()
        return True
    except Exception as e:
        print(f"❌ Event logging failed: {e}")
        return False


def main():
    """Run all integration tests."""
    print("=" * 60)
    print("Convex Integration Test Suite")
    print("=" * 60)
    
    if not config.is_convex_enabled():
        print("\n❌ ERROR: Convex not configured!")
        print("\nSet up environment variable:")
        print("  CONVEX_DEPLOYMENT_URL=https://your-deployment.convex.cloud")
        print("\nSee CONVEX_SETUP.md for details.")
        return False
    
    print(f"\nConnecting to: {config.CONVEX_DEPLOYMENT_URL}")
    
    tests = [
        ("Convex Connection", test_convex_connection),
        ("Project Sync", test_project_sync),
        ("Analysis Sync", test_analysis_sync),
        ("Document Sync", test_document_sync),
        ("Full Project Sync", test_full_project_sync),
        ("Event Logging", test_event_logging),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ {name} raised exception: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Convex integration is working.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

