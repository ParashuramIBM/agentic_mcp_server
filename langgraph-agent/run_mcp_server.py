#!/usr/bin/env python3
"""
Standalone MCP Server Launcher
Runs the LangGraph MCP server without requiring package installation
"""

import sys
import os

# Add the langgraph-agent directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Now import and run the MCP server
from src.mcp.mcp_server import main
import asyncio

if __name__ == "__main__":
    print("Starting LangGraph MCP Server...")
    print(f"Python path: {sys.path[0]}")
    print(f"Current directory: {os.getcwd()}")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nMCP Server stopped by user")
    except Exception as e:
        print(f"Error starting MCP server: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
