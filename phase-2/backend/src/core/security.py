"""JWT verification and security utilities."""

import uuid
from datetime import datetime, timezone
from typing import Any

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

from src.config import get_settings
from src.core.exceptions import AuthenticationError, AuthorizationError
from src.core.logging_config import get_logger
from src.schemas.auth import TokenPayload, UserInfo

logger = get_logger(__name__)
settings = get_settings()


def verify_token(token: str) -> TokenPayload:
    """
    Verify JWT token and return payload.

    Args:
        token: JWT token string

    Returns:
        TokenPayload with user claims

    Raises:
        AuthenticationError: If token is invalid, expired, or malformed
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret,
            algorithms=[settings.jwt_algorithm],
            options={"require": ["sub", "exp", "iat"]},
        )

        # Parse UUID from sub claim
        try:
            user_id = uuid.UUID(payload["sub"])
        except (ValueError, TypeError) as e:
            raise AuthenticationError("Invalid user ID in token") from e

        return TokenPayload(
            sub=user_id,
            email=payload.get("email", ""),
            name=payload.get("name", ""),
            iat=payload["iat"],
            exp=payload["exp"],
        )

    except ExpiredSignatureError:
        log_security_event(
            "token_expired",
            details={"reason": "Token has expired"},
        )
        raise AuthenticationError("Token has expired", error_code="TOKEN_EXPIRED")

    except InvalidTokenError as e:
        log_security_event(
            "invalid_token",
            details={"reason": str(e)},
        )
        raise AuthenticationError("Invalid token", error_code="INVALID_TOKEN") from e


def extract_user_info(token_payload: TokenPayload) -> UserInfo:
    """
    Extract user information from token payload.

    Args:
        token_payload: Verified token payload

    Returns:
        UserInfo with user details
    """
    return UserInfo(
        id=token_payload.sub,
        email=token_payload.email,
        name=token_payload.name,
    )


def validate_user_authorization(token_user_id: uuid.UUID, path_user_id: str) -> None:
    """
    Validate that the token user ID matches the URL path user ID.

    Args:
        token_user_id: User ID from JWT token
        path_user_id: User ID from URL path

    Raises:
        AuthorizationError: If user IDs don't match
    """
    try:
        path_uuid = uuid.UUID(path_user_id)
    except (ValueError, TypeError) as e:
        raise AuthorizationError("Invalid user ID format in path") from e

    if token_user_id != path_uuid:
        log_security_event(
            "authorization_failed",
            user_id=str(token_user_id),
            details={
                "reason": "User ID mismatch",
                "requested_user_id": path_user_id,
            },
        )
        raise AuthorizationError("Access denied", error_code="ACCESS_DENIED")


def check_token_expiration(exp: int) -> bool:
    """
    Check if token expiration is valid.

    Args:
        exp: Expiration timestamp from token

    Returns:
        True if token is still valid
    """
    current_time = int(datetime.now(timezone.utc).timestamp())
    return exp > current_time


def log_security_event(
    event: str,
    user_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    """
    Log a security event with structured data.

    Args:
        event: Event type (e.g., "login_success", "auth_failed")
        user_id: Optional user ID
        details: Optional additional details
    """
    log_data = {
        "security_event": event,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    if user_id:
        log_data["user_id"] = user_id

    if details:
        log_data.update(details)

    if "failed" in event or "expired" in event or "invalid" in event:
        logger.warning("Security event", extra=log_data)
    else:
        logger.info("Security event", extra=log_data)


def log_logout_event(user_id: str) -> None:
    """
    Log a user logout event.

    Args:
        user_id: ID of the user logging out
    """
    log_security_event(
        "logout",
        user_id=user_id,
        details={"action": "User logged out"},
    )
