import logging
import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv

from middleware.human_in_loop import HumanInLoopMiddleware, pending_requests
from models import ReviewAction

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("app")

app = FastAPI(title="Human-in-the-Loop API")

# Add the Human-in-the-Loop middleware
review_timeout = int(os.getenv("REVIEW_TIMEOUT", "30"))
review_fallback = os.getenv("REVIEW_FALLBACK", "reject")
app.add_middleware(
    HumanInLoopMiddleware,
    timeout=review_timeout,
    fallback=review_fallback,
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

# Sample endpoint that requires human review
@app.post("/process")
async def process_endpoint(data: dict):
    # In a real application, do something with the data
    return {"status": "processed", "data": data}

# Review endpoint for admins
@app.post("/review/{request_id}")
async def review_request(request_id: str, review: ReviewAction):
    future = pending_requests.get(request_id)
    if future is None:
        raise HTTPException(status_code=404, detail="Request ID not found or already reviewed")

    if future.done():
        raise HTTPException(status_code=400, detail="Request already reviewed")

    future.set_result(review.action)
    return {"status": "ok", "request_id": request_id, "action": review.action}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
