"""
Unit tests for GitHubTools
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from tools.github_tools import GitHubTools
from utils.config import Config


@pytest.fixture
def mock_config():
    """Create a mock config"""
    config = MagicMock(spec=Config)
    config.github_token = "test_token_12345"
    config.github_api_url = "https://api.github.com"
    return config


@pytest.fixture
def github_tools(mock_config):
    """Create GitHubTools instance with mock config"""
    return GitHubTools(mock_config)


class TestGitHubToolsGetWorkflowRun:
    """Test suite for get_workflow_run method"""
    
    @pytest.mark.asyncio
    async def test_get_workflow_run_with_run_id(self, github_tools):
        """Test fetching a specific workflow run by ID"""
        run_id = 12345678
        repository = "owner/repo"
        
        expected_response = {
            "id": run_id,
            "name": "CI Pipeline",
            "conclusion": "failure",
            "status": "completed",
            "created_at": "2026-05-21T10:00:00Z"
        }
        
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=expected_response)
            
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.get = AsyncMock()
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session.get.return_value.__aexit__.return_value = None
            
            mock_session_class.return_value = mock_session
            
            result = await github_tools.get_workflow_run(repository, run_id)
            
            assert result is not None
            assert result["id"] == run_id
            assert result["conclusion"] == "failure"
    
    @pytest.mark.asyncio
    async def test_get_workflow_run_without_run_id(self, github_tools):
        """Test fetching latest failed workflow run"""
        repository = "owner/repo"
        
        expected_response = {
            "workflow_runs": [
                {
                    "id": 111,
                    "conclusion": "success",
                    "status": "completed"
                },
                {
                    "id": 222,
                    "conclusion": "failure",
                    "status": "completed"
                }
            ]
        }
        
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=expected_response)
            
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.get = AsyncMock()
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session.get.return_value.__aexit__.return_value = None
            
            mock_session_class.return_value = mock_session
            
            result = await github_tools.get_workflow_run(repository)
            
            assert result is not None
            assert result["id"] == 222
            assert result["conclusion"] == "failure"
    
    @pytest.mark.asyncio
    async def test_get_workflow_run_api_error(self, github_tools):
        """Test handling of API errors"""
        repository = "owner/repo"
        run_id = 12345678
        
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_response = AsyncMock()
            mock_response.status = 404
            
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.get = AsyncMock()
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session.get.return_value.__aexit__.return_value = None
            
            mock_session_class.return_value = mock_session
            
            result = await github_tools.get_workflow_run(repository, run_id)
            
            assert result is None


class TestGitHubToolsGetFailedJobs:
    """Test suite for get_failed_jobs method"""
    
    @pytest.mark.asyncio
    async def test_get_failed_jobs_success(self, github_tools):
        """Test fetching failed jobs from a workflow run"""
        repository = "owner/repo"
        run_id = 12345678
        
        expected_response = {
            "jobs": [
                {
                    "id": 1,
                    "name": "build",
                    "conclusion": "success",
                    "status": "completed"
                },
                {
                    "id": 2,
                    "name": "test",
                    "conclusion": "failure",
                    "status": "completed"
                },
                {
                    "id": 3,
                    "name": "deploy",
                    "conclusion": "failure",
                    "status": "completed"
                }
            ]
        }
        
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=expected_response)
            
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.get = AsyncMock()
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session.get.return_value.__aexit__.return_value = None
            
            mock_session_class.return_value = mock_session
            
            result = await github_tools.get_failed_jobs(repository, run_id)
            
            assert len(result) == 2
            assert all(job["conclusion"] == "failure" for job in result)
            assert result[0]["name"] == "test"
            assert result[1]["name"] == "deploy"
    
    @pytest.mark.asyncio
    async def test_get_failed_jobs_no_failures(self, github_tools):
        """Test when no jobs have failed"""
        repository = "owner/repo"
        run_id = 12345678
        
        expected_response = {
            "jobs": [
                {
                    "id": 1,
                    "name": "build",
                    "conclusion": "success",
                    "status": "completed"
                },
                {
                    "id": 2,
                    "name": "test",
                    "conclusion": "success",
                    "status": "completed"
                }
            ]
        }
        
        with patch('aiohttp.ClientSession') as mock_session_class:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=expected_response)
            
            mock_session = AsyncMock()
            mock_session.__aenter__.return_value = mock_session
            mock_session.__aexit__.return_value = None
            mock_session.get = AsyncMock()
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_session.get.return_value.__aexit__.return_value = None
            
            mock_session_class.return_value = mock_session
            
            result = await github_tools.get_failed_jobs(repository, run_id)
            
            assert len(result) == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
