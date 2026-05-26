import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimitMiddleware(BaseHTTPMiddleware):

    request_history = {}

    async def dispatch(self, request: Request, call_next):

        client_ip = request.client.host

        current_time = time.time()

        # 1 minute window
        time_window = 60

        # Max requests allowed
        max_requests = 30

        # Existing request timestamps
        request_times = self.request_history.get(client_ip, [])

        # Keep only valid timestamps
        request_times = [
            t for t in request_times
            if current_time - t < time_window
        ]

        # Rate limit check
        if len(request_times) >= max_requests:

            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "message": "Rate limit exceeded",
                    "data": None
                }
            )

        # Add current request time
        request_times.append(current_time)

        # Update memory
        self.request_history[client_ip] = request_times

        # Continue request
        response = await call_next(request)

        return response