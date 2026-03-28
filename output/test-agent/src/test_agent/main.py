"""
Main entry point for test-agent.

This module initializes and runs the AgentScope agent.
"""

import asyncio
import os
from dotenv import load_dotenv

from test_agent.config import settings, get_model, get_memory, get_toolkit
from agentscope.agent import ReActAgent

# Load environment variables
load_dotenv()


async def main():
    """Main entry point."""
    # Initialize configuration
    model = get_model()
    memory = get_memory()
    toolkit = get_toolkit()

    # Create agent
    agent = ReActAgent(
        name="test-agent",
        sys_prompt=settings.SYSTEM_PROMPT,
        model=model,
        toolkit=toolkit,
        memory=memory,
    )

    # Start interaction
    print(f"🤖 test-agent is ready! Type 'exit' to quit.")
    print(f"   Agent Type: basic")
    print(f"   Model Provider: openai")
    print()

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break

            response = await agent(user_input)
            print(f"\ntest-agent: {response}")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")


if __name__ == "__main__":
    asyncio.run(main())
