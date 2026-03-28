"""
Advanced multi-agent example for integration-test-agent.

This example demonstrates multi-agent collaboration.
"""

import asyncio
from agentscope.agent import ReActAgent
from integration_test_agent.config import get_model, get_memory, get_toolkit


async def main():
    """Run advanced multi-agent example."""
    # Create specialized agents
    researcher = ReActAgent(
        name="Researcher",
        sys_prompt="You are a research specialist. Find and analyze information.",
        model=get_model(),
        memory=get_memory(),
        toolkit=get_toolkit(),
    )

    analyst = ReActAgent(
        name="Analyst",
        sys_prompt="You are an analyst. Synthesize information and provide insights.",
        model=get_model(),
        memory=get_memory(),
        toolkit=get_toolkit(),
    )

    # Example workflow
    query = "What are the latest developments in AI?"

    print(f"\nQuery: {query}")
    print(f"\n--- Researcher Agent ---")
    research_result = await researcher(query)
    print(f"Research result: {research_result}")

    print(f"\n--- Analyst Agent ---")
    analysis = await analyst(f"Analyze this research: {research_result}")
    print(f"Analysis: {analysis}")


if __name__ == "__main__":
    asyncio.run(main())
