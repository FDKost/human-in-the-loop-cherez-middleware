from langchain.callbacks.base import BaseCallbackHandler
import json

class InterruptException(Exception):
    """Custom exception to interrupt agent execution and pass payload."""
    def __init__(self, payload):
        super().__init__("Agent interrupted by HumanInTheLoopMiddleware")
        self.payload = payload

class HumanInTheLoopMiddleware(BaseCallbackHandler):
    """
    Middleware that intercepts tool calls, prompts the user for approval,
    and can interrupt the agent if the user rejects the tool invocation.
    """
    def __init__(self):
        super().__init__()

    def on_tool_start(
        self,
        serialized,
        inputs,
        run_id=None,
        parent_run_id=None,
        tags=None,
        metadata=None,
    ):
        """
        Called before a tool is executed. Prompts the user for approval.
        If the user rejects, raises InterruptException with a payload
        that signals the agent to pause.
        """
        tool_name = serialized.get("name", "unknown_tool")
        tool_args = inputs

        print(f"\n[HumanInTheLoop] Tool call detected: {tool_name}")
        print(f"[HumanInTheLoop] Arguments: {json.dumps(tool_args)}")
        print("[HumanInTheLoop] Approve? (y/n): ", end="")

        choice = input().strip().lower()
        if choice in ("y", "yes"):
            # Allow the tool to run normally
            return None
        else:
            # Interrupt the agent and provide the action request for review
            payload = {
                "__interrupt__": True,
                "action_requests": [
                    {
                        "name": tool_name,
                        "arguments": tool_args,
                    }
                ],
                "review_configs": [],
            }
            raise InterruptException(payload)
