"""
Base ReAct agent implementation.
"""

from agentscope.agent import ReActAgent
from test_agent.config import get_model, get_memory, get_toolkit


def create_react_agent(name: str = "test-agent") -> ReActAgent:
    """
    Create a ReAct agent instance.

    Args:
        name: Agent name

    Returns:
        Configured ReActAgent instance
    """
    model = get_model()
    memory = get_memory()
    toolkit = get_toolkit()

    return ReActAgent(
        name=name,
        sys_prompt="You are a helpful assistant with access to various tools.",
        model=model,
        toolkit=toolkit,
        memory=memory,
    )
