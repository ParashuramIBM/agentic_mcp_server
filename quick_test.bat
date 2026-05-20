@echo off
echo ========================================
echo MCP CI/CD Quick Test
echo ========================================

REM Step 1: Setup test repository
echo.
echo [1/4] Setting up test repository...
call test_scenario\setup_test_repo.bat

REM Step 2: Install dependencies
echo.
echo [2/4] Installing dependencies...
pip install -r requirements.txt

REM Step 3: Set environment
echo.
echo [3/4] Setting up environment...
if not exist .env (
    copy .env.example .env
    echo Please edit .env and add your GITHUB_TOKEN
    pause
)

REM Step 4: Run the test scenario
echo.
echo [4/4] Running CI/CD test scenario...
python run_scenario.py

echo.
echo Test completed!
pause