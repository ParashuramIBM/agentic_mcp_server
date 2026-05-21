#!/usr/bin/env python
"""
Simple runner for the CI/CD test scenario
"""

import argparse
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(__file__))

from test_scenario.trigger_failure import CI_FailureSimulator


async def main(auto: bool = False):
    print("\n" + "*" * 30)
    print("MCP CI/CD ORCHESTRATOR - TEST SCENARIO")
    print("*" * 30)

    print("""
This scenario simulates:
1. Developer commits buggy code to PR
2. CI pipeline detects test failure
3. MCP server automatically:
   - Inspects the failure
   - Analyzes root cause
   - Assesses risk
   - Creates auto-repair PR
   - Validates the fix
   - Orchestrates merge to main

""")

    if not auto:
        try:
            input("Press Enter to start the scenario...\n")
        except Exception:
            # In some non-interactive environments, input() may fail
            pass

    simulator = CI_FailureSimulator()
    await simulator.run_complete_scenario()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run MCP CI/CD test scenario")
    parser.add_argument("--auto", action="store_true", help="Run non-interactively (CI)")
    args = parser.parse_args()

    asyncio.run(main(auto=args.auto))