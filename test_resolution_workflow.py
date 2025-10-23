#!/usr/bin/env python3
"""
Test Resolution Workflow
Automated testing for resolution and clarification detection in the Discovery Agent MCP.

Usage:
    python test_resolution_workflow.py --run-full
    python test_resolution_workflow.py --validate
    python test_resolution_workflow.py --wipe-only
    python test_resolution_workflow.py --iterations 3
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime
import importlib

# Add MCP src to path
sys.path.insert(0, str(Path(__file__).parent / "mcp" / "src"))

from models.project_state import ProjectState
from models.analysis import AnalysisResult
from models.document import Document, DocumentType
from core.state_manager import ProjectStateManager
from core.analyzer import DiscoveryAnalyzer
from storage import get_storage_provider
from persistence import ConvexSync, ConvexClient
from config import config


class TestResults:
    """Container for test results."""
    
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.conflicts_found = []
        self.ambiguities_found = []
        self.gaps_found = []
        self.confidence_score = 0.0
        self.systems_identified = []
        self.client_name = None
        self.errors = []
        self.warnings = []
        
    def to_dict(self) -> Dict:
        return {
            "timestamp": self.timestamp,
            "conflicts": self.conflicts_found,
            "ambiguities": self.ambiguities_found,
            "gaps": self.gaps_found,
            "confidence_score": self.confidence_score,
            "systems_identified": self.systems_identified,
            "client_name": self.client_name,
            "errors": self.errors,
            "warnings": self.warnings
        }


class ResolutionWorkflowTester:
    """Automated test runner for resolution/clarification workflow."""
    
    def __init__(self, scenario_id: str = "scenario-6-enterprise-full", demo_mode: bool = False):
        self.scenario_id = scenario_id
        self.base_path = Path(__file__).parent / "test-data" / scenario_id
        self.expected_results_path = self.base_path / "expected-results.json"
        self.demo_mode = demo_mode
        
        # Set demo mode in config if enabled
        if demo_mode:
            os.environ["DEMO_MODE"] = "true"
            # Reload config module to pick up new env var
            import config as config_module
            importlib.reload(config_module)
            from config import config as reloaded_config
            # Update global config reference
            globals()['config'] = reloaded_config
            print(f"🎭 Demo mode enabled: {reloaded_config.get_demo_context()}")
        
        # Initialize components
        self.storage = get_storage_provider("local", base_path=str(Path(__file__).parent / "test-data"))
        self.state_manager = ProjectStateManager()
        self.analyzer = DiscoveryAnalyzer()
        
        # Initialize Convex if available
        from config import config as current_config
        if current_config.is_convex_enabled():
            try:
                self.convex_sync = ConvexSync()
            except Exception as e:
                print(f"⚠️  Convex not available: {e}")
        else:
            self.convex_sync = None
        
        # Load expected results
        self.expected_results = self._load_expected_results()
    
    def _load_expected_results(self) -> Dict:
        """Load expected results JSON."""
        if not self.expected_results_path.exists():
            print(f"⚠️  Expected results file not found: {self.expected_results_path}")
            return {}
        
        with open(self.expected_results_path) as f:
            return json.load(f)
    
    def run_full_test(self) -> TestResults:
        """Run complete test cycle: ingest → analyze → sync."""
        print(f"\n{'='*60}")
        print(f"🧪 Running Full Test: {self.scenario_id}")
        print(f"{'='*60}\n")
        
        results = TestResults()
        
        try:
            # Step 1: Ingest documents
            print("📥 Step 1: Ingesting documents...")
            project = self._ingest_documents()
            print(f"   ✅ Ingested {len(project.documents)} documents")
            
            # Step 2: Analyze documents
            print("\n🔍 Step 2: Analyzing documents...")
            analysis = self._analyze_documents(project)
            print(f"   ✅ Analysis complete")
            print(f"      Confidence: {analysis.overall_confidence:.1f}%")
            print(f"      Conflicts: {len(analysis.conflicts)}")
            print(f"      Ambiguities: {len(analysis.ambiguities)}")
            print(f"      Gaps: {len(analysis.gaps)}")
            
            # Step 3: Extract results
            results.conflicts_found = [c.to_dict() for c in analysis.conflicts]
            results.ambiguities_found = [a.to_dict() for a in analysis.ambiguities]
            results.gaps_found = [g.to_dict() for g in analysis.gaps]
            results.confidence_score = analysis.overall_confidence
            results.systems_identified = analysis.systems_identified
            results.client_name = analysis.client_name
            
            # Step 4: Sync to Convex (if available)
            if self.convex_sync:
                try:
                    print("\n☁️  Step 3: Syncing to Convex...")
                    self._sync_to_convex(project)
                    print("   ✅ Sync complete")
                except Exception as e:
                    print(f"   ⚠️  Convex sync failed: {e}")
                    results.warnings.append(f"Convex sync failed: {e}")
            
            # Step 5: Display detailed results
            self._display_results(analysis)
            
        except Exception as e:
            results.errors.append(str(e))
            print(f"\n❌ Error during test: {e}")
            import traceback
            traceback.print_exc()
        
        return results
    
    def _ingest_documents(self) -> ProjectState:
        """Ingest documents from scenario folder."""
        # Create or get project
        project = self.state_manager.get_project(self.scenario_id)
        if not project:
            project = ProjectState(
                project_id=self.scenario_id,
                project_name=self.expected_results.get("scenario_name", self.scenario_id)
            )
        
        # Get all discovery documents using the storage provider's method
        doc_paths = self.storage.get_all_discovery_documents(self.scenario_id)
        
        for doc_path in doc_paths:
            try:
                # Read file directly
                with open(doc_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Determine document type based on folder
                doc_type = DocumentType.OTHER
                if 'email' in str(doc_path):
                    doc_type = DocumentType.EMAIL
                elif 'transcript' in str(doc_path):
                    doc_type = DocumentType.TRANSCRIPT
                elif 'client-doc' in str(doc_path) or 'rfp' in doc_path.name.lower():
                    doc_type = DocumentType.SOW  # Use SOW for client documents
                
                # Create document object
                doc = Document(
                    file_path=str(doc_path),
                    content=content,
                    doc_type=doc_type,
                    date=datetime.fromtimestamp(doc_path.stat().st_mtime),
                    metadata={"size": doc_path.stat().st_size}
                )
                
                if doc not in project.documents:
                    project.documents.append(doc)
                    
            except Exception as e:
                print(f"   ⚠️  Could not load {doc_path.name}: {e}")
        
        # Save project state
        self.state_manager.update_project(project)
        return project
    
    def _analyze_documents(self, project: ProjectState) -> AnalysisResult:
        """Analyze project documents."""
        analysis = self.analyzer.analyze(project.documents, project.additional_context)
        project.update_analysis(analysis)
        self.state_manager.update_project(project)
        return analysis
    
    def _sync_to_convex(self, project: ProjectState):
        """Sync project data to Convex."""
        if self.convex_sync:
            self.convex_sync.sync_full_project(project)
    
    def _display_results(self, analysis: AnalysisResult):
        """Display detailed analysis results."""
        print(f"\n{'='*60}")
        print("📊 ANALYSIS RESULTS")
        print(f"{'='*60}\n")
        
        # Conflicts
        print("🔴 CONFLICTS:")
        if analysis.conflicts:
            for i, conflict in enumerate(analysis.conflicts, 1):
                print(f"\n   {i}. {conflict.topic}")
                print(f"      Priority: {conflict.priority.value}")
                print(f"      Statements: {len(conflict.conflicting_statements)}")
                if conflict.resolution:
                    print(f"      ✅ RESOLUTION FOUND: {conflict.resolution[:100]}...")
                else:
                    print(f"      ❌ NO RESOLUTION")
        else:
            print("   None found")
        
        # Ambiguities
        print(f"\n🟡 AMBIGUITIES:")
        if analysis.ambiguities:
            for i, ambiguity in enumerate(analysis.ambiguities, 1):
                print(f"\n   {i}. '{ambiguity.term}' in context: {ambiguity.context[:50]}...")
                print(f"      Clarification needed: {ambiguity.clarification_needed[:60]}...")
                if ambiguity.clarification:
                    print(f"      ✅ CLARIFICATION FOUND: {ambiguity.clarification[:100]}...")
                else:
                    print(f"      ❌ NO CLARIFICATION")
        else:
            print("   None found")
        
        # Gaps
        print(f"\n🔵 GAPS:")
        if analysis.gaps:
            for i, gap in enumerate(analysis.gaps, 1):
                print(f"\n   {i}. {gap.description}")
                print(f"      Category: {gap.category.value}")
                print(f"      Priority: {gap.priority.value}")
                print(f"      Impact: {gap.impact}")
        else:
            print("   None found")
        
        # Summary
        print(f"\n{'='*60}")
        print(f"Overall Confidence: {analysis.overall_confidence:.1f}%")
        print(f"Client: {analysis.client_name}")
        print(f"Systems: {', '.join(analysis.systems_identified)}")
        print(f"{'='*60}\n")
    
    def validate_results(self, results: TestResults = None) -> bool:
        """Validate results against expected outcomes."""
        if not results:
            # Load latest results
            print("⚠️  No results provided, running new test...")
            results = self.run_full_test()
        
        print(f"\n{'='*60}")
        print("✅ VALIDATING RESULTS")
        print(f"{'='*60}\n")
        
        all_passed = True
        
        # Validate conflicts
        print("Validating conflicts...")
        for expected_conflict in self.expected_results.get("expected_conflicts", []):
            found = False
            for conflict in results.conflicts_found:
                if any(keyword.lower() in conflict.get("topic", "").lower() 
                       for keyword in expected_conflict["description_contains"]):
                    found = True
                    if expected_conflict.get("should_have_resolution"):
                        if conflict.get("resolution"):
                            print(f"   ✅ Conflict resolution found for '{conflict['topic']}'")
                        else:
                            print(f"   ❌ Expected resolution for '{conflict['topic']}' but none found")
                            all_passed = False
                    break
            
            if not found:
                print(f"   ❌ Expected conflict not found: {expected_conflict['topic']}")
                all_passed = False
        
        # Validate ambiguities
        print("\nValidating ambiguities...")
        for expected_amb in self.expected_results.get("expected_ambiguities", []):
            found = False
            for ambiguity in results.ambiguities_found:
                if expected_amb["term"].lower() in ambiguity.get("term", "").lower():
                    found = True
                    if expected_amb.get("should_have_clarification"):
                        if ambiguity.get("clarification"):
                            print(f"   ✅ Clarification found for '{ambiguity['term']}'")
                        else:
                            print(f"   ❌ Expected clarification for '{ambiguity['term']}' but none found")
                            all_passed = False
                    break
            
            if not found:
                print(f"   ❌ Expected ambiguity not found: {expected_amb['term']}")
                all_passed = False
        
        # Validate gaps
        print("\nValidating gaps...")
        expected_gaps = self.expected_results.get("expected_gaps", [])
        found_gaps = len(results.gaps_found)
        expected_count = len(expected_gaps)
        
        if abs(found_gaps - expected_count) <= 1:  # Allow ±1 tolerance
            print(f"   ✅ Gap count acceptable: {found_gaps} (expected ~{expected_count})")
        else:
            print(f"   ❌ Gap count mismatch: {found_gaps} found, expected ~{expected_count}")
            all_passed = False
        
        # Validate confidence range
        print("\nValidating confidence score...")
        conf_range = self.expected_results.get("confidence_range", {})
        min_conf = conf_range.get("min", 0)
        max_conf = conf_range.get("max", 100)
        
        if min_conf <= results.confidence_score <= max_conf:
            print(f"   ✅ Confidence score in range: {results.confidence_score:.1f}% ({min_conf}-{max_conf}%)")
        else:
            print(f"   ❌ Confidence score out of range: {results.confidence_score:.1f}% (expected {min_conf}-{max_conf}%)")
            all_passed = False
        
        # Final result
        print(f"\n{'='*60}")
        if all_passed:
            print("✅ ALL VALIDATIONS PASSED")
        else:
            print("❌ SOME VALIDATIONS FAILED")
        print(f"{'='*60}\n")
        
        return all_passed
    
    def wipe_data(self):
        """Wipe project data (local state and Convex)."""
        print(f"\n🗑️  Wiping data for {self.scenario_id}...")
        
        # Wipe local state
        try:
            project = self.state_manager.get_project(self.scenario_id)
            if project:
                self.state_manager.delete_project(self.scenario_id)
                print("   ✅ Local state wiped")
        except Exception as e:
            print(f"   ⚠️  Could not wipe local state: {e}")
        
        # Wipe Convex (if available)
        if self.convex_sync:
            try:
                # Note: We'd need a delete mutation in Convex to fully wipe
                # For now, just note that it should be done manually
                print("   ⚠️  Convex data should be wiped manually (no delete API yet)")
            except Exception as e:
                print(f"   ⚠️  Could not wipe Convex: {e}")
        
        print("   ✅ Wipe complete\n")
    
    def run_iterations(self, count: int = 1) -> List[TestResults]:
        """Run multiple test iterations."""
        all_results = []
        
        for i in range(count):
            print(f"\n{'#'*60}")
            print(f"ITERATION {i + 1} of {count}")
            print(f"{'#'*60}")
            
            # Wipe previous data
            if i > 0:
                self.wipe_data()
            
            # Run test
            results = self.run_full_test()
            all_results.append(results)
            
            # Validate
            if i == count - 1:  # Only validate on last iteration
                self.validate_results(results)
        
        return all_results


def main():
    parser = argparse.ArgumentParser(description="Test resolution/clarification workflow")
    parser.add_argument("--scenario", default="scenario-6-enterprise-full", help="Test scenario ID")
    parser.add_argument("--run-full", action="store_true", help="Run full test cycle")
    parser.add_argument("--validate", action="store_true", help="Validate results against expected")
    parser.add_argument("--wipe-only", action="store_true", help="Only wipe data, don't run test")
    parser.add_argument("--iterations", type=int, default=1, help="Number of test iterations")
    parser.add_argument("--demo", action="store_true", help="Enable demo mode (tags data for portal demo)")
    
    args = parser.parse_args()
    
    tester = ResolutionWorkflowTester(scenario_id=args.scenario, demo_mode=args.demo)
    
    if args.wipe_only:
        tester.wipe_data()
    elif args.validate:
        tester.validate_results()
    elif args.iterations > 1:
        tester.run_iterations(args.iterations)
    else:
        results = tester.run_full_test()
        tester.validate_results(results)


if __name__ == "__main__":
    main()

