# Agentic Studio UI Registration - Step-by-Step Guide

## Overview

This guide provides detailed instructions for registering your LangGraph multi-agent system with IBM Enterprise Advantage Agentic Studio through the web UI.

**Important**: Currently, agents must be registered through the Agentic Studio UI. The programmatic API registration is not yet available.

---

## Prerequisites

Before you begin:
- ✅ LangGraph agent is running locally or deployed
- ✅ Agent is accessible at a URL (e.g., `http://localhost:8000`)
- ✅ You have access to Agentic Studio
- ✅ You have your ICA credentials configured

---

## Step-by-Step Registration

### Step 1: Start Your Agent

```bash
cd langgraph-agent

# Make sure AUTO_REGISTRATION_ENABLED=false in .env
# (to avoid 404 errors from API registration attempts)

# Start the agent
python -m src.api.server
```

Verify the agent is running:
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Step 2: Access Agentic Studio

1. Open your browser and navigate to:
   ```
   https://agentstudio.servicesessentials.ibm.com
   ```

2. Log in with your IBM credentials

3. Select your workspace (e.g., "AgenticAIDevops")

### Step 3: Navigate to Your Application

1. Click on "Agentic App Home" in the breadcrumb
2. Find and click on your application: **"agentic_devops"**
3. Click on the **"Agents"** tab

You should see a page with:
- Search bar
- "Code Your Own Agent" button
- "Import Agent (A2A)" button  
- **"Create agent orchestration"** button (blue, on the right)

### Step 4: Create Agent Orchestration

1. Click the **"Create agent orchestration"** button (blue button on the right)

2. You'll see a dialog: **"Welcome to Agent Orchestration"**
   - "Let's start by selecting your platform and framework, then tell me what you'd like to build."

### Step 5: Select Platform and Framework

**Choose Your Platform:**
- Select: **IBM Consulting Advantage** (blue button)

**Choose Your Framework:**
- Select: **LangGraph** (blue button)

**Choose Your Model:**
- Select: **gpt-5.2** ✓ (blue button with checkmark)

**Choose Your Orchestration Pattern:**
- Select: **ReAct** ✓ (blue button with checkmark)
  - Description: "ReAct - Iteratively reasons and acts, allowing the agent to think, use tools, and refine responses dynamically. Ideal for complex problem-solving."

### Step 6: Describe Your Agent

In the text box at the bottom, enter:

```
Create a LangGraph ReAct multi-agent system for DevOps automation that helps teams design, evolve, and reason about production-ready Agentic DevOps workflows. 

The agent iteratively analyzes DevOps requirements, proposes agent roles and orchestration patterns, and refines designs based on user feedback.

Capabilities:
- DevOps automation (Docker, Kubernetes, CI/CD pipelines)
- Infrastructure as Code generation (Terraform)
- Code review and analysis
- Service orchestration and workflow management
- Multi-agent coordination with supervisor pattern

The system uses a supervisor agent to route requests to specialized agents (DevOps, Code Review, Orchestrator) and aggregates their responses.
```

Click the **send button** (arrow icon) or press Enter.

### Step 7: Configure Agent Details

The system will generate an agent configuration. Review and update:

**Agent Name:**
```
agentic-devops-langgraph-react
```

**Agent Description:**
```
LangGraph ReAct multi-agent system for DevOps automation, code review, and service orchestration. Iteratively analyzes DevOps workflows, proposes agent roles and orchestration patterns, and refines designs based on user feedback.
```

**Version:**
```
1.0.0
```

### Step 8: Configure Endpoints

**Important**: Update these with your actual deployment URL.

For local development:
```
Base URL: http://localhost:8000

Endpoints:
- Invoke: http://localhost:8000/agent/invoke
- Stream: http://localhost:8000/agent/stream  
- Status: http://localhost:8000/agent/status
- Health: http://localhost:8000/health
- A2A: http://localhost:8000/a2a/invoke
```

For production deployment:
```
Base URL: https://your-deployment-url.com

Endpoints:
- Invoke: https://your-deployment-url.com/agent/invoke
- Stream: https://your-deployment-url.com/agent/stream
- Status: https://your-deployment-url.com/agent/status
- Health: https://your-deployment-url.com/health
- A2A: https://your-deployment-url.com/a2a/invoke
```

### Step 9: Configure Integration

Based on your Agentic Studio configuration:

**MCP Gateway:**
- ✅ Enable: ICA Shared MCP Gateway
- URL: `https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007.us-south.containers.appdomain.cloud`
- Status: Active

**Workflow Orchestration:**
- ✅ Enable: AgentCore Orchestrator
- URL: `https://langflow.servicesessentials.ibm.com`
- Status: Active

**Observability:**
- ✅ Enable: Arize Phoenix
- URL: `https://observability.servicesessentials.ibm.com`
- Status: Active (monitoring only - managed by system)

### Step 10: Review and Save

1. Review all configuration details
2. Click **"Save"** or **"Create"** button
3. Wait for confirmation message

You should see your agent appear in the Agents list with:
- Name: agentic-devops-langgraph-react
- Version: 1.0.0
- Status: Success (green checkmark)
- Registry ID: e571f647-8fff-48d1-a6b5-5aea... (example)

---

## Step 11: Test Your Agent

### Test from Agentic Studio UI

1. Click on your registered agent in the list
2. You'll see a chat interface
3. Try these test prompts:

**Test 1: Dockerfile Generation**
```
Create a production-ready Dockerfile for a Python FastAPI application
```

**Test 2: Kubernetes Deployment**
```
Generate Kubernetes deployment and service manifests for my-app in production environment
```

**Test 3: CI/CD Pipeline**
```
Create a GitHub Actions CI/CD pipeline with testing, security scanning, and deployment stages
```

### Test via API

```bash
# Test direct API call
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Create a Dockerfile for Node.js Express application",
    "task_type": "devops",
    "environment": "production"
  }'
```

### Test A2A Protocol

```bash
# Test A2A JSON-RPC endpoint
curl -X POST http://localhost:8000/a2a/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "method": "agent.invoke",
    "params": {
      "task": "Generate Terraform configuration for AWS EKS cluster",
      "context": {
        "cloud_provider": "aws",
        "environment": "production"
      }
    },
    "id": "test-123"
  }'
```

---

## Verification Checklist

After registration, verify:

- [ ] Agent appears in Agentic Studio Agents list
- [ ] Status shows as "Success" (green)
- [ ] Agent responds to test prompts in UI
- [ ] Health endpoint is accessible
- [ ] Status endpoint returns agent info
- [ ] Invoke endpoint processes requests
- [ ] A2A endpoint accepts JSON-RPC calls
- [ ] Observability shows traces (if enabled)

---

## Troubleshooting

### Issue: Agent Not Appearing in List

**Possible Causes:**
- Registration didn't complete
- Wrong application selected
- Browser cache issue

**Solutions:**
1. Refresh the page (Ctrl+F5)
2. Verify you're in the correct application
3. Try registering again
4. Check browser console for errors

### Issue: Agent Status Shows Error

**Possible Causes:**
- Agent not running
- Endpoints not accessible
- Network connectivity issues

**Solutions:**
1. Verify agent is running: `curl http://localhost:8000/health`
2. Check agent logs for errors
3. Verify firewall/network settings
4. Update endpoint URLs if needed

### Issue: Test Prompts Don't Work

**Possible Causes:**
- Agent endpoints incorrect
- Agent not responding
- Configuration mismatch

**Solutions:**
1. Test endpoints directly with curl
2. Check agent logs for errors
3. Verify ICA credentials in .env
4. Restart the agent

### Issue: Can't Access from Agentic Studio

**Possible Causes:**
- Using localhost URL (not accessible from cloud)
- Firewall blocking external access
- Need public URL or tunnel

**Solutions:**

**For Development:**
Use a tunnel service like ngrok:
```bash
# Install ngrok
# Start tunnel
ngrok http 8000

# Use the ngrok URL in Agentic Studio
# Example: https://abc123.ngrok.io
```

**For Production:**
Deploy to a cloud service with public URL:
- AWS ECS/EKS
- Azure Container Instances
- Google Cloud Run
- IBM Cloud Code Engine

---

## Production Deployment

### Deploy to Cloud

**Option 1: Docker Container**
```bash
# Build image
docker build -t langgraph-agent:1.0.0 .

# Push to registry
docker tag langgraph-agent:1.0.0 your-registry/langgraph-agent:1.0.0
docker push your-registry/langgraph-agent:1.0.0

# Deploy to cloud service
# Update Agentic Studio with production URL
```

**Option 2: Kubernetes**
```bash
# Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Get external IP
kubectl get service langgraph-agent

# Update Agentic Studio with service URL
```

### Update Agent Configuration

After deployment:
1. Go to Agentic Studio
2. Find your agent
3. Click "Edit" or "Configure"
4. Update endpoint URLs to production URLs
5. Save changes
6. Test the updated configuration

---

## Best Practices

### Security
- ✅ Use HTTPS for production endpoints
- ✅ Implement API key authentication
- ✅ Use secrets management for credentials
- ✅ Enable CORS only for trusted origins
- ✅ Regular security updates

### Monitoring
- ✅ Enable observability (Arize Phoenix)
- ✅ Set up health check monitoring
- ✅ Configure alerting for failures
- ✅ Track token usage and costs
- ✅ Monitor response times

### Maintenance
- ✅ Regular agent updates
- ✅ Version control for configurations
- ✅ Backup agent metadata
- ✅ Document changes
- ✅ Test before production updates

---

## Next Steps

After successful registration:

1. ✅ Test all agent capabilities
2. ✅ Configure MCP tools and resources
3. ✅ Set up monitoring dashboards
4. ✅ Deploy to production environment
5. ✅ Train team on agent usage
6. ✅ Extend with additional agents
7. ✅ Integrate with existing workflows

---

## Support

**Documentation:**
- Architecture: `LANGGRAPH_AGENT_ARCHITECTURE.md`
- Quick Start: `LANGGRAPH_QUICK_START.md`
- Agent README: `langgraph-agent/README.md`

**Resources:**
- Agentic Studio: https://agentstudio.servicesessentials.ibm.com
- MCP Gateway: https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007...
- Observability: https://observability.servicesessentials.ibm.com

**Contact:**
- Slack: #ica-procode-agents
- Email: support@enterprise-advantage.ibm.com

---

**Your agent is now registered and ready to use in Agentic Studio!** 🎉