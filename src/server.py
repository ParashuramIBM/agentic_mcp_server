import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

# Add parent directory to path for VS Code
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.github_tools import GitHubTools
from tools.repair_tools import RepairTools
from tools.governance_tools import GovernanceTools
from utils.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)

class VSCodeMCPServer:
    """MCP Server optimized for VS Code"""
    
    def __init__(self):
        self.config = Config()
        self.github_tools = GitHubTools(self.config)
        self.repair_tools = RepairTools(self.config)
        self.governance_tools = GovernanceTools(self.config)
        self.server = Server("simple-cicd-orchestrator")
        self.setup_handlers()
        
        # Log startup for VS Code
        logger.info("VS Code MCP Server initialized")
        logger.info(f"GitHub Token configured: {'Yes' if self.config.github_token else 'No'}")
        logger.info(f"Risk thresholds: auto={self.config.risk_auto_fix_threshold}, review={self.config.risk_human_review_threshold}")

    def setup_handlers(self):
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """List all available MCP tools"""
            logger.debug("Listing tools")
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
                                "description": "Workflow run ID (optional - gets latest if not provided)"
                            }
                        },
                        "required": ["repository"]
                    }
                ),
                types.Tool(
                    name="analyze_and_repair",
                    description="Analyze failure and generate auto-repair pull request",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "repository": {
                                "type": "string",
                                "description": "GitHub repository (format: owner/repo)"
                            },
                            "run_id": {
                                "type": "integer",
                                "description": "Workflow run ID to analyze"
                            },
                            "auto_approve": {
                                "type": "boolean",
                                "description": "Auto-approve low-risk changes",
                                "default": False
                            }
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
                            "repository": {
                                "type": "string",
                                "description": "GitHub repository (format: owner/repo)"
                            },
                            "version": {
                                "type": "string",
                                "description": "Release version (e.g., v1.0.0)"
                            },
                            "branch": {
                                "type": "string",
                                "description": "Branch to release from",
                                "default": "main"
                            }
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
                            "repository": {
                                "type": "string",
                                "description": "GitHub repository (format: owner/repo)"
                            },
                            "workflow_name": {
                                "type": "string",
                                "description": "Optional workflow name filter"
                            }
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
            """Handle tool calls with VS Code specific logging"""
            logger.info(f"Tool called: {name} with arguments: {json.dumps(arguments, default=str)}")
            
            try:
                # Validate arguments
                if not arguments:
                    arguments = {}
                
                # Route to appropriate handler
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

                # Format result
                response_text = json.dumps(result, indent=2, default=str)
                logger.debug(f"Tool {name} returned successfully")
                
                return [types.TextContent(
                    type="text",
                    text=response_text
                )]
                
            except Exception as e:
                logger.error(f"Error in tool {name}: {str(e)}", exc_info=True)
                return [types.TextContent(
                    type="text",
                    text=json.dumps({
                        "error": str(e),
                        "tool": name,
                        "arguments": arguments
                    }, indent=2)
                )]

    async def inspect_failure(self, args: Dict[str, Any]) -> Dict:
        """Inspect pipeline failure"""
        repository = args.get("repository")
        if not repository:
            return {"error": "Repository parameter is required"}
            
        run_id = args.get("run_id")
        
        logger.info(f"Inspecting failure for {repository}, run_id={run_id}")
        
        try:
            # Get workflow run
            run = await self.github_tools.get_workflow_run(repository, run_id)
            if not run:
                return {
                    "error": "Workflow run not found",
                    "repository": repository,
                    "run_id": run_id
                }
            
            # Get failed jobs
            failed_jobs = await self.github_tools.get_failed_jobs(repository, run["id"])
            
            # Get logs for failed jobs
            logs = await self.github_tools.get_job_logs(repository, failed_jobs)
            
            # Analyze failure
            analysis = await self.repair_tools.analyze_failure(run, failed_jobs, logs)
            
            return {
                "run_id": run["id"],
                "repository": repository,
                "status": run["status"],
                "conclusion": run["conclusion"],
                "failed_jobs_count": len(failed_jobs),
                "failed_jobs": [
                    {
                        "name": job["name"],
                        "status": job["status"],
                        "conclusion": job["conclusion"]
                    }
                    for job in failed_jobs
                ],
                "analysis": analysis,
                "severity": analysis.get("severity", "unknown"),
                "suggested_fix": analysis.get("suggested_fix")
            }
            
        except Exception as e:
            logger.error(f"Failed to inspect failure: {str(e)}")
            return {"error": f"Failed to inspect failure: {str(e)}"}

    async def analyze_and_repair(self, args: Dict[str, Any]) -> Dict:
        """Analyze failure and create repair PR"""
        repository = args.get("repository")
        run_id = args.get("run_id")
        auto_approve = args.get("auto_approve", False)
        
        if not repository:
            return {"error": "Repository parameter is required"}
        if not run_id:
            return {"error": "Run ID parameter is required"}
        
        logger.info(f"Analyzing and repairing {repository}, run_id={run_id}, auto_approve={auto_approve}")
        
        try:
            # First inspect the failure
            inspection = await self.inspect_failure({
                "repository": repository,
                "run_id": run_id
            })
            
            if "error" in inspection:
                return inspection
            
            # Calculate risk score
            risk_score = await self.governance_tools.calculate_risk_score(
                inspection["analysis"]
            )
            
            # Determine action based on risk
            action = self.governance_tools.determine_action(risk_score, auto_approve)
            
            result = {
                "run_id": run_id,
                "repository": repository,
                "risk_score": risk_score,
                "action": action,
                "analysis": inspection["analysis"]
            }
            
            # Take action based on risk level
            if action in ["auto_fix", "auto_approve"]:
                logger.info(f"Auto-fixing with risk score {risk_score}")
                pr_result = await self.repair_tools.create_repair_pr(
                    repository,
                    inspection["analysis"],
                    run_id
                )
                result["pull_request"] = pr_result
                result["status"] = "repair_pr_created"
                result["message"] = "Auto-generated fix PR created"
                
            elif action == "human_review":
                logger.info(f"Requiring human review (risk score: {risk_score})")
                result["status"] = "requires_human_review"
                result["message"] = "Risk score too high for auto-fix. Manual review required."
                
            else:
                logger.warning(f"Action blocked (risk score: {risk_score})")
                result["status"] = "blocked"
                result["message"] = "Risk score exceeds threshold. Action blocked."
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to analyze and repair: {str(e)}")
            return {"error": f"Failed to analyze and repair: {str(e)}"}

    async def create_release(self, args: Dict[str, Any]) -> Dict:
        """Create a governed release"""
        repository = args.get("repository")
        version = args.get("version")
        branch = args.get("branch", "main")
        
        if not repository:
            return {"error": "Repository parameter is required"}
        if not version:
            return {"error": "Version parameter is required"}
        
        logger.info(f"Creating release {version} for {repository} from {branch}")
        
        try:
            # Verify CI status
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
            
            # Run pre-release checks
            checks = await self.governance_tools.run_pre_release_checks(
                repository, version
            )
            
            if not checks["passed"]:
                return {
                    "error": "Pre-release checks failed",
                    "checks": checks,
                    "status": "checks_failed"
                }
            
            # Create release
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
            
        except Exception as e:
            logger.error(f"Failed to create release: {str(e)}")
            return {"error": f"Failed to create release: {str(e)}"}

    async def get_pipeline_status(self, args: Dict[str, Any]) -> Dict:
        """Get pipeline status"""
        repository = args.get("repository")
        if not repository:
            return {"error": "Repository parameter is required"}
            
        workflow_name = args.get("workflow_name")
        
        try:
            workflows = await self.github_tools.get_workflow_runs(
                repository, workflow_name
            )
            
            return {
                "repository": repository,
                "workflow_filter": workflow_name or "all",
                "latest_runs": workflows[:5],
                "summary": {
                    "total": len(workflows),
                    "success": sum(1 for w in workflows if w["conclusion"] == "success"),
                    "failed": sum(1 for w in workflows if w["conclusion"] == "failure"),
                    "in_progress": sum(1 for w in workflows if w["status"] == "in_progress")
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get pipeline status: {str(e)}")
            return {"error": f"Failed to get pipeline status: {str(e)}"}

    async def run(self):
        """Run the MCP server for VS Code"""
        logger.info("Starting VS Code MCP Server...")
        
        try:
            async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
                logger.info("MCP server running on stdio")
                await self.server.run(
                    read_stream,
                    write_stream,
                    InitializationOptions(
                        server_name="simple-cicd-orchestrator",
                        server_version="0.1.0",
                        capabilities={}
                    )
                )
        except Exception as e:
            logger.error(f"Server error: {str(e)}", exc_info=True)
            raise

async def main():
    server = VSCodeMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())