#!/usr/bin/env python3
"""Test prepare_deliverable function directly."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import functions from main WITHOUT the MCP wrapper
import main
from core.state_manager import ProjectStateManager
from core.analyzer import DiscoveryAnalyzer

def test_prepare_deliverable():
    """Test the complete workflow."""
    print("=" * 80)
    print("TESTING PREPARE_DELIVERABLE WORKFLOW")
    print("=" * 80)
    
    project_id = "scenario-1-cozyhome"
    
    # Step 1: Ingest documents (call the underlying function)
    print("\nStep 1: Ingesting documents...")
    project_path = Path(main.TEST_DATA_PATH) / project_id
    
    state_manager = ProjectStateManager()
    project = state_manager.get_or_create(
        project_id=project_id,
        project_name="CozyHome",
        project_description="Home décor retailer"
    )
    
    project.documents = []
    doc_count = 0
    
    # Load emails
    emails_dir = project_path / "emails"
    if emails_dir.exists():
        for file in emails_dir.glob("*.txt"):
            doc = main._parse_email(file)
            project.add_document(doc)
            doc_count += 1
    
    # Load client docs
    client_docs_dir = project_path / "client-docs"
    if client_docs_dir.exists():
        for file in client_docs_dir.glob("*.txt"):
            doc = main._parse_client_doc(file)
            project.add_document(doc)
            doc_count += 1
    
    state_manager.update_project(project)
    print(f"✓ Loaded {doc_count} documents")
    
    # Step 2: Analyze
    print("\nStep 2: Analyzing project...")
    analyzer = DiscoveryAnalyzer()
    analysis = analyzer.analyze(project.documents, project.additional_context)
    project.update_analysis(analysis)
    state_manager.update_project(project)
    print(f"✓ Confidence: {round(analysis.overall_confidence, 1)}%")
    print(f"✓ Systems: {analysis.systems_identified}")
    
    # Step 3: Get template
    print("\nStep 3: Getting template...")
    template_result = main.get_template.__wrapped__("sow")  # Call unwrapped function
    if "error" in template_result:
        print(f"✗ Template error: {template_result['error']}")
        return
    print(f"✓ Template loaded: {template_result['template_file']}")
    
    # Step 4: Detect integration type
    print("\nStep 4: Detecting integration type...")
    integration_type = main._detect_integration_type(
        analysis.systems_identified,
        "\n".join([doc.content for doc in project.documents])
    )
    print(f"✓ Integration type: {integration_type}")
    
    # Step 5: Load mapping guide
    print("\nStep 5: Loading mapping guide...")
    mapping_guide_path = Path(main.TEMPLATES_PATH) / "PLACEHOLDER-MAPPING-GUIDE.md"
    if mapping_guide_path.exists():
        with open(mapping_guide_path, 'r') as f:
            mapping_guide = f.read()
        print(f"✓ Mapping guide loaded: {len(mapping_guide)} chars")
    else:
        print(f"✗ Mapping guide not found")
        mapping_guide = ""
    
    # Step 6: Build the result
    print("\nStep 6: Building deliverable response...")
    result = {
        "project_id": project_id,
        "template_type": "sow",
        "template": {
            "filename": template_result["template_file"],
            "content": template_result["content"]
        },
        "analysis": {
            "project_id": project.project_id,
            "project_name": project.project_name,
            "project_description": project.project_description,
            "analysis": analysis.to_dict(),
            "additional_context": project.additional_context
        },
        "integration_type": integration_type,
        "mapping_guide": mapping_guide,
        "instructions": (
            f"Use the template structure as a guide. Fill placeholders with data from "
            f"the analysis. Refer to the mapping_guide for how to map analysis fields "
            f"to template placeholders. Include only sections relevant to the "
            f"'{integration_type}' integration type. Output the completed document "
            f"to the user for copy/paste."
        ),
        "message": f"Ready to generate sow for {project.project_name}"
    }
    
    print("\n" + "=" * 80)
    print("✅ SUCCESS! Deliverable prepared")
    print("=" * 80)
    print(f"\nProject ID: {result['project_id']}")
    print(f"Template: {result['template']['filename']}")
    print(f"Integration Type: {result['integration_type']}")
    print(f"Template Content: {len(result['template']['content'])} chars")
    print(f"Analysis Data: {len(str(result['analysis']))} chars")
    print(f"Mapping Guide: {len(result['mapping_guide'])} chars")
    print(f"\n{result['message']}")
    
    return result

if __name__ == "__main__":
    try:
        test_prepare_deliverable()
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

