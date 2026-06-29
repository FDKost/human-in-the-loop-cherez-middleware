from langchain.schema import ToolCall
from langchain.memory import MemorySaver
import uuid
from typing import List, Dict, Any

class HumanInTheLoopMiddleware:
    """
    Middleware that pauses execution when a specified tool is called.
    It injects a unique thread_id into the config and returns an interrupt payload.
    """
    def __init__(self, interrupt_on: List[str], memory: MemorySaver):
        self.interrupt_on = interrupt_on
        self.memory = memory

    async def on_tool_call(self, tool_call: ToolCall, **kwargs) -> Dict[str, Any] | None:
        """
        Intercept tool calls. If the tool name is in interrupt_on, pause execution.
        """
        if tool_call.name in self.interrupt_on:
            token = str(uuid.uuid4())
            # Ensure the config contains the thread_id for persistence
            config = kwargs.get("config", {})
            config["thread_id"] = token
            kwargs["config"] = config
            return {"__interrupt__": {"token": token, "tool_call": tool_call.dict()}}
        return None
