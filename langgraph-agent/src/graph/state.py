"""
State definitions for LangGraph workflow
"""

from typing import TypedDict, List, Dict, Any, Optional, Literal
from datetime import datetime


class AgentState(TypedDict):
    """
    State schema for LangGraph multi-agent workflow.
    
    This state is passed between nodes in the graph and maintains
    the complete context of the agent execution.
    """
    
    # ============================================================================
    # Request Information
    # ============================================================================
    request_id: str
    """Unique identifier for this request"""
    
    user_input: str
    """Original user input/request"""
    
    task_type: Literal["devops", "code_review", "orchestration", "multi", "auto"]
    """Type of task to perform"""
    
    # ============================================================================
    # Agent Routing
    # ============================================================================
    current_agent: str
    """Currently active agent"""
    
    agent_history: List[str]
    """History of agents that have processed this request"""
    
    next_agent: Optional[str]
    """Next agent to route to (if any)"""
    
    # ============================================================================
    # Task Context
    # ============================================================================
    files: List[str]
    """List of files relevant to this task"""
    
    repository: Optional[str]
    """Git repository URL or path"""
    
    environment: Literal["dev", "staging", "production"]
    """Target environment"""
    
    context: Dict[str, Any]
    """Additional context information"""
    
    # ============================================================================
    # Agent Responses
    # ============================================================================
    agent_responses: Dict[str, Any]
    """Responses from each agent that has processed this request"""
    
    intermediate_results: List[Dict[str, Any]]
    """Intermediate results from agent processing"""
    
    final_output: Optional[str]
    """Final aggregated output"""
    
    # ============================================================================
    # Error Handling
    # ============================================================================
    error: Optional[str]
    """Error message if any"""
    
    error_details: Optional[Dict[str, Any]]
    """Detailed error information"""
    
    retry_count: int
    """Number of retry attempts"""
    
    # ============================================================================
    # Metadata
    # ============================================================================
    timestamp: str
    """Request timestamp in ISO format"""
    
    ica_context_id: str
    """ICA Context Studio context ID"""
    
    trace_id: str
    """OpenTelemetry trace ID"""
    
    metadata: Dict[str, Any]
    """Additional metadata"""
    
    # ============================================================================
    # Workflow Control
    # ============================================================================
    should_continue: bool
    """Whether to continue workflow execution"""
    
    requires_human_input: bool
    """Whether human input is required"""
    
    confidence_score: float
    """Confidence score of the current result (0.0 to 1.0)"""


class SupervisorDecision(TypedDict):
    """Decision made by supervisor agent"""
    agent: str
    """Agent to route to"""
    
    reasoning: str
    """Reasoning for the routing decision"""
    
    confidence: float
    """Confidence in the decision (0.0 to 1.0)"""
    
    requires_multi_agent: bool
    """Whether multiple agents are needed"""
    
    agent_sequence: Optional[List[str]]
    """Sequence of agents if multi-agent workflow"""


class AgentResponse(TypedDict):
    """Response from an agent"""
    agent_name: str
    """Name of the agent"""
    
    output: str
    """Agent output"""
    
    artifacts: Dict[str, Any]
    """Generated artifacts (files, configs, etc.)"""
    
    confidence: float
    """Confidence in the output"""
    
    suggestions: List[str]
    """Additional suggestions"""
    
    next_steps: List[str]
    """Recommended next steps"""
    
    metadata: Dict[str, Any]
    """Additional metadata"""


class WorkflowMetrics(TypedDict):
    """Metrics for workflow execution"""
    total_duration: float
    """Total execution time in seconds"""
    
    agent_durations: Dict[str, float]
    """Duration for each agent"""
    
    token_usage: Dict[str, int]
    """Token usage per agent"""
    
    api_calls: int
    """Total number of API calls"""
    
    cache_hits: int
    """Number of cache hits"""
    
    errors: int
    """Number of errors encountered"""


def create_initial_state(
    user_input: str,
    task_type: str = "auto",
    environment: str = "dev",
    files: Optional[List[str]] = None,
    repository: Optional[str] = None,
    ica_context_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> AgentState:
    """
    Create initial state for workflow execution.
    
    Args:
        user_input: User's request
        task_type: Type of task (devops, code_review, orchestration, multi, auto)
        environment: Target environment (dev, staging, production)
        files: List of relevant files
        repository: Git repository URL or path
        ica_context_id: ICA Context Studio context ID
        metadata: Additional metadata
    
    Returns:
        Initial AgentState
    """
    import uuid
    
    return AgentState(
        # Request information
        request_id=str(uuid.uuid4()),
        user_input=user_input,
        task_type=task_type,
        
        # Agent routing
        current_agent="",
        agent_history=[],
        next_agent=None,
        
        # Task context
        files=files or [],
        repository=repository,
        environment=environment,
        context={},
        
        # Agent responses
        agent_responses={},
        intermediate_results=[],
        final_output=None,
        
        # Error handling
        error=None,
        error_details=None,
        retry_count=0,
        
        # Metadata
        timestamp=datetime.utcnow().isoformat(),
        ica_context_id=ica_context_id or "",
        trace_id=str(uuid.uuid4()),
        metadata=metadata or {},
        
        # Workflow control
        should_continue=True,
        requires_human_input=False,
        confidence_score=1.0
    )


def update_state(
    state: AgentState,
    **updates
) -> AgentState:
    """
    Update state with new values.
    
    Args:
        state: Current state
        **updates: Key-value pairs to update
    
    Returns:
        Updated state
    """
    return {**state, **updates}


def add_agent_response(
    state: AgentState,
    agent_name: str,
    response: AgentResponse
) -> AgentState:
    """
    Add agent response to state.
    
    Args:
        state: Current state
        agent_name: Name of the agent
        response: Agent response
    
    Returns:
        Updated state
    """
    agent_responses = state.get("agent_responses", {})
    agent_responses[agent_name] = response
    
    agent_history = state.get("agent_history", [])
    if agent_name not in agent_history:
        agent_history.append(agent_name)
    
    return update_state(
        state,
        agent_responses=agent_responses,
        agent_history=agent_history,
        current_agent=agent_name
    )


def set_error(
    state: AgentState,
    error_message: str,
    error_details: Optional[Dict[str, Any]] = None
) -> AgentState:
    """
    Set error in state.
    
    Args:
        state: Current state
        error_message: Error message
        error_details: Detailed error information
    
    Returns:
        Updated state
    """
    return update_state(
        state,
        error=error_message,
        error_details=error_details or {},
        should_continue=False
    )

# Made with Bob
