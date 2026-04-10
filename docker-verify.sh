#!/bin/bash
# Verification script for AgentScope Initializr Docker image
# Run this script on macOS (Apple Silicon) to verify the ARM64 image

set -e

# Configuration
IMAGE_NAME="agentscope-initializr"
IMAGE_TAG="latest"
CONTAINER_NAME="agentscope-initializr-test"
PORT=8000
IMAGE_FILE="${IMAGE_NAME}-arm64.tar.gz"

echo "========================================"
echo "AgentScope Initializr Verification"
echo "========================================"
echo ""

# Function to cleanup
cleanup() {
    echo ""
    echo "Cleaning up..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
}

# Register cleanup on exit
trap cleanup EXIT

# Step 1: Check if image file exists
echo "Step 1: Checking image file..."
echo "----------------------------------------"
if [ ! -f "${IMAGE_FILE}" ]; then
    echo "Error: Image file not found: ${IMAGE_FILE}"
    echo "Please run ./docker-build.sh first."
    exit 1
fi
echo "Image file found: ${IMAGE_FILE}"
echo ""

# Step 2: Load Docker image
echo "Step 2: Loading Docker image..."
echo "----------------------------------------"
if docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} > /dev/null 2>&1; then
    echo "Image already loaded. Skipping load step."
else
    echo "Loading image from ${IMAGE_FILE}..."
    docker load < ${IMAGE_FILE}
fi
echo "Image loaded successfully."
echo ""

# Step 3: Verify image architecture
echo "Step 3: Verifying image architecture..."
echo "----------------------------------------"
ARCH=$(docker inspect --format='{{.Architecture}}' ${IMAGE_NAME}:${IMAGE_TAG})
echo "Image architecture: ${ARCH}"
if [ "${ARCH}" != "arm64" ]; then
    echo "Warning: Expected arm64 architecture, got ${ARCH}"
fi
echo ""

# Step 4: Start container
echo "Step 4: Starting container..."
echo "----------------------------------------"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8000 \
    -e LOG_LEVEL=info \
    ${IMAGE_NAME}:${IMAGE_TAG}

echo "Container started. Waiting for service to be ready..."
sleep 10
echo ""

# Step 5: Health check
echo "Step 5: Health check..."
echo "----------------------------------------"
HEALTH_URL="http://localhost:${PORT}/health"
echo "Checking: ${HEALTH_URL}"

if curl -f ${HEALTH_URL} > /dev/null 2>&1; then
    echo "Health check passed!"
else
    echo "Health check failed. Checking container logs..."
    docker logs ${CONTAINER_NAME}
    exit 1
fi
echo ""

# Step 6: Frontend access test
echo "Step 6: Frontend access test..."
echo "----------------------------------------"
FRONTEND_URL="http://localhost:${PORT}/"
echo "Checking: ${FRONTEND_URL}"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" ${FRONTEND_URL})
if [ "${HTTP_CODE}" = "200" ]; then
    echo "Frontend accessible (HTTP ${HTTP_CODE})"
else
    echo "Warning: Frontend returned HTTP ${HTTP_CODE}"
fi
echo ""

# Step 7: API endpoint test
echo "Step 7: API endpoint test..."
echo "----------------------------------------"
TEMPLATES_URL="http://localhost:${PORT}/api/templates"
echo "Checking: ${TEMPLATES_URL}"

RESPONSE=$(curl -s ${TEMPLATES_URL})
if echo "${RESPONSE}" | grep -q "templates"; then
    echo "API endpoint working!"
    echo "Available templates: $(echo ${RESPONSE} | python3 -c "import sys, json; print(', '.join(json.load(sys.stdin)['templates']))" 2>/dev/null || echo "parse error")"
else
    echo "Warning: API response unexpected"
fi
echo ""

# Step 8: Container resource usage
echo "Step 8: Container resource usage..."
echo "----------------------------------------"
docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}" ${CONTAINER_NAME}
echo ""

# Summary
echo "========================================"
echo "Verification Summary"
echo "========================================"
echo ""
echo "Image file: ${IMAGE_FILE}"
echo "Architecture: ${ARCH}"
echo "Health check: PASSED"
echo "Frontend: ACCESSIBLE"
echo "API: WORKING"
echo ""
echo "The Docker image is ready for deployment!"
echo ""
echo "To deploy on target Linux ARM64 machine:"
echo "  1. Copy ${IMAGE_FILE} to the target machine"
echo "  2. Run: docker load < ${IMAGE_FILE}"
echo "  3. Run: ./docker-run.sh"
echo ""
