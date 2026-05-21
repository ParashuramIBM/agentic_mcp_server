# MCP Server Setup Guide

This guide explains how to run your LangGraph MCP server and register it with Bob/Claude Desktop.

## 🎯 Overview

Your MCP server is **fully implemented** with 5 tools, 4 resources, and 3 prompts. This guide shows you how to run it.

## 📋 Prerequisites

1. Python 3.11+ installed
2. All dependencies installed:
   ```bash
   cd langgraph-agent
   pip install -r requirements.txt
   ```

3. Environment variables set in `.env` file

## 🚀 Running the MCP Server

### Option 1: Direct Python Execution (Recommended)

```bash
cd langgraph-agent
python run_mcp_server.py
```

This will:
- ✅ Start the MCP server on stdio
- ✅ Load all tools and resources
- ✅ Wait for MCP protocol messages

### Option 2: Module Execution

```bash
cd langgraph-agent
python -m src.mcp.mcp_server
```

**Note**: This requires proper PYTHONPATH setup.

## 🔧 Bob/Claude Desktop Configuration

Your `.bob/mcp.json` is already configured:

```json
{
  "mcpServers": {
    "langgraph-devops-agent": {
      "command": "python",
      "args": ["langgraph-agent/run_mcp_server.py"],
      "cwd": "c:/Workspaces/ibm/agentic_devops/agentic-devops",
      "env": {
        "ICA_API_KEY": "735fb204-d173-487a-b86e-c4ceb5e7641c",
        "ICA_ORGANIZATION_ID": "6a016fabe9eed92a72d7a945",
        "ICA_PROJECT_ID": "511cd8a4-2a9a-4247-b7a2-e9fcfbead831",
        "ICA_API_BASE": "https://agentstudio.servicesessentials.ibm.com",
        "OPENAI_API_KEY": "735fb204-d173-487a-b86e-c4ceb5e7641c",
        "OPENAI_API_BASE": "https://agentstudio.servicesessentials.ibm.com/api/v1",
        "PYTHONPATH": "c:/Workspaces/ibm/agentic_devops/agentic-devops/langgraph-agent"
      }
    }
  }
}
```

### Restart Bob/Claude Desktop

After updating `mcp.json`:
1. Close Bob/Claude Desktop completely
2. Reopen it
3. The MCP server will start automatically

## ✅ Verify MCP Server is Running

### Check Bob's MCP Status

In Bob/Claude Desktop, you should see:
- ✅ `langgraph-devops-agent` server connected
- ✅ 5 tools available
- ✅ 4 resources available
- ✅ 3 prompts available

### Test with Bob

Ask Bob:
```
What MCP tools are available?
```

You should see:
- `devops_automation`
- `code_review`
- `service_orchestration`
- `multi_agent_task`
- `get_agent_status`

### Use a Tool

Ask Bob:
```
Use the devops_automation tool to create a Dockerfile for Python FastAPI
```

Bob will call your MCP server and return the result!

## 🛠️ Available Tools

### 1. devops_automation
```json
{
  "task": "Create Dockerfile for Python FastAPI",
  "environment": "production",
  "context": {
    "language": "python",
    "framework": "fastapi"
  }
}
```

### 2. code_review
```json
{
  "code": "def hello(): print('world')",
  "language": "python",
  "focus_areas": ["security", "performance"]
}
```

### 3. service_orchestration
```json
{
  "services": ["api-gateway", "auth-service"],
  "workflow_type": "deployment",
  "requirements": {}
}
```

### 4. multi_agent_task
```json
{
  "task": "Create complete DevOps setup for microservices",
  "context": {}
}
```

### 5. get_agent_status
```json
{
  "agent_name": "devops_agent"
}
```

## 📊 Available Resources

### 1. langgraph://agent/status
Get current status of all agents

### 2. langgraph://workflow/state
Get workflow state and configuration

### 3. langgraph://execution/history
Get recent execution history

### 4. langgraph://config/settings
Get agent configuration

## 🎯 Available Prompts

### 1. devops_dockerfile
```
Arguments: language, framework
```

### 2. devops_kubernetes
```
Arguments: app_name, environment
```

### 3. devops_cicd
```
Arguments: provider, language
```

## 🔍 Troubleshooting

### Issue: "Connection closed" Error

**Cause**: MCP server failed to start

**Solutions**:

1. **Check Python Path**
   ```bash
   python --version  # Should be 3.11+
   which python      # Verify correct Python
   ```

2. **Check Dependencies**
   ```bash
   cd langgraph-agent
   pip install -r requirements.txt
   ```

3. **Check Environment Variables**
   ```bash
   # Verify .env file exists
   cat .env | grep ICA_API_KEY
   ```

4. **Run Server Manually**
   ```bash
   cd langgraph-agent
   python run_mcp_server.py
   ```
   
   Look for errors in output.

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Use `run_mcp_server.py` instead of module execution:

```json
{
  "command": "python",
  "args": ["langgraph-agent/run_mcp_server.py"]
}
```

### Issue: "No tools available"

**Cause**: MCP server not connected

**Solutions**:

1. Check Bob's MCP status
2. Restart Bob/Claude Desktop
3. Check server logs
4. Verify mcp.json configuration

### Issue: Settings Validation Error

**Cause**: Missing required environment variables

**Solution**: Ensure `.env` has all required variables:
```bash
ICA_API_KEY=your-key
ICA_ORGANIZATION_ID=your-org-id
ICA_PROJECT_ID=your-project-id
OPENAI_API_KEY=your-key
```

## 📝 Testing the MCP Server

### Test 1: Manual Start

```bash
cd langgraph-agent
python run_mcp_server.py
```

Expected output:
```
Starting LangGraph MCP Server...
Python path: /path/to/langgraph-agent
Current directory: /path/to/langgraph-agent
INFO:__main__:LangGraph MCP Server initialized
INFO:__main__:Starting LangGraph MCP Server...
```

### Test 2: Tool Call via Bob

In Bob/Claude Desktop:
```
Use devops_automation to create a Dockerfile for Python FastAPI
```

Expected: Bob calls the tool and returns a Dockerfile

### Test 3: Resource Access

In Bob/Claude Desktop:
```
Read the langgraph://agent/status resource
```

Expected: Bob returns agent status information

## 🎉 Success Indicators

✅ MCP server starts without errors
✅ Bob shows "langgraph-devops-agent" connected
✅ 5 tools are available in Bob
✅ Tool calls return results
✅ Resources are accessible

## 📞 Support

If issues persist:
1. Check logs in Bob/Claude Desktop
2. Run server manually to see errors
3. Verify all environment variables
4. Check Python version and dependencies

## 🔗 Related Documentation

- [MCP_TROUBLESHOOTING.md](MCP_TROUBLESHOOTING.md) - Detailed troubleshooting
- [MCP_CONTEXT_STUDIO_INTEGRATION.md](MCP_CONTEXT_STUDIO_INTEGRATION.md) - Context Studio integration
- [src/mcp/mcp_server.py](src/mcp/mcp_server.py) - Server implementation

---

**Your MCP server is ready to use!** 🚀