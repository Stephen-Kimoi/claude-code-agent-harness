import asyncio
import time
from claude_agent_sdk import (
    query,
    ClaudeAgentOptions,
    AssistantMessage,
    UserMessage,
    SystemMessage,
    ResultMessage,
    TextBlock,
    ToolUseBlock,
    ToolResultBlock,
)

# ANSI colors
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
BLUE   = "\033[34m"
MAGENTA = "\033[35m"
RED    = "\033[31m"

TOOL_COLORS = {
    "Bash": CYAN,
    "Read": BLUE,
    "Edit": YELLOW,
    "Grep": MAGENTA,
}


def log_tool_call(block: ToolUseBlock):
    color = TOOL_COLORS.get(block.name, CYAN)
    inp = block.input

    if block.name == "Bash":
        cmd = inp.get("command", "").strip()
        print(f"\n{color}{BOLD}[{block.name}]{RESET} {cmd}")

    elif block.name == "Read":
        path = inp.get("file_path", "")
        limit = inp.get("limit", "")
        suffix = f"  (lines {inp['offset']}–{inp['offset']+limit})" if inp.get("offset") else ""
        print(f"\n{color}{BOLD}[{block.name}]{RESET} {path}{DIM}{suffix}{RESET}")

    elif block.name == "Edit":
        path = inp.get("file_path", "")
        old = inp.get("old_string", "").strip().splitlines()
        new = inp.get("new_string", "").strip().splitlines()
        print(f"\n{color}{BOLD}[{block.name}]{RESET} {path}")
        for line in old[:3]:
            print(f"  {RED}- {line}{RESET}")
        for line in new[:3]:
            print(f"  {GREEN}+ {line}{RESET}")
        if len(old) > 3 or len(new) > 3:
            print(f"  {DIM}... ({max(len(old), len(new))} lines total){RESET}")

    elif block.name == "Grep":
        pattern = inp.get("pattern", "")
        path = inp.get("path", inp.get("include", ""))
        print(f"\n{color}{BOLD}[{block.name}]{RESET} {pattern!r} in {path or '.'}")

    else:
        print(f"\n{color}{BOLD}[{block.name}]{RESET} {str(inp)[:120]}")


def log_tool_result(block: ToolResultBlock):
    if not block.content:
        return
    text = block.content if isinstance(block.content, str) else str(block.content)
    lines = text.strip().splitlines()
    shown = lines[:8]
    print(f"{DIM}", end="")
    for line in shown:
        print(f"  {line}")
    if len(lines) > 8:
        print(f"  ... ({len(lines) - 8} more lines)")
    print(f"{RESET}", end="")


async def main():
    start = time.time()
    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{BOLD}  Codebase Health Agent  —  Claude Agent SDK{RESET}")
    print(f"{BOLD}{'─' * 56}{RESET}\n")

    try:
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
            if isinstance(message, SystemMessage):
                if message.subtype == "init":
                    session_id = message.data.get("session_id", "")
                    print(f"{DIM}session  {session_id}{RESET}\n")

            elif isinstance(message, AssistantMessage):
                for block in message.content:
                    if isinstance(block, TextBlock) and block.text.strip():
                        print(f"\n{DIM}{block.text.strip()}{RESET}")
                    elif isinstance(block, ToolUseBlock):
                        log_tool_call(block)

            elif isinstance(message, UserMessage):
                if isinstance(message.content, list):
                    for block in message.content:
                        if isinstance(block, ToolResultBlock):
                            log_tool_result(block)

            elif isinstance(message, ResultMessage):
                elapsed = time.time() - start
                cost = f"  ${message.total_cost_usd:.4f}" if message.total_cost_usd else ""
                turns = f"  {message.num_turns} turns"
                print(f"\n{BOLD}{GREEN}{'─' * 56}{RESET}")
                print(f"{BOLD}{GREEN}  Done{RESET}{DIM}  {elapsed:.1f}s{turns}{cost}{RESET}")
                print(f"{BOLD}{GREEN}{'─' * 56}{RESET}\n")
                if message.result:
                    print(message.result)

    except Exception as e:
        print(f"\n{RED}{BOLD}Error:{RESET} {e}")


asyncio.run(main())
