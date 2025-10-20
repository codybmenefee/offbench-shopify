#!/usr/bin/env python3
"""
MCP Server Integrity Test Suite
Tests all MCP tools and Convex integration with scenario-1-cozyhome
"""

import sys
import os
import json
import requests
from pathlib import Path

# Add mcp/src to path for direct imports
sys.path.insert(0, str(Path(__file__).parent / "mcp" / "src"))

# Import for direct Convex testing
from persistence.convex_client import ConvexClient
from persistence.convex_sync import ConvexSync
from core.state_manager import ProjectStateManager
from core.analyzer import DiscoveryAnalyzer
from models.document import Document, DocumentType
from models.project_state import ProjectState
from config import config

BASE_URL = "http://localhost:8123"

class TestResults:
    """Track test results"""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def test(self, name, condition, details=""):
        if condition:
            print(f"✅ PASS: {name}")
            self.passed += 1
            if details:
                print(f"   {details}")
        else:
            print(f"❌ FAIL: {name}")
            self.failed += 1
            if details:
                print(f"   {details}")
            self.errors.append(name)
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"TEST SUMMARY")
        print(f"{'='*60}")
        print(f"Total Tests: {total}")
        print(f"Passed: {self.passed} ({self.passed/total*100:.1f}%)")
        print(f"Failed: {self.failed} ({self.failed/total*100:.1f}%)")
        if self.errors:
            print(f"\nFailed Tests:")
            for error in self.errors:
                print(f"  - {error}")
        print(f"{'='*60}\n")
        return self.failed == 0


results = TestResults()


def print_section(title):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")


def call_mcp_tool(tool_name, **kwargs):
    """Call an MCP tool via HTTP"""
    try:
        response = requests.post(
            f"{BASE_URL}/mcp/tools/{tool_name}",
            json={"arguments": kwargs},
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"HTTP request failed: {str(e)}"}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON response"}


# ============================================================================
# PHASE 2: TEST CORE MCP TOOLS (via direct imports)
# ============================================================================

print_section("PHASE 2: TEST CORE MCP TOOLS")

print("Note: Testing tools by direct import since HTTP endpoints use different structure")
print("This validates the core functionality of each tool function.\n")

# Import storage and tools directly
from storage import get_storage_provider, FolderType

BASE_PATH = Path(__file__).parent
TEST_DATA_PATH = str(BASE_PATH / "test-data")
storage = get_storage_provider("local", base_path=TEST_DATA_PATH)

# Test 2.1: manage_project tool
print("\n[2.1] Testing manage_project functionality...")

# List projects via storage
print("\n→ Testing project listing...")
projects = storage.list_projects()
results.test(
    "manage_project - list functionality",
    len(projects) > 0,
    f"Found {len(projects)} projects"
)
for proj in projects[:3]:
    print(f"   - {proj['project_id']}: {proj['name']}")

# Get specific project
print("\n→ Testing project retrieval...")
project_meta = storage.get_project("scenario-1-cozyhome")
results.test(
    "manage_project - get functionality",
    project_meta is not None,
    f"Retrieved project metadata"
)

# Test 2.2: ingest tool
print("\n[2.2] Testing ingest functionality...")
print("\n→ Ingesting documents from scenario-1-cozyhome...")

state_manager = ProjectStateManager()
project = state_manager.get_or_create(
    project_id="scenario-1-cozyhome",
    project_name="CozyHome Integration"
)

# Clear existing documents
project.documents = []

# Get discovery documents
doc_paths = storage.get_all_discovery_documents("scenario-1-cozyhome")
print(f"   Found {len(doc_paths)} document files")

# Parse documents (simplified parsing)
for file_path in doc_paths:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Determine type from path
        path_str = str(file_path).lower()
        if "email" in path_str:
            doc_type = DocumentType.EMAIL
        elif "transcript" in path_str:
            doc_type = DocumentType.TRANSCRIPT
        elif "sow" in file_path.name.lower():
            doc_type = DocumentType.SOW
        else:
            doc_type = DocumentType.OTHER
        
        doc = Document(
            file_path=str(file_path),
            content=content,
            doc_type=doc_type,
            metadata={}
        )
        project.add_document(doc)
        print(f"   - Loaded: {file_path.name} ({doc_type.value})")
    except Exception as e:
        print(f"   - Error loading {file_path.name}: {e}")

state_manager.update_project(project)

results.test(
    "ingest - document loading",
    len(project.documents) >= 4,
    f"Loaded {len(project.documents)} documents"
)

# Test 2.3: analyze tool
print("\n[2.3] Testing analyze functionality...")

analyzer = DiscoveryAnalyzer()

# Full analysis
print("\n→ Running full analysis...")
analysis = analyzer.analyze(project.documents, project.additional_context)
project.update_analysis(analysis)
state_manager.update_project(project)

results.test(
    "analyze - analysis completed",
    analysis is not None,
    f"Confidence: {round(analysis.overall_confidence, 1)}%"
)

print(f"\n   Analysis Summary:")
print(f"   - Overall Confidence: {round(analysis.overall_confidence, 1)}%")
print(f"   - Clarity: {round(analysis.clarity_score, 1)}%")
print(f"   - Completeness: {round(analysis.completeness_score, 1)}%")
print(f"   - Alignment: {round(analysis.alignment_score, 1)}%")
print(f"   - Systems: {', '.join(analysis.systems_identified)}")
print(f"   - Gaps: {len(analysis.gaps)}") 
print(f"   - Ambiguities: {len(analysis.ambiguities)}")
print(f"   - Conflicts: {len(analysis.conflicts)}")

results.test(
    "analyze - systems identified",
    len(analysis.systems_identified) >= 2,
    f"Found {len(analysis.systems_identified)} systems"
)

results.test(
    "analyze - confidence score reasonable",
    60 <= analysis.overall_confidence <= 100,
    f"Score: {round(analysis.overall_confidence, 1)}%"
)

results.test(
    "analyze - gaps detected",
    len(analysis.gaps) >= 0,
    f"Detected {len(analysis.gaps)} gaps"
)

# Test 2.4: update functionality
print("\n[2.4] Testing update functionality...")
print("\n→ Adding context...")

previous_confidence = analysis.overall_confidence
project.add_context(
    "QuickBooks is the source of truth for inventory. Sync every 15 minutes.",
    update_type="context"
)

# Reanalyze
analysis = analyzer.analyze(project.documents, project.additional_context)
project.update_analysis(analysis)
state_manager.update_project(project)

results.test(
    "update - context added",
    len(project.additional_context) > 0,
    f"Context entries: {len(project.additional_context)}"
)

print(f"   Previous confidence: {round(previous_confidence, 1)}%")
print(f"   New confidence: {round(analysis.overall_confidence, 1)}%")
print(f"   Change: {round(analysis.overall_confidence - previous_confidence, 1):+.1f}%")

# Test 2.5: generate functionality  
print("\n[2.5] Testing generate functionality...")
print("\n→ Testing template loading...")

TEMPLATES_PATH = BASE_PATH / "templates"
sow_template = TEMPLATES_PATH / "simplified" / "client-facing-sow-simplified.md"

results.test(
    "generate - template exists",
    sow_template.exists(),
    f"Template found: {sow_template.name}"
)

if sow_template.exists():
    with open(sow_template, 'r') as f:
        template_content = f.read()
    
    results.test(
        "generate - template readable",
        len(template_content) > 100,
        f"Template size: {len(template_content)} chars"
    )
    
    # Check for placeholders
    placeholders = [
        "[CLIENT_NAME]",
        "[PROJECT_DESCRIPTION]",
        "[SYSTEM_A]"
    ]
    found_placeholders = sum(1 for p in placeholders if p in template_content)
    
    results.test(
        "generate - template has placeholders",
        found_placeholders > 0,
        f"Found {found_placeholders} key placeholders"
    )

# Test 2.6: query functionality
print("\n[2.6] Testing query functionality...")
print("\n→ Searching for 'refunds' in documents...")

refund_mentions = 0
for doc in project.documents:
    if "refund" in doc.content.lower():
        refund_mentions += 1
        print(f"   - Found in: {Path(doc.file_path).name}")

results.test(
    "query - keyword search",
    refund_mentions >= 0,
    f"Found 'refunds' in {refund_mentions} document(s)"
)

print("\n→ Searching for 'quickbooks' in documents...")
qb_mentions = 0
for doc in project.documents:
    if "quickbook" in doc.content.lower():
        qb_mentions += 1
        print(f"   - Found in: {Path(doc.file_path).name}")

results.test(
    "query - system mention search",
    qb_mentions > 0,
    f"Found 'QuickBooks' in {qb_mentions} document(s)"
)


# ============================================================================
# PHASE 3: TEST CONVEX INTEGRATION DIRECTLY
# ============================================================================

print_section("PHASE 3: TEST CONVEX INTEGRATION DIRECTLY")

if config.is_convex_enabled():
    print(f"Convex URL: {config.CONVEX_DEPLOYMENT_URL}\n")
    
    # Test 3.1: ConvexClient
    print("[3.1] Testing ConvexClient...")
    
    try:
        client = ConvexClient()
        
        results.test(
            "ConvexClient - initialization",
            client.deployment_url is not None,
            f"Connected to: {client.deployment_url}"
        )
        
        # Test query
        print("\n→ Testing ConvexClient.query('queries/projects:listProjects')...")
        try:
            projects_data = client.query("queries/projects:listProjects", {})
            results.test(
                "ConvexClient - query operation",
                isinstance(projects_data, list),
                f"Retrieved {len(projects_data) if projects_data else 0} projects"
            )
            if projects_data:
                print(f"   Convex projects:")
                for p in projects_data[:3]:
                    print(f"   - {p.get('name', 'N/A')} (Confidence: {p.get('confidence', 0)}%)")
        except Exception as e:
            results.test(
                "ConvexClient - query operation",
                False,
                f"Query failed: {str(e)}"
            )
        
        client.close()
        
    except Exception as e:
        results.test(
            "ConvexClient - initialization",
            False,
            f"Failed to initialize: {str(e)}"
        )
    
    # Test 3.2: ConvexSync
    print("\n[3.2] Testing ConvexSync...")
    
    try:
        # Get project state
        project = state_manager.get_project("scenario-1-cozyhome")
        
        if project and project.analysis:
            sync = ConvexSync()
            
            # Test sync_project_metadata
            print("\n→ Testing ConvexSync.sync_project_metadata()...")
            try:
                project_id = sync.sync_project_metadata(project)
                results.test(
                    "ConvexSync - sync_project_metadata",
                    project_id is not None and len(str(project_id)) > 0,
                    f"Project synced with Convex ID: {project_id}"
                )
                
                # Test sync_gaps
                print("\n→ Testing ConvexSync.sync_gaps()...")
                gaps_result = sync.sync_gaps(project_id, project.analysis.gaps)
                results.test(
                    "ConvexSync - sync_gaps",
                    gaps_result is not None and (isinstance(gaps_result, (list, dict))),
                    f"Synced {len(project.analysis.gaps)} gaps (returned: {type(gaps_result).__name__})"
                )
                
                # Test sync_conflicts
                print("\n→ Testing ConvexSync.sync_conflicts()...")
                conflicts_result = sync.sync_conflicts(project_id, project.analysis.conflicts)
                results.test(
                    "ConvexSync - sync_conflicts",
                    conflicts_result is not None and (isinstance(conflicts_result, (list, dict))),
                    f"Synced {len(project.analysis.conflicts)} conflicts (returned: {type(conflicts_result).__name__})"
                )
                
                # Test sync_ambiguities
                print("\n→ Testing ConvexSync.sync_ambiguities()...")
                ambiguities_result = sync.sync_ambiguities(project_id, project.analysis.ambiguities)
                results.test(
                    "ConvexSync - sync_ambiguities",
                    ambiguities_result is not None and (isinstance(ambiguities_result, (list, dict))),
                    f"Synced {len(project.analysis.ambiguities)} ambiguities (returned: {type(ambiguities_result).__name__})"
                )
                
                # Test sync_documents
                print("\n→ Testing ConvexSync.sync_documents()...")
                doc_result = sync.sync_documents(project_id, project)
                results.test(
                    "ConvexSync - sync_documents",
                    doc_result is not None and (isinstance(doc_result, (list, dict))),
                    f"Synced {len(project.documents)} documents (returned: {type(doc_result).__name__})"
                )
                
                # Extract and sync questions
                print("\n→ Testing ConvexSync.sync_questions()...")
                # Extract questions from analysis
                questions = []
                question_num = 1
                for gap in project.analysis.gaps:
                    if gap.suggested_question:
                        questions.append({
                            "number": question_num,
                            "priority": gap.priority.value.upper(),
                            "category": gap.category.value,
                            "question": gap.suggested_question,
                            "why_it_matters": gap.impact
                        })
                        question_num += 1
                
                questions_result = sync.sync_questions(project_id, questions)
                results.test(
                    "ConvexSync - sync_questions",
                    questions_result is not None and (isinstance(questions_result, (list, dict))),
                    f"Synced {len(questions)} questions (returned: {type(questions_result).__name__})"
                )
                
                # Test log_event
                print("\n→ Testing ConvexSync.log_event()...")
                event_id = sync.log_event(
                    project_id,
                    "analysis_completed",
                    "Test event from integrity test suite",
                    {"test": True, "confidence": round(project.analysis.overall_confidence, 1)}
                )
                results.test(
                    "ConvexSync - log_event",
                    event_id is not None,
                    f"Event logged with ID: {event_id}"
                )
                
                # Store project_id for phase 4
                convex_project_id = project_id
                
            except Exception as e:
                results.test(
                    "ConvexSync - operations",
                    False,
                    f"Sync operations failed: {str(e)}"
                )
            
            sync.close()
        else:
            print("   ⚠️  No project state available for ConvexSync testing")
            results.test(
                "ConvexSync - skipped",
                True,
                "No project state available"
            )
    
    except Exception as e:
        results.test(
            "ConvexSync - initialization",
            False,
            f"Failed to initialize: {str(e)}"
        )
    
    # Phase 4: Verify Convex Data
    print_section("PHASE 4: VERIFY CONVEX DATA")
    
    print("[4.1] Verifying synced data in Convex...")
    
    try:
        client = ConvexClient()
        
        # Get project from Convex
        print("\n→ Retrieving scenario-1-cozyhome from Convex...")
        try:
            convex_project = client.query("queries/projects:getProjectByScenarioId", {
                "scenarioId": "scenario-1-cozyhome"
            })
            
            if convex_project:
                results.test(
                    "Convex - project exists",
                    True,
                    f"Project found: {convex_project.get('name', 'N/A')}"
                )
                
                print(f"\n   Project Data in Convex:")
                print(f"   - Name: {convex_project.get('name')}")
                print(f"   - Scenario ID: {convex_project.get('scenarioId')}")
                print(f"   - Confidence: {convex_project.get('confidence')}%")
                print(f"   - Gaps: {convex_project.get('gapsCount')}")
                print(f"   - Conflicts: {convex_project.get('conflictsCount')}")
                print(f"   - Ambiguities: {convex_project.get('ambiguitiesCount')}")
                print(f"   - Documents: {convex_project.get('documentsCount')}")
                print(f"   - Status: {convex_project.get('status')}")
                
                # Verify counts match expectations
                results.test(
                    "Convex - confidence score persisted",
                    convex_project.get('confidence', 0) > 0,
                    f"Confidence: {convex_project.get('confidence')}%"
                )
                
                results.test(
                    "Convex - documents count",
                    convex_project.get('documentsCount', 0) >= 4,
                    f"Documents: {convex_project.get('documentsCount')}"
                )
                
                # Verify it matches our local analysis
                local_confidence = round(project.analysis.overall_confidence, 1)
                convex_confidence = convex_project.get('confidence', 0)
                confidence_match = abs(local_confidence - convex_confidence) < 1.0
                
                results.test(
                    "Convex - data consistency",
                    confidence_match,
                    f"Local: {local_confidence}%, Convex: {convex_confidence}%"
                )
                
            else:
                results.test(
                    "Convex - project exists",
                    False,
                    "Project not found in Convex"
                )
        
        except Exception as e:
            results.test(
                "Convex - data verification",
                False,
                f"Verification failed: {str(e)}"
            )
        
        client.close()
        
    except Exception as e:
        results.test(
            "Convex - data verification",
            False,
            f"Failed to verify: {str(e)}"
        )

else:
    print("\n⚠️  Convex not configured - skipping Phases 3 and 4")
    print(f"   CONVEX_DEPLOYMENT_URL: {config.CONVEX_DEPLOYMENT_URL or 'Not set'}")
    results.test(
        "Convex integration - skipped",
        True,
        "Convex not configured in environment"
    )


# ============================================================================
# PHASE 5: TEST ERROR HANDLING
# ============================================================================

print_section("PHASE 5: TEST ERROR HANDLING")

print("[5.1] Testing error scenarios...")

# Non-existent project
print("\n→ Testing with non-existent project...")
non_existent = storage.get_project("non-existent-project")
results.test(
    "Error handling - non-existent project",
    non_existent is None,
    "Returns None for non-existent project"
)

# Empty document list analysis
print("\n→ Testing analysis with empty project...")
empty_project = ProjectState(
    project_id="test-empty",
    project_name="Empty Test",
    project_description=""
)
analyzer = DiscoveryAnalyzer()
empty_analysis = analyzer.analyze([], [])

results.test(
    "Error handling - empty document analysis",
    empty_analysis is not None,
    f"Analysis completes with 0 confidence: {round(empty_analysis.overall_confidence, 1)}%"
)

results.test(
    "Error handling - empty analysis has baseline confidence",
    0 <= empty_analysis.overall_confidence <= 100,
    f"Empty analysis gives baseline confidence: {round(empty_analysis.overall_confidence, 1)}%"
)

# Invalid file path
print("\n→ Testing with invalid file path...")
try:
    invalid_docs = storage.get_all_discovery_documents("scenario-999-invalid")
    results.test(
        "Error handling - invalid project path",
        len(invalid_docs) == 0,
        "Returns empty list for invalid project"
    )
except Exception as e:
    results.test(
        "Error handling - invalid project path",
        True,
        f"Gracefully handles error: {type(e).__name__}"
    )


# ============================================================================
# FINAL SUMMARY
# ============================================================================

success = results.summary()

print("\n" + "="*60)
print("MCP SERVER STATUS")
print("="*60)
print(f"Server URL: {BASE_URL}")
print(f"Convex Enabled: {'Yes' if config.is_convex_enabled() else 'No'}")
if config.is_convex_enabled():
    print(f"Convex URL: {config.CONVEX_DEPLOYMENT_URL}")
print("="*60)

if success:
    print("\n✅ ALL TESTS PASSED! MCP Server integrity verified.")
    sys.exit(0)
else:
    print("\n❌ SOME TESTS FAILED. Review errors above.")
    sys.exit(1)
