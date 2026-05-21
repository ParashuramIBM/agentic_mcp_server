# MCP Context Studio Integration Guide

This guide shows how to integrate the LangGraph DevOps Agent with IBM Context Studio via MCP (Model Context Protocol).

## 🎯 Overview

The MCP Context Studio server provides access to enterprise context and knowledge bases. By integrating it with your LangGraph agent, you can:

- Access enterprise documentation and knowledge
- Retrieve context-specific information
- Enhance agent responses with organizational context
- Connect to shared knowledge repositories

## 🔑 MCP Server Configuration

Your MCP Context Studio server details:

```json
{
  "mcpServers": {
    "context-studio": {
      "type": "streamable-http",
      "url": "https://servicesessentials.ibm.com/mcp-gateway/service/gateway/servers/8ccdd203bdee4014b08e82eedb6046e2/mcp",
      "headers": {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
        "x-api-key": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9..."
      }
    }
  }
}
```

**Server Details:**
- **Server ID**: `8ccdd203bdee4014b08e82eedb6046e2`
- **Context ID**: `ctx_93a08f26fcb9`
- **Team ID**: `6a016fabe9eed92a72d7a945`
- **Type**: Streamable HTTP
- **Gateway**: IBM MCP Gateway

## 🚀 Quick Start

### Step 1: Update MCP Configuration

Update your `langgraph-agent/mcp_config.json`:

```json
{
  "mcpServers": {
    "context-studio": {
      "type": "streamable-http",
      "url": "https://servicesessentials.ibm.com/mcp-gateway/service/gateway/servers/8ccdd203bdee4014b08e82eedb6046e2/mcp",
      "headers": {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaHJhZGRoYS5wYXJpa2gxQGlibS5jb20iLCJqdGkiOiI1MjcxMDY5Ni1jYWMwLTQzZGMtYmUxOS04YmZlMWE5MzZmMTMiLCJ0b2tlbl91c2UiOiJhcGkiLCJpYXQiOjE3NzkyNjMzMTYsImlzcyI6Im1jcGdhdGV3YXkiLCJhdWQiOiJtY3BnYXRld2F5LWFwaSIsInVzZXIiOnsiZW1haWwiOiJzaHJhZGRoYS5wYXJpa2gxQGlibS5jb20iLCJmdWxsX25hbWUiOiJBUEkgVG9rZW4gVXNlciIsImlzX2FkbWluIjp0cnVlLCJhdXRoX3Byb3ZpZGVyIjoiYXBpX3Rva2VuIn0sInRlYW1zIjpudWxsLCJzY29wZXMiOnsic2VydmVyX2lkIjoiOGNjZGQyMDNiZGVlNDAxNGIwOGU4MmVlZGI2MDQ2ZTIiLCJwZXJtaXNzaW9ucyI6W10sImlwX3Jlc3RyaWN0aW9ucyI6W10sInRpbWVfcmVzdHJpY3Rpb25zIjp7fX0sImV4cCI6MTc4NzAzOTMxNn0.aguoRnOyoQiDDUnlrxajgmnX60XLndU-YhMCpEjuBi4",
        "x-api-key": "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbEFkZHJlc3MiOiJwYXJhc2h1cmFtLm5AaWJtLmNvbSIsInRlYW1JZCI6IjZhMDE2ZmFiZTllZWQ5MmE3MmQ3YTk0NSIsImNvbnRleHRJZCI6ImN0eF85M2EwOGYyNmZjYjkiLCJpYXQiOjE3NzkyNjMzMTUsImV4cCI6MTc4NzAzOTMxNSwiaXNzIjoiY29udGV4dC1icm9rZXIiLCJ0b2tlbl9pZCI6IjFjNmM2YjI5LTYxNzItNDQ5Zi05OTYzLTI2NzlkZTMwMzQyNSJ9.o3xFHmuTzXqFd47JiLsXDkxsemmV-OpuNg8eYuDJ0YOUxIJdmuEnqZX-GKtB4ABSsvvnw0HOJfgE_H-GAlR_NQ"
      },
      "disabled": false
    }
  }
}
```

### Step 2: Update Environment Variables

Add to your `.env` file:

```bash
# MCP Context Studio Configuration
MCP_ENABLED=true
MCP_SERVER_URL=https://servicesessentials.ibm.com/mcp-gateway/service/gateway/servers/8ccdd203bdee4014b08e82eedb6046e2/mcp
MCP_SERVER_ID=8ccdd203bdee4014b08e82eedb6046e2
MCP_CONTEXT_ID=ctx_93a08f26fcb9
MCP_TEAM_ID=6a016fabe9eed92a72d7a945

# MCP Authentication
MCP_BEARER_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzaHJhZGRoYS5wYXJpa2gxQGlibS5jb20iLCJqdGkiOiI1MjcxMDY5Ni1jYWMwLTQzZGMtYmUxOS04YmZlMWE5MzZmMTMiLCJ0b2tlbl91c2UiOiJhcGkiLCJpYXQiOjE3NzkyNjMzMTYsImlzcyI6Im1jcGdhdGV3YXkiLCJhdWQiOiJtY3BnYXRld2F5LWFwaSIsInVzZXIiOnsiZW1haWwiOiJzaHJhZGRoYS5wYXJpa2gxQGlibS5jb20iLCJmdWxsX25hbWUiOiJBUEkgVG9rZW4gVXNlciIsImlzX2FkbWluIjp0cnVlLCJhdXRoX3Byb3ZpZGVyIjoiYXBpX3Rva2VuIn0sInRlYW1zIjpudWxsLCJzY29wZXMiOnsic2VydmVyX2lkIjoiOGNjZGQyMDNiZGVlNDAxNGIwOGU4MmVlZGI2MDQ2ZTIiLCJwZXJtaXNzaW9ucyI6W10sImlwX3Jlc3RyaWN0aW9ucyI6W10sInRpbWVfcmVzdHJpY3Rpb25zIjp7fX0sImV4cCI6MTc4NzAzOTMxNn0.aguoRnOyoQiDDUnlrxajgmnX60XLndU-YhMCpEjuBi4
MCP_API_KEY=eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbEFkZHJlc3MiOiJwYXJhc2h1cmFtLm5AaWJtLmNvbSIsInRlYW1JZCI6IjZhMDE2ZmFiZTllZWQ5MmE3MmQ3YTk0NSIsImNvbnRleHRJZCI6ImN0eF85M2EwOGYyNmZjYjkiLCJpYXQiOjE3NzkyNjMzMTUsImV4cCI6MTc4NzAzOTMxNSwiaXNzIjoiY29udGV4dC1icm9rZXIiLCJ0b2tlbl9pZCI6IjFjNmM2YjI5LTYxNzItNDQ5Zi05OTYzLTI2NzlkZTMwMzQyNSJ9.o3xFHmuTzXqFd47JiLsXDkxsemmV-OpuNg8eYuDJ0YOUxIJdmuEnqZX-GKtB4ABSsvvnw0HOJfgE_H-GAlR_NQ
```

## 💻 Python Integration

### Create MCP Context Studio Client

Create `langgraph-agent/src/mcp/context_studio_client.py`:

```python
"""
MCP Context Studio Client
Provides access to IBM Context Studio via MCP protocol
"""

import os
import requests
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)


class MCPContextStudioClient:
    """Client for IBM Context Studio via MCP Gateway"""
    
    def __init__(
        self,
        server_url: Optional[str] = None,
        bearer_token: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize MCP Context Studio client.
        
        Args:
            server_url: MCP server URL
            bearer_token: Bearer token for authentication
            api_key: API key for x-api-key header
        """
        self.server_url = server_url or os.getenv(
            "MCP_SERVER_URL",
            "https://servicesessentials.ibm.com/mcp-gateway/service/gateway/servers/8ccdd203bdee4014b08e82eedb6046e2/mcp"
        )
        self.bearer_token = bearer_token or os.getenv("MCP_BEARER_TOKEN")
        self.api_key = api_key or os.getenv("MCP_API_KEY")
        
        if not self.bearer_token or not self.api_key:
            raise ValueError("MCP_BEARER_TOKEN and MCP_API_KEY must be set")
        
        self.headers = {
            "Authorization": f"Bearer {self.bearer_token}",
            "x-api-key": self.api_key,
            "Content-Type": "application/json"
        }
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """
        List available MCP tools.
        
        Returns:
            List of available tools
        """
        try:
            response = requests.post(
                self.server_url,
                headers=self.headers,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "params": {},
                    "id": 1
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("tools", [])
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
    
    def call_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Call an MCP tool.
        
        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments
        
        Returns:
            Tool execution result
        """
        try:
            response = requests.post(
                self.server_url,
                headers=self.headers,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/call",
                    "params": {
                        "name": tool_name,
                        "arguments": arguments
                    },
                    "id": 1
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {})
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}
    
    def search_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Search context studio for relevant information.
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of search results
        """
        return self.call_tool(
            "search_context",
            {"query": query, "limit": limit}
        )
    
    def get_context(self, context_id: str) -> Dict[str, Any]:
        """
        Get specific context by ID.
        
        Args:
            context_id: Context identifier
        
        Returns:
            Context data
        """
        return self.call_tool(
            "get_context",
            {"context_id": context_id}
        )
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """
        List available resources in context studio.
        
        Returns:
            List of resources
        """
        try:
            response = requests.post(
                self.server_url,
                headers=self.headers,
                json={
                    "jsonrpc": "2.0",
                    "method": "resources/list",
                    "params": {},
                    "id": 1
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("resources", [])
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            return []
    
    def read_resource(self, uri: str) -> Dict[str, Any]:
        """
        Read a specific resource.
        
        Args:
            uri: Resource URI
        
        Returns:
            Resource content
        """
        try:
            response = requests.post(
                self.server_url,
                headers=self.headers,
                json={
                    "jsonrpc": "2.0",
                    "method": "resources/read",
                    "params": {"uri": uri},
                    "id": 1
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {})
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            return {"error": str(e)}
```

### Integration Example

Create `langgraph-agent/examples/mcp_integration_example.py`:

```python
"""
Example: Integrating LangGraph Agent with MCP Context Studio
"""

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.mcp.context_studio_client import MCPContextStudioClient
from examples.agent_client import AgentClient


def main():
    print("=" * 80)
    print("  LangGraph Agent + MCP Context Studio Integration")
    print("=" * 80)
    
    # Initialize clients
    print("\n1. Initializing clients...")
    mcp_client = MCPContextStudioClient()
    agent_client = AgentClient()
    
    # List available MCP tools
    print("\n2. Listing available MCP tools...")
    tools = mcp_client.list_tools()
    print(f"   Found {len(tools)} tools:")
    for tool in tools:
        print(f"   - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")
    
    # List available resources
    print("\n3. Listing available resources...")
    resources = mcp_client.list_resources()
    print(f"   Found {len(resources)} resources:")
    for resource in resources[:5]:  # Show first 5
        print(f"   - {resource.get('uri', 'Unknown')}: {resource.get('name', 'No name')}")
    
    # Search context for DevOps information
    print("\n4. Searching context for 'DevOps best practices'...")
    search_results = mcp_client.search_context("DevOps best practices", limit=3)
    print(f"   Found {len(search_results)} results")
    
    # Use context to enhance agent request
    print("\n5. Creating Dockerfile with context enhancement...")
    
    # Get context about Docker best practices
    docker_context = mcp_client.search_context("Docker security best practices", limit=2)
    
    # Build enhanced prompt with context
    context_info = "\n".join([
        f"- {item.get('content', '')[:100]}..."
        for item in docker_context
        if isinstance(item, dict) and 'content' in item
    ])
    
    enhanced_message = f"""Create a production-ready Dockerfile for Python FastAPI application.
    
Consider these enterprise best practices:
{context_info}
"""
    
    # Invoke agent with enhanced context
    result = agent_client.invoke(
        message=enhanced_message,
        context={
            "environment": "production",
            "language": "python",
            "framework": "fastapi",
            "mcp_context": True
        }
    )
    
    print(f"\n   Status: {result.status}")
    print(f"   Confidence: {result.confidence_score:.2%}")
    
    if "dockerfile" in result.artifacts:
        dockerfile = result.artifacts["dockerfile"]
        lines = dockerfile.split('\n')[:15]
        print(f"\n   Dockerfile Preview (first 15 lines):")
        for line in lines:
            print(f"   {line}")
    
    print("\n" + "=" * 80)
    print("  Integration complete!")
    print("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
```

## 🔧 Advanced Integration

### Enhanced Agent with MCP Context

Create `langgraph-agent/examples/context_enhanced_agent.py`:

```python
"""
Context-Enhanced Agent
Combines LangGraph Agent with MCP Context Studio for enhanced responses
"""

from typing import Dict, Any, Optional
from src.mcp.context_studio_client import MCPContextStudioClient
from examples.agent_client import AgentClient, AgentResponse


class ContextEnhancedAgent:
    """Agent that enhances requests with MCP Context Studio data"""
    
    def __init__(self):
        self.mcp_client = MCPContextStudioClient()
        self.agent_client = AgentClient()
    
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

Enterprise Context:
{context_info}

Ensure the Dockerfile follows these enterprise standards."""
        
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
        environment: str = "production"
    ) -> AgentResponse:
        """
        Create Kubernetes manifests enhanced with enterprise context.
        
        Args:
            app_name: Application name
            environment: Target environment
        
        Returns:
            Enhanced agent response
        """
        # Search for K8s best practices
        context_results = self.mcp_client.search_context(
            "Kubernetes security best practices production",
            limit=3
        )
        
        context_info = self._format_context(context_results)
        message = f"""Generate Kubernetes deployment and service manifests for {app_name}.

Enterprise Standards:
{context_info}

Apply these standards to the manifests."""
        
        return self.agent_client.invoke(
            message=message,
            context={
                "app_name": app_name,
                "environment": environment,
                "mcp_enhanced": True
            }
        )
    
    def _format_context(self, context_results: list) -> str:
        """Format context results for inclusion in prompt"""
        if not context_results:
            return "No additional context available"
        
        formatted = []
        for i, item in enumerate(context_results, 1):
            if isinstance(item, dict):
                content = item.get('content', item.get('text', ''))
                if content:
                    formatted.append(f"{i}. {content[:200]}...")
        
        return "\n".join(formatted) if formatted else "No additional context available"


# Example usage
if __name__ == "__main__":
    agent = ContextEnhancedAgent()
    
    print("Creating Dockerfile with enterprise context...")
    result = agent.create_dockerfile_with_context("python", "fastapi")
    print(f"Status: {result.status}")
    print(f"Confidence: {result.confidence_score:.2%}")
```

## 📊 Testing the Integration

Run the integration test:

```bash
cd langgraph-agent/examples
python mcp_integration_example.py
```

## 🔍 Troubleshooting

### Issue: Authentication Failed

**Solution**: Verify your tokens are correct and not expired:
```bash
echo $MCP_BEARER_TOKEN
echo $MCP_API_KEY
```

### Issue: Connection Timeout

**Solution**: Check network connectivity to MCP Gateway:
```bash
curl -H "Authorization: Bearer $MCP_BEARER_TOKEN" \
     -H "x-api-key: $MCP_API_KEY" \
     https://servicesessentials.ibm.com/mcp-gateway/service/gateway/servers/8ccdd203bdee4014b08e82eedb6046e2/mcp
```

### Issue: Tool Not Found

**Solution**: List available tools first:
```python
client = MCPContextStudioClient()
tools = client.list_tools()
print([t['name'] for t in tools])
```

## 📚 Additional Resources

- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [IBM Context Studio Documentation](https://servicesessentials.ibm.com/docs/context-studio)
- [MCP Gateway API Reference](https://servicesessentials.ibm.com/docs/mcp-gateway)

## 📞 Support

- **Slack**: #ica-procode-agents
- **Email**: support@enterprise-advantage.ibm.com

---

**Integration Ready!** Your LangGraph agent can now leverage enterprise context from Context Studio. 🚀