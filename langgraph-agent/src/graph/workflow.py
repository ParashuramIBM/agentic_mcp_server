"""
LangGraph Workflow - Defines the multi-agent workflow graph
"""

from langgraph.graph import StateGraph, END
from src.graph.state import AgentState, create_initial_state
from src.agents.supervisor import supervisor
from src.agents.devops_agent import devops_agent
from src.config.settings import settings
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)


def create_workflow() -> StateGraph:
    """
    Create and configure the LangGraph workflow.
    
    Returns:
        Compiled StateGraph
    """
    logger.info("Creating LangGraph workflow...")
    
    # Initialize graph with AgentState
    workflow = StateGraph(AgentState)
    
    # ============================================================================
    # Define Node Functions
    # ============================================================================
    
    def supervisor_node(state: AgentState) -> AgentState:
        """
        Supervisor node - analyzes request and routes to appropriate agent.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with routing decision
        """
        try:
            logger.info(f"Supervisor analyzing request: {state['request_id']}")
            result = supervisor.analyze_and_route(state)
            return {**state, **result}
        except Exception as e:
            logger.error(f"Error in supervisor node: {str(e)}")
            return {
                **state,
                "error": f"Supervisor error: {str(e)}",
                "should_continue": False
            }
    
    def devops_node(state: AgentState) -> AgentState:
        """
        DevOps agent node - handles DevOps automation tasks.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with DevOps results
        """
        try:
            logger.info(f"DevOps agent processing: {state['request_id']}")
            result = devops_agent.execute(state)
            return {**state, **result}
        except Exception as e:
            logger.error(f"Error in devops node: {str(e)}")
            return {
                **state,
                "error": f"DevOps agent error: {str(e)}",
                "agent_history": state.get("agent_history", []) + ["devops_agent"]
            }
    
    def code_review_node(state: AgentState) -> AgentState:
        """
        Code review agent node - handles code analysis tasks.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with code review results
        """
        try:
            logger.info(f"Code review agent processing: {state['request_id']}")
            # TODO: Implement code review agent
            # For now, fallback to devops agent
            logger.warning("Code review agent not yet implemented, using devops agent")
            result = devops_agent.execute(state)
            return {**state, **result}
        except Exception as e:
            logger.error(f"Error in code review node: {str(e)}")
            return {
                **state,
                "error": f"Code review agent error: {str(e)}",
                "agent_history": state.get("agent_history", []) + ["code_review_agent"]
            }
    
    def orchestrator_node(state: AgentState) -> AgentState:
        """
        Orchestrator agent node - handles service orchestration tasks.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with orchestration results
        """
        try:
            logger.info(f"Orchestrator agent processing: {state['request_id']}")
            # TODO: Implement orchestrator agent
            # For now, fallback to devops agent
            logger.warning("Orchestrator agent not yet implemented, using devops agent")
            result = devops_agent.execute(state)
            return {**state, **result}
        except Exception as e:
            logger.error(f"Error in orchestrator node: {str(e)}")
            return {
                **state,
                "error": f"Orchestrator agent error: {str(e)}",
                "agent_history": state.get("agent_history", []) + ["orchestrator_agent"]
            }
    
    def finalize_node(state: AgentState) -> AgentState:
        """
        Finalize node - aggregates results and prepares final output.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with final output
        """
        try:
            logger.info(f"Finalizing results: {state['request_id']}")
            result = supervisor.aggregate_results(state)
            return {**state, **result}
        except Exception as e:
            logger.error(f"Error in finalize node: {str(e)}")
            return {
                **state,
                "final_output": f"Error finalizing results: {str(e)}",
                "error": str(e),
                "should_continue": False
            }
    
    def error_handler_node(state: AgentState) -> AgentState:
        """
        Error handler node - handles errors and retries.
        
        Args:
            state: Current state
        
        Returns:
            Updated state with error handling
        """
        error = state.get("error", "Unknown error")
        retry_count = state.get("retry_count", 0)
        
        logger.error(f"Error handler: {error} (retry {retry_count})")
        
        # Check if we should retry
        max_retries = 2
        if retry_count < max_retries and not state.get("requires_human_input", False):
            logger.info(f"Retrying request (attempt {retry_count + 1}/{max_retries})")
            return {
                **state,
                "retry_count": retry_count + 1,
                "error": None,
                "should_continue": True,
                "current_agent": ""  # Reset to start over
            }
        
        # Max retries reached or human input required
        return {
            **state,
            "final_output": f"Error: {error}\n\nPlease try rephrasing your request or contact support.",
            "should_continue": False
        }
    
    # ============================================================================
    # Add Nodes to Graph
    # ============================================================================
    
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("devops_agent", devops_node)
    workflow.add_node("code_review_agent", code_review_node)
    workflow.add_node("orchestrator_agent", orchestrator_node)
    workflow.add_node("finalize", finalize_node)
    workflow.add_node("error_handler", error_handler_node)
    
    # ============================================================================
    # Define Routing Logic
    # ============================================================================
    
    def route_to_agent(state: AgentState) -> str:
        """
        Route to appropriate agent based on supervisor decision.
        
        Args:
            state: Current state
        
        Returns:
            Next node name
        """
        # Check for errors
        if state.get("error"):
            return "error_handler"
        
        # Get current agent from state
        current_agent = state.get("current_agent", "")
        
        # Route to appropriate agent
        if current_agent == "devops_agent":
            return "devops_agent"
        elif current_agent == "code_review_agent":
            return "code_review_agent"
        elif current_agent == "orchestrator_agent":
            return "orchestrator_agent"
        else:
            # Default to devops if no agent specified
            logger.warning(f"No agent specified, defaulting to devops_agent")
            return "devops_agent"
    
    def should_continue(state: AgentState) -> str:
        """
        Determine if workflow should continue or end.
        
        Args:
            state: Current state
        
        Returns:
            Next node name or END
        """
        # Check if we should continue
        if not state.get("should_continue", True):
            return END
        
        # Check if there's a next agent to route to
        next_agent = state.get("next_agent")
        if next_agent:
            return next_agent
        
        # Check if there's an error
        if state.get("error"):
            return "error_handler"
        
        # Otherwise, finalize
        return "finalize"
    
    def after_agent(state: AgentState) -> str:
        """
        Determine next step after agent execution.
        
        Args:
            state: Current state
        
        Returns:
            Next node name
        """
        # Check for errors
        if state.get("error"):
            return "error_handler"
        
        # Check if there's a next agent
        next_agent = state.get("next_agent")
        if next_agent:
            return "supervisor"  # Go back to supervisor for routing
        
        # Otherwise, finalize
        return "finalize"
    
    # ============================================================================
    # Define Edges
    # ============================================================================
    
    # Set entry point
    workflow.set_entry_point("supervisor")
    
    # Supervisor routes to agents
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "devops_agent": "devops_agent",
            "code_review_agent": "code_review_agent",
            "orchestrator_agent": "orchestrator_agent",
            "error_handler": "error_handler"
        }
    )
    
    # After each agent, determine next step
    workflow.add_conditional_edges(
        "devops_agent",
        after_agent,
        {
            "supervisor": "supervisor",
            "finalize": "finalize",
            "error_handler": "error_handler"
        }
    )
    
    workflow.add_conditional_edges(
        "code_review_agent",
        after_agent,
        {
            "supervisor": "supervisor",
            "finalize": "finalize",
            "error_handler": "error_handler"
        }
    )
    
    workflow.add_conditional_edges(
        "orchestrator_agent",
        after_agent,
        {
            "supervisor": "supervisor",
            "finalize": "finalize",
            "error_handler": "error_handler"
        }
    )
    
    # Finalize goes to end
    workflow.add_edge("finalize", END)
    
    # Error handler can retry or end
    workflow.add_conditional_edges(
        "error_handler",
        should_continue,
        {
            "supervisor": "supervisor",
            END: END
        }
    )
    
    logger.info("LangGraph workflow created successfully")
    
    return workflow


def compile_workflow() -> StateGraph:
    """
    Create and compile the workflow.
    
    Returns:
        Compiled workflow ready for execution
    """
    workflow = create_workflow()
    compiled = workflow.compile()
    logger.info("Workflow compiled successfully")
    return compiled


# Global compiled workflow instance
graph = compile_workflow()


def invoke_workflow(
    user_input: str,
    task_type: str = "auto",
    environment: str = "dev",
    files: list = None,
    repository: str = None,
    metadata: dict = None
) -> AgentState:
    """
    Invoke the workflow with a user request.
    
    Args:
        user_input: User's request
        task_type: Type of task
        environment: Target environment
        files: List of relevant files
        repository: Git repository
        metadata: Additional metadata
    
    Returns:
        Final state after workflow execution
    """
    # Create initial state
    initial_state = create_initial_state(
        user_input=user_input,
        task_type=task_type,
        environment=environment,
        files=files,
        repository=repository,
        ica_context_id=settings.ica_context_id,
        metadata=metadata
    )
    
    logger.info(f"Invoking workflow for request: {initial_state['request_id']}")
    
    try:
        # Execute workflow
        final_state = graph.invoke(initial_state)
        logger.info(f"Workflow completed: {initial_state['request_id']}")
        return final_state
    except Exception as e:
        logger.error(f"Workflow execution error: {str(e)}")
        return {
            **initial_state,
            "error": str(e),
            "final_output": f"Workflow error: {str(e)}",
            "should_continue": False
        }

# Made with Bob
