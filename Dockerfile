# Multi-stage build for AgentScope Initializr Web Service
# Target: Linux AMD64
# Supports offline deployment - all dependencies bundled in image
# No external network access required at runtime

# Stage 1: Builder - download and bundle all dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system dependencies for building
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    wget \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Create vendor directories for offline packages
RUN mkdir -p /app/vendor/lib /app/vendor/npm

# Install Python packages to vendor directory (for offline deployment)
RUN pip install --no-cache-dir --target=/app/vendor/lib -i https://mirrors.aliyun.com/pypi/simple/ \
    fastapi \
    uvicorn \
    h11 \
    python-multipart \
    aiofiles \
    agentscope \
    click \
    jinja2 \
    python-dotenv

# Download frontend packages
COPY initializr-web/frontend/package.json ./initializr-web/frontend/
WORKDIR /app/initializr-web/frontend
RUN npm config set registry https://registry.npmmirror.com && npm install --prefer-offline --no-audit --progress=false

# Copy project source
WORKDIR /app
COPY initializr-core ./initializr-core
COPY initializr-cli ./initializr-cli
COPY initializr-templates ./initializr-templates
COPY initializr-web/frontend ./initializr-web/frontend
COPY initializr-web/initializr_web ./initializr-web/initializr_web

# Build frontend
WORKDIR /app/initializr-web/frontend
RUN npm run build

# Verify build output
RUN ls -la /app/initializr-web/initializr_web/static/

# Stage 2: Runtime - minimal image with all dependencies bundled
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install only runtime system dependencies
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /app/vendor/lib /app/vendor/lib

# Copy project source
COPY --from=builder /app/initializr-core /app/initializr-core
COPY --from=builder /app/initializr-cli /app/initializr-cli
COPY --from=builder /app/initializr-templates /app/initializr-templates
COPY --from=builder /app/initializr-web/initializr_web /app/initializr-web/initializr_web
COPY --from=builder /app/initializr-web/initializr_web/static /app/initializr-web/initializr_web/static

# Set environment variables
ENV PYTHONPATH=/app/vendor/lib:/app/initializr-core:/app/initializr-cli:/app/initializr-web
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["python", "-m", "initializr_web"]
