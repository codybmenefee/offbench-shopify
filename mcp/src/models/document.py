"""Document data model."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List


class DocumentType(Enum):
    """Types of discovery documents."""
    EMAIL = "email"
    TRANSCRIPT = "transcript"
    SOW = "sow"
    GUIDE = "guide"
    NOTES = "notes"
    OTHER = "other"


@dataclass
class Document:
    """Represents a discovery document."""
    
    file_path: str
    content: str
    doc_type: DocumentType
    metadata: dict = field(default_factory=dict)
    
    # Optional extracted metadata
    date: Optional[datetime] = None
    participants: List[str] = field(default_factory=list)
    subject: Optional[str] = None
    
    # New fields for integration-based storage
    external_id: Optional[str] = None  # Google Drive file ID
    external_url: Optional[str] = None  # Merge API URL
    integration_id: Optional[str] = None  # Integration ID
    summary: Optional[str] = None  # AI-generated summary (from agent)
    source: str = "local"  # "local", "integration", "upload"
    convex_document_id: Optional[str] = None  # Convex document ID for updates
    
    def __post_init__(self):
        """Ensure doc_type is DocumentType enum."""
        if isinstance(self.doc_type, str):
            self.doc_type = DocumentType(self.doc_type)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "file_path": self.file_path,
            "content": self.content,
            "doc_type": self.doc_type.value,
            "metadata": self.metadata,
            "date": self.date.isoformat() if self.date else None,
            "participants": self.participants,
            "subject": self.subject,
            # New fields for integration-based storage
            "external_id": self.external_id,
            "external_url": self.external_url,
            "integration_id": self.integration_id,
            "summary": self.summary,
            "source": self.source,
            "convex_document_id": self.convex_document_id,
        }

