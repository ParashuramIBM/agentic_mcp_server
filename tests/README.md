# Test Suite for MCP CI/CD Server

## Overview

This directory contains comprehensive test suites for the Model Context Protocol (MCP) CI/CD orchestration server. The tests cover unit tests, integration tests, and end-to-end workflows.

## Test Structure

### Unit Tests

#### `test_github_tools.py`
Tests for GitHub API interactions:
- **TestGitHubToolsGetWorkflowRun**: Tests workflow run retrieval
  - Success cases with specific run IDs
  - Fetching latest failed runs
  - API error handling
  
- **TestGitHubToolsGetFailedJobs**: Tests failed job extraction
  - Retrieving failed jobs from workflow runs
  - Handling runs with no failures
  - Job filtering logic

#### `test_repair_tools.py`
Tests for repair and analysis functionality:
- **TestRepairToolsAnalyzeFailure**: Tests failure analysis
  - Low, medium, and high severity failures
  - Multiple failed jobs analysis
  
- **TestRepairToolsCreateRepairPR**: Tests PR creation
  - PR generation from analysis
  - Branch naming conventions
  
- **TestRepairToolsHelperMethods**: Tests internal methods
  - Context preparation
  - Severity determination
  - Root cause identification

#### `test_governance_tools.py`
Tests for governance and risk management:
- **TestGovernanceToolsRiskScore**: Tests risk calculation
  - Risk scores for different severity levels
  - Boundary conditions
  
- **TestGovernanceToolsDetermineAction**: Tests action determination
  - Auto-approve responses
  - Auto-fix decisions
  - Human review requirements
  - Blocked high-risk changes
  
- **TestGovernanceToolsPreReleaseChecks**: Tests release validation
- **TestGovernanceToolsIntegration**: Full workflow tests
- **TestGovernanceToolsCustomThresholds**: Tests with custom configurations

#### `test_config.py`
Tests for configuration management:
- **TestConfigInitialization**: Tests config loading
  - Environment variable handling
  - Default values
  - Validation
  
- **TestConfigValidation**: Tests validation logic
- **TestConfigIntegration**: Full config integration tests

### Integration Tests

#### `test_integration_server.py`
End-to-end server integration tests:
- **TestMCPServerInitialization**: Tests server setup
- **TestMCPServerTools**: Tests tool registration and schemas
- **TestMCPServerE2E**: Complete workflow tests
  - Workflow inspection flow
  - Analysis and repair workflow
  - Release process
  - Auto-approve overrides
  
- **TestMCPServerErrorHandling**: Tests error scenarios
- **TestMCPServerConfiguration**: Tests configuration handling
- **TestMCPServerScalability**: Tests concurrent operations

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install pytest pytest-asyncio pytest-cov
```

### Run All Tests

```bash
pytest tests/ -v
```

### Run Specific Test File

```bash
pytest tests/test_github_tools.py -v
```

### Run Specific Test Class

```bash
pytest tests/test_governance_tools.py::TestGovernanceToolsRiskScore -v
```

### Run Specific Test

```bash
pytest tests/test_governance_tools.py::TestGovernanceToolsRiskScore::test_calculate_risk_score_low_severity -v
```

### Run with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

This generates a coverage report in `htmlcov/index.html`.

## Test Scenarios

### Scenario 1: Low-Risk Failure Repair
```
Test: test_full_workflow_analysis_and_repair
- Workflow fails during tests
- Analysis indicates low severity (dependency issue)
- Risk score < 0.3 (auto_fix threshold)
- Action: Automatically approve and merge fix
```

### Scenario 2: High-Risk Deployment Failure
```
Test: test_workflow_with_auto_approve_override
- Production deployment fails
- Analysis indicates high severity (database issue)
- Risk score > 0.7 (blocked threshold)
- Requires manual review before proceeding
- Can be overridden with auto_approve flag
```

### Scenario 3: Release Governance
```
Test: test_full_workflow_release_process
- Pre-release checks validate version format
- Dependency checks pass
- Release is blessed for production
```

### Scenario 4: Multiple Concurrent Failures
```
Test: test_handle_multiple_workflow_inspections
- Multiple repositories have failing workflows
- Server handles concurrent inspection requests
- Each gets appropriate governance response
```

## Mocking Strategy

Tests use Python's `unittest.mock` library:
- **AsyncMock**: For async functions (GitHub API calls)
- **MagicMock**: For configuration and dependencies
- **patch.dict**: For environment variables

Example:
```python
with patch('aiohttp.ClientSession') as mock_session_class:
    mock_response = AsyncMock()
    mock_response.status = 200
    mock_response.json = AsyncMock(return_value=expected_data)
    # ... test logic
```

## Test Data

Tests use realistic but synthetic data:
- Valid GitHub repository format: `owner/repo`
- Valid workflow run IDs: numeric (e.g., 12345678)
- Valid version formats: `v1.0.0`, `v2.1.0-beta`
- Error messages and logs: representative of real failures

## Common Test Patterns

### Async Test Pattern
```python
@pytest.mark.asyncio
async def test_async_function(self):
    result = await some_async_function()
    assert result is not None
```

### Mock API Pattern
```python
with patch('aiohttp.ClientSession') as mock_session:
    mock_response = AsyncMock()
    mock_response.status = 200
    # Configure mock...
    result = await function_that_uses_api()
```

### Environment Variable Pattern
```python
@patch.dict(os.environ, {'VAR': 'value'})
def test_with_env_var(self):
    config = Config()
    assert config.value == 'expected'
```

## CI/CD Integration

These tests can be integrated into your CI/CD pipeline:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: pytest tests/ --cov=src -v
  
- name: Upload Coverage
  uses: codecov/codecov-action@v3
```

## Extending Tests

To add new tests:

1. **Create new test file**: `tests/test_new_feature.py`
2. **Follow naming convention**: `test_<module>.py`
3. **Use fixtures**: Leverage existing fixtures for setup
4. **Mock external calls**: Use patches for external dependencies
5. **Document scenarios**: Add docstrings explaining test purpose

Example template:
```python
@pytest.fixture
def setup_resource():
    """Setup test resource"""
    resource = SomeClass()
    yield resource
    # Cleanup if needed

def test_feature(setup_resource):
    """Test description"""
    result = setup_resource.method()
    assert result == expected
```

## Troubleshooting

### Test Fails with Import Error
- Ensure `PYTHONPATH` includes `src/`
- Check `__init__.py` files exist in package directories

### Async Tests Timeout
- Increase timeout: `@pytest.mark.asyncio(scope="function")`
- Check for hanging mock await calls

### Mock Not Being Applied
- Ensure patch path matches import path
- Use `spec=` to catch attribute errors

## Performance Considerations

- Tests run asynchronously where possible
- Mocking prevents network calls (fast)
- Total test suite runs in <10 seconds
- Can be parallelized with `pytest-xdist`:
  ```bash
  pytest tests/ -n auto
  ```

## References

- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [MCP Protocol](https://modelcontextprotocol.io/)
