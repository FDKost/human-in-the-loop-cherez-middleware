# Human-in-the-Loop Agent

This project demonstrates a simple LangGraph agent that pauses execution when a tool call requires user approval. The agent uses the `HumanInTheLoopMiddleware` to interrupt on a specific tool, and the `MemorySaver` checkpointer to persist state between requests.

## Features

- Human-in-the-loop via middleware
- Persistent state with `MemorySaver`
- FastAPI API with `/run` and `/resume` endpoints
- Simple dummy tool that requires approval

## Requirements

- Python 3.10+
- OpenAI API key (set `OPENAI_API_KEY` environment variable)

## Installation

```bash
pip install -r requirements.txt
```

## Running the Server

```bash
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

## API Endpoints

### POST /run

Start or continue an agent session.

Request body:
```json
{
  "message": "Your message to the agent",
  "thread_id": "session-1"
}
```

Response:
- If the agent pauses, returns `{"interrupt": {...}}` containing `action_requests` and `review_configs`.
- If the agent finishes, returns `{"output": {...}}`.

### POST /resume

Resume a paused agent session with decisions.

Request body:
```json
{
  "thread_id": "session-1",
  "decisions": [
    {
      "type": "approve",
      "message": null
    },
    {
      "type": "reject",
      "message": "Not needed"
    }
  ]
}
```

Response:
- If the agent pauses again, returns `{"interrupt": {...}}`.
- If the agent finishes, returns `{"output": {...}}`.

## Example Flow

1. Send a request to `/run` with your message.
2. If you receive an `interrupt`, inspect the `action_requests` and decide to approve or reject each.
3. Send a request to `/resume` with your decisions.
4. Repeat until the agent returns an `output`.

## License

MIT
