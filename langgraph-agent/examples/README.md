# Agent Client Examples

This directory contains examples and utilities for invoking the deployed LangGraph DevOps Agent.

## 📁 Files

- **`agent_client.py`** - Python client library for invoking the agent via A2A protocol
- **`ica_agent_example.py`** - Example using ICA integration (existing)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install requests
```

### 2. Set API Key

```bash
export AGENTIC_STUDIO_API_KEY="your-api-key-here"
```

Get your API key from: https://agentstudio.servicesessentials.ibm.com/settings

### 3. Run Examples

```bash
# Run the agent client examples
python agent_client.py

# Or use it as a library
python -c "from agent_client import AgentClient; client = AgentClient(); print(client.get_agent_card())"
```

## 📚 Usage Examples

### Basic Usage

```python
from agent_client import AgentClient

# Initialize client
client = AgentClient()

# Get agent information
card = client.get_agent_card()
print(f"Agent: {card['name']}")
print(f"Capabilities: {card['capabilities']}")

# Invoke agent
result = client.invoke(
    message="Create a Dockerfile for Python FastAPI",
    context={
        "environment": "production",
        "language": "python",
        "framework": "fastapi"
    }
)

print(f"Status: {result.status}")
print(f"Output: {result.message}")
print(f"Artifacts: {result.artifacts.keys()}")
```

### Create Dockerfile

```python
result = client.create_dockerfile(
    language="python",
    framework="fastapi",
    environment="production",
    features=["multi-stage", "security-hardened", "minimal-size"]
)

# Access the generated Dockerfile
dockerfile_content = result.artifacts.get("dockerfile")
print(dockerfile_content)
```

### Generate Kubernetes Manifests

```python
result = client.create_kubernetes_manifests(
    app_name="my-app",
    environment="production",
    replicas=3,
    port=8000
)

# Access manifests
deployment = result.artifacts.get("deployment.yaml")
service = result.artifacts.get("service.yaml")
```

### Create CI/CD Pipeline

```python
result = client.create_cicd_pipeline(
    provider="github",
    language="python",
    stages=["test", "security-scan", "build", "deploy"]
)

# Access pipeline configuration
pipeline = result.artifacts.get("github_actions.yaml")
```

### Complete DevOps Setup

```python
result = client.create_complete_devops_setup(
    architecture="microservices",
    language="nodejs",
    framework="express",
    services=["api-gateway", "auth-service", "user-service"],
    cloud="aws"
)

# Access all artifacts
for name, content in result.artifacts.items():
    print(f"Generated: {name}")
```

### Streaming Responses

```python
# Stream responses for long-running tasks
for event in client.invoke_streaming(
    message="Create complete DevOps setup",
    context={"architecture": "microservices"}
):
    print(f"Event: {event['type']}")
    if 'content' in event:
        print(f"Content: {event['content']}")
```

## 🔧 Advanced Usage

### Custom Agent URL

```python
# Use a different agent endpoint
client = AgentClient(
    api_key="your-api-key",
    agent_url="https://your-custom-agent-url"
)
```

### Error Handling

```python
try:
    result = client.create_dockerfile("python", "fastapi")
    if result.error:
        print(f"Agent error: {result.error}")
    else:
        print(f"Success: {result.message}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except Exception as e:
    print(f"Error: {e}")
```

### Using Response Metadata

```python
result = client.invoke("Create a Dockerfile")

# Access metadata
print(f"Request ID: {result.request_id}")
print(f"Confidence: {result.confidence_score}")
print(f"Processing time: {result.metadata.get('processing_time_ms')}ms")
print(f"Tokens used: {result.metadata.get('tokens_used')}")
print(f"Model: {result.metadata.get('model')}")
```

## 🎯 Use Cases

### 1. Automated DevOps Workflows

```python
def setup_new_project(project_name, language, framework):
    """Automate complete project setup"""
    client = AgentClient()
    
    # Create Dockerfile
    dockerfile_result = client.create_dockerfile(language, framework)
    
    # Create Kubernetes manifests
    k8s_result = client.create_kubernetes_manifests(
        app_name=project_name,
        environment="production"
    )
    
    # Create CI/CD pipeline
    cicd_result = client.create_cicd_pipeline(
        provider="github",
        language=language
    )
    
    return {
        "dockerfile": dockerfile_result.artifacts.get("dockerfile"),
        "k8s_manifests": k8s_result.artifacts,
        "cicd_pipeline": cicd_result.artifacts
    }
```

### 2. Integration with Existing Tools

```python
def integrate_with_git_repo(repo_path):
    """Add DevOps files to existing repository"""
    import os
    
    client = AgentClient()
    
    # Detect language and framework
    # (simplified - you'd implement proper detection)
    language = "python"
    framework = "fastapi"
    
    # Generate files
    result = client.create_complete_devops_setup(
        architecture="monolith",
        language=language,
        framework=framework,
        services=[os.path.basename(repo_path)]
    )
    
    # Write files to repository
    for filename, content in result.artifacts.items():
        filepath = os.path.join(repo_path, filename)
        with open(filepath, 'w') as f:
            f.write(content)
    
    print(f"Added {len(result.artifacts)} DevOps files to {repo_path}")
```

### 3. Multi-Agent Orchestration

```python
def orchestrate_deployment(app_config):
    """Orchestrate deployment using multiple agent calls"""
    client = AgentClient()
    
    # Step 1: Create infrastructure
    infra_result = client.invoke(
        message="Create infrastructure as code",
        context=app_config
    )
    
    # Step 2: Create deployment configs
    deploy_result = client.create_kubernetes_manifests(
        app_name=app_config["app_name"],
        environment=app_config["environment"]
    )
    
    # Step 3: Create monitoring setup
    monitor_result = client.invoke(
        message="Create monitoring and alerting configuration",
        context={"app_name": app_config["app_name"]}
    )
    
    return {
        "infrastructure": infra_result.artifacts,
        "deployment": deploy_result.artifacts,
        "monitoring": monitor_result.artifacts
    }
```

## 🔗 Integration Patterns

### REST API Integration

```python
from flask import Flask, request, jsonify
from agent_client import AgentClient

app = Flask(__name__)
client = AgentClient()

@app.route('/api/generate-dockerfile', methods=['POST'])
def generate_dockerfile():
    data = request.json
    result = client.create_dockerfile(
        language=data['language'],
        framework=data['framework']
    )
    return jsonify({
        "dockerfile": result.artifacts.get("dockerfile"),
        "confidence": result.confidence_score
    })

if __name__ == '__main__':
    app.run(port=5000)
```

### CLI Tool

```python
import click
from agent_client import AgentClient

@click.group()
def cli():
    """DevOps Agent CLI"""
    pass

@cli.command()
@click.option('--language', required=True)
@click.option('--framework', required=True)
def dockerfile(language, framework):
    """Generate Dockerfile"""
    client = AgentClient()
    result = client.create_dockerfile(language, framework)
    click.echo(result.artifacts.get("dockerfile"))

@cli.command()
@click.option('--app-name', required=True)
def k8s(app_name):
    """Generate Kubernetes manifests"""
    client = AgentClient()
    result = client.create_kubernetes_manifests(app_name)
    for name, content in result.artifacts.items():
        click.echo(f"\n=== {name} ===")
        click.echo(content)

if __name__ == '__main__':
    cli()
```

## 📊 Response Format

The `AgentResponse` object contains:

```python
@dataclass
class AgentResponse:
    request_id: str          # Unique request identifier
    status: str              # "completed", "failed", etc.
    message: str             # Human-readable response
    artifacts: Dict[str, Any]  # Generated files/configs
    confidence_score: float  # 0.0 to 1.0
    metadata: Dict[str, Any]  # Processing info
    error: Optional[str]     # Error message if failed
```

## 🛡️ Best Practices

1. **Always check for errors**:
   ```python
   if result.error:
       handle_error(result.error)
   ```

2. **Use confidence scores**:
   ```python
   if result.confidence_score < 0.8:
       request_human_review(result)
   ```

3. **Handle rate limits**:
   ```python
   import time
   from requests.exceptions import HTTPError
   
   def invoke_with_retry(client, message, max_retries=3):
       for i in range(max_retries):
           try:
               return client.invoke(message)
           except HTTPError as e:
               if e.response.status_code == 429:
                   time.sleep(2 ** i)  # Exponential backoff
               else:
                   raise
   ```

4. **Validate artifacts**:
   ```python
   def validate_dockerfile(content):
       required = ["FROM", "WORKDIR", "COPY"]
       return all(cmd in content for cmd in required)
   
   result = client.create_dockerfile("python", "fastapi")
   if validate_dockerfile(result.artifacts.get("dockerfile")):
       save_dockerfile(result.artifacts["dockerfile"])
   ```

## 📞 Support

- **Documentation**: [Agent Invocation Guide](../AGENT_INVOCATION_GUIDE.md)
- **API Reference**: https://docs.servicesessentials.ibm.com/api
- **Slack**: #ica-procode-agents
- **Email**: support@enterprise-advantage.ibm.com

## 📄 License

Part of the Agentic DevOps platform. See LICENSE for details.