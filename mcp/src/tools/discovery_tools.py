"""Discovery document processing tools."""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import List, Dict

from models.document import Document, DocumentType
from core.state_manager import ProjectStateManager
from core.analyzer import DiscoveryAnalyzer


# Base path for test data
TEST_DATA_PATH = "/Users/codymenefee/Documents/Projects/offBench/mcp-servers/clients/shopify/offbench-shopify/test-data"


def register_discovery_tools(mcp):
    """Register all discovery tools with the MCP server."""
    
    @mcp.tool()
    def find_project_folders() -> List[Dict]:
        """
        Find all available project scenarios in the test-data directory.
        Returns list of projects with their metadata.
        """
        projects = []
        
        try:
            test_data_dir = Path(TEST_DATA_PATH)
            if not test_data_dir.exists():
                return {"error": f"Test data directory not found: {TEST_DATA_PATH}"}
            
            # Scan for scenario folders
            for folder in test_data_dir.iterdir():
                if folder.is_dir() and folder.name.startswith("scenario-"):
                    project_info = {
                        "project_id": folder.name,
                        "name": folder.name.replace("scenario-", "").replace("-", " ").title(),
                        "path": str(folder),
                        "description": ""
                    }
                    
                    # Try to read README for description
                    readme_path = folder / "README.md"
                    if readme_path.exists():
                        with open(readme_path, 'r') as f:
                            content = f.read()
                            # Extract first paragraph or business context
                            lines = content.split('\n')
                            for i, line in enumerate(lines):
                                if "Business Context" in line or "Context" in line:
                                    if i + 1 < len(lines):
                                        project_info["description"] = lines[i + 1].strip()
                                        break
                    
                    projects.append(project_info)
            
            return {
                "projects": projects,
                "count": len(projects),
                "message": f"Found {len(projects)} project scenario(s)"
            }
        
        except Exception as e:
            return {"error": f"Error scanning projects: {str(e)}"}
    
    
    @mcp.tool()
    def ingest_documents(project_id: str) -> Dict:
        """
        Load and parse all discovery documents from a project folder.
        
        Args:
            project_id: Project identifier (e.g., 'scenario-1-cozyhome')
        
        Returns:
            Summary of ingested documents and project state
        """
        try:
            project_path = Path(TEST_DATA_PATH) / project_id
            if not project_path.exists():
                return {"error": f"Project not found: {project_id}"}
            
            # Get or create project state
            state_manager = ProjectStateManager()
            
            # Read project name from README
            project_name = project_id.replace("scenario-", "").replace("-", " ").title()
            readme_path = project_path / "README.md"
            project_description = ""
            
            if readme_path.exists():
                with open(readme_path, 'r') as f:
                    content = f.read()
                    # Extract business context
                    match = re.search(r'## Business Context\s+(.+?)(?=\n##|\Z)', content, re.DOTALL)
                    if match:
                        project_description = match.group(1).strip()
            
            project = state_manager.get_or_create(
                project_id=project_id,
                project_name=project_name,
                project_description=project_description
            )
            
            # Clear existing documents
            project.documents = []
            
            # Scan for documents
            documents_found = []
            
            # Scan emails
            emails_dir = project_path / "emails"
            if emails_dir.exists():
                for file in emails_dir.glob("*.txt"):
                    doc = _parse_email(file)
                    project.add_document(doc)
                    documents_found.append({
                        "type": "email",
                        "file": file.name,
                        "subject": doc.subject
                    })
            
            # Scan transcripts
            transcripts_dir = project_path / "transcripts"
            if transcripts_dir.exists():
                for file in transcripts_dir.glob("*.txt"):
                    doc = _parse_transcript(file)
                    project.add_document(doc)
                    documents_found.append({
                        "type": "transcript",
                        "file": file.name
                    })
            
            # Scan client docs
            client_docs_dir = project_path / "client-docs"
            if client_docs_dir.exists():
                for file in client_docs_dir.glob("*.txt"):
                    doc = _parse_client_doc(file)
                    project.add_document(doc)
                    documents_found.append({
                        "type": "document",
                        "file": file.name
                    })
            
            # Update state
            state_manager.update_project(project)
            
            return {
                "project_id": project_id,
                "project_name": project_name,
                "documents_loaded": len(documents_found),
                "documents": documents_found,
                "message": f"Successfully loaded {len(documents_found)} documents for {project_name}"
            }
        
        except Exception as e:
            return {"error": f"Error ingesting documents: {str(e)}"}
    
    
    @mcp.tool()
    def analyze_discovery(project_id: str) -> Dict:
        """
        Analyze discovery documents for gaps, ambiguities, and conflicts.
        Calculate confidence score.
        
        Args:
            project_id: Project identifier
        
        Returns:
            Analysis results with confidence score and findings
        """
        try:
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            
            if not project:
                return {"error": f"Project not found: {project_id}. Run ingest_documents first."}
            
            if not project.documents:
                return {"error": f"No documents found for project: {project_id}"}
            
            # Run analysis
            analyzer = DiscoveryAnalyzer()
            analysis = analyzer.analyze(project.documents, project.additional_context)
            
            # Update project state
            project.update_analysis(analysis)
            state_manager.update_project(project)
            
            # Prepare response
            return {
                "project_id": project_id,
                "analysis": analysis.to_dict(),
                "summary": {
                    "confidence_score": round(analysis.overall_confidence, 1),
                    "gaps_found": len(analysis.gaps),
                    "ambiguities_found": len(analysis.ambiguities),
                    "conflicts_found": len(analysis.conflicts),
                    "systems_identified": analysis.systems_identified,
                    "client_name": analysis.client_name
                },
                "message": f"Analysis complete. Confidence score: {round(analysis.overall_confidence, 1)}%"
            }
        
        except Exception as e:
            return {"error": f"Error analyzing discovery: {str(e)}"}
    
    
    @mcp.tool()
    def extract_open_questions(project_id: str) -> Dict:
        """
        Generate prioritized clarifying questions from analysis.
        
        Args:
            project_id: Project identifier
        
        Returns:
            List of prioritized questions with context
        """
        try:
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            
            if not project:
                return {"error": f"Project not found: {project_id}"}
            
            if not project.analysis:
                return {"error": "No analysis found. Run analyze_discovery first."}
            
            questions = []
            
            # High priority gaps first
            high_priority_gaps = [g for g in project.analysis.gaps if g.priority.value == "high" and not g.answered]
            medium_priority_gaps = [g for g in project.analysis.gaps if g.priority.value == "medium" and not g.answered]
            low_priority_gaps = [g for g in project.analysis.gaps if g.priority.value == "low" and not g.answered]
            
            question_num = 1
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
            for ambiguity in project.analysis.ambiguities[:3]:
                questions.append({
                    "number": question_num,
                    "priority": ambiguity.priority.value.upper(),
                    "category": "clarity",
                    "question": f"Regarding '{ambiguity.term}': {ambiguity.clarification_needed}",
                    "why_it_matters": f"Context: {ambiguity.context}"
                })
                question_num += 1
            
            return {
                "project_id": project_id,
                "questions": questions,
                "total_questions": len(questions),
                "message": f"Generated {len(questions)} clarifying questions"
            }
        
        except Exception as e:
            return {"error": f"Error extracting questions: {str(e)}"}
    
    
    @mcp.tool()
    def update_project_context(project_id: str, new_information: str) -> Dict:
        """
        Add new information or answers to the project context.
        
        Args:
            project_id: Project identifier
            new_information: Additional context or answers from user
        
        Returns:
            Confirmation of update
        """
        try:
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            
            if not project:
                return {"error": f"Project not found: {project_id}"}
            
            # Add context
            project.add_context(new_information)
            
            # Try to match answers to gaps
            if project.analysis:
                new_info_lower = new_information.lower()
                
                for gap in project.analysis.gaps:
                    # Simple keyword matching to mark gaps as answered
                    gap_keywords = gap.description.lower().split()
                    if any(keyword in new_info_lower for keyword in gap_keywords if len(keyword) > 4):
                        gap.answered = True
                        gap.answer = new_information
            
            state_manager.update_project(project)
            
            return {
                "project_id": project_id,
                "context_added": True,
                "total_context_items": len(project.additional_context),
                "message": "Context updated successfully. Run recalculate_confidence to see impact."
            }
        
        except Exception as e:
            return {"error": f"Error updating context: {str(e)}"}
    
    
    @mcp.tool()
    def recalculate_confidence(project_id: str) -> Dict:
        """
        Re-run analysis with updated context and recalculate confidence score.
        
        Args:
            project_id: Project identifier
        
        Returns:
            New confidence score and improvement metrics
        """
        try:
            state_manager = ProjectStateManager()
            project = state_manager.get_project(project_id)
            
            if not project:
                return {"error": f"Project not found: {project_id}"}
            
            if not project.documents:
                return {"error": "No documents to analyze"}
            
            # Get previous confidence
            previous_confidence = None
            if project.analysis:
                previous_confidence = project.analysis.overall_confidence
            
            # Re-run analysis with additional context
            analyzer = DiscoveryAnalyzer()
            new_analysis = analyzer.analyze(project.documents, project.additional_context)
            
            # Update project state
            project.update_analysis(new_analysis)
            state_manager.update_project(project)
            
            # Calculate improvement
            improvement = None
            if previous_confidence is not None:
                improvement = new_analysis.overall_confidence - previous_confidence
            
            return {
                "project_id": project_id,
                "previous_confidence": round(previous_confidence, 1) if previous_confidence else None,
                "new_confidence": round(new_analysis.overall_confidence, 1),
                "improvement": round(improvement, 1) if improvement else None,
                "gaps_remaining": len([g for g in new_analysis.gaps if not g.answered]),
                "ambiguities_remaining": len(new_analysis.ambiguities),
                "conflicts_remaining": len(new_analysis.conflicts),
                "message": f"Confidence updated to {round(new_analysis.overall_confidence, 1)}%" + 
                          (f" (improved by {round(improvement, 1)}%)" if improvement and improvement > 0 else "")
            }
        
        except Exception as e:
            return {"error": f"Error recalculating confidence: {str(e)}"}


def _parse_email(file_path: Path) -> Document:
    """Parse an email file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract metadata from email headers
    metadata = {}
    participants = []
    subject = None
    date = None
    
    lines = content.split('\n')
    for line in lines[:10]:  # Check first 10 lines for headers
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
            # Try to parse date
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
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Extract participants from transcript (people speaking)
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


def _parse_client_doc(file_path: Path) -> Document:
    """Parse a client document file."""
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Determine doc type from filename
    filename_lower = file_path.name.lower()
    if 'sow' in filename_lower:
        doc_type = DocumentType.SOW
    elif 'guide' in filename_lower or 'brand' in filename_lower:
        doc_type = DocumentType.GUIDE
    elif 'notes' in filename_lower:
        doc_type = DocumentType.NOTES
    else:
        doc_type = DocumentType.OTHER
    
    return Document(
        file_path=str(file_path),
        content=content,
        doc_type=doc_type,
        metadata={}
    )

