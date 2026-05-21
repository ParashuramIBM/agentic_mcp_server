"""
Agent Registration with Agentic Studio
Handles automatic registration, heartbeat, and deregistration
"""

import requests
import logging
from typing import Dict, Any, Optional
from src.config.settings import settings
import json
import os

logger = logging.getLogger(__name__)


class AgenticStudioRegistration:
    """Handle agent registration with Agentic Studio"""
    
    def __init__(self):
        self.studio_url = settings.agentic_studio_url
        self.api_key = settings.ica_api_key
        self.organization_id = settings.ica_organization_id
        self.project_id = settings.ica_project_id
        self.agent_metadata = self._load_metadata()
        
    def _load_metadata(self) -> Dict[str, Any]:
        """Load agent metadata from JSON file"""
        try:
            metadata_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                "agent_metadata.json"
            )
            
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    return json.load(f)
            else:
                logger.warning(f"Metadata file not found: {metadata_path}")
                return {}
        except Exception as e:
            logger.error(f"Error loading metadata: {str(e)}")
            return {}
    
    def register_agent(self) -> Optional[str]:
        """
        Register agent with Agentic Studio.
        
        Returns:
            Agent registry ID if successful, None otherwise
        """
        try:
            logger.info("Registering agent with Agentic Studio...")
            
            # Get base URL for endpoints
            base_url = f"http://{settings.agent_host}:{settings.agent_port}"
            if settings.agent_host == "0.0.0.0":
                # Use localhost for registration
                base_url = f"http://localhost:{settings.agent_port}"
            
            # Prepare registration payload
            payload = {
                "name": self.agent_metadata.get("agent_name", settings.agent_name),
                "version": self.agent_metadata.get("agent_version", settings.agent_version),
                "description": self.agent_metadata.get("agent_description", settings.agent_description),
                "framework": "langgraph",
                "platform": "enterprise_advantage",
                "orchestration_pattern": "react",
                "model": self.agent_metadata.get("model", "gpt-5.2-chat"),
                "capabilities": self.agent_metadata.get("capabilities", settings.agent_capabilities),
                "agents": self.agent_metadata.get("agents", []),
                "endpoints": {
                    "invoke": f"{base_url}/agent/invoke",
                    "stream": f"{base_url}/agent/stream",
                    "status": f"{base_url}/agent/status",
                    "capabilities": f"{base_url}/agent/capabilities",
                    "a2a": f"{base_url}/a2a/invoke",
                    "health": f"{base_url}/health"
                },
                "integration": self.agent_metadata.get("integration", {
                    "mcp_gateway": "ICA Shared MCP Gateway",
                    "workflow_orchestrator": "AgentCore Orchestrator",
                    "observability": "Arize Phoenix"
                }),
                "deployment": self.agent_metadata.get("deployment", {
                    "type": "containerized",
                    "runtime": "docker",
                    "health_check": "/health"
                }),
                "tags": self.agent_metadata.get("tags", ["devops", "automation", "langgraph"])
            }
            
            # Register with Agentic Studio API
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Organization-ID": self.organization_id,
                "X-Project-ID": self.project_id
            }
            
            # Try registration with retries
            for attempt in range(settings.registration_retry_attempts):
                try:
                    response = requests.post(
                        f"{self.studio_url}/api/v1/agents/register",
                        json=payload,
                        headers=headers,
                        timeout=30
                    )
                    
                    if response.status_code in [200, 201]:
                        result = response.json()
                        agent_id = result.get("agent_id") or result.get("id") or result.get("registry_id")
                        
                        if agent_id:
                            logger.info(f"✅ Agent registered successfully: {agent_id}")
                            logger.info(f"   Name: {payload['name']}")
                            logger.info(f"   Version: {payload['version']}")
                            logger.info(f"   Endpoints: {base_url}")
                            return agent_id
                        else:
                            logger.warning("Registration succeeded but no agent ID returned")
                            return "registered-no-id"
                    
                    elif response.status_code == 409:
                        # Agent already registered
                        logger.info("Agent already registered, using existing registration")
                        result = response.json()
                        return result.get("agent_id") or result.get("id") or "existing"
                    
                    else:
                        logger.error(f"Registration failed (attempt {attempt + 1}/{settings.registration_retry_attempts}): {response.status_code}")
                        logger.error(f"Response: {response.text}")
                        
                        if attempt < settings.registration_retry_attempts - 1:
                            import time
                            time.sleep(settings.registration_retry_delay)
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"Network error during registration (attempt {attempt + 1}): {str(e)}")
                    if attempt < settings.registration_retry_attempts - 1:
                        import time
                        time.sleep(settings.registration_retry_delay)
            
            logger.error("All registration attempts failed")
            return None
                
        except Exception as e:
            logger.error(f"Error registering agent: {str(e)}")
            logger.exception(e)
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
                "Content-Type": "application/json",
                "X-Organization-ID": self.organization_id
            }
            
            payload = {
                "status": "healthy",
                "timestamp": "now",
                "metrics": {
                    "uptime": "running",
                    "requests_processed": 0  # TODO: Track actual metrics
                }
            }
            
            response = requests.post(
                f"{self.studio_url}/api/v1/agents/{agent_id}/heartbeat",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                logger.debug(f"Heartbeat sent successfully for agent {agent_id}")
                return True
            else:
                logger.warning(f"Heartbeat failed: {response.status_code}")
                return False
            
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
            logger.info(f"Deregistering agent: {agent_id}")
            
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "X-Organization-ID": self.organization_id
            }
            
            response = requests.delete(
                f"{self.studio_url}/api/v1/agents/{agent_id}",
                headers=headers,
                timeout=10
            )
            
            if response.status_code in [200, 204]:
                logger.info(f"✅ Agent deregistered successfully: {agent_id}")
                return True
            elif response.status_code == 404:
                logger.info(f"Agent not found (may have been already deregistered): {agent_id}")
                return True
            else:
                logger.error(f"Deregistration failed: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Error deregistering agent: {str(e)}")
            return False
    
    def update_agent_status(self, agent_id: str, status: str, message: str = "") -> bool:
        """
        Update agent status in Agentic Studio.
        
        Args:
            agent_id: Agent registry ID
            status: Status (healthy, degraded, error)
            message: Optional status message
        
        Returns:
            True if successful, False otherwise
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-Organization-ID": self.organization_id
            }
            
            payload = {
                "status": status,
                "message": message,
                "timestamp": "now"
            }
            
            response = requests.patch(
                f"{self.studio_url}/api/v1/agents/{agent_id}/status",
                json=payload,
                headers=headers,
                timeout=10
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Error updating agent status: {str(e)}")
            return False


# Global registration instance
registration = AgenticStudioRegistration()

# Made with Bob
