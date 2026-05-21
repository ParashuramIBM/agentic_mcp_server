"""
FastAPI Server - REST API for LangGraph Multi-Agent System
Implements A2A (Agent-to-Agent) protocol for Enterprise Advantage integration
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from src.graph.workflow import invoke_workflow
from src.config.settings import settings
import logging
import json
import asyncio
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.agent_name,
    version=settings.agent_version,
    description=settings.agent_description,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================

class AgentRequest(BaseModel):
    """Request model for agent invocation"""
    user_input: str = Field(..., description="User's request or query")
    task_type: Optional[str] = Field("auto", description="Type of task (devops, code_review, orchestration, multi, auto)")
    environment: Optional[str] = Field("dev", description="Target environment (dev, staging, production)")
    files: Optional[List[str]] = Field(default_factory=list, description="List of relevant files")
    repository: Optional[str] = Field(None, description="Git repository URL or path")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")


class AgentResponse(BaseModel):
    """Response model for agent invocation"""
    request_id: str
    final_output: str
    agent_history: List[str]
    confidence_score: float
    metadata: Dict[str, Any]
    error: Optional[str] = None


class StatusResponse(BaseModel):
    """Response model for status check"""
    status: str
    agent_name: str
    version: str
    uptime: str
    capabilities: List[str]


class CapabilitiesResponse(BaseModel):
    """Response model for capabilities"""
    capabilities: List[str]
    agents: List[str]
    supported_tasks: List[str]
    metadata: Dict[str, Any]


class A2ARequest(BaseModel):
    """A2A Protocol JSON-RPC request"""
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any]
    id: str


class A2AResponse(BaseModel):
    """A2A Protocol JSON-RPC response"""
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: str


# ============================================================================
# Startup/Shutdown Events
# ============================================================================

# Global agent registry ID
agent_registry_id = None

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    global agent_registry_id
    
    logger.info(f"Starting {settings.agent_name} v{settings.agent_version}")
    logger.info(f"ICA API Base: {settings.ica_api_base}")
    logger.info(f"Agent capabilities: {', '.join(settings.agent_capabilities)}")
    
    # Initialize OTEL instrumentation
    if settings.otel_enabled:
        logger.info("OTEL instrumentation enabled")
        # TODO: Initialize OTEL SDK
    
    # Register with Agentic Studio
    if settings.auto_registration_enabled:
        logger.info("Auto-registration with Agentic Studio enabled")
        try:
            from src.integration.registration import registration
            agent_registry_id = registration.register_agent()
            
            if agent_registry_id:
                logger.info(f"✅ Agent registered with ID: {agent_registry_id}")
                # Start heartbeat task
                asyncio.create_task(heartbeat_task())
            else:
                logger.warning("⚠️  Agent registration failed, continuing without registration")
        except Exception as e:
            logger.error(f"Error during registration: {str(e)}")
    
    logger.info(f"🚀 Server ready on {settings.agent_host}:{settings.agent_port}")
    logger.info(f"📚 API Documentation: http://localhost:{settings.agent_port}/docs")


async def heartbeat_task():
    """Send periodic heartbeats to Agentic Studio"""
    global agent_registry_id
    
    from src.integration.registration import registration
    
    while True:
        await asyncio.sleep(settings.heartbeat_interval)
        
        if agent_registry_id:
            try:
                success = registration.send_heartbeat(agent_registry_id)
                if not success:
                    logger.warning("Heartbeat failed")
            except Exception as e:
                logger.error(f"Error sending heartbeat: {str(e)}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global agent_registry_id
    
    logger.info(f"Shutting down {settings.agent_name}")
    
    # Deregister from Agentic Studio
    if settings.auto_registration_enabled and agent_registry_id:
        logger.info("Deregistering from Agentic Studio...")
        try:
            from src.integration.registration import registration
            success = registration.deregister_agent(agent_registry_id)
            if success:
                logger.info("✅ Agent deregistered successfully")
            else:
                logger.warning("⚠️  Deregistration failed")
        except Exception as e:
            logger.error(f"Error during deregistration: {str(e)}")


# ============================================================================
# Health & Status Endpoints
# ============================================================================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.agent_name}",
        "version": settings.agent_version,
        "docs": "/docs",
        "status": "/agent/status"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes"""
    return {"status": "healthy"}


@app.get("/agent/status", response_model=StatusResponse)
async def agent_status():
    """
    Get agent status and information.
    
    Returns:
        Agent status information
    """
    return StatusResponse(
        status="healthy",
        agent_name=settings.agent_name,
        version=settings.agent_version,
        uptime="running",  # TODO: Calculate actual uptime
        capabilities=settings.agent_capabilities
    )


@app.get("/agent/capabilities", response_model=CapabilitiesResponse)
async def agent_capabilities():
    """
    Get agent capabilities and supported operations.
    
    Returns:
        Agent capabilities information
    """
    return CapabilitiesResponse(
        capabilities=settings.agent_capabilities,
        agents=["supervisor", "devops_agent", "code_review_agent", "orchestrator_agent"],
        supported_tasks=["devops", "code_review", "orchestration", "multi"],
        metadata=settings.agent_metadata
    )


# ============================================================================
# Agent Invocation Endpoints
# ============================================================================

@app.post("/agent/invoke", response_model=AgentResponse)
async def invoke_agent(request: AgentRequest):
    """
    Invoke agent with a request (synchronous).
    
    Args:
        request: Agent request
    
    Returns:
        Agent response with results
    """
    try:
        logger.info(f"Received request: {request.user_input[:100]}...")
        
        # Invoke workflow
        final_state = invoke_workflow(
            user_input=request.user_input,
            task_type=request.task_type,
            environment=request.environment,
            files=request.files,
            repository=request.repository,
            metadata=request.metadata
        )
        
        # Create response
        response = AgentResponse(
            request_id=final_state["request_id"],
            final_output=final_state.get("final_output", "No output generated"),
            agent_history=final_state.get("agent_history", []),
            confidence_score=final_state.get("confidence_score", 0.0),
            metadata=final_state.get("metadata", {}),
            error=final_state.get("error")
        )
        
        logger.info(f"Request completed: {response.request_id}")
        return response
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/agent/stream")
async def stream_agent(request: AgentRequest):
    """
    Invoke agent with streaming response.
    
    Args:
        request: Agent request
    
    Returns:
        Streaming response
    """
    async def generate():
        try:
            # Send initial message
            yield f"data: {json.dumps({'status': 'started', 'request_id': 'streaming'})}\n\n"
            
            # Invoke workflow
            final_state = invoke_workflow(
                user_input=request.user_input,
                task_type=request.task_type,
                environment=request.environment,
                files=request.files,
                repository=request.repository,
                metadata=request.metadata
            )
            
            # Stream agent history
            for agent in final_state.get("agent_history", []):
                yield f"data: {json.dumps({'agent': agent, 'status': 'processing'})}\n\n"
                await asyncio.sleep(0.1)
            
            # Send final output
            yield f"data: {json.dumps({'status': 'completed', 'output': final_state.get('final_output', '')})}\n\n"
            
        except Exception as e:
            logger.error(f"Error in streaming: {str(e)}")
            yield f"data: {json.dumps({'status': 'error', 'error': str(e)})}\n\n"
    
    return StreamingResponse(generate(), media_type="text/event-stream")


# ============================================================================
# A2A Protocol Endpoints (JSON-RPC)
# ============================================================================

@app.post("/a2a/invoke", response_model=A2AResponse)
async def a2a_invoke(request: A2ARequest):
    """
    A2A Protocol endpoint (JSON-RPC 2.0).
    
    Implements the Agent-to-Agent protocol for Enterprise Advantage integration.
    
    Args:
        request: A2A JSON-RPC request
    
    Returns:
        A2A JSON-RPC response
    """
    try:
        logger.info(f"A2A request: {request.method}")
        
        # Validate JSON-RPC version
        if request.jsonrpc != "2.0":
            return A2AResponse(
                jsonrpc="2.0",
                error={"code": -32600, "message": "Invalid JSON-RPC version"},
                id=request.id
            )
        
        # Handle different methods
        if request.method == "agent.invoke":
            # Extract parameters
            params = request.params
            user_input = params.get("task", params.get("user_input", ""))
            context = params.get("context", {})
            
            # Invoke workflow
            final_state = invoke_workflow(
                user_input=user_input,
                task_type=context.get("task_type", "auto"),
                environment=context.get("environment", "dev"),
                files=context.get("files", []),
                repository=context.get("repository"),
                metadata=context
            )
            
            # Return result
            return A2AResponse(
                jsonrpc="2.0",
                result={
                    "request_id": final_state["request_id"],
                    "output": final_state.get("final_output", ""),
                    "agent_history": final_state.get("agent_history", []),
                    "confidence": final_state.get("confidence_score", 0.0),
                    "metadata": final_state.get("metadata", {})
                },
                id=request.id
            )
        
        elif request.method == "agent.status":
            # Return agent status
            return A2AResponse(
                jsonrpc="2.0",
                result={
                    "status": "healthy",
                    "agent_name": settings.agent_name,
                    "version": settings.agent_version,
                    "capabilities": settings.agent_capabilities
                },
                id=request.id
            )
        
        elif request.method == "agent.capabilities":
            # Return capabilities
            return A2AResponse(
                jsonrpc="2.0",
                result={
                    "capabilities": settings.agent_capabilities,
                    "agents": ["supervisor", "devops_agent", "code_review_agent", "orchestrator_agent"],
                    "metadata": settings.agent_metadata
                },
                id=request.id
            )
        
        else:
            # Method not found
            return A2AResponse(
                jsonrpc="2.0",
                error={"code": -32601, "message": f"Method not found: {request.method}"},
                id=request.id
            )
    
    except Exception as e:
        logger.error(f"A2A error: {str(e)}")
        return A2AResponse(
            jsonrpc="2.0",
            error={"code": -32603, "message": f"Internal error: {str(e)}"},
            id=request.id
        )


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host=settings.agent_host,
        port=settings.agent_port,
        log_level=settings.log_level.lower(),
        reload=settings.reload
    )

# Made with Bob
