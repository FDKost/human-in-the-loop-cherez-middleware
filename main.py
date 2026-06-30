import os
from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.tools import tool
from langgraph.agents import create_agent
from langgraph.moderation import HumanInTheLoopMiddleware
from langgraph.checkpoint.memory import MemorySaver
from langgraph import Command

# Ensure OpenAI API key is set
if "OPENAI_API_KEY" not in os.environ:
    raise RuntimeError("Please set the OPENAI_API_KEY environment variable.")

# Initialize LLM
llm = ChatOpenAI(temperature=0)

# Define a simple tool that requires approval
@tool
def dummy_tool(input: str) -> str:
    """A dummy tool that returns a string requiring user approval."""
    return f"Tool executed with input: {input}"

# Create the agent with Human-in-the-Loop middleware
agent = create_agent(
    llm=llm,
    tools=[dummy_tool],
    checkpointer=MemorySaver(),
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on=["dummy_tool"],
            description_prefix="Please review the following tool request:",
        )
    ],
)

app = FastAPI(title="Human-in-the-Loop Agent")

class RunRequest(BaseModel):
    message: str
    thread_id: str

class Decision(BaseModel):
    type: str  # "approve" or "reject"
    message: str | None = None

class ResumeRequest(BaseModel):
    thread_id: str
    decisions: list[Decision]

def _invoke_agent(message: str | None, thread_id: str, decisions: list[dict] | None = None):
    config = {"configurable": {"thread_id": thread_id}}
    if decisions is None:
        # First invocation with user message
        result = agent.invoke({"input": message}, config=config)
    else:
        # Resume invocation with decisions
        result = agent.invoke(Command(resume={"decisions": decisions}), config=config)
    return result

@app.post("/run")
async def run_agent(req: RunRequest):
    result = _invoke_agent(req.message, req.thread_id)
    if "__interrupt__" in result:
        # Return the interrupt information to the client
        return {"interrupt": result["__interrupt__"]}
    return {"output": result}

@app.post("/resume")
async def resume_agent(req: ResumeRequest):
    # Convert Decision objects to dicts
    decisions = [d.dict() for d in req.decisions]
    result = _invoke_agent(None, req.thread_id, decisions=decisions)
    if "__interrupt__" in result:
        return {"interrupt": result["__interrupt__"]}
    return {"output": result}
