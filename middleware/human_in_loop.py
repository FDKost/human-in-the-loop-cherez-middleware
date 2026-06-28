import asyncio
import logging
import uuid
from typing import Dict

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# In-memory store for pending requests
pending_requests: Dict[str, asyncio.Future] = {}

logger = logging.getLogger("human_in_loop")

class HumanInLoopMiddleware(BaseHTTPMiddleware):
    """
    Middleware that intercepts incoming requests, queues them for manual review,
    and waits for an approval or rejection before proceeding.
    """

    def __init__(self, app, timeout: int = 30, fallback: str = "reject"):
        super().__init__(app)
        self.timeout = timeout
        self.fallback = fallback.lower()
        if self.fallback not in {"approve", "reject"}:
            raise ValueError("fallback must be 'approve' or 'reject'")

    async def dispatch(self, request: Request, call_next):
        # Read the body so we can forward it later
        body = await request.body()
        request_id = str(uuid.uuid4())

        # Create a future that will be set by the review endpoint
        future = asyncio.get_event_loop().create_future()
        pending_requests[request_id] = future

        logger.info(f"Request queued for review: id={request_id}")

        # Optionally notify a Slack channel or send an email here
        # For simplicity, we just log the event

        try:
            # Wait for the review result with timeout
            result = await asyncio.wait_for(future, timeout=self.timeout)
        except asyncio.TimeoutError:
            logger.warning(f"Review timeout for request {request_id}")
            result = self.fallback
        except Exception as exc:
            logger.exception(f"Error while waiting for review of request {request_id}")
            result = "reject"

        # Clean up the pending request
        pending_requests.pop(request_id, None)

        if result == "approve":
            # Reset the request body so downstream handlers can read it
            request._body = body
            response: Response = await call_next(request)
            return response
        else:
            return JSONResponse(
                status_code=403,
                content={"detail": "Request rejected by human review"},
            )
