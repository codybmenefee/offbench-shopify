"""
Test script for discovery tools.
Run this to validate the implementation with scenario-1-cozyhome.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from tools.discovery_tools import (
    _parse_email, _parse_transcript, _parse_client_doc,
    TEST_DATA_PATH
)
from core.state_manager import ProjectStateManager
from core.analyzer import DiscoveryAnalyzer
from core.template_filler import TemplateFiller
from models.document import Document


def test_document_parsing():
    """Test document parsing functions."""
    print("=" * 80)
    print("TEST 1: Document Parsing")
    print("=" * 80)
    
    # Test email parsing
    email_path = Path(TEST_DATA_PATH) / "scenario-1-cozyhome/emails/01-initial-inquiry.txt"
    if email_path.exists():
        doc = _parse_email(email_path)
        print(f"\n✓ Email parsed: {doc.subject}")
        print(f"  From: {doc.participants[0] if doc.participants else 'Unknown'}")
        print(f"  Type: {doc.doc_type.value}")
        print(f"  Content length: {len(doc.content)} chars")
    else:
        print(f"\n✗ Email not found: {email_path}")
    
    print("\n" + "=" * 80)


def test_project_ingestion():
    """Test full project ingestion."""
    print("=" * 80)
    print("TEST 2: Project Ingestion")
    print("=" * 80)
    
    project_id = "scenario-1-cozyhome"
    project_path = Path(TEST_DATA_PATH) / project_id
    
    if not project_path.exists():
        print(f"\n✗ Project path not found: {project_path}")
        return None
    
    # Create project state
    state_manager = ProjectStateManager()
    project = state_manager.get_or_create(
        project_id=project_id,
        project_name="CozyHome",
        project_description="Shopify + QuickBooks integration"
    )
    
    # Load documents
    doc_count = 0
    
    # Load emails
    emails_dir = project_path / "emails"
    if emails_dir.exists():
        for file in emails_dir.glob("*.txt"):
            doc = _parse_email(file)
            project.add_document(doc)
            doc_count += 1
    
    # Load client docs
    client_docs_dir = project_path / "client-docs"
    if client_docs_dir.exists():
        for file in client_docs_dir.glob("*.txt"):
            doc = _parse_client_doc(file)
            project.add_document(doc)
            doc_count += 1
    
    print(f"\n✓ Loaded {doc_count} documents for {project.project_name}")
    print(f"  Project ID: {project.project_id}")
    print(f"  Documents: {len(project.documents)}")
    
    state_manager.update_project(project)
    
    print("\n" + "=" * 80)
    return project


def test_analysis():
    """Test discovery analysis."""
    print("=" * 80)
    print("TEST 3: Discovery Analysis")
    print("=" * 80)
    
    state_manager = ProjectStateManager()
    project = state_manager.get_project("scenario-1-cozyhome")
    
    if not project:
        print("\n✗ Project not found. Run test_project_ingestion first.")
        return None
    
    if not project.documents:
        print("\n✗ No documents in project")
        return None
    
    # Run analysis
    analyzer = DiscoveryAnalyzer()
    analysis = analyzer.analyze(project.documents, project.additional_context)
    
    print(f"\n✓ Analysis complete")
    print(f"\n  Confidence Score: {round(analysis.overall_confidence, 1)}%")
    print(f"    - Clarity: {round(analysis.clarity_score, 1)}%")
    print(f"    - Completeness: {round(analysis.completeness_score, 1)}%")
    print(f"    - Alignment: {round(analysis.alignment_score, 1)}%")
    
    print(f"\n  Systems Identified: {', '.join(analysis.systems_identified)}")
    print(f"  Client Name: {analysis.client_name}")
    
    print(f"\n  Gaps Found: {len(analysis.gaps)}")
    for i, gap in enumerate(analysis.gaps[:3], 1):
        print(f"    {i}. [{gap.priority.value.upper()}] {gap.description}")
    
    print(f"\n  Ambiguities Found: {len(analysis.ambiguities)}")
    for i, ambiguity in enumerate(analysis.ambiguities[:3], 1):
        print(f"    {i}. '{ambiguity.term}' - {ambiguity.clarification_needed}")
    
    print(f"\n  Conflicts Found: {len(analysis.conflicts)}")
    for i, conflict in enumerate(analysis.conflicts, 1):
        print(f"    {i}. {conflict.topic}")
    
    # Update project
    project.update_analysis(analysis)
    state_manager.update_project(project)
    
    print("\n" + "=" * 80)
    return analysis


def test_template_filling():
    """Test template filling."""
    print("=" * 80)
    print("TEST 4: Template Filling")
    print("=" * 80)
    
    state_manager = ProjectStateManager()
    project = state_manager.get_project("scenario-1-cozyhome")
    
    if not project or not project.analysis:
        print("\n✗ Project or analysis not found")
        return
    
    # Load SOW template
    template_path = Path("/Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify/templates/client-facing-sow.md")
    if not template_path.exists():
        print(f"\n✗ Template not found: {template_path}")
        return
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Fill template
    filler = TemplateFiller()
    filled = filler.fill(template, project)
    
    # Count replacements
    original_placeholders = template.count("[")
    remaining_placeholders = filled.count("[NEEDS_CLARIFICATION:")
    filled_placeholders = original_placeholders - remaining_placeholders
    
    print(f"\n✓ Template filled")
    print(f"  Original placeholders: ~{original_placeholders}")
    print(f"  Filled automatically: ~{filled_placeholders}")
    print(f"  Need clarification: {remaining_placeholders}")
    
    # Show sample output
    print(f"\n  Sample output (first 500 chars):")
    print("  " + "-" * 76)
    for line in filled[:500].split('\n'):
        print(f"  {line}")
    print("  " + "-" * 76)
    
    print("\n" + "=" * 80)


def test_context_update():
    """Test adding context and recalculating."""
    print("=" * 80)
    print("TEST 5: Context Update & Recalculation")
    print("=" * 80)
    
    state_manager = ProjectStateManager()
    project = state_manager.get_project("scenario-1-cozyhome")
    
    if not project or not project.analysis:
        print("\n✗ Project or analysis not found")
        return
    
    previous_confidence = project.analysis.overall_confidence
    print(f"\n  Previous confidence: {round(previous_confidence, 1)}%")
    
    # Add context
    new_context = """
    Based on follow-up discussion:
    - Refunds should sync to QuickBooks as credit memos within 24 hours
    - QuickBooks is the source of truth for inventory
    - Sync frequency should be every 15 minutes via polling (webhooks as future enhancement)
    - Tax calculation happens in Shopify and syncs to QuickBooks
    - Error notifications should go to both Sarah and David via email
    """
    
    project.add_context(new_context)
    print(f"\n✓ Added context ({len(new_context)} chars)")
    
    # Re-analyze
    analyzer = DiscoveryAnalyzer()
    new_analysis = analyzer.analyze(project.documents, project.additional_context)
    project.update_analysis(new_analysis)
    state_manager.update_project(project)
    
    improvement = new_analysis.overall_confidence - previous_confidence
    
    print(f"\n  New confidence: {round(new_analysis.overall_confidence, 1)}%")
    print(f"  Improvement: {round(improvement, 1)}%")
    print(f"  Gaps remaining: {len(new_analysis.gaps)}")
    
    print("\n" + "=" * 80)


def run_all_tests():
    """Run all tests in sequence."""
    print("\n")
    print("*" * 80)
    print(" DISCOVERY TOOLS TEST SUITE")
    print("*" * 80)
    print("\n")
    
    try:
        test_document_parsing()
        project = test_project_ingestion()
        if project:
            analysis = test_analysis()
            if analysis:
                test_template_filling()
                test_context_update()
        
        print("\n")
        print("*" * 80)
        print(" ALL TESTS COMPLETED")
        print("*" * 80)
        print("\n")
        
        # Final summary
        state_manager = ProjectStateManager()
        project = state_manager.get_project("scenario-1-cozyhome")
        if project and project.analysis:
            print("FINAL PROJECT STATE:")
            print(f"  Project: {project.project_name}")
            print(f"  Documents: {len(project.documents)}")
            print(f"  Confidence: {round(project.analysis.overall_confidence, 1)}%")
            print(f"  Confidence history: {len(project.confidence_history)} snapshots")
            if len(project.confidence_history) > 1:
                improvement = project.get_confidence_improvement()
                print(f"  Total improvement: {round(improvement, 1)}%")
            print()
    
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()

