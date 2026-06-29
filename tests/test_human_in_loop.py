import pytest
from app.agent import create_agent
from langchain.schema import Command

@pytest.mark.asyncio
async def test_human_in_loop():
    agent = create_agent()
    # Prompt that triggers the PythonREPLTool
    prompt = "Run python code: print(2+2)"
    result = await agent.invoke(prompt)
    assert "__interrupt__" in result, "Agent did not pause as expected."
    token = result["__interrupt__"]["token"]
    # Simulate user approving the tool call
    decisions = [
        {"name": "PythonREPLTool", "approved": True, "edited_input": None}
    ]
    resume_result = await agent.invoke(Command(resume={"decisions": decisions}), config={"thread_id": token})
    assert "output" in resume_result, "Agent did not produce output after resumption."
    assert "4" in resume_result["output"], "Unexpected output from PythonREPLTool."
