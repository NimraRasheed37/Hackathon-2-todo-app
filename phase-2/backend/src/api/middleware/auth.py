"""JWT authentication middleware for FastAPI."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.core.exceptions import AuthenticationError
from src.core.logging_config import get_logger
from src.core.security import log_security_event, verify_token
from src.schemas.auth import UserInfo

logger = get_logger(__name__)

# HTTPBearer extracts token from Authorization header
security = HTTPBearer(auto_error=True)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserInfo:
    """
    Extract and verify JWT token from Authorization header.

    This dependency can be used on any route to require authentication.
    Returns UserInfo with the authenticated user's details.

    Args:
        credentials: Authorization credentials from HTTPBearer

    Returns:
        UserInfo with authenticated user details

    Raises:
        HTTPException: 401 if token is missing, invalid, or expired
    """
    token = credentials.credentials

    try:
        payload = verify_token(token)

        # Log successful verification
        log_security_event(
            "token_verified",
            user_id=str(payload.sub),
            details={"email": payload.email},
        )

        return UserInfo(
            id=payload.sub,
            email=payload.email,
            name=payload.name,
        )

    except AuthenticationError as e:
        log_security_event(
            "auth_failed",
            details={
                "reason": e.message,
                "error_code": e.error_code,
            },
        )

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
