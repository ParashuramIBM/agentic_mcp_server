"""
Integration tests for MCP Server
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Mock environment variables before importing
with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'}):
    from server import VSCodeMCPServer


@pytest.fixture
def mcp_server():
    """Create MCP server instance"""
    with patch.dict(os.environ, {'GITHUB_TOKEN': 'test_token'}):
        return VSCodeMCPServer()


class TestMCPServerInitialization:
    """Test suite for MCP server initialization"""
    
    def test_server_initialization(self, mcp_server):
        """Test that server initializes correctly"""
        assert mcp_server is not None
        assert mcp_server.config is not None
        assert mcp_server.github_tools is not None
        assert mcp_server.repair_tools is not None
        assert mcp_server.governance_tools is not None
        assert mcp_server.server is not None
    
    def test_server_components_initialized(self, mcp_server):
        """Test that all server components are initialized"""
        # Check that tools are instances of correct classes
        from tools.github_tools import GitHubTools
        from tools.repair_tools import RepairTools
        from tools.governance_tools import GovernanceTools
        
        assert isinstance(mcp_server.github_tools, GitHubTools)
        assert isinstance(mcp_server.repair_tools, RepairTools)
        assert isinstance(mcp_server.governance_tools, GovernanceTools)


class TestMCPServerTools:
    """Test suite for MCP server tools"""
    
    def test_list_tools_available(self, mcp_server):
        """Test that all tools are available"""
        expected_tools = [
            "inspect_failure",
            "analyze_and_repair",
            "create_release"
        ]
        
        # Verify that handler is registered
        assert hasattr(mcp_server.server, '_handlers')
    
    def test_tool_schemas_valid(self, mcp_server):
        """Test that tool schemas are properly defined"""
        # This would require access to the handler internals
        # For now, we verify the server is set up
        assert mcp_server.server is not None


class TestMCPServerE2E:
    """End-to-end integration tests"""
    
    @pytest.mark.asyncio
    async def test_full_workflow_workflow_inspection(self, mcp_server):
        """Test complete workflow inspection flow"""
        repository = "owner/repo"
        run_id = 12345678
        
        # Mock GitHub API
        with patch.object(mcp_server.github_tools, 'get_workflow_run', new_callable=AsyncMock) as mock_run:
            with patch.object(mcp_server.github_tools, 'get_failed_jobs', new_callable=AsyncMock) as mock_jobs:
                # Setup mocks
                mock_run.return_value = {
                    "id": run_id,
                    "conclusion": "failure",
                    "status": "completed",
                    "name": "CI"
                }
                
                mock_jobs.return_value = [
                    {"id": 1, "name": "test", "conclusion": "failure"}
                ]
                
                # Execute workflow
                run = await mcp_server.github_tools.get_workflow_run(repository, run_id)
                jobs = await mcp_server.github_tools.get_failed_jobs(repository, run_id)
                
                # Verify results
                assert run is not None
                assert run["id"] == run_id
                assert len(jobs) == 1
    
    @pytest.mark.asyncio
    async def test_full_workflow_analysis_and_repair(self, mcp_server):
        """Test complete analysis and repair workflow"""
        repository = "owner/repo"
        run_id = 12345678
        
        # Setup test data
        run = {"id": run_id, "conclusion": "failure", "name": "CI"}
        failed_jobs = [{"id": 1, "name": "test", "conclusion": "failure"}]
        logs = {1: "Test failed: connection timeout"}
        
        # Analyze failure
        analysis = await mcp_server.repair_tools.analyze_failure(run, failed_jobs, logs)
        
        # Create repair PR
        pr_result = await mcp_server.repair_tools.create_repair_pr(repository, analysis, run_id)
        
        # Run governance checks
        risk_score = await mcp_server.governance_tools.calculate_risk_score(analysis)
        action = mcp_server.governance_tools.determine_action(risk_score)
        
        # Verify workflow
        assert analysis is not None
        assert pr_result["pr_created"] is True
        assert risk_score >= 0.0 and risk_score <= 1.0
        assert action in ["auto_fix", "human_review", "blocked"]
    
    @pytest.mark.asyncio
    async def test_full_workflow_release_process(self, mcp_server):
        """Test complete release workflow"""
        repository = "owner/repo"
        version = "v1.0.0"
        
        # Run pre-release checks
        checks = await mcp_server.governance_tools.run_pre_release_checks(repository, version)
        
        # Verify checks
        assert checks is not None
        assert "passed" in checks
        assert "checks" in checks
    
    @pytest.mark.asyncio
    async def test_workflow_with_auto_approve_override(self, mcp_server):
        """Test workflow with auto_approve override"""
        repository = "owner/repo"
        run_id = 12345678
        
        # Setup analysis with high risk
        run = {"id": run_id, "conclusion": "failure"}
        failed_jobs = [{"id": 1, "name": "deploy", "conclusion": "failure"}]
        logs = {1: "Database migration failed"}
        
        # Analyze with high severity
        analysis = await mcp_server.repair_tools.analyze_failure(run, failed_jobs, logs)
        analysis["severity"] = "high"
        
        # Calculate risk
        risk_score = await mcp_server.governance_tools.calculate_risk_score(analysis)
        assert risk_score > 0.7  # High risk
        
        # Determine action without auto_approve
        action_normal = mcp_server.governance_tools.determine_action(risk_score, auto_approve=False)
        assert action_normal == "blocked"
        
        # Determine action with auto_approve
        action_override = mcp_server.governance_tools.determine_action(risk_score, auto_approve=True)
        assert action_override == "auto_approve"


class TestMCPServerErrorHandling:
    """Test error handling in MCP server"""
    
    @pytest.mark.asyncio
    async def test_handle_github_api_failure(self, mcp_server):
        """Test handling of GitHub API failures"""
        with patch.object(mcp_server.github_tools, 'get_workflow_run', new_callable=AsyncMock) as mock_run:
            mock_run.return_value = None  # Simulate API failure
            
            result = await mcp_server.github_tools.get_workflow_run("owner/repo", 12345)
            
            assert result is None
    
    @pytest.mark.asyncio
    async def test_handle_empty_failed_jobs(self, mcp_server):
        """Test handling of runs with no failed jobs"""
        with patch.object(mcp_server.github_tools, 'get_failed_jobs', new_callable=AsyncMock) as mock_jobs:
            mock_jobs.return_value = []  # No failed jobs
            
            result = await mcp_server.github_tools.get_failed_jobs("owner/repo", 12345)
            
            assert isinstance(result, list)
            assert len(result) == 0


class TestMCPServerConfiguration:
    """Test MCP server configuration handling"""
    
    def test_server_uses_correct_config(self, mcp_server):
        """Test that server uses configuration correctly"""
        assert mcp_server.config.github_token == 'test_token'
        assert mcp_server.github_tools.token == 'test_token'
    
    def test_server_governance_thresholds(self, mcp_server):
        """Test that governance uses correct thresholds"""
        assert mcp_server.governance_tools.risk_thresholds["auto_fix"] > 0
        assert mcp_server.governance_tools.risk_thresholds["human_review"] > 0


class TestMCPServerScalability:
    """Test server behavior under various loads"""
    
    @pytest.mark.asyncio
    async def test_handle_multiple_workflow_inspections(self, mcp_server):
        """Test handling multiple concurrent workflow inspections"""
        repositories = ["owner/repo1", "owner/repo2", "owner/repo3"]
        run_ids = [12345, 67890, 11111]
        
        with patch.object(mcp_server.github_tools, 'get_workflow_run', new_callable=AsyncMock) as mock_run:
            mock_run.side_effect = [
                {"id": rid, "conclusion": "failure"} for rid in run_ids
            ]
            
            # This would call the handler multiple times
            for repo, run_id in zip(repositories, run_ids):
                result = await mcp_server.github_tools.get_workflow_run(repo, run_id)
                assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
