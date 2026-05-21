# Agent Invocation Guide

## 🎉 Your Agent is Live!

Your LangGraph DevOps agent is now deployed and accessible via the A2A (Agent-to-Agent) protocol.

## 📍 Agent Endpoint

```
https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024
```

**Agent Details:**
- **Application ID**: `511cd8a4-2a9a-4247-b7a2-e9fcfbead831`
- **Agent ID**: `e571f647-8fff-48d1-a6b5-5aea1205e024`
- **Protocol**: A2A (Agent-to-Agent)
- **Authentication**: Bearer token (API key)

---

## 🔑 Authentication

### Step 1: Generate API Key

1. Go to Agentic Studio Settings page
2. Navigate to "API Keys" section
3. Click "Generate New API Key"
4. Copy the key (it will only be shown once!)
5. Store it securely

### Step 2: Set Environment Variable

```bash
export AGENTIC_STUDIO_API_KEY="your-api-key-here"
```

---

## 📡 Supported Methods

### 1. GET - Retrieve Agent Card (Discovery)

Get agent metadata and capabilities.

**Request:**
```bash
curl -X GET \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY"
```

**Response:**
```json
{
  "agent_id": "e571f647-8fff-48d1-a6b5-5aea1205e024",
  "name": "agentic-devops-architect-react",
  "version": "1.0.0",
  "description": "LangGraph ReAct multi-agent system for DevOps automation",
  "capabilities": [
    "devops_automation",
    "code_review",
    "service_orchestration",
    "multi_agent_coordination"
  ],
  "framework": "LangGraph",
  "model": "gpt-5.2-chat",
  "pattern": "ReAct",
  "status": "active"
}
```

### 2. POST - Send Message/Task to Agent

Send a task or message to the agent for processing.

**Request:**
```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a production-ready Dockerfile for Python FastAPI application",
    "context": {
      "environment": "production",
      "language": "python",
      "framework": "fastapi"
    }
  }'
```

**Response:**
```json
{
  "agent_id": "e571f647-8fff-48d1-a6b5-5aea1205e024",
  "request_id": "req-123456",
  "status": "completed",
  "response": {
    "message": "Here's a production-ready Dockerfile for Python FastAPI...",
    "artifacts": {
      "dockerfile": "FROM python:3.11-slim\n...",
      "docker_compose": "version: '3.8'\n..."
    },
    "confidence_score": 0.95
  },
  "metadata": {
    "processing_time_ms": 2500,
    "tokens_used": 1200,
    "model": "gpt-5.2-chat"
  }
}
```

---

## 🌊 Streaming Responses

For real-time streaming responses, use Server-Sent Events (SSE).

**Request:**
```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: text/event-stream" \
  -d '{
    "message": "Create Kubernetes manifests for my-app",
    "stream": true
  }'
```

**Response (SSE):**
```
data: {"type": "start", "request_id": "req-123456"}

data: {"type": "thinking", "content": "Analyzing requirements..."}

data: {"type": "tool_use", "tool": "devops_automation", "status": "running"}

data: {"type": "content", "content": "Creating deployment manifest..."}

data: {"type": "artifact", "name": "deployment.yaml", "content": "apiVersion: apps/v1\n..."}

data: {"type": "complete", "status": "success"}
```

---

## 💻 Code Examples

### Python

```python
import requests
import os

# Configuration
AGENT_URL = "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024"
API_KEY = os.getenv("AGENTIC_STUDIO_API_KEY")

# Headers
headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 1. Get agent card
response = requests.get(AGENT_URL, headers=headers)
agent_card = response.json()
print(f"Agent: {agent_card['name']}")
print(f"Capabilities: {agent_card['capabilities']}")

# 2. Send a task
payload = {
    "message": "Create a Dockerfile for Python FastAPI",
    "context": {
        "environment": "production",
        "language": "python",
        "framework": "fastapi"
    }
}

response = requests.post(AGENT_URL, headers=headers, json=payload)
result = response.json()

print(f"Status: {result['status']}")
print(f"Response: {result['response']['message']}")
print(f"Artifacts: {result['response']['artifacts'].keys()}")

# 3. Stream responses
headers["Accept"] = "text/event-stream"
payload["stream"] = True

response = requests.post(AGENT_URL, headers=headers, json=payload, stream=True)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = json.loads(line[6:])
            print(f"Event: {data['type']}")
            if 'content' in data:
                print(f"Content: {data['content']}")
```

### JavaScript/Node.js

```javascript
const axios = require('axios');

const AGENT_URL = 'https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024';
const API_KEY = process.env.AGENTIC_STUDIO_API_KEY;

const headers = {
  'Authorization': `Bearer ${API_KEY}`,
  'Content-Type': 'application/json'
};

// 1. Get agent card
async function getAgentCard() {
  const response = await axios.get(AGENT_URL, { headers });
  console.log('Agent:', response.data.name);
  console.log('Capabilities:', response.data.capabilities);
  return response.data;
}

// 2. Send a task
async function sendTask(message, context = {}) {
  const payload = { message, context };
  const response = await axios.post(AGENT_URL, payload, { headers });
  
  console.log('Status:', response.data.status);
  console.log('Response:', response.data.response.message);
  console.log('Artifacts:', Object.keys(response.data.response.artifacts));
  
  return response.data;
}

// 3. Stream responses
async function streamTask(message, context = {}) {
  const payload = { message, context, stream: true };
  const streamHeaders = {
    ...headers,
    'Accept': 'text/event-stream'
  };
  
  const response = await axios.post(AGENT_URL, payload, {
    headers: streamHeaders,
    responseType: 'stream'
  });
  
  response.data.on('data', (chunk) => {
    const lines = chunk.toString().split('\n');
    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = JSON.parse(line.substring(6));
        console.log('Event:', data.type);
        if (data.content) {
          console.log('Content:', data.content);
        }
      }
    }
  });
}

// Usage
(async () => {
  await getAgentCard();
  
  await sendTask('Create a Dockerfile for Python FastAPI', {
    environment: 'production',
    language: 'python',
    framework: 'fastapi'
  });
  
  await streamTask('Generate Kubernetes manifests for my-app');
})();
```

### cURL Examples

**Example 1: Create Dockerfile**
```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a production-ready Dockerfile for Python FastAPI application with multi-stage build",
    "context": {
      "environment": "production",
      "language": "python",
      "framework": "fastapi",
      "features": ["multi-stage", "security-hardened", "minimal-size"]
    }
  }'
```

**Example 2: Generate Kubernetes Manifests**
```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Generate Kubernetes deployment and service manifests for my-app in production environment",
    "context": {
      "app_name": "my-app",
      "environment": "production",
      "replicas": 3,
      "port": 8000
    }
  }'
```

**Example 3: Create CI/CD Pipeline**
```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a GitHub Actions CI/CD pipeline with testing, security scanning, and deployment to production",
    "context": {
      "provider": "github",
      "language": "python",
      "stages": ["test", "security-scan", "build", "deploy"]
    }
  }'
```

**Example 4: Multi-Agent Task**
```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a complete DevOps setup including Dockerfile, Kubernetes manifests, and CI/CD pipeline for a Node.js Express microservices application",
    "context": {
      "architecture": "microservices",
      "language": "nodejs",
      "framework": "express",
      "services": ["api-gateway", "auth-service", "user-service"],
      "cloud": "aws"
    }
  }'
```

---

## 🧪 Testing in Sandbox

Agentic Studio provides an interactive sandbox for testing your agent.

**Access Sandbox:**
```
https://servicesessentials.ibm.com/agenticapps/sandbox?agent=e571f647-8fff-48d1-a6b5-5aea1205e024
```

**Features:**
- Interactive chat interface
- Real-time response streaming
- View artifacts and outputs
- Test different prompts
- Monitor performance metrics

---

## 🔗 Integration Patterns

### 1. Direct Integration

Call the agent directly from your application:

```python
def create_dockerfile(language, framework):
    response = requests.post(
        AGENT_URL,
        headers=headers,
        json={
            "message": f"Create Dockerfile for {language} {framework}",
            "context": {"language": language, "framework": framework}
        }
    )
    return response.json()["response"]["artifacts"]["dockerfile"]
```

### 2. Workflow Integration

Integrate with other agents in a workflow:

```python
# Step 1: Use DevOps agent to create Dockerfile
dockerfile_response = requests.post(devops_agent_url, ...)

# Step 2: Use Code Review agent to review the Dockerfile
review_response = requests.post(code_review_agent_url, {
    "message": "Review this Dockerfile",
    "context": {"code": dockerfile_response["artifacts"]["dockerfile"]}
})

# Step 3: Use Orchestrator agent to deploy
deploy_response = requests.post(orchestrator_agent_url, ...)
```

### 3. Event-Driven Integration

Use webhooks for asynchronous processing:

```python
# Register webhook
webhook_config = {
    "url": "https://your-app.com/webhook",
    "events": ["task_completed", "task_failed"]
}

# Send task with webhook
response = requests.post(AGENT_URL, {
    "message": "Create Kubernetes manifests",
    "webhook": webhook_config
})

# Your webhook endpoint receives:
# POST https://your-app.com/webhook
# {
#   "event": "task_completed",
#   "agent_id": "e571f647-8fff-48d1-a6b5-5aea1205e024",
#   "request_id": "req-123456",
#   "result": {...}
# }
```

---

## 📊 Response Format

### Success Response

```json
{
  "agent_id": "e571f647-8fff-48d1-a6b5-5aea1205e024",
  "request_id": "req-123456",
  "status": "completed",
  "response": {
    "message": "Generated Dockerfile successfully",
    "artifacts": {
      "dockerfile": "FROM python:3.11-slim\n...",
      "docker_compose": "version: '3.8'\n...",
      "readme": "# Docker Setup\n..."
    },
    "confidence_score": 0.95,
    "agents_involved": ["supervisor", "devops_agent"],
    "tools_used": ["create_dockerfile", "generate_docker_compose"]
  },
  "metadata": {
    "processing_time_ms": 2500,
    "tokens_used": 1200,
    "model": "gpt-5.2-chat",
    "timestamp": "2026-05-19T20:00:00Z"
  }
}
```

### Error Response

```json
{
  "agent_id": "e571f647-8fff-48d1-a6b5-5aea1205e024",
  "request_id": "req-123456",
  "status": "failed",
  "error": {
    "code": "INVALID_INPUT",
    "message": "Missing required context parameter: language",
    "details": {
      "required": ["language", "framework"],
      "provided": ["framework"]
    }
  },
  "metadata": {
    "timestamp": "2026-05-19T20:00:00Z"
  }
}
```

---

## 🔍 Monitoring and Observability

### View Execution Traces

Access Arize Phoenix observability dashboard:
```
https://observability.servicesessentials.ibm.com
```

**Metrics Available:**
- Request count and rate
- Response times (p50, p95, p99)
- Error rates
- Token usage
- Agent routing decisions
- Tool execution times

### Query Execution History

```bash
curl -X GET \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024/history" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY"
```

---

## 🛡️ Best Practices

### Security
- ✅ Store API keys securely (use environment variables or secrets manager)
- ✅ Rotate API keys regularly
- ✅ Use HTTPS only
- ✅ Implement rate limiting in your application
- ✅ Validate responses before using artifacts

### Performance
- ✅ Use streaming for long-running tasks
- ✅ Implement caching for repeated requests
- ✅ Set appropriate timeouts
- ✅ Handle retries with exponential backoff
- ✅ Monitor token usage

### Error Handling
- ✅ Check response status before processing
- ✅ Handle network errors gracefully
- ✅ Log errors for debugging
- ✅ Provide fallback mechanisms
- ✅ Validate artifacts before deployment

---

## 📞 Support

**Documentation:**
- Agent Studio: https://agentstudio.servicesessentials.ibm.com
- API Reference: https://docs.servicesessentials.ibm.com/api

**Contact:**
- Slack: #ica-procode-agents
- Email: support@enterprise-advantage.ibm.com

---

## 🎉 Your Agent is Ready!

You can now invoke your LangGraph DevOps agent from any application using the A2A endpoint.

**Quick Test:**
```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"message": "Create a Dockerfile for Python FastAPI"}'
```

**Happy automating!** 🚀