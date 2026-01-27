"""Custom exception classes for the backend API."""


class TaskNotFoundError(Exception):
    """Raised when a task is not found or doesn't belong to the user."""

    def __init__(self, task_id: int, user_id: str):
        self.task_id = task_id
        self.user_id = user_id
        super().__init__(f"Task {task_id} not found for user {user_id}")


class ValidationError(Exception):
    """Raised when input validation fails."""

    def __init__(self, message: str, field: str | None = None):
        self.message = message
        self.field = field
        super().__init__(message)


class DatabaseError(Exception):
    """Raised when a database operation fails."""

    def __init__(self, message: str, original_error: Exception | None = None):
        self.message = message
        self.original_error = original_error
        super().__init__(message)


class AuthenticationError(Exception):
    """Raised when authentication fails (invalid/expired token)."""

    def __init__(self, message: str, error_code: str | None = None):
        self.message = message
        self.error_code = error_code
        super().__init__(message)


class AuthorizationError(Exception):
    """Raised when authorization fails (user lacks permission)."""

    def __init__(self, message: str, error_code: str | None = None):
        self.message = message
        self.error_code = error_code
        super().__init__(message)
