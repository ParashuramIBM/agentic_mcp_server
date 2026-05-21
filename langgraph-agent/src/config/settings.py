"""
Configuration settings for LangGraph Multi-Agent System
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # ============================================================================
    # ICA (IBM Consulting Advantage) Configuration
    # ============================================================================
    ica_api_key: str
    ica_api_base: str = "https://agentstudio.servicesessentials.ibm.com"
    ica_organization_id: str
    ica_project_id: str
    ica_context_id: Optional[str] = None
    ica_use_context_studio: bool = True
    
    # ============================================================================
    # OpenAI-compatible Configuration (for LiteLLM)
    # ============================================================================
    openai_api_key: str
    openai_api_base: str = "https://agentstudio.servicesessentials.ibm.com/api/v1"
    
    # ============================================================================
    # Agent Configuration
    # ============================================================================
    agent_name: str = "agentic-devops-langgraph"
    agent_version: str = "1.0.0"
    agent_description: str = "Multi-agent system for DevOps automation, code review, and service orchestration"
    agent_port: int = 8000
    agent_host: str = "0.0.0.0"
    
    # ============================================================================
    # Model Configuration
    # ============================================================================
    default_model: str = "gpt-5.2-chat"
    supervisor_model: str = "gpt-5.2-chat"
    devops_model: str = "gpt-5.2-chat"
    review_model: str = "gpt-5.2-chat"
    orchestrator_model: str = "gpt-5.2-chat"
    model_temperature: float = 0.7
    model_max_tokens: int = 4096
    
    # ============================================================================
    # OpenTelemetry (OTEL) Configuration
    # ============================================================================
    otel_enabled: bool = False
    otel_exporter_otlp_endpoint: Optional[str] = None
    otel_service_name: str = "langgraph-agent"
    otel_service_version: str = "1.0.0"
    otel_environment: str = "development"
    
    # ============================================================================
    # MCP (Model Context Protocol) Configuration
    # ============================================================================
    mcp_enabled: bool = False
    mcp_server_url: Optional[str] = None
    mcp_virtual_server_id: Optional[str] = None
    
    # ============================================================================
    # Enterprise Advantage A2A Protocol Configuration
    # ============================================================================
    a2a_enabled: bool = True
    a2a_protocol: str = "json-rpc"  # json-rpc or rest
    a2a_version: str = "2.0"
    
    # Auto-registration with Agentic Studio
    auto_registration_enabled: bool = True
    agentic_studio_url: str = "https://agentstudio.servicesessentials.ibm.com"
    registration_retry_attempts: int = 3
    registration_retry_delay: int = 5  # seconds
    heartbeat_interval: int = 60  # seconds
    
    # ============================================================================
    # Logging Configuration
    # ============================================================================
    log_level: str = "INFO"
    log_format: str = "json"  # json or text
    log_file: Optional[str] = None
    
    # ============================================================================
    # Performance Configuration
    # ============================================================================
    max_concurrent_requests: int = 100
    request_timeout: int = 300  # seconds
    enable_caching: bool = True
    cache_ttl: int = 3600  # seconds
    max_iterations: int = 10  # Maximum workflow iterations
    environment: str = "production"  # Environment name
    
    # ============================================================================
    # Security Configuration
    # ============================================================================
    enable_auth: bool = False
    api_key_header: str = "X-API-Key"
    allowed_origins: list = ["*"]
    
    # ============================================================================
    # Development Configuration
    # ============================================================================
    debug: bool = False
    reload: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set OpenAI environment variables for LiteLLM
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
        os.environ["OPENAI_API_BASE"] = self.openai_api_base
    
    @property
    def agent_capabilities(self) -> list:
        """Return list of agent capabilities"""
        return [
            "devops_automation",
            "code_review",
            "service_orchestration",
            "multi_agent_coordination"
        ]
    
    @property
    def agent_metadata(self) -> dict:
        """Return agent metadata for registration"""
        return {
            "name": self.agent_name,
            "version": self.agent_version,
            "description": self.agent_description,
            "capabilities": self.agent_capabilities,
            "framework": "langgraph",
            "platform": "enterprise_advantage",
            "endpoints": {
                "invoke": f"http://{self.agent_host}:{self.agent_port}/agent/invoke",
                "stream": f"http://{self.agent_host}:{self.agent_port}/agent/stream",
                "status": f"http://{self.agent_host}:{self.agent_port}/agent/status",
                "capabilities": f"http://{self.agent_host}:{self.agent_port}/agent/capabilities"
            }
        }


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get the global settings instance"""
    return settings


# Made with Bob
