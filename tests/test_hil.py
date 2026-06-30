import pytest
from callbacks import HumanInTheLoopMiddleware, InterruptException

def test_hil_middleware_reject(monkeypatch):
    """
    Test that the middleware raises an InterruptException when the user rejects a tool call.
    """
    middleware = HumanInTheLoopMiddleware()

    # Simulate user input 'n' for rejection
    monkeypatch.setattr("builtins.input", lambda *args: "n")

    serialized = {"name": "calculator"}
    inputs = {"a": 1, "b": 2}

    with pytest.raises(InterruptException) as excinfo:
        middleware.on_tool_start(serialized, inputs)

    payload = excinfo.value.payload
    assert payload["__interrupt__"] is True
    assert payload["action_requests"][0]["name"] == "calculator"
    assert payload["action_requests"][0]["arguments"] == {"a": 1, "b": 2}
