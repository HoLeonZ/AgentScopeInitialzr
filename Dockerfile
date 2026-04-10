# Multi-stage build for AgentScope Initializr Web Service
# Target: Linux ARM64 (Optimized)
# All sources are configured for China mirrors
# Explicitly ensures ARM64 compatibility for all dependencies

# Stage 1: Builder - compile frontend and install dependencies
FROM --platform=linux/arm64 python:3.11-slim AS builder

WORKDIR /app

# Configure apt to use Aliyun mirror (China)
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# Install system dependencies for building (cached layer)
# ARM64 specific: Ensure compatible versions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js from NodeSource repository for ARM64
# This ensures we get a recent, ARM64-compatible version
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Verify Node.js architecture
RUN echo "Node.js version: $(node --version)" && \
    echo "Node.js architecture: $(node -p 'process.arch')" && \
    echo "NPM version: $(npm --version)"

# Configure pip to use Aliyun mirror (China)
RUN pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set install.trusted-host mirrors.aliyun.com

# Configure npm to use Taobao mirror (China)
RUN npm config set registry https://registry.npmmirror.com

# Copy dependency files first (for better caching)
COPY pyproject.toml ./
COPY initializr-web/pyproject.toml ./initializr-web/

# Install Python dependencies (cached if pyproject.toml unchanged)
# Note: Using ARM64-optimized dependencies from pyproject.toml (uvicorn without uvloop)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e ".[web]"

# Copy source code (changes frequently, so placed after dependency installation)
COPY initializr-core ./initializr-core
COPY initializr-cli ./initializr-cli
COPY initializr-templates ./initializr-templates

# Build frontend - separate layers for better caching
COPY initializr-web/frontend/package.json ./initializr-web/frontend/
WORKDIR /app/initializr-web/frontend
RUN npm install

# Copy frontend source and build
COPY initializr-web/frontend ./.
COPY initializr-web/initializr_web ../initializr_web
RUN npm run build

# Verify build output
RUN ls -la /app/initializr-web/initializr_web/static/

# Stage 2: Runtime - minimal image with only runtime dependencies
FROM --platform=linux/arm64 python:3.11-slim AS runtime

WORKDIR /app

# Configure apt to use Aliyun mirror (China)
RUN sed -i 's/deb.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources && \
    sed -i 's/security.debian.org/mirrors.aliyun.com/g' /etc/apt/sources.list.d/debian.sources

# Install only runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project code
COPY pyproject.toml ./
COPY initializr-core ./initializr-core
COPY initializr-cli ./initializr-cli
COPY initializr-templates ./initializr-templates
COPY initializr-web/pyproject.toml ./initializr-web/
COPY initializr-web/initializr_web ./initializr-web/initializr_web

# Copy built frontend assets (vite outputs to initializr_web/static)
COPY --from=builder /app/initializr-web/initializr_web/static ./initializr-web/initializr_web/static

# Create output directory
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OUTPUT_DIR=/app/output \
    PYTHONPATH=/app/initializr-core:/app/initializr-cli:/app/initializr-web

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the web service (using standard asyncio, optimized for ARM64)
CMD ["uvicorn", "initializr_web.api:app", "--host", "0.0.0.0", "--port", "8000"]
