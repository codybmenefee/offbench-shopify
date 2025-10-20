"""
Discovery to Implementation Confidence Tool - MCP Server (Refactored)
5 general-purpose tools with storage abstraction for Google Drive readiness.
"""

import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime

from fastmcp import FastMCP

# Import storage layer
from storage import get_storage_provider, FolderType

# Import models and core logic
from models.document import Document, DocumentType
from models.project_state import ProjectState, ProjectConfig
from core.state_manager import ProjectStateManager
from core.analyzer import DiscoveryAnalyzer

# Import Convex integration
from config import config
from persistence import ConvexSync

# Create FastMCP instance
mcp = FastMCP(name="Discovery Agent")

# Base paths - calculate relative to this file for portability
BASE_PATH = Path(__file__).parent.parent.parent  # Go up to repo root
TEST_DATA_PATH = str(BASE_PATH / "test-data")
TEMPLATES_PATH = str(BASE_PATH / "templates")

# Initialize storage provider (default to local for prototype)
storage = get_storage_provider("local", base_path=TEST_DATA_PATH)

# Initialize Convex sync (optional - only if configured)
convex_sync = None
if config.is_convex_enabled():
    try:
        convex_sync = ConvexSync()
    except Exception as e:
        print(f"Warning: Could not initialize Convex sync: {e}")
        convex_sync = None


# ============================================================================
# CORE TOOLS (5 General-Purpose Tools)
# ============================================================================

@mcp.tool()
def manage_project(
    action: str,
    project_id: Optional[str] = None,
    project_name: Optional[str] = None,
    config: Optional[Dict] = None
) -> Dict:
    """
    Unified project management tool.
    
    Args:
        action: Action to perform ("list", "create", "get", "delete", "configure")
        project_id: Project identifier (required for get/delete/configure)
        project_name: Human-readable name (required for create)
        config: Project configuration dict (for create/configure)
    
    Returns:
        Result of the action with relevant project data
    
    Actions:
        - list: Show all available projects
        - create: Create new project with folder structure
        - get: Retrieve project metadata and status
        - delete: Remove project
        - configure: Update project settings (thresholds, patterns, etc.)
    """
    try:
        if action == "list":
            projects = storage.list_projects()
            return {
                "action": "list",
                "projects": projects,
                "count": len(projects),
                "message": f"Found {len(projects)} project(s)"
            }
        
        elif action == "create":
            if not project_id or not project_name:
                return {"error": "create action requires project_id and project_name"}
            
            if storage.project_exists(project_id):
                return {"error": f"Project {project_id} already exists"}
            
            # Create via storage provider (creates folder structure)
            project_meta = storage.create_project(
                project_id=project_id,
                project_name=project_name,
                config=config
            )
            
            # Initialize in state manager
            state_manager = ProjectStateManager()
            project_config = ProjectConfig.from_dict(config) if config else ProjectConfig()
            project = state_manager.create_project(
                project_id=project_id,
                project_name=project_name,
                project_description=""
            )
            project.config = project_config
            state_manager.update_project(project)
            
            return {
                "action": "create",
                "project_id": project_id,
                "project_name": project_name,
                "project_meta": project_meta,
                "message": f"Created project: {project_name}"
            }
        
        elif action == "get":
            if not project_id:
                return {"error": "get action requires project_id"}
            
            project_meta = storage.get_project(project_id)
            if not project_meta:
                return {"error": f"Project {project_id} not found"}
            
            # Get state from state manager
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            
            result = {
                "action": "get",
                "project_id": project_id,
                "project_meta": project_meta
            }
            
            if project:
                result["state"] = {
                    "documents_loaded": len(project.documents),
                    "has_analysis": project.analysis is not None,
                    "confidence": round(project.analysis.overall_confidence, 1) if project.analysis else None,
                    "config": project.config.to_dict()
                }
            
            return result
        
        elif action == "delete":
            if not project_id:
                return {"error": "delete action requires project_id"}
            
            deleted = storage.delete_project(project_id)
            if deleted:
                # Also clear from state manager
                state_manager = ProjectStateManager()
                state_manager.clear_project(project_id)
                
                return {
                    "action": "delete",
                    "project_id": project_id,
                    "message": f"Deleted project: {project_id}"
                }
            else:
                return {"error": f"Project {project_id} not found"}
        
        elif action == "configure":
            if not project_id:
                return {"error": "configure action requires project_id"}
            
            if not config:
                return {"error": "configure action requires config parameter"}
            
            # Update in storage
            storage.save_config(project_id, config)
            
            # Update in state manager
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            if project:
                project.config = ProjectConfig.from_dict(config)
                state_manager.update_project(project)
            
            return {
                "action": "configure",
                "project_id": project_id,
                "config": config,
                "message": "Configuration updated"
            }
        
        else:
            return {"error": f"Unknown action: {action}. Valid: list, create, get, delete, configure"}
    
    except Exception as e:
        return {"error": f"Error in manage_project: {str(e)}"}


@mcp.tool()
def ingest(
    project_id: str,
    source: str = "local",
    location: str = "",
    doc_type: Optional[str] = None,
    append: bool = True
) -> Dict:
    """
    Universal document ingestion from any source.
    
    Args:
        project_id: Project identifier
        source: Source type ("local", "text", "google_drive", "url")
        location: Source location (path, folder ID, URL, or raw text)
        doc_type: Override document type detection ("email", "transcript", "sow", "note")
        append: If True, add to existing docs. If False, replace all docs.
    
    Returns:
        Summary of ingested documents
    
    Examples:
        # Ingest from local folder (current behavior)
        ingest(project_id="cozyhome", source="local", location="/path/to/discovery/docs")
        
        # Add a single text note
        ingest(project_id="cozyhome", source="text", location="Client confirmed...", doc_type="note")
        
        # Future: Google Drive
        ingest(project_id="cozyhome", source="google_drive", location="folder_id_xyz")
    """
    try:
        if not storage.project_exists(project_id):
            return {"error": f"Project {project_id} not found. Create it first with manage_project(action='create')"}
        
        state_manager = ProjectStateManager()
        project = state_manager.get_or_create(
            project_id=project_id,
            project_name=project_id.replace("-", " ").title()
        )
        
        # Clear existing documents if not appending
        if not append:
            project.documents = []
        
        documents_found = []
        
        if source == "local":
            # Ingest from local filesystem
            location_path = Path(location) if location else storage._get_folder_path(project_id, FolderType.DISCOVERY)
            
            if not location_path or not location_path.exists():
                return {"error": f"Location not found: {location}"}
            
            # Use storage provider's method to get all discovery documents
            if hasattr(storage, 'get_all_discovery_documents'):
                doc_paths = storage.get_all_discovery_documents(project_id)
            else:
                # Fallback: scan location
                doc_paths = list(location_path.rglob("*.txt"))
            
            for file_path in doc_paths:
                doc = _parse_document_file(file_path, doc_type_override=doc_type)
                project.add_document(doc)
                documents_found.append({
                    "file": file_path.name,
                    "type": doc.doc_type.value
                })
        
        elif source == "text":
            # Ingest raw text as a document
            if not location:
                return {"error": "text source requires location parameter with content"}
            
            doc_type_enum = DocumentType(doc_type) if doc_type else DocumentType.NOTES
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"note_{timestamp}.txt"
            
            doc = Document(
                file_path=filename,
                content=location,
                doc_type=doc_type_enum,
                metadata={"source": "text_input", "timestamp": timestamp}
            )
            project.add_document(doc)
            
            # Save to working folder for persistence
            storage.add_document(
                project_id=project_id,
                folder_type=FolderType.WORKING,
                filename=filename,
                content=location,
                metadata={"type": "text_input"}
            )
            
            documents_found.append({
                "file": filename,
                "type": doc_type_enum.value
            })
        
        elif source == "google_drive":
            return {"error": "Google Drive ingestion not yet implemented. Coming soon!"}
        
        elif source == "url":
            return {"error": "URL ingestion not yet implemented. Coming soon!"}
        
        else:
            return {"error": f"Unknown source: {source}. Valid: local, text, google_drive, url"}
        
        # Update state
        state_manager.update_project(project)
        
        return {
            "project_id": project_id,
            "source": source,
            "documents_loaded": len(documents_found),
            "total_documents": len(project.documents),
            "documents": documents_found,
            "message": f"Successfully ingested {len(documents_found)} document(s)"
        }
    
    except Exception as e:
        return {"error": f"Error ingesting documents: {str(e)}"}


@mcp.tool()
def analyze(
    project_id: Union[str, List[str]],
    mode: str = "full",
    focus: Optional[List[str]] = None,
    compare_to: Optional[str] = None
) -> Dict:
    """
    Comprehensive analysis engine with multiple modes.
    
    Args:
        project_id: Project identifier (or list for batch mode)
        mode: Analysis mode ("full", "quick", "gaps_only", "questions_only", "confidence_only", "compare")
        focus: Specific categories to focus on (["business_rules", "technical_constraints"])
        compare_to: Another project ID to compare against (for mode="compare")
    
    Returns:
        Analysis results based on mode
    
    Modes:
        - full: Complete analysis with all findings
        - quick: Confidence score only
        - gaps_only: Just gap detection
        - questions_only: Prioritized clarifying questions
        - confidence_only: Score without detailed findings
        - compare: Compare this project to another
    
    Examples:
        # Full analysis
        analyze(project_id="cozyhome", mode="full")
        
        # Quick confidence check
        analyze(project_id="cozyhome", mode="quick")
        
        # Just get questions for client meeting
        analyze(project_id="cozyhome", mode="questions_only")
        
        # Compare two projects
        analyze(project_id="cozyhome", mode="compare", compare_to="brewcrew")
        
        # Batch analysis
        analyze(project_id=["cozyhome", "brewcrew"], mode="quick")
    """
    try:
        # Batch mode
        if isinstance(project_id, list):
            results = []
            for pid in project_id:
                result = analyze(pid, mode=mode, focus=focus, compare_to=compare_to)
                results.append(result)
            return {
                "batch_mode": True,
                "projects_analyzed": len(results),
                "results": results
            }
        
        # Single project analysis
        state_manager = ProjectStateManager()
        project = state_manager.get_project(project_id)
        
        if not project:
            return {"error": f"Project {project_id} not found. Run ingest() first."}
        
        if not project.documents:
            return {"error": f"No documents found for {project_id}. Run ingest() first."}
        
        # Store previous confidence for comparison
        previous_confidence = None
        if project.analysis:
            previous_confidence = project.analysis.overall_confidence
        
        # Run analysis based on mode
        analyzer = DiscoveryAnalyzer()
        
        if mode in ["full", "gaps_only", "questions_only", "quick", "confidence_only"]:
            analysis = analyzer.analyze(project.documents, project.additional_context)
            
            # Update project state unless mode is read-only
            if mode in ["full", "quick"]:
                project.update_analysis(analysis)
                state_manager.update_project(project)
            
            # Build response based on mode
            if mode == "full":
                questions = _extract_questions_from_analysis(analysis)
                return {
                    "project_id": project_id,
                    "mode": "full",
                    "confidence": round(analysis.overall_confidence, 1),
                    "previous_confidence": round(previous_confidence, 1) if previous_confidence else None,
                    "improvement": round(analysis.overall_confidence - previous_confidence, 1) if previous_confidence else None,
                    "analysis": analysis.to_dict(),
                    "questions": questions,
                    "message": f"Analysis complete. Confidence: {round(analysis.overall_confidence, 1)}%"
                }
            
            elif mode == "quick" or mode == "confidence_only":
                return {
                    "project_id": project_id,
                    "mode": mode,
                    "confidence": round(analysis.overall_confidence, 1),
                    "previous_confidence": round(previous_confidence, 1) if previous_confidence else None,
                    "improvement": round(analysis.overall_confidence - previous_confidence, 1) if previous_confidence else None,
                    "clarity": round(analysis.clarity_score, 1),
                    "completeness": round(analysis.completeness_score, 1),
                    "alignment": round(analysis.alignment_score, 1)
                }
            
            elif mode == "gaps_only":
                gaps = [g.to_dict() for g in analysis.gaps]
                if focus:
                    gaps = [g for g in gaps if g["category"] in focus]
                return {
                    "project_id": project_id,
                    "mode": "gaps_only",
                    "gaps": gaps,
                    "gaps_count": len(gaps)
                }
            
            elif mode == "questions_only":
                questions = _extract_questions_from_analysis(analysis)
                return {
                    "project_id": project_id,
                    "mode": "questions_only",
                    "questions": questions,
                    "questions_count": len(questions)
                }
        
        elif mode == "compare":
            if not compare_to:
                return {"error": "compare mode requires compare_to parameter"}
            
            # Analyze both projects
            analysis1 = analyzer.analyze(project.documents, project.additional_context)
            
            project2 = state_manager.get_project(compare_to)
            if not project2:
                return {"error": f"Comparison project {compare_to} not found"}
            
            analysis2 = analyzer.analyze(project2.documents, project2.additional_context)
            
            return {
                "mode": "compare",
                "project_1": {
                    "project_id": project_id,
                    "confidence": round(analysis1.overall_confidence, 1),
                    "gaps": len(analysis1.gaps),
                    "ambiguities": len(analysis1.ambiguities),
                    "conflicts": len(analysis1.conflicts),
                    "systems": analysis1.systems_identified
                },
                "project_2": {
                    "project_id": compare_to,
                    "confidence": round(analysis2.overall_confidence, 1),
                    "gaps": len(analysis2.gaps),
                    "ambiguities": len(analysis2.ambiguities),
                    "conflicts": len(analysis2.conflicts),
                    "systems": analysis2.systems_identified
                },
                "comparison": {
                    "confidence_diff": round(analysis1.overall_confidence - analysis2.overall_confidence, 1),
                    "better_project": project_id if analysis1.overall_confidence > analysis2.overall_confidence else compare_to
                }
            }
        
        else:
            return {"error": f"Unknown mode: {mode}. Valid: full, quick, gaps_only, questions_only, confidence_only, compare"}
    
    except Exception as e:
        return {"error": f"Error analyzing project: {str(e)}"}


@mcp.tool()
def update(
    project_id: str,
    type: str,
    content: str,
    target_id: Optional[str] = None,
    metadata: Optional[Dict] = None
) -> Dict:
    """
    Add context, answer questions, override findings, or resolve items.
    
    Args:
        project_id: Project identifier
        type: Update type ("context", "answer", "override", "resolve")
        content: Update content
        target_id: Target gap/question/finding ID (for answer/override/resolve)
        metadata: Optional metadata
    
    Returns:
        Confirmation of update with impact
    
    Types:
        - context: Add general information
        - answer: Answer specific gap/question by ID
        - override: Correct wrong analysis finding
        - resolve: Mark ambiguity/gap as resolved
    
    Examples:
        # Add general context
        update(project_id="cozyhome", type="context", content="Client uses QB Online, not Desktop")
        
        # Answer specific gap
        update(project_id="cozyhome", type="answer", content="Refunds create credit memos", target_id="gap_refund_001")
        
        # Override incorrect finding
        update(project_id="cozyhome", type="override", content="Klaviyo not involved", target_id="system_klaviyo")
    """
    try:
        state_manager = ProjectStateManager()
        project = state_manager.get_project(project_id)
        
        if not project:
            return {"error": f"Project {project_id} not found"}
        
        update_record = {
            "type": type,
            "content": content,
            "target_id": target_id,
            "metadata": metadata,
            "timestamp": datetime.now().isoformat()
        }
        
        if type == "context":
            # Add general context
            project.add_context(content, update_type="context")
            
            # Save to working folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"context_{timestamp}.txt"
            storage.add_document(
                project_id=project_id,
                folder_type=FolderType.WORKING,
                filename=filename,
                content=content,
                metadata={"type": "context"}
            )
            
            message = "Context added"
        
        elif type == "answer":
            # Answer specific gap
            if not target_id:
                return {"error": "answer type requires target_id"}
            
            project.add_context(f"[Answer to {target_id}]: {content}", update_type="answer")
            
            # Try to mark gap as answered
            if project.analysis:
                for gap in project.analysis.gaps:
                    if target_id in gap.description.lower() or (gap.suggested_question and target_id in gap.suggested_question.lower()):
                        gap.answered = True
                        gap.answer = content
                        break
            
            message = f"Answer recorded for {target_id}"
        
        elif type == "override":
            # Override analysis finding
            project.add_context(f"[Override {target_id}]: {content}", update_type="override")
            message = f"Override recorded for {target_id}"
        
        elif type == "resolve":
            # Mark item as resolved
            if not target_id:
                return {"error": "resolve type requires target_id"}
            
            project.add_context(f"[Resolved {target_id}]: {content}", update_type="resolve")
            
            # Mark in analysis
            if project.analysis:
                for ambiguity in project.analysis.ambiguities:
                    if target_id in ambiguity.term.lower():
                        # Remove from list (mark as resolved)
                        project.analysis.ambiguities.remove(ambiguity)
                        break
            
            message = f"Resolved {target_id}"
        
        else:
            return {"error": f"Unknown type: {type}. Valid: context, answer, override, resolve"}
        
        # Update state
        state_manager.update_project(project)
        
        # Auto-reanalyze if configured
        should_reanalyze = project.config.auto_reanalyze if project.config else True
        new_confidence = None
        
        if should_reanalyze and project.analysis:
            # Re-analyze to update confidence
            result = analyze(project_id, mode="quick")
            if "confidence" in result:
                new_confidence = result["confidence"]
        
        return {
            "project_id": project_id,
            "update_type": type,
            "target_id": target_id,
            "updates_count": len(project.updates_log),
            "auto_reanalyzed": should_reanalyze,
            "new_confidence": new_confidence,
            "message": message
        }
    
    except Exception as e:
        return {"error": f"Error updating project: {str(e)}"}


@mcp.tool()
def generate(
    project_id: str,
    output_type: str,
    format: str = "markdown",
    template: str = "standard",
    options: Optional[Dict] = None
) -> Dict:
    """
    Generate and export deliverables.
    
    Args:
        project_id: Project identifier
        output_type: Type of deliverable ("sow", "implementation_plan", "tech_specs", "questions_doc", "report", "analysis_snapshot")
        format: Output format ("markdown", "json", "pdf", "html")
        template: Template variant ("standard", "simplified", "custom_name")
        options: Additional options (include_examples, skip_sections, etc.)
    
    Returns:
        Generated content and metadata
    
    Output Types:
        - sow: Client-facing Statement of Work
        - implementation_plan: Internal implementation plan
        - tech_specs: Technical specifications
        - questions_doc: Formatted questions for client meeting
        - report: Analysis summary with trends
        - analysis_snapshot: JSON export of analysis state
    
    Examples:
        # Generate SOW
        generate(project_id="cozyhome", output_type="sow", template="simplified")
        
        # Generate questions doc for meeting
        generate(project_id="cozyhome", output_type="questions_doc", format="pdf")
        
        # Export analysis as JSON
        generate(project_id="cozyhome", output_type="analysis_snapshot", format="json")
    """
    try:
        state_manager = ProjectStateManager()
        project = state_manager.get_project(project_id)
        
        if not project:
            return {"error": f"Project {project_id} not found"}
        
        if not project.analysis and output_type != "analysis_snapshot":
            return {"error": "No analysis found. Run analyze() first."}
        
        options = options or {}
        
        # Generate based on output type
        if output_type in ["sow", "implementation_plan", "tech_specs"]:
            # Load template
            template_map = {
                "sow": "client-facing-sow.md" if template == "standard" else "simplified/client-facing-sow-simplified.md",
                "implementation_plan": "internal-implementation-plan.md" if template == "standard" else "simplified/internal-implementation-plan-simplified.md",
                "tech_specs": "internal-technical-specs.md" if template == "standard" else "simplified/internal-technical-specs-simplified.md"
            }
            
            template_file = template_map.get(output_type)
            if not template_file:
                return {"error": f"Unknown output type: {output_type}"}
            
            template_path = Path(TEMPLATES_PATH) / template_file
            if not template_path.exists():
                return {"error": f"Template not found: {template_file}"}
            
            with open(template_path, 'r') as f:
                template_content = f.read()
            
            # Return template + analysis for AI to fill
            content = {
                "template": template_content,
                "analysis": project.analysis.to_dict(),
                "project_name": project.project_name,
                "instructions": "Fill the template placeholders with analysis data"
            }
            
            # Save to implementation folder
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{output_type}_{timestamp}.{format}"
            
            if format == "json":
                import json
                storage.save_deliverable(
                    project_id=project_id,
                    filename=filename,
                    content=json.dumps(content, indent=2),
                    metadata={"confidence": project.analysis.overall_confidence}
                )
            else:
                storage.save_deliverable(
                    project_id=project_id,
                    filename=filename,
                    content=str(content),
                    metadata={"confidence": project.analysis.overall_confidence}
                )
            
            return {
                "project_id": project_id,
                "output_type": output_type,
                "format": format,
                "template": template,
                "content": content,
                "saved_to": filename,
                "confidence_at_generation": round(project.analysis.overall_confidence, 1),
                "message": f"Generated {output_type}"
            }
        
        elif output_type == "questions_doc":
            # Generate formatted questions document
            questions = _extract_questions_from_analysis(project.analysis)
            
            content = f"# Clarifying Questions for {project.project_name}\n\n"
            content += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            content += f"Current Confidence: {round(project.analysis.overall_confidence, 1)}%\n\n"
            
            for q in questions:
                content += f"## Question {q['number']} - {q['priority']} Priority\n\n"
                content += f"**Category**: {q['category']}\n\n"
                content += f"{q['question']}\n\n"
                content += f"**Why it matters**: {q['why_it_matters']}\n\n"
                content += "---\n\n"
            
            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"questions_{timestamp}.md"
            storage.save_deliverable(project_id=project_id, filename=filename, content=content)
            
            return {
                "project_id": project_id,
                "output_type": "questions_doc",
                "content": content,
                "saved_to": filename,
                "questions_count": len(questions)
            }
        
        elif output_type == "report":
            # Generate analysis report
            content = f"# Discovery Analysis Report: {project.project_name}\n\n"
            content += f"**Project ID**: {project_id}\n"
            content += f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            
            content += f"## Confidence Score\n\n"
            content += f"**Overall**: {round(project.analysis.overall_confidence, 1)}%\n"
            content += f"- Clarity: {round(project.analysis.clarity_score, 1)}%\n"
            content += f"- Completeness: {round(project.analysis.completeness_score, 1)}%\n"
            content += f"- Alignment: {round(project.analysis.alignment_score, 1)}%\n\n"
            
            if project.confidence_history:
                content += f"## Confidence Trend\n\n"
                for entry in project.confidence_history:
                    content += f"- {entry.get('timestamp', 'N/A')}: {round(entry['overall_confidence'], 1)}%\n"
                content += "\n"
            
            content += f"## Systems Identified\n\n"
            for system in project.analysis.systems_identified:
                content += f"- {system}\n"
            content += "\n"
            
            content += f"## Findings Summary\n\n"
            content += f"- **Gaps**: {len(project.analysis.gaps)}\n"
            content += f"- **Ambiguities**: {len(project.analysis.ambiguities)}\n"
            content += f"- **Conflicts**: {len(project.analysis.conflicts)}\n\n"
            
            # Save
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.md"
            storage.save_deliverable(project_id=project_id, filename=filename, content=content)
            
            return {
                "project_id": project_id,
                "output_type": "report",
                "content": content,
                "saved_to": filename
            }
        
        elif output_type == "analysis_snapshot":
            # Export full analysis state as JSON
            import json
            snapshot = project.to_dict()
            content = json.dumps(snapshot, indent=2)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"snapshot_{timestamp}.json"
            storage.save_deliverable(project_id=project_id, filename=filename, content=content)
            
            return {
                "project_id": project_id,
                "output_type": "analysis_snapshot",
                "format": "json",
                "content": snapshot,
                "saved_to": filename
            }
        
        else:
            return {"error": f"Unknown output_type: {output_type}"}
    
    except Exception as e:
        return {"error": f"Error generating deliverable: {str(e)}"}


@mcp.tool()
def sync_to_convex(
    project_id: str,
    sync_type: str = "full",
    components: Optional[List[str]] = None
) -> Dict:
    """
    Sync project data to Convex for admin portal observability.
    
    Args:
        project_id: Project identifier
        sync_type: Type of sync ("full", "metadata", "analysis", "questions", "documents")
        components: Specific components to sync (optional, for partial syncs)
    
    Returns:
        Sync results with details of what was synced
    
    Sync Types:
        - full: Sync everything (metadata, analysis, questions, documents, events)
        - metadata: Only project metadata and counts
        - analysis: Only gaps, conflicts, ambiguities
        - questions: Only extracted questions
        - documents: Only document metadata
    
    Examples:
        # Full sync after analysis
        sync_to_convex(project_id="cozyhome", sync_type="full")
        
        # Just update questions
        sync_to_convex(project_id="cozyhome", sync_type="questions")
        
        # Partial sync of specific components
        sync_to_convex(project_id="cozyhome", sync_type="full", 
                      components=["metadata", "questions"])
    """
    try:
        if not convex_sync:
            return {
                "error": "Convex not configured. Set CONVEX_DEPLOYMENT_URL and CONVEX_ADMIN_KEY in environment.",
                "convex_enabled": False
            }
        
        state_manager = ProjectStateManager()
        project = state_manager.get_project(project_id)
        
        if not project:
            return {"error": f"Project {project_id} not found"}
        
        results = {
            "project_id": project_id,
            "sync_type": sync_type,
            "synced_components": []
        }
        
        # Determine which components to sync
        if sync_type == "full":
            sync_components = components or ["metadata", "analysis", "documents", "questions"]
        elif sync_type == "metadata":
            sync_components = ["metadata"]
        elif sync_type == "analysis":
            sync_components = ["analysis"]
        elif sync_type == "questions":
            sync_components = ["questions"]
        elif sync_type == "documents":
            sync_components = ["documents"]
        else:
            return {"error": f"Unknown sync_type: {sync_type}. Valid: full, metadata, analysis, questions, documents"}
        
        # Perform sync operations
        convex_project_id = None
        
        if "metadata" in sync_components:
            convex_project_id = convex_sync.sync_project_metadata(project)
            results["convex_project_id"] = convex_project_id
            results["synced_components"].append("metadata")
        
        # Get convex project ID for other operations
        if not convex_project_id and project.analysis:
            # Need to sync metadata first to get the ID
            convex_project_id = convex_sync.sync_project_metadata(project)
            results["convex_project_id"] = convex_project_id
        
        if convex_project_id:
            if "analysis" in sync_components and project.analysis:
                gaps_ids = convex_sync.sync_gaps(convex_project_id, project.analysis.gaps)
                conflicts_ids = convex_sync.sync_conflicts(convex_project_id, project.analysis.conflicts)
                ambiguities_ids = convex_sync.sync_ambiguities(convex_project_id, project.analysis.ambiguities)
                
                results["gaps_synced"] = len(gaps_ids)
                results["conflicts_synced"] = len(conflicts_ids)
                results["ambiguities_synced"] = len(ambiguities_ids)
                results["synced_components"].append("analysis")
            
            if "questions" in sync_components and project.analysis:
                questions = _extract_questions_from_analysis(project.analysis)
                questions_ids = convex_sync.sync_questions(convex_project_id, questions)
                results["questions_synced"] = len(questions_ids)
                results["synced_components"].append("questions")
            
            if "documents" in sync_components:
                doc_ids = convex_sync.sync_documents(convex_project_id, project)
                results["documents_synced"] = len(doc_ids)
                results["synced_components"].append("documents")
        
        results["message"] = f"Successfully synced {len(results['synced_components'])} component(s) to Convex"
        return results
    
    except Exception as e:
        return {"error": f"Error syncing to Convex: {str(e)}"}


@mcp.tool()
def query(project_id: str, question: str) -> Dict:
    """
    Answer questions about project documents and analysis.
    
    Args:
        project_id: Project identifier
        question: Question to answer
    
    Returns:
        Answer with relevant excerpts
    
    Examples:
        - "What did the client say about refunds?"
        - "Which documents mention QuickBooks?"
        - "Who are the stakeholders?"
        - "What are the main pain points?"
    """
    try:
        state_manager = ProjectStateManager()
        project = state_manager.get_project(project_id)
        
        if not project:
            return {"error": f"Project {project_id} not found"}
        
        question_lower = question.lower()
        results = []
        
        # Search documents
        for doc in project.documents:
            content_lower = doc.content.lower()
            
            # Simple keyword matching (can be enhanced with semantic search later)
            keywords = [word for word in question_lower.split() if len(word) > 3]
            matches = sum(1 for kw in keywords if kw in content_lower)
            
            if matches > 0:
                # Find relevant excerpts
                sentences = doc.content.split('.')
                relevant_excerpts = []
                
                for sentence in sentences:
                    sentence_lower = sentence.lower()
                    if any(kw in sentence_lower for kw in keywords):
                        relevant_excerpts.append(sentence.strip())
                
                if relevant_excerpts:
                    results.append({
                        "document": doc.file_path,
                        "doc_type": doc.doc_type.value,
                        "relevance_score": matches,
                        "excerpts": relevant_excerpts[:3]  # Top 3
                    })
        
        # Also search analysis results
        analysis_insights = []
        if project.analysis:
            if "pain point" in question_lower or "problem" in question_lower:
                analysis_insights.append({
                    "type": "pain_points",
                    "data": project.analysis.pain_points
                })
            
            if "objective" in question_lower or "goal" in question_lower:
                analysis_insights.append({
                    "type": "objectives",
                    "data": project.analysis.business_objectives
                })
            
            if "system" in question_lower or "tool" in question_lower:
                analysis_insights.append({
                    "type": "systems",
                    "data": project.analysis.systems_identified
                })
            
            if "stakeholder" in question_lower or "participant" in question_lower:
                participants = []
                for doc in project.documents:
                    participants.extend(doc.participants)
                analysis_insights.append({
                    "type": "stakeholders",
                    "data": list(set(participants))
                })
        
        # Sort results by relevance
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        
        return {
            "project_id": project_id,
            "question": question,
            "document_results": results[:5],  # Top 5
            "analysis_insights": analysis_insights,
            "results_count": len(results),
            "message": f"Found {len(results)} relevant result(s)"
        }
    
    except Exception as e:
        return {"error": f"Error querying project: {str(e)}"}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _parse_document_file(file_path: Path, doc_type_override: Optional[str] = None) -> Document:
    """Parse a document file based on its location and type."""
    # Determine document type from path
    path_str = str(file_path).lower()
    
    if doc_type_override:
        doc_type = DocumentType(doc_type_override)
    elif "email" in path_str:
        doc_type = DocumentType.EMAIL
    elif "transcript" in path_str:
        doc_type = DocumentType.TRANSCRIPT
    elif "sow" in file_path.name.lower():
        doc_type = DocumentType.SOW
    elif "guide" in file_path.name.lower() or "brand" in file_path.name.lower():
        doc_type = DocumentType.GUIDE
    elif "note" in file_path.name.lower():
        doc_type = DocumentType.NOTES
    else:
        doc_type = DocumentType.OTHER
    
    # Parse based on type
    if doc_type == DocumentType.EMAIL:
        return _parse_email(file_path)
    elif doc_type == DocumentType.TRANSCRIPT:
        return _parse_transcript(file_path)
    else:
        return _parse_client_doc(file_path, doc_type)


def _parse_email(file_path: Path) -> Document:
    """Parse an email file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    metadata = {}
    participants = []
    subject = None
    date = None
    
    lines = content.split('\n')
    for line in lines[:10]:
        if line.startswith('From:'):
            sender = line.replace('From:', '').strip()
            participants.append(sender)
            if '<' in sender:
                email = sender.split('<')[1].split('>')[0]
                metadata['from'] = email
        elif line.startswith('To:'):
            recipient = line.replace('To:', '').strip()
            participants.append(recipient)
            if '<' in recipient:
                email = recipient.split('<')[1].split('>')[0]
                metadata['to'] = email
        elif line.startswith('Subject:'):
            subject = line.replace('Subject:', '').strip()
        elif line.startswith('Date:'):
            date_str = line.replace('Date:', '').strip()
            try:
                date = datetime.strptime(date_str, '%A, %B %d, %Y, %I:%M %p')
            except:
                pass
    
    return Document(
        file_path=str(file_path),
        content=content,
        doc_type=DocumentType.EMAIL,
        metadata=metadata,
        date=date,
        participants=participants,
        subject=subject
    )


def _parse_transcript(file_path: Path) -> Document:
    """Parse a transcript file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    participants = []
    speaker_pattern = r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\s*:'
    matches = re.finditer(speaker_pattern, content, re.MULTILINE)
    for match in matches:
        speaker = match.group(1)
        if speaker not in participants:
            participants.append(speaker)
    
    return Document(
        file_path=str(file_path),
        content=content,
        doc_type=DocumentType.TRANSCRIPT,
        metadata={},
        participants=participants
    )


def _parse_client_doc(file_path: Path, doc_type: DocumentType) -> Document:
    """Parse a client document file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return Document(
        file_path=str(file_path),
        content=content,
        doc_type=doc_type,
        metadata={}
    )


def _extract_questions_from_analysis(analysis) -> List[Dict]:
    """Extract prioritized questions from analysis results."""
    questions = []
    question_num = 1
    
    # High priority gaps first
    high_priority_gaps = [g for g in analysis.gaps if g.priority.value == "high" and not g.answered]
    medium_priority_gaps = [g for g in analysis.gaps if g.priority.value == "medium" and not g.answered]
    
    for gap in high_priority_gaps:
        if gap.suggested_question:
            questions.append({
                "number": question_num,
                "priority": "HIGH",
                "category": gap.category.value,
                "question": gap.suggested_question,
                "why_it_matters": gap.impact
            })
            question_num += 1
    
    for gap in medium_priority_gaps:
        if gap.suggested_question:
            questions.append({
                "number": question_num,
                "priority": "MEDIUM",
                "category": gap.category.value,
                "question": gap.suggested_question,
                "why_it_matters": gap.impact
            })
            question_num += 1
    
    # Add top ambiguities
    for ambiguity in analysis.ambiguities[:3]:
        questions.append({
            "number": question_num,
            "priority": ambiguity.priority.value.upper(),
            "category": "clarity",
            "question": f"Regarding '{ambiguity.term}': {ambiguity.clarification_needed}",
            "why_it_matters": f"Context: {ambiguity.context}"
        })
        question_num += 1
    
    return questions


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    # Support both transports via command line
    transport = "http"  # default
    if len(sys.argv) > 1 and sys.argv[1] == "--stdio":
        transport = "stdio"
    
    if transport == "stdio":
        mcp.run(transport="stdio")
    else:
        port = int(os.getenv("PORT", 8123))
        mcp.run(transport="http", host="0.0.0.0", port=port)
