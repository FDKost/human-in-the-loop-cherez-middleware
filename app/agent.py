from langchain_openai import ChatOpenAI
from langchain.tools import PythonREPLTool
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.memory import MemorySaver
from .middleware import HumanInTheLoopMiddleware

def create_agent() -> AgentExecutor:
    """
    Creates an AgentExecutor with HumanInTheLoopMiddleware and MemorySaver.
    """
    llm = ChatOpenAI(temperature=0)
    tools = [PythonREPLTool()]
    agent = create_openai_tools_agent(llm=llm, tools=tools)
    memory = MemorySaver()
    middleware = HumanInTheLoopMiddleware(interrupt_on=["PythonREPLTool"], memory=memory)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        middleware=[middleware],
        checkpointer=memory,
        max_iterations=5,
    )
    return agent_executor
