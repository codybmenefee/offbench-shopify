"""Project state management."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

from .document import Document
from .analysis import AnalysisResult


@dataclass
class ProjectConfig:
    """Project configuration and settings."""
    
    confidence_threshold: float = 80.0
    custom_gap_patterns: List[Dict] = field(default_factory=list)
    priority_weights: Dict[str, float] = field(default_factory=lambda: {
        "business_rules": 1.0,
        "technical_constraints": 1.0,
        "edge_cases": 0.5,
        "success_criteria": 1.0,
        "error_handling": 1.0
    })
    auto_reanalyze: bool = True
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "confidence_threshold": self.confidence_threshold,
            "custom_gap_patterns": self.custom_gap_patterns,
            "priority_weights": self.priority_weights,
            "auto_reanalyze": self.auto_reanalyze
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ProjectConfig':
        """Create from dictionary."""
        return cls(
            confidence_threshold=data.get("confidence_threshold", 80.0),
            custom_gap_patterns=data.get("custom_gap_patterns", []),
            priority_weights=data.get("priority_weights", {}),
            auto_reanalyze=data.get("auto_reanalyze", True)
        )


@dataclass
class ProjectState:
    """Maintains state for a project across tool calls."""
    
    project_id: str
    project_name: str
    project_description: str = ""
    
    # Project configuration
    config: ProjectConfig = field(default_factory=ProjectConfig)
    
    # Discovery documents
    documents: List[Document] = field(default_factory=list)
    
    # Analysis results
    analysis: Optional[AnalysisResult] = None
    
    # Additional context from user
    additional_context: List[str] = field(default_factory=list)
    
    # Updates log (for traceability)
    updates_log: List[Dict] = field(default_factory=list)
    
    # Confidence history for tracking improvement
    confidence_history: List[Dict[str, float]] = field(default_factory=list)
    
    # Generated deliverables removed - AI agents now write deliverables on-the-fly
    # using templates as reference examples rather than storing filled versions
    
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
    
    def add_context(self, context: str, update_type: str = "context"):
        """Add additional context from user."""
        self.additional_context.append(context)
        self.updates_log.append({
            "type": update_type,
            "content": context,
            "timestamp": datetime.now().isoformat()
        })
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
            "config": self.config.to_dict(),
            "documents_count": len(self.documents),
            "analysis": self.analysis.to_dict() if self.analysis else None,
            "additional_context": self.additional_context,
            "updates_log": self.updates_log,
            "confidence_history": self.confidence_history,
            "created_at": self.created_at.isoformat(),
            "last_updated": self.last_updated.isoformat(),
        }

