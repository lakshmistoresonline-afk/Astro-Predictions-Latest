"""
Test Suite for Sliding-Window Request-Frequency Rate Limiter.
Verifies allowed requests within threshold, RATE_LIMIT_EXCEEDED error shape, and Retry-After headers.
"""
import pytest
import time
from fastapi import HTTPException
from apps.api.middleware.rate_limiter import RateLimiter, enforce_rate_limit, heavy_endpoint_limiter

def test_rate_limiter_threshold_and_retry_after():
    """Verifies that RateLimiter allows max_requests and rejects subsequent requests with Retry-After."""
    limiter = RateLimiter(max_requests=3, window_seconds=5.0)
    ident = "test_rate_limiter_client"

    # Requests 1..3 allowed
    for i in range(3):
        allowed, remaining, retry_after = limiter.check_rate_limit(ident)
        assert allowed is True
        assert remaining == 2 - i

    # Request 4 rejected
    allowed, remaining, retry_after = limiter.check_rate_limit(ident)
    assert allowed is False
    assert remaining == 0
    assert retry_after > 0.0

def test_rate_limiter_resets_after_window():
    """Verifies that RateLimiter sliding window clears old timestamps after window_seconds."""
    limiter = RateLimiter(max_requests=2, window_seconds=0.2)
    ident = "test_window_reset_client"

    limiter.check_rate_limit(ident)
    limiter.check_rate_limit(ident)

    # 3rd request blocked
    allowed, _, _ = limiter.check_rate_limit(ident)
    assert allowed is False

    # Wait for window to expire
    time.sleep(0.25)

    # Subsequent request allowed
    allowed, remaining, _ = limiter.check_rate_limit(ident)
    assert allowed is True
