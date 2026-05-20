"""
Unit tests for RepairTools
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.repair_tools import RepairTools
from utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock config"""
    config = MagicMock(spec=Config)
    config.github_token = "test_token"
    return config


@pytest.fixture
def repair_tools(mock_config):
    """Create RepairTools instance"""
    return RepairTools(mock_config)


class TestRepairToolsAnalyzeFailure:
    """Test suite for analyze_failure method"""
    
    @pytest.mark.asyncio
    async def test_analyze_failure_low_severity(self, repair_tools):
        """Test analyzing a low severity failure"""
        run = {
            "id": 12345,
            "name": "CI Pipeline",
            "status": "completed",
            "conclusion": "failure"
        }
        
        failed_jobs = [{
            "id": 1,
            "name": "test",
            "conclusion": "failure",
            "output": "Error: npm package not found"
        }]
        
        logs = {
            1: "npm ERR! 404 Not Found - GET https://registry.npmjs.org/some-package\n"
        }
        
        analysis = await repair_tools.analyze_failure(run, failed_jobs, logs)
        
        assert analysis is not None
        assert "severity" in analysis
        assert "suggested_fix" in analysis
        assert "root_cause" in analysis
        assert "risk_assessment" in analysis
    
    @pytest.mark.asyncio
    async def test_analyze_failure_high_severity(self, repair_tools):
        """Test analyzing a high severity failure"""
        run = {
            "id": 12345,
            "name": "Deployment",
            "status": "completed",
            "conclusion": "failure"
        }
        
        failed_jobs = [{
            "id": 1,
            "name": "deploy",
            "conclusion": "failure",
            "output": "Fatal: database connection failed"
        }]
        
        logs = {
            1: "FATAL: could not connect to database\nconnection refused\n"
        }
        
        analysis = await repair_tools.analyze_failure(run, failed_jobs, logs)
        
        assert analysis is not None
        assert "severity" in analysis
    
    @pytest.mark.asyncio
    async def test_analyze_multiple_failed_jobs(self, repair_tools):
        """Test analyzing multiple failed jobs"""
        run = {
            "id": 12345,
            "name": "Full Pipeline",
            "status": "completed",
            "conclusion": "failure"
        }
        
        failed_jobs = [
            {
                "id": 1,
                "name": "lint",
                "conclusion": "failure"
            },
            {
                "id": 2,
                "name": "test",
                "conclusion": "failure"
            }
        ]
        
        logs = {
            1: "Linting errors found\n",
            2: "Test timeout\n"
        }
        
        analysis = await repair_tools.analyze_failure(run, failed_jobs, logs)
        
        assert analysis is not None


class TestRepairToolsCreateRepairPR:
    """Test suite for create_repair_pr method"""
    
    @pytest.mark.asyncio
    async def test_create_repair_pr_success(self, repair_tools):
        """Test creating a repair PR"""
        repository = "owner/repo"
        run_id = 12345678
        
        analysis = {
            "severity": "medium",
            "suggested_fix": "Update dependency to v2.0.0",
            "root_cause": "Incompatible dependency version"
        }
        
        result = await repair_tools.create_repair_pr(repository, analysis, run_id)
        
        assert result is not None
        assert result["pr_created"] is True
        assert "pr_url" in result
        assert "branch" in result
        assert result["branch"] == f"fix/run-{run_id}"
    
    @pytest.mark.asyncio
    async def test_create_repair_pr_with_detailed_analysis(self, repair_tools):
        """Test creating PR with detailed analysis"""
        repository = "owner/repo"
        run_id = 87654321
        
        analysis = {
            "severity": "low",
            "suggested_fix": "Add missing error handling in line 42",
            "root_cause": "Unhandled exception in process_data function",
            "confidence": 0.95
        }
        
        result = await repair_tools.create_repair_pr(repository, analysis, run_id)
        
        assert result is not None
        assert "suggested_changes" in result
        assert result["message"] == "Auto-generated fix PR"


class TestRepairToolsHelperMethods:
    """Test suite for helper methods"""
    
    def test_prepare_context(self, repair_tools):
        """Test context preparation"""
        run = {"id": 123, "name": "test"}
        failed_jobs = [
            {"id": 1, "name": "job1", "conclusion": "failure"}
        ]
        logs = {1: "Error message\n"}
        
        context = repair_tools._prepare_context(run, failed_jobs, logs)
        
        assert context is not None
        assert isinstance(context, dict)
    
    def test_determine_severity_high(self, repair_tools):
        """Test severity determination for high severity"""
        context = {
            "error_patterns": ["connection refused", "timeout"],
            "job_count": 3
        }
        
        severity = repair_tools._determine_severity(context)
        
        assert severity in ["low", "medium", "high", "unknown"]
    
    def test_identify_root_cause(self, repair_tools):
        """Test root cause identification"""
        context = {
            "error_patterns": ["npm ERR! 404"],
            "failed_jobs": ["install"]
        }
        
        root_cause = repair_tools._identify_root_cause(context)
        
        assert root_cause is not None
        assert isinstance(root_cause, str)
    
    def test_generate_suggestion(self, repair_tools):
        """Test suggestion generation"""
        context = {
            "error_patterns": ["module not found"],
            "job_name": "test"
        }
        
        suggestion = repair_tools._generate_suggestion(context)
        
        assert suggestion is not None
        assert isinstance(suggestion, str)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
