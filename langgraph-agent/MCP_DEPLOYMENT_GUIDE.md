# MCP Server Deployment Guide

## Overview

This guide explains how to deploy your LangGraph multi-agent system as an MCP (Model Context Protocol) server that integrates with IBM Context Forge (MCP Gateway).

**Benefits of MCP Deployment:**
- ✅ No need for localhost or public URL hosting
- ✅ Direct integration with MCP Gateway infrastructure
- ✅ Automatic tool and resource discovery
- ✅ Seamless integration with Agentic Studio
- ✅ Built-in observability and monitoring
- ✅ Managed by IBM Cloud infrastructure

---

## Architecture

```
┌─────────────────────────────────────────────┐
│     IBM Context Forge (MCP Gateway)         │
│  https://ica-pr-us-south-global-...         │
└─────────────────────────────────────────────┘
                    ↕ MCP Protocol
┌─────────────────────────────────────────────┐
│      LangGraph MCP Server                   │
│  (Running as MCP Server Process)            │
├─────────────────────────────────────────────┤
│  Tools:                                     │
│  - devops_automation                        │
│  - code_review                              │
│  - service_orchestration                    │
│  - multi_agent_task                         │
│  - get_agent_status                         │
│                                             │
│  Resources:                                 │
│  - langgraph://agent/status                 │
│  - langgraph://workflow/state               │
│  - langgraph://execution/history            │
│  - langgraph://config/settings              │
│                                             │
│  Prompts:                                   │
│  - devops_dockerfile                        │
│  - devops_kubernetes                        │
│  - devops_cicd                              │
└─────────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────────┐
│      LangGraph Multi-Agent System           │
│  (Supervisor + Specialized Agents)          │
└─────────────────────────────────────────────┘
```

---

## Prerequisites

1. **Python Environment**
   ```bash
   python --version  # 3.11 or higher
   ```

2. **ICA Credentials**
   - ICA API Key
   - Organization ID
   - Project ID
   - Base URL

3. **MCP Gateway Access**
   - Access to IBM Context Forge
   - Virtual server configuration (if required)

---

## Step 1: Install Dependencies

```bash
cd langgraph-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies (includes MCP SDK)
pip install -r requirements.txt
```

---

## Step 2: Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env with your credentials
nano .env  # or use your preferred editor
```

Required environment variables:
```bash
# ICA Configuration
ICA_API_KEY=your_ica_api_key_here
ICA_ORGANIZATION_ID=your_org_id_here
ICA_PROJECT_ID=your_project_id_here
ICA_BASE_URL=https://api.ibm.com/consulting-advantage/v1

# Agent Configuration
AGENT_NAME=langgraph-devops-agent
AGENT_VERSION=1.0.0
DEFAULT_MODEL=gpt-5.2-chat
ENVIRONMENT=production

# MCP Configuration
MCP_GATEWAY_URL=https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007.us-south.containers.appdomain.cloud
MCP_VIRTUAL_SERVER_ID=your_virtual_server_id  # Optional
```

---

## Step 3: Test MCP Server Locally

Before deploying to MCP Gateway, test the server locally:

```bash
# Run MCP server
python -m src.mcp.mcp_server
```

The server will start and listen for MCP protocol messages via stdio.

**Test with MCP Inspector:**
```bash
# Install MCP Inspector (if not already installed)
npm install -g @modelcontextprotocol/inspector

# Run inspector
mcp-inspector python -m src.mcp.mcp_server
```

This will open a web interface where you can:
- View available tools
- Test tool execution
- Inspect resources
- Try prompts

---

## Step 4: Register with MCP Gateway

### Option A: Using MCP Gateway UI

1. **Access MCP Gateway**
   ```
   https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007.us-south.containers.appdomain.cloud
   ```

2. **Navigate to Virtual Servers**
   - Click "Virtual Servers" in the sidebar
   - Click "Create Virtual Server" or select existing one

3. **Add MCP Server**
   - Click "Add MCP Server"
   - Fill in details:
     - **Name**: `langgraph-devops-agent`
     - **Description**: Multi-agent system for DevOps automation
     - **Command**: `python -m src.mcp.mcp_server`
     - **Working Directory**: `/path/to/langgraph-agent`
     - **Environment Variables**: (from .env file)

4. **Configure Server**
   - Upload `mcp_config.json`
   - Set resource limits (CPU, memory)
   - Configure restart policy

5. **Start Server**
   - Click "Start Server"
   - Monitor logs for successful startup
   - Verify tools are registered

### Option B: Using MCP CLI

```bash
# Install MCP CLI
npm install -g @modelcontextprotocol/cli

# Login to MCP Gateway
mcp login --gateway-url https://ica-pr-us-south-global-...

# Deploy MCP server
mcp deploy \
  --name langgraph-devops-agent \
  --config mcp_config.json \
  --working-dir . \
  --env-file .env

# Check status
mcp status langgraph-devops-agent

# View logs
mcp logs langgraph-devops-agent --follow
```

### Option C: Using Docker Container

```bash
# Build Docker image
docker build -t langgraph-mcp-server:1.0.0 -f Dockerfile.mcp .

# Run container
docker run -d \
  --name langgraph-mcp-server \
  --env-file .env \
  -v $(pwd)/mcp_config.json:/app/mcp_config.json \
  langgraph-mcp-server:1.0.0

# Check logs
docker logs -f langgraph-mcp-server
```

---

## Step 5: Register in Agentic Studio

Once your MCP server is running on the gateway:

1. **Access Agentic Studio**
   ```
   https://agentstudio.servicesessentials.ibm.com
   ```

2. **Navigate to Your Application**
   - Go to "agentic_devops" application
   - Click "Agents" tab

3. **Create Agent Orchestration**
   - Click "Create agent orchestration"
   - Select: IBM Consulting Advantage → LangGraph → gpt-5.2 → ReAct

4. **Configure MCP Integration**
   - Enable "MCP Gateway Integration"
   - Select your virtual server
   - Select "langgraph-devops-agent" from available MCP servers
   - The tools, resources, and prompts will be automatically discovered

5. **Configure Agent Details**
   ```
   Name: agentic-devops-langgraph-mcp
   Description: LangGraph multi-agent system via MCP Gateway
   Version: 1.0.0
   ```

6. **Enable Integrations**
   - ✅ MCP Gateway: ICA Shared MCP Gateway
   - ✅ Workflow Orchestration: AgentCore Orchestrator
   - ✅ Observability: Arize Phoenix

7. **Save and Test**
   - Click "Save"
   - Test with sample prompts in the chat interface

---

## Step 6: Test Your MCP Agent

### Test from Agentic Studio

**Test 1: DevOps Automation**
```
Use the devops_automation tool to create a production-ready Dockerfile for Python FastAPI
```

**Test 2: Code Review**
```
Use the code_review tool to analyze this Python code:
def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total
```

**Test 3: Service Orchestration**
```
Use the service_orchestration tool to create a deployment workflow for services: api-gateway, auth-service, user-service
```

**Test 4: Multi-Agent Task**
```
Use the multi_agent_task tool to: Create a complete DevOps setup including Dockerfile, Kubernetes manifests, and CI/CD pipeline for a Node.js Express application
```

**Test 5: Agent Status**
```
Use the get_agent_status tool to show all available agents and their capabilities
```

### Test via MCP Gateway API

```bash
# Get available tools
curl -X POST https://ica-pr-us-south-global-.../mcp/tools/list \
  -H "Authorization: Bearer $ICA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "server": "langgraph-devops-agent"
  }'

# Call a tool
curl -X POST https://ica-pr-us-south-global-.../mcp/tools/call \
  -H "Authorization: Bearer $ICA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "server": "langgraph-devops-agent",
    "tool": "devops_automation",
    "arguments": {
      "task": "Create Dockerfile for Python FastAPI",
      "environment": "production"
    }
  }'

# Read a resource
curl -X POST https://ica-pr-us-south-global-.../mcp/resources/read \
  -H "Authorization: Bearer $ICA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "server": "langgraph-devops-agent",
    "uri": "langgraph://agent/status"
  }'
```

---

## Available MCP Tools

### 1. devops_automation
**Description**: Automate DevOps tasks (Docker, Kubernetes, CI/CD, Infrastructure)

**Input Schema**:
```json
{
  "task": "Create Dockerfile for Python FastAPI",
  "environment": "production",
  "context": {
    "language": "python",
    "framework": "fastapi",
    "cloud_provider": "aws"
  }
}
```

**Output**: DevOps artifacts and configurations

### 2. code_review
**Description**: Perform comprehensive code review and analysis

**Input Schema**:
```json
{
  "code": "def example(): pass",
  "language": "python",
  "focus_areas": ["security", "performance", "maintainability"]
}
```

**Output**: Code review report with issues and suggestions

### 3. service_orchestration
**Description**: Orchestrate multi-service workflows

**Input Schema**:
```json
{
  "services": ["api-gateway", "auth-service", "user-service"],
  "workflow_type": "deployment",
  "requirements": {
    "high_availability": true,
    "auto_scaling": true
  }
}
```

**Output**: Orchestration plan and configurations

### 4. multi_agent_task
**Description**: Execute complex tasks with multiple agents

**Input Schema**:
```json
{
  "task": "Create complete DevOps setup for microservices application",
  "agents": ["devops_agent", "orchestrator_agent"],
  "context": {
    "architecture": "microservices",
    "cloud": "aws"
  }
}
```

**Output**: Coordinated response from multiple agents

### 5. get_agent_status
**Description**: Get agent status and capabilities

**Input Schema**:
```json
{
  "agent_name": "devops_agent"  // Optional
}
```

**Output**: Agent status, capabilities, and metadata

---

## Available MCP Resources

### 1. langgraph://agent/status
Current status of all agents in the system

### 2. langgraph://workflow/state
Current state of the LangGraph workflow

### 3. langgraph://execution/history
History of recent agent executions

### 4. langgraph://config/settings
Agent configuration and settings

---

## Available MCP Prompts

### 1. devops_dockerfile
Generate production-ready Dockerfile

**Arguments**:
- `language` (required): Programming language
- `framework` (optional): Framework name

### 2. devops_kubernetes
Generate Kubernetes deployment manifests

**Arguments**:
- `app_name` (required): Application name
- `environment` (required): Target environment

### 3. devops_cicd
Generate CI/CD pipeline configuration

**Arguments**:
- `provider` (required): CI/CD provider (github, gitlab, jenkins)
- `language` (required): Programming language

---

## Monitoring and Observability

### View Logs

**MCP Gateway UI**:
1. Navigate to Virtual Servers
2. Select your server
3. Click "Logs" tab
4. View real-time logs

**MCP CLI**:
```bash
mcp logs langgraph-devops-agent --follow
```

**Docker**:
```bash
docker logs -f langgraph-mcp-server
```

### Monitor Performance

**Arize Phoenix** (Observability Dashboard):
```
https://observability.servicesessentials.ibm.com
```

View:
- Tool execution traces
- Response times
- Error rates
- Token usage
- Agent interactions

### Health Checks

The MCP server automatically reports health status to the gateway.

**Check health via API**:
```bash
curl -X GET https://ica-pr-us-south-global-.../mcp/servers/langgraph-devops-agent/health \
  -H "Authorization: Bearer $ICA_API_KEY"
```

---

## Troubleshooting

### Issue: MCP Server Not Starting

**Possible Causes**:
- Missing dependencies
- Invalid configuration
- Environment variables not set

**Solutions**:
```bash
# Check dependencies
pip list | grep mcp

# Validate configuration
python -c "import json; json.load(open('mcp_config.json'))"

# Check environment
python -c "from src.config.settings import get_settings; print(get_settings())"

# View detailed logs
python -m src.mcp.mcp_server 2>&1 | tee mcp_server.log
```

### Issue: Tools Not Appearing in Agentic Studio

**Possible Causes**:
- MCP server not registered with gateway
- Configuration not synced
- Cache issue

**Solutions**:
1. Restart MCP server
2. Re-register with gateway
3. Clear Agentic Studio cache (Ctrl+F5)
4. Check MCP Gateway logs

### Issue: Tool Execution Fails

**Possible Causes**:
- Invalid input arguments
- ICA credentials expired
- LLM model unavailable

**Solutions**:
```bash
# Test tool locally
python -c "
from src.mcp.mcp_server import LangGraphMCPServer
import asyncio

async def test():
    server = LangGraphMCPServer()
    result = await server._execute_devops_task({
        'task': 'Create Dockerfile for Python',
        'environment': 'production'
    })
    print(result)

asyncio.run(test())
"

# Check ICA credentials
curl -X GET $ICA_BASE_URL/health \
  -H "Authorization: Bearer $ICA_API_KEY"

# Check model availability
curl -X POST $ICA_BASE_URL/models/list \
  -H "Authorization: Bearer $ICA_API_KEY"
```

### Issue: High Latency

**Possible Causes**:
- Network latency to ICA LLM Gateway
- Complex agent workflows
- Resource constraints

**Solutions**:
1. Increase timeout settings
2. Optimize agent workflows
3. Scale MCP server resources
4. Use caching for repeated requests

---

## Best Practices

### Security
- ✅ Store credentials in secure vault (not in code)
- ✅ Use environment-specific configurations
- ✅ Rotate API keys regularly
- ✅ Enable audit logging
- ✅ Restrict MCP server access

### Performance
- ✅ Monitor tool execution times
- ✅ Implement caching for common requests
- ✅ Use async operations
- ✅ Optimize LLM prompts
- ✅ Set appropriate timeouts

### Reliability
- ✅ Implement retry logic
- ✅ Handle errors gracefully
- ✅ Monitor health checks
- ✅ Set up alerting
- ✅ Regular backups of configuration

### Maintenance
- ✅ Keep dependencies updated
- ✅ Monitor for security vulnerabilities
- ✅ Review and optimize prompts
- ✅ Document changes
- ✅ Test before production updates

---

## Scaling

### Horizontal Scaling

Deploy multiple instances of the MCP server:

```bash
# Deploy instance 1
mcp deploy --name langgraph-devops-agent-1 --config mcp_config.json

# Deploy instance 2
mcp deploy --name langgraph-devops-agent-2 --config mcp_config.json

# Configure load balancing in MCP Gateway
```

### Vertical Scaling

Increase resources for the MCP server:

```json
{
  "resources": {
    "cpu": "2000m",
    "memory": "4Gi",
    "storage": "10Gi"
  }
}
```

---

## Next Steps

After successful MCP deployment:

1. ✅ Test all tools and resources
2. ✅ Configure monitoring and alerting
3. ✅ Set up CI/CD for MCP server updates
4. ✅ Implement additional agents (Code Review, Orchestrator)
5. ✅ Extend with custom tools and resources
6. ✅ Integrate with other MCP servers
7. ✅ Train team on MCP usage

---

## Support

**Documentation**:
- MCP Protocol: https://modelcontextprotocol.io
- IBM Context Forge: https://ibm.com/context-forge
- Agentic Studio: https://agentstudio.servicesessentials.ibm.com

**Resources**:
- MCP Gateway: https://ica-pr-us-south-global-...
- Observability: https://observability.servicesessentials.ibm.com

**Contact**:
- Slack: #ica-procode-agents
- Email: support@enterprise-advantage.ibm.com

---

**Your LangGraph agent is now deployed as an MCP server!** 🎉

No need for localhost or public URLs - everything runs through the MCP Gateway infrastructure.