from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from .agent import create_agent
from langchain.schema import Command

app = FastAPI()
agent = create_agent()

class Decision(BaseModel):
    name: str
    approved: bool
    edited_input: str | None = None

class ApprovalRequest(BaseModel):
    token: str
    decisions: List[Decision]

@app.post("/approve")
async def approve(request: ApprovalRequest):
    """
    Endpoint to handle user decisions and resume the agent.
    """
    decisions = []
    for d in request.decisions:
        decisions.append({
            "name": d.name,
            "approved": d.approved,
            "edited_input": d.edited_input
        })
    try:
        result = await agent.invoke(Command(resume={"decisions": decisions}), config={"thread_id": request.token})
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
