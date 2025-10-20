"""
Test suite for refactored MCP tools (5 core tools + query).
Tests the new storage-abstracted tool architecture.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import FastMCP instance and get tools directly
from main import mcp

# Get tool functions from the MCP instance
def call_tool(tool_name: str, **kwargs):
    """Helper to call MCP tools."""
    # Find the tool in mcp's registered tools
    tools = mcp.get_tools()
    for tool in tools:
        if tool.name == tool_name:
            # Get the actual function
            fn = tool.fn
            return fn(**kwargs)
    raise ValueError(f"Tool {tool_name} not found")

# Create wrapper functions
def manage_project(**kwargs):
    return call_tool("manage_project", **kwargs)

def ingest(**kwargs):
    return call_tool("ingest", **kwargs)

def analyze(**kwargs):
    return call_tool("analyze", **kwargs)

def update(**kwargs):
    return call_tool("update", **kwargs)

def generate(**kwargs):
    return call_tool("generate", **kwargs)

def query(**kwargs):
    return call_tool("query", **kwargs)


def test_manage_project():
    """Test manage_project tool."""
    print("\n" + "="*80)
    print("TEST: manage_project()")
    print("="*80)
    
    # List projects
    print("\n1. List all projects...")
    result = manage_project(action="list")
    print(f"✓ Found {result['count']} projects")
    assert result['count'] > 0, "Should find at least one project"
    
    # Get specific project
    print("\n2. Get project details...")
    result = manage_project(action="get", project_id="scenario-1-cozyhome")
    print(f"✓ Project: {result['project_id']}")
    print(f"  Path: {result['project_meta']['path']}")
    
    print("\n✅ manage_project() tests passed")


def test_ingest():
    """Test ingest tool."""
    print("\n" + "="*80)
    print("TEST: ingest()")
    print("="*80)
    
    # Ingest from local
    print("\n1. Ingest documents from local...")
    result = ingest(project_id="scenario-1-cozyhome", source="local")
    print(f"✓ Ingested {result['documents_loaded']} documents")
    print(f"  Total documents: {result['total_documents']}")
    assert result['documents_loaded'] > 0, "Should ingest at least one document"
    
    # Add text note
    print("\n2. Add text note...")
    result = ingest(
        project_id="scenario-1-cozyhome",
        source="text",
        location="Test note: Client confirmed QuickBooks Online integration",
        doc_type="note"
    )
    print(f"✓ Added text note")
    print(f"  Total documents now: {result['total_documents']}")
    
    print("\n✅ ingest() tests passed")


def test_analyze():
    """Test analyze tool."""
    print("\n" + "="*80)
    print("TEST: analyze()")
    print("="*80)
    
    # Full analysis
    print("\n1. Full analysis...")
    result = analyze(project_id="scenario-1-cozyhome", mode="full")
    print(f"✓ Confidence: {result['confidence']}%")
    print(f"  Gaps: {len(result['analysis']['gaps'])}")
    print(f"  Ambiguities: {len(result['analysis']['ambiguities'])}")
    print(f"  Systems: {', '.join(result['analysis']['systems_identified'])}")
    assert result['confidence'] > 0, "Confidence should be calculated"
    
    # Quick analysis
    print("\n2. Quick confidence check...")
    result = analyze(project_id="scenario-1-cozyhome", mode="quick")
    print(f"✓ Confidence: {result['confidence']}%")
    print(f"  Clarity: {result['clarity']}%")
    print(f"  Completeness: {result['completeness']}%")
    print(f"  Alignment: {result['alignment']}%")
    
    # Questions only
    print("\n3. Extract questions...")
    result = analyze(project_id="scenario-1-cozyhome", mode="questions_only")
    print(f"✓ Generated {result['questions_count']} questions")
    if result['questions']:
        print(f"  First question: {result['questions'][0]['question'][:60]}...")
    
    # Gaps only
    print("\n4. Gaps only...")
    result = analyze(project_id="scenario-1-cozyhome", mode="gaps_only")
    print(f"✓ Found {result['gaps_count']} gaps")
    
    print("\n✅ analyze() tests passed")


def test_update():
    """Test update tool."""
    print("\n" + "="*80)
    print("TEST: update()")
    print("="*80)
    
    # Add context
    print("\n1. Add context...")
    result = update(
        project_id="scenario-1-cozyhome",
        type="context",
        content="Client confirmed: QuickBooks Online is the source of truth for inventory"
    )
    print(f"✓ Context added")
    print(f"  Total updates: {result['updates_count']}")
    if result.get('new_confidence'):
        print(f"  New confidence: {result['new_confidence']}%")
    
    # Answer gap (simulate)
    print("\n2. Answer gap...")
    result = update(
        project_id="scenario-1-cozyhome",
        type="answer",
        content="Refunds create credit memos in QuickBooks. Sync daily at midnight.",
        target_id="gap_refund"
    )
    print(f"✓ Answer recorded")
    print(f"  Target: {result.get('target_id', 'N/A')}")
    
    print("\n✅ update() tests passed")


def test_generate():
    """Test generate tool."""
    print("\n" + "="*80)
    print("TEST: generate()")
    print("="*80)
    
    # Generate questions doc
    print("\n1. Generate questions document...")
    result = generate(
        project_id="scenario-1-cozyhome",
        output_type="questions_doc"
    )
    print(f"✓ Questions doc generated")
    print(f"  Questions: {result.get('questions_count', 'N/A')}")
    print(f"  Saved to: {result['saved_to']}")
    
    # Generate report
    print("\n2. Generate analysis report...")
    result = generate(
        project_id="scenario-1-cozyhome",
        output_type="report"
    )
    print(f"✓ Report generated")
    print(f"  Saved to: {result['saved_to']}")
    
    # Generate analysis snapshot
    print("\n3. Export analysis snapshot...")
    result = generate(
        project_id="scenario-1-cozyhome",
        output_type="analysis_snapshot",
        format="json"
    )
    print(f"✓ Snapshot exported")
    print(f"  Format: {result['format']}")
    print(f"  Saved to: {result['saved_to']}")
    
    print("\n✅ generate() tests passed")


def test_query():
    """Test query tool."""
    print("\n" + "="*80)
    print("TEST: query()")
    print("="*80)
    
    # Search for specific info
    print("\n1. Query: 'What did the client say about QuickBooks?'")
    result = query(
        project_id="scenario-1-cozyhome",
        question="What did the client say about QuickBooks?"
    )
    print(f"✓ Found {result['results_count']} relevant results")
    if result['document_results']:
        print(f"  Top result from: {result['document_results'][0]['document']}")
    
    # Query for stakeholders
    print("\n2. Query: 'Who are the stakeholders?'")
    result = query(
        project_id="scenario-1-cozyhome",
        question="Who are the stakeholders?"
    )
    print(f"✓ Found {result['results_count']} results")
    if result['analysis_insights']:
        for insight in result['analysis_insights']:
            if insight['type'] == 'stakeholders':
                print(f"  Stakeholders: {', '.join(insight['data'][:3])}...")
    
    # Query for pain points
    print("\n3. Query: 'What are the main pain points?'")
    result = query(
        project_id="scenario-1-cozyhome",
        question="What are the main pain points?"
    )
    print(f"✓ Query completed")
    if result['analysis_insights']:
        for insight in result['analysis_insights']:
            if insight['type'] == 'pain_points' and insight['data']:
                print(f"  Pain point: {insight['data'][0][:60]}...")
    
    print("\n✅ query() tests passed")


def test_backward_compatibility():
    """Test that deprecated tools still work."""
    print("\n" + "="*80)
    print("TEST: Backward Compatibility (Deprecated Tools)")
    print("="*80)
    
    print("\n1. find_project_folders() [deprecated]...")
    result = call_tool("find_project_folders")
    print(f"✓ Works (found {result['count']} projects)")
    
    print("\n2. ingest_documents() [deprecated]...")
    result = call_tool("ingest_documents", project_id="scenario-1-cozyhome")
    print(f"✓ Works (loaded {result['documents_loaded']} documents)")
    
    print("\n3. analyze_discovery() [deprecated]...")
    result = call_tool("analyze_discovery", project_id="scenario-1-cozyhome")
    print(f"✓ Works (confidence: {result['summary']['confidence_score']}%)")
    
    print("\n✅ Backward compatibility tests passed")


def test_storage_abstraction():
    """Test that storage layer is working."""
    print("\n" + "="*80)
    print("TEST: Storage Abstraction")
    print("="*80)
    
    from storage import get_storage_provider, FolderType
    
    print("\n1. Get local storage provider...")
    storage = get_storage_provider("local", base_path=str(Path(__file__).parent.parent / "test-data"))
    print(f"✓ Storage provider initialized")
    
    print("\n2. List projects via storage...")
    projects = storage.list_projects()
    print(f"✓ Found {len(projects)} projects")
    
    print("\n3. Get project config...")
    config = storage.get_config("scenario-1-cozyhome")
    print(f"✓ Config loaded")
    print(f"  Confidence threshold: {config.get('confidence_threshold', 'N/A')}")
    
    print("\n✅ Storage abstraction tests passed")


def run_all_tests():
    """Run all test suites."""
    print("\n" + "="*80)
    print("REFACTORED MCP TOOLS TEST SUITE")
    print("Testing: 5 core tools + query + storage abstraction")
    print("="*80)
    
    try:
        test_manage_project()
        test_ingest()
        test_analyze()
        test_update()
        test_generate()
        test_query()
        test_backward_compatibility()
        test_storage_abstraction()
        
        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80)
        print("\nRefactored toolkit is working correctly!")
        print("- 6 new tools functional")
        print("- Storage abstraction working")
        print("- Backward compatibility maintained")
        print("- Ready for Google Drive integration")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    run_all_tests()

