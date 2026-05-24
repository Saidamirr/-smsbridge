from __future__ import annotations
import time
from collections import defaultdict, deque

from fastapi import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.core.config import settings
from app.db.session import SessionLocal
from app.models import ApiRequestLog


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.hits: dict[str, deque[float]] = defaultdict(deque)

    async def dispatch(self, request: Request, call_next):
        key = request.client.host if request.client else "unknown"
        now = time.time()
        bucket = self.hits[key]
        while bucket and bucket[0] <= now - 60:
            bucket.popleft()
        if len(bucket) >= settings.rate_limit_per_minute:
            return JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
        bucket.append(now)
        return await call_next(request)


class ApiRequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if request.url.path.startswith(("/api/", "/admin", "/auth")):
            db = SessionLocal()
            try:
                db.add(
                    ApiRequestLog(
                        user_id=getattr(request.state, "user_id", None),
                        endpoint=request.url.path,
                        method=request.method,
                        ip_address=request.client.host if request.client else None,
                        status_code=response.status_code,
                    )
                )
                db.commit()
            finally:
                db.close()
        return response
