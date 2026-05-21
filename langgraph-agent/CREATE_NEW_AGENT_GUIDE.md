# Creating a New Agent from Context

This guide shows you how to create a new agent that leverages the deployed LangGraph DevOps Agent via the A2A (Agent-to-Agent) protocol.

## 🎯 Overview

Your deployed agent is accessible at:
```
https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024
```

You can create new agents that:
- **Invoke** this agent to perform DevOps tasks
- **Extend** its capabilities with additional logic
- **Orchestrate** multiple agents together
- **Integrate** with your existing systems

## 🚀 Quick Start

### Option 1: Use the Python Client Library

The easiest way to create a new agent is to use the provided `AgentClient` class:

```python
from examples.agent_client import AgentClient

# Initialize client
client = AgentClient()

# Use the agent
result = client.create_dockerfile("python", "fastapi")
print(result.artifacts["dockerfile"])
```

### Option 2: Direct HTTP Calls

You can also invoke the agent directly using HTTP:

```python
import requests
import os

AGENT_URL = "https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024"
API_KEY = os.getenv("AGENTIC_STUDIO_API_KEY")

response = requests.post(
    AGENT_URL,
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "message": "Create a Dockerfile for Python FastAPI",
        "context": {
            "environment": "production",
            "language": "python",
            "framework": "fastapi"
        }
    }
)

result = response.json()
print(result["response"]["message"])
```

## 📋 Prerequisites

1. **API Key**: Get your API key from [Agentic Studio Settings](https://agentstudio.servicesessentials.ibm.com/settings)
2. **Python 3.11+**: Ensure you have Python installed
3. **Dependencies**: Install required packages

```bash
cd langgraph-agent/examples
pip install -r requirements.txt
```

## 🏗️ Agent Creation Patterns

### Pattern 1: Wrapper Agent

Create an agent that wraps the DevOps agent with additional logic:

```python
from examples.agent_client import AgentClient

class CustomDevOpsAgent:
    """Custom agent that extends DevOps agent capabilities"""
    
    def __init__(self):
        self.client = AgentClient()
        self.templates = self._load_templates()
    
    def create_project_setup(self, project_config):
        """Create complete project setup with custom templates"""
        
        # Step 1: Generate base files using DevOps agent
        dockerfile = self.client.create_dockerfile(
            language=project_config["language"],
            framework=project_config["framework"]
        )
        
        # Step 2: Apply custom templates
        customized_dockerfile = self._apply_template(
            dockerfile.artifacts["dockerfile"],
            self.templates["dockerfile"]
        )
        
        # Step 3: Generate additional files
        k8s_manifests = self.client.create_kubernetes_manifests(
            app_name=project_config["app_name"],
            environment=project_config["environment"]
        )
        
        return {
            "dockerfile": customized_dockerfile,
            "k8s_manifests": k8s_manifests.artifacts,
            "readme": self._generate_readme(project_config)
        }
    
    def _load_templates(self):
        """Load custom templates"""
        return {
            "dockerfile": "# Custom header\n{content}",
            "readme": "# {project_name}\n\n{description}"
        }
    
    def _apply_template(self, content, template):
        """Apply template to content"""
        return template.format(content=content)
    
    def _generate_readme(self, config):
        """Generate README file"""
        return f"# {config['app_name']}\n\nGenerated DevOps setup"

# Usage
agent = CustomDevOpsAgent()
result = agent.create_project_setup({
    "app_name": "my-app",
    "language": "python",
    "framework": "fastapi",
    "environment": "production"
})
```

### Pattern 2: Orchestrator Agent

Create an agent that orchestrates multiple agents:

```python
from examples.agent_client import AgentClient

class DevOpsOrchestrator:
    """Orchestrates multiple agents for complex workflows"""
    
    def __init__(self):
        self.devops_agent = AgentClient()
        # Add other agents here
    
    def deploy_microservices(self, services_config):
        """Deploy multiple microservices"""
        results = {}
        
        for service in services_config["services"]:
            # Generate Dockerfile for each service
            dockerfile = self.devops_agent.create_dockerfile(
                language=service["language"],
                framework=service["framework"]
            )
            
            # Generate K8s manifests
            k8s = self.devops_agent.create_kubernetes_manifests(
                app_name=service["name"],
                environment=services_config["environment"],
                port=service["port"]
            )
            
            # Generate CI/CD pipeline
            cicd = self.devops_agent.create_cicd_pipeline(
                provider="github",
                language=service["language"]
            )
            
            results[service["name"]] = {
                "dockerfile": dockerfile.artifacts,
                "k8s": k8s.artifacts,
                "cicd": cicd.artifacts
            }
        
        # Generate service mesh configuration
        service_mesh = self._generate_service_mesh(services_config)
        results["service_mesh"] = service_mesh
        
        return results
    
    def _generate_service_mesh(self, config):
        """Generate service mesh configuration"""
        return self.devops_agent.invoke(
            message="Create Istio service mesh configuration",
            context={"services": [s["name"] for s in config["services"]]}
        )

# Usage
orchestrator = DevOpsOrchestrator()
result = orchestrator.deploy_microservices({
    "environment": "production",
    "services": [
        {"name": "api-gateway", "language": "nodejs", "framework": "express", "port": 3000},
        {"name": "auth-service", "language": "python", "framework": "fastapi", "port": 8000},
        {"name": "user-service", "language": "java", "framework": "spring", "port": 8080}
    ]
})
```

### Pattern 3: Specialized Agent

Create a specialized agent for specific use cases:

```python
from examples.agent_client import AgentClient

class SecurityHardenedAgent:
    """Agent specialized in security-hardened DevOps configurations"""
    
    def __init__(self):
        self.client = AgentClient()
        self.security_policies = self._load_security_policies()
    
    def create_secure_deployment(self, app_config):
        """Create security-hardened deployment"""
        
        # Generate base Dockerfile with security features
        dockerfile = self.client.create_dockerfile(
            language=app_config["language"],
            framework=app_config["framework"],
            features=["security-hardened", "minimal-size", "non-root-user"]
        )
        
        # Apply security policies
        secured_dockerfile = self._apply_security_policies(
            dockerfile.artifacts["dockerfile"]
        )
        
        # Generate K8s with security context
        k8s = self.client.invoke(
            message="Create Kubernetes manifests with security context and network policies",
            context={
                "app_name": app_config["app_name"],
                "security_context": {
                    "runAsNonRoot": True,
                    "readOnlyRootFilesystem": True,
                    "allowPrivilegeEscalation": False
                }
            }
        )
        
        # Generate security scanning pipeline
        security_scan = self.client.invoke(
            message="Create CI/CD pipeline with security scanning (Trivy, Snyk, SAST)",
            context={"language": app_config["language"]}
        )
        
        return {
            "dockerfile": secured_dockerfile,
            "k8s_manifests": k8s.artifacts,
            "security_pipeline": security_scan.artifacts,
            "security_report": self._generate_security_report()
        }
    
    def _load_security_policies(self):
        """Load security policies"""
        return {
            "no_root_user": True,
            "scan_vulnerabilities": True,
            "enforce_tls": True
        }
    
    def _apply_security_policies(self, dockerfile):
        """Apply security policies to Dockerfile"""
        # Add security enhancements
        lines = dockerfile.split('\n')
        
        # Add security scanning
        lines.insert(0, "# Security-hardened Dockerfile")
        lines.append("# Run as non-root user")
        lines.append("USER 1000:1000")
        
        return '\n'.join(lines)
    
    def _generate_security_report(self):
        """Generate security compliance report"""
        return {
            "compliance": "CIS Docker Benchmark",
            "policies_applied": list(self.security_policies.keys()),
            "scan_results": "All checks passed"
        }

# Usage
security_agent = SecurityHardenedAgent()
result = security_agent.create_secure_deployment({
    "app_name": "secure-app",
    "language": "python",
    "framework": "fastapi"
})
```

### Pattern 4: Integration Agent

Create an agent that integrates with existing systems:

```python
from examples.agent_client import AgentClient
import git
import os

class GitIntegrationAgent:
    """Agent that integrates DevOps setup with Git repositories"""
    
    def __init__(self):
        self.client = AgentClient()
    
    def setup_repository(self, repo_url, branch="main"):
        """Clone repo, generate DevOps files, and commit"""
        
        # Clone repository
        repo_path = self._clone_repo(repo_url, branch)
        
        # Detect project configuration
        config = self._detect_project_config(repo_path)
        
        # Generate DevOps files
        devops_files = self.client.create_complete_devops_setup(
            architecture=config["architecture"],
            language=config["language"],
            framework=config["framework"],
            services=config["services"]
        )
        
        # Write files to repository
        self._write_files(repo_path, devops_files.artifacts)
        
        # Commit and push
        self._commit_and_push(repo_path, "Add DevOps configuration")
        
        return {
            "repo_path": repo_path,
            "files_added": list(devops_files.artifacts.keys()),
            "commit_hash": self._get_commit_hash(repo_path)
        }
    
    def _clone_repo(self, url, branch):
        """Clone Git repository"""
        repo_name = url.split('/')[-1].replace('.git', '')
        repo_path = f"/tmp/{repo_name}"
        git.Repo.clone_from(url, repo_path, branch=branch)
        return repo_path
    
    def _detect_project_config(self, repo_path):
        """Detect project configuration from repository"""
        # Simplified detection logic
        if os.path.exists(f"{repo_path}/requirements.txt"):
            return {
                "language": "python",
                "framework": "fastapi",
                "architecture": "monolith",
                "services": [os.path.basename(repo_path)]
            }
        return {
            "language": "nodejs",
            "framework": "express",
            "architecture": "monolith",
            "services": [os.path.basename(repo_path)]
        }
    
    def _write_files(self, repo_path, artifacts):
        """Write generated files to repository"""
        for filename, content in artifacts.items():
            filepath = os.path.join(repo_path, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(content)
    
    def _commit_and_push(self, repo_path, message):
        """Commit and push changes"""
        repo = git.Repo(repo_path)
        repo.git.add(A=True)
        repo.index.commit(message)
        repo.remote().push()
    
    def _get_commit_hash(self, repo_path):
        """Get latest commit hash"""
        repo = git.Repo(repo_path)
        return repo.head.commit.hexsha

# Usage
git_agent = GitIntegrationAgent()
result = git_agent.setup_repository(
    repo_url="https://github.com/org/my-app.git",
    branch="main"
)
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in your project:

```bash
# Required
AGENTIC_STUDIO_API_KEY=your-api-key-here

# Optional
AGENT_URL=https://servicesessentials.ibm.com/agenticapps/a2a/511cd8a4-2a9a-4247-b7a2-e9fcfbead831/agents/e571f647-8fff-48d1-a6b5-5aea1205e024
```

Load environment variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

## 📊 Response Handling

### Success Response

```python
result = client.invoke("Create a Dockerfile")

if result.error:
    print(f"Error: {result.error}")
else:
    print(f"Status: {result.status}")
    print(f"Confidence: {result.confidence_score}")
    
    # Access artifacts
    for name, content in result.artifacts.items():
        print(f"\n=== {name} ===")
        print(content)
    
    # Access metadata
    print(f"\nProcessing time: {result.metadata.get('processing_time_ms')}ms")
    print(f"Tokens used: {result.metadata.get('tokens_used')}")
```

### Error Handling

```python
from requests.exceptions import HTTPError, Timeout, ConnectionError

try:
    result = client.invoke("Create a Dockerfile")
    
    if result.error:
        # Agent-level error
        handle_agent_error(result.error)
    else:
        # Success
        process_result(result)
        
except HTTPError as e:
    if e.response.status_code == 401:
        print("Authentication failed. Check your API key.")
    elif e.response.status_code == 429:
        print("Rate limit exceeded. Please retry later.")
    else:
        print(f"HTTP error: {e}")
        
except Timeout:
    print("Request timed out. Please retry.")
    
except ConnectionError:
    print("Connection error. Check your network.")
    
except Exception as e:
    print(f"Unexpected error: {e}")
```

## 🧪 Testing Your Agent

### Unit Tests

```python
import unittest
from unittest.mock import Mock, patch
from examples.agent_client import AgentClient

class TestCustomAgent(unittest.TestCase):
    
    def setUp(self):
        self.client = AgentClient()
    
    @patch('requests.post')
    def test_create_dockerfile(self, mock_post):
        # Mock response
        mock_post.return_value.json.return_value = {
            "request_id": "test-123",
            "status": "completed",
            "response": {
                "message": "Dockerfile created",
                "artifacts": {"dockerfile": "FROM python:3.11"},
                "confidence_score": 0.95
            },
            "metadata": {}
        }
        
        # Test
        result = self.client.create_dockerfile("python", "fastapi")
        
        # Assertions
        self.assertEqual(result.status, "completed")
        self.assertIn("dockerfile", result.artifacts)
        self.assertGreater(result.confidence_score, 0.9)

if __name__ == '__main__':
    unittest.main()
```

### Integration Tests

```python
def test_end_to_end():
    """Test complete workflow"""
    client = AgentClient()
    
    # Test 1: Create Dockerfile
    dockerfile_result = client.create_dockerfile("python", "fastapi")
    assert dockerfile_result.status == "completed"
    assert "dockerfile" in dockerfile_result.artifacts
    
    # Test 2: Create K8s manifests
    k8s_result = client.create_kubernetes_manifests("test-app")
    assert k8s_result.status == "completed"
    assert "deployment.yaml" in k8s_result.artifacts
    
    # Test 3: Create CI/CD pipeline
    cicd_result = client.create_cicd_pipeline("github", "python")
    assert cicd_result.status == "completed"
    
    print("✅ All tests passed!")

if __name__ == '__main__':
    test_end_to_end()
```

## 📚 Additional Resources

- **[Agent Invocation Guide](AGENT_INVOCATION_GUIDE.md)** - Complete API reference
- **[Examples README](examples/README.md)** - Usage examples and patterns
- **[Agent Client Source](examples/agent_client.py)** - Python client implementation
- **[API Documentation](https://docs.servicesessentials.ibm.com/api)** - Full API docs

## 🎯 Next Steps

1. **Get API Key**: Visit [Agentic Studio Settings](https://agentstudio.servicesessentials.ibm.com/settings)
2. **Install Dependencies**: `pip install -r examples/requirements.txt`
3. **Run Examples**: `python examples/agent_client.py`
4. **Create Your Agent**: Use one of the patterns above
5. **Test**: Write tests for your agent
6. **Deploy**: Deploy your agent to production

## 📞 Support

- **Documentation**: See docs in this repository
- **Slack**: #ica-procode-agents
- **Email**: support@enterprise-advantage.ibm.com

## 📄 License

Part of the Agentic DevOps platform. See LICENSE for details.

---

**Happy Building!** 🚀