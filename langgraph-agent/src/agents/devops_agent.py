"""
DevOps Automation Agent - Handles CI/CD, infrastructure, and deployment tasks
"""

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.graph.state import AgentState, AgentResponse
from src.config.settings import settings
from src.tools.devops_tools import DevOpsTools
import logging
import json

logger = logging.getLogger(__name__)


class DevOpsAgent:
    """
    DevOps automation agent that handles:
    - CI/CD pipeline creation
    - Docker and containerization
    - Kubernetes configuration
    - Infrastructure provisioning
    - Deployment automation
    """
    
    def __init__(self):
        """Initialize DevOps agent with LLM and tools"""
        self.llm = ChatOpenAI(
            model=settings.devops_model,
            temperature=0.3,  # Lower temperature for more deterministic outputs
            max_tokens=settings.model_max_tokens
        )
        
        self.tools = DevOpsTools()
        
        logger.info(f"DevOps agent initialized with model: {settings.devops_model}")
    
    def execute(self, state: AgentState) -> Dict[str, Any]:
        """
        Execute DevOps task based on user input.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with DevOps agent response
        """
        try:
            user_input = state["user_input"]
            context = state.get("context", {})
            files = state.get("files", [])
            repository = state.get("repository")
            environment = state.get("environment", "dev")
            
            logger.info(f"DevOps agent processing request: {user_input[:100]}...")
            
            # Analyze request and determine what to generate
            analysis = self._analyze_request(user_input, context)
            
            # Generate artifacts based on analysis
            artifacts = self._generate_artifacts(analysis, user_input, environment)
            
            # Create response
            response = self._create_response(analysis, artifacts, user_input)
            
            # Update state
            agent_responses = state.get("agent_responses", {})
            agent_responses["devops_agent"] = response
            
            agent_history = state.get("agent_history", [])
            agent_history.append("devops_agent")
            
            return {
                "agent_responses": agent_responses,
                "agent_history": agent_history,
                "current_agent": "devops_agent"
            }
            
        except Exception as e:
            logger.error(f"Error in DevOps agent: {str(e)}")
            return {
                "error": f"DevOps agent error: {str(e)}",
                "agent_history": state.get("agent_history", []) + ["devops_agent"]
            }
    
    def _analyze_request(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze user request to determine what artifacts to generate.
        
        Args:
            user_input: User's request
            context: Additional context
        
        Returns:
            Analysis results
        """
        system_prompt = """You are a DevOps expert analyzing a request.

Determine what DevOps artifacts need to be generated. Respond with JSON:
{
    "artifacts": ["dockerfile", "kubernetes", "ci_cd", "infrastructure"],
    "language": "python",
    "framework": "fastapi",
    "platform": "kubernetes",
    "ci_cd_provider": "github_actions",
    "cloud_provider": "aws",
    "reasoning": "explanation"
}

Available artifacts:
- dockerfile: Docker container configuration
- kubernetes: Kubernetes manifests (deployment, service, ingress)
- ci_cd: CI/CD pipeline configuration
- infrastructure: Infrastructure as Code (Terraform, etc.)
- monitoring: Monitoring and observability setup
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"Request: {user_input}\nContext: {json.dumps(context)}")
        ]
        
        try:
            response = self.llm.invoke(messages)
            content = response.content
            
            # Parse JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            analysis = json.loads(content)
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing request: {str(e)}")
            # Fallback to keyword-based analysis
            return self._keyword_based_analysis(user_input)
    
    def _keyword_based_analysis(self, user_input: str) -> Dict[str, Any]:
        """
        Fallback analysis based on keywords.
        
        Args:
            user_input: User's request
        
        Returns:
            Analysis results
        """
        user_input_lower = user_input.lower()
        artifacts = []
        
        if any(kw in user_input_lower for kw in ["docker", "dockerfile", "container"]):
            artifacts.append("dockerfile")
        
        if any(kw in user_input_lower for kw in ["kubernetes", "k8s", "deployment", "service"]):
            artifacts.append("kubernetes")
        
        if any(kw in user_input_lower for kw in ["ci/cd", "pipeline", "github actions", "jenkins"]):
            artifacts.append("ci_cd")
        
        if any(kw in user_input_lower for kw in ["infrastructure", "terraform", "provision"]):
            artifacts.append("infrastructure")
        
        if any(kw in user_input_lower for kw in ["monitor", "observability", "prometheus"]):
            artifacts.append("monitoring")
        
        # Default to dockerfile if nothing detected
        if not artifacts:
            artifacts = ["dockerfile"]
        
        return {
            "artifacts": artifacts,
            "language": "python",
            "framework": "fastapi",
            "platform": "kubernetes",
            "ci_cd_provider": "github_actions",
            "cloud_provider": "aws",
            "reasoning": "Keyword-based analysis"
        }
    
    def _generate_artifacts(
        self,
        analysis: Dict[str, Any],
        user_input: str,
        environment: str
    ) -> Dict[str, str]:
        """
        Generate DevOps artifacts based on analysis.
        
        Args:
            analysis: Analysis results
            user_input: Original user input
            environment: Target environment
        
        Returns:
            Generated artifacts
        """
        artifacts = {}
        artifact_types = analysis.get("artifacts", [])
        
        try:
            # Generate Dockerfile
            if "dockerfile" in artifact_types:
                dockerfile = self.tools.create_dockerfile(
                    language=analysis.get("language", "python"),
                    framework=analysis.get("framework", "fastapi"),
                    user_input=user_input
                )
                artifacts["Dockerfile"] = dockerfile
            
            # Generate Kubernetes manifests
            if "kubernetes" in artifact_types:
                k8s_manifests = self.tools.generate_kubernetes_manifests(
                    app_name=analysis.get("app_name", "app"),
                    environment=environment,
                    user_input=user_input
                )
                artifacts.update(k8s_manifests)
            
            # Generate CI/CD pipeline
            if "ci_cd" in artifact_types:
                pipeline = self.tools.create_ci_cd_pipeline(
                    provider=analysis.get("ci_cd_provider", "github_actions"),
                    language=analysis.get("language", "python"),
                    user_input=user_input
                )
                artifacts["ci_cd_pipeline"] = pipeline
            
            # Generate infrastructure code
            if "infrastructure" in artifact_types:
                infra = self.tools.generate_infrastructure_code(
                    cloud_provider=analysis.get("cloud_provider", "aws"),
                    user_input=user_input
                )
                artifacts["infrastructure"] = infra
            
            # Generate monitoring configuration
            if "monitoring" in artifact_types:
                monitoring = self.tools.generate_monitoring_config(
                    user_input=user_input
                )
                artifacts["monitoring"] = monitoring
            
        except Exception as e:
            logger.error(f"Error generating artifacts: {str(e)}")
            artifacts["error"] = str(e)
        
        return artifacts
    
    def _create_response(
        self,
        analysis: Dict[str, Any],
        artifacts: Dict[str, str],
        user_input: str
    ) -> AgentResponse:
        """
        Create agent response with generated artifacts.
        
        Args:
            analysis: Analysis results
            artifacts: Generated artifacts
            user_input: Original user input
        
        Returns:
            Agent response
        """
        # Create output summary
        output_parts = [
            "# DevOps Automation Results\n",
            f"**Analysis**: {analysis.get('reasoning', 'Generated DevOps artifacts')}\n",
            f"\n**Generated Artifacts**: {', '.join(artifacts.keys())}\n\n"
        ]
        
        # Add each artifact
        for name, content in artifacts.items():
            if name != "error":
                output_parts.append(f"## {name}\n")
                output_parts.append(f"```\n{content}\n```\n\n")
        
        if "error" in artifacts:
            output_parts.append(f"\n**Error**: {artifacts['error']}\n")
        
        output = "".join(output_parts)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(analysis, artifacts)
        
        # Generate next steps
        next_steps = self._generate_next_steps(analysis, artifacts)
        
        return AgentResponse(
            agent_name="devops_agent",
            output=output,
            artifacts=artifacts,
            confidence=0.85 if "error" not in artifacts else 0.5,
            suggestions=suggestions,
            next_steps=next_steps,
            metadata={
                "analysis": analysis,
                "artifact_count": len(artifacts)
            }
        )
    
    def _generate_suggestions(
        self,
        analysis: Dict[str, Any],
        artifacts: Dict[str, str]
    ) -> List[str]:
        """Generate suggestions based on artifacts"""
        suggestions = []
        
        if "Dockerfile" in artifacts:
            suggestions.append("Consider using multi-stage builds to reduce image size")
            suggestions.append("Add health checks to your Docker container")
        
        if any("kubernetes" in k.lower() for k in artifacts.keys()):
            suggestions.append("Set resource limits and requests for production")
            suggestions.append("Implement horizontal pod autoscaling")
            suggestions.append("Use ConfigMaps and Secrets for configuration")
        
        if "ci_cd_pipeline" in artifacts:
            suggestions.append("Add security scanning to your CI/CD pipeline")
            suggestions.append("Implement automated testing before deployment")
        
        return suggestions
    
    def _generate_next_steps(
        self,
        analysis: Dict[str, Any],
        artifacts: Dict[str, str]
    ) -> List[str]:
        """Generate next steps"""
        next_steps = []
        
        if "Dockerfile" in artifacts:
            next_steps.append("Build and test the Docker image locally")
            next_steps.append("Push the image to a container registry")
        
        if any("kubernetes" in k.lower() for k in artifacts.keys()):
            next_steps.append("Apply Kubernetes manifests to your cluster")
            next_steps.append("Verify deployment status and pod health")
        
        if "ci_cd_pipeline" in artifacts:
            next_steps.append("Commit the pipeline configuration to your repository")
            next_steps.append("Test the pipeline with a sample commit")
        
        next_steps.append("Set up monitoring and alerting")
        next_steps.append("Document the deployment process")
        
        return next_steps


# Global DevOps agent instance
devops_agent = DevOpsAgent()

# Made with Bob
