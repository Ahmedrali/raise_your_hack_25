from typing import Dict, Any, List
import json
from src.agents.base_agent import BaseAgent
from src.models.agent_models import WorkflowState

class ArchitectureAgent(BaseAgent):
    """Architecture agent that designs comprehensive system architectures."""
    
    def __init__(self):
        super().__init__("architecture")

    async def process(self, state: WorkflowState) -> Dict[str, Any]:
        """Generate comprehensive architecture design with intelligent complexity analysis."""
        self.logger.info("Generating architecture design", conversation_id=state.conversation_id)
        
        try:
            # Get context from previous agents
            orchestrator_plan = getattr(state, 'orchestrator_plan', {})
            requirements = getattr(state, 'requirements_analysis', {})
            research_data = getattr(state, 'research_data', {})
            
            # Check for existing architecture from conversation history
            existing_architecture = self._extract_existing_architecture(state)
            
            # Step 1: Intelligent complexity analysis (considers existing architecture)
            self.logger.info("Analyzing system complexity with LLM", conversation_id=state.conversation_id)
            complexity_analysis = await self._analyze_system_complexity(state.user_query, existing_architecture)
            
            self.logger.info("Complexity analysis completed", 
                           conversation_id=state.conversation_id,
                           complexity_level=complexity_analysis.get("complexity_level"),
                           criticality=complexity_analysis.get("criticality_level"))
            
            # Store existing architecture for error recovery
            self._current_existing_architecture = existing_architecture
            
            # Step 2: Build architecture prompt with intelligent analysis and existing architecture
            architecture_prompt = self._build_architecture_prompt_with_analysis(
                state, orchestrator_plan, requirements, research_data, complexity_analysis, existing_architecture
            )
            
            # Generate architecture design
            architecture_response = await self.groq_service.query(
                architecture_prompt,
                system_message=self.get_system_prompt()
            )
            
            # Parse architecture design
            architecture_design = self._parse_architecture_response(architecture_response)
            
            # Enhance with visualization data
            architecture_design["visualization_data"] = self._generate_visualization_data(architecture_design)
            
            self.logger.info("Architecture design completed", 
                           conversation_id=state.conversation_id,
                           components_count=len(architecture_design.get("components", [])))
            
            return {
                "success": True,
                "architecture_design": architecture_design,
                "agent": self.name,
                "confidence": architecture_design.get("confidence_score", 0.85)
            }
            
        except Exception as e:
            self.logger.error("Architecture generation failed", error=str(e), conversation_id=state.conversation_id)
            return {
                "success": False,
                "error": str(e),
                "architecture_design": self._get_fallback_architecture(),
                "agent": self.name
            }

    def get_system_prompt(self) -> str:
        """Get the system prompt for architecture agent."""
        return """
You are the Architecture Agent for the Agentic Architect platform. Your role is to design world-class, enterprise-grade system architectures with intelligent layer separation for optimal visualization and stakeholder communication.

CRITICAL: When enhancing existing architectures, you MUST:
- PRESERVE all existing components and their relationships
- ADD new components to fulfill new requirements 
- MAINTAIN architectural consistency and integration
- BUILD UPON rather than replace the existing design

ARCHITECTURE DESIGN PRINCIPLES:
1. Design for scalability, maintainability, and performance
2. Follow established architecture patterns and best practices
3. Consider security, reliability, and operational concerns
4. Adapt complexity to user expertise level
5. Provide clear rationale for all design decisions
6. Generate layer-specific intelligent data for world-class visualization
7. Ensure seamless integration when enhancing existing systems

DESIGN METHODOLOGY:
- Analyze functional and non-functional requirements thoroughly
- Select appropriate architecture patterns (microservices, event-driven, etc.)
- Design comprehensive system components and their interactions
- Include ALL necessary infrastructure components (load balancers, caches, monitoring)
- Define data flow and communication patterns with protocols
- Specify complete technology stack and infrastructure
- Consider deployment, scaling, and operational aspects
- Create detailed business capability mappings
- Design infrastructure zones and security boundaries
- Include observability, security, and resilience patterns

COMPREHENSIVE COMPONENT COVERAGE:
For user-facing systems, ALWAYS include:
🖥️ Frontend/UI components (web apps, mobile apps, dashboards, admin panels)
🌐 User-facing interfaces and client applications

For complex systems, ensure inclusion of:
🔄 Load Balancers & API Gateways for traffic management
⚡ Caching layers (Redis, CDN) for performance
📊 Monitoring & Observability (metrics, logging, tracing)
🔒 Security components (auth, authorization, encryption)
📨 Message brokers for async communication
🗄️ Multiple data stores (primary DB, cache, search)
☁️ Cloud services and infrastructure components
🔧 DevOps tooling (CI/CD, deployment, scaling)

VISUALIZATION LAYERS:
1. SYSTEM OVERVIEW: Business capabilities, core systems, data domains, external integrations
2. DEPLOYMENT ARCHITECTURE: Infrastructure zones, container clusters, network topology, security boundaries

OUTPUT FORMAT:
Return a JSON object with:
{
  "architecture_overview": {
    "pattern": "microservices|monolithic|serverless|hybrid",
    "description": "high_level_description",
    "key_principles": ["principle_1", "principle_2"]
  },
  "components": [
    {
      "id": "component_id",
      "name": "Component Name",
      "type": "service|database|gateway|cache|queue|frontend|external",
      "description": "component_description",
      "responsibilities": ["responsibility_1", "responsibility_2"],
      "technology": "recommended_technology",
      "scalability": "horizontal|vertical|auto",
      "dependencies": ["component_id_1", "component_id_2"],
      "visualization_metadata": {
        "layer_assignments": {
          "system_overview": "core_system|external_integration|data_component",
          "deployment": "dmz|application|data|management"
        },
        "business_criticality": "high|medium|low",
        "visual_importance": 1-10,
        "icon_category": "frontend|backend|database|infrastructure|external",
        "technology_badges": ["react", "nodejs", "postgresql"],
        "health_indicators": {
          "monitoring_required": true,
          "performance_critical": true,
          "availability_target": "99.9%"
        }
      }
    }
  ],
  "connections": [
    {
      "from_component": "component_id",
      "to_component": "component_id",
      "connection_type": "http|grpc|message_queue|database|websocket",
      "description": "connection_purpose",
      "data_flow": "request_response|event_driven|streaming",
      "visualization_metadata": {
        "protocol_display": "HTTPS/REST|gRPC|WebSocket|Database|Message Queue",
        "traffic_volume": "high|medium|low",
        "latency_requirement": "real_time|near_real_time|batch",
        "security_level": "high|medium|low",
        "dependency_strength": "critical|important|optional",
        "line_style": "solid|dashed|dotted",
        "animation_type": "bidirectional|unidirectional|pulsing"
      }
    }
  ],
  "data_architecture": {
    "storage_strategy": "centralized|distributed|hybrid",
    "databases": [
      {
        "name": "database_name",
        "type": "relational|nosql|cache|search",
        "purpose": "primary_data|analytics|cache|search",
        "technology": "postgresql|mongodb|redis|elasticsearch"
      }
    ],
    "data_flow": "description_of_data_movement"
  },
  "security_architecture": {
    "authentication": "jwt|oauth|saml",
    "authorization": "rbac|abac|custom",
    "data_protection": ["encryption", "access_control"],
    "network_security": ["firewall", "vpc", "ssl_tls"]
  },
  "system_overview": {
    "business_capabilities": [
      {
        "capability": "capability_name",
        "components": ["component_id_1", "component_id_2"],
        "business_value": "value_description",
        "complexity": "low|medium|high",
        "priority": "high|medium|low"
      }
    ],
    "core_systems": [
      {
        "system": "system_name",
        "components": ["component_id_1", "component_id_2"],
        "purpose": "system_purpose",
        "criticality": "high|medium|low",
        "user_facing": true
      }
    ],
    "external_integrations": [
      {
        "system": "external_system_name",
        "type": "third_party|internal|saas",
        "data_flow": "inbound|outbound|bidirectional",
        "security_level": "high|medium|low",
        "dependency_level": "critical|important|optional"
      }
    ],
    "data_domains": [
      {
        "domain": "domain_name",
        "components": ["component_id_1", "component_id_2"],
        "sensitivity": "high|medium|low",
        "data_types": ["customer_data", "transaction_data"]
      }
    ]
  },
  "deployment_architecture": {
    "strategy": "containers|serverless|vm|hybrid",
    "orchestration": "kubernetes|docker_swarm|none",
    "environments": ["development", "staging", "production"],
    "ci_cd": "github_actions|jenkins|gitlab_ci",
    "infrastructure_zones": [
      {
        "zone": "zone_name",
        "components": ["component_id_1", "component_id_2"],
        "security_level": "high|medium|low",
        "network_access": "public|private|isolated",
        "zone_type": "dmz|application|data|management"
      }
    ],
    "container_clusters": [
      {
        "cluster": "cluster_name",
        "components": ["component_id_1", "component_id_2"],
        "scaling": "auto|manual|none",
        "replicas": "min-max",
        "resource_requirements": "high|medium|low"
      }
    ],
    "network_topology": {
      "load_balancers": [
        {
          "name": "lb_name",
          "type": "application|network",
          "targets": ["component_id_1"]
        }
      ],
      "security_groups": [
        {
          "name": "sg_name",
          "components": ["component_id_1"],
          "rules": ["rule_description"]
        }
      ]
    }
  },
  "scalability_strategy": {
    "horizontal_scaling": ["component_1", "component_2"],
    "vertical_scaling": ["component_3"],
    "auto_scaling": "enabled|disabled",
    "load_balancing": "application|network|database"
  },
  "monitoring_observability": {
    "logging": "centralized|distributed",
    "metrics": "application|infrastructure|business",
    "tracing": "distributed|local",
    "alerting": "proactive|reactive"
  },
  "technology_stack": {
    "frontend": "react|vue|angular",
    "backend": "node|python|java|go",
    "database": "postgresql|mysql|mongodb",
    "infrastructure": "aws|azure|gcp|on_premise",
    "additional_tools": ["tool_1", "tool_2"]
  },
  "implementation_phases": [
    {
      "phase": 1,
      "name": "phase_name",
      "duration": "estimated_weeks",
      "components": ["component_1", "component_2"],
      "deliverables": ["deliverable_1", "deliverable_2"]
    }
  ],
  "risks_mitigations": [
    {
      "risk": "identified_risk",
      "impact": "high|medium|low",
      "probability": "high|medium|low",
      "mitigation": "mitigation_strategy"
    }
  ],
  "confidence_score": 0.0-1.0
}

Design architectures that are practical, implementable, and aligned with the user's expertise level and business constraints.
"""

    def _extract_existing_architecture(self, state: WorkflowState) -> Dict[str, Any]:
        """Extract existing architecture from conversation history."""
        existing_architecture = {}
        
        # Check if there's architecture in current state
        if state.architecture_design:
            existing_architecture = state.architecture_design
            self.logger.info("Found existing architecture in current state", 
                           conversation_id=state.conversation_id,
                           components_count=len(existing_architecture.get("components", [])))
        
        # Check conversation history for previous architecture decisions
        elif state.conversation_history:
            for msg in reversed(state.conversation_history):  # Start from most recent
                if msg.get('messageType') == 'ARCHITECTURE_UPDATE':
                    metadata = msg.get('metadata', {})
                    agent_response = metadata.get('agentResponse', {})
                    architecture_update = agent_response.get('architectureUpdate', {})
                    
                    if architecture_update and architecture_update.get('components'):
                        existing_architecture = architecture_update
                        self.logger.info("Found existing architecture in conversation history",
                                       conversation_id=state.conversation_id,
                                       components_count=len(architecture_update.get("components", [])))
                        break
        
        return existing_architecture

    async def _analyze_system_complexity(self, user_query: str, existing_architecture: Dict[str, Any] = None) -> Dict[str, Any]:
        """Use LLM to intelligently analyze system complexity and requirements."""
        
        # Build analysis prompt considering existing architecture
        if existing_architecture and existing_architecture.get('components'):
            analysis_prompt = f"""
Analyze this user request for system architecture requirements, considering there is an EXISTING ARCHITECTURE that should be enhanced:

User Request: "{user_query}"

EXISTING ARCHITECTURE:
- Components: {len(existing_architecture.get('components', []))} components
- Component Types: {', '.join(set(comp.get('type', 'unknown') for comp in existing_architecture.get('components', [])))}
- Previous Architecture Summary: {existing_architecture.get('metadata', {}).get('description', 'Previous architecture design')}

IMPORTANT: This is an ENHANCEMENT request, not a new architecture. Analyze complexity for ADDING to the existing system.

Provide a JSON analysis with:"""
        else:
            analysis_prompt = f"""
Analyze this user request for system architecture requirements:
"{user_query}"

Provide a JSON analysis with:
{{
  "complexity_level": "simple|moderate|high|enterprise",
  "criticality_level": "standard|important|critical|mission_critical", 
  "performance_requirements": "basic|optimized|high_performance|ultra_high_performance",
  "scale_requirements": "small|medium|large|massive",
  "domain_type": "web_app|mobile_app|enterprise|fintech|healthcare|gaming|iot|ai_ml|ecommerce|other",
  "architecture_patterns_suggested": ["microservices", "event_driven", "serverless", "etc"],
  "required_components_count": "4-6|6-10|10-15|15+",
  "infrastructure_needs": ["load_balancing", "caching", "monitoring", "security", "etc"],
  "reasoning": "Brief explanation of the analysis"
}}

Focus on understanding the TRUE intent and requirements, not just keywords.
"""
        
        try:
            analysis_response = await self.groq_service.query(
                analysis_prompt,
                system_message="You are an expert system architect. Analyze requirements intelligently based on context and intent, not just keywords."
            )
            
            # Parse the JSON response
            import json
            if "```json" in analysis_response:
                json_start = analysis_response.find("```json") + 7
                json_end = analysis_response.find("```", json_start)
                json_str = analysis_response[json_start:json_end].strip()
            elif "{" in analysis_response:
                json_start = analysis_response.find("{")
                json_end = analysis_response.rfind("}") + 1
                json_str = analysis_response[json_start:json_end]
            else:
                raise ValueError("No JSON found in analysis response")
                
            return json.loads(json_str)
            
        except Exception as e:
            self.logger.warning("Failed to analyze system complexity", error=str(e))
            # Fallback to moderate complexity
            return {
                "complexity_level": "moderate",
                "criticality_level": "important", 
                "performance_requirements": "optimized",
                "scale_requirements": "medium",
                "domain_type": "web_app",
                "architecture_patterns_suggested": ["layered"],
                "required_components_count": "6-10",
                "infrastructure_needs": ["load_balancing", "caching"],
                "reasoning": "Default analysis due to parsing error"
            }

    def _build_architecture_prompt_with_analysis(self, state: WorkflowState, orchestrator_plan: Dict, 
                                                requirements: Dict, research_data: Dict, complexity_analysis: Dict, 
                                                existing_architecture: Dict = None) -> str:
        """Build enhanced architecture design prompt with intelligent complexity analysis and existing architecture context."""
        user_query = state.user_query
        expertise_level = state.user_profile.expertise_level.value if state.user_profile.expertise_level else "intermediate"
        
        # Determine if this is an enhancement or new architecture
        is_enhancement = existing_architecture and existing_architecture.get('components')
        
        if is_enhancement:
            prompt_parts = [
                f"ENHANCE the existing architecture by adding: {user_query}",
                f"User expertise level: {expertise_level}",
                "",
                "🔄 EXISTING ARCHITECTURE TO ENHANCE:",
                f"📦 Current Components: {len(existing_architecture.get('components', []))}",
                f"🏗️ Current Types: {', '.join(set(comp.get('type', 'unknown') for comp in existing_architecture.get('components', [])))}",
                "",
                "EXISTING COMPONENTS:",
            ]
            
            # List existing components
            for comp in existing_architecture.get('components', [])[:10]:  # Show first 10
                comp_name = comp.get('name', 'Unknown')
                comp_type = comp.get('type', 'unknown')
                prompt_parts.append(f"- {comp_name} ({comp_type})")
                
            if len(existing_architecture.get('components', [])) > 10:
                prompt_parts.append(f"... and {len(existing_architecture.get('components', [])) - 10} more components")
            
            prompt_parts.extend([
                "",
                "🎯 ENHANCEMENT REQUIREMENTS:",
                "- PRESERVE all existing components and their relationships",
                "- ADD new components to fulfill the new requirements",
                "- EXTEND existing components if they can be enhanced",
                "- MAINTAIN architectural consistency and patterns",
                "- INTEGRATE new functionality seamlessly with existing system",
                "",
                "INTELLIGENT SYSTEM ANALYSIS FOR ENHANCEMENT:",
            ])
        else:
            prompt_parts = [
                f"Design a comprehensive, production-ready architecture for: {user_query}",
                f"User expertise level: {expertise_level}",
                "",
                "INTELLIGENT SYSTEM ANALYSIS:",
            ]
        
        prompt_parts.extend([
            f"🎯 Complexity Level: {complexity_analysis.get('complexity_level', 'moderate')}",
            f"⚡ Criticality Level: {complexity_analysis.get('criticality_level', 'important')}",
            f"🚀 Performance Requirements: {complexity_analysis.get('performance_requirements', 'optimized')}",
            f"📈 Scale Requirements: {complexity_analysis.get('scale_requirements', 'medium')}",
            f"🏗️ Domain Type: {complexity_analysis.get('domain_type', 'web_app')}",
            f"📦 Suggested Component Count: {complexity_analysis.get('required_components_count', '6-10')}",
            f"🔧 Infrastructure Needs: {', '.join(complexity_analysis.get('infrastructure_needs', ['basic']))}",
            f"💡 Analysis Reasoning: {complexity_analysis.get('reasoning', 'Standard system requirements')}",
            ""
        ])
        
        # Add architecture guidance based on analysis
        complexity_level = complexity_analysis.get('complexity_level', 'moderate')
        criticality_level = complexity_analysis.get('criticality_level', 'important')
        
        if complexity_level in ['high', 'enterprise']:
            prompt_parts.extend([
                "🎯 HIGH COMPLEXITY ARCHITECTURE REQUIREMENTS:",
                "- Include comprehensive infrastructure components (load balancers, caches, monitoring)",
                "- Design for horizontal scaling and distributed architecture",
                "- Implement proper service mesh and API gateway patterns",
                "- Add observability stack (metrics, logging, tracing)",
                "- Include security layers and authentication services",
                ""
            ])
        
        if criticality_level in ['critical', 'mission_critical']:
            prompt_parts.extend([
                "⚡ MISSION-CRITICAL SYSTEM REQUIREMENTS:",
                "- Implement circuit breakers and fallback mechanisms",
                "- Design for high availability and disaster recovery",
                "- Add comprehensive monitoring, alerting, and health checks",
                "- Include audit logging and compliance considerations",
                "- Plan for zero-downtime deployments and auto-recovery",
                ""
            ])
        
        performance_req = complexity_analysis.get('performance_requirements', 'optimized')
        if performance_req in ['high_performance', 'ultra_high_performance']:
            prompt_parts.extend([
                "🚀 HIGH PERFORMANCE REQUIREMENTS:",
                "- Include multiple caching layers (in-memory, distributed, CDN)",
                "- Design for minimal latency with edge computing considerations",
                "- Implement async processing and event-driven patterns",
                "- Add performance monitoring and real-time optimization",
                ""
            ])
        
        prompt_parts.extend([
            "ARCHITECTURE COMPONENT GUIDANCE:",
            f"- Target component count: {complexity_analysis.get('required_components_count', '6-10')}",
            f"- Include infrastructure needs: {', '.join(complexity_analysis.get('infrastructure_needs', ['load_balancing', 'caching']))}",
            f"- Apply patterns: {', '.join(complexity_analysis.get('architecture_patterns_suggested', ['layered']))}",
            "",
            "REQUIREMENTS ANALYSIS:"
        ])
        
        # Add functional requirements
        if functional_reqs := requirements.get("functional_requirements", []):
            prompt_parts.append("Functional Requirements:")
            for req in functional_reqs:
                prompt_parts.append(f"- {req}")
        
        # Add non-functional requirements
        if non_functional_reqs := requirements.get("non_functional_requirements", []):
            prompt_parts.append("Non-Functional Requirements:")
            for req in non_functional_reqs:
                prompt_parts.append(f"- {req}")
        
        # Add business requirements
        if business_reqs := requirements.get("business_requirements", []):
            prompt_parts.append("Business Requirements:")
            for req in business_reqs:
                prompt_parts.append(f"- {req}")
        
        # Add research insights
        if research_data:
            prompt_parts.append("\nRESEARCH INSIGHTS:")
            
            if patterns := research_data.get("architecture_patterns", []):
                prompt_parts.append("Recommended Architecture Patterns:")
                for pattern in patterns[:3]:
                    prompt_parts.append(f"- {pattern.get('name', '')}: {pattern.get('description', '')}")
            
            if tech_recs := research_data.get("technology_recommendations", []):
                prompt_parts.append("Technology Recommendations:")
                for tech in tech_recs[:5]:
                    prompt_parts.append(f"- {tech.get('category', '')}: {tech.get('technology', '')} - {tech.get('rationale', '')}")
        
        # Add business context
        if business_context := state.business_context:
            prompt_parts.extend([
                "",
                "BUSINESS CONTEXT:",
                f"Industry: {getattr(business_context, 'industry', 'Not specified')}",
                f"Company Size: {getattr(business_context, 'company_size', 'Not specified')}",
                f"Budget: {getattr(business_context, 'budget_range', 'Not specified')}",
                f"Timeline: {getattr(business_context, 'timeline', 'Not specified')}"
            ])
        
        prompt_parts.extend([
            "",
            "Please design a comprehensive architecture that:",
            "1. Addresses all functional and non-functional requirements",
            "2. Incorporates research insights and best practices",
            "3. Is appropriate for the user's expertise level",
            "4. Considers business constraints and context",
            "5. Provides clear implementation guidance",
            "",
            "🔗 CRITICAL CONNECTION REQUIREMENTS:",
            "- EVERY component MUST be connected to at least one other component",
            "- Frontend components MUST connect through API Gateway/Load Balancer",
            "- Services MUST connect to databases they use",
            "- All components MUST have realistic, complete data flow connections",
            "- NO isolated/disconnected components are acceptable",
            "- Create connections between related services (e.g., auth service ↔ user data)",
            "",
            "📈 ENHANCEMENT FEATURES GUIDANCE:",
            "- Multi-tenant: Add tenant service, tenant database, tenant middleware",
            "- Scheduling: Add scheduler service, job queue, notification service",
            "- SEO: Add SEO service, content optimization, sitemap generation", 
            "- Email: Add email service, template engine, delivery tracking",
            "",
            "Include detailed component design, data architecture, security considerations, and deployment strategy."
        ])
        
        return "\n".join(prompt_parts)

    def _parse_architecture_response(self, response: str) -> Dict[str, Any]:
        """Parse architecture response from LLM."""
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
            
            architecture_design = json.loads(json_str)
            
            # Validate and set defaults
            self._validate_architecture_design(architecture_design)
            
            return architecture_design
            
        except Exception as e:
            self.logger.warning("Failed to parse architecture response", error=str(e))
            # If we have existing architecture, return it instead of generic fallback
            if hasattr(self, '_current_existing_architecture') and self._current_existing_architecture:
                self.logger.info("Returning existing architecture due to parsing failure")
                return self._current_existing_architecture
            return self._get_fallback_architecture()

    def _validate_architecture_design(self, design: Dict[str, Any]) -> None:
        """Validate and set defaults for architecture design."""
        design.setdefault("architecture_overview", {})
        design.setdefault("components", [])
        design.setdefault("connections", [])
        design.setdefault("system_overview", {})
        design.setdefault("data_architecture", {})
        design.setdefault("security_architecture", {})
        design.setdefault("deployment_architecture", {})
        design.setdefault("scalability_strategy", {})
        design.setdefault("monitoring_observability", {})
        design.setdefault("technology_stack", {})
        design.setdefault("implementation_phases", [])
        design.setdefault("risks_mitigations", [])
        design.setdefault("confidence_score", 0.85)
        
        # Critical validation: Ensure we have components
        if not design.get("components"):
            self.logger.warning("No components found in architecture design - using fallback")
            # If we have existing architecture, preserve it
            if hasattr(self, '_current_existing_architecture') and self._current_existing_architecture:
                design["components"] = self._current_existing_architecture.get("components", [])
                design["connections"] = self._current_existing_architecture.get("connections", [])
            else:
                # Use fallback architecture components
                fallback = self._get_fallback_architecture()
                design["components"] = fallback.get("components", [])
                design["connections"] = fallback.get("connections", [])
        
        # Ensure visualization metadata exists for components
        for component in design.get("components", []):
            if "visualization_metadata" not in component:
                component["visualization_metadata"] = {
                    "layer_assignments": {
                        "system_overview": "core_system",
                        "deployment": "application"
                    },
                    "business_criticality": "medium",
                    "visual_importance": 5,
                    "icon_category": "backend",
                    "technology_badges": [],
                    "health_indicators": {
                        "monitoring_required": True,
                        "performance_critical": False,
                        "availability_target": "99%"
                    }
                }
        
        # Ensure visualization metadata exists for connections
        for connection in design.get("connections", []):
            if "visualization_metadata" not in connection:
                connection["visualization_metadata"] = {
                    "protocol_display": "HTTP/REST",
                    "traffic_volume": "medium",
                    "latency_requirement": "near_real_time",
                    "security_level": "medium",
                    "dependency_strength": "important",
                    "line_style": "solid",
                    "animation_type": "unidirectional"
                }

    def _generate_visualization_data(self, architecture_design: Dict[str, Any]) -> Dict[str, Any]:
        """Generate enhanced visualization data for two-layer system."""
        components = architecture_design.get("components", [])
        connections = architecture_design.get("connections", [])
        system_overview = architecture_design.get("system_overview", {})
        deployment_arch = architecture_design.get("deployment_architecture", {})
        
        # Generate enhanced nodes for D3.js visualization
        nodes = []
        for i, component in enumerate(components):
            viz_metadata = component.get("visualization_metadata", {})
            
            nodes.append({
                "id": component.get("id", f"component_{i}"),
                "name": component.get("name", f"Component {i+1}"),
                "type": component.get("type", "service"),
                "description": component.get("description", ""),
                "technology": component.get("technology", ""),
                "group": self._get_component_group(component.get("type", "service")),
                
                # Enhanced visualization properties
                "visual_importance": viz_metadata.get("visual_importance", 5),
                "business_criticality": viz_metadata.get("business_criticality", "medium"),
                "icon_category": viz_metadata.get("icon_category", "backend"),
                "technology_badges": viz_metadata.get("technology_badges", []),
                "layer_assignments": viz_metadata.get("layer_assignments", {}),
                "health_indicators": viz_metadata.get("health_indicators", {}),
                
                # Layer-specific positioning hints
                "system_overview_position": self._get_system_overview_position(component, system_overview, i),
                "deployment_position": self._get_deployment_position(component, deployment_arch, i)
            })
        
        # Generate enhanced links for D3.js visualization
        links = []
        for connection in connections:
            viz_metadata = connection.get("visualization_metadata", {})
            
            links.append({
                "source": connection.get("from_component", ""),
                "target": connection.get("to_component", ""),
                "type": connection.get("connection_type", "http"),
                "description": connection.get("description", ""),
                "data_flow": connection.get("data_flow", "request_response"),
                
                # Enhanced visualization properties
                "protocol_display": viz_metadata.get("protocol_display", "HTTP/REST"),
                "traffic_volume": viz_metadata.get("traffic_volume", "medium"),
                "latency_requirement": viz_metadata.get("latency_requirement", "near_real_time"),
                "security_level": viz_metadata.get("security_level", "medium"),
                "dependency_strength": viz_metadata.get("dependency_strength", "important"),
                "line_style": viz_metadata.get("line_style", "solid"),
                "animation_type": viz_metadata.get("animation_type", "unidirectional")
            })
        
        # Generate layer-specific data
        layer_data = {
            "system_overview": self._generate_system_overview_data(components, connections, system_overview),
            "deployment": self._generate_deployment_data(components, connections, deployment_arch)
        }
        
        # Generate enhanced Mermaid diagrams for each layer
        mermaid_diagrams = {
            "system_overview": self._generate_mermaid_diagram(components, connections, "system_overview"),
            "deployment": self._generate_mermaid_diagram(components, connections, "deployment")
        }
        
        return {
            "d3_data": {
                "nodes": nodes,
                "links": links
            },
            "layer_data": layer_data,
            "mermaid_diagrams": mermaid_diagrams,
            "diagram_types": ["system_overview", "deployment"],
            "layout_options": ["business_capability", "infrastructure_zones", "hierarchical"],
            "visualization_metadata": {
                "total_components": len(components),
                "total_connections": len(connections),
                "complexity_score": self._calculate_complexity_score(components, connections),
                "recommended_default_view": "system_overview"
            }
        }

    def _get_component_group(self, component_type: str) -> int:
        """Get component group for visualization."""
        type_groups = {
            "service": 1,
            "database": 2,
            "gateway": 3,
            "cache": 4,
            "queue": 5,
            "frontend": 6,
            "external": 7
        }
        return type_groups.get(component_type, 1)

    def _get_system_overview_position(self, component: Dict, system_overview: Dict, index: int) -> Dict[str, int]:
        """Get positioning hints for System Overview layer."""
        # Business capability-based positioning
        capabilities = system_overview.get("business_capabilities", [])
        for cap in capabilities:
            if component.get("id") in cap.get("components", []):
                return {
                    "x": 200 + (capabilities.index(cap) * 300),
                    "y": 150,
                    "priority": cap.get("priority", "medium")
                }
        
        # Default positioning
        return {
            "x": 100 + (index % 3) * 250,
            "y": 100 + (index // 3) * 200,
            "priority": "medium"
        }
    
    def _get_deployment_position(self, component: Dict, deployment_arch: Dict, index: int) -> Dict[str, int]:
        """Get positioning hints for Deployment Architecture layer."""
        # Zone-based positioning
        zones = deployment_arch.get("infrastructure_zones", [])
        for zone in zones:
            if component.get("id") in zone.get("components", []):
                zone_index = zones.index(zone)
                return {
                    "x": 150 + (zone_index * 200),
                    "y": 100 + (zone.get("security_level") == "high" and 50 or 150),
                    "zone": zone.get("zone", "application")
                }
        
        # Default positioning
        return {
            "x": 100 + (index % 4) * 200,
            "y": 100 + (index // 4) * 150,
            "zone": "application"
        }
    
    def _generate_system_overview_data(self, components: List[Dict], connections: List[Dict], system_overview: Dict) -> Dict[str, Any]:
        """Generate System Overview layer-specific data."""
        return {
            "business_capabilities": system_overview.get("business_capabilities", []),
            "core_systems": system_overview.get("core_systems", []),
            "external_integrations": system_overview.get("external_integrations", []),
            "data_domains": system_overview.get("data_domains", []),
            "layout_type": "business_capability",
            "grouping_strategy": "by_capability"
        }
    
    def _generate_deployment_data(self, components: List[Dict], connections: List[Dict], deployment_arch: Dict) -> Dict[str, Any]:
        """Generate Deployment Architecture layer-specific data."""
        return {
            "infrastructure_zones": deployment_arch.get("infrastructure_zones", []),
            "container_clusters": deployment_arch.get("container_clusters", []),
            "network_topology": deployment_arch.get("network_topology", {}),
            "layout_type": "infrastructure_zones",
            "grouping_strategy": "by_zone"
        }
    
    def _calculate_complexity_score(self, components: List[Dict], connections: List[Dict]) -> int:
        """Calculate architecture complexity score (1-10)."""
        component_count = len(components)
        connection_count = len(connections)
        
        # Simple scoring algorithm
        if component_count <= 3 and connection_count <= 3:
            return 1  # Very Simple
        elif component_count <= 6 and connection_count <= 8:
            return 3  # Simple
        elif component_count <= 10 and connection_count <= 15:
            return 5  # Medium
        elif component_count <= 15 and connection_count <= 25:
            return 7  # Complex
        else:
            return 10  # Very Complex

    def _generate_mermaid_diagram(self, components: List[Dict], connections: List[Dict], layer_type: str = "system_overview") -> str:
        """Generate Mermaid diagram syntax."""
        mermaid_lines = ["graph TD"]
        
        # Add component nodes
        for component in components:
            comp_id = component.get("id", "")
            comp_name = component.get("name", "")
            comp_type = component.get("type", "service")
            
            # Choose node shape based on type
            if comp_type == "database":
                mermaid_lines.append(f"    {comp_id}[({comp_name})]")
            elif comp_type == "gateway":
                mermaid_lines.append(f"    {comp_id}{{{comp_name}}}")
            elif comp_type == "queue":
                mermaid_lines.append(f"    {comp_id}>{comp_name}]")
            else:
                mermaid_lines.append(f"    {comp_id}[{comp_name}]")
        
        # Add connections
        for connection in connections:
            from_comp = connection.get("from_component", "")
            to_comp = connection.get("to_component", "")
            conn_type = connection.get("connection_type", "http")
            
            # Choose arrow style based on connection type
            if conn_type == "message_queue":
                mermaid_lines.append(f"    {from_comp} -.-> {to_comp}")
            elif conn_type == "database":
                mermaid_lines.append(f"    {from_comp} --> {to_comp}")
            else:
                mermaid_lines.append(f"    {from_comp} --> {to_comp}")
        
        return "\n".join(mermaid_lines)

    def _get_fallback_architecture(self) -> Dict[str, Any]:
        """Get fallback architecture design."""
        return {
            "architecture_overview": {
                "pattern": "layered",
                "description": "Traditional three-tier architecture with presentation, business, and data layers",
                "key_principles": ["Separation of concerns", "Scalability", "Maintainability"]
            },
            "components": [
                {
                    "id": "frontend",
                    "name": "Frontend Application",
                    "type": "frontend",
                    "description": "User interface and presentation layer",
                    "responsibilities": ["User interaction", "Data presentation", "Client-side validation"],
                    "technology": "React",
                    "scalability": "horizontal",
                    "dependencies": ["api-gateway"],
                    "visualization_metadata": {
                        "layer_assignments": {
                            "system_overview": "core_system",
                            "deployment": "dmz"
                        },
                        "business_criticality": "high",
                        "visual_importance": 8,
                        "icon_category": "frontend",
                        "technology_badges": ["react", "javascript"],
                        "health_indicators": {
                            "monitoring_required": True,
                            "performance_critical": True,
                            "availability_target": "99.9%"
                        }
                    }
                },
                {
                    "id": "api-gateway",
                    "name": "API Gateway",
                    "type": "gateway",
                    "description": "Central entry point for all client requests",
                    "responsibilities": ["Request routing", "Authentication", "Rate limiting"],
                    "technology": "Express.js",
                    "scalability": "horizontal",
                    "dependencies": ["backend-service"],
                    "visualization_metadata": {
                        "layer_assignments": {
                            "system_overview": "core_system",
                            "deployment": "dmz"
                        },
                        "business_criticality": "high",
                        "visual_importance": 7,
                        "icon_category": "backend",
                        "technology_badges": ["express", "nodejs"],
                        "health_indicators": {
                            "monitoring_required": True,
                            "performance_critical": True,
                            "availability_target": "99.9%"
                        }
                    }
                },
                {
                    "id": "backend-service",
                    "name": "Backend Service",
                    "type": "service",
                    "description": "Core business logic and data processing",
                    "responsibilities": ["Business logic", "Data validation", "External integrations"],
                    "technology": "Node.js",
                    "scalability": "horizontal",
                    "dependencies": ["database"],
                    "visualization_metadata": {
                        "layer_assignments": {
                            "system_overview": "core_system",
                            "deployment": "application"
                        },
                        "business_criticality": "high",
                        "visual_importance": 9,
                        "icon_category": "backend",
                        "technology_badges": ["nodejs", "javascript"],
                        "health_indicators": {
                            "monitoring_required": True,
                            "performance_critical": True,
                            "availability_target": "99.9%"
                        }
                    }
                },
                {
                    "id": "database",
                    "name": "Primary Database",
                    "type": "database",
                    "description": "Main data storage for application data",
                    "responsibilities": ["Data persistence", "Data integrity", "Query processing"],
                    "technology": "PostgreSQL",
                    "scalability": "vertical",
                    "dependencies": [],
                    "visualization_metadata": {
                        "layer_assignments": {
                            "system_overview": "data_component",
                            "deployment": "data"
                        },
                        "business_criticality": "high",
                        "visual_importance": 8,
                        "icon_category": "database",
                        "technology_badges": ["postgresql", "sql"],
                        "health_indicators": {
                            "monitoring_required": True,
                            "performance_critical": True,
                            "availability_target": "99.99%"
                        }
                    }
                }
            ],
            "connections": [
                {
                    "from_component": "frontend",
                    "to_component": "api-gateway",
                    "connection_type": "http",
                    "description": "User requests and responses",
                    "data_flow": "request_response",
                    "visualization_metadata": {
                        "protocol_display": "HTTPS/REST",
                        "traffic_volume": "high",
                        "latency_requirement": "real_time",
                        "security_level": "high",
                        "dependency_strength": "critical",
                        "line_style": "solid",
                        "animation_type": "bidirectional"
                    }
                },
                {
                    "from_component": "api-gateway",
                    "to_component": "backend-service",
                    "connection_type": "http",
                    "description": "API calls to business logic",
                    "data_flow": "request_response",
                    "visualization_metadata": {
                        "protocol_display": "HTTP/REST",
                        "traffic_volume": "high",
                        "latency_requirement": "near_real_time",
                        "security_level": "medium",
                        "dependency_strength": "critical",
                        "line_style": "solid",
                        "animation_type": "unidirectional"
                    }
                },
                {
                    "from_component": "backend-service",
                    "to_component": "database",
                    "connection_type": "database",
                    "description": "Data operations",
                    "data_flow": "request_response",
                    "visualization_metadata": {
                        "protocol_display": "PostgreSQL",
                        "traffic_volume": "medium",
                        "latency_requirement": "near_real_time",
                        "security_level": "high",
                        "dependency_strength": "critical",
                        "line_style": "solid",
                        "animation_type": "unidirectional"
                    }
                }
            ],
            "system_overview": {
                "business_capabilities": [
                    {
                        "capability": "User Interface Management",
                        "components": ["frontend"],
                        "business_value": "User experience and engagement",
                        "complexity": "medium",
                        "priority": "high"
                    },
                    {
                        "capability": "API Management",
                        "components": ["api-gateway", "backend-service"],
                        "business_value": "Secure and scalable API operations",
                        "complexity": "high",
                        "priority": "high"
                    },
                    {
                        "capability": "Data Management",
                        "components": ["database"],
                        "business_value": "Reliable data storage and retrieval",
                        "complexity": "medium",
                        "priority": "high"
                    }
                ],
                "core_systems": [
                    {
                        "system": "Web Application Platform",
                        "components": ["frontend", "api-gateway", "backend-service"],
                        "purpose": "Primary user-facing application",
                        "criticality": "high",
                        "user_facing": True
                    }
                ],
                "external_integrations": [],
                "data_domains": [
                    {
                        "domain": "Application Data",
                        "components": ["backend-service", "database"],
                        "sensitivity": "high",
                        "data_types": ["user_data", "business_data"]
                    }
                ]
            },
            "deployment_architecture": {
                "strategy": "containers",
                "orchestration": "docker",
                "environments": ["development", "staging", "production"],
                "ci_cd": "github_actions",
                "infrastructure_zones": [
                    {
                        "zone": "DMZ",
                        "components": ["frontend", "api-gateway"],
                        "security_level": "high",
                        "network_access": "public",
                        "zone_type": "dmz"
                    },
                    {
                        "zone": "Application Tier",
                        "components": ["backend-service"],
                        "security_level": "medium",
                        "network_access": "private",
                        "zone_type": "application"
                    },
                    {
                        "zone": "Data Tier",
                        "components": ["database"],
                        "security_level": "high",
                        "network_access": "isolated",
                        "zone_type": "data"
                    }
                ],
                "container_clusters": [
                    {
                        "cluster": "Web Frontend Cluster",
                        "components": ["frontend"],
                        "scaling": "auto",
                        "replicas": "2-5",
                        "resource_requirements": "medium"
                    },
                    {
                        "cluster": "API Services Cluster",
                        "components": ["api-gateway", "backend-service"],
                        "scaling": "auto",
                        "replicas": "3-10",
                        "resource_requirements": "high"
                    }
                ],
                "network_topology": {
                    "load_balancers": [
                        {
                            "name": "Frontend Load Balancer",
                            "type": "application",
                            "targets": ["frontend"]
                        }
                    ],
                    "security_groups": [
                        {
                            "name": "Web Security Group",
                            "components": ["frontend", "api-gateway"],
                            "rules": ["HTTPS inbound", "HTTP outbound"]
                        }
                    ]
                }
            },
            "data_architecture": {
                "storage_strategy": "centralized",
                "databases": [
                    {
                        "name": "primary_db",
                        "type": "relational",
                        "purpose": "primary_data",
                        "technology": "postgresql"
                    }
                ],
                "data_flow": "Client requests flow through API gateway to backend service and database"
            },
            "security_architecture": {
                "authentication": "jwt",
                "authorization": "rbac",
                "data_protection": ["encryption", "access_control"],
                "network_security": ["firewall", "ssl_tls"]
            },
            "deployment_architecture": {
                "strategy": "containers",
                "orchestration": "docker",
                "environments": ["development", "staging", "production"],
                "ci_cd": "github_actions"
            },
            "technology_stack": {
                "frontend": "react",
                "backend": "node",
                "database": "postgresql",
                "infrastructure": "aws"
            },
            "visualization_data": {
                "d3_data": {
                    "nodes": [
                        {"id": "frontend", "name": "Frontend", "type": "frontend", "x": 100, "y": 100, "group": 6},
                        {"id": "api-gateway", "name": "API Gateway", "type": "gateway", "x": 300, "y": 100, "group": 3},
                        {"id": "backend-service", "name": "Backend", "type": "service", "x": 500, "y": 100, "group": 1},
                        {"id": "database", "name": "Database", "type": "database", "x": 700, "y": 100, "group": 2}
                    ],
                    "links": [
                        {"source": "frontend", "target": "api-gateway", "type": "http"},
                        {"source": "api-gateway", "target": "backend-service", "type": "http"},
                        {"source": "backend-service", "target": "database", "type": "database"}
                    ]
                },
                "mermaid_diagram": "graph TD\n    frontend[Frontend]\n    api-gateway{API Gateway}\n    backend-service[Backend]\n    database[(Database)]\n    frontend --> api-gateway\n    api-gateway --> backend-service\n    backend-service --> database"
            },
            "confidence_score": 0.8
        }
