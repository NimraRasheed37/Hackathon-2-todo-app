"""Prometheus metrics middleware for FastAPI."""
import time
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Metrics definitions
HTTP_REQUESTS_TOTAL = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"]
)

HTTP_REQUEST_DURATION_SECONDS = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path"],
    buckets=[0.01, 0.025, 0.05, 0.075, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0]
)

HTTP_REQUESTS_IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "HTTP requests currently in progress",
    ["method", "path"]
)

# Task-specific metrics
TASK_OPERATIONS_TOTAL = Counter(
    "task_operations_total",
    "Total task operations",
    ["operation", "status"]
)

KAFKA_MESSAGES_PRODUCED_TOTAL = Counter(
    "kafka_messages_produced_total",
    "Total Kafka messages produced",
    ["topic", "event_type"]
)

KAFKA_MESSAGES_CONSUMED_TOTAL = Counter(
    "kafka_messages_consumed_total",
    "Total Kafka messages consumed",
    ["topic", "event_type", "status"]
)

DATABASE_CONNECTIONS_ACTIVE = Gauge(
    "database_connections_active",
    "Active database connections"
)

DATABASE_CONNECTION_ERRORS_TOTAL = Counter(
    "database_connection_errors_total",
    "Total database connection errors"
)


def normalize_path(path: str) -> str:
    """Normalize path for metrics labels (replace IDs with placeholders)."""
    parts = path.split("/")
    normalized = []
    for i, part in enumerate(parts):
        # Replace numeric IDs with placeholder
        if part.isdigit():
            normalized.append("{id}")
        # Replace UUIDs with placeholder
        elif len(part) == 36 and part.count("-") == 4:
            normalized.append("{uuid}")
        else:
            normalized.append(part)
    return "/".join(normalized)


class PrometheusMiddleware(BaseHTTPMiddleware):
    """Middleware to collect HTTP metrics for Prometheus."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        method = request.method
        path = normalize_path(request.url.path)

        # Skip metrics endpoint to avoid recursion
        if path == "/metrics":
            return await call_next(request)

        # Track in-progress requests
        HTTP_REQUESTS_IN_PROGRESS.labels(method=method, path=path).inc()

        # Time the request
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            status = response.status_code
        except Exception as e:
            status = 500
            raise e
        finally:
            # Record metrics
            duration = time.perf_counter() - start_time

            HTTP_REQUESTS_TOTAL.labels(
                method=method,
                path=path,
                status=str(status)
            ).inc()

            HTTP_REQUEST_DURATION_SECONDS.labels(
                method=method,
                path=path
            ).observe(duration)

            HTTP_REQUESTS_IN_PROGRESS.labels(method=method, path=path).dec()

        return response


def get_metrics() -> bytes:
    """Generate Prometheus metrics output."""
    return generate_latest()


def get_metrics_content_type() -> str:
    """Get the content type for Prometheus metrics."""
    return CONTENT_TYPE_LATEST


# Helper functions for instrumenting application code

def record_task_operation(operation: str, success: bool = True):
    """Record a task operation metric."""
    status = "success" if success else "failure"
    TASK_OPERATIONS_TOTAL.labels(operation=operation, status=status).inc()


def record_kafka_produced(topic: str, event_type: str):
    """Record a Kafka message produced."""
    KAFKA_MESSAGES_PRODUCED_TOTAL.labels(topic=topic, event_type=event_type).inc()


def record_kafka_consumed(topic: str, event_type: str, success: bool = True):
    """Record a Kafka message consumed."""
    status = "success" if success else "failure"
    KAFKA_MESSAGES_CONSUMED_TOTAL.labels(
        topic=topic,
        event_type=event_type,
        status=status
    ).inc()


def record_database_error():
    """Record a database connection error."""
    DATABASE_CONNECTION_ERRORS_TOTAL.inc()


def set_active_connections(count: int):
    """Set the current number of active database connections."""
    DATABASE_CONNECTIONS_ACTIVE.set(count)
