"""
MCP Server Implementation for LangGraph Multi-Agent System

This module implements the Model Context Protocol (MCP) server that exposes
the LangGraph multi-agent system as MCP tools and resources.

The MCP server integrates with IBM Context Forge (MCP Gateway) to provide:
- Tools: DevOps automation, code review, orchestration
- Resources: Agent status, workflow state, execution history
- Prompts: Pre-configured agent interaction patterns
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional, Sequence
from datetime import datetime

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    Resource,
    Prompt,
    PromptMessage,
    GetPromptResult,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import AnyUrl

from ..graph.workflow import create_workflow
from ..graph.state import AgentState
from ..config.settings import get_settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize settings
settings = get_settings()


class LangGraphMCPServer:
    """MCP Server for LangGraph Multi-Agent System"""
    
    def __init__(self):
        self.server = Server("langgraph-devops-agent")
        self.workflow = create_workflow()
        self.execution_history: List[Dict[str, Any]] = []
        
        # Register handlers
        self._register_handlers()
        
        logger.info("LangGraph MCP Server initialized")
    
    def _register_handlers(self):
        """Register MCP protocol handlers"""
        
        # List available tools
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List all available agent tools"""
            return [
                Tool(
                    name="devops_automation",
                    description=(
                        "Automate DevOps tasks including Docker, Kubernetes, CI/CD pipelines, "
                        "and infrastructure provisioning. Generates production-ready configurations "
                        "and deployment manifests."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "The DevOps task to perform (e.g., 'Create Dockerfile for Python FastAPI')"
                            },
                            "environment": {
                                "type": "string",
                                "enum": ["development", "staging", "production"],
                                "default": "production",
                                "description": "Target environment"
                            },
                            "context": {
                                "type": "object",
                                "description": "Additional context (language, framework, cloud provider, etc.)",
                                "properties": {
                                    "language": {"type": "string"},
                                    "framework": {"type": "string"},
                                    "cloud_provider": {"type": "string"},
                                    "app_name": {"type": "string"}
                                }
                            }
                        },
                        "required": ["task"]
                    }
                ),
                Tool(
                    name="code_review",
                    description=(
                        "Perform comprehensive code review including quality analysis, "
                        "security scanning, best practices validation, and improvement suggestions."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "description": "The code to review"
                            },
                            "language": {
                                "type": "string",
                                "description": "Programming language"
                            },
                            "focus_areas": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific areas to focus on (security, performance, maintainability, etc.)"
                            }
                        },
                        "required": ["code"]
                    }
                ),
                Tool(
                    name="service_orchestration",
                    description=(
                        "Orchestrate multi-service workflows, manage microservices coordination, "
                        "and handle complex deployment scenarios."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "services": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of services to orchestrate"
                            },
                            "workflow_type": {
                                "type": "string",
                                "enum": ["deployment", "scaling", "migration", "monitoring"],
                                "description": "Type of orchestration workflow"
                            },
                            "requirements": {
                                "type": "object",
                                "description": "Orchestration requirements and constraints"
                            }
                        },
                        "required": ["services", "workflow_type"]
                    }
                ),
                Tool(
                    name="multi_agent_task",
                    description=(
                        "Execute complex tasks that require coordination between multiple agents. "
                        "The supervisor agent will analyze the task and route to appropriate specialized agents."
                    ),
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "The complex task to execute"
                            },
                            "agents": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Specific agents to involve (optional, auto-detected if not provided)"
                            },
                            "context": {
                                "type": "object",
                                "description": "Additional context for the task"
                            }
                        },
                        "required": ["task"]
                    }
                ),
                Tool(
                    name="get_agent_status",
                    description="Get the current status and capabilities of all agents in the system",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "agent_name": {
                                "type": "string",
                                "description": "Specific agent name (optional, returns all if not provided)"
                            }
                        }
                    }
                )
            ]
        
        # Call tool
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
            """Execute a tool"""
            try:
                logger.info(f"Calling tool: {name} with arguments: {arguments}")
                
                if name == "devops_automation":
                    result = await self._execute_devops_task(arguments)
                elif name == "code_review":
                    result = await self._execute_code_review(arguments)
                elif name == "service_orchestration":
                    result = await self._execute_orchestration(arguments)
                elif name == "multi_agent_task":
                    result = await self._execute_multi_agent_task(arguments)
                elif name == "get_agent_status":
                    result = await self._get_agent_status(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")
                
                # Store in execution history
                self.execution_history.append({
                    "timestamp": datetime.utcnow().isoformat(),
                    "tool": name,
                    "arguments": arguments,
                    "result": result
                })
                
                return [TextContent(type="text", text=json.dumps(result, indent=2))]
                
            except Exception as e:
                logger.error(f"Error executing tool {name}: {str(e)}", exc_info=True)
                return [TextContent(
                    type="text",
                    text=json.dumps({
                        "error": str(e),
                        "tool": name,
                        "arguments": arguments
                    }, indent=2)
                )]
        
        # List resources
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available resources"""
            return [
                Resource(
                    uri=AnyUrl("langgraph://agent/status"),
                    name="Agent Status",
                    mimeType="application/json",
                    description="Current status of all agents in the system"
                ),
                Resource(
                    uri=AnyUrl("langgraph://workflow/state"),
                    name="Workflow State",
                    mimeType="application/json",
                    description="Current state of the LangGraph workflow"
                ),
                Resource(
                    uri=AnyUrl("langgraph://execution/history"),
                    name="Execution History",
                    mimeType="application/json",
                    description="History of recent agent executions"
                ),
                Resource(
                    uri=AnyUrl("langgraph://config/settings"),
                    name="Configuration Settings",
                    mimeType="application/json",
                    description="Current agent configuration and settings"
                )
            ]
        
        # Read resource
        @self.server.read_resource()
        async def read_resource(uri: AnyUrl) -> str:
            """Read a resource"""
            uri_str = str(uri)
            
            if uri_str == "langgraph://agent/status":
                return json.dumps(await self._get_agent_status({}), indent=2)
            
            elif uri_str == "langgraph://workflow/state":
                return json.dumps({
                    "workflow_type": "StateGraph",
                    "nodes": ["supervisor", "devops_agent", "code_review_agent", "orchestrator_agent", "finalize"],
                    "edges": ["conditional_routing", "error_handling"],
                    "status": "active"
                }, indent=2)
            
            elif uri_str == "langgraph://execution/history":
                return json.dumps({
                    "total_executions": len(self.execution_history),
                    "recent_executions": self.execution_history[-10:],  # Last 10
                }, indent=2)
            
            elif uri_str == "langgraph://config/settings":
                return json.dumps({
                    "agent_name": settings.agent_name,
                    "agent_version": settings.agent_version,
                    "default_model": settings.default_model,
                    "max_iterations": settings.max_iterations,
                    "environment": settings.environment
                }, indent=2)
            
            else:
                raise ValueError(f"Unknown resource: {uri_str}")
        
        # List prompts
        @self.server.list_prompts()
        async def list_prompts() -> List[Prompt]:
            """List available prompts"""
            return [
                Prompt(
                    name="devops_dockerfile",
                    description="Generate a production-ready Dockerfile",
                    arguments=[
                        {"name": "language", "description": "Programming language", "required": True},
                        {"name": "framework", "description": "Framework name", "required": False}
                    ]
                ),
                Prompt(
                    name="devops_kubernetes",
                    description="Generate Kubernetes deployment manifests",
                    arguments=[
                        {"name": "app_name", "description": "Application name", "required": True},
                        {"name": "environment", "description": "Target environment", "required": True}
                    ]
                ),
                Prompt(
                    name="devops_cicd",
                    description="Generate CI/CD pipeline configuration",
                    arguments=[
                        {"name": "provider", "description": "CI/CD provider (github, gitlab, jenkins)", "required": True},
                        {"name": "language", "description": "Programming language", "required": True}
                    ]
                )
            ]
        
        # Get prompt
        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: Dict[str, str] | None) -> GetPromptResult:
            """Get a specific prompt"""
            args = arguments or {}
            
            if name == "devops_dockerfile":
                language = args.get("language", "python")
                framework = args.get("framework", "")
                prompt_text = f"Create a production-ready Dockerfile for {language}"
                if framework:
                    prompt_text += f" using {framework} framework"
                
            elif name == "devops_kubernetes":
                app_name = args.get("app_name", "my-app")
                environment = args.get("environment", "production")
                prompt_text = f"Generate Kubernetes deployment and service manifests for {app_name} in {environment} environment"
                
            elif name == "devops_cicd":
                provider = args.get("provider", "github")
                language = args.get("language", "python")
                prompt_text = f"Create a {provider} CI/CD pipeline for {language} with testing, security scanning, and deployment"
                
            else:
                raise ValueError(f"Unknown prompt: {name}")
            
            return GetPromptResult(
                description=f"Prompt for {name}",
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(type="text", text=prompt_text)
                    )
                ]
            )
    
    async def _execute_devops_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute DevOps automation task"""
        task = arguments.get("task", "")
        environment = arguments.get("environment", "production")
        context = arguments.get("context", {})
        
        # Create initial state
        state: AgentState = {
            "request_id": f"mcp-{datetime.utcnow().timestamp()}",
            "user_input": task,
            "task_type": "devops",
            "current_agent": "supervisor",
            "agent_responses": {},
            "final_response": "",
            "error": None,
            "metadata": {
                "environment": environment,
                **context
            },
            "iteration_count": 0,
            "max_iterations": settings.max_iterations,
            "tools_used": [],
            "artifacts_generated": {},
            "confidence_score": 0.0,
            "requires_human_review": False,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Execute workflow
        result = await self.workflow.ainvoke(state)
        
        return {
            "status": "success",
            "task": task,
            "environment": environment,
            "response": result.get("final_response", ""),
            "artifacts": result.get("artifacts_generated", {}),
            "tools_used": result.get("tools_used", []),
            "confidence_score": result.get("confidence_score", 0.0)
        }
    
    async def _execute_code_review(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute code review task"""
        code = arguments.get("code", "")
        language = arguments.get("language", "")
        focus_areas = arguments.get("focus_areas", [])
        
        state: AgentState = {
            "request_id": f"mcp-{datetime.utcnow().timestamp()}",
            "user_input": f"Review this {language} code: {code[:200]}...",
            "task_type": "code_review",
            "current_agent": "supervisor",
            "agent_responses": {},
            "final_response": "",
            "error": None,
            "metadata": {
                "language": language,
                "focus_areas": focus_areas,
                "code_length": len(code)
            },
            "iteration_count": 0,
            "max_iterations": settings.max_iterations,
            "tools_used": [],
            "artifacts_generated": {},
            "confidence_score": 0.0,
            "requires_human_review": False,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = await self.workflow.ainvoke(state)
        
        return {
            "status": "success",
            "language": language,
            "review": result.get("final_response", ""),
            "issues_found": result.get("agent_responses", {}).get("code_review_agent", {}).get("issues", []),
            "confidence_score": result.get("confidence_score", 0.0)
        }
    
    async def _execute_orchestration(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute service orchestration task"""
        services = arguments.get("services", [])
        workflow_type = arguments.get("workflow_type", "deployment")
        requirements = arguments.get("requirements", {})
        
        state: AgentState = {
            "request_id": f"mcp-{datetime.utcnow().timestamp()}",
            "user_input": f"Orchestrate {workflow_type} for services: {', '.join(services)}",
            "task_type": "orchestration",
            "current_agent": "supervisor",
            "agent_responses": {},
            "final_response": "",
            "error": None,
            "metadata": {
                "services": services,
                "workflow_type": workflow_type,
                "requirements": requirements
            },
            "iteration_count": 0,
            "max_iterations": settings.max_iterations,
            "tools_used": [],
            "artifacts_generated": {},
            "confidence_score": 0.0,
            "requires_human_review": False,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = await self.workflow.ainvoke(state)
        
        return {
            "status": "success",
            "services": services,
            "workflow_type": workflow_type,
            "orchestration_plan": result.get("final_response", ""),
            "confidence_score": result.get("confidence_score", 0.0)
        }
    
    async def _execute_multi_agent_task(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multi-agent task"""
        task = arguments.get("task", "")
        agents = arguments.get("agents", [])
        context = arguments.get("context", {})
        
        state: AgentState = {
            "request_id": f"mcp-{datetime.utcnow().timestamp()}",
            "user_input": task,
            "task_type": "multi",
            "current_agent": "supervisor",
            "agent_responses": {},
            "final_response": "",
            "error": None,
            "metadata": {
                "requested_agents": agents,
                **context
            },
            "iteration_count": 0,
            "max_iterations": settings.max_iterations,
            "tools_used": [],
            "artifacts_generated": {},
            "confidence_score": 0.0,
            "requires_human_review": False,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        result = await self.workflow.ainvoke(state)
        
        return {
            "status": "success",
            "task": task,
            "agents_involved": list(result.get("agent_responses", {}).keys()),
            "response": result.get("final_response", ""),
            "confidence_score": result.get("confidence_score", 0.0)
        }
    
    async def _get_agent_status(self, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Get agent status"""
        agent_name = arguments.get("agent_name")
        
        agents_status = {
            "supervisor": {
                "name": "Supervisor Agent",
                "status": "active",
                "capabilities": ["routing", "aggregation", "coordination"],
                "description": "Routes requests to specialized agents and aggregates responses"
            },
            "devops_agent": {
                "name": "DevOps Agent",
                "status": "active",
                "capabilities": ["docker", "kubernetes", "ci_cd", "terraform", "infrastructure"],
                "description": "Handles DevOps automation and infrastructure tasks"
            },
            "code_review_agent": {
                "name": "Code Review Agent",
                "status": "placeholder",
                "capabilities": ["code_analysis", "security_scan", "best_practices"],
                "description": "Performs code review and quality analysis"
            },
            "orchestrator_agent": {
                "name": "Orchestrator Agent",
                "status": "placeholder",
                "capabilities": ["service_coordination", "workflow_management", "deployment"],
                "description": "Manages multi-service orchestration"
            }
        }
        
        if agent_name:
            return agents_status.get(agent_name, {"error": "Agent not found"})
        
        return {
            "total_agents": len(agents_status),
            "active_agents": sum(1 for a in agents_status.values() if a["status"] == "active"),
            "agents": agents_status
        }
    
    async def run(self):
        """Run the MCP server"""
        logger.info("Starting LangGraph MCP Server...")
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point"""
    server = LangGraphMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
