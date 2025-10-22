"""High-level data sync operations for Convex."""

import os
from typing import Dict, List, Optional, Any, Tuple
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

    def _tenant_context(self) -> Dict[str, Any]:
        ctx: Dict[str, Any] = {}
        if getattr(config, "MCP_USER_ID", None):
            ctx["userId"] = config.MCP_USER_ID
        if getattr(config, "MCP_ORG_ID", None):
            ctx["orgId"] = config.MCP_ORG_ID
        return ctx

    def _ensure_project(self, scenario_id: str, name: str) -> str:
        """Find or create a project in the portal's Convex, returns Convex project id."""
        # Try to find by scenarioId via portal query
        existing = None
        try:
            existing = self.client.query(
                "queries/projects:getByScenarioId",
                {"scenarioId": scenario_id}
            )
        except Exception:
            # Some portals use getProjectByScenarioId; fall back to that
            try:
                existing = self.client.query(
                    "queries/projects:getProjectByScenarioId",
                    {"scenarioId": scenario_id}
                )
            except Exception:
                existing = None

        if existing and existing.get("_id"):
            return existing["_id"]

        # Create new project with required fields; let portal defaults init counts
        create_args = {
            "name": name,
            "scenarioId": scenario_id,
            "status": "active",
            **self._tenant_context(),
        }
        project_id = self.client.mutation("mutations/projects:create", create_args)
        # Some portals return {_id: ...}, others return id directly
        if isinstance(project_id, dict) and project_id.get("_id"):
            return project_id["_id"]
        return project_id

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
        # Ensure project exists, then update confidence via portal mutation
        project_id = self._ensure_project(project.project_id, project.project_name)

        confidence = round(project.analysis.overall_confidence, 1) if project.analysis else 0.0
        try:
            self.client.mutation(
                "mutations/projects:update",
                {"id": project_id, "confidence": confidence, **self._tenant_context()}
            )
            # Log confidence update for timeline visibility
            try:
                self.log_event(
                    project_id,
                    "confidence_updated",
                    f"Confidence updated to {confidence}",
                    {"confidence": confidence}
                )
            except Exception:
                pass
        except Exception:
            # Some portals expose a recalculateConfidence or updateConfidence; try a fallback
            try:
                self.client.mutation(
                    "mutations/projects:recalculateConfidence",
                    {"id": project_id, "confidence": confidence, **self._tenant_context()}
                )
            except Exception:
                # Best effort; continue
                pass

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
        
        created_ids: List[str] = []
        for gap in gaps:
            args = {
                "projectId": project_convex_id,
                "category": gap.category.value,
                "description": gap.description,
                "impact": self._map_impact(gap.priority.value),
                "priority": self._map_priority(gap.priority.value),
                "status": "resolved" if gap.answered else "open",
                "identifiedDate": timestamp,
                **self._tenant_context(),
            }
            if gap.suggested_question:
                args["suggestedQuestion"] = gap.suggested_question
            gap_id = self.client.mutation("mutations/gaps:create", args)
            created_ids.append(gap_id if isinstance(gap_id, str) else gap_id.get("_id", gap_id))
        return created_ids

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
        
        created_ids: List[str] = []
        for conflict in conflicts:
            args = {
                "projectId": project_convex_id,
                "category": conflict.topic,
                "description": conflict.resolution_needed,
                "impact": self._map_impact(conflict.priority.value),
                "priority": self._map_priority(conflict.priority.value),
                "status": "open",
                "identifiedDate": timestamp,
                "conflictingStatements": conflict.conflicting_statements,
                "sources": conflict.sources,
                **self._tenant_context(),
            }
            conflict_id = self.client.mutation("mutations/conflicts:create", args)
            created_ids.append(conflict_id if isinstance(conflict_id, str) else conflict_id.get("_id", conflict_id))
        return created_ids

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
        
        created_ids: List[str] = []
        for ambiguity in ambiguities:
            args = {
                "projectId": project_convex_id,
                "category": "clarity",
                "description": ambiguity.term,
                "impact": self._map_impact(ambiguity.priority.value),
                "clarificationNeeded": ambiguity.clarification_needed,
                "status": "open",
                "identifiedDate": timestamp,
                "context": ambiguity.context,
                **self._tenant_context(),
            }
            amb_id = self.client.mutation("mutations/ambiguities:create", args)
            created_ids.append(amb_id if isinstance(amb_id, str) else amb_id.get("_id", amb_id))
        return created_ids

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
        
        created_ids: List[str] = []
        for q in questions:
            args = {
                "projectId": project_convex_id,
                "question": q["question"],
                "category": q.get("category", "general"),
                "priority": q.get("priority", "medium").lower(),
                "status": "open",
                "askedDate": int(datetime.now().timestamp() * 1000),
                **self._tenant_context(),
            }
            if "why_it_matters" in q:
                args["whyItMatters"] = q["why_it_matters"]
            q_id = self.client.mutation("mutations/questions:add", args)
            created_ids.append(q_id if isinstance(q_id, str) else q_id.get("_id", q_id))
        return created_ids

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
        
        created_ids: List[str] = []
        for doc in project.documents:
            upload_ts = int(doc.date.timestamp() * 1000) if getattr(doc, "date", None) else int(datetime.now().timestamp() * 1000)
            size_bytes: Optional[int] = None
            try:
                size_bytes = os.path.getsize(doc.file_path) if os.path.exists(doc.file_path) else None
            except Exception:
                size_bytes = None

            args = {
                "projectId": project_convex_id,
                "name": os.path.basename(doc.file_path),
                "type": doc.doc_type.value,
                "uploadDate": upload_ts,
                "size": size_bytes if size_bytes is not None else 0,
                "status": "processed",
                "source": "upload",
                "metadata": doc.metadata,
                **self._tenant_context(),
            }
            doc_id = self.client.mutation("mutations/documents:create", args)
            created_ids.append(doc_id if isinstance(doc_id, str) else doc_id.get("_id", doc_id))
        return created_ids

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
            "mutations/contextEvents:create",
            {
                "projectId": project_convex_id,
                "eventType": event_type,
                "description": description,
                "metadata": metadata,
                **self._tenant_context(),
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
        # Log analysis completed event
        try:
            self.log_event(
                project_id,
                "analysis_completed",
                f"Full project sync completed for {project.project_name}",
                {"confidence": project.analysis.overall_confidence if project.analysis else 0}
            )
        except Exception:
            pass
        
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
