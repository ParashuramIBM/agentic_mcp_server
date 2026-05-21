"""
Agent Client - Python wrapper for invoking the LangGraph DevOps Agent
This demonstrates how to create a new agent that invokes the deployed agent via A2A protocol.

Usage:
    from agent_client import AgentClient
    
    client = AgentClient()
    result = client.create_dockerfile("python", "fastapi")
    print(result)
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List, Iterator
from dataclasses import dataclass
from enum import Enum


class TaskType(Enum):
    """Supported task types"""
    DEVOPS = "devops"
    CODE_REVIEW = "code_review"
    ORCHESTRATION = "orchestration"
    MULTI = "multi"
    AUTO = "auto"


class Environment(Enum):
    """Target environments"""
    DEV = "dev"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class AgentResponse:
    """Response from agent invocation"""
    request_id: str
    status: str
    message: str
    artifacts: Dict[str, Any]
    confidence_score: float
    metadata: Dict[str, Any]
    error: Optional[str] = None


class AgentClient:
    """
    Client for invoking the LangGraph DevOps Agent via A2A protocol.
    
    This can be used as a template for creating new agents that leverage
    the deployed agent's capabilities.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        agent_url: Optional[str] = None
    ):
        """
        Initialize the agent client.
        
        Args:
            api_key: Agentic Studio API key (defaults to AGENTIC_STUDIO_API_KEY env var)
            agent_url: Agent endpoint URL (defaults to the deployed agent)
        """
        self.api_key = api_key or os.getenv("AGENTIC_STUDIO_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set AGENTIC_STUDIO_API_KEY or pass api_key parameter")
        
        self.agent_url = agent_url or (
            "https://servicesessentials.ibm.com/agenticapps/a2a/"
            "511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/"
            "e571f647-8fff-48d1-a6b5-5aea1205e024"
        )
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_agent_card(self) -> Dict[str, Any]:
        """
        Get agent metadata and capabilities (discovery).
        
        Returns:
            Agent card with metadata
        """
        response = requests.get(self.agent_url, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def invoke(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AgentResponse:
        """
        Invoke the agent with a message/task.
        
        Args:
            message: The task or request
            context: Additional context (environment, language, framework, etc.)
        
        Returns:
            AgentResponse with results
        """
        payload = {
            "message": message,
            "context": context or {}
        }
        
        response = requests.post(
            self.agent_url,
            headers=self.headers,
            json=payload
        )
        response.raise_for_status()
        
        data = response.json()
        return AgentResponse(
            request_id=data.get("request_id", ""),
            status=data.get("status", ""),
            message=data.get("response", {}).get("message", ""),
            artifacts=data.get("response", {}).get("artifacts", {}),
            confidence_score=data.get("response", {}).get("confidence_score", 0.0),
            metadata=data.get("metadata", {}),
            error=data.get("error")
        )
    
    def invoke_streaming(self, message: str, context: Optional[Dict[str, Any]] = None) -> Iterator[Dict[str, Any]]:
        """
        Invoke agent with streaming response.
        
        Args:
            message: The task or request
            context: Additional context
        
        Yields:
            Streaming events
        """
        payload = {
            "message": message,
            "context": context or {},
            "stream": True
        }
        
        headers = {**self.headers, "Accept": "text/event-stream"}
        
        response = requests.post(
            self.agent_url,
            headers=headers,
            json=payload,
            stream=True
        )
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8')
                if line.startswith('data: '):
                    yield json.loads(line[6:])
    
    # ========================================================================
    # High-level convenience methods
    # ========================================================================
    
    def create_dockerfile(
        self,
        language: str,
        framework: str,
        environment: str = "production",
        features: Optional[List[str]] = None
    ) -> AgentResponse:
        """
        Create a Dockerfile for an application.
        
        Args:
            language: Programming language (python, nodejs, java, etc.)
            framework: Framework (fastapi, express, spring, etc.)
            environment: Target environment
            features: Additional features (multi-stage, security-hardened, etc.)
        
        Returns:
            AgentResponse with Dockerfile
        """
        message = f"Create a production-ready Dockerfile for {language} {framework} application"
        if features:
            message += f" with {', '.join(features)}"
        
        context = {
            "environment": environment,
            "language": language,
            "framework": framework,
            "features": features or []
        }
        
        return self.invoke(message, context)
    
    def create_kubernetes_manifests(
        self,
        app_name: str,
        environment: str = "production",
        replicas: int = 3,
        port: int = 8000
    ) -> AgentResponse:
        """
        Generate Kubernetes deployment and service manifests.
        
        Args:
            app_name: Application name
            environment: Target environment
            replicas: Number of replicas
            port: Application port
        
        Returns:
            AgentResponse with Kubernetes manifests
        """
        message = f"Generate Kubernetes deployment and service manifests for {app_name} in {environment} environment"
        
        context = {
            "app_name": app_name,
            "environment": environment,
            "replicas": replicas,
            "port": port
        }
        
        return self.invoke(message, context)
    
    def create_cicd_pipeline(
        self,
        provider: str,
        language: str,
        stages: Optional[List[str]] = None
    ) -> AgentResponse:
        """
        Create a CI/CD pipeline configuration.
        
        Args:
            provider: CI/CD provider (github, gitlab, jenkins, etc.)
            language: Programming language
            stages: Pipeline stages (test, build, deploy, etc.)
        
        Returns:
            AgentResponse with pipeline configuration
        """
        stages = stages or ["test", "security-scan", "build", "deploy"]
        message = f"Create a {provider} CI/CD pipeline with {', '.join(stages)}"
        
        context = {
            "provider": provider,
            "language": language,
            "stages": stages
        }
        
        return self.invoke(message, context)
    
    def create_complete_devops_setup(
        self,
        architecture: str,
        language: str,
        framework: str,
        services: List[str],
        cloud: str = "aws"
    ) -> AgentResponse:
        """
        Create a complete DevOps setup (Dockerfile, K8s, CI/CD).
        
        Args:
            architecture: Architecture type (microservices, monolith, etc.)
            language: Programming language
            framework: Framework
            services: List of services
            cloud: Cloud provider
        
        Returns:
            AgentResponse with complete setup
        """
        message = (
            f"Create a complete DevOps setup including Dockerfile, "
            f"Kubernetes manifests, and CI/CD pipeline for a {language} "
            f"{framework} {architecture} application"
        )
        
        context = {
            "architecture": architecture,
            "language": language,
            "framework": framework,
            "services": services,
            "cloud": cloud
        }
        
        return self.invoke(message, context)


# ============================================================================
# Example Usage
# ============================================================================

def main():
    """Example usage of the AgentClient"""
    
    # Initialize client
    client = AgentClient()
    
    print("=" * 80)
    print("LangGraph DevOps Agent Client - Examples")
    print("=" * 80)
    
    # Example 1: Get agent card
    print("\n1. Getting agent card...")
    try:
        card = client.get_agent_card()
        print(f"   Agent: {card.get('name', 'N/A')}")
        print(f"   Version: {card.get('version', 'N/A')}")
        print(f"   Capabilities: {', '.join(card.get('capabilities', []))}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 2: Create Dockerfile
    print("\n2. Creating Dockerfile for Python FastAPI...")
    try:
        result = client.create_dockerfile(
            language="python",
            framework="fastapi",
            environment="production",
            features=["multi-stage", "security-hardened"]
        )
        print(f"   Status: {result.status}")
        print(f"   Confidence: {result.confidence_score}")
        if "dockerfile" in result.artifacts:
            print(f"   Dockerfile created: {len(result.artifacts['dockerfile'])} bytes")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 3: Create Kubernetes manifests
    print("\n3. Creating Kubernetes manifests...")
    try:
        result = client.create_kubernetes_manifests(
            app_name="my-app",
            environment="production",
            replicas=3,
            port=8000
        )
        print(f"   Status: {result.status}")
        print(f"   Artifacts: {', '.join(result.artifacts.keys())}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 4: Create CI/CD pipeline
    print("\n4. Creating GitHub Actions pipeline...")
    try:
        result = client.create_cicd_pipeline(
            provider="github",
            language="python",
            stages=["test", "security-scan", "build", "deploy"]
        )
        print(f"   Status: {result.status}")
        print(f"   Message: {result.message[:100]}...")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Example 5: Complete DevOps setup
    print("\n5. Creating complete DevOps setup...")
    try:
        result = client.create_complete_devops_setup(
            architecture="microservices",
            language="nodejs",
            framework="express",
            services=["api-gateway", "auth-service", "user-service"],
            cloud="aws"
        )
        print(f"   Status: {result.status}")
        print(f"   Artifacts: {', '.join(result.artifacts.keys())}")
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

# Made with Bob
