import asyncio
import json
from agent import create_agent

async def main():
    thread_id = "session-1"
    agent = create_agent(thread_id)

    # Initial user message
    user_message = {"role": "user", "content": "Calculate 2 + 2"}
    result = await agent.invoke(
        user_message,
        config={"configurable": {"thread_id": thread_id}}
    )

    # Check for interruption
    if "__interrupt__" in result:
        action_requests = result.get("action_requests", [])
        review_configs = result.get("review_configs", [])
        print("\n=== Interruption detected ===")
        for i, req in enumerate(action_requests, 1):
            print(f"{i}. Tool: {req.get('name')}, Args: {req.get('arguments')}")

        decisions = []
        for req in action_requests:
            tool_name = req.get("name")
            args = req.get("arguments", {})
            print(f"\nTool '{tool_name}' with arguments {args}")
            while True:
                choice = input("Approve? (y/n/edit): ").strip().lower()
                if choice in ("y", "yes"):
                    decisions.append({"type": "approve"})
                    break
                elif choice in ("n", "no"):
                    decisions.append({"type": "reject", "message": "User rejected"})
                    break
                elif choice == "edit":
                    new_args_str = input("Enter new arguments as JSON: ").strip()
                    try:
                        new_args = json.loads(new_args_str)
                        # For simplicity, we treat edit as an approval with new args
                        decisions.append({"type": "approve"})
                        break
                    except json.JSONDecodeError:
                        print("Invalid JSON. Try again.")
                else:
                    print("Please enter 'y', 'n', or 'edit'.")

        # Resume the chain with decisions
        resume_message = {
            "role": "assistant",
            "content": {"Command": {"resume": {"decisions": decisions}}}
        }
        result = await agent.invoke(
            resume_message,
            config={"configurable": {"thread_id": thread_id}}
        )
        if "__interrupt__" in result:
            print("\n=== Second interruption detected ===")
            print(result)
        else:
            print("\n=== Final result ===")
            print(result)
    else:
        print("\n=== Result ===")
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
