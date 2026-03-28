"""
Custom tools for the agent.
"""

from agentscope.tools import tool


@tool("calculate")
def calculator(expression: str) -> str:
    """
    Calculate mathematical expressions.

    Args:
        expression: Mathematical expression to evaluate

    Returns:
        Calculation result
    """
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"


@tool("get_current_time")
def get_current_time() -> str:
    """
    Get the current time.

    Returns:
        Current time as string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
