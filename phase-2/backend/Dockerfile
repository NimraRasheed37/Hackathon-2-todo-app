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
COPY alembic/ ./alembic/
COPY alembic.ini .

# Copy entrypoint script
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

USER appuser

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Environment variable to control run mode: api (default), consumer, or both
ENV RUN_MODE=api

# Use entrypoint script to handle different run modes
ENTRYPOINT ["/docker-entrypoint.sh"]

# Default command (for api mode)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
