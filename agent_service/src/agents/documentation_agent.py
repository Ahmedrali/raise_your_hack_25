from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class DocumentationAgent(BaseAgent):
    """Documentation agent that generates comprehensive technical and business documentation."""
    
    def __init__(self):
        super().__init__("documentation")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate comprehensive documentation for the architecture."""
        self.logger.info("Generating documentation", conversation_id=state.conversation_id)
        
        try:
            # Get context from all previous agents
            orchestrator_plan = getattr(state, 'orchestrator_plan', {})
            requirements = getattr(state, 'requirements_analysis', {})
            research_data = getattr(state, 'research_data', {})
            architecture_design = getattr(state, 'architecture_design', {})
            why_reasoning = getattr(state, 'why_reasoning', {})
            business_impact = getattr(state, 'business_impact', {})
            educational_content = getattr(state, 'educational_content', {})
            
            # Build documentation prompt
            documentation_prompt = self._build_documentation_prompt(
                state, orchestrator_plan, requirements, research_data, 
                architecture_design, why_reasoning, business_impact, educational_content
            )
            
            # Generate documentation
            documentation_response = await self.groq_service.query(
                documentation_prompt,
                system_message=self.get_system_prompt()
            )
            
            # Parse documentation
            documentation = self._parse_documentation_response(documentation_response)
            
            # Enhance with structured formats
            documentation["export_formats"] = self._generate_export_formats(
                documentation, architecture_design, why_reasoning, business_impact
            )
            
            self.logger.info("Documentation generated", 
                           conversation_id=state.conversation_id,
                           sections_count=len(documentation.get("sections", [])))
            
            return {
                "success": True,
                "documentation": documentation,
                "agent": self.name,
                "confidence": documentation.get("confidence_score", 0.9)
            }
            
        except Exception as e:
            self.logger.error("Documentation generation failed", error=str(e), conversation_id=state.conversation_id)
            return {
                "success": False,
                "error": str(e),
                "documentation": self._get_fallback_documentation(),
                "agent": self.name
            }

    def get_system_prompt(self) -> str:
        """Get the system prompt for documentation agent."""
        return """
You are the Documentation Agent for the Agentic Architect platform. Your role is to generate comprehensive, professional documentation that captures all aspects of the architectural design, decisions, and implementation guidance.

DOCUMENTATION OBJECTIVES:
1. Create comprehensive technical documentation for developers
2. Generate executive summaries for business stakeholders
3. Provide implementation guides and best practices
4. Document architectural decisions and rationale
5. Include deployment and operational guidance
6. Create user-friendly guides and tutorials

DOCUMENTATION STANDARDS:
- Clear, professional writing suitable for technical and business audiences
- Structured format with logical flow and clear sections
- Include diagrams, code examples, and practical guidance
- Provide both high-level overviews and detailed technical specifications
- Include troubleshooting guides and FAQ sections
- Ensure documentation is maintainable and updatable

OUTPUT FORMAT:
Return a JSON object with:
{
  "document_metadata": {
    "title": "document_title",
    "version": "1.0",
    "created_date": "current_date",
    "authors": ["Agentic Architect Platform"],
    "document_type": "Architecture Design Document",
    "classification": "Internal|Confidential|Public"
  },
  "executive_summary": {
    "overview": "high_level_project_overview",
    "key_benefits": ["benefit_1", "benefit_2", "benefit_3"],
    "investment_required": "investment_summary",
    "timeline": "implementation_timeline",
    "success_metrics": ["metric_1", "metric_2", "metric_3"],
    "recommendation": "executive_recommendation"
  },
  "sections": [
    {
      "section_id": "section_identifier",
      "title": "Section Title",
      "content": "detailed_section_content",
      "subsections": [
        {
          "title": "Subsection Title",
          "content": "subsection_content"
        }
      ],
      "diagrams": ["diagram_reference_1", "diagram_reference_2"],
      "code_examples": ["code_example_1", "code_example_2"]
    }
  ],
  "technical_specifications": {
    "architecture_overview": "technical_architecture_description",
    "component_specifications": [
      {
        "component": "component_name",
        "description": "component_description",
        "interfaces": ["interface_1", "interface_2"],
        "dependencies": ["dependency_1", "dependency_2"],
        "configuration": "configuration_details"
      }
    ],
    "data_models": [
      {
        "model": "data_model_name",
        "description": "model_description",
        "fields": ["field_1", "field_2"],
        "relationships": ["relationship_1", "relationship_2"]
      }
    ],
    "api_specifications": [
      {
        "endpoint": "api_endpoint",
        "method": "HTTP_method",
        "description": "endpoint_description",
        "parameters": ["param_1", "param_2"],
        "responses": ["response_1", "response_2"]
      }
    ]
  },
  "implementation_guide": {
    "prerequisites": ["prerequisite_1", "prerequisite_2"],
    "setup_instructions": ["step_1", "step_2", "step_3"],
    "configuration_guide": "configuration_instructions",
    "deployment_steps": ["deploy_step_1", "deploy_step_2"],
    "testing_strategy": "testing_approach",
    "rollback_procedures": "rollback_instructions"
  },
  "operational_guide": {
    "monitoring_setup": "monitoring_configuration",
    "logging_strategy": "logging_approach",
    "backup_procedures": "backup_instructions",
    "security_considerations": ["security_1", "security_2"],
    "performance_tuning": "performance_optimization_guide",
    "troubleshooting": [
      {
        "issue": "common_issue",
        "symptoms": ["symptom_1", "symptom_2"],
        "resolution": "resolution_steps"
      }
    ]
  },
  "decision_log": [
    {
      "decision": "architectural_decision",
      "date": "decision_date",
      "rationale": "decision_reasoning",
      "alternatives": ["alternative_1", "alternative_2"],
      "impact": "decision_impact",
      "status": "approved|pending|rejected"
    }
  ],
  "appendices": {
    "glossary": [
      {
        "term": "technical_term",
        "definition": "term_definition"
      }
    ],
    "references": ["reference_1", "reference_2"],
    "change_log": [
      {
        "version": "version_number",
        "date": "change_date",
        "changes": ["change_1", "change_2"]
      }
    ]
  },
  "confidence_score": 0.0-1.0
}

Create documentation that is comprehensive, professional, and serves both technical and business stakeholders effectively.
"""

    def _build_documentation_prompt(self, state: WorkflowState, orchestrator_plan: Dict, 
                                  requirements: Dict, research_data: Dict, architecture_design: Dict,
                                  why_reasoning: Dict, business_impact: Dict, educational_content: Dict) -> str:
        """Build documentation generation prompt."""
        user_query = state.user_query
        
        prompt_parts = [
            f"Generate comprehensive documentation for the architecture project: {user_query}",
            "",
            "CONTEXT FOR DOCUMENTATION:"
        ]
        
        # Add project overview
        if business_context := state.business_context:
            prompt_parts.extend([
                "PROJECT CONTEXT:",
                f"Industry: {getattr(business_context, 'industry', 'Not specified')}",
                f"Company Size: {getattr(business_context, 'company_size', 'Not specified')}",
                f"Timeline: {getattr(business_context, 'timeline', 'Not specified')}",
                f"Budget: {getattr(business_context, 'budget_range', 'Not specified')}"
            ])
        
        # Add requirements summary
        if requirements:
            prompt_parts.append("\nREQUIREMENTS SUMMARY:")
            if functional_reqs := requirements.get("functional_requirements", []):
                prompt_parts.append("Functional Requirements:")
                for req in functional_reqs[:5]:
                    prompt_parts.append(f"- {req}")
            
            if non_functional_reqs := requirements.get("non_functional_requirements", []):
                prompt_parts.append("Non-Functional Requirements:")
                for req in non_functional_reqs[:5]:
                    prompt_parts.append(f"- {req}")
        
        # Add architecture overview
        if architecture_design:
            prompt_parts.append("\nARCHITECTURE OVERVIEW:")
            if overview := architecture_design.get("architecture_overview", {}):
                prompt_parts.append(f"Pattern: {overview.get('pattern', 'Not specified')}")
                prompt_parts.append(f"Description: {overview.get('description', 'Not specified')}")
            
            if components := architecture_design.get("components", []):
                prompt_parts.append("Key Components:")
                for comp in components[:5]:
                    prompt_parts.append(f"- {comp.get('name', '')}: {comp.get('description', '')}")
            
            if tech_stack := architecture_design.get("technology_stack", {}):
                prompt_parts.append("Technology Stack:")
                for category, tech in tech_stack.items():
                    prompt_parts.append(f"- {category}: {tech}")
        
        # Add key decisions
        if decisions := why_reasoning.get("architectural_decisions", []):
            prompt_parts.append("\nKEY ARCHITECTURAL DECISIONS:")
            for decision in decisions[:3]:
                prompt_parts.append(f"- {decision.get('decision', '')}")
                prompt_parts.append(f"  Rationale: {decision.get('rationale', '')}")
        
        # Add business impact summary
        if business_impact:
            prompt_parts.append("\nBUSINESS IMPACT SUMMARY:")
            if exec_summary := business_impact.get("executive_summary", {}):
                prompt_parts.append(f"Overall Impact: {exec_summary.get('overall_impact', 'Not specified')}")
                if benefits := exec_summary.get("key_benefits", []):
                    prompt_parts.append("Key Benefits:")
                    for benefit in benefits[:3]:
                        prompt_parts.append(f"- {benefit}")
        
        prompt_parts.extend([
            "",
            "Please generate comprehensive documentation that includes:",
            "1. Executive summary for business stakeholders",
            "2. Technical specifications and architecture details",
            "3. Implementation and deployment guides",
            "4. Operational procedures and troubleshooting",
            "5. Decision log with rationale",
            "6. Appendices with glossary and references",
            "",
            "Ensure the documentation is professional, comprehensive, and suitable for both technical and business audiences."
        ])
        
        return "\n".join(prompt_parts)

    def _parse_documentation_response(self, response: str) -> Dict[str, Any]:
        """Parse documentation response from LLM."""
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                raise ValueError("No JSON found in response")
            
            documentation_data = json.loads(json_str)
            
            # Validate and set defaults
            self._validate_documentation_data(documentation_data)
            
            return documentation_data
            
        except Exception as e:
            self.logger.warning("Failed to parse documentation response", error=str(e))
            return self._get_fallback_documentation()

    def _validate_documentation_data(self, data: Dict[str, Any]) -> None:
        """Validate and set defaults for documentation data."""
        data.setdefault("document_metadata", {})
        data.setdefault("executive_summary", {})
        data.setdefault("sections", [])
        data.setdefault("technical_specifications", {})
        data.setdefault("implementation_guide", {})
        data.setdefault("operational_guide", {})
        data.setdefault("decision_log", [])
        data.setdefault("appendices", {})
        data.setdefault("confidence_score", 0.9)

    def _generate_export_formats(self, documentation: Dict, architecture_design: Dict, 
                                why_reasoning: Dict, business_impact: Dict) -> Dict[str, Any]:
        """Generate different export formats for the documentation."""
        return {
            "markdown": self._generate_markdown_format(documentation, architecture_design),
            "pdf_ready": self._generate_pdf_ready_format(documentation),
            "confluence": self._generate_confluence_format(documentation),
            "word_document": self._generate_word_format(documentation),
            "presentation_slides": self._generate_presentation_format(documentation, business_impact)
        }

    def _generate_markdown_format(self, documentation: Dict, architecture_design: Dict) -> str:
        """Generate markdown format of the documentation."""
        metadata = documentation.get("document_metadata", {})
        exec_summary = documentation.get("executive_summary", {})
        
        markdown_parts = [
            f"# {metadata.get('title', 'Architecture Design Document')}",
            "",
            f"**Version:** {metadata.get('version', '1.0')}  ",
            f"**Created:** {metadata.get('created_date', 'Current Date')}  ",
            f"**Authors:** {', '.join(metadata.get('authors', ['Agentic Architect Platform']))}",
            "",
            "## Executive Summary",
            "",
            exec_summary.get('overview', 'Project overview not available'),
            "",
            "### Key Benefits",
            ""
        ]
        
        for benefit in exec_summary.get('key_benefits', []):
            markdown_parts.append(f"- {benefit}")
        
        markdown_parts.extend([
            "",
            "### Investment Required",
            exec_summary.get('investment_required', 'Investment details not available'),
            "",
            "### Timeline",
            exec_summary.get('timeline', 'Timeline not available'),
            ""
        ])
        
        # Add sections
        for section in documentation.get("sections", []):
            markdown_parts.extend([
                f"## {section.get('title', 'Section')}",
                "",
                section.get('content', 'Content not available'),
                ""
            ])
            
            for subsection in section.get('subsections', []):
                markdown_parts.extend([
                    f"### {subsection.get('title', 'Subsection')}",
                    "",
                    subsection.get('content', 'Content not available'),
                    ""
                ])
        
        # Add architecture diagram if available
        if architecture_design and architecture_design.get("visualization_data", {}).get("mermaid_diagram"):
            markdown_parts.extend([
                "## Architecture Diagram",
                "",
                "```mermaid",
                architecture_design["visualization_data"]["mermaid_diagram"],
                "```",
                ""
            ])
        
        return "\n".join(markdown_parts)

    def _generate_pdf_ready_format(self, documentation: Dict) -> Dict[str, Any]:
        """Generate PDF-ready format with styling information."""
        return {
            "title_page": {
                "title": documentation.get("document_metadata", {}).get("title", "Architecture Design Document"),
                "subtitle": "Comprehensive Architecture Documentation",
                "version": documentation.get("document_metadata", {}).get("version", "1.0"),
                "date": documentation.get("document_metadata", {}).get("created_date", "Current Date")
            },
            "table_of_contents": True,
            "page_numbering": True,
            "header_footer": True,
            "styling": {
                "font_family": "Arial, sans-serif",
                "font_size": "11pt",
                "line_spacing": "1.2",
                "margins": "1 inch"
            }
        }

    def _generate_confluence_format(self, documentation: Dict) -> Dict[str, Any]:
        """Generate Confluence-compatible format."""
        return {
            "page_title": documentation.get("document_metadata", {}).get("title", "Architecture Design Document"),
            "labels": ["architecture", "design", "documentation"],
            "macros_used": ["info", "note", "warning", "code", "expand"],
            "attachments": ["architecture_diagram.png", "component_diagram.png"],
            "page_properties": {
                "version": documentation.get("document_metadata", {}).get("version", "1.0"),
                "status": "Draft",
                "owner": "Architecture Team"
            }
        }

    def _generate_word_format(self, documentation: Dict) -> Dict[str, Any]:
        """Generate Microsoft Word compatible format."""
        return {
            "document_properties": {
                "title": documentation.get("document_metadata", {}).get("title", "Architecture Design Document"),
                "author": ", ".join(documentation.get("document_metadata", {}).get("authors", ["Agentic Architect Platform"])),
                "subject": "System Architecture Documentation",
                "keywords": "architecture, design, documentation, system"
            },
            "styles": {
                "heading_1": "Arial, 16pt, Bold",
                "heading_2": "Arial, 14pt, Bold",
                "heading_3": "Arial, 12pt, Bold",
                "body_text": "Arial, 11pt, Normal",
                "code": "Courier New, 10pt, Normal"
            },
            "page_setup": {
                "orientation": "Portrait",
                "margins": "1 inch all sides",
                "page_numbering": "Bottom center"
            }
        }

    def _generate_presentation_format(self, documentation: Dict, business_impact: Dict) -> Dict[str, Any]:
        """Generate presentation slides format."""
        slides = [
            {
                "slide_number": 1,
                "type": "title",
                "title": documentation.get("document_metadata", {}).get("title", "Architecture Design Document"),
                "subtitle": "Executive Presentation"
            },
            {
                "slide_number": 2,
                "type": "content",
                "title": "Executive Summary",
                "content": documentation.get("executive_summary", {}).get("overview", "Project overview")
            },
            {
                "slide_number": 3,
                "type": "bullet_points",
                "title": "Key Benefits",
                "bullets": documentation.get("executive_summary", {}).get("key_benefits", [])
            }
        ]
        
        if business_impact:
            slides.append({
                "slide_number": 4,
                "type": "content",
                "title": "Business Impact",
                "content": business_impact.get("executive_summary", {}).get("overall_impact", "Positive business impact expected")
            })
        
        return {
            "slides": slides,
            "template": "Professional Business Template",
            "color_scheme": "Blue and White",
            "font_scheme": "Arial/Calibri"
        }

    def _get_fallback_documentation(self) -> Dict[str, Any]:
        """Get fallback documentation."""
        return {
            "document_metadata": {
                "title": "Architecture Design Document",
                "version": "1.0",
                "created_date": "2024-01-01",
                "authors": ["Agentic Architect Platform"],
                "document_type": "Architecture Design Document",
                "classification": "Internal"
            },
            "executive_summary": {
                "overview": "This document outlines the proposed architecture for a scalable, maintainable system that addresses current business requirements while providing a foundation for future growth.",
                "key_benefits": [
                    "Improved system scalability and performance",
                    "Enhanced maintainability and development productivity",
                    "Reduced operational costs and complexity",
                    "Better security and compliance posture"
                ],
                "investment_required": "Initial investment of $65,000 - $195,000 with ongoing operational costs",
                "timeline": "3-6 months for initial implementation, with full benefits realized within 12 months",
                "success_metrics": [
                    "99.5% system uptime",
                    "25% faster feature delivery",
                    "40% reduction in maintenance overhead"
                ],
                "recommendation": "Proceed with implementation as outlined in this document"
            },
            "sections": [
                {
                    "section_id": "introduction",
                    "title": "Introduction",
                    "content": "This architecture design document provides a comprehensive overview of the proposed system architecture, including technical specifications, implementation guidance, and operational procedures.",
                    "subsections": [
                        {
                            "title": "Purpose",
                            "content": "Define the architecture for a scalable, maintainable system that meets current and future business needs."
                        },
                        {
                            "title": "Scope",
                            "content": "This document covers the complete system architecture including frontend, backend, database, and infrastructure components."
                        }
                    ],
                    "diagrams": ["system_overview_diagram"],
                    "code_examples": []
                },
                {
                    "section_id": "architecture_overview",
                    "title": "Architecture Overview",
                    "content": "The proposed architecture follows a layered pattern with clear separation of concerns, providing a solid foundation for scalable application development.",
                    "subsections": [
                        {
                            "title": "Architecture Pattern",
                            "content": "Layered architecture with presentation, business logic, and data access layers."
                        },
                        {
                            "title": "Key Components",
                            "content": "Frontend application, API gateway, backend services, and database layer."
                        }
                    ],
                    "diagrams": ["architecture_diagram", "component_diagram"],
                    "code_examples": ["api_example", "database_schema"]
                }
            ],
            "technical_specifications": {
                "architecture_overview": "Layered architecture with React frontend, Node.js backend, and PostgreSQL database",
                "component_specifications": [
                    {
                        "component": "Frontend Application",
                        "description": "React-based user interface with responsive design",
                        "interfaces": ["REST API", "WebSocket"],
                        "dependencies": ["API Gateway", "Authentication Service"],
                        "configuration": "Environment-specific configuration files"
                    },
                    {
                        "component": "Backend Service",
                        "description": "Node.js application with Express framework",
                        "interfaces": ["REST API", "Database Connection"],
                        "dependencies": ["Database", "External APIs"],
                        "configuration": "Environment variables and configuration files"
                    }
                ],
                "data_models": [
                    {
                        "model": "User",
                        "description": "User account and profile information",
                        "fields": ["id", "email", "name", "created_at"],
                        "relationships": ["has_many conversations"]
                    }
                ],
                "api_specifications": [
                    {
                        "endpoint": "/api/users",
                        "method": "GET",
                        "description": "Retrieve user information",
                        "parameters": ["user_id"],
                        "responses": ["200 OK", "404 Not Found"]
                    }
                ]
            },
            "implementation_guide": {
                "prerequisites": [
                    "Node.js 18+ installed",
                    "PostgreSQL 13+ database",
                    "Git version control",
                    "Development environment setup"
                ],
                "setup_instructions": [
                    "Clone the repository",
                    "Install dependencies with npm install",
                    "Configure environment variables",
                    "Run database migrations",
                    "Start the development server"
                ],
                "configuration_guide": "Configure environment variables for database connection, API keys, and application settings",
                "deployment_steps": [
                    "Build production assets",
                    "Deploy to staging environment",
                    "Run integration tests",
                    "Deploy to production",
                    "Monitor deployment"
                ],
                "testing_strategy": "Unit tests, integration tests, and end-to-end testing with automated CI/CD pipeline",
                "rollback_procedures": "Automated rollback using deployment scripts and database migration rollbacks"
            },
            "operational_guide": {
                "monitoring_setup": "Application performance monitoring with logging and alerting",
                "logging_strategy": "Centralized logging with structured log format and log aggregation",
                "backup_procedures": "Automated daily database backups with point-in-time recovery",
                "security_considerations": [
                    "HTTPS encryption for all communications",
                    "JWT token-based authentication",
                    "Input validation and sanitization",
                    "Regular security updates"
                ],
                "performance_tuning": "Database query optimization, caching strategies, and load balancing",
                "troubleshooting": [
                    {
                        "issue": "Application slow response times",
                        "symptoms": ["High response times", "User complaints"],
                        "resolution": "Check database performance, review slow queries, optimize caching"
                    }
                ]
            },
            "decision_log": [
                {
                    "decision": "Use React for frontend framework",
                    "date": "2024-01-01",
                    "rationale": "Team expertise, large ecosystem, component reusability",
                    "alternatives": ["Vue.js", "Angular"],
                    "impact": "Faster development, better maintainability",
                    "status": "approved"
                },
                {
                    "decision": "Use PostgreSQL for primary database",
                    "date": "2024-01-01",
                    "rationale": "ACID compliance, advanced features, performance",
                    "alternatives": ["MySQL", "MongoDB"],
                    "impact": "Better data consistency, advanced query capabilities",
                    "status": "approved"
                }
            ],
            "appendices": {
                "glossary": [
                    {
                        "term": "API",
                        "definition": "Application Programming Interface - a set of protocols and tools for building software applications"
                    },
                    {
                        "term": "REST",
                        "definition": "Representational State Transfer - an architectural style for designing networked applications"
                    }
                ],
                "references": [
                    "Clean Architecture by Robert Martin",
                    "Designing Data-Intensive Applications by Martin Kleppmann",
                    "React Documentation - https://reactjs.org/docs/",
                    "PostgreSQL Documentation - https://www.postgresql.org/docs/"
                ],
                "change_log": [
                    {
                        "version": "1.0",
                        "date": "2024-01-01",
                        "changes": ["Initial document creation", "Architecture design completed"]
                    }
                ]
            },
            "export_formats": {
                "markdown": "# Architecture Design Document\n\n## Executive Summary\n\nThis document outlines the proposed architecture...",
                "pdf_ready": {
                    "title_page": {
                        "title": "Architecture Design Document",
                        "subtitle": "Comprehensive Architecture Documentation",
                        "version": "1.0",
                        "date": "2024-01-01"
                    }
                }
            },
            "confidence_score": 0.9
        }
