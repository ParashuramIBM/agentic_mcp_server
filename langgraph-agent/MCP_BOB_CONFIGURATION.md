# LangGraph DevOps Agent - Bob/Claude Desktop MCP Configuration

## Overview

This guide documents the complete MCP (Model Context Protocol) server configuration for the LangGraph DevOps Agent, integrated with Bob/Claude Desktop for seamless AI-powered DevOps automation.

## 🎯 Use Case

**Scenario:** Enterprise DevOps automation using AI agents through Bob/Claude Desktop

**Problem Solved:**
- Manual DevOps tasks (Dockerfile creation, K8s manifests, CI/CD pipelines)
- Code review bottlenecks
- Complex multi-service orchestration
- Lack of standardization across teams

**Solution:** MCP-enabled LangGraph agent accessible directly from Bob/Claude Desktop

## 📋 Configuration File

**Location:** `~/.bob/settings/mcp_settings.json` (Windows: `C:\Users\<username>\.bob\settings\mcp_settings.json`)

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
        "AGENT_NAME": "langgraph-devops-agent",
        "AGENT_VERSION": "1.0.0",
        "DEFAULT_MODEL": "gpt-5.2-chat",
        "ENVIRONMENT": "production",
        "PYTHONPATH": "c:/Workspaces/ibm/agentic_devops/agentic-devops/langgraph-agent"
      },
      "metadata": {
        "name": "LangGraph DevOps Agent",
        "version": "1.0.0",
        "description": "Multi-agent system for DevOps automation, code review, and service orchestration",
        "author": "IBM Consulting Advantage",
        "capabilities": [
          "devops_automation",
          "code_review",
          "service_orchestration",
          "multi_agent_coordination"
        ],
        "tools": [
          {
            "name": "devops_automation",
            "description": "Automate DevOps tasks (Docker, Kubernetes, CI/CD, Infrastructure)",
            "category": "automation"
          },
          {
            "name": "code_review",
            "description": "Perform comprehensive code review and analysis",
            "category": "quality"
          },
          {
            "name": "service_orchestration",
            "description": "Orchestrate multi-service workflows",
            "category": "orchestration"
          },
          {
            "name": "multi_agent_task",
            "description": "Execute complex tasks with multiple agents",
            "category": "coordination"
          },
          {
            "name": "get_agent_status",
            "description": "Get agent status and capabilities",
            "category": "monitoring"
          }
        ],
        "resources": [
          {
            "uri": "langgraph://agent/status",
            "name": "Agent Status",
            "description": "Current status of all agents"
          },
          {
            "uri": "langgraph://workflow/state",
            "name": "Workflow State",
            "description": "Current workflow state"
          },
          {
            "uri": "langgraph://execution/history",
            "name": "Execution History",
            "description": "Recent execution history"
          },
          {
            "uri": "langgraph://config/settings",
            "name": "Configuration",
            "description": "Agent configuration settings"
          }
        ],
        "prompts": [
          {
            "name": "devops_dockerfile",
            "description": "Generate production-ready Dockerfile"
          },
          {
            "name": "devops_kubernetes",
            "description": "Generate Kubernetes manifests"
          },
          {
            "name": "devops_cicd",
            "description": "Generate CI/CD pipeline"
          }
        ]
      }
    }
  }
}
```

## 🔧 Configuration Breakdown

### 1. Server Identification
```json
"langgraph-devops-agent": {
  // Unique server name in Bob's MCP registry
}
```

### 2. Command Execution
```json
"command": "python",
"args": ["langgraph-agent/run_mcp_server.py"],
"cwd": "c:/Workspaces/ibm/agentic_devops/agentic-devops"
```

**What it does:**
- Launches Python interpreter
- Runs the MCP server script
- Sets working directory for relative paths

### 3. Environment Variables

#### IBM Consulting Advantage (ICA) Credentials
```json
"ICA_API_KEY": "735fb204-d173-487a-b86e-c4ceb5e7641c",
"ICA_ORGANIZATION_ID": "6a016fabe9eed92a72d7a945",
"ICA_PROJECT_ID": "511cd8a4-2a9a-4247-b7a2-e9fcfbead831",
"ICA_API_BASE": "https://agentstudio.servicesessentials.ibm.com"
```

**Purpose:** Authenticate with IBM's Enterprise AI platform

#### OpenAI-Compatible API Configuration
```json
"OPENAI_API_KEY": "735fb204-d173-487a-b86e-c4ceb5e7641c",
"OPENAI_API_BASE": "https://agentstudio.servicesessentials.ibm.com/api/v1"
```

**Purpose:** Enable LangGraph to use ICA's LLM gateway (OpenAI-compatible)

#### Agent Configuration
```json
"AGENT_NAME": "langgraph-devops-agent",
"AGENT_VERSION": "1.0.0",
"DEFAULT_MODEL": "gpt-5.2-chat",
"ENVIRONMENT": "production"
```

**Purpose:** Configure agent behavior and model selection

#### Python Path
```json
"PYTHONPATH": "c:/Workspaces/ibm/agentic_devops/agentic-devops/langgraph-agent"
```

**Purpose:** Ensure Python can import the `src` module

### 4. Metadata

#### Capabilities
```json
"capabilities": [
  "devops_automation",
  "code_review",
  "service_orchestration",
  "multi_agent_coordination"
]
```

**What the agent can do:**
- Automate DevOps workflows
- Review code for quality and security
- Orchestrate multiple services
- Coordinate complex multi-agent tasks

#### Tools (5 Total)

**Tool 1: devops_automation**
```json
{
  "name": "devops_automation",
  "description": "Automate DevOps tasks (Docker, Kubernetes, CI/CD, Infrastructure)",
  "category": "automation"
}
```
- Creates Dockerfiles
- Generates Kubernetes manifests
- Builds CI/CD pipelines
- Provisions infrastructure

**Tool 2: code_review**
```json
{
  "name": "code_review",
  "description": "Perform comprehensive code review and analysis",
  "category": "quality"
}
```
- Static code analysis
- Security vulnerability scanning
- Best practices validation
- Performance optimization suggestions

**Tool 3: service_orchestration**
```json
{
  "name": "service_orchestration",
  "description": "Orchestrate multi-service workflows",
  "category": "orchestration"
}
```
- Multi-service deployment
- Service mesh configuration
- Load balancing setup
- Inter-service communication

**Tool 4: multi_agent_task**
```json
{
  "name": "multi_agent_task",
  "description": "Execute complex tasks with multiple agents",
  "category": "coordination"
}
```
- Complex workflow coordination
- Multi-agent collaboration
- Task decomposition and delegation
- Result aggregation

**Tool 5: get_agent_status**
```json
{
  "name": "get_agent_status",
  "description": "Get agent status and capabilities",
  "category": "monitoring"
}
```
- Agent health monitoring
- Capability discovery
- Performance metrics
- Execution history

#### Resources (4 Total)

**Resource 1: Agent Status**
```json
{
  "uri": "langgraph://agent/status",
  "name": "Agent Status",
  "description": "Current status of all agents"
}
```

**Resource 2: Workflow State**
```json
{
  "uri": "langgraph://workflow/state",
  "name": "Workflow State",
  "description": "Current workflow state"
}
```

**Resource 3: Execution History**
```json
{
  "uri": "langgraph://execution/history",
  "name": "Execution History",
  "description": "Recent execution history"
}
```

**Resource 4: Configuration**
```json
{
  "uri": "langgraph://config/settings",
  "name": "Configuration",
  "description": "Agent configuration settings"
}
```

#### Prompts (3 Total)

**Prompt 1: Dockerfile Generation**
```json
{
  "name": "devops_dockerfile",
  "description": "Generate production-ready Dockerfile"
}
```

**Prompt 2: Kubernetes Manifests**
```json
{
  "name": "devops_kubernetes",
  "description": "Generate Kubernetes manifests"
}
```

**Prompt 3: CI/CD Pipeline**
```json
{
  "name": "devops_cicd",
  "description": "Generate CI/CD pipeline"
}
```

## 🚀 How to Use

### Step 1: Setup Configuration

1. **Locate Bob settings directory:**
   - Windows: `C:\Users\<username>\.bob\settings\`
   - macOS/Linux: `~/.bob/settings/`

2. **Create or edit `mcp_settings.json`:**
   ```bash
   # Windows
   notepad C:\Users\<username>\.bob\settings\mcp_settings.json
   
   # macOS/Linux
   nano ~/.bob/settings/mcp_settings.json
   ```

3. **Paste the configuration** (see above)

4. **Update paths and credentials:**
   - Change `cwd` to your workspace path
   - Update `ICA_API_KEY`, `ICA_ORGANIZATION_ID`, `ICA_PROJECT_ID`
   - Adjust `PYTHONPATH` to match your directory structure

### Step 2: Restart Bob/Claude Desktop

Close and reopen Bob to load the new MCP server configuration.

### Step 3: Verify Connection

In Bob, ask:
```
What MCP tools are available?
```

Expected response should list all 5 tools.

### Step 4: Use the Tools

#### Example 1: Create Dockerfile
```
Use the devops_automation tool to create a Dockerfile for Python FastAPI application
```

#### Example 2: Review Code
```
Use the code_review tool to review this Python code:

def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
```

#### Example 3: Orchestrate Services
```
Use the service_orchestration tool to create a deployment workflow for api-gateway, auth-service, and user-service
```

#### Example 4: Multi-Agent Task
```
Use the multi_agent_task tool to create a complete DevOps setup for a Node.js Express microservices application
```

#### Example 5: Check Status
```
Use the get_agent_status tool to show me the current status of all agents
```

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Bob/Claude Desktop                        │
│                    (MCP Client)                              │
└────────────────────────┬────────────────────────────────────┘
                         │ MCP Protocol (stdio)
                         │
┌────────────────────────▼────────────────────────────────────┐
│              LangGraph MCP Server                            │
│              (run_mcp_server.py)                             │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  5 Tools:                                            │  │
│  │  • devops_automation                                 │  │
│  │  • code_review                                       │  │
│  │  • service_orchestration                             │  │
│  │  • multi_agent_task                                  │  │
│  │  • get_agent_status                                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  4 Resources:                                        │  │
│  │  • langgraph://agent/status                          │  │
│  │  • langgraph://workflow/state                        │  │
│  │  • langgraph://execution/history                     │  │
│  │  • langgraph://config/settings                       │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│              LangGraph Workflow Engine                       │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Supervisor  │  │   DevOps     │  │  Code Review │     │
│  │    Agent     │──│    Agent     │  │    Agent     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│         IBM Consulting Advantage (ICA)                       │
│         LLM Gateway (OpenAI-compatible)                      │
│                                                              │
│         Model: gpt-5.2-chat                                  │
└──────────────────────────────────────────────────────────────┘
```

## 🔐 Security Considerations

### API Key Management
- **Never commit** `mcp_settings.json` to version control
- Store credentials in environment variables or secure vaults
- Rotate API keys regularly

### Network Security
- MCP server runs locally (stdio communication)
- API calls to ICA use HTTPS
- No external network exposure required

### Access Control
- Bob/Claude Desktop has full access to MCP tools
- Consider implementing rate limiting for production
- Monitor execution logs for suspicious activity

## 🐛 Troubleshooting

### Issue 1: Server Not Starting

**Symptom:** Bob shows "MCP server failed to start"

**Solutions:**
1. Check Python is in PATH: `python --version`
2. Verify working directory exists
3. Check PYTHONPATH is correct
4. Review Bob logs: `~/.bob/logs/`

### Issue 2: Import Errors

**Symptom:** `ModuleNotFoundError: No module named 'src'`

**Solutions:**
1. Verify PYTHONPATH in configuration
2. Check `run_mcp_server.py` exists
3. Ensure `src/` directory structure is correct

### Issue 3: Authentication Errors

**Symptom:** 401 Unauthorized or 403 Forbidden

**Solutions:**
1. Verify ICA_API_KEY is valid
2. Check ICA_ORGANIZATION_ID and ICA_PROJECT_ID
3. Ensure API key has required permissions
4. Test credentials with curl:
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
        https://agentstudio.servicesessentials.ibm.com/api/v1/models
   ```

### Issue 4: Tools Not Appearing

**Symptom:** Bob doesn't show MCP tools

**Solutions:**
1. Restart Bob/Claude Desktop
2. Check `mcp_settings.json` syntax (valid JSON)
3. Verify server is running: Check Bob logs
4. Test manually: `python langgraph-agent/run_mcp_server.py`

## 📈 Performance Optimization

### 1. Model Selection
```json
"DEFAULT_MODEL": "gpt-5.2-chat"  // Fast, balanced
// or
"DEFAULT_MODEL": "gpt-5.2-turbo"  // Faster, less accurate
// or
"DEFAULT_MODEL": "gpt-5.2-advanced"  // Slower, more accurate
```

### 2. Caching
Enable response caching in `settings.py`:
```python
ENABLE_CACHE = True
CACHE_TTL = 3600  # 1 hour
```

### 3. Concurrent Execution
Adjust max concurrent agents:
```python
MAX_CONCURRENT_AGENTS = 3
```

## 🎯 Real-World Use Cases

### Use Case 1: Microservices Deployment
**Scenario:** Deploy 5 microservices with service mesh

**Bob Command:**
```
Use service_orchestration to deploy api-gateway, auth-service, user-service, payment-service, and notification-service with Istio service mesh
```

**Output:**
- Kubernetes manifests for all services
- Istio VirtualService and DestinationRule configs
- Service mesh policies
- Deployment workflow

### Use Case 2: Code Quality Gate
**Scenario:** Automated code review in CI/CD

**Bob Command:**
```
Use code_review to analyze the entire src/ directory for security vulnerabilities and code quality issues
```

**Output:**
- Security vulnerability report
- Code quality metrics
- Best practice violations
- Refactoring suggestions

### Use Case 3: Infrastructure as Code
**Scenario:** Generate complete IaC for new project

**Bob Command:**
```
Use multi_agent_task to create complete infrastructure for a Python FastAPI application with PostgreSQL, Redis, and Nginx
```

**Output:**
- Dockerfile for FastAPI
- Docker Compose configuration
- Kubernetes manifests
- Terraform/CloudFormation templates
- CI/CD pipeline (GitHub Actions/GitLab CI)

## 📚 Additional Resources

- **MCP Protocol Specification:** https://modelcontextprotocol.io/
- **LangGraph Documentation:** https://langchain-ai.github.io/langgraph/
- **IBM Consulting Advantage:** https://www.ibm.com/consulting/advantage
- **Bob/Claude Desktop:** https://claude.ai/

## 🤝 Support

For issues or questions:
1. Check troubleshooting section above
2. Review Bob logs: `~/.bob/logs/`
3. Test MCP server manually: `python langgraph-agent/run_mcp_server.py`
4. Contact IBM Consulting Advantage support

## 📝 Version History

- **v1.0.0** (2026-05-20)
  - Initial release
  - 5 tools implemented
  - 4 resources available
  - 3 prompts configured
  - Full Bob/Claude Desktop integration

## 🎉 Success Metrics

**What Success Looks Like:**
- ✅ Bob shows all 5 MCP tools
- ✅ Tools execute without errors
- ✅ Generated artifacts are production-ready
- ✅ Response time < 10 seconds
- ✅ Zero authentication failures

**Current Status:**
- ✅ 2/5 tools tested and working
- ✅ Server running stable
- ✅ Bob integration successful
- ✅ ICA authentication working
- ✅ Multi-agent coordination functional

---

**Created:** 2026-05-20  
**Author:** IBM Consulting Advantage  
**License:** Enterprise Use Only