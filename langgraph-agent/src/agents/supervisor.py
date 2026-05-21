"""
Supervisor Agent - Routes requests to specialized agents
"""

from typing import Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import JsonOutputParser
from src.graph.state import AgentState, SupervisorDecision
from src.config.settings import settings
import json
import logging

logger = logging.getLogger(__name__)


class SupervisorAgent:
    """
    Supervisor agent that analyzes requests and routes them to appropriate specialized agents.
    
    The supervisor uses an LLM to understand the user's request and determine which
    agent(s) should handle it. It can route to a single agent or coordinate multiple
    agents for complex tasks.
    """
    
    def __init__(self):
        """Initialize supervisor agent with LLM"""
        self.llm = ChatOpenAI(
            model=settings.supervisor_model,
            temperature=settings.model_temperature,
            max_tokens=settings.model_max_tokens
        )
        
        self.parser = JsonOutputParser()
        
        logger.info(f"Supervisor agent initialized with model: {settings.supervisor_model}")
    
    def analyze_and_route(self, state: AgentState) -> Dict[str, Any]:
        """
        Analyze user request and determine routing.
        
        Args:
            state: Current agent state
        
        Returns:
            Updated state with routing decision
        """
        try:
            user_input = state["user_input"]
            task_type = state.get("task_type", "auto")
            
            logger.info(f"Analyzing request: {user_input[:100]}...")
            
            # If task type is explicitly specified, use it
            if task_type != "auto":
                agent = self._map_task_type_to_agent(task_type)
                return self._create_routing_response(state, agent, f"Explicit task type: {task_type}")
            
            # Otherwise, use LLM to determine routing
            decision = self._llm_route_decision(user_input, state)
            
            return self._create_routing_response(
                state,
                decision["agent"],
                decision["reasoning"],
                decision.get("confidence", 0.8),
                decision.get("requires_multi_agent", False),
                decision.get("agent_sequence")
            )
            
        except Exception as e:
            logger.error(f"Error in supervisor routing: {str(e)}")
            # Default to devops agent on error
            return self._create_routing_response(
                state,
                "devops_agent",
                f"Error in routing, defaulting to devops agent: {str(e)}",
                0.5
            )
    
    def _llm_route_decision(self, user_input: str, state: AgentState) -> Dict[str, Any]:
        """
        Use LLM to make routing decision.
        
        Args:
            user_input: User's request
            state: Current state
        
        Returns:
            Routing decision
        """
        system_prompt = """You are a supervisor agent that routes tasks to specialized agents.

Available agents:
1. devops_agent: Handles CI/CD pipelines, Docker, Kubernetes, infrastructure provisioning, deployment automation
2. code_review_agent: Handles code analysis, security scanning, best practices, code quality, documentation
3. orchestrator_agent: Handles microservices coordination, workflow management, service mesh, distributed systems

Analyze the user request and determine which agent should handle it.

Respond with JSON in this exact format:
{
    "agent": "agent_name",
    "reasoning": "explanation of why this agent was chosen",
    "confidence": 0.9,
    "requires_multi_agent": false,
    "agent_sequence": null
}

If multiple agents are needed, set requires_multi_agent to true and provide agent_sequence as a list.

Examples:
- "Create a Dockerfile" -> devops_agent
- "Review this Python code for security issues" -> code_review_agent
- "Set up microservices communication" -> orchestrator_agent
- "Deploy and monitor a service" -> requires_multi_agent with [devops_agent, orchestrator_agent]
"""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=f"User request: {user_input}")
        ]
        
        try:
            response = self.llm.invoke(messages)
            content = response.content
            
            # Try to parse JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            decision = json.loads(content)
            
            # Validate agent name
            valid_agents = ["devops_agent", "code_review_agent", "orchestrator_agent"]
            if decision["agent"] not in valid_agents:
                logger.warning(f"Invalid agent name: {decision['agent']}, defaulting to devops_agent")
                decision["agent"] = "devops_agent"
            
            return decision
            
        except Exception as e:
            logger.error(f"Error parsing LLM response: {str(e)}")
            # Fallback to simple keyword matching
            return self._keyword_based_routing(user_input)
    
    def _keyword_based_routing(self, user_input: str) -> Dict[str, Any]:
        """
        Fallback routing based on keywords.
        
        Args:
            user_input: User's request
        
        Returns:
            Routing decision
        """
        user_input_lower = user_input.lower()
        
        # DevOps keywords
        devops_keywords = [
            "docker", "dockerfile", "kubernetes", "k8s", "ci/cd", "pipeline",
            "deploy", "deployment", "infrastructure", "terraform", "helm",
            "container", "build", "release"
        ]
        
        # Code review keywords
        review_keywords = [
            "review", "code", "security", "vulnerability", "scan", "analyze",
            "quality", "best practice", "lint", "test", "bug", "refactor"
        ]
        
        # Orchestration keywords
        orchestration_keywords = [
            "microservice", "service mesh", "orchestrat", "workflow",
            "coordinate", "distributed", "event", "message", "queue"
        ]
        
        # Count keyword matches
        devops_score = sum(1 for kw in devops_keywords if kw in user_input_lower)
        review_score = sum(1 for kw in review_keywords if kw in user_input_lower)
        orchestration_score = sum(1 for kw in orchestration_keywords if kw in user_input_lower)
        
        # Determine agent based on highest score
        scores = {
            "devops_agent": devops_score,
            "code_review_agent": review_score,
            "orchestrator_agent": orchestration_score
        }
        
        agent = max(scores, key=scores.get)
        confidence = scores[agent] / max(sum(scores.values()), 1)
        
        return {
            "agent": agent,
            "reasoning": f"Keyword-based routing (score: {scores[agent]})",
            "confidence": confidence,
            "requires_multi_agent": False,
            "agent_sequence": None
        }
    
    def _map_task_type_to_agent(self, task_type: str) -> str:
        """
        Map task type to agent name.
        
        Args:
            task_type: Task type
        
        Returns:
            Agent name
        """
        mapping = {
            "devops": "devops_agent",
            "code_review": "code_review_agent",
            "orchestration": "orchestrator_agent",
            "multi": "devops_agent"  # Start with devops for multi-agent
        }
        return mapping.get(task_type, "devops_agent")
    
    def _create_routing_response(
        self,
        state: AgentState,
        agent: str,
        reasoning: str,
        confidence: float = 0.8,
        requires_multi_agent: bool = False,
        agent_sequence: List[str] = None
    ) -> Dict[str, Any]:
        """
        Create routing response with updated state.
        
        Args:
            state: Current state
            agent: Agent to route to
            reasoning: Reasoning for routing decision
            confidence: Confidence score
            requires_multi_agent: Whether multiple agents are needed
            agent_sequence: Sequence of agents if multi-agent
        
        Returns:
            Updated state
        """
        agent_history = state.get("agent_history", [])
        agent_history.append("supervisor")
        
        metadata = state.get("metadata", {})
        metadata["routing_decision"] = {
            "agent": agent,
            "reasoning": reasoning,
            "confidence": confidence,
            "requires_multi_agent": requires_multi_agent,
            "agent_sequence": agent_sequence
        }
        
        logger.info(f"Routing to {agent} (confidence: {confidence:.2f}): {reasoning}")
        
        return {
            "current_agent": agent,
            "next_agent": agent_sequence[1] if agent_sequence and len(agent_sequence) > 1 else None,
            "agent_history": agent_history,
            "metadata": metadata,
            "confidence_score": confidence
        }
    
    def aggregate_results(self, state: AgentState) -> Dict[str, Any]:
        """
        Aggregate results from multiple agents.
        
        Args:
            state: Current state with agent responses
        
        Returns:
            Updated state with final output
        """
        try:
            agent_responses = state.get("agent_responses", {})
            
            if not agent_responses:
                return {
                    "final_output": "No agent responses to aggregate",
                    "confidence_score": 0.0
                }
            
            # Create formatted output
            output_parts = []
            total_confidence = 0.0
            
            for agent_name, response in agent_responses.items():
                output_parts.append(f"## {agent_name.replace('_', ' ').title()}\n")
                
                if isinstance(response, dict):
                    output_parts.append(response.get("output", str(response)))
                    total_confidence += response.get("confidence", 0.5)
                else:
                    output_parts.append(str(response))
                    total_confidence += 0.5
                
                output_parts.append("\n\n")
            
            final_output = "\n".join(output_parts)
            avg_confidence = total_confidence / len(agent_responses) if agent_responses else 0.0
            
            logger.info(f"Aggregated results from {len(agent_responses)} agents")
            
            return {
                "final_output": final_output,
                "confidence_score": avg_confidence,
                "should_continue": False
            }
            
        except Exception as e:
            logger.error(f"Error aggregating results: {str(e)}")
            return {
                "final_output": f"Error aggregating results: {str(e)}",
                "confidence_score": 0.0,
                "error": str(e)
            }


# Global supervisor instance
supervisor = SupervisorAgent()

# Made with Bob
