from typing import Dict, List, Any
import re
from utils.logger import setup_logger

logger = setup_logger(__name__)

class GovernanceTools:
    def __init__(self, config):
        self.config = config
        self.risk_thresholds = {
            "auto_fix": config.risk_auto_fix_threshold,
            "human_review": config.risk_human_review_threshold
        }

    async def calculate_risk_score(self, analysis: Dict) -> float:
        """Calculate risk score for a proposed fix"""
        severity = analysis.get("severity", "medium")
        
        # Base risk by severity
        risk_map = {
            "low": 0.2,
            "medium": 0.5,
            "high": 0.8,
            "unknown": 0.6
        }
        
        risk_score = risk_map.get(severity, 0.5)
        
        # Additional risk factors could be added here
        return risk_score

    def determine_action(self, risk_score: float, auto_approve: bool = False) -> str:
        """Determine action based on risk score"""
        if auto_approve:
            return "auto_approve"
        elif risk_score < self.risk_thresholds["auto_fix"]:
            return "auto_fix"
        elif risk_score < self.risk_thresholds["human_review"]:
            return "human_review"
        else:
            return "blocked"

    async def run_pre_release_checks(self, repository: str, version: str) -> Dict:
        """Run pre-release validation checks"""
        checks = {
            "passed": True,
            "checks": []
        }
        
        # Version format check
        if not self._validate_version_format(version):
            checks["passed"] = False
            checks["checks"].append({
                "name": "version_format",
                "passed": False,
                "message": f"Invalid version format: {version}"
            })
        else:
            checks["checks"].append({
                "name": "version_format",
                "passed": True,
                "message": "Version format valid"
            })
        
        return checks

    def _validate_version_format(self, version: str) -> bool:
        """Validate semantic version format"""
        pattern = r'^v?\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version))

    async def assess_change_impact(self, changes: List[Dict]) -> Dict:
        """Assess the impact of proposed changes"""
        impact = {
            "risk_level": "low",
            "affected_services": [],
            "requires_approval": False,
            "estimated_deployment_time": "5 minutes"
        }
        
        for change in changes:
            file_path = change.get("file", "")
            
            # Check for high-risk files
            high_risk_patterns = [
                "database", "migration", "security",
                "auth", "payment", "critical"
            ]
            
            for pattern in high_risk_patterns:
                if pattern in file_path.lower():
                    impact["risk_level"] = "high"
                    impact["requires_approval"] = True
                    impact["affected_services"].append(pattern)
                    break
        
        return impact