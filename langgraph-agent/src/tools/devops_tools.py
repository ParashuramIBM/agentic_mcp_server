"""
DevOps Tools - Tools for CI/CD, Docker, Kubernetes, and infrastructure automation
"""

from typing import Dict, Any, List, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class DevOpsTools:
    """Collection of DevOps automation tools"""
    
    def __init__(self):
        """Initialize DevOps tools with LLM"""
        self.llm = ChatOpenAI(
            model=settings.devops_model,
            temperature=0.2,  # Very low temperature for consistent outputs
            max_tokens=settings.model_max_tokens
        )
        logger.info("DevOps tools initialized")
    
    def create_dockerfile(
        self,
        language: str = "python",
        framework: str = "fastapi",
        user_input: str = ""
    ) -> str:
        """
        Generate a Dockerfile based on language and framework.
        
        Args:
            language: Programming language
            framework: Framework being used
            user_input: Additional context from user
        
        Returns:
            Dockerfile content
        """
        prompt = f"""Generate a production-ready Dockerfile for a {language} application using {framework}.

Requirements:
- Use multi-stage build for smaller image size
- Include security best practices
- Add health checks
- Optimize for caching
- Include proper user permissions (non-root)
- Add labels for metadata

User context: {user_input}

Generate only the Dockerfile content, no explanations."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            dockerfile = self._extract_code(response.content)
            logger.info(f"Generated Dockerfile for {language}/{framework}")
            return dockerfile
        except Exception as e:
            logger.error(f"Error generating Dockerfile: {str(e)}")
            return self._fallback_dockerfile(language, framework)
    
    def generate_kubernetes_manifests(
        self,
        app_name: str = "app",
        environment: str = "dev",
        user_input: str = ""
    ) -> Dict[str, str]:
        """
        Generate Kubernetes manifests (Deployment, Service, Ingress).
        
        Args:
            app_name: Application name
            environment: Target environment
            user_input: Additional context
        
        Returns:
            Dictionary of manifest files
        """
        manifests = {}
        
        # Generate Deployment
        deployment_prompt = f"""Generate a Kubernetes Deployment manifest for {app_name} in {environment} environment.

Requirements:
- Include resource limits and requests
- Add liveness and readiness probes
- Use rolling update strategy
- Include proper labels and selectors
- Set replicas based on environment (dev: 1, staging: 2, production: 3)

User context: {user_input}

Generate only the YAML content."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=deployment_prompt)])
            manifests["deployment.yaml"] = self._extract_code(response.content)
            logger.info(f"Generated Kubernetes Deployment for {app_name}")
        except Exception as e:
            logger.error(f"Error generating Deployment: {str(e)}")
            manifests["deployment.yaml"] = self._fallback_deployment(app_name, environment)
        
        # Generate Service
        service_prompt = f"""Generate a Kubernetes Service manifest for {app_name}.

Requirements:
- Type: ClusterIP for internal services, LoadBalancer for external
- Include proper selectors matching the deployment
- Expose appropriate ports

Generate only the YAML content."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=service_prompt)])
            manifests["service.yaml"] = self._extract_code(response.content)
            logger.info(f"Generated Kubernetes Service for {app_name}")
        except Exception as e:
            logger.error(f"Error generating Service: {str(e)}")
            manifests["service.yaml"] = self._fallback_service(app_name)
        
        return manifests
    
    def create_ci_cd_pipeline(
        self,
        provider: str = "github_actions",
        language: str = "python",
        user_input: str = ""
    ) -> str:
        """
        Generate CI/CD pipeline configuration.
        
        Args:
            provider: CI/CD provider (github_actions, gitlab_ci, jenkins)
            language: Programming language
            user_input: Additional context
        
        Returns:
            Pipeline configuration
        """
        prompt = f"""Generate a {provider} CI/CD pipeline for a {language} application.

Requirements:
- Build and test stages
- Security scanning (dependencies, code)
- Docker image build and push
- Deployment to Kubernetes
- Environment-based deployment (dev, staging, production)
- Proper secrets management

User context: {user_input}

Generate only the pipeline configuration file."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            pipeline = self._extract_code(response.content)
            logger.info(f"Generated {provider} pipeline for {language}")
            return pipeline
        except Exception as e:
            logger.error(f"Error generating pipeline: {str(e)}")
            return self._fallback_pipeline(provider, language)
    
    def generate_infrastructure_code(
        self,
        cloud_provider: str = "aws",
        user_input: str = ""
    ) -> str:
        """
        Generate Infrastructure as Code (Terraform).
        
        Args:
            cloud_provider: Cloud provider (aws, azure, gcp)
            user_input: Additional context
        
        Returns:
            Terraform configuration
        """
        prompt = f"""Generate Terraform configuration for {cloud_provider}.

Requirements:
- VPC and networking setup
- Kubernetes cluster (EKS/AKS/GKE)
- Database (RDS/Azure SQL/Cloud SQL)
- Load balancer
- Security groups and IAM roles
- Proper variable definitions

User context: {user_input}

Generate only the Terraform code."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            terraform = self._extract_code(response.content)
            logger.info(f"Generated Terraform for {cloud_provider}")
            return terraform
        except Exception as e:
            logger.error(f"Error generating infrastructure code: {str(e)}")
            return self._fallback_terraform(cloud_provider)
    
    def generate_monitoring_config(self, user_input: str = "") -> str:
        """
        Generate monitoring and observability configuration.
        
        Args:
            user_input: Additional context
        
        Returns:
            Monitoring configuration
        """
        prompt = f"""Generate monitoring configuration using Prometheus and Grafana.

Requirements:
- Prometheus scrape configs
- Service monitors
- Alert rules for common issues
- Grafana dashboard JSON
- Log aggregation setup

User context: {user_input}

Generate the configuration files."""
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            monitoring = self._extract_code(response.content)
            logger.info("Generated monitoring configuration")
            return monitoring
        except Exception as e:
            logger.error(f"Error generating monitoring config: {str(e)}")
            return self._fallback_monitoring()
    
    def _extract_code(self, content: str) -> str:
        """Extract code from LLM response"""
        if "```" in content:
            # Extract content between code blocks
            parts = content.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 1:  # Odd indices are code blocks
                    # Remove language identifier if present
                    lines = part.strip().split("\n")
                    if lines[0].strip() in ["yaml", "dockerfile", "python", "terraform", "hcl", "json"]:
                        return "\n".join(lines[1:])
                    return part.strip()
        return content.strip()
    
    # Fallback methods for when LLM fails
    
    def _fallback_dockerfile(self, language: str, framework: str) -> str:
        """Fallback Dockerfile template"""
        if language.lower() == "python":
            return f"""# Multi-stage build for Python {framework}
FROM python:3.11-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .

ENV PATH=/root/.local/bin:$PATH
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
  CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""
        return f"# Dockerfile for {language} {framework}\nFROM {language}:latest\n"
    
    def _fallback_deployment(self, app_name: str, environment: str) -> str:
        """Fallback Kubernetes Deployment"""
        replicas = {"dev": 1, "staging": 2, "production": 3}.get(environment, 1)
        return f"""apiVersion: apps/v1
kind: Deployment
metadata:
  name: {app_name}
  labels:
    app: {app_name}
    environment: {environment}
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: {app_name}
  template:
    metadata:
      labels:
        app: {app_name}
    spec:
      containers:
      - name: {app_name}
        image: {app_name}:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
"""
    
    def _fallback_service(self, app_name: str) -> str:
        """Fallback Kubernetes Service"""
        return f"""apiVersion: v1
kind: Service
metadata:
  name: {app_name}
spec:
  selector:
    app: {app_name}
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
"""
    
    def _fallback_pipeline(self, provider: str, language: str) -> str:
        """Fallback CI/CD pipeline"""
        if provider == "github_actions":
            return """name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
      - name: Build Docker image
        run: docker build -t app:${{ github.sha }} .
"""
        return f"# {provider} pipeline for {language}\n"
    
    def _fallback_terraform(self, cloud_provider: str) -> str:
        """Fallback Terraform configuration"""
        return f"""# Terraform configuration for {cloud_provider}
terraform {{
  required_version = ">= 1.0"
  required_providers {{
    {cloud_provider} = {{
      source  = "hashicorp/{cloud_provider}"
      version = "~> 5.0"
    }}
  }}
}}

provider "{cloud_provider}" {{
  region = var.region
}}

variable "region" {{
  description = "Cloud region"
  type        = string
  default     = "us-east-1"
}}
"""
    
    def _fallback_monitoring(self) -> str:
        """Fallback monitoring configuration"""
        return """# Prometheus configuration
global:
  scrape_interval: 15s
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
"""


# Global tools instance
devops_tools = DevOpsTools()

# Made with Bob
