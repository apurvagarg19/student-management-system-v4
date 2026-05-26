import time
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request


logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.time()

        logger.info(
            f"Request Started | "
            f"Method={request.method} "
            f"Path={request.url.path}"
        )

        try:
            response = await call_next(request)

            execution_time = time.time() - start_time

            logger.info(
                f"Request Completed | "
                f"Method={request.method} "
                f"Path={request.url.path} "
                f"Status={response.status_code} "
                f"Time={execution_time:.4f}s"
            )

            return response

        except Exception as e:

            execution_time = time.time() - start_time

            logger.exception(
                f"Request Failed | "
                f"Method={request.method} "
                f"Path={request.url.path} "
                f"Time={execution_time:.4f}s "
                f"Error={str(e)}"
            )

            raise