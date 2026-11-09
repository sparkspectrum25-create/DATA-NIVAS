import hmac

from fastapi import Header, HTTPException

from .config import settings


def require_token(authorization: str | None = Header(default=None)) -> None:
    if not settings.token:
        raise HTTPException(status_code=503, detail="server token not configured")
    expected = f"Bearer {settings.token}"
    if not authorization or not hmac.compare_digest(authorization, expected):
        raise HTTPException(status_code=401, detail="unauthorized")
