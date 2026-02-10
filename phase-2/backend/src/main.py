"""FastAPI application entry point."""

import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from src.api.routes import chat, tasks, recurring, reminders, notifications, tags, search, subscriptions
from src.middleware.metrics import PrometheusMiddleware, get_metrics, get_metrics_content_type
from src.config import get_settings
from src.core.exceptions import (
    AuthenticationError,
    AuthorizationError,
    TaskNotFoundError,
)
from src.core.logging_config import get_logger, setup_logging
from src.database import create_db_and_tables, engine
from src.schemas.task import ErrorResponse

# Initialize logging
setup_logging()
logger = get_logger(__name__)

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup and shutdown."""
    # Startup
    logger.info("Starting application...")

    # Verify database connection
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            result.fetchone()
            logger.info("Database connection verified successfully")

            # Log connection pool status
            pool = engine.pool
            logger.info(
                f"Connection pool status: size={pool.size()}, "
                f"checked_in={pool.checkedin()}, checked_out={pool.checkedout()}"
            )
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise SystemExit("Cannot start application without database connection")

    # Create tables
    try:
        create_db_and_tables()
        logger.info("Database tables created/verified successfully")

        # Verify indexes
        with engine.connect() as conn:
            result = conn.execute(
                text(
                    "SELECT indexname FROM pg_indexes WHERE tablename = 'tasks'"
                )
            )
            indexes = [row[0] for row in result.fetchall()]
            logger.info(f"Indexes on tasks table: {indexes}")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise SystemExit("Cannot start application without database tables")

    logger.info("Application startup complete")
    yield

    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI app
app = FastAPI(
    title="Todo Backend API",
    description="RESTful API for task management with user-scoped data isolation",
    version="1.0.0",
    lifespan=lifespan,
)


# Add Prometheus metrics middleware (must be added first to capture all requests)
app.add_middleware(PrometheusMiddleware)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID to each request."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    logger.info(f"Request started: {request.method} {request.url.path} [request_id={request_id}]")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    logger.info(
        f"Request completed: {request.method} {request.url.path} "
        f"[request_id={request_id}] [status={response.status_code}]"
    )
    return response


# Exception handlers
@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(request: Request, exc: TaskNotFoundError):
    """Handle TaskNotFoundError."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Task not found: {exc} [request_id={request_id}]")
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            detail="Task not found",
            error_code="NOT_FOUND",
        ).model_dump(),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    request_id = getattr(request.state, "request_id", "unknown")
    errors = exc.errors()

    # Get first error for response
    first_error = errors[0] if errors else {"msg": "Validation error", "loc": []}
    field = first_error.get("loc", [])[-1] if first_error.get("loc") else None
    message = first_error.get("msg", "Validation error")

    logger.warning(f"Validation error: {message} [request_id={request_id}]")
    return JSONResponse(
        status_code=400,
        content=ErrorResponse(
            detail=message,
            error_code="VALIDATION_ERROR",
            field=str(field) if field else None,
        ).model_dump(),
    )


@app.exception_handler(AuthenticationError)
async def authentication_error_handler(request: Request, exc: AuthenticationError):
    """Handle AuthenticationError - 401 Unauthorized."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Authentication failed: {exc.message} [request_id={request_id}]")
    return JSONResponse(
        status_code=401,
        content=ErrorResponse(
            detail=exc.message,
            error_code=exc.error_code or "AUTHENTICATION_ERROR",
        ).model_dump(),
        headers={"WWW-Authenticate": "Bearer"},
    )


@app.exception_handler(AuthorizationError)
async def authorization_error_handler(request: Request, exc: AuthorizationError):
    """Handle AuthorizationError - 403 Forbidden."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"Authorization failed: {exc.message} [request_id={request_id}]")
    return JSONResponse(
        status_code=403,
        content=ErrorResponse(
            detail=exc.message,
            error_code=exc.error_code or "ACCESS_DENIED",
        ).model_dump(),
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTPException."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(f"HTTP error: {exc.detail} [request_id={request_id}]")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            error_code="HTTP_ERROR",
        ).model_dump(),
        headers=exc.headers,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions."""
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(f"Unexpected error: {exc} [request_id={request_id}]", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            detail="An unexpected error occurred. Please try again later.",
            error_code="INTERNAL_ERROR",
        ).model_dump(),
    )


# Health check endpoints for Kubernetes probes

@app.get("/", tags=["health"])
async def root_health_check():
    """Root health check endpoint (legacy)."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "database": "disconnected"},
        )


@app.get("/health", tags=["health"])
async def liveness_check():
    """Liveness probe - is the application running?

    Used by Kubernetes to determine if the container should be restarted.
    Returns 200 if the application process is alive.
    """
    return {"status": "alive"}


@app.get("/ready", tags=["health"])
async def readiness_check():
    """Readiness probe - is the application ready to serve traffic?

    Used by Kubernetes to determine if the pod should receive traffic.
    Checks database connectivity before returning ready status.
    """
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": "disconnected"},
        )


@app.get("/metrics", tags=["monitoring"])
async def metrics():
    """Prometheus metrics endpoint.

    Exposes application metrics in Prometheus format for scraping.
    """
    return Response(
        content=get_metrics(),
        media_type=get_metrics_content_type(),
    )


# Include routers
app.include_router(tasks.router, prefix="/api", tags=["tasks"])
app.include_router(recurring.router, prefix="/api", tags=["recurring"])
app.include_router(reminders.router, prefix="/api", tags=["reminders"])
app.include_router(notifications.router, prefix="/api", tags=["notifications"])
app.include_router(tags.router, prefix="/api", tags=["tags"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(subscriptions.router, tags=["subscriptions"])
app.include_router(chat.router, prefix="/api", tags=["chat"])
