# LangGraph Multi-Agent System

A comprehensive multi-agent system built with LangGraph that integrates with IBM Enterprise Advantage platform for DevOps automation, code review, and service orchestration.

## 🎯 Overview

This project implements a sophisticated multi-agent system using LangGraph that combines:

- **DevOps Automation**: CI/CD pipelines, Docker, Kubernetes, infrastructure provisioning
- **Code Review & Analysis**: Code quality, security scanning, best practices
- **Service Orchestration**: Microservices coordination, workflow management

### Key Features

✅ **Multi-Agent Architecture**: Supervisor agent coordinates specialized agents
✅ **Enterprise Advantage Integration**: A2A protocol, auto-registration, OTEL instrumentation
✅ **ICA LLM Gateway**: Access to enterprise AI models
✅ **Production-Ready**: FastAPI server, error handling, logging

## 📚 Documentation

- 📘 **[UI Registration Guide](UI_REGISTRATION_GUIDE.md)** - Step-by-step guide for registering your agent in Agentic Studio
- 📗 **[Quick Start Guide](../LANGGRAPH_QUICK_START.md)** - 30-minute setup guide
- 📕 **[Architecture Document](../LANGGRAPH_AGENT_ARCHITECTURE.md)** - Complete system architecture
- 📙 **[MCP Deployment Guide](MCP_DEPLOYMENT_GUIDE.md)** - Deploy as MCP server to IBM Context Forge
- 📙 **[Implementation Plan](../LANGGRAPH_IMPLEMENTATION_PLAN.md)** - Development roadmap
- 📓 **[Agent Studio Registration](AGENT_STUDIO_REGISTRATION.md)** - Registration details and troubleshooting
✅ **Extensible**: Easy to add new agents and tools

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│     Enterprise Advantage Platform       │
│  (Agentic Studio, LLM Gateway, OTEL)   │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│      LangGraph Multi-Agent System       │
├─────────────────────────────────────────┤
│  ┌──────────────┐                       │
│  │  Supervisor  │ ← Routes requests     │
│  └──────────────┘                       │
│         ↓                                │
│  ┌──────────────┬──────────────┬───────┐│
│  │DevOps Agent  │Review Agent  │Orch.  ││
│  └──────────────┴──────────────┴───────┘│
│                                          │
│  FastAPI Server (A2A Protocol)          │
└─────────────────────────────────────────┘
```

## 📋 Prerequisites

- Python 3.11 or higher
- IBM Enterprise Advantage account with API credentials
- Git
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
# Navigate to the langgraph-agent directory
cd langgraph-agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy environment template
cp .env.template .env

# Edit .env and add your ICA credentials
# Required variables:
# - ICA_API_KEY
# - ICA_ORGANIZATION_ID
# - ICA_PROJECT_ID
```

### 3. Run the Agent

```bash
# Start the FastAPI server
python -m src.api.server

# Or use uvicorn directly
uvicorn src.api.server:app --host 0.0.0.0 --port 8000 --reload
```

### 4. Test the Agent

```bash
# Health check
curl http://localhost:8000/health

# Get agent status
curl http://localhost:8000/agent/status

# Invoke agent
curl -X POST http://localhost:8000/agent/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Create a Dockerfile for a Python FastAPI application",
    "task_type": "devops",
    "environment": "dev"
  }'
```

## 📁 Project Structure

```
langgraph-agent/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── supervisor.py    # Supervisor/Router agent
│   │   ├── devops_agent.py  # DevOps automation
│   │   ├── code_review_agent.py (TODO)
│   │   └── orchestrator_agent.py (TODO)
│   ├── graph/               # LangGraph workflow
│   │   ├── state.py         # State definitions
│   │   └── workflow.py      # Graph workflow
│   ├── tools/               # Agent tools
│   │   ├── devops_tools.py  # DevOps tools
│   │   ├── analysis_tools.py (TODO)
│   │   └── orchestration_tools.py (TODO)
│   ├── integration/         # Enterprise Advantage integration
│   │   ├── a2a_protocol.py (TODO)
│   │   ├── registration.py (TODO)
│   │   ├── otel_instrumentation.py (TODO)
│   │   └── ica_integration.py (TODO)
│   ├── api/                 # FastAPI server
│   │   └── server.py        # REST API endpoints
│   └── config/              # Configuration
│       └── settings.py      # Settings management
├── tests/                   # Test suite (TODO)
├── docs/                    # Documentation
├── .env.template           # Environment template
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Key configuration variables in `.env`:

```bash
# ICA Credentials (Required)
ICA_API_KEY=your-api-key
ICA_ORGANIZATION_ID=your-org-id
ICA_PROJECT_ID=your-project-id

# Agent Configuration
AGENT_NAME=agentic-devops-langgraph
AGENT_PORT=8000

# Model Configuration
DEFAULT_MODEL=gpt-5.2-chat
MODEL_TEMPERATURE=0.7

# Features
OTEL_ENABLED=false
MCP_ENABLED=false
AUTO_REGISTRATION_ENABLED=true
```

See `.env.template` for all available options.

## 📡 API Endpoints

### Health & Status

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /agent/status` - Agent status
- `GET /agent/capabilities` - Agent capabilities

### Agent Invocation

- `POST /agent/invoke` - Synchronous invocation
- `POST /agent/stream` - Streaming invocation

### A2A Protocol

- `POST /a2a/invoke` - JSON-RPC 2.0 endpoint

### API Documentation

- `/docs` - Swagger UI
- `/redoc` - ReDoc documentation

## 🎯 Usage Examples

### Example 1: Create Dockerfile

```python
import requests

response = requests.post(
    "http://localhost:8000/agent/invoke",
    json={
        "user_input": "Create a production-ready Dockerfile for a Python FastAPI application",
        "task_type": "devops",
        "environment": "production"
    }
)

result = response.json()
print(result["final_output"])
```

### Example 2: Generate Kubernetes Manifests

```python
response = requests.post(
    "http://localhost:8000/agent/invoke",
    json={
        "user_input": "Generate Kubernetes deployment and service manifests for my-app",
        "task_type": "devops",
        "environment": "staging",
        "metadata": {
            "app_name": "my-app",
            "replicas": 3
        }
    }
)
```

### Example 3: Create CI/CD Pipeline

```python
response = requests.post(
    "http://localhost:8000/agent/invoke",
    json={
        "user_input": "Create a GitHub Actions CI/CD pipeline with testing and deployment",
        "task_type": "devops",
        "repository": "https://github.com/org/repo"
    }
)
```

### Example 4: A2A Protocol (JSON-RPC)

```python
response = requests.post(
    "http://localhost:8000/a2a/invoke",
    json={
        "jsonrpc": "2.0",
        "method": "agent.invoke",
        "params": {
            "task": "Create a Dockerfile for Node.js",
            "context": {
                "task_type": "devops",
                "environment": "dev"
            }
        },
        "id": "req-123"
    }
)
```

## 🧪 Testing

```bash
# Run tests (TODO: Implement tests)
pytest tests/

# Run with coverage
pytest --cov=src tests/

# Run specific test
pytest tests/test_agents.py::test_supervisor_routing
```

## 🐳 Docker Deployment

### Build Image

```bash
docker build -t langgraph-agent:1.0.0 .
```

### Run Container

```bash
docker run -d \
  --name langgraph-agent \
  -p 8000:8000 \
  --env-file .env \
  langgraph-agent:1.0.0
```

### Docker Compose

```bash
docker-compose up -d
```

## ☸️ Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace langgraph-agent

# Create secret with ICA credentials
kubectl create secret generic ica-credentials \
  --from-literal=api-key=your-api-key \
  --namespace langgraph-agent

# Apply manifests
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## 🔍 Monitoring & Observability

### OpenTelemetry (OTEL)

Enable OTEL instrumentation in `.env`:

```bash
OTEL_ENABLED=true
OTEL_EXPORTER_OTLP_ENDPOINT=https://otel-collector:4317
```

### Logs

```bash
# View logs
tail -f logs/agent.log

# Docker logs
docker logs -f langgraph-agent

# Kubernetes logs
kubectl logs -f deployment/langgraph-agent -n langgraph-agent
```

## 🛠️ Development

### Adding a New Agent

1. Create agent file in `src/agents/`
2. Implement agent class with `execute()` method
3. Add agent node to `src/graph/workflow.py`
4. Update routing logic in supervisor
5. Add tests

### Adding New Tools

1. Create tool file in `src/tools/`
2. Implement tool methods
3. Import and use in agent
4. Add tests

### Code Style

```bash
# Format code
black src/

# Sort imports
isort src/

# Type checking
mypy src/
```

## 📚 Documentation

- [Architecture Document](../LANGGRAPH_AGENT_ARCHITECTURE.md)
- [Implementation Plan](../LANGGRAPH_IMPLEMENTATION_PLAN.md)
- [Quick Start Guide](../LANGGRAPH_QUICK_START.md)
- [Project Summary](../LANGGRAPH_PROJECT_SUMMARY.md)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📝 TODO

- [ ] Implement Code Review Agent
- [ ] Implement Orchestrator Agent
- [ ] Add comprehensive test suite
- [ ] Implement OTEL instrumentation
- [ ] Add auto-registration with Agentic Studio
- [ ] Implement MCP Gateway integration
- [ ] Add more DevOps tools
- [ ] Create Helm charts
- [ ] Add performance benchmarks
- [ ] Implement caching layer

## 🐛 Troubleshooting

### Issue: Import errors

**Solution**: Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: ICA API errors

**Solution**: Verify your ICA credentials in `.env`:
- Check `ICA_API_KEY` is correct
- Verify `ICA_ORGANIZATION_ID` and `ICA_PROJECT_ID`
- Ensure API base URL is correct

### Issue: Port already in use

**Solution**: Change port in `.env` or kill existing process:
```bash
# Change port
AGENT_PORT=8001

# Or kill process (Linux/Mac)
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## 📞 Support

- **Documentation**: See docs/ directory
- **Issues**: GitHub Issues
- **Slack**: #ica-procode-agents
- **Email**: support@enterprise-advantage.ibm.com

## 📄 License

This project is part of the Agentic DevOps platform. See LICENSE for details.

## 🙏 Acknowledgments

- IBM Enterprise Advantage team
- LangChain/LangGraph community
- FastAPI framework
- All contributors

---

**Version**: 1.0.0  
**Last Updated**: 2026-05-19  
**Status**: Development 🚧