"""
Basic usage example for test-agent.

This example demonstrates how to use the agent to answer questions.
"""

import asyncio
from test_agent.agents.react_agent import create_react_agent


async def main():
    """Run basic agent example."""
    # Create agent
    agent = create_react_agent()

    # Example questions
    questions = [
        "What is 25 * 34?",
        "What time is it now?",
        "Can you help me with a math problem?",
    ]

    for question in questions:
        print(f"\nUser: {question}")
        response = await agent(question)
        print(f"Agent: {response}")


if __name__ == "__main__":
    asyncio.run(main())
