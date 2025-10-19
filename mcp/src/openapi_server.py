"""
OpenAPI REST wrapper for ChatGPT Actions.
This wraps the MCP tools in REST endpoints with OpenAPI spec.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.state_manager import ProjectStateManager
from core.analyzer import DiscoveryAnalyzer
from models.document import Document, DocumentType

app = FastAPI(
    title="Discovery Agent API",
    description="Discovery to Implementation Confidence Tool - REST API for ChatGPT Actions",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS for ChatGPT
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://chatgpt.com", "https://chat.openai.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import the helper functions and paths from main.py
BASE_PATH = Path(__file__).parent.parent.parent
TEST_DATA_PATH = str(BASE_PATH / "test-data")
TEMPLATES_PATH = str(BASE_PATH / "templates")


# === ENDPOINTS ===

@app.get("/")
def root():
    """Root endpoint with API info."""
    return {
        "name": "Discovery Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }


@app.get("/projects")
def list_projects():
    """List all available project scenarios."""
    projects = []
    test_data_dir = Path(TEST_DATA_PATH)
    
    for folder in test_data_dir.iterdir():
        if folder.is_dir() and folder.name.startswith("scenario-"):
            projects.append({
                "project_id": folder.name,
                "name": folder.name.replace("scenario-", "").replace("-", " ").title()
            })
    
    return {"projects": projects}


@app.post("/projects/{project_id}/ingest")
def ingest_project(project_id: str):
    """Load and analyze discovery documents for a project."""
    from main import _parse_email, _parse_transcript, _parse_client_doc
    
    project_path = Path(TEST_DATA_PATH) / project_id
    if not project_path.exists():
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    
    state_manager = ProjectStateManager()
    project = state_manager.get_or_create(
        project_id=project_id,
        project_name=project_id.replace("scenario-", "").replace("-", " ").title()
    )
    
    project.documents = []
    doc_count = 0
    
    # Scan for documents
    for doc_type_dir, parser in [
        ("emails", _parse_email),
        ("transcripts", _parse_transcript),
        ("client-docs", _parse_client_doc)
    ]:
        dir_path = project_path / doc_type_dir
        if dir_path.exists():
            for file in dir_path.glob("*.txt"):
                doc = parser(file)
                project.add_document(doc)
                doc_count += 1
    
    state_manager.update_project(project)
    
    return {
        "project_id": project_id,
        "documents_loaded": doc_count,
        "message": f"Loaded {doc_count} documents"
    }


@app.get("/projects/{project_id}/analysis")
def get_analysis(project_id: str):
    """Get analysis results for a project."""
    state_manager = ProjectStateManager()
    project = state_manager.get_project(project_id)
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found. Call /ingest first.")
    
    if not project.documents:
        raise HTTPException(status_code=400, detail="No documents loaded. Call /ingest first.")
    
    # Run analysis
    analyzer = DiscoveryAnalyzer()
    analysis = analyzer.analyze(project.documents, project.additional_context)
    
    project.update_analysis(analysis)
    state_manager.update_project(project)
    
    return {
        "project_id": project_id,
        "confidence_score": round(analysis.overall_confidence, 1),
        "systems": analysis.systems_identified,
        "client_name": analysis.client_name,
        "gaps": len(analysis.gaps),
        "ambiguities": len(analysis.ambiguities),
        "conflicts": len(analysis.conflicts)
    }


@app.get("/projects/{project_id}/questions")
def get_questions(project_id: str):
    """Get clarifying questions for a project."""
    state_manager = ProjectStateManager()
    project = state_manager.get_project(project_id)
    
    if not project or not project.analysis:
        raise HTTPException(status_code=404, detail="Run analysis first")
    
    questions = []
    for gap in project.analysis.gaps:
        if not gap.answered and gap.suggested_question:
            questions.append({
                "priority": gap.priority.value,
                "category": gap.category.value,
                "question": gap.suggested_question,
                "impact": gap.impact
            })
    
    return {"questions": questions[:10]}


class DeliverableResponse(BaseModel):
    project_id: str
    template_type: str
    content: str
    confidence_score: float


@app.get("/projects/{project_id}/deliverable/{template_type}", response_model=DeliverableResponse)
def generate_deliverable(project_id: str, template_type: str):
    """
    Generate a deliverable document (SOW, implementation plan, or technical specs).
    Returns the filled template content.
    """
    from main import _detect_integration_type
    
    if template_type not in ["sow", "implementation-plan", "technical-specs"]:
        raise HTTPException(status_code=400, detail="Invalid template type")
    
    state_manager = ProjectStateManager()
    project = state_manager.get_project(project_id)
    
    if not project or not project.analysis:
        raise HTTPException(status_code=404, detail="Run analysis first")
    
    # Load template
    template_files = {
        "sow": "client-facing-sow.md",
        "implementation-plan": "internal-implementation-plan.md",
        "technical-specs": "internal-technical-specs.md"
    }
    
    template_path = Path(TEMPLATES_PATH) / template_files[template_type]
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Detect integration type
    integration_type = _detect_integration_type(
        project.analysis.systems_identified,
        "\n".join([doc.content for doc in project.documents])
    )
    
    # Return structured data for ChatGPT to fill
    return {
        "project_id": project_id,
        "template_type": template_type,
        "content": template,
        "confidence_score": project.analysis.overall_confidence
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8124)

