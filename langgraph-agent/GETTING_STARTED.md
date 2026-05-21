# Getting Started with Your LangGraph DevOps Agent

Welcome! Your LangGraph DevOps Agent is deployed and ready to use. This guide will help you get started quickly.

## 🎯 What You Have

Your agent is live at:
```
https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024
```

**Agent Details:**
- **Name**: agentic-devops-architect-react
- **Version**: 1.0.0
- **Framework**: LangGraph
- **Model**: gpt-5.2-chat
- **Pattern**: ReAct (Reasoning + Acting)

**Capabilities:**
- ✅ DevOps automation (Docker, Kubernetes, CI/CD)
- ✅ Code review and analysis
- ✅ Service orchestration
- ✅ Multi-agent coordination

## 🚀 Quick Start (5 Minutes)

### Step 1: Get Your API Key

1. Visit [Agentic Studio Settings](https://agentstudio.servicesessentials.ibm.com/settings)
2. Navigate to "API Keys" section
3. Click "Generate New API Key"
4. Copy the key (shown only once!)

### Step 2: Set Environment Variable

```bash
export AGENTIC_STUDIO_API_KEY="your-api-key-here"
```

### Step 3: Install Dependencies

```bash
cd langgraph-agent/examples
pip install -r requirements.txt
```

### Step 4: Run Quick Start

```bash
python quick_start.py
```

This will test your agent with 5 different requests and show you the results!

## 📚 What's Next?

### Option 1: Use the Python Client (Recommended)

The easiest way to use your agent:

```python
from examples.agent_client import AgentClient

# Initialize
client = AgentClient()

# Create a Dockerfile
result = client.create_dockerfile("python", "fastapi")
print(result.artifacts["dockerfile"])

# Create Kubernetes manifests
result = client.create_kubernetes_manifests("my-app")
print(result.artifacts["deployment.yaml"])

# Create CI/CD pipeline
result = client.create_cicd_pipeline("github", "python")
print(result.artifacts["github_actions.yaml"])
```

### Option 2: Use Direct HTTP Calls

```bash
curl -X POST \
  "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024" \
  -H "Authorization: Bearer $AGENTIC_STUDIO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Create a Dockerfile for Python FastAPI",
    "context": {
      "environment": "production",
      "language": "python",
      "framework": "fastapi"
    }
  }'
```

### Option 3: Create Your Own Agent

Build a custom agent that uses this agent as a backend:

```python
from examples.agent_client import AgentClient

class MyCustomAgent:
    def __init__(self):
        self.client = AgentClient()
    
    def setup_project(self, project_name, language, framework):
        # Use the DevOps agent to generate files
        dockerfile = self.client.create_dockerfile(language, framework)
        k8s = self.client.create_kubernetes_manifests(project_name)
        cicd = self.client.create_cicd_pipeline("github", language)
        
        # Add your custom logic here
        return {
            "dockerfile": dockerfile.artifacts,
            "k8s": k8s.artifacts,
            "cicd": cicd.artifacts
        }
```

## 📖 Documentation

| Document | Description |
|----------|-------------|
| **[AGENT_INVOCATION_GUIDE.md](AGENT_INVOCATION_GUIDE.md)** | Complete API reference with examples |
| **[CREATE_NEW_AGENT_GUIDE.md](CREATE_NEW_AGENT_GUIDE.md)** | How to create new agents from this context |
| **[examples/README.md](examples/README.md)** | Usage examples and patterns |
| **[examples/agent_client.py](examples/agent_client.py)** | Python client library source |
| **[examples/quick_start.py](examples/quick_start.py)** | Quick start test script |

## 🎯 Common Use Cases

### 1. Generate Dockerfile

```python
client = AgentClient()
result = client.create_dockerfile(
    language="python",
    framework="fastapi",
    environment="production",
    features=["multi-stage", "security-hardened"]
)
```

### 2. Generate Kubernetes Manifests

```python
result = client.create_kubernetes_manifests(
    app_name="my-app",
    environment="production",
    replicas=3,
    port=8000
)
```

### 3. Create CI/CD Pipeline

```python
result = client.create_cicd_pipeline(
    provider="github",
    language="python",
    stages=["test", "security-scan", "build", "deploy"]
)
```

### 4. Complete DevOps Setup

```python
result = client.create_complete_devops_setup(
    architecture="microservices",
    language="nodejs",
    framework="express",
    services=["api-gateway", "auth-service", "user-service"],
    cloud="aws"
)
```

## 🧪 Test in Sandbox

Try your agent interactively in the Agentic Studio Sandbox:

```
https://servicesessentials.ibm.com/agenticapps/sandbox?agent=e571f647-8fff-48d1-a6b5-5aea1205e024
```

Features:
- Interactive chat interface
- Real-time response streaming
- View artifacts and outputs
- Test different prompts
- Monitor performance metrics

## 🔍 Monitoring

View execution traces and metrics:

```
https://observability.servicesessentials.ibm.com
```

Available metrics:
- Request count and rate
- Response times (p50, p95, p99)
- Error rates
- Token usage
- Agent routing decisions
- Tool execution times

## 💡 Tips & Best Practices

1. **Check Confidence Scores**: Use `result.confidence_score` to determine if you need human review
2. **Handle Errors**: Always check `result.error` before using artifacts
3. **Use Streaming**: For long-running tasks, use `client.invoke_streaming()`
4. **Cache Results**: Implement caching for repeated requests
5. **Validate Artifacts**: Always validate generated files before deployment

## 🛠️ Troubleshooting

### Issue: "Authentication failed"
**Solution**: Check your API key is correct and not expired

### Issue: "Rate limit exceeded"
**Solution**: Implement exponential backoff and retry logic

### Issue: "Connection timeout"
**Solution**: Increase timeout or check network connectivity

### Issue: "Low confidence score"
**Solution**: Provide more context in your request or review output manually

## 📞 Support

- **Documentation**: See docs in this repository
- **API Reference**: https://docs.servicesessentials.ibm.com/api
- **Slack**: #ica-procode-agents
- **Email**: support@enterprise-advantage.ibm.com

## 🎉 You're Ready!

Your agent is deployed and ready to use. Here's what to do next:

1. ✅ Run `python examples/quick_start.py` to test your setup
2. ✅ Read [CREATE_NEW_AGENT_GUIDE.md](CREATE_NEW_AGENT_GUIDE.md) to build custom agents
3. ✅ Explore [examples/README.md](examples/README.md) for more patterns
4. ✅ Try the [Sandbox](https://servicesessentials.ibm.com/agenticapps/sandbox?agent=e571f647-8fff-48d1-a6b5-5aea1205e024)

**Happy automating!** 🚀

---

**Need Help?** Check the documentation or reach out on Slack (#ica-procode-agents)