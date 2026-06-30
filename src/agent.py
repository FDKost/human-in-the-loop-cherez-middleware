import json
from typing import Dict, Any, List
from langchain_core.agents import BaseMiddleware
from langchain.memory import MemorySaver
from langchain.tools import tool
from langchain.chat_models import ChatOpenAI
from langchain_core.agents import ConversationalAgent
from langchain.agents import AgentExecutor

class HumanInTheLoopMiddleware(BaseMiddleware):
    """
    Middleware that pauses the chain when a tool call is about to be executed.
    It returns an interrupt response containing the pending tool calls.
    """
    def __init__(self, thread_id: str):
        self.thread_id = thread_id

    async def __call__(self, chain_state: Dict[str, Any], next):
        tool_calls = chain_state.get("tool_calls")
        if tool_calls:
            print(f"\n[Human-in-the-Loop] Thread {self.thread_id}: Tool calls detected:")
            for i, call in enumerate(tool_calls):
                name = call.get("name")
                args = call.get("arguments", {})
                print(f"  {i+1}. Tool '{name}' with arguments {args}")
            # Interrupt the chain and return the action requests
            return {
                "__interrupt__": True,
                "action_requests": tool_calls,
                "review_configs": []
            }
        # Continue the chain normally
        return await next(chain_state)

@tool
def Command(resume: Dict[str, Any]):
    """
    Tool used to resume the chain after a Human-in-the-Loop interruption.
    The resume argument should contain a list of decisions.
    """
    return resume

def create_agent(thread_id: str) -> AgentExecutor:
    """
    Create a LangChain agent with Human-in-the-Loop middleware,
    interrupt_on for tools, description_prefix, and MemorySaver checkpointer.
    """
    llm = ChatOpenAI(temperature=0)
    calculator_tool = tool(
        name="calculator",
        description="A simple calculator that can add, subtract, multiply, or divide two numbers.",
        func=lambda a: a  # placeholder, will be overridden by the tool's JSON schema
    )
    # Use the built-in Calculator tool from langchain.tools
    from langchain.tools import Calculator
    calculator_tool = Calculator()

    agent = ConversationalAgent(
        llm=llm,
        description="You are a helpful assistant."
    )
    agent.description_prefix = "You are a helpful assistant."
    agent.set_interrupt_on(["calculator", "Command"])

    agent_executor = AgentExecutor(
        agent=agent,
        tools=[calculator_tool, Command],
        memory=MemorySaver(),
        verbose=True,
        middleware=[HumanInTheLoopMiddleware(thread_id)],
    )
    return agent_executor
