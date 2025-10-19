"""Template filling logic for generating deliverables."""

import re
from typing import Dict, List, Optional
from models.project_state import ProjectState
from models.analysis import GapCategory


class TemplateFiller:
    """Fills templates with discovery data."""
    
    def fill(self, template: str, project_state: ProjectState) -> str:
        """Fill template with data from project state."""
        if not project_state.analysis:
            return template
        
        # Extract data
        data = self._extract_template_data(project_state)
        
        # Replace placeholders
        filled = template
        for placeholder, value in data.items():
            filled = filled.replace(f"[{placeholder}]", value)
        
        # Fill open questions section
        filled = self._fill_open_questions(filled, project_state)
        
        # Fill confidence score
        if project_state.analysis:
            confidence = str(round(project_state.analysis.overall_confidence, 1))
            filled = filled.replace("[CONFIDENCE_SCORE]", confidence)
        
        return filled
    
    def _extract_template_data(self, project_state: ProjectState) -> Dict[str, str]:
        """Extract data from project state for template filling."""
        analysis = project_state.analysis
        data = {}
        
        # Basic project info
        data["PROJECT_NAME"] = project_state.project_name
        data["CLIENT_NAME"] = analysis.client_name or project_state.project_name
        
        # Systems
        systems = analysis.systems_identified
        if len(systems) >= 2:
            data["SYSTEM_A"] = systems[0]
            data["SYSTEM_B"] = systems[1]
            data["INTEGRATION_TYPE"] = f"{systems[0]} to {systems[1]}"
        elif len(systems) == 1:
            data["SYSTEM_A"] = systems[0]
            data["SYSTEM_B"] = "[NEEDS_CLARIFICATION: Second system not identified]"
            data["INTEGRATION_TYPE"] = f"{systems[0]} Integration"
        else:
            data["SYSTEM_A"] = "[NEEDS_CLARIFICATION: Systems not identified]"
            data["SYSTEM_B"] = "[NEEDS_CLARIFICATION: Systems not identified]"
            data["INTEGRATION_TYPE"] = "[NEEDS_CLARIFICATION: Integration type not clear]"
        
        # Pain points
        if analysis.pain_points:
            pain_points_list = "\n".join([f"- {pp}" for pp in analysis.pain_points[:3]])
            data["PAIN_POINT_1"] = analysis.pain_points[0] if len(analysis.pain_points) > 0 else "Not specified"
            data["PAIN_POINT_2"] = analysis.pain_points[1] if len(analysis.pain_points) > 1 else "Not specified"
            data["PAIN_POINT_3"] = analysis.pain_points[2] if len(analysis.pain_points) > 2 else "Not specified"
            data["CURRENT_PAIN_POINTS"] = pain_points_list
        else:
            data["PAIN_POINT_1"] = "[NEEDS_CLARIFICATION: Pain points not documented]"
            data["PAIN_POINT_2"] = ""
            data["PAIN_POINT_3"] = ""
            data["CURRENT_PAIN_POINTS"] = "[NEEDS_CLARIFICATION: Pain points not documented]"
        
        # Business objectives
        if analysis.business_objectives:
            objectives_list = "\n".join([f"- {obj}" for obj in analysis.business_objectives[:3]])
            data["OBJECTIVE_1"] = analysis.business_objectives[0] if len(analysis.business_objectives) > 0 else "Not specified"
            data["OBJECTIVE_2"] = analysis.business_objectives[1] if len(analysis.business_objectives) > 1 else "Not specified"
            data["OBJECTIVE_3"] = analysis.business_objectives[2] if len(analysis.business_objectives) > 2 else "Not specified"
            data["BUSINESS_OBJECTIVES"] = objectives_list
        else:
            data["OBJECTIVE_1"] = "[NEEDS_CLARIFICATION: Business objectives not documented]"
            data["OBJECTIVE_2"] = ""
            data["OBJECTIVE_3"] = ""
            data["BUSINESS_OBJECTIVES"] = "[NEEDS_CLARIFICATION: Business objectives not documented]"
        
        # Business description
        if project_state.project_description:
            data["BUSINESS_DESCRIPTION"] = project_state.project_description
        else:
            data["BUSINESS_DESCRIPTION"] = f"a business using {data.get('SYSTEM_A', 'multiple systems')}"
        
        # Integration description
        if len(systems) >= 2:
            data["HIGH_LEVEL_INTEGRATION_DESCRIPTION"] = (
                f"This integration will connect {systems[0]} with {systems[1]} to enable "
                f"automated data synchronization and eliminate manual data entry."
            )
        else:
            data["HIGH_LEVEL_INTEGRATION_DESCRIPTION"] = "[NEEDS_CLARIFICATION: Integration details not clear]"
        
        # Current state
        if analysis.pain_points:
            data["CURRENT_STATE_DESCRIPTION"] = f"experiencing {analysis.pain_points[0] if analysis.pain_points else 'operational challenges'}"
        else:
            data["CURRENT_STATE_DESCRIPTION"] = "[NEEDS_CLARIFICATION: Current state not documented]"
        
        # Placeholders that need clarification if not found
        clarification_fields = [
            "PROJECT_ID", "CLIENT_CONTACT_NAME", "CLIENT_CONTACT_TITLE", "DATE",
            "TOTAL_TIMELINE", "TOTAL_COST", "MONTHLY_FEE", "SUPPORT_HOURS",
            "LEAD_ENGINEER", "PROJECT_MANAGER", "STATUS",
            "PHASE_1_DURATION", "PHASE_2_DURATION", "PHASE_3_DURATION",
            "PHASE_4_DURATION", "PHASE_5_DURATION",
            "TIME_SAVINGS", "ERROR_REDUCTION", "ROI_ESTIMATE",
        ]
        
        for field in clarification_fields:
            if field not in data:
                data[field] = f"[NEEDS_CLARIFICATION: {field.replace('_', ' ').title()}]"
        
        return data
    
    def _fill_open_questions(self, template: str, project_state: ProjectState) -> str:
        """Fill the open questions section."""
        if not project_state.analysis:
            return template
        
        questions = []
        
        # Add gap-based questions
        for i, gap in enumerate(project_state.analysis.gaps, 1):
            if gap.suggested_question and not gap.answered:
                questions.append(f"{i}. **{gap.category.value.replace('_', ' ').title()}**: {gap.suggested_question}")
                questions.append(f"   - *Why this matters*: {gap.impact}")
        
        # Add ambiguity-based questions
        for ambiguity in project_state.analysis.ambiguities:
            questions.append(f"- **Ambiguous term '{ambiguity.term}'**: {ambiguity.clarification_needed}")
            questions.append(f"   - *Context*: {ambiguity.context}")
        
        # Add conflict-based questions
        for conflict in project_state.analysis.conflicts:
            questions.append(f"- **Conflicting information about {conflict.topic}**: {conflict.resolution_needed}")
        
        if questions:
            questions_text = "\n".join(questions)
        else:
            questions_text = "No open questions - all requirements are clear."
        
        # Replace [OPEN_QUESTIONS] placeholder
        template = template.replace("[OPEN_QUESTIONS]", questions_text)
        
        return template
    
    def generate_data_sync_table(self, project_state: ProjectState) -> str:
        """Generate data synchronization table for SOW."""
        if not project_state.analysis:
            return "[NEEDS_CLARIFICATION: Data sync details not available]"
        
        systems = project_state.analysis.systems_identified
        if len(systems) < 2:
            return "[NEEDS_CLARIFICATION: Systems not fully identified]"
        
        # Default data types based on common integrations
        data_types = [
            ("Orders", systems[0], systems[1], "Every 15 minutes", "Create invoices/records"),
            ("Inventory Levels", "[TO BE DETERMINED]", "[TO BE DETERMINED]", "Every 30 minutes", "Prevent overselling"),
            ("Customer Data", systems[0], systems[1], "Real-time (on create/update)", "Sync contact information"),
        ]
        
        table_rows = []
        for data_type, source, dest, freq, notes in data_types:
            table_rows.append(f"| {data_type} | {source} | {dest} | {freq} | {notes} |")
        
        return "\n".join(table_rows)

