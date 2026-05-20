import aiohttp
from typing import Dict, List, Optional, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)

class GitHubTools:
    def __init__(self, config):
        self.config = config
        self.token = config.github_token
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def get_workflow_run(self, repository: str, run_id: Optional[int] = None) -> Optional[Dict]:
        """Get workflow run details"""
        if run_id:
            url = f"{self.api_base}/repos/{repository}/actions/runs/{run_id}"
        else:
            url = f"{self.api_base}/repos/{repository}/actions/runs"
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if run_id:
                        return data
                    # Return latest failed run
                    for run in data.get("workflow_runs", []):
                        if run["conclusion"] == "failure":
                            return run
                    return None
                else:
                    logger.error(f"GitHub API error: {resp.status}")
                    return None

    async def get_failed_jobs(self, repository: str, run_id: int) -> List[Dict]:
        """Get failed jobs from a workflow run"""
        url = f"{self.api_base}/repos/{repository}/actions/runs/{run_id}/jobs"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    jobs = data.get("jobs", [])
                    return [j for j in jobs if j["conclusion"] == "failure"]
                return []

    async def get_job_logs(self, repository: str, failed_jobs: List[Dict]) -> Dict[int, str]:
        """Get logs for failed jobs"""
        logs = {}
        
        async with aiohttp.ClientSession() as session:
            for job in failed_jobs:
                job_id = job["id"]
                url = f"{self.api_base}/repos/{repository}/actions/jobs/{job_id}/logs"
                
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        logs[job_id] = await resp.text()
                    else:
                        logs[job_id] = f"Failed to fetch logs: {resp.status}"
                        
        return logs

    async def get_workflow_status(self, repository: str, workflow_name: str) -> Dict:
        """Get status of a specific workflow"""
        url = f"{self.api_base}/repos/{repository}/actions/workflows/{workflow_name}/runs"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    latest = data.get("workflow_runs", [{}])[0]
                    return {
                        "success": latest.get("conclusion") == "success",
                        "status": latest.get("status"),
                        "conclusion": latest.get("conclusion"),
                        "run_id": latest.get("id")
                    }
                return {"success": False, "error": f"HTTP {resp.status}"}

    async def get_workflow_runs(self, repository: str, workflow_name: Optional[str] = None) -> List[Dict]:
        """Get recent workflow runs"""
        if workflow_name:
            url = f"{self.api_base}/repos/{repository}/actions/workflows/{workflow_name}/runs"
        else:
            url = f"{self.api_base}/repos/{repository}/actions/runs"
            
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    runs = data.get("workflow_runs", [])
                    return [{
                        "id": r["id"],
                        "name": r["name"],
                        "status": r["status"],
                        "conclusion": r["conclusion"],
                        "created_at": r["created_at"],
                        "html_url": r["html_url"]
                    } for r in runs[:10]]
                return []

    async def create_release(self, repository: str, version: str, branch: str) -> Dict:
        """Create a GitHub release"""
        url = f"{self.api_base}/repos/{repository}/releases"
        payload = {
            "tag_name": version,
            "target_commitish": branch,
            "name": f"Release {version}",
            "body": f"## Release {version}\n\nAutomated release created by MCP orchestrator.",
            "draft": False,
            "prerelease": False
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=self.headers, json=payload) as resp:
                if resp.status in [200, 201]:
                    return await resp.json()
                else:
                    return {"error": f"Failed to create release: {resp.status}"}