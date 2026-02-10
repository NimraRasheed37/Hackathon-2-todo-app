#!/bin/bash
set -e

# Docker entrypoint script for Todo Backend
# Supports different run modes via RUN_MODE environment variable:
# - api: Run the FastAPI application (default)
# - consumer: Run the Kafka event consumer
# - both: Run both API and consumer (for development)

# Use PORT from environment or default to 8000
PORT="${PORT:-8000}"

case "${RUN_MODE}" in
  api)
    echo "Starting API server on port ${PORT}..."
    exec uvicorn src.main:app --host 0.0.0.0 --port "${PORT}"
    ;;
  consumer)
    echo "Starting event consumer..."
    exec uvicorn src.events.consumer_runner:app --host 0.0.0.0 --port 3500
    ;;
  both)
    echo "Starting both API server and event consumer..."
    # Start consumer in background
    uvicorn src.events.consumer_runner:app --host 0.0.0.0 --port 3500 &
    # Start API in foreground
    exec uvicorn src.main:app --host 0.0.0.0 --port "${PORT}"
    ;;
  *)
    # Default: run whatever command was passed
    exec "$@"
    ;;
esac
