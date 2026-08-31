from typing import Any, Dict, Optional
from agents.graph import build_graph
from agents.nodes import AgentState


def run_pipeline(user_input: str, project_id: Optional[str] = None, context: Optional[Dict] = None) -> Dict[str, Any]:
    """Run the full 7-node LangGraph pipeline."""
    graph = build_graph()
    initial: AgentState = {
        "messages": [],
        "user_input": user_input,
        "project_id": project_id,
        "intent": None,
        "plan": None,
        "research": None,
        "code": None,
        "review": None,
        "deploy": None,
        "memory": None,
        "context": context or {},
        "errors": [],
    }
    result = graph.invoke(initial)
    return result
