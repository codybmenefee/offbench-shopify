"""High-level data sync operations for Convex."""

import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from .convex_client import ConvexClient
from models.project_state import ProjectState
from models.analysis import Gap, Ambiguity, Conflict
from config import config


class ConvexSync:
    """High-level sync operations for pushing MCP data to Convex."""

    def __init__(self, client: Optional[ConvexClient] = None):
        """
        Initialize sync manager.
        
        Args:
            client: Optional ConvexClient instance (creates new one if not provided)
        """
        self.client = client or ConvexClient()
        self._owns_client = client is None

    def _map_priority(self, priority_value: str) -> str:
        """Map MCP priority to frontend priority format."""
        return priority_value.lower()

    def _map_impact(self, priority_value: str) -> str:
        """Map MCP priority to frontend impact format (same mapping)."""
        return priority_value.lower()

    def _get_file_size(self, file_path: str) -> str:
        """Get human-readable file size."""
        try:
            size_bytes = os.path.getsize(file_path)
            for unit in ['B', 'KB', 'MB', 'GB']:
                if size_bytes < 1024.0:
                    return f"{size_bytes:.1f} {unit}"
                size_bytes /= 1024.0
            return f"{size_bytes:.1f} TB"
        except:
            return "Unknown"

    def sync_project_metadata(self, project: ProjectState) -> str:
        """
        Sync project metadata to Convex.
        
        Args:
            project: ProjectState instance
            
        Returns:
            Convex project ID
        """
        # Calculate counts from analysis
        gaps_count = len(project.analysis.gaps) if project.analysis else 0
        conflicts_count = len(project.analysis.conflicts) if project.analysis else 0
        ambiguities_count = len(project.analysis.ambiguities) if project.analysis else 0
        documents_count = len(project.documents)
        
        # Determine status (default to active for now)
        status = "active"
        
        project_data = {
            "scenarioId": project.project_id,
            "name": project.project_name,
            "confidence": round(project.analysis.overall_confidence, 1) if project.analysis else 0.0,
            "gapsCount": gaps_count,
            "conflictsCount": conflicts_count,
            "ambiguitiesCount": ambiguities_count,
            "documentsCount": documents_count,
            "status": status,
        }
        
        project_id = self.client.mutation(
            "mutations/projects:upsertProject",
            project_data
        )
        
        return project_id

    def sync_gaps(self, project_convex_id: str, gaps: List[Gap], identified_date: Optional[datetime] = None) -> List[str]:
        """
        Sync gaps to Convex.
        
        Args:
            project_convex_id: Convex project ID
            gaps: List of Gap objects
            identified_date: When gaps were identified
            
        Returns:
            List of gap IDs
        """
        if not gaps:
            return []
        
        timestamp = int((identified_date or datetime.now()).timestamp() * 1000)
        
        gaps_data = []
        for gap in gaps:
            gap_dict = {
                "category": gap.category.value,
                "description": gap.description,
                "impact": self._map_impact(gap.priority.value),
                "priority": self._map_priority(gap.priority.value),
                "status": "resolved" if gap.answered else "open",
                "identifiedDate": timestamp,
            }
            
            if gap.suggested_question:
                gap_dict["suggestedQuestion"] = gap.suggested_question
            
            gaps_data.append(gap_dict)
        
        result = self.client.mutation(
            "mutations/gaps:syncGaps",
            {
                "projectId": project_convex_id,
                "gaps": gaps_data
            }
        )
        
        return result

    def sync_conflicts(self, project_convex_id: str, conflicts: List[Conflict], identified_date: Optional[datetime] = None) -> List[str]:
        """
        Sync conflicts to Convex.
        
        Args:
            project_convex_id: Convex project ID
            conflicts: List of Conflict objects
            identified_date: When conflicts were identified
            
        Returns:
            List of conflict IDs
        """
        if not conflicts:
            return []
        
        timestamp = int((identified_date or datetime.now()).timestamp() * 1000)
        
        conflicts_data = []
        for conflict in conflicts:
            conflict_dict = {
                "category": conflict.topic,
                "description": conflict.resolution_needed,
                "impact": self._map_impact(conflict.priority.value),
                "priority": self._map_priority(conflict.priority.value),
                "status": "open",
                "identifiedDate": timestamp,
                "conflictingStatements": conflict.conflicting_statements,
                "sources": conflict.sources,
            }
            conflicts_data.append(conflict_dict)
        
        result = self.client.mutation(
            "mutations/conflicts:syncConflicts",
            {
                "projectId": project_convex_id,
                "conflicts": conflicts_data
            }
        )
        
        return result

    def sync_ambiguities(self, project_convex_id: str, ambiguities: List[Ambiguity], identified_date: Optional[datetime] = None) -> List[str]:
        """
        Sync ambiguities to Convex.
        
        Args:
            project_convex_id: Convex project ID
            ambiguities: List of Ambiguity objects
            identified_date: When ambiguities were identified
            
        Returns:
            List of ambiguity IDs
        """
        if not ambiguities:
            return []
        
        timestamp = int((identified_date or datetime.now()).timestamp() * 1000)
        
        ambiguities_data = []
        for ambiguity in ambiguities:
            ambiguity_dict = {
                "category": "clarity",  # Default category
                "description": ambiguity.term,
                "impact": self._map_impact(ambiguity.priority.value),
                "clarificationNeeded": ambiguity.clarification_needed,
                "status": "open",
                "identifiedDate": timestamp,
                "context": ambiguity.context,
            }
            ambiguities_data.append(ambiguity_dict)
        
        result = self.client.mutation(
            "mutations/ambiguities:syncAmbiguities",
            {
                "projectId": project_convex_id,
                "ambiguities": ambiguities_data
            }
        )
        
        return result

    def sync_questions(self, project_convex_id: str, questions: List[Dict[str, Any]]) -> List[str]:
        """
        Sync extracted questions to Convex.
        
        Args:
            project_convex_id: Convex project ID
            questions: List of question dicts from _extract_questions_from_analysis
            
        Returns:
            List of question IDs
        """
        if not questions:
            return []
        
        questions_data = []
        for q in questions:
            question_dict = {
                "question": q["question"],
                "category": q.get("category", "general"),
                "priority": q.get("priority", "medium").lower(),
                "status": "open",
                "askedDate": int(datetime.now().timestamp() * 1000),
            }
            
            if "why_it_matters" in q:
                question_dict["whyItMatters"] = q["why_it_matters"]
            
            questions_data.append(question_dict)
        
        result = self.client.mutation(
            "mutations/questions:syncQuestions",
            {
                "projectId": project_convex_id,
                "questions": questions_data
            }
        )
        
        return result

    def sync_documents(self, project_convex_id: str, project: ProjectState) -> List[str]:
        """
        Sync document metadata to Convex.
        
        Args:
            project_convex_id: Convex project ID
            project: ProjectState instance
            
        Returns:
            List of document IDs
        """
        if not project.documents:
            return []
        
        documents_data = []
        for doc in project.documents:
            # Mock Google Drive link for now
            source_link = f"https://drive.google.com/file/d/mock_{project.project_id}_{doc.file_path}"
            
            doc_dict = {
                "name": os.path.basename(doc.file_path),
                "type": doc.doc_type.value,
                "uploadDate": int(doc.date.timestamp() * 1000) if doc.date else int(datetime.now().timestamp() * 1000),
                "size": self._get_file_size(doc.file_path) if os.path.exists(doc.file_path) else "Unknown",
                "status": "processed",
                "sourceLink": source_link,
                "metadata": doc.metadata,
            }
            documents_data.append(doc_dict)
        
        result = self.client.mutation(
            "mutations/documents:syncDocuments",
            {
                "projectId": project_convex_id,
                "documents": documents_data
            }
        )
        
        return result

    def log_event(
        self,
        project_convex_id: str,
        event_type: str,
        description: str,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Log a context event to Convex timeline.
        
        Args:
            project_convex_id: Convex project ID
            event_type: Event type (e.g., "analysis_completed")
            description: Human-readable description
            metadata: Optional additional data
            
        Returns:
            Event ID
        """
        event_id = self.client.mutation(
            "mutations/events:logEvent",
            {
                "projectId": project_convex_id,
                "eventType": event_type,
                "description": description,
                "metadata": metadata,
            }
        )
        
        return event_id

    def sync_full_project(self, project: ProjectState) -> Dict[str, Any]:
        """
        Sync all project data to Convex.
        
        Args:
            project: ProjectState instance
            
        Returns:
            Dictionary with sync results
        """
        # 1. Sync project metadata (returns Convex ID)
        project_id = self.sync_project_metadata(project)
        
        results = {
            "project_id": project_id,
            "project_name": project.project_name,
        }
        
        # 2. Sync analysis results if available
        if project.analysis:
            results["gaps"] = self.sync_gaps(project_id, project.analysis.gaps)
            results["conflicts"] = self.sync_conflicts(project_id, project.analysis.conflicts)
            results["ambiguities"] = self.sync_ambiguities(project_id, project.analysis.ambiguities)
        
        # 3. Sync documents
        results["documents"] = self.sync_documents(project_id, project)
        
        # 4. Log sync event
        self.log_event(
            project_id,
            "analysis_completed",
            f"Full project sync completed for {project.project_name}",
            {"confidence": project.analysis.overall_confidence if project.analysis else 0}
        )
        
        return results

    def close(self):
        """Close the Convex client if owned by this sync manager."""
        if self._owns_client:
            self.client.close()

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()

