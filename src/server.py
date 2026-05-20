import asyncio
import json
import os
from typing import Any, Dict, List
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from tools.github_tools import GitHubTools
from tools.repair_tools import RepairTools
from tools.governance_tools import GovernanceTools
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class SimpleCICDMCPServer:
    def __init__(self):
        self.config = Config()
        self.github_tools = GitHubTools(self.config)
        self.repair_tools = RepairTools(self.config)
        self.governance_tools = GovernanceTools(self.config)
        self.server = Server("simple-cicd-orchestrator")
        self.setup_handlers()

    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List all available MCP tools"""
            return [
                types.Tool(
                    name="inspect_failure",
                    description="Inspect a failed GitHub Actions workflow run",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repository": {
                                "type": "string",
                                "description": "GitHub repository (format: owner/repo)"
                            },
                            "run_id": {
                                "type": "integer",
                                "description": "Workflow run ID (optional)"
                            }
                        },
                        "required": ["repository"]
                    }
                ),
                types.Tool(
                    name="analyze_and_repair",
                    description="Analyze failure and generate repair PR",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repository": {"type": "string"},
                            "run_id": {"type": "integer"},
                            "auto_approve": {"type": "boolean", "default": False}
                        },
                        "required": ["repository", "run_id"]
                    }
                ),
                types.Tool(
                    name="create_release",
                    description="Create a governed software release",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repository": {"type": "string"},
                            "version": {"type": "string"},
                            "branch": {"type": "string", "default": "main"}
                        },
                        "required": ["repository", "version"]
                    }
                ),
                types.Tool(
                    name="get_pipeline_status",
                    description="Get status of latest pipelines",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repository": {"type": "string"},
                            "workflow_name": {"type": "string"}
                        },
                        "required": ["repository"]
                    }
                )
            ]

        @self.server.call_tool()
        async def handle_call_tool(
            name: str, 
            arguments: Dict[str, Any]
        ) -> List[types.TextContent]:
            """Handle tool calls"""
            try:
                if name == "inspect_failure":
                    result = await self.inspect_failure(arguments)
                elif name == "analyze_and_repair":
                    result = await self.analyze_and_repair(arguments)
                elif name == "create_release":
                    result = await self.create_release(arguments)
                elif name == "get_pipeline_status":
                    result = await self.get_pipeline_status(arguments)
                else:
                    raise ValueError(f"Unknown tool: {name}")

                return [types.TextContent(
                    type="text",
                    text=json.dumps(result, indent=2)
                )]
            except Exception as e:
                logger.error(f"Error handling tool {name}: {str(e)}")
                return [types.TextContent(
                    type="text",
                    text=json.dumps({"error": str(e)}, indent=2)
                )]

    async def inspect_failure(self, args: Dict[str, Any]) -> Dict:
        """Inspect pipeline failure"""
        repository = args["repository"]
        run_id = args.get("run_id")
        
        logger.info(f"Inspecting failure for {repository}, run_id={run_id}")
        
        run = await self.github_tools.get_workflow_run(repository, run_id)
        if not run:
            return {"error": "Workflow run not found"}
        
        failed_jobs = await self.github_tools.get_failed_jobs(repository, run["id"])
        logs = await self.github_tools.get_job_logs(repository, failed_jobs)
        analysis = await self.repair_tools.analyze_failure(run, failed_jobs, logs)
        
        return {
            "run_id": run["id"],
            "status": run["status"],
            "conclusion": run["conclusion"],
            "failed_jobs": failed_jobs,
            "analysis": analysis,
            "severity": analysis.get("severity", "unknown"),
            "suggested_fix": analysis.get("suggested_fix")
        }

    async def analyze_and_repair(self, args: Dict[str, Any]) -> Dict:
        """Analyze failure and create repair PR"""
        repository = args["repository"]
        run_id = args["run_id"]
        auto_approve = args.get("auto_approve", False)
        
        logger.info(f"Analyzing and repairing {repository}, run_id={run_id}")
        
        inspection = await self.inspect_failure({
            "repository": repository,
            "run_id": run_id
        })
        
        if "error" in inspection:
            return inspection
        
        risk_score = await self.governance_tools.calculate_risk_score(
            inspection["analysis"]
        )
        
        action = self.governance_tools.determine_action(risk_score, auto_approve)
        
        result = {
            "run_id": run_id,
            "risk_score": risk_score,
            "action": action,
            "analysis": inspection["analysis"]
        }
        
        if action in ["auto_fix", "auto_approve"]:
            pr_result = await self.repair_tools.create_repair_pr(
                repository,
                inspection["analysis"],
                run_id
            )
            result["pull_request"] = pr_result
            result["status"] = "repair_pr_created"
        elif action == "human_review":
            result["status"] = "requires_human_review"
            result["message"] = "Risk score too high for auto-fix. Manual review required."
        else:
            result["status"] = "blocked"
            result["message"] = "Risk score exceeds threshold. Action blocked."
        
        return result

    async def create_release(self, args: Dict[str, Any]) -> Dict:
        """Create a governed release"""
        repository = args["repository"]
        version = args["version"]
        branch = args.get("branch", "main")
        
        logger.info(f"Creating release {version} for {repository} from {branch}")
        
        ci_status = await self.github_tools.get_workflow_status(
            repository, 
            "ci"
        )
        
        if not ci_status.get("success", False):
            return {
                "error": "CI pipeline not passing",
                "status": "ci_failed",
                "details": ci_status
            }
        
        checks = await self.governance_tools.run_pre_release_checks(
            repository, version
        )
        
        if not checks["passed"]:
            return {
                "error": "Pre-release checks failed",
                "checks": checks,
                "status": "checks_failed"
            }
        
        release = await self.github_tools.create_release(
            repository, version, branch
        )
        
        return {
            "status": "release_created",
            "release": release,
            "version": version,
            "branch": branch,
            "checks": checks
        }

    async def get_pipeline_status(self, args: Dict[str, Any]) -> Dict:
        """Get pipeline status"""
        repository = args["repository"]
        workflow_name = args.get("workflow_name")
        
        workflows = await self.github_tools.get_workflow_runs(
            repository, workflow_name
        )
        
        return {
            "repository": repository,
            "latest_runs": workflows[:5],
            "summary": {
                "total": len(workflows),
                "success": sum(1 for w in workflows if w["conclusion"] == "success"),
                "failed": sum(1 for w in workflows if w["conclusion"] == "failure")
            }
        }

    async def run(self):
        """Run the MCP server"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="simple-cicd-orchestrator",
                    server_version="0.1.0"
                )
            )

async def main():
    server = SimpleCICDMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())