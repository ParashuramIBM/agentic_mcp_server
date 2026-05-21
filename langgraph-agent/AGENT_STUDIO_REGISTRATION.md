# Agent Studio Registration Guide

This guide explains how to register the LangGraph Multi-Agent System with IBM Enterprise Advantage Agentic Studio.

## Overview

Based on the Agentic Studio configuration, we need to register our agent with:
- **MCP Gateway**: ICA Shared MCP Gateway
- **Workflow Orchestration**: AgentCore Orchestrator
- **Observability**: Arize Phoenix

## Configuration Details from Agentic Studio

### MCP Gateway
- **Gateway Name**: ICA Shared MCP Gateway
- **URL**: `https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007.us-south.containers.appdomain.cloud`
- **Status**: ✅ Active
- **Access Token**: (Managed by ICA platform)

### Workflow Orchestration
- **Orchestrator Name**: AgentCore Orchestrator
- **URL**: `https://langflow.servicesessentials.ibm.com`
- **Status**: ✅ Active

### Observability
- **Provider**: Arize Phoenix
- **URL**: `https://observability.servicesessentials.ibm.com`
- **Status**: ✅ Active
- **Note**: For monitoring only - managed by system

## Step-by-Step Registration

### Step 1: Prepare Agent Metadata

Create a file `langgraph-agent/agent_metadata.json`:

```json
{
  "agent_name": "agentic-devops-langgraph",
  "agent_version": "1.0.0",
  "agent_description": "LangGraph ReAct multi-agent system for DevOps automation, code review, and service orchestration. Iteratively analyzes DevOps workflows, proposes agent roles and orchestration patterns, and refines designs based on user feedback.",
  "framework": "langgraph",
  "platform": "enterprise_advantage",
  "capabilities": [
    "devops_automation",
    "code_review",
    "service_orchestration",
    "multi_agent_coordination"
  ],
  "agents": [
    {
      "name": "supervisor",
      "type": "router",
      "description": "Routes requests to specialized agents"
    },
    {
      "name": "devops_agent",
      "type": "executor",
      "description": "Handles CI/CD, Docker, Kubernetes, infrastructure"
    },
    {
      "name": "code_review_agent",
      "type": "executor",
      "description": "Code analysis and security scanning"
    },
    {
      "name": "orchestrator_agent",
      "type": "executor",
      "description": "Microservices coordination and workflows"
    }
  ],
  "endpoints": {
    "invoke": "http://localhost:8000/agent/invoke",
    "stream": "http://localhost:8000/agent/stream",
    "status": "http://localhost:8000/agent/status",
    "capabilities": "http://localhost:8000/agent/capabilities",
    "a2a": "http://localhost:8000/a2a/invoke"
  },
  "integration": {
    "mcp_gateway": "ICA Shared MCP Gateway",
    "workflow_orchestrator": "AgentCore Orchestrator",
    "observability": "Arize Phoenix"
  }
}
```

### Step 2: Update Environment Configuration

Add these to your `.env` file:

```bash
# MCP Gateway Configuration
MCP_ENABLED=true
MCP_GATEWAY_NAME=ICA Shared MCP Gateway
MCP_GATEWAY_URL=https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007.us-south.containers.appdomain.cloud
MCP_ACCESS_TOKEN=your-mcp-access-token

# Workflow Orchestration
WORKFLOW_ORCHESTRATOR_NAME=AgentCore Orchestrator
WORKFLOW_ORCHESTRATOR_URL=https://langflow.servicesessentials.ibm.com

# Observability
OBSERVABILITY_PROVIDER=Arize Phoenix
OBSERVABILITY_URL=https://observability.servicesessentials.ibm.com
OBSERVABILITY_ENABLED=true

# Agent Registration
AGENT_REGISTRY_ID=e571f647-8fff-48d1-a6b5-5aea...
```

### Step 3: Register Agent via Agentic Studio UI

**Note**: Based on the current Agentic Studio implementation, agents must be registered through the UI. The programmatic API registration is not yet available.

#### Manual Registration via UI (Required)

1. **Navigate to Agentic Studio**:
   ```
   https://agentstudio.servicesessentials.ibm.com
   ```

2. **Go to Your Application**:
   - Click on "agentic_devops" application
   - Navigate to "Agents" tab

3. **Click "Create agent orchestration"** (Blue button on right)

4. **Fill in Agent Details**:
   - **Platform**: IBM Consulting Advantage
   - **Framework**: LangGraph
   - **Model**: gpt-5.2 (ICA)
   - **Orchestration Pattern**: ReAct

5. **Configure Agent**:
   ```
   Name: agentic-devops-langgraph-react
   Description: LangGraph ReAct single-agent that helps teams design, 
                evolve, and reason about a production-ready Agentic DevOps 
                Suite. The agent iteratively analyzes DevOps workflows, 
                proposes agent roles and orchestration patterns, and refines 
                designs based on user feedback.
   
   Version: 1.0.0
   ```

6. **Set Endpoints**:
   ```
   Invoke URL: http://your-deployment-url:8000/agent/invoke
   Stream URL: http://your-deployment-url:8000/agent/stream
   Status URL: http://your-deployment-url:8000/agent/status
   A2A URL: http://your-deployment-url:8000/a2a/invoke
   ```

7. **Configure Integration**:
   - ✅ Enable MCP Gateway: ICA Shared MCP Gateway
   - ✅ Enable Workflow Orchestration: AgentCore Orchestrator
   - ✅ Enable Observability: Arize Phoenix

8. **Save and Deploy**

#### Option B: Programmatic Registration (API)

Use the registration script (see Step 4 below).

### Step 4: Implement Auto-Registration

Create `langgraph-agent/src/integration/registration.py`:

```python
"""
Agent Registration with Agentic Studio
"""

import requests
import logging
from typing import Dict, Any, Optional
from src.config.settings import settings
import json

logger = logging.getLogger(__name__)


class AgenticStudioRegistration:
    """Handle agent registration with Agentic Studio"""
    
    def __init__(self):
        self.studio_url = settings.agentic_studio_url
        self.api_key = settings.ica_api_key
        self.organization_id = settings.ica_organization_id
        self.project_id = settings.ica_project_id
        
    def register_agent(self) -> Optional[str]:
        """
        Register agent with Agentic Studio.
        
        Returns:
            Agent registry ID if successful, None otherwise
        """
        try:
            # Prepare registration payload
            payload = {
                "name": settings.agent_name,
                "version": settings.agent_version,
                "description": settings.agent_description,
                "framework": "langgraph",
                "platform": "enterprise_advantage",
                "capabilities": settings.agent_capabilities,
                "endpoints": {
                    "invoke": f"http://{settings.agent_host}:{settings.agent_port}/agent/invoke",
                    "stream": f"http://{settings.agent_host}:{settings.agent_port}/agent/stream",
                    "status": f"http://{settings.agent_host}:{settings.agent_port}/agent/status",
                    "capabilities": f"http://{settings.agent_host}:{settings.agent_port}/agent/capabilities",
                    "a2a": f"http://{settings.agent_host}:{settings.agent_port}/a2a/invoke"
                },
                "integration": {
                    "mcp_gateway": "ICA Shared MCP Gateway",
                    "workflow_orchestrator": "AgentCore Orchestrator",
                    "observability": "Arize Phoenix"
                },
                "metadata": settings.agent_metadata
            }
            
            # Register with Agentic Studio
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Organization-ID": self.organization_id,
                "X-Project-ID": self.project_id
            }
            
            response = requests.post(
                f"{self.studio_url}/api/v1/agents/register",
                json=payload,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200 or response.status_code == 201:
                result = response.json()
                agent_id = result.get("agent_id") or result.get("id")
                logger.info(f"Agent registered successfully: {agent_id}")
                return agent_id
            else:
                logger.error(f"Registration failed: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"Error registering agent: {str(e)}")
            return None
    
    def send_heartbeat(self, agent_id: str) -> bool:
        """
        Send heartbeat to Agentic Studio.
        
        Args:
            agent_id: Agent registry ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            response = requests.post(
                f"{self.studio_url}/api/v1/agents/{agent_id}/heartbeat",
                json={"status": "healthy", "timestamp": "now"},
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error sending heartbeat: {str(e)}")
            return False
    
    def deregister_agent(self, agent_id: str) -> bool:
        """
        Deregister agent from Agentic Studio.
        
        Args:
            agent_id: Agent registry ID
        
        Returns:
            True if successful, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}"
            }
            
            response = requests.delete(
                f"{self.studio_url}/api/v1/agents/{agent_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200 or response.status_code == 204:
                logger.info(f"Agent deregistered successfully: {agent_id}")
                return True
            else:
                logger.error(f"Deregistration failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error deregistering agent: {str(e)}")
            return False


# Global registration instance
registration = AgenticStudioRegistration()
```

### Step 5: Update FastAPI Server for Auto-Registration

Update `langgraph-agent/src/api/server.py` startup event:

```python
from src.integration.registration import registration
import asyncio

# Global agent ID
agent_registry_id = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global agent_registry_id
    
    logger.info(f"Starting {settings.agent_name} v{settings.agent_version}")
    
    # Register with Agentic Studio
    if settings.auto_registration_enabled:
        logger.info("Registering with Agentic Studio...")
        agent_registry_id = registration.register_agent()
        
        if agent_registry_id:
            logger.info(f"Agent registered: {agent_registry_id}")
            
            # Start heartbeat task
            asyncio.create_task(heartbeat_task())
        else:
            logger.warning("Agent registration failed, continuing without registration")
    
    logger.info(f"Server ready on {settings.agent_host}:{settings.agent_port}")


async def heartbeat_task():
    """Send periodic heartbeats to Agentic Studio"""
    global agent_registry_id
    
    while True:
        await asyncio.sleep(settings.heartbeat_interval)
        
        if agent_registry_id:
            success = registration.send_heartbeat(agent_registry_id)
            if not success:
                logger.warning("Heartbeat failed")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global agent_registry_id
    
    logger.info(f"Shutting down {settings.agent_name}")
    
    # Deregister from Agentic Studio
    if settings.auto_registration_enabled and agent_registry_id:
        logger.info("Deregistering from Agentic Studio...")
        registration.deregister_agent(agent_registry_id)
```

### Step 6: Test Registration

1. **Start the agent**:
   ```bash
   cd langgraph-agent
   python -m src.api.server
   ```

2. **Check logs** for registration confirmation:
   ```
   INFO: Registering with Agentic Studio...
   INFO: Agent registered: e571f647-8fff-48d1-a6b5-5aea...
   INFO: Server ready on 0.0.0.0:8000
   ```

3. **Verify in Agentic Studio**:
   - Go to your application's Agents tab
   - You should see "agentic-devops-langgraph-react" listed
   - Status should show as "Success" (green)

### Step 7: Test Agent Integration

1. **Test from Agentic Studio UI**:
   - Click on your registered agent
   - Use the built-in chat interface
   - Try: "Create a Dockerfile for Python FastAPI"

2. **Test A2A Protocol**:
   ```bash
   curl -X POST http://localhost:8000/a2a/invoke \
     -H "Content-Type: application/json" \
     -d '{
       "jsonrpc": "2.0",
       "method": "agent.invoke",
       "params": {
         "task": "Generate Kubernetes deployment manifest",
         "context": {"environment": "production"}
       },
       "id": "test-123"
     }'
   ```

3. **Monitor in Observability**:
   - Go to: https://observability.servicesessentials.ibm.com
   - View traces and metrics for your agent

## Troubleshooting

### Issue: Registration Fails

**Check**:
1. ICA API key is valid
2. Organization ID and Project ID are correct
3. Network connectivity to Agentic Studio
4. Agent endpoints are accessible

**Solution**:
```bash
# Test API connectivity
curl -H "Authorization: Bearer $ICA_API_KEY" \
  https://agentstudio.servicesessentials.ibm.com/api/v1/health
```

### Issue: Agent Not Visible in Studio

**Check**:
1. Registration returned agent ID
2. Heartbeat is being sent
3. Agent status endpoint is responding

**Solution**:
```bash
# Check agent status
curl http://localhost:8000/agent/status
```

### Issue: MCP Gateway Connection Fails

**Check**:
1. MCP access token is configured
2. Gateway URL is correct
3. Network access to MCP Gateway

**Solution**: Contact admin to verify MCP Gateway access

## Next Steps

1. ✅ Register agent in Agentic Studio
2. ✅ Verify agent appears in Agents list
3. ✅ Test agent invocation from Studio UI
4. ✅ Monitor agent in Observability dashboard
5. ✅ Configure MCP tools and resources
6. ✅ Set up workflow orchestration
7. ✅ Deploy to production environment

## Resources

- **Agentic Studio**: https://agentstudio.servicesessentials.ibm.com
- **MCP Gateway**: https://ica-pr-us-south-global-83f075ec965da16d61cd1225fb631fe-0007.us-south.containers.appdomain.cloud
- **Workflow Orchestrator**: https://langflow.servicesessentials.ibm.com
- **Observability**: https://observability.servicesessentials.ibm.com

---

**Your LangGraph agent is now ready to be registered with Agentic Studio!** 🎉