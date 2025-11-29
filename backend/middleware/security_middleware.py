import re

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware


class SecurityMiddleware(BaseHTTPMiddleware):
    """Middleware для защиты от атак"""

    DANGEROUS_PATTERNS = [
        r'<script',
        r'javascript:',
        r'union\s+select',
        r';\s*drop\s+table',
    ]

    async def dispatch(self, request: Request, call_next):
        query_string = str(request.url.query)
        if self._is_dangerous(query_string):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Potentially dangerous request"
            )

        if self._is_dangerous(request.url.path):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid request path"
            )

        response = await call_next(request)

        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Content-Security-Policy"] = "default-src 'self'"

        return response

    def _is_dangerous(self, value: str) -> bool:
        if not value:
            return False
        for pattern in self.DANGEROUS_PATTERNS:
            if re.search(pattern, value.lower(), re.IGNORECASE):
                return True
        return False
