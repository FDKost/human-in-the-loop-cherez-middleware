# Human-in-the-Loop Agent with Middleware

This project demonstrates how to add a Human-in-the-Loop (HITL) pause to a LangChain agent using custom middleware, memory persistence, and a FastAPI backend to resume execution.

## Features

- **HumanInTheLoopMiddleware**: Pauses the agent when a specified tool is called.
- **MemorySaver**: Persists agent state keyed by a unique thread ID.
- **FastAPI Endpoint**: Accepts user decisions and resumes the agent.
- **Integration Tests**: Simulate the pause, approval, and resumption flow.

## Setup

```bash
# Clone the repo
git clone https://github.com/yourusername/hitl-agent.git
cd hitl-agent

# Create a virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your OpenAI API key
export OPENAI_API_KEY="your-openai-key"
```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API

### POST /approve

```json
{
  "token": "unique-thread-id",
  "decisions": [
    {
      "name": "PythonREPLTool",
      "approved": true,
      "edited_input": null
    }
  ]
}
```

The endpoint returns the agent's output after resumption.

## Testing

```bash
pytest
```

The test suite simulates a full HITL cycle.

## License

MIT License
