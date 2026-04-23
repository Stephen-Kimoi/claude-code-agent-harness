# Claude Code Agent Harness

Starter project for the **[Build Your First Agent Harness with Claude Code](https://lablab.ai/t/claude-code-agent-harness)** tutorial on Lablab.

A codebase health agent that autonomously finds and fixes bugs in a Python project using the [Claude Agent SDK](https://code.claude.com/docs/en/agent-sdk/overview). Point it at a buggy repo, and it runs tests, reads failures, edits source files, and verifies fixes — no human intervention required.

## What's in this repo

| File | Purpose |
|---|---|
| `stats.py` | Python utility library with 3 seeded bugs |
| `test_stats.py` | pytest suite — 4 failures out of 6 tests at the start |
| `CLAUDE.md` | Agent instructions: run tests first, never touch test files, verify after fixing |
| `agent.py` | Claude Agent SDK script that drives the whole thing |

## Quickstart

**Prerequisites:** Python 3.10+, an [Anthropic API key](https://platform.claude.com/)

```bash
git clone https://github.com/Stephen-Kimoi/claude-code-agent-harness.git
cd claude-code-agent-harness
python3 -m venv venv
source venv/bin/activate
pip install claude-agent-sdk pytest
export ANTHROPIC_API_KEY=your-api-key-here
```

Confirm the tests are failing:

```bash
pytest test_stats.py -v
# 4 failed, 2 passed
```

Run the agent:

```bash
python3 agent.py
```

The agent runs `pytest`, reads the failures, fixes each bug in `stats.py`, and runs `pytest` again to verify. All 6 tests pass at the end.

## The three bugs

| Function | Bug | Fix |
|---|---|---|
| `mean` | Subtracts 1 from every result (`/ len - 1`) | Remove the `- 1` |
| `median` | Even-length lists return wrong middle element | Average the two middle elements |
| `normalize` | `ZeroDivisionError` when all values are equal | Guard against zero range |

## How the harness works

The agent is controlled by three things:

- **`CLAUDE.md`** — persistent instructions loaded every session. Tells the agent to run tests before and after, never modify test files, and report what it fixed.
- **`allowed_tools`** — permission boundary. Only `Read`, `Bash`, `Edit`, and `Grep` are available. File creation and network access are blocked.
- **`permission_mode="acceptEdits"`** — auto-approves file edits for a trusted local task.

## Learn more

Full tutorial: [lablab.ai/t/claude-code-agent-harness](https://lablab.ai/t/claude-code-agent-harness)

Claude Agent SDK docs: [code.claude.com/docs/en/agent-sdk/overview](https://code.claude.com/docs/en/agent-sdk/overview)
