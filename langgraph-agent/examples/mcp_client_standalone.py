"""
Standalone MCP Context Studio Client
Does not depend on the main package to avoid import issues
"""

import os
import requests
from typing import Dict, Any, List, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPContextStudioClient:
    """Standalone client for IBM Context Studio via MCP Gateway"""
    
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
        """List available MCP tools"""
        try:
            response = requests.post(
                self.server_url,
                headers=self.headers,
                json={
                    "jsonrpc": "2.0",
                    "method": "tools/list",
                    "params": {},
                    "id": 1
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("tools", [])
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
    
    def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool"""
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
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {})
        except Exception as e:
            logger.error(f"Error calling tool {tool_name}: {e}")
            return {"error": str(e)}
    
    def search_context(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search context studio for relevant information"""
        result = self.call_tool("search_context", {"query": query, "limit": limit})
        
        if isinstance(result, dict):
            if "error" in result:
                return []
            if "results" in result:
                return result["results"]
            if "content" in result:
                return [result]
        
        return []
    
    def list_resources(self) -> List[Dict[str, Any]]:
        """List available resources in context studio"""
        try:
            response = requests.post(
                self.server_url,
                headers=self.headers,
                json={
                    "jsonrpc": "2.0",
                    "method": "resources/list",
                    "params": {},
                    "id": 1
                },
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("result", {}).get("resources", [])
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            return []
    
    def test_connection(self) -> bool:
        """Test connection to MCP server"""
        try:
            tools = self.list_tools()
            return len(tools) >= 0
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

# Made with Bob
