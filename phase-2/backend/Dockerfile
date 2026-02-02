# Build stage
FROM python:3.13-slim AS builder

WORKDIR /app

# Install build dependencies
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Create non-root user
RUN adduser --disabled-password --gecos "" appuser

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY src/ ./src/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Run the application using shell form to allow $PORT substitution
# Railway sets PORT env var; fallback to 8000 for local development
CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8000}
