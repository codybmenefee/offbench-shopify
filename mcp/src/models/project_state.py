"""Project state management."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

from .document import Document
from .analysis import AnalysisResult


@dataclass
class ProjectState:
    """Maintains state for a project across tool calls."""
    
    project_id: str
    project_name: str
    project_description: str = ""
    
    # Discovery documents
    documents: List[Document] = field(default_factory=list)
    
    # Analysis results
    analysis: Optional[AnalysisResult] = None
    
    # Additional context from user
    additional_context: List[str] = field(default_factory=list)
    
    # Confidence history for tracking improvement
    confidence_history: List[Dict[str, float]] = field(default_factory=list)
    
    # Generated deliverables
    generated_sow: Optional[str] = None
    generated_implementation_plan: Optional[str] = None
    generated_technical_specs: Optional[str] = None
    
    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    
    def add_document(self, document: Document):
        """Add a document to the project."""
        self.documents.append(document)
        self.last_updated = datetime.now()
    
    def update_analysis(self, analysis: AnalysisResult):
        """Update analysis and track confidence history."""
        self.analysis = analysis
        self.confidence_history.append({
            "timestamp": datetime.now().isoformat(),
            "overall_confidence": analysis.overall_confidence,
            "clarity_score": analysis.clarity_score,
            "completeness_score": analysis.completeness_score,
            "alignment_score": analysis.alignment_score,
        })
        self.last_updated = datetime.now()
    
    def add_context(self, context: str):
        """Add additional context from user."""
        self.additional_context.append(context)
        self.last_updated = datetime.now()
    
    def get_confidence_improvement(self) -> Optional[float]:
        """Calculate confidence improvement from first to last analysis."""
        if len(self.confidence_history) < 2:
            return None
        first = self.confidence_history[0]["overall_confidence"]
        last = self.confidence_history[-1]["overall_confidence"]
        return last - first
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "project_description": self.project_description,
            "documents_count": len(self.documents),
            "analysis": self.analysis.to_dict() if self.analysis else None,
            "additional_context": self.additional_context,
            "confidence_history": self.confidence_history,
            "has_sow": self.generated_sow is not None,
            "has_implementation_plan": self.generated_implementation_plan is not None,
            "has_technical_specs": self.generated_technical_specs is not None,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }

