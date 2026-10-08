"""
Sliding-Window Request-Frequency Rate Limiter for Astrovision.
Protects heavy computational API endpoints against rapid request-frequency abuse.
Operates independently from daily free-tier usage quotas!
Returns HTTP 429 with error_code 'RATE_LIMIT_EXCEEDED'.
"""
import time
import threading
from typing import Dict, List, Tuple
from fastapi import Request, HTTPException, status
from apps.api.config import settings

class RateLimiter:
    """Thread-safe sliding-window request frequency rate limiter."""

    def __init__(self, max_requests: int = 5, window_seconds: float = 10.0):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: Dict[str, List[float]] = {}
        self._lock = threading.Lock()

    def check_rate_limit(self, identifier: str) -> Tuple[bool, int, float]:
        """
        Checks if identifier has exceeded request frequency limit.
        Returns (is_allowed, remaining_requests, retry_after_seconds).
        """
        now = time.time()
        cutoff = now - self.window_seconds

        with self._lock:
            timestamps = self._requests.get(identifier, [])
            timestamps = [t for t in timestamps if t > cutoff]

            if len(timestamps) >= self.max_requests:
                oldest = timestamps[0]
                retry_after = round(self.window_seconds - (now - oldest), 1)
                self._requests[identifier] = timestamps
                return False, 0, max(1.0, retry_after)

            timestamps.append(now)
            self._requests[identifier] = timestamps
            remaining = self.max_requests - len(timestamps)
            return True, remaining, 0.0

# Singleton global instance for heavy endpoints (5 requests per 10s per client/user)
heavy_endpoint_limiter = RateLimiter(max_requests=5, window_seconds=10.0)

def enforce_rate_limit(request: Request, identifier: str) -> None:
    """Enforces request frequency rate limit or raises HTTP 429 RATE_LIMIT_EXCEEDED."""
    allowed, remaining, retry_after = heavy_endpoint_limiter.check_rate_limit(identifier)
    if not allowed:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "message": f"Too many requests. Rate limit of {heavy_endpoint_limiter.max_requests} requests per {int(heavy_endpoint_limiter.window_seconds)}s exceeded.",
                "error_code": "RATE_LIMIT_EXCEEDED",
                "retry_after_seconds": retry_after,
                "remaining": 0
            },
            headers={"Retry-After": str(int(retry_after))}
        )
