from typing import Dict, List, Any
from utils.logger import setup_logger

logger = setup_logger(__name__)

class RepairTools:
    def __init__(self, config):
        self.config = config

    async def analyze_failure(self, run: Dict, failed_jobs: List[Dict], logs: Dict) -> Dict:
        """Analyze failure (simplified without LLM for now)"""
        # Prepare context
        context = self._prepare_context(run, failed_jobs, logs)
        
        # Simple analysis logic
        analysis = {
            "severity": self._determine_severity(context),
            "suggested_fix": self._generate_suggestion(context),
            "root_cause": self._identify_root_cause(context),
            "risk_assessment": "Medium risk - requires review"
        }
        
        return analysis

    async def create_repair_pr(self, repository: str, analysis: Dict, run_id: int) -> Dict:
        """Create a pull request with the suggested fix"""
        suggested_fix = analysis.get("suggested_fix")
        
        # In a real implementation, you would:
        # 1. Create a new branch
        # 2. Apply the suggested changes
        # 3. Commit and push
        # 4. Create PR
        
        return {
            "pr_created": True,
            "pr_url": f"https://github.com/{repository}/pull/123",
            "branch": f"fix/run-{run_id}",
            "message": "Auto-generated fix PR",
            "suggested_changes": suggested_fix
        }

    def _prepare_context(self, run: Dict, failed_jobs: List[Dict], logs: Dict) -> Dict:
        """Prepare context for analysis"""
        error_summary = []
        for job in failed_jobs:
            job_logs = logs.get(job["id"], "")
            lines = job_logs.split('\n')
            errors = [line for line in lines if 'error' in line.lower() or 'failed' in line.lower()]
            error_summary.extend(errors[:5])
        
        return {
            "workflow_name": run.get("name", "unknown"),
            "status": run.get("conclusion", "unknown"),
            "failed_jobs": failed_jobs,
            "error_summary": "\n".join(error_summary[:10])
        }

    def _determine_severity(self, context: Dict) -> str:
        """Determine severity based on errors"""
        error_summary = context.get("error_summary", "").lower()
        if "critical" in error_summary or "security" in error_summary:
            return "high"
        elif "warning" in error_summary or "timeout" in error_summary:
            return "medium"
        else:
            return "low"

    def _generate_suggestion(self, context: Dict) -> str:
        """Generate a simple suggestion"""
        error_summary = context.get("error_summary", "").lower()
        
        if "syntax error" in error_summary:
            return "Fix syntax errors in the code"
        elif "import error" in error_summary:
            return "Check and fix missing dependencies"
        elif "test failed" in error_summary:
            return "Review and fix failing tests"
        else:
            return "Review logs and fix the underlying issue"

    def _identify_root_cause(self, context: Dict) -> str:
        """Identify root cause"""
        error_summary = context.get("error_summary", "")
        if error_summary:
            return error_summary.split('\n')[0][:200]
        return "Unknown - manual investigation required"