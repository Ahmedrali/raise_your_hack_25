from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class EducationalAgent(BaseAgent):
    """Educational agent that provides adaptive learning content based on user expertise."""
    
    def __init__(self):
        super().__init__("educational")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate educational content adapted to user expertise level."""
        self.logger.info("Generating educational content", conversation_id=state.conversation_id)
        
        try:
            # Get context from previous agents
            orchestrator_plan = getattr(state, 'orchestrator_plan', {})
            requirements = getattr(state, 'requirements_analysis', {})
            research_data = getattr(state, 'research_data', {})
            architecture_design = getattr(state, 'architecture_design', {})
            why_reasoning = getattr(state, 'why_reasoning', {})
            business_impact = getattr(state, 'business_impact', {})
            
            # Build educational content prompt
            educational_prompt = self._build_educational_prompt(
                state, orchestrator_plan, requirements, research_data, 
                architecture_design, why_reasoning, business_impact
            )
            
            # Generate educational content
            educational_response = await self.groq_service.query(
                educational_prompt,
                system_message=self.get_system_prompt()
            )
            
            # Parse educational content
            educational_content = self._parse_educational_response(educational_response)
            
            # Enhance with learning path
            educational_content["learning_path"] = self._generate_learning_path(
                state.user_profile.expertise_level, architecture_design, why_reasoning
            )
            
            self.logger.info("Educational content generated", 
                           conversation_id=state.conversation_id,
                           concepts_covered=len(educational_content.get("key_concepts", [])))
            
            return {
                "success": True,
                "educational_content": educational_content,
                "agent": self.name,
                "confidence": educational_content.get("confidence_score", 0.9)
            }
            
        except Exception as e:
            self.logger.error("Educational content generation failed", error=str(e), conversation_id=state.conversation_id)
            return {
                "success": False,
                "error": str(e),
                "educational_content": self._get_fallback_educational_content(),
                "agent": self.name
            }

    def get_system_prompt(self) -> str:
        """Get the system prompt for educational agent."""
        return """
You are the Educational Agent for the Agentic Architect platform. Your role is to provide adaptive, comprehensive educational content that helps users understand architectural concepts, patterns, and decisions at their appropriate expertise level.

EDUCATIONAL OBJECTIVES:
1. Adapt content complexity to user expertise level (beginner, intermediate, advanced)
2. Provide clear explanations of architectural concepts and patterns
3. Offer practical examples and real-world applications
4. Create progressive learning paths for skill development
5. Include hands-on exercises and validation checkpoints
6. Connect theoretical concepts to practical implementation

CONTENT ADAPTATION STRATEGY:
- BEGINNER: Focus on fundamental concepts, simple explanations, basic examples
- INTERMEDIATE: Include design patterns, trade-offs, implementation details
- ADVANCED: Cover complex patterns, optimization strategies, architectural evolution

OUTPUT FORMAT:
Return a JSON object with:
{
  "key_concepts": [
    {
      "concept": "architectural_concept_name",
      "definition": "clear_definition_adapted_to_level",
      "importance": "why_this_concept_matters",
      "examples": ["example_1", "example_2"],
      "common_mistakes": ["mistake_1", "mistake_2"],
      "best_practices": ["practice_1", "practice_2"]
    }
  ],
  "pattern_explanations": [
    {
      "pattern": "architecture_pattern_name",
      "explanation": "detailed_explanation_for_user_level",
      "when_to_use": "appropriate_use_cases",
      "implementation_guide": "step_by_step_guidance",
      "code_examples": ["example_1", "example_2"],
      "variations": ["variation_1", "variation_2"]
    }
  ],
  "technology_deep_dives": [
    {
      "technology": "technology_name",
      "overview": "technology_explanation",
      "strengths": ["strength_1", "strength_2"],
      "limitations": ["limitation_1", "limitation_2"],
      "learning_resources": ["resource_1", "resource_2"],
      "hands_on_exercises": ["exercise_1", "exercise_2"]
    }
  ],
  "practical_exercises": [
    {
      "exercise": "exercise_name",
      "objective": "learning_objective",
      "difficulty": "beginner|intermediate|advanced",
      "instructions": "step_by_step_instructions",
      "expected_outcome": "what_user_should_achieve",
      "validation_criteria": ["criterion_1", "criterion_2"]
    }
  ],
  "learning_progression": {
    "current_level_topics": ["topic_1", "topic_2"],
    "next_level_prerequisites": ["prerequisite_1", "prerequisite_2"],
    "skill_development_path": ["step_1", "step_2", "step_3"],
    "estimated_learning_time": "time_estimate"
  },
  "real_world_applications": [
    {
      "scenario": "business_scenario",
      "architecture_application": "how_concepts_apply",
      "case_study": "detailed_case_study",
      "lessons_learned": ["lesson_1", "lesson_2"]
    }
  ],
  "troubleshooting_guide": [
    {
      "problem": "common_problem",
      "symptoms": ["symptom_1", "symptom_2"],
      "root_causes": ["cause_1", "cause_2"],
      "solutions": ["solution_1", "solution_2"],
      "prevention": "how_to_prevent"
    }
  ],
  "further_learning": {
    "recommended_books": ["book_1", "book_2"],
    "online_courses": ["course_1", "course_2"],
    "documentation": ["doc_1", "doc_2"],
    "communities": ["community_1", "community_2"]
  },
  "assessment_questions": [
    {
      "question": "assessment_question",
      "type": "multiple_choice|open_ended|practical",
      "difficulty": "beginner|intermediate|advanced",
      "correct_answer": "answer_or_guidance",
      "explanation": "why_this_is_correct"
    }
  ],
  "confidence_score": 0.0-1.0
}

Create educational content that is engaging, practical, and appropriately challenging for the user's expertise level.
"""

    def _build_educational_prompt(self, state: WorkflowState, orchestrator_plan: Dict, 
                                requirements: Dict, research_data: Dict, architecture_design: Dict,
                                why_reasoning: Dict, business_impact: Dict) -> str:
        """Build educational content prompt."""
        user_query = state.user_query
        expertise_level = state.user_profile.expertise_level.value if state.user_profile.expertise_level else "intermediate"
        
        prompt_parts = [
            f"Create comprehensive educational content for: {user_query}",
            f"User expertise level: {expertise_level}",
            "",
            "CONTEXT FOR EDUCATIONAL CONTENT:"
        ]
        
        # Add architecture context
        if architecture_design:
            prompt_parts.append("ARCHITECTURE TO EXPLAIN:")
            if overview := architecture_design.get("architecture_overview", {}):
                prompt_parts.append(f"Pattern: {overview.get('pattern', 'Not specified')}")
                prompt_parts.append(f"Description: {overview.get('description', 'Not specified')}")
            
            if components := architecture_design.get("components", []):
                prompt_parts.append("Key Components:")
                for comp in components[:5]:
                    prompt_parts.append(f"- {comp.get('name', '')}: {comp.get('description', '')}")
            
            if tech_stack := architecture_design.get("technology_stack", {}):
                prompt_parts.append("Technologies Used:")
                for category, tech in tech_stack.items():
                    prompt_parts.append(f"- {category}: {tech}")
        
        # Add key concepts from reasoning
        if decisions := why_reasoning.get("architectural_decisions", []):
            prompt_parts.append("\nKEY DECISIONS TO EXPLAIN:")
            for decision in decisions[:3]:
                prompt_parts.append(f"- {decision.get('decision', '')}")
        
        # Add design principles
        if principles := why_reasoning.get("design_principles", []):
            prompt_parts.append("\nDESIGN PRINCIPLES TO COVER:")
            for principle in principles[:3]:
                prompt_parts.append(f"- {principle.get('principle', '')}: {principle.get('importance', '')}")
        
        # Add business context for relevance
        if business_context := state.business_context:
            prompt_parts.extend([
                "",
                "BUSINESS CONTEXT FOR RELEVANCE:",
                f"Industry: {getattr(business_context, 'industry', 'Not specified')}",
                f"Company Size: {getattr(business_context, 'company_size', 'Not specified')}"
            ])
        
        # Expertise-specific instructions
        if expertise_level == "beginner":
            prompt_parts.extend([
                "",
                "BEGINNER-LEVEL REQUIREMENTS:",
                "- Focus on fundamental concepts and basic explanations",
                "- Use simple analogies and real-world comparisons",
                "- Provide step-by-step guidance",
                "- Include basic terminology definitions",
                "- Offer simple, practical exercises"
            ])
        elif expertise_level == "intermediate":
            prompt_parts.extend([
                "",
                "INTERMEDIATE-LEVEL REQUIREMENTS:",
                "- Include design patterns and architectural trade-offs",
                "- Explain implementation details and best practices",
                "- Provide comparative analysis of different approaches",
                "- Include moderate complexity exercises",
                "- Cover common pitfalls and how to avoid them"
            ])
        else:  # advanced
            prompt_parts.extend([
                "",
                "ADVANCED-LEVEL REQUIREMENTS:",
                "- Cover complex architectural patterns and optimizations",
                "- Include performance considerations and scalability strategies",
                "- Discuss architectural evolution and migration strategies",
                "- Provide challenging, real-world scenarios",
                "- Include cutting-edge practices and emerging patterns"
            ])
        
        prompt_parts.extend([
            "",
            "Please create educational content that:",
            "1. Explains all architectural concepts clearly for the user's level",
            "2. Provides practical examples and hands-on exercises",
            "3. Includes real-world applications and case studies",
            "4. Offers a clear learning progression path",
            "5. Includes assessment questions to validate understanding",
            "",
            "Make the content engaging, practical, and immediately applicable."
        ])
        
        return "\n".join(prompt_parts)

    def _parse_educational_response(self, response: str) -> Dict[str, Any]:
        """Parse educational content response from LLM."""
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
            
            educational_data = json.loads(json_str)
            
            # Validate and set defaults
            self._validate_educational_data(educational_data)
            
            return educational_data
            
        except Exception as e:
            self.logger.warning("Failed to parse educational response", error=str(e))
            return self._get_fallback_educational_content()

    def _validate_educational_data(self, data: Dict[str, Any]) -> None:
        """Validate and set defaults for educational data."""
        data.setdefault("key_concepts", [])
        data.setdefault("pattern_explanations", [])
        data.setdefault("technology_deep_dives", [])
        data.setdefault("practical_exercises", [])
        data.setdefault("learning_progression", {})
        data.setdefault("real_world_applications", [])
        data.setdefault("troubleshooting_guide", [])
        data.setdefault("further_learning", {})
        data.setdefault("assessment_questions", [])
        data.setdefault("confidence_score", 0.9)

    def _generate_learning_path(self, expertise_level, architecture_design: Dict, 
                              why_reasoning: Dict) -> Dict[str, Any]:
        """Generate personalized learning path based on user level and architecture."""
        base_path = {
            "current_session_focus": [],
            "next_steps": [],
            "long_term_goals": [],
            "estimated_completion_time": "2-4 weeks"
        }
        
        # Extract key technologies and patterns
        tech_stack = architecture_design.get("technology_stack", {})
        pattern = architecture_design.get("architecture_overview", {}).get("pattern", "")
        
        if expertise_level and hasattr(expertise_level, 'value'):
            level = expertise_level.value
        else:
            level = "intermediate"
        
        if level == "beginner":
            base_path.update({
                "current_session_focus": [
                    "Understanding basic architecture concepts",
                    "Learning about layered architecture",
                    "Introduction to databases and APIs"
                ],
                "next_steps": [
                    "Practice with simple web application architecture",
                    "Learn about REST API design",
                    "Understand database relationships"
                ],
                "long_term_goals": [
                    "Master fundamental design patterns",
                    "Build confidence with common technologies",
                    "Understand system integration basics"
                ],
                "estimated_completion_time": "4-6 weeks"
            })
        elif level == "intermediate":
            base_path.update({
                "current_session_focus": [
                    "Advanced architectural patterns",
                    "Scalability considerations",
                    "Technology trade-offs and selection"
                ],
                "next_steps": [
                    "Implement microservices patterns",
                    "Learn about distributed systems",
                    "Practice with cloud architectures"
                ],
                "long_term_goals": [
                    "Master complex architectural patterns",
                    "Understand performance optimization",
                    "Lead architectural decisions"
                ],
                "estimated_completion_time": "3-4 weeks"
            })
        else:  # advanced
            base_path.update({
                "current_session_focus": [
                    "Architectural evolution strategies",
                    "Performance optimization techniques",
                    "Enterprise integration patterns"
                ],
                "next_steps": [
                    "Design for extreme scale",
                    "Master distributed systems patterns",
                    "Architect for multi-cloud environments"
                ],
                "long_term_goals": [
                    "Become an architecture thought leader",
                    "Design innovative solutions",
                    "Mentor other architects"
                ],
                "estimated_completion_time": "2-3 weeks"
            })
        
        return base_path

    def _get_fallback_educational_content(self) -> Dict[str, Any]:
        """Get fallback educational content."""
        return {
            "key_concepts": [
                {
                    "concept": "Layered Architecture",
                    "definition": "An architectural pattern that organizes code into horizontal layers, each with specific responsibilities",
                    "importance": "Provides clear separation of concerns and makes applications easier to understand and maintain",
                    "examples": ["Three-tier web applications", "MVC pattern", "Clean Architecture"],
                    "common_mistakes": ["Tight coupling between layers", "Business logic in presentation layer"],
                    "best_practices": ["Keep layers loosely coupled", "Define clear interfaces", "Avoid circular dependencies"]
                },
                {
                    "concept": "API Design",
                    "definition": "The process of creating interfaces that allow different software components to communicate",
                    "importance": "Good API design enables system integration and provides a stable contract for clients",
                    "examples": ["REST APIs", "GraphQL", "gRPC services"],
                    "common_mistakes": ["Inconsistent naming", "Poor error handling", "Lack of versioning"],
                    "best_practices": ["Use consistent naming conventions", "Provide clear documentation", "Implement proper error responses"]
                }
            ],
            "pattern_explanations": [
                {
                    "pattern": "Model-View-Controller (MVC)",
                    "explanation": "Separates application logic into three interconnected components: Model (data), View (presentation), and Controller (business logic)",
                    "when_to_use": "Web applications, desktop applications, any system with user interface",
                    "implementation_guide": "1. Define models for data, 2. Create views for presentation, 3. Implement controllers for logic, 4. Connect components with clear interfaces",
                    "code_examples": ["Express.js with MVC structure", "Spring Boot MVC", "Django MVT"],
                    "variations": ["MVP (Model-View-Presenter)", "MVVM (Model-View-ViewModel)"]
                }
            ],
            "technology_deep_dives": [
                {
                    "technology": "PostgreSQL",
                    "overview": "Advanced open-source relational database with strong ACID compliance and rich feature set",
                    "strengths": ["ACID compliance", "Advanced data types", "Excellent performance", "Strong community"],
                    "limitations": ["Vertical scaling challenges", "Complex configuration", "Memory usage"],
                    "learning_resources": ["PostgreSQL official documentation", "PostgreSQL Tutorial", "Database design courses"],
                    "hands_on_exercises": ["Set up a PostgreSQL database", "Design a normalized schema", "Write complex queries"]
                },
                {
                    "technology": "React",
                    "overview": "JavaScript library for building user interfaces with component-based architecture",
                    "strengths": ["Component reusability", "Virtual DOM", "Large ecosystem", "Strong community"],
                    "limitations": ["Learning curve", "Rapid ecosystem changes", "SEO challenges"],
                    "learning_resources": ["React official documentation", "React tutorials", "Modern React courses"],
                    "hands_on_exercises": ["Build a simple React app", "Create reusable components", "Implement state management"]
                }
            ],
            "practical_exercises": [
                {
                    "exercise": "Design a Simple E-commerce Architecture",
                    "objective": "Apply layered architecture principles to design a basic e-commerce system",
                    "difficulty": "intermediate",
                    "instructions": "1. Identify main components (user management, product catalog, orders), 2. Design database schema, 3. Define API endpoints, 4. Create component interaction diagram",
                    "expected_outcome": "Complete architecture diagram with clear component responsibilities",
                    "validation_criteria": ["All major functions covered", "Clear separation of concerns", "Scalable design"]
                }
            ],
            "learning_progression": {
                "current_level_topics": ["Basic architecture patterns", "Database design", "API development"],
                "next_level_prerequisites": ["Understanding of design patterns", "Experience with databases", "API design knowledge"],
                "skill_development_path": ["Master fundamentals", "Practice with real projects", "Learn advanced patterns", "Gain experience with scale"],
                "estimated_learning_time": "3-4 weeks"
            },
            "real_world_applications": [
                {
                    "scenario": "E-commerce Platform Scaling",
                    "architecture_application": "Using microservices to handle different business domains (users, products, orders)",
                    "case_study": "Amazon's evolution from monolith to microservices enabled massive scale and team autonomy",
                    "lessons_learned": ["Start simple, evolve complexity", "Domain boundaries are crucial", "Operational complexity increases"]
                }
            ],
            "troubleshooting_guide": [
                {
                    "problem": "Database Performance Issues",
                    "symptoms": ["Slow query responses", "High CPU usage", "Connection timeouts"],
                    "root_causes": ["Missing indexes", "Inefficient queries", "Connection pool exhaustion"],
                    "solutions": ["Add appropriate indexes", "Optimize query structure", "Tune connection pool settings"],
                    "prevention": "Regular performance monitoring and query analysis"
                }
            ],
            "further_learning": {
                "recommended_books": [
                    "Clean Architecture by Robert Martin",
                    "Designing Data-Intensive Applications by Martin Kleppmann",
                    "Building Microservices by Sam Newman"
                ],
                "online_courses": [
                    "System Design Interview courses",
                    "Database design fundamentals",
                    "Cloud architecture patterns"
                ],
                "documentation": [
                    "AWS Architecture Center",
                    "Google Cloud Architecture Framework",
                    "Microsoft Azure Architecture Center"
                ],
                "communities": [
                    "Stack Overflow",
                    "Reddit r/softwarearchitecture",
                    "Architecture decision records community"
                ]
            },
            "assessment_questions": [
                {
                    "question": "What are the main benefits of using a layered architecture pattern?",
                    "type": "open_ended",
                    "difficulty": "beginner",
                    "correct_answer": "Separation of concerns, maintainability, testability, clear structure",
                    "explanation": "Layered architecture provides clear separation between different aspects of the application, making it easier to understand, maintain, and test"
                },
                {
                    "question": "When would you choose PostgreSQL over MongoDB for a new project?",
                    "type": "open_ended",
                    "difficulty": "intermediate",
                    "correct_answer": "When you need ACID compliance, complex relationships, or strong consistency",
                    "explanation": "PostgreSQL is better for applications requiring strong consistency, complex queries, and relational data structures"
                }
            ],
            "learning_path": {
                "current_session_focus": [
                    "Understanding basic architecture concepts",
                    "Learning about layered architecture",
                    "Introduction to databases and APIs"
                ],
                "next_steps": [
                    "Practice with simple web application architecture",
                    "Learn about REST API design",
                    "Understand database relationships"
                ],
                "long_term_goals": [
                    "Master fundamental design patterns",
                    "Build confidence with common technologies",
                    "Understand system integration basics"
                ],
                "estimated_completion_time": "3-4 weeks"
            },
            "confidence_score": 0.85
        }
