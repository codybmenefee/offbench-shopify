"""Discovery document analyzer."""

import re
from typing import List
from models.document import Document
from models.analysis import (
    AnalysisResult, Gap, Ambiguity, Conflict,
    GapCategory, Priority
)


class DiscoveryAnalyzer:
    """Analyzes discovery documents for gaps, ambiguities, and conflicts."""
    
    # Common ambiguous terms that need clarification
    AMBIGUOUS_TERMS = [
        "real-time", "fast", "quick", "simple", "easy", "scalable",
        "robust", "flexible", "soon", "later", "eventually", "approximately"
    ]
    
    # Known systems to detect
    KNOWN_SYSTEMS = [
        "Shopify", "QuickBooks", "Klaviyo", "ShipStation", "Stocky",
        "Stripe", "PayPal", "Mailchimp", "HubSpot", "Salesforce",
        "Zendesk", "Freshdesk", "WooCommerce", "BigCommerce"
    ]
    
    # Critical topics that should be addressed
    CRITICAL_TOPICS = {
        "refund": GapCategory.BUSINESS_RULES,
        "return": GapCategory.BUSINESS_RULES,
        "tax": GapCategory.BUSINESS_RULES,
        "error": GapCategory.ERROR_HANDLING,
        "failure": GapCategory.ERROR_HANDLING,
        "retry": GapCategory.ERROR_HANDLING,
        "sync frequency": GapCategory.TECHNICAL_CONSTRAINTS,
        "rate limit": GapCategory.TECHNICAL_CONSTRAINTS,
        "authentication": GapCategory.TECHNICAL_CONSTRAINTS,
        "success metric": GapCategory.SUCCESS_CRITERIA,
        "acceptance criteria": GapCategory.SUCCESS_CRITERIA,
    }
    
    def analyze(self, documents: List[Document], 
                additional_context: List[str] = None) -> AnalysisResult:
        """Analyze discovery documents and return analysis result."""
        result = AnalysisResult()
        
        # Combine all document content, preferring summaries for integration documents
        content_parts = []
        for doc in documents:
            if doc.summary and doc.source == "integration":
                # Use summary for integration documents
                content_parts.append(f"[SUMMARY: {doc.file_path}]\n{doc.summary}")
            else:
                # Use full content for local documents or when no summary available
                content_parts.append(f"[DOCUMENT: {doc.file_path}]\n{doc.content}")
        
        all_content = "\n\n".join(content_parts)
        if additional_context:
            all_content += "\n\n" + "\n".join(additional_context)
        
        # Extract information
        result.systems_identified = self._extract_systems(all_content)
        result.client_name = self._extract_client_name(documents)
        result.pain_points = self._extract_pain_points(all_content)
        result.business_objectives = self._extract_objectives(all_content)
        
        # Detect gaps
        result.gaps = self._detect_gaps(all_content, additional_context or [])
        
        # Detect ambiguities
        result.ambiguities = self._detect_ambiguities(all_content)
        
        # Detect conflicts
        result.conflicts = self._detect_conflicts(documents)
        
        # Calculate confidence scores
        result.calculate_confidence()
        
        return result
    
    def _extract_systems(self, content: str) -> List[str]:
        """Extract mentioned systems from content."""
        systems = []
        for system in self.KNOWN_SYSTEMS:
            if system.lower() in content.lower():
                systems.append(system)
        return list(set(systems))
    
    def _extract_client_name(self, documents: List[Document]) -> str:
        """Extract client name from documents."""
        # Try to get from email metadata first
        for doc in documents:
            if doc.participants:
                # Get first email domain or name
                for participant in doc.participants:
                    if "@" in participant:
                        domain = participant.split("@")[1].split(".")[0]
                        return domain.capitalize()
        
        # Look for company names in content (basic heuristic)
        for doc in documents:
            # Look for patterns like "I'm from Company" or "at Company"
            match = re.search(r'(?:from|at)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)',
                            doc.content)
            if match:
                return match.group(1)
        
        return "Unknown Client"
    
    def _extract_pain_points(self, content: str) -> List[str]:
        """Extract pain points mentioned in discovery."""
        pain_points = []
        
        # Look for problem indicators
        problem_patterns = [
            r'problem[s]?\s+(?:is|are)\s+([^.]+)',
            r'issue[s]?\s+(?:is|are)\s+([^.]+)',
            r'spending\s+(\d+[^.]+(?:hours?|minutes?)[^.]+)',
            r'frustrated\s+(?:with|about)\s+([^.]+)',
            r'difficulty\s+(?:with|in)\s+([^.]+)',
            r'struggle\s+(?:with|to)\s+([^.]+)',
        ]
        
        for pattern in problem_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                pain_point = match.group(1).strip()
                if len(pain_point) > 10:  # Filter out too short matches
                    pain_points.append(pain_point)
        
        return pain_points[:5]  # Return top 5
    
    def _extract_objectives(self, content: str) -> List[str]:
        """Extract business objectives from discovery."""
        objectives = []
        
        # Look for objective indicators
        objective_patterns = [
            r'(?:want|need|would like)\s+to\s+([^.]+)',
            r'goal\s+is\s+to\s+([^.]+)',
            r'objective\s+is\s+to\s+([^.]+)',
            r'looking\s+to\s+([^.]+)',
            r'hoping\s+to\s+([^.]+)',
        ]
        
        for pattern in objective_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                objective = match.group(1).strip()
                if len(objective) > 10:
                    objectives.append(objective)
        
        return objectives[:5]  # Return top 5
    
    def _detect_gaps(self, content: str, 
                     additional_context: List[str]) -> List[Gap]:
        """Detect missing critical information."""
        gaps = []
        content_lower = content.lower()
        context_lower = " ".join(additional_context).lower()
        
        # Check for critical topics not mentioned
        gap_checks = [
            {
                "keywords": ["refund", "return"],
                "category": GapCategory.BUSINESS_RULES,
                "description": "Refund and return handling not discussed",
                "impact": "Returns could fail to sync or create duplicate credits",
                "question": "How should refunds and returns be handled? Should they create credit notes or adjustment entries?",
                "priority": Priority.HIGH
            },
            {
                "keywords": ["tax", "vat", "sales tax"],
                "category": GapCategory.BUSINESS_RULES,
                "description": "Tax handling not specified",
                "impact": "Tax calculations could be incorrect or missing in synced data",
                "question": "How should taxes be calculated and synced? Which system is responsible for tax calculation?",
                "priority": Priority.HIGH
            },
            {
                "keywords": ["error", "failure", "retry", "error handling"],
                "category": GapCategory.ERROR_HANDLING,
                "description": "Error handling and retry logic not defined",
                "impact": "Failed syncs could go unnoticed or cause data inconsistencies",
                "question": "What should happen when a sync fails? Should we retry automatically? How should errors be reported?",
                "priority": Priority.HIGH
            },
            {
                "keywords": ["sync frequency", "real-time", "interval", "schedule"],
                "category": GapCategory.TECHNICAL_CONSTRAINTS,
                "description": "Sync frequency not clearly defined",
                "impact": "Could build wrong sync mechanism (webhook vs polling)",
                "question": "How often should data sync? Real-time via webhooks, or scheduled intervals (every 15 min, hourly, daily)?",
                "priority": Priority.MEDIUM
            },
            {
                "keywords": ["success", "acceptance", "criteria", "metric"],
                "category": GapCategory.SUCCESS_CRITERIA,
                "description": "Success criteria not explicitly defined",
                "impact": "Unclear definition of project completion",
                "question": "What are the specific success criteria? How will we measure if the integration is working correctly?",
                "priority": Priority.MEDIUM
            },
            {
                "keywords": ["rate limit", "api limit", "throttle"],
                "category": GapCategory.TECHNICAL_CONSTRAINTS,
                "description": "API rate limits not discussed",
                "impact": "Could hit rate limits and cause sync failures",
                "question": "What are the API rate limits for each system? Do we need to implement throttling?",
                "priority": Priority.MEDIUM
            },
            {
                "keywords": ["authentication", "credentials", "api key", "oauth"],
                "category": GapCategory.TECHNICAL_CONSTRAINTS,
                "description": "Authentication method not specified",
                "impact": "Could start with wrong authentication approach",
                "question": "What authentication method should be used? API keys, OAuth, or something else?",
                "priority": Priority.MEDIUM
            },
            {
                "keywords": ["edge case", "exception", "special case"],
                "category": GapCategory.EDGE_CASES,
                "description": "Edge cases not explored",
                "impact": "Unexpected scenarios could break the integration",
                "question": "What edge cases should we handle? (e.g., partial refunds, split payments, cancelled orders)",
                "priority": Priority.LOW
            },
        ]
        
        for check in gap_checks:
            # Check if any keyword is mentioned in content or context
            mentioned = any(keyword in content_lower for keyword in check["keywords"])
            addressed_in_context = any(keyword in context_lower for keyword in check["keywords"])
            
            if not mentioned and not addressed_in_context:
                gap = Gap(
                    category=check["category"],
                    description=check["description"],
                    impact=check["impact"],
                    priority=check["priority"],
                    suggested_question=check["question"]
                )
                gaps.append(gap)
        
        return gaps
    
    def _detect_ambiguities(self, content: str) -> List[Ambiguity]:
        """Detect ambiguous or vague terms and search for clarifications."""
        ambiguities = []
        
        for term in self.AMBIGUOUS_TERMS:
            # Find occurrences with context
            pattern = rf'(.{{0,50}}\b{term}\b.{{0,50}})'
            matches = re.finditer(pattern, content, re.IGNORECASE)
            
            for match in matches:
                context = match.group(1).strip()
                
                clarifications_needed = {
                    "real-time": "Please specify exact sync timing: instant webhooks, sub-second, within 5 minutes?",
                    "fast": "What is the specific performance requirement? Response time in milliseconds?",
                    "quick": "What is the specific time requirement?",
                    "simple": "What does 'simple' mean in this context? What complexity level is acceptable?",
                    "scalable": "What volume needs to be supported? Current and projected?",
                    "soon": "What is the specific timeline? Days, weeks, months?",
                    "approximately": "What is the exact figure or acceptable range?",
                }
                
                clarification_needed = clarifications_needed.get(term.lower(), 
                                                  f"Please provide specific details instead of '{term}'")
                
                # Search for clarification in the content
                clarification_found = self._search_for_clarification(term, content)
                
                ambiguity = Ambiguity(
                    term=term,
                    context=context,
                    clarification_needed=clarification_needed,
                    priority=Priority.MEDIUM,
                    clarification=clarification_found
                )
                ambiguities.append(ambiguity)
                break  # Only report each term once
        
        return ambiguities
    
    def _search_for_clarification(self, term: str, content: str) -> str:
        """
        Search for clarification of an ambiguous term in documents.
        Only returns clarification if explicitly stated, never infers.
        
        Args:
            term: The ambiguous term to clarify
            content: All document content to search
            
        Returns:
            Clarification text if found, None otherwise
        """
        # Look for clarification patterns near the term
        # Pattern: term followed by specific details
        clarification_patterns = {
            "real-time": [
                rf'{term}.{{0,100}}(?:within|under|less than)\s+(\d+\s*(?:seconds?|minutes?|milliseconds?))',
                rf'{term}.{{0,100}}(?:webhook|instant|immediately)',
            ],
            "fast": [
                rf'{term}.{{0,100}}(?:within|under|less than)\s+(\d+\s*(?:seconds?|minutes?|milliseconds?))',
                rf'{term}.{{0,100}}(?:response time|load time|performance).{{0,50}}(\d+\s*(?:ms|seconds?))',
            ],
            "scalable": [
                rf'{term}.{{0,100}}(?:up to|support|handle)\s+([\d,]+)\s*(?:orders?|users?|transactions?|requests?)',
            ],
            "soon": [
                rf'{term}.{{0,100}}(?:within|in|by)\s+(\d+\s*(?:days?|weeks?|months?))',
            ],
        }
        
        patterns = clarification_patterns.get(term.lower(), [])
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
            if match:
                # Extract the surrounding context (200 chars) that contains the clarification
                match_pos = match.start()
                start = max(0, match_pos - 100)
                end = min(len(content), match_pos + 200)
                clarification_context = content[start:end].strip()
                
                # Clean up and return
                clarification_context = " ".join(clarification_context.split())
                if len(clarification_context) > 20:  # Only return if substantial
                    return clarification_context
        
        return None
    
    def _detect_conflicts(self, documents: List[Document]) -> List[Conflict]:
        """Detect conflicting information between documents/stakeholders and search for resolutions."""
        conflicts = []
        
        # Look for conflicting statements about system of record
        inventory_mentions = []
        for doc in documents:
            content_lower = doc.content.lower()
            if "inventory" in content_lower or "stock" in content_lower:
                # Look for source of truth statements
                if "source of truth" in content_lower or "master" in content_lower:
                    # Extract the sentence
                    sentences = doc.content.split(".")
                    for sentence in sentences:
                        if "inventory" in sentence.lower() or "stock" in sentence.lower():
                            if "source" in sentence.lower() or "master" in sentence.lower():
                                inventory_mentions.append({
                                    "statement": sentence.strip(),
                                    "source": doc.file_path,
                                    "doc": doc
                                })
        
        if len(inventory_mentions) > 1:
            # Search for resolution
            resolution = self._search_for_resolution("inventory system of record", documents)
            
            conflict = Conflict(
                topic="Inventory System of Record",
                conflicting_statements=[m["statement"] for m in inventory_mentions],
                sources=[m["source"] for m in inventory_mentions],
                resolution_needed="Clarify which system is the definitive source of truth for inventory levels",
                priority=Priority.HIGH,
                resolution=resolution
            )
            conflicts.append(conflict)
        
        return conflicts
    
    def _search_for_resolution(self, conflict_topic: str, documents: List[Document]) -> str:
        """
        Search for resolution of a conflict in documents.
        Only returns resolution if explicitly stated, never infers.
        
        Args:
            conflict_topic: The topic of the conflict
            documents: List of documents to search
            
        Returns:
            Resolution text if found, None otherwise
        """
        # Look for resolution patterns
        resolution_keywords = [
            "decided", "decision", "agreed", "final decision", "conclusion",
            "resolved", "settled on", "confirmed", "ultimately", "clarification"
        ]
        
        all_content = "\n\n".join([doc.content for doc in documents])
        
        # Search for resolution statements related to the conflict topic
        for keyword in resolution_keywords:
            # Look for sentences containing both the keyword and topic-related terms
            pattern = rf'([^.]*{keyword}[^.]*{conflict_topic.split()[0]}[^.]*\.)'
            matches = re.finditer(pattern, all_content, re.IGNORECASE | re.DOTALL)
            
            for match in matches:
                resolution_text = match.group(1).strip()
                # Ensure it's substantial (not just a passing mention)
                if len(resolution_text) > 30:
                    # Extract surrounding context for better clarity
                    match_pos = match.start()
                    start = max(0, match_pos - 50)
                    end = min(len(all_content), match_pos + 300)
                    context = all_content[start:end].strip()
                    context = " ".join(context.split())
                    return context
        
        # Also look for "we will use X" or "X will be" statements
        decision_patterns = [
            rf'(?:we will use|using|use)\s+([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)?)\s+(?:as|for).{{0,50}}{conflict_topic.split()[0]}',
            rf'{conflict_topic.split()[0]}.{{0,30}}(?:will be|is)\s+([A-Z][a-zA-Z]+)',
        ]
        
        for pattern in decision_patterns:
            match = re.search(pattern, all_content, re.IGNORECASE)
            if match:
                # Extract context around the match
                match_pos = match.start()
                start = max(0, match_pos - 50)
                end = min(len(all_content), match_pos + 200)
                context = all_content[start:end].strip()
                context = " ".join(context.split())
                if len(context) > 30:
                    return context
        
        return None

