# Human-in-the-Loop Agent Demo

This project demonstrates how to use LangGraph's `HumanInTheLoopMiddleware` to pause an agent for human approval before executing a tool.

## Prerequisites

- Python 3.10+
- pip

## Installation

```bash
pip install -r requirements.txt
```

## Running the Demo

```bash
python main.py
```

The script will:

1. Invoke the agent with a simple echo tool.
2. Pause and ask for human approval.
3. Resume execution based on your decisions.

## Project Structure

- `main.py` – The main script that sets up the agent and demonstrates the workflow.
- `requirements.txt` – Python dependencies.
- `README.md` – This file.

## Notes

- The demo uses a simple echo tool; no OpenAI API key is required.
- You can replace the echo tool with any function or LLM chain.
