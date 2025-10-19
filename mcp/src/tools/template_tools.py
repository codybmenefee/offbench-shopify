"""Template management and filling tools."""

from pathlib import Path
from typing import Dict

from core.state_manager import ProjectStateManager
from core.template_filler import TemplateFiller


# Base path for templates
TEMPLATES_PATH = "/Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify/templates"


def register_template_tools(mcp):
    """Register all template tools with the MCP server."""
    
    @mcp.tool()
    def get_template(template_type: str) -> Dict:
        """
        Get template content from the templates directory.
        
        Args:
            template_type: Type of template ('sow', 'implementation-plan', 'technical-specs')
        
        Returns:
            Template content as string
        """
        try:
            template_files = {
                "sow": "client-facing-sow.md",
                "implementation-plan": "internal-implementation-plan.md",
                "implementation_plan": "internal-implementation-plan.md",
                "technical-specs": "internal-technical-specs.md",
                "technical_specs": "internal-technical-specs.md",
            }
            
            if template_type not in template_files:
                return {
                    "error": f"Unknown template type: {template_type}. "
                            f"Available: {', '.join(set(template_files.values()))}"
                }
            
            template_file = template_files[template_type]
            template_path = Path(TEMPLATES_PATH) / template_file
            
            if not template_path.exists():
                return {"error": f"Template file not found: {template_path}"}
            
            with open(template_path, 'r') as f:
                content = f.read()
            
            return {
                "template_type": template_type,
                "template_file": template_file,
                "content": content,
                "length": len(content),
                "message": f"Template loaded: {template_file}"
            }
        
        except Exception as e:
            return {"error": f"Error loading template: {str(e)}"}
    
    
    @mcp.tool()
    def fill_template(project_id: str, template_type: str) -> Dict:
        """
        Fill a template with project discovery data.
        
        Args:
            project_id: Project identifier
            template_type: Type of template to fill ('sow', 'implementation-plan', 'technical-specs')
        
        Returns:
            Filled template content
        """
        try:
            # Get project state
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            
            if not project:
                return {"error": f"Project not found: {project_id}"}
            
            if not project.analysis:
                return {
                    "error": "No analysis found. Run analyze_discovery first.",
                    "hint": "You need to analyze the discovery documents before generating templates."
                }
            
            # Get template
            template_result = get_template(template_type)
            if "error" in template_result:
                return template_result
            
            template_content = template_result["content"]
            
            # Fill template
            filler = TemplateFiller()
            filled_content = filler.fill(template_content, project)
            
            # Store in project state
            if template_type in ["sow"]:
                project.generated_sow = filled_content
            elif template_type in ["implementation-plan", "implementation_plan"]:
                project.generated_implementation_plan = filled_content
            elif template_type in ["technical-specs", "technical_specs"]:
                project.generated_technical_specs = filled_content
            
            state_manager.update_project(project)
            
            # Count placeholders still needing clarification
            needs_clarification_count = filled_content.count("[NEEDS_CLARIFICATION:")
            
            return {
                "project_id": project_id,
                "template_type": template_type,
                "filled_content": filled_content,
                "length": len(filled_content),
                "needs_clarification_count": needs_clarification_count,
                "confidence_score": round(project.analysis.overall_confidence, 1),
                "message": f"Template filled. {needs_clarification_count} items need clarification."
            }
        
        except Exception as e:
            return {"error": f"Error filling template: {str(e)}"}
    
    
    @mcp.tool()
    def save_filled_template(project_id: str, template_type: str, 
                            output_path: str = None) -> Dict:
        """
        Save a filled template to disk.
        
        Args:
            project_id: Project identifier
            template_type: Type of template ('sow', 'implementation-plan', 'technical-specs')
            output_path: Optional custom output path (defaults to test-data/project_id/)
        
        Returns:
            Confirmation with file path
        """
        try:
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            
            if not project:
                return {"error": f"Project not found: {project_id}"}
            
            # Get filled content from project state
            content = None
            default_filename = None
            
            if template_type == "sow":
                content = project.generated_sow
                default_filename = f"{project_id}-sow.md"
            elif template_type in ["implementation-plan", "implementation_plan"]:
                content = project.generated_implementation_plan
                default_filename = f"{project_id}-implementation-plan.md"
            elif template_type in ["technical-specs", "technical_specs"]:
                content = project.generated_technical_specs
                default_filename = f"{project_id}-technical-specs.md"
            
            if not content:
                return {
                    "error": f"No filled {template_type} found. Run fill_template first."
                }
            
            # Determine output path
            if output_path:
                file_path = Path(output_path)
            else:
                # Default to project test-data folder
                project_dir = Path("/Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify/test-data") / project_id
                file_path = project_dir / default_filename
            
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Write file
            with open(file_path, 'w') as f:
                f.write(content)
            
            return {
                "project_id": project_id,
                "template_type": template_type,
                "file_path": str(file_path),
                "message": f"Template saved to {file_path}"
            }
        
        except Exception as e:
            return {"error": f"Error saving template: {str(e)}"}

