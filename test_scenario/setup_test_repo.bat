@echo off
echo ========================================
echo Setting up Test Repository
echo ========================================

REM Create test directory
mkdir test-repo
cd test-repo

REM Initialize git repo
git init

REM Create sample Python application with a bug
echo Creating sample application with bug...

(
echo # Test Application with Bug
echo.
echo def calculate_average(numbers):
echo     """Calculate average with a bug - doesn't handle empty list"""
echo     total = sum(numbers)
echo     # BUG: Division by zero when numbers is empty
echo     return total / len(numbers)
echo.
echo def main():
echo     print("Testing calculator...")
echo     result = calculate_average([1, 2, 3, 4, 5])
echo     print(f"Average: {result}")
echo.
echo if __name__ == "__main__":
echo     main()
) > app.py

REM Create test file
(
echo import unittest
echo from app import calculate_average
echo.
echo class TestApp(unittest.TestCase):
echo     def test_average_normal(self):
echo         self.assertEqual(calculate_average([1, 2, 3]), 2.0)
echo.
echo     def test_average_empty_list(self):
echo         # This test will fail due to the bug
echo         self.assertEqual(calculate_average([]), 0)
echo.
echo if __name__ == "__main__":
echo     unittest.main()
) > test_app.py

REM Create GitHub Actions workflow
mkdir .github
mkdir .github\workflows

(
echo name: CI Pipeline
echo.
echo on:
echo   push:
echo     branches: [ main ]
echo   pull_request:
echo     branches: [ main ]
echo.
echo jobs:
echo   test:
echo     runs-on: ubuntu-latest
echo     steps:
echo     - uses: actions/checkout@v3
echo     - name: Set up Python
echo       uses: actions/setup-python@v4
echo       with:
echo         python-version: '3.11'
echo     - name: Run tests
echo       run: |
echo         python -m unittest test_app.py
) > .github\workflows/ci.yml

REM Create README
(
echo # Test Repository
echo.
echo This repository is used for testing the MCP CI/CD Server
echo.
echo ## Bug
echo The calculate_average function has a bug - it doesn't handle empty lists.
) > README.md

REM Initial commit
git add .
git config user.email "test@example.com"
git config user.name "Test User"
git commit -m "Initial commit with buggy code"

echo.
echo ========================================
echo Test repository created successfully!
echo Location: %CD%
echo ========================================