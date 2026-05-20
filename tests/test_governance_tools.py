"""
Unit tests for GovernanceTools
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.governance_tools import GovernanceTools
from utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock config"""
    config = MagicMock(spec=Config)
    config.risk_auto_fix_threshold = 0.3
    config.risk_human_review_threshold = 0.7
    return config


@pytest.fixture
def governance_tools(mock_config):
    """Create GovernanceTools instance"""
    return GovernanceTools(mock_config)


class TestGovernanceToolsRiskScore:
    """Test suite for calculate_risk_score method"""
    
    @pytest.mark.asyncio
    async def test_calculate_risk_score_low_severity(self, governance_tools):
        """Test risk score calculation for low severity"""
        analysis = {"severity": "low"}
        
        risk_score = await governance_tools.calculate_risk_score(analysis)
        
        assert risk_score == 0.2
        assert risk_score < 0.3
    
    @pytest.mark.asyncio
    async def test_calculate_risk_score_medium_severity(self, governance_tools):
        """Test risk score calculation for medium severity"""
        analysis = {"severity": "medium"}
        
        risk_score = await governance_tools.calculate_risk_score(analysis)
        
        assert risk_score == 0.5
        assert 0.3 <= risk_score < 0.7
    
    @pytest.mark.asyncio
    async def test_calculate_risk_score_high_severity(self, governance_tools):
        """Test risk score calculation for high severity"""
        analysis = {"severity": "high"}
        
        risk_score = await governance_tools.calculate_risk_score(analysis)
        
        assert risk_score == 0.8
        assert risk_score >= 0.7
    
    @pytest.mark.asyncio
    async def test_calculate_risk_score_unknown_severity(self, governance_tools):
        """Test risk score calculation for unknown severity"""
        analysis = {"severity": "unknown"}
        
        risk_score = await governance_tools.calculate_risk_score(analysis)
        
        assert risk_score == 0.6
    
    @pytest.mark.asyncio
    async def test_calculate_risk_score_missing_severity(self, governance_tools):
        """Test risk score calculation when severity is missing"""
        analysis = {}
        
        risk_score = await governance_tools.calculate_risk_score(analysis)
        
        assert risk_score == 0.5  # Default


class TestGovernanceToolsDetermineAction:
    """Test suite for determine_action method"""
    
    def test_determine_action_auto_approve_override(self, governance_tools):
        """Test that auto_approve overrides risk score"""
        risk_score = 0.9  # High risk
        
        action = governance_tools.determine_action(risk_score, auto_approve=True)
        
        assert action == "auto_approve"
    
    def test_determine_action_auto_fix(self, governance_tools):
        """Test auto_fix action for low risk"""
        risk_score = 0.2  # Low risk (below 0.3 threshold)
        
        action = governance_tools.determine_action(risk_score)
        
        assert action == "auto_fix"
    
    def test_determine_action_human_review(self, governance_tools):
        """Test human_review action for medium risk"""
        risk_score = 0.5  # Medium risk (between 0.3 and 0.7)
        
        action = governance_tools.determine_action(risk_score)
        
        assert action == "human_review"
    
    def test_determine_action_blocked(self, governance_tools):
        """Test blocked action for high risk"""
        risk_score = 0.8  # High risk (above 0.7 threshold)
        
        action = governance_tools.determine_action(risk_score)
        
        assert action == "blocked"
    
    def test_determine_action_boundary_low(self, governance_tools):
        """Test action at low risk boundary"""
        risk_score = 0.3  # At auto_fix threshold
        
        action = governance_tools.determine_action(risk_score)
        
        assert action == "human_review"
    
    def test_determine_action_boundary_high(self, governance_tools):
        """Test action at high risk boundary"""
        risk_score = 0.7  # At human_review threshold
        
        action = governance_tools.determine_action(risk_score)
        
        assert action == "blocked"


class TestGovernanceToolsPreReleaseChecks:
    """Test suite for run_pre_release_checks method"""
    
    @pytest.mark.asyncio
    async def test_pre_release_checks_valid_version(self, governance_tools):
        """Test pre-release checks with valid version"""
        repository = "owner/repo"
        version = "v1.2.3"
        
        result = await governance_tools.run_pre_release_checks(repository, version)
        
        assert result is not None
        assert "passed" in result
        assert "checks" in result
        assert isinstance(result["checks"], list)
    
    @pytest.mark.asyncio
    async def test_pre_release_checks_returns_checks_list(self, governance_tools):
        """Test that pre-release checks returns a list of checks"""
        repository = "owner/repo"
        version = "v2.0.0"
        
        result = await governance_tools.run_pre_release_checks(repository, version)
        
        assert result["passed"] is True
        assert isinstance(result["checks"], list)
    
    @pytest.mark.asyncio
    async def test_pre_release_checks_with_different_versions(self, governance_tools):
        """Test pre-release checks with various version formats"""
        repository = "owner/repo"
        versions = ["v1.0.0", "v2.1.0-beta", "v3.0.0-rc.1"]
        
        for version in versions:
            result = await governance_tools.run_pre_release_checks(repository, version)
            
            assert result is not None
            assert "passed" in result


class TestGovernanceToolsIntegration:
    """Integration tests for governance workflows"""
    
    @pytest.mark.asyncio
    async def test_full_governance_workflow_low_risk(self, governance_tools):
        """Test full governance workflow for low-risk change"""
        analysis = {"severity": "low"}
        
        # Step 1: Calculate risk
        risk_score = await governance_tools.calculate_risk_score(analysis)
        assert risk_score < 0.3
        
        # Step 2: Determine action
        action = governance_tools.determine_action(risk_score)
        assert action == "auto_fix"
    
    @pytest.mark.asyncio
    async def test_full_governance_workflow_high_risk(self, governance_tools):
        """Test full governance workflow for high-risk change"""
        analysis = {"severity": "high"}
        
        # Step 1: Calculate risk
        risk_score = await governance_tools.calculate_risk_score(analysis)
        assert risk_score >= 0.7
        
        # Step 2: Determine action
        action = governance_tools.determine_action(risk_score)
        assert action == "blocked"
    
    @pytest.mark.asyncio
    async def test_full_release_workflow(self, governance_tools):
        """Test full release workflow"""
        repository = "owner/repo"
        version = "v1.0.0"
        
        # Run pre-release checks
        checks = await governance_tools.run_pre_release_checks(repository, version)
        
        assert checks["passed"] is True
        assert len(checks["checks"]) > 0
    
    @pytest.mark.asyncio
    async def test_governance_with_auto_approve_override(self, governance_tools):
        """Test governance allows auto_approve to override risk"""
        analysis = {"severity": "high"}  # Would normally be blocked
        
        # Calculate risk
        risk_score = await governance_tools.calculate_risk_score(analysis)
        assert risk_score > 0.7
        
        # But auto_approve overrides
        action = governance_tools.determine_action(risk_score, auto_approve=True)
        assert action == "auto_approve"


class TestGovernanceToolsCustomThresholds:
    """Test governance with custom risk thresholds"""
    
    def test_custom_thresholds_initialization(self, mock_config):
        """Test governance initialization with custom thresholds"""
        mock_config.risk_auto_fix_threshold = 0.25
        mock_config.risk_human_review_threshold = 0.75
        
        tools = GovernanceTools(mock_config)
        
        assert tools.risk_thresholds["auto_fix"] == 0.25
        assert tools.risk_thresholds["human_review"] == 0.75
    
    def test_determine_action_with_custom_thresholds(self, mock_config):
        """Test action determination with custom thresholds"""
        mock_config.risk_auto_fix_threshold = 0.4
        mock_config.risk_human_review_threshold = 0.8
        
        tools = GovernanceTools(mock_config)
        
        # Score just below custom auto_fix threshold
        action = tools.determine_action(0.35)
        assert action == "auto_fix"
        
        # Score between custom thresholds
        action = tools.determine_action(0.6)
        assert action == "human_review"
        
        # Score above custom human_review threshold
        action = tools.determine_action(0.85)
        assert action == "blocked"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
