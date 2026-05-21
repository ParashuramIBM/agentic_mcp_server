# Testing MCP Tools Guide

Complete guide for testing all MCP tools exposed by your LangGraph server.

## 🎯 Three Ways to Test

1. **Via Bob/Claude Desktop** (MCP Client) ⭐ RECOMMENDED
2. **Via A2A Agent** (HTTP) ⭐ WORKS NOW
3. **Via Python Test Script** (Direct) - Requires langgraph installation

---

## Method 1: Test via Bob/Claude Desktop (Recommended)

### Prerequisites
1. MCP server running: `python langgraph-agent/run_mcp_server.py`
2. Bob/Claude Desktop restarted
3. Server shows as connected in Bob

### Test Tool 1: devops_automation

**In Bob/Claude Desktop, ask:**
```
Use the devops_automation tool to create a production-ready Dockerfile for Python FastAPI application
```

**Expected Response:**
Bob will call the tool and return a complete Dockerfile with:
- Multi-stage build
- Security hardening
- Production optimizations

### Test Tool 2: code_review

**In Bob/Claude Desktop, ask:**
```
Use the code_review tool to review this Python code:

def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
```

**Expected Response:**
Bob will return code review with:
- Quality analysis
- Performance suggestions
- Best practices recommendations

### Test Tool 3: service_orchestration

**In Bob/Claude Desktop, ask:**
```
Use the service_orchestration tool to create a deployment workflow for these services: api-gateway, auth-service, user-service
```

**Expected Response:**
Bob will return orchestration plan with:
- Deployment sequence
- Dependencies
- Health checks

### Test Tool 4: multi_agent_task

**In Bob/Claude Desktop, ask:**
```
Use the multi_agent_task tool to create a complete DevOps setup including Dockerfile, Kubernetes manifests, and CI/CD pipeline for a Node.js Express application
```

**Expected Response:**
Bob will coordinate multiple agents and return:
- Complete Dockerfile
- Kubernetes manifests
- CI/CD pipeline configuration

### Test Tool 5: get_agent_status

**In Bob/Claude Desktop, ask:**
```
Use the get_agent_status tool to show me the status of all agents
```

**Expected Response:**
Bob will return:
- List of all agents
- Their status (active/inactive)
- Capabilities of each agent

### Test Resources

**In Bob/Claude Desktop, ask:**
```
Read the langgraph://agent/status resource
```

**Expected Response:**
Bob will return current agent status information

---

## Method 2: Test via Python Script (Direct)

### Run the Test Suite

```bash
cd langgraph-agent/examples
python test_mcp_tools.py
```

This will:
- ✅ Test all 5 tools
- ✅ Test all 4 resources
- ✅ Show detailed results
- ✅ Provide summary

**Expected Output:**
```
================================================================================
  🧪 MCP Tools Comprehensive Test Suite
================================================================================

================================================================================
  Test 1: devops_automation Tool
================================================================================
✅ PASS - devops_automation
Result: {
  "status": "success",
  "task": "Create a production-ready Dockerfile...",
  ...
}

... (tests for all tools)

================================================================================
  📊 Test Summary
================================================================================
✅ Passed: 6/6
❌ Failed: 0/6

🎉 All tests passed! Your MCP server is fully functional.
```

---

## Method 3: Test via A2A Agent (HTTP)

### Create Test Agent

Create `test_a2a_agent.py`:

```python
#!/usr/bin/env python3
"""
Test MCP Tools via A2A Agent
Demonstrates how another agent can invoke your MCP tools via HTTP
"""

import requests
import json
import os

# Your A2A agent endpoint
AGENT_URL = "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024"
API_KEY = os.getenv("AGENTIC_STUDIO_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_devops_automation():
    """Test devops_automation via A2A"""
    print("\n" + "=" * 80)
    print("Test 1: devops_automation via A2A")
    print("=" * 80)
    
    payload = {
        "message": "Create a production-ready Dockerfile for Python FastAPI application",
        "context": {
            "task_type": "devops",
            "environment": "production",
            "language": "python",
            "framework": "fastapi"
        }
    }
    
    response = requests.post(AGENT_URL, headers=headers, json=payload)
    result = response.json()
    
    print(f"Status: {result.get('status')}")
    print(f"Response: {result.get('response', {}).get('message', '')[:200]}...")
    
    return result

def test_code_review():
    """Test code_review via A2A"""
    print("\n" + "=" * 80)
    print("Test 2: code_review via A2A")
    print("=" * 80)
    
    code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
"""
    
    payload = {
        "message": f"Review this Python code: {code}",
        "context": {
            "task_type": "code_review",
            "language": "python"
        }
    }
    
    response = requests.post(AGENT_URL, headers=headers, json=payload)
    result = response.json()
    
    print(f"Status: {result.get('status')}")
    print(f"Review: {result.get('response', {}).get('message', '')[:200]}...")
    
    return result

def test_service_orchestration():
    """Test service_orchestration via A2A"""
    print("\n" + "=" * 80)
    print("Test 3: service_orchestration via A2A")
    print("=" * 80)
    
    payload = {
        "message": "Orchestrate deployment for api-gateway, auth-service, and user-service",
        "context": {
            "task_type": "orchestration",
            "services": ["api-gateway", "auth-service", "user-service"],
            "workflow_type": "deployment"
        }
    }
    
    response = requests.post(AGENT_URL, headers=headers, json=payload)
    result = response.json()
    
    print(f"Status: {result.get('status')}")
    print(f"Plan: {result.get('response', {}).get('message', '')[:200]}...")
    
    return result

def test_multi_agent_task():
    """Test multi_agent_task via A2A"""
    print("\n" + "=" * 80)
    print("Test 4: multi_agent_task via A2A")
    print("=" * 80)
    
    payload = {
        "message": "Create complete DevOps setup for Node.js Express microservices",
        "context": {
            "task_type": "multi",
            "architecture": "microservices",
            "language": "nodejs",
            "framework": "express"
        }
    }
    
    response = requests.post(AGENT_URL, headers=headers, json=payload)
    result = response.json()
    
    print(f"Status: {result.get('status')}")
    print(f"Setup: {result.get('response', {}).get('message', '')[:200]}...")
    
    return result

def main():
    """Run all A2A tests"""
    print("=" * 80)
    print("Testing MCP Tools via A2A Agent")
    print("=" * 80)
    
    if not API_KEY:
        print("❌ Error: AGENTIC_STUDIO_API_KEY not set")
        return
    
    tests = [
        ("devops_automation", test_devops_automation),
        ("code_review", test_code_review),
        ("service_orchestration", test_service_orchestration),
        ("multi_agent_task", test_multi_agent_task)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            success = result.get('status') == 'completed'
            results.append((name, success))
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"   {status} - {name}")

if __name__ == "__main__":
    main()
```

### Run A2A Tests

```bash
export AGENTIC_STUDIO_API_KEY="your-key"
python test_a2a_agent.py
```

---

## 🔍 Verification Checklist

### MCP Server Running
- [ ] Server started without errors
- [ ] Shows "LangGraph MCP Server initialized"
- [ ] Shows "Starting LangGraph MCP Server..."

### Bob/Claude Desktop
- [ ] Bob restarted after mcp.json update
- [ ] Server shows as connected
- [ ] Tools are listed when asked
- [ ] Tools execute successfully

### Direct Testing
- [ ] test_mcp_tools.py runs without errors
- [ ] All 5 tools pass
- [ ] All 4 resources accessible
- [ ] Summary shows 6/6 passed

### A2A Testing
- [ ] API key is set
- [ ] Agent endpoint is accessible
- [ ] Tools respond via HTTP
- [ ] Results are returned correctly

---

## 📊 Expected Results

### Tool: devops_automation
**Input**: "Create Dockerfile for Python FastAPI"
**Output**: Complete Dockerfile with multi-stage build, security, optimization

### Tool: code_review
**Input**: Python code snippet
**Output**: Code review with quality, security, performance analysis

### Tool: service_orchestration
**Input**: List of services
**Output**: Orchestration plan with deployment sequence

### Tool: multi_agent_task
**Input**: Complex task description
**Output**: Coordinated response from multiple agents

### Tool: get_agent_status
**Input**: (none or agent_name)
**Output**: Status of all agents with capabilities

---

## 🐛 Troubleshooting

### Issue: "Tool not found"
**Solution**: Restart Bob/Claude Desktop

### Issue: "Connection closed"
**Solution**: Check MCP server is running

### Issue: "401 Unauthorized" (A2A)
**Solution**: Set AGENTIC_STUDIO_API_KEY

### Issue: "Tool execution failed"
**Solution**: Check server logs for errors

---

## 📞 Support

- **MCP Server Logs**: Check terminal where server is running
- **Bob Logs**: Check Bob/Claude Desktop logs
- **Documentation**: See MCP_SERVER_SETUP.md

---

**Your MCP tools are ready to test!** 🚀

Choose your preferred testing method and verify all tools work correctly.