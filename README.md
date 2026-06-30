# Human-in-the-Loop Agent with Middleware

This project demonstrates how to build a LangChain agent that pauses execution when a tool call is about to be executed, allowing a human to approve, reject, or edit the action before it proceeds. The agent uses:

- **HumanInTheLoopMiddleware** – a custom middleware that intercepts tool calls.
- **MemorySaver** – a simple in-memory checkpointer for conversation state.
- **Command tool** – used to resume the chain after a human decision.

## Prerequisites

- Python 3.10+
- An OpenAI API key set in the environment variable `OPENAI_API_KEY`.

## Installation

```bash
git clone https://github.com/your-username/human-in-the-loop-agent.git
cd human-in-the-loop-agent
python -m venv .venv
source .venv/bin/activate   # On Windows use `.venv\Scripts\activate`
pip install -r requirements.txt
```

## Usage

```bash
python src/main.py
```

You will be prompted to approve or reject tool calls. For example:

```
[Human-in-the-Loop] Thread session-1: Tool calls detected:
  1. Tool 'calculator' with arguments {'a': 2, 'b': 2, 'operation': 'add'}

Tool 'calculator' with arguments {'a': 2, 'b': 2, 'operation': 'add'}
Approve? (y/n/edit): y

=== Final result ===
{'role': 'assistant', 'content': '4'}
```

## Project Structure

- `src/agent.py` – Defines the middleware, tools, and agent creation function.
- `src/main.py` – Example script that runs the agent and handles interruptions.
- `requirements.txt` – Python dependencies.

## Extending

- Add more tools to the agent by importing them from `langchain.tools` or defining custom ones.
- Modify the middleware to change the prompt format or add timeouts.
- Persist the `MemorySaver` to a database for long‑term conversation history.

## License

MIT License
