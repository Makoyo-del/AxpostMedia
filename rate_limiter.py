import time
from threading import Lock
from fastapi import HTTPException

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

class TokenBucket:
    def __init__(self, capacity: int, fill_rate: float):
        self.capacity = float(capacity)
        self._tokens = float(capacity)
        self.fill_rate = float(fill_rate)  # tokens per second
        self.last_update = time.monotonic()
        self.lock = Lock()

    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.last_update
            self._tokens = min(self.capacity, self._tokens + elapsed * self.fill_rate)
            self.last_update = now
            
            if self._tokens >= tokens:
                self._tokens -= tokens
                return True
            return False

# 50 requests per hour = 50 / 3600 tokens per second
rate_limiter = TokenBucket(capacity=50, fill_rate=50/3600)

class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Whitelist stats and static assets from rate limiting
        path = request.url.path
        if path == "/stats" or path.startswith("/static"):
            return await call_next(request)
            
        if not rate_limiter.consume():
            return JSONResponse(
                status_code=429,
                content={"detail": "Rate limit exceeded. 50 requests/hour limit applied."}
            )
        response = await call_next(request)
        return response
