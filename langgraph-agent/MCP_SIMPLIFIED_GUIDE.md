# Simplified MCP Deployment Guide

## Understanding MCP Gateway

The MCP Gateway at `https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007.us-south.containers.appdomain.cloud` is **not a REST API endpoint**. 

It's an infrastructure service that:
1. **Hosts MCP servers** (your LangGraph agent)
2. **Manages stdio communication** between clients and servers
3. **Provides service discovery** for Agentic Studio

## The Correct Deployment Approach

### Option 1: Register MCP Server in Agentic Studio (Recommended)

This is the **easiest and recommended** approach:

**Step 1: Prepare Your MCP Server**
```bash
cd langgraph-agent
pip install -r requirements.txt
cp .env.template .env
# Edit .env with your ICA credentials
```

**Step 2: Test Locally**
```bash
# Test the MCP server works
python -m src.mcp.mcp_server
```

**Step 3: Register in Agentic Studio**

1. Go to https://agentstudio.servicesessentials.ibm.com
2. Navigate to "agentic_devops" → "Agents" tab
3. Click "Create agent orchestration"
4. Select: IBM Consulting Advantage → LangGraph → gpt-5.2 → ReAct

5. **In the configuration dialog:**
   - Enable "MCP Gateway Integration"
   - Select "ICA Shared MCP Gateway"
   - **Upload your MCP configuration:**
     - Click "Upload MCP Config"
     - Select `mcp_config.json`
   - The system will:
     - Deploy your MCP server to the gateway
     - Register all tools, resources, and prompts
     - Make them available in Agentic Studio

6. **Configure agent details:**
   ```
   Name: agentic-devops-langgraph-mcp
   Description: LangGraph multi-agent system via MCP Gateway
   Version: 1.0.0
   ```

7. **Save and test** in the Agentic Studio chat interface

**Step 4: Use Your Agent**

Once registered, you can use your agent directly in Agentic Studio:

```
Create a production-ready Dockerfile for Python FastAPI application
```

The Agentic Studio will:
1. Route your request to the MCP Gateway
2. The gateway invokes your MCP server's `devops_automation` tool
3. Your LangGraph agent processes the request
4. Results are returned to Agentic Studio

---

### Option 2: Use Agentic Studio's Built-in Agent Creation

Instead of deploying an external MCP server, you can create the agent directly in Agentic Studio:

**Step 1: Create Agent in Agentic Studio**

1. Go to https://agentstudio.servicesessentials.ibm.com
2. Click "Create agent orchestration"
3. Select: IBM Consulting Advantage → LangGraph → gpt-5.2 → ReAct

4. **Describe your agent:**
   ```
   Create a LangGraph ReAct multi-agent system for DevOps automation that helps teams 
   design, evolve, and reason about production-ready Agentic DevOps workflows.
   
   Capabilities:
   - DevOps automation (Docker, Kubernetes, CI/CD pipelines)
   - Infrastructure as Code generation (Terraform)
   - Code review and analysis
   - Service orchestration and workflow management
   - Multi-agent coordination with supervisor pattern
   ```

5. **Agentic Studio will:**
   - Generate the agent configuration
   - Create the LangGraph workflow
   - Deploy it to the platform
   - Make it available immediately

6. **Test your agent** in the chat interface

**This approach:**
- ✅ No manual deployment needed
- ✅ Fully managed by Agentic Studio
- ✅ Automatic scaling and monitoring
- ✅ Integrated observability
- ✅ No infrastructure management

---

### Option 3: Deploy as Standalone Service (Advanced)

If you need full control and want to deploy independently:

**Step 1: Deploy to IBM Cloud Code Engine**

```bash
# Install IBM Cloud CLI
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh

# Login
ibmcloud login --sso

# Target your resource group
ibmcloud target -g your-resource-group

# Create Code Engine project
ibmcloud ce project create --name langgraph-agent

# Build and deploy
ibmcloud ce application create \
  --name langgraph-agent \
  --build-source . \
  --dockerfile Dockerfile \
  --env-from-configmap langgraph-config \
  --env-from-secret langgraph-secrets \
  --port 8000 \
  --min-scale 1 \
  --max-scale 5

# Get the URL
ibmcloud ce application get --name langgraph-agent
```

**Step 2: Register in Agentic Studio**

1. Go to Agentic Studio → "Agents" tab
2. Click "Import Agent (A2A)"
3. Enter your Code Engine URL:
   ```
   https://langgraph-agent.xxx.us-south.codeengine.appdomain.cloud
   ```
4. Configure endpoints:
   - Invoke: `/agent/invoke`
   - Stream: `/agent/stream`
   - Status: `/agent/status`
   - Health: `/health`
5. Save and test

---

## Recommended Approach

**For most users, we recommend Option 2** (Agentic Studio's built-in agent creation):

✅ **Easiest** - No deployment needed
✅ **Fastest** - Agent ready in minutes
✅ **Managed** - Platform handles everything
✅ **Integrated** - Full observability and monitoring
✅ **Scalable** - Automatic scaling

**Use Option 1** (MCP Server) if you:
- Need custom MCP tools and resources
- Want to integrate with other MCP clients
- Have existing MCP infrastructure

**Use Option 3** (Standalone) if you:
- Need full control over deployment
- Have specific infrastructure requirements
- Want to integrate with existing services

---

## Quick Start: Recommended Path

**5-Minute Setup:**

1. Go to https://agentstudio.servicesessentials.ibm.com
2. Navigate to "agentic_devops" → "Agents"
3. Click "Create agent orchestration"
4. Select: LangGraph → gpt-5.2 → ReAct
5. Paste the agent description (see Option 2 above)
6. Click "Create"
7. Test in chat: "Create a Dockerfile for Python FastAPI"

**Done!** Your agent is live and ready to use.

---

## Why MCP Gateway Doesn't Have a REST API

The MCP Gateway is designed for:
- **Server hosting** - It hosts MCP servers (like yours)
- **Stdio communication** - MCP protocol uses stdin/stdout
- **Service discovery** - Makes servers available to clients
- **Management** - Lifecycle management of MCP servers

It's **not designed for**:
- Direct REST API calls
- External HTTP requests
- Public API access

**Instead:**
- Agentic Studio communicates with the gateway internally
- Your MCP server runs on the gateway
- Clients (like Agentic Studio) discover and use your tools
- All communication is managed by the platform

---

## Summary

**The MCP Gateway URL is for infrastructure, not for direct API calls.**

**To use your LangGraph agent:**
1. Register it in Agentic Studio (easiest)
2. Or deploy to IBM Cloud Code Engine (more control)
3. Use it through Agentic Studio's chat interface

**The agent is then accessible:**
- In Agentic Studio UI
- Via Agentic Studio API
- Through workflow orchestration
- In other agents via A2A protocol

---

## Next Steps

1. ✅ Choose your deployment approach (we recommend Option 2)
2. ✅ Follow the steps for your chosen option
3. ✅ Test your agent in Agentic Studio
4. ✅ Integrate with workflows and other agents

Need help? Check the main documentation or contact support on Slack: #ica-procode-agents