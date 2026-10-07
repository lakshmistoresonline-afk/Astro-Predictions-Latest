"""
Request Correlation ID Middleware for Astrovision.
Attaches a unique X-Request-ID header to every request/response for 100% request traceability.
"""
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID")
        if not request_id or not request_id.strip():
            request_id = f"req_{uuid.uuid4().hex[:12]}"
        else:
            request_id = request_id.strip()

        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
