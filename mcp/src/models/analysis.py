"""Analysis result data models."""

from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class GapCategory(Enum):
    """Categories of gaps in discovery."""
    BUSINESS_RULES = "business_rules"
    TECHNICAL_CONSTRAINTS = "technical_constraints"
    EDGE_CASES = "edge_cases"
    SUCCESS_CRITERIA = "success_criteria"
    DATA_FLOWS = "data_flows"
    ERROR_HANDLING = "error_handling"


class Priority(Enum):
    """Priority levels for gaps and questions."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


@dataclass
class Gap:
    """Represents missing information in discovery."""
    
    category: GapCategory
    description: str
    impact: str
    priority: Priority
    suggested_question: Optional[str] = None
    answered: bool = False
    answer: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "category": self.category.value,
            "description": self.description,
            "impact": self.impact,
            "priority": self.priority.value,
            "suggested_question": self.suggested_question,
            "answered": self.answered,
            "answer": self.answer,
        }


@dataclass
class Ambiguity:
    """Represents ambiguous or vague requirements."""
    
    term: str
    context: str
    clarification_needed: str
    priority: Priority
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "term": self.term,
            "context": self.context,
            "clarification_needed": self.clarification_needed,
            "priority": self.priority.value,
        }


@dataclass
class Conflict:
    """Represents conflicting information between stakeholders."""
    
    topic: str
    conflicting_statements: List[str]
    sources: List[str]
    resolution_needed: str
    priority: Priority
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "topic": self.topic,
            "conflicting_statements": self.conflicting_statements,
            "sources": self.sources,
            "resolution_needed": self.resolution_needed,
            "priority": self.priority.value,
        }


@dataclass
class AnalysisResult:
    """Complete analysis of discovery documents."""
    
    gaps: List[Gap] = field(default_factory=list)
    ambiguities: List[Ambiguity] = field(default_factory=list)
    conflicts: List[Conflict] = field(default_factory=list)
    
    # Confidence scores (0-100)
    clarity_score: float = 100.0
    completeness_score: float = 100.0
    alignment_score: float = 100.0
    overall_confidence: float = 100.0
    
    # Extracted information
    systems_identified: List[str] = field(default_factory=list)
    client_name: Optional[str] = None
    pain_points: List[str] = field(default_factory=list)
    business_objectives: List[str] = field(default_factory=list)
    
    def calculate_confidence(self):
        """Calculate overall confidence score."""
        # Clarity: fewer ambiguities = higher score
        self.clarity_score = max(0, 100 - (len(self.ambiguities) * 5))
        
        # Completeness: fewer gaps = higher score
        self.completeness_score = max(0, 100 - (len(self.gaps) * 10))
        
        # Alignment: fewer conflicts = higher score
        self.alignment_score = max(0, 100 - (len(self.conflicts) * 15))
        
        # Weighted overall score
        self.overall_confidence = (
            self.clarity_score * 0.4 +
            self.completeness_score * 0.4 +
            self.alignment_score * 0.2
        )
        
        return self.overall_confidence
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "gaps": [g.to_dict() for g in self.gaps],
            "ambiguities": [a.to_dict() for a in self.ambiguities],
            "conflicts": [c.to_dict() for c in self.conflicts],
            "clarity_score": round(self.clarity_score, 1),
            "completeness_score": round(self.completeness_score, 1),
            "alignment_score": round(self.alignment_score, 1),
            "overall_confidence": round(self.overall_confidence, 1),
            "systems_identified": self.systems_identified,
            "client_name": self.client_name,
            "pain_points": self.pain_points,
            "business_objectives": self.business_objectives,
        }

