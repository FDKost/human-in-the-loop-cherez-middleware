import os
from langgraph import Graph, Tool, HumanInTheLoopMiddleware
from langgraph.types import Command
from langgraph.checkpoint.memory import MemorySaver

# Define a simple echo tool
def echo_func(input: str) -> str:
    return input

echo_tool = Tool(
    name="echo",
    description="Echo the input string",
    func=echo_func
)

# Create the middleware with interrupt_on for the echo tool
middleware = HumanInTheLoopMiddleware(
    interrupt_on={"echo"},
    description_prefix="Please confirm the following action:",
)

# Build the graph
graph = Graph()
graph.add_node("echo", echo_tool)
graph.add_node("middleware", middleware)
graph.set_entry_point("middleware")
graph.connect("middleware", "echo")

# Compile the agent with MemorySaver as checkpointer
agent = graph.compile(checkpointer=MemorySaver())

def run_agent():
    # Invoke the agent with a thread_id
    config = {"configurable": {"thread_id": "session-1"}}
    print("Invoking agent...")
    result = agent.invoke("Hello, world!", config=config)
    print("Result:", result)

    # Check for interrupt
    if "__interrupt__" in result and result["__interrupt__"]:
        print("\nAgent paused for human approval.")
        action_requests = result.get("action_requests", [])
        review_configs = result.get("review_configs", [])
        print("\nAction Requests:")
        for i, req in enumerate(action_requests):
            print(f"{i+1}. {req}")

        print("\nReview Configs:")
        for i, cfg in enumerate(review_configs):
            print(f"{i+1}. {cfg}")

        # Collect decisions
        decisions = []
        for i, req in enumerate(action_requests):
            while True:
                decision = input(f"Approve action {i+1} (approve/reject)? ").strip().lower()
                if decision in {"approve", "reject"}:
                    decisions.append({"action": req, "decision": decision})
                    break
                else:
                    print("Please enter 'approve' or 'reject'.")

        # Resume execution
        resume_command = Command(resume={"decisions": decisions})
        print("\nResuming agent...")
        resume_result = agent.invoke(resume_command, config=config)
        print("\nResume Result:", resume_result)
    else:
        print("\nAgent completed without interruption.")

if __name__ == "__main__":
    run_agent()
