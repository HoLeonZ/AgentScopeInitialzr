# Multi-stage build for AgentScope Initializr Web Service
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e .

# Build frontend assets
COPY initializr-web/frontend ./initializr-web/frontend
RUN cd initializr-web/frontend && npm install && npm run build

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
COPY pyproject.toml ./
RUN pip install --no-cache-dir -e ".[web]"

# Copy built artifacts from builder
COPY --from=builder /app/initializr-web/initializr_web ./initializr-web/initializr_web
COPY --from=builder /app/initializr-web/frontend/dist ./initializr-web/initializr_web/static
COPY --from=builder /app/initializr-core ./initializr-core
COPY --from=builder /app/initializr-cli ./initializr-cli
COPY --from=builder /app/initializr-templates ./initializr-templates

# Create directories for generated projects
RUN mkdir -p /app/output

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the web service
CMD ["uvicorn", "initializr_web.api:app", "--host", "0.0.0.0", "--port", "8000"]
