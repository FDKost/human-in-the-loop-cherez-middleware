import uuid
from langchain import OpenAI
from langchain.agents import initialize_agent
from langchain.tools import CalculatorTool
from langchain.callbacks.manager import CallbackManager
from callbacks import HumanInTheLoopMiddleware, InterruptException
from langgraph.checkpoint.memory import MemorySaver
from langgraph import Command

def main():
    # Initialize LLM
    llm = OpenAI(temperature=0)

    # Define tools
    calculator = CalculatorTool()
    tools = [calculator]

    # Set up Human-in-the-Loop middleware
    hil_middleware = HumanInTheLoopMiddleware()
    callback_manager = CallbackManager([hil_middleware])

    # Memory saver for state persistence
    memory_saver = MemorySaver()

    # Create the agent executor
    agent = initialize_agent(
        tools,
        llm,
        agent="zero-shot-react-description",
        handle_parsing_errors=True,
        callback_manager=callback_manager,
        memory=memory_saver,
    )

    # Unique thread identifier for this conversation
    thread_id = str(uuid.uuid4())
    config = {"thread_id": thread_id}

    # Initial agent invocation
    try:
        result = agent.invoke({"input": "What is 2+2?"}, config=config)
    except InterruptException as e:
        result = e.payload

    # Handle potential pauses
    while isinstance(result, dict) and result.get("__interrupt__"):
        action_requests = result.get("action_requests", [])
        decisions = []

        for ar in action_requests:
            tool_name = ar.get("name", "unknown_tool")
            args = ar.get("arguments", {})
            print(f"\n[Review] Tool: {tool_name}")
            print(f"[Review] Arguments: {args}")
            print("[Review] Approve? (y/n): ", end="")

            choice = input().strip().lower()
            if choice in ("y", "yes"):
                decisions.append(
                    {"type": "approve", "message": f"Approved {tool_name}"}
                )
            else:
                decisions.append(
                    {"type": "reject", "message": f"Rejected {tool_name}"}
                )

        # Resume agent execution with decisions
        cmd = Command(resume={"decisions": decisions})
        try:
            result = agent.invoke(
                {"input": "Continue"}, config=config, command=cmd
            )
        except InterruptException as e:
            result = e.payload

    # Final output
    print("\n[Result] Agent finished with output:")
    print(result)

if __name__ == "__main__":
    main()
