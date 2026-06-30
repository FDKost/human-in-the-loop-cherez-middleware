# Human-in-the-Loop (HIL) Agent with Middleware

This repository demonstrates how to add a Human-in-the-Loop (HIL) experience to a LangChain agent using a custom middleware. The agent pauses before executing any tool, prompts the user for approval, and can resume execution based on the user's decision. The state is persisted using `MemorySaver` so that the conversation can be resumed seamlessly.

## Features

- **Human-in-the-Loop Middleware** – Intercepts tool calls, displays the tool name and arguments, and asks the user to approve or reject.
- **Interrupt Handling** – If the user rejects a tool call, the agent pauses and returns a structured payload.
- **Decision Collection** – The user can approve or reject each tool invocation. The decisions are collected in the same order as the tool requests.
- **Resume Execution** – The agent can be resumed with a `Command` object containing the decisions.
- **State Persistence** – Uses `MemorySaver` to persist the agent’s state across pauses and resumes.

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/hil-agent.git
   cd hil-agent
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**

   ```bash
   export OPENAI_API_KEY="your-openai-key"
   ```

   On Windows:

   ```cmd
   set OPENAI_API_KEY=your-openai-key
   ```

## Running the Agent

```bash
python main.py
```

You will see prompts like:

```
[HumanInTheLoop] Tool call detected: calculator
[HumanInTheLoop] Arguments: {"a": 2, "b": 2}
[HumanInTheLoop] Approve? (y/n): 
```

Type `y` to approve or `n` to reject. If you reject, the agent will pause and ask you to review the tool request. After making your decisions, the agent will resume execution.

## Testing

The repository includes a simple test for the middleware:

```bash
pytest
```

The test verifies that the middleware correctly interrupts the agent when the user rejects a tool call.

## Customization

- **Tools** – Add or replace tools in `main.py` by importing from `langchain.tools`.
- **Agent Type** – Change the agent type in `initialize_agent` (e.g., `"react"` or `"chat-zero-shot-react-description"`).
- **Middleware Logic** – Modify `callbacks.py` to change how decisions are collected or to add more sophisticated prompts.

## License

MIT License
