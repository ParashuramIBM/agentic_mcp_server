# Final Deployment Guide - Agentic Studio Integration

## ✅ The Correct Approach

Based on the Agentic Studio UI, here's the **actual** way to deploy your LangGraph agent:

## Option 1: Use Agentic Studio's Agent Orchestration (Recommended) ⭐

This is the **easiest and correct** approach - the platform creates the agent for you.

### Step-by-Step Instructions

**1. Access Agentic Studio**
```
https://agentstudio.servicesessentials.ibm.com
```

**2. Navigate to Your Application**
- Click on "Agentic App Home"
- Select "agentic_devops" application
- Click on "Agents" tab

**3. Create Agent Orchestration**
- Click the blue "Create agent orchestration" button (top right)
- You'll see: "Welcome to Agent Orchestration"

**4. Select Your Configuration**
- **Platform**: IBM Consulting Advantage
- **Framework**: LangGraph
- **Model**: gpt-5.2
- **Orchestration Pattern**: ReAct

**5. Describe Your Agent**
In the text box, paste:
```
Create a LangGraph ReAct multi-agent system for DevOps automation that helps teams design, evolve, and reason about production-ready Agentic DevOps workflows.

The agent iteratively analyzes DevOps requirements, proposes agent roles and orchestration patterns, and refines designs based on user feedback.

Capabilities:
- DevOps automation (Docker, Kubernetes, CI/CD pipelines, Terraform)
- Infrastructure as Code generation
- Code review and analysis
- Service orchestration and workflow management
- Multi-agent coordination with supervisor pattern

The system uses a supervisor agent to route requests to specialized agents (DevOps, Code Review, Orchestrator) and aggregates their responses.
```

**6. Let Agentic Studio Create the Agent**
- Click the send button (arrow icon)
- The platform will:
  - Generate the agent configuration
  - Create the LangGraph workflow
  - Deploy it automatically
  - Make it available immediately

**7. Test Your Agent**
Once created, test with:
```
Create a production-ready Dockerfile for a Python FastAPI application
```

**Benefits:**
- ✅ No manual deployment
- ✅ No MCP server configuration needed
- ✅ Fully managed by platform
- ✅ Automatic scaling
- ✅ Built-in observability
- ✅ Ready in 5 minutes

---

## Option 2: Deploy Your Own Service and Use REST/A2A

If you want to use your custom implementation:

### Step A: Deploy Your FastAPI Server

**Option A1: Deploy to IBM Cloud Code Engine**

```bash
# Install IBM Cloud CLI
curl -fsSL https://clis.cloud.ibm.com/install/linux | sh

# Login
ibmcloud login --sso

# Target resource group
ibmcloud target -g your-resource-group

# Create Code Engine project
ibmcloud ce project create --name langgraph-agent

# Deploy application
ibmcloud ce application create \
  --name langgraph-agent \
  --build-source . \
  --dockerfile Dockerfile \
  --port 8000 \
  --min-scale 1 \
  --max-scale 5 \
  --env ICA_API_KEY=$ICA_API_KEY \
  --env ICA_ORGANIZATION_ID=$ICA_ORGANIZATION_ID \
  --env ICA_PROJECT_ID=$ICA_PROJECT_ID

# Get the URL
ibmcloud ce application get --name langgraph-agent --output url
```

You'll get a URL like:
```
https://langgraph-agent.xxx.us-south.codeengine.appdomain.cloud
```

**Option A2: Use ngrok for Local Testing**

```bash
# Start your agent locally
cd langgraph-agent
python -m src.api.server

# In another terminal, start ngrok
ngrok http 8000
```

You'll get a URL like:
```
https://abc123.ngrok.io
```

### Step B: Register in Agentic Studio

**1. Go to MCP Servers Page**
```
https://agentstudio.servicesessentials.ibm.com/create/mcp-servers
```

**2. Select REST/A2A Server**
- In the "MCP Servers" section
- Check the box for "REST/A2A"
- Click "Select All" if needed

**3. Configure Virtual Server**
- The system will ask you to configure the REST/A2A connection
- Enter your deployment URL:
  - **Base URL**: `https://your-deployment-url.com`
  - **Invoke Endpoint**: `/agent/invoke`
  - **Stream Endpoint**: `/agent/stream`
  - **Status Endpoint**: `/agent/status`
  - **Health Endpoint**: `/health`

**4. Add Tags** (optional)
```
development, production, api-gateway
```

**5. Save Configuration**
- Click "Save" or "Create Virtual Server"
- The system will validate your endpoints

**6. Test the Connection**
- Go back to "Agents" tab
- Your agent should appear in the list
- Test it in the chat interface

---

## Option 3: Use the Existing Agent You Created

Based on the screenshot showing you already have an agent:
```
agentic-devops-architect-react-d...
```

**You can use this existing agent!**

1. Go to the Agents tab
2. Click on your existing agent
3. Test it with DevOps prompts
4. If it works, you're done!

---

## Understanding the MCP Gateway UI

The screenshot shows:

**Left Sidebar:**
- MCP Servers
- Virtual Servers ← You are here
- Tools
- Prompts
- Resources
- Agents (A2A)

**Main Panel:**
- **MCP Servers**: Select from pre-configured servers (REST/A2A, etc.)
- **Associated Tools**: Tools available from selected server
- **Associated Resources**: Resources available from selected server
- **Associated Prompts**: Prompts available from selected server
- **Tags**: Metadata for organization

**What This Means:**
- You don't upload custom MCP servers here
- You select from existing server types (REST/A2A)
- You configure how to connect to your deployed service
- The "REST/A2A" option is for connecting to external REST APIs (like your FastAPI server)

---

## Recommended Path Forward

### For Quickest Results (5 minutes):
**Use Option 1** - Let Agentic Studio create the agent for you
- No deployment needed
- No configuration needed
- Just describe what you want
- Platform handles everything

### For Custom Implementation (30 minutes):
**Use Option 2** - Deploy your FastAPI server and connect via REST/A2A
- Deploy to IBM Cloud Code Engine or use ngrok
- Select "REST/A2A" in MCP Servers
- Configure your endpoints
- Test the connection

### If You Already Have an Agent:
**Use Option 3** - Use your existing agent
- It's already deployed
- Just test it
- Extend it as needed

---

## Testing Your Agent

Once deployed (any option), test with these prompts:

**Test 1: Dockerfile**
```
Create a production-ready Dockerfile for Python FastAPI with multi-stage build
```

**Test 2: Kubernetes**
```
Generate Kubernetes deployment and service manifests for my-app in production
```

**Test 3: CI/CD**
```
Create a GitHub Actions pipeline with testing, security scanning, and deployment
```

**Test 4: Infrastructure**
```
Generate Terraform configuration for AWS EKS cluster with auto-scaling
```

**Test 5: Multi-Agent**
```
Create a complete DevOps setup including Dockerfile, K8s manifests, and CI/CD pipeline for a Node.js Express microservices application
```

---

## Troubleshooting

### Issue: Can't Find "Upload" Option
**Solution**: You don't upload MCP servers. Instead:
1. Select "REST/A2A" from existing servers
2. Configure your deployment URL
3. The system connects to your service

### Issue: REST/A2A Not Working
**Solution**: Make sure your service is:
1. Deployed and accessible
2. Has the correct endpoints (/agent/invoke, etc.)
3. Returns proper JSON responses
4. Has CORS enabled for Agentic Studio domain

### Issue: Agent Not Responding
**Solution**: Check:
1. Service is running (check health endpoint)
2. ICA credentials are correct in .env
3. Logs for errors
4. Network connectivity

---

## Summary

**The MCP Gateway UI is for:**
- Selecting pre-configured MCP server types (REST/A2A, etc.)
- Configuring connections to your deployed services
- Managing virtual servers and their tools/resources

**It's NOT for:**
- Uploading custom MCP server code
- Deploying new server implementations
- Direct file uploads

**To use your LangGraph agent:**
1. **Easiest**: Let Agentic Studio create it (Option 1)
2. **Custom**: Deploy your FastAPI server and connect via REST/A2A (Option 2)
3. **Existing**: Use the agent you already have (Option 3)

---

## Next Steps

1. ✅ Choose your deployment option (we recommend Option 1)
2. ✅ Follow the steps for your chosen option
3. ✅ Test your agent with sample prompts
4. ✅ Integrate with workflows and other agents
5. ✅ Monitor performance in observability dashboard

**Need help?** Contact support on Slack: #ica-procode-agents

---

**Your agent is ready to use!** 🎉

Choose the option that best fits your needs and follow the steps above.