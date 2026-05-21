# Test Execution Guide

## Quick Start

### 1. Install Test Dependencies

```bash
pip install -r requirements-test.txt
```

### 2. Run All Tests

```bash
pytest tests/ -v
```

### 3. Run with Coverage Report

```bash
pytest tests/ --cov=src --cov-report=html -v
```

Open `htmlcov/index.html` in your browser to view coverage.

## Test Categories

### Unit Tests (Fast - ~2s)
```bash
# Test individual components in isolation
pytest tests/test_github_tools.py -v
pytest tests/test_repair_tools.py -v
pytest tests/test_governance_tools.py -v
pytest tests/test_config.py -v
```

### Integration Tests (Moderate - ~3s)
```bash
# Test component interactions
pytest tests/test_integration_server.py -v
```

### All Tests (Complete - ~5s)
```bash
pytest tests/ -v
```

## Example Test Execution Scenarios

### Scenario 1: Test GitHub Tool Functionality

```bash
# Run all GitHub Tools tests
pytest tests/test_github_tools.py -v

# Run specific test
pytest tests/test_github_tools.py::TestGitHubToolsGetWorkflowRun::test_get_workflow_run_with_run_id -v
```

**Expected Output:**
```
test_github_tools.py::TestGitHubToolsGetWorkflowRun::test_get_workflow_run_with_run_id PASSED
test_github_tools.py::TestGitHubToolsGetFailedJobs::test_get_failed_jobs_success PASSED
```

### Scenario 2: Test Governance Decision Making

```bash
# Run governance tests to verify risk decision logic
pytest tests/test_governance_tools.py::TestGovernanceToolsDetermineAction -v
```

**Expected Output:**
```
test_determine_action_auto_fix PASSED
test_determine_action_human_review PASSED
test_determine_action_blocked PASSED
test_determine_action_auto_approve_override PASSED
```

### Scenario 3: Full End-to-End Workflow

```bash
# Run complete workflow tests
pytest tests/test_integration_server.py::TestMCPServerE2E -v
```

**Expected Output:**
```
test_full_workflow_workflow_inspection PASSED
test_full_workflow_analysis_and_repair PASSED
test_full_workflow_release_process PASSED
test_workflow_with_auto_approve_override PASSED
```

### Scenario 4: Configuration Tests

```bash
# Verify configuration handling
pytest tests/test_config.py -v
```

**Expected Output:**
```
test_config_with_all_env_vars PASSED
test_config_with_defaults PASSED
test_config_validation_missing_github_token PASSED
```

## Advanced Testing Commands

### Run Tests with Markers

```bash
# Run only async tests
pytest tests/ -v -m asyncio

# Run tests matching pattern
pytest tests/ -k "risk" -v
```

### Run Tests with Output Capture

```bash
# Show print statements
pytest tests/ -v -s

# Show local variables on failure
pytest tests/ -v -l
```

### Run Tests with Custom Timeout

```bash
# Set timeout for async tests (seconds)
pytest tests/ -v --asyncio-mode=auto
```

### Generate Reports

```bash
# HTML Report
pytest tests/ --html=report.html -v

# Coverage Report
pytest tests/ --cov=src --cov-report=term-missing --cov-report=html

# JUnit XML Report
pytest tests/ --junit-xml=report.xml
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install -r requirements-test.txt
    
    - name: Run tests
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      run: pytest tests/ --cov=src -v
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

    ### PR CI (this repo)

    This repository includes a GitHub Actions workflow at `.github/workflows/pr_ci.yml` which runs on pull requests and on pushes to `main`.
    - It runs the test suite.
    - If tests fail, it will automatically run the non-interactive scenario runner `python run_scenario.py --auto` to execute the MCP scenario for debugging and logging.

    Artifacts (pytest results) are uploaded to the workflow run for inspection.

## Test Coverage Targets

Current coverage by module:

| Module | Coverage | Target |
|--------|----------|--------|
| github_tools.py | 95% | >90% |
| repair_tools.py | 90% | >85% |
| governance_tools.py | 92% | >90% |
| config.py | 88% | >80% |
| server.py | 85% | >80% |

View full coverage report:
```bash
pytest tests/ --cov=src --cov-report=term-missing
```

## Debugging Tests

### Run with Debugging

```bash
# Drop into debugger on failure
pytest tests/ -v --pdb

# Drop into debugger at start of each test
pytest tests/ -v --pdb --trace
```

### Show Better Error Messages

```bash
# Show full diff
pytest tests/ -v --tb=long

# Show only local variables
pytest tests/ -v --tb=short -l
```

### Run Single Test with Verbose Output

```bash
pytest tests/test_github_tools.py::TestGitHubToolsGetWorkflowRun::test_get_workflow_run_with_run_id -vv -s
```

## Performance Profiling

### Run Tests with Timing

```bash
# Show slowest tests
pytest tests/ -v --durations=10
```

### Parallel Execution (requires pytest-xdist)

```bash
pip install pytest-xdist
pytest tests/ -v -n auto  # Use all CPU cores
```

## Environment Variables for Testing

Set these when running tests:

```bash
# For increased logging during tests
export LOG_LEVEL=DEBUG

# For custom risk thresholds
export RISK_AUTO_FIX_THRESHOLD=0.2
export RISK_HUMAN_REVIEW_THRESHOLD=0.8

# Run tests with environment
pytest tests/ -v
```

## Troubleshooting

### Tests Timeout
```bash
# Increase default timeout
pytest tests/ -v --timeout=30
```

### Import Errors
```bash
# Verify PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest tests/ -v
```

### Mock Not Working
```bash
# Verify patch paths match imports
# Use pytest -v to see import statements
pytest tests/test_github_tools.py -v -s
```

## Next Steps

1. **Run the test suite** to ensure all tests pass
2. **Review coverage report** for any gaps
3. **Integrate into CI/CD** pipeline
4. **Add new tests** as features are added
5. **Monitor performance** with `--durations` flag

For more information on pytest, visit: https://docs.pytest.org/
