#!/usr/bin/env python3
"""
Context-Enhanced Agent
Combines LangGraph Agent with MCP Context Studio for enhanced responses
"""

import os
import sys
from typing import Dict, Any, Optional

# Use standalone MCP client to avoid import issues
from mcp_client_standalone import MCPContextStudioClient
from agent_client import AgentClient, AgentResponse


class ContextEnhancedAgent:
    """Agent that enhances requests with MCP Context Studio data"""
    
    def __init__(self):
        """Initialize the context-enhanced agent"""
        self.mcp_client = MCPContextStudioClient()
        self.agent_client = AgentClient()
        self.context_cache = {}
    
    def create_dockerfile_with_context(
        self,
        language: str,
        framework: str,
        environment: str = "production"
    ) -> AgentResponse:
        """
        Create Dockerfile enhanced with enterprise context.
        
        Args:
            language: Programming language
            framework: Framework
            environment: Target environment
        
        Returns:
            Enhanced agent response
        """
        # Search for relevant context
        context_query = f"{language} {framework} Docker best practices security"
        context_results = self.mcp_client.search_context(context_query, limit=3)
        
        # Build enhanced message
        context_info = self._format_context(context_results)
        message = f"""Create a production-ready Dockerfile for {language} {framework} application.

Enterprise Context and Best Practices:
{context_info}

Ensure the Dockerfile follows these enterprise standards and security guidelines."""
        
        # Invoke agent
        return self.agent_client.invoke(
            message=message,
            context={
                "environment": environment,
                "language": language,
                "framework": framework,
                "mcp_enhanced": True
            }
        )
    
    def create_k8s_with_context(
        self,
        app_name: str,
        environment: str = "production",
        replicas: int = 3
    ) -> AgentResponse:
        """
        Create Kubernetes manifests enhanced with enterprise context.
        
        Args:
            app_name: Application name
            environment: Target environment
            replicas: Number of replicas
        
        Returns:
            Enhanced agent response
        """
        # Search for K8s best practices
        context_results = self.mcp_client.search_context(
            "Kubernetes security best practices production deployment",
            limit=3
        )
        
        context_info = self._format_context(context_results)
        message = f"""Generate Kubernetes deployment and service manifests for {app_name}.

Enterprise Standards and Security Requirements:
{context_info}

Apply these standards to the manifests with {replicas} replicas in {environment} environment."""
        
        return self.agent_client.invoke(
            message=message,
            context={
                "app_name": app_name,
                "environment": environment,
                "replicas": replicas,
                "mcp_enhanced": True
            }
        )
    
    def create_cicd_with_context(
        self,
        provider: str,
        language: str,
        environment: str = "production"
    ) -> AgentResponse:
        """
        Create CI/CD pipeline enhanced with enterprise context.
        
        Args:
            provider: CI/CD provider (github, gitlab, etc.)
            language: Programming language
            environment: Target environment
        
        Returns:
            Enhanced agent response
        """
        # Search for CI/CD best practices
        context_results = self.mcp_client.search_context(
            f"{provider} CI/CD pipeline security best practices {language}",
            limit=3
        )
        
        context_info = self._format_context(context_results)
        message = f"""Create a {provider} CI/CD pipeline for {language} application.

Enterprise CI/CD Standards:
{context_info}

Include testing, security scanning, and deployment to {environment}."""
        
        return self.agent_client.invoke(
            message=message,
            context={
                "provider": provider,
                "language": language,
                "environment": environment,
                "mcp_enhanced": True
            }
        )
    
    def create_complete_setup_with_context(
        self,
        app_name: str,
        language: str,
        framework: str,
        architecture: str = "microservices"
    ) -> Dict[str, AgentResponse]:
        """
        Create complete DevOps setup with enterprise context.
        
        Args:
            app_name: Application name
            language: Programming language
            framework: Framework
            architecture: Architecture type
        
        Returns:
            Dictionary of enhanced responses
        """
        results = {}
        
        # Create Dockerfile with context
        print(f"Creating Dockerfile for {language} {framework}...")
        results['dockerfile'] = self.create_dockerfile_with_context(
            language, framework
        )
        
        # Create K8s manifests with context
        print(f"Creating Kubernetes manifests for {app_name}...")
        results['kubernetes'] = self.create_k8s_with_context(app_name)
        
        # Create CI/CD pipeline with context
        print(f"Creating CI/CD pipeline...")
        results['cicd'] = self.create_cicd_with_context("github", language)
        
        return results
    
    def _format_context(self, context_results: list) -> str:
        """
        Format context results for inclusion in prompt.
        
        Args:
            context_results: List of context items
        
        Returns:
            Formatted context string
        """
        if not context_results:
            return """- Follow security best practices
- Use minimal base images
- Implement proper error handling
- Include health checks and monitoring"""
        
        formatted = []
        for i, item in enumerate(context_results, 1):
            if isinstance(item, dict):
                content = item.get('content', item.get('text', ''))
                if content:
                    # Truncate long content
                    truncated = content[:200] + "..." if len(content) > 200 else content
                    formatted.append(f"{i}. {truncated}")
        
        return "\n".join(formatted) if formatted else "No additional context available"
    
    def get_cached_context(self, key: str) -> Optional[Any]:
        """Get cached context"""
        return self.context_cache.get(key)
    
    def set_cached_context(self, key: str, value: Any):
        """Set cached context"""
        self.context_cache[key] = value


# Example usage and testing
def main():
    """Example usage of ContextEnhancedAgent"""
    print("=" * 80)
    print("  Context-Enhanced Agent Example")
    print("=" * 80)
    
    # Initialize agent
    print("\n🔧 Initializing context-enhanced agent...")
    try:
        agent = ContextEnhancedAgent()
        print("✅ Agent initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return
    
    # Example 1: Create Dockerfile with context
    print("\n" + "=" * 80)
    print("  Example 1: Create Dockerfile with Enterprise Context")
    print("=" * 80)
    
    try:
        result = agent.create_dockerfile_with_context("python", "fastapi")
        print(f"\n✅ Status: {result.status}")
        print(f"📊 Confidence: {result.confidence_score:.2%}")
        
        if "dockerfile" in result.artifacts:
            dockerfile = result.artifacts["dockerfile"]
            lines = dockerfile.split('\n')[:10]
            print(f"\n📄 Dockerfile Preview:")
            for line in lines:
                print(f"   {line}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 2: Create K8s manifests with context
    print("\n" + "=" * 80)
    print("  Example 2: Create Kubernetes Manifests with Context")
    print("=" * 80)
    
    try:
        result = agent.create_k8s_with_context("my-app", replicas=3)
        print(f"\n✅ Status: {result.status}")
        print(f"📊 Confidence: {result.confidence_score:.2%}")
        print(f"📦 Artifacts: {', '.join(result.artifacts.keys())}")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    # Example 3: Create complete setup
    print("\n" + "=" * 80)
    print("  Example 3: Create Complete DevOps Setup with Context")
    print("=" * 80)
    
    try:
        results = agent.create_complete_setup_with_context(
            app_name="my-app",
            language="python",
            framework="fastapi",
            architecture="microservices"
        )
        
        print(f"\n✅ Created {len(results)} components:")
        for component, result in results.items():
            print(f"   - {component}: {result.status} (confidence: {result.confidence_score:.2%})")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("  Examples Complete!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
