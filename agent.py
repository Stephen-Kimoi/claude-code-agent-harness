import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions


async def main():
    print("Starting codebase health agent...\n")

    async for message in query(
        prompt=(
            "Run the test suite to see what is failing. "
            "Read the source files to understand the bugs. "
            "Fix every bug in the source files. "
            "Run the tests again to confirm all tests pass. "
            "Do not modify test files."
        ),
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Bash", "Edit", "Grep"],
            permission_mode="acceptEdits",
        ),
    ):
        if hasattr(message, "text"):
            print(message.text, end="", flush=True)
        elif hasattr(message, "result"):
            print(f"\n\nResult: {message.result}")


asyncio.run(main())
