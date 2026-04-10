#!/bin/bash
# Run script for AgentScope Initializr Docker container
# Use this script on the target Linux ARM64 machine

set -e

# Configuration
IMAGE_NAME="agentscope-initializr"
IMAGE_TAG="latest"
CONTAINER_NAME="agentscope-initializr"
PORT=8000

echo "========================================"
echo "AgentScope Initializr Container Runner"
echo "========================================"
echo ""

# Check if image exists
if ! docker image inspect ${IMAGE_NAME}:${IMAGE_TAG} > /dev/null 2>&1; then
    echo "Error: Image ${IMAGE_NAME}:${IMAGE_TAG} not found."
    echo "Please load the image first:"
    echo "  docker load < ${IMAGE_NAME}-arm64.tar.gz"
    exit 1
fi

# Stop and remove existing container if exists
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Stopping existing container..."
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

echo "Starting container..."
echo "----------------------------------------"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:8000 \
    -v ${PWD}/output:/app/output \
    -e LOG_LEVEL=info \
    -e OUTPUT_DIR=/app/output \
    -e ALLOW_ORIGINS="http://localhost:${PORT},http://localhost:5173,http://localhost:8080" \
    --restart unless-stopped \
    ${IMAGE_NAME}:${IMAGE_TAG}

echo ""
echo "Waiting for service to start..."
sleep 5

# Check if container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "Error: Container failed to start."
    echo "Checking logs..."
    docker logs ${CONTAINER_NAME}
    exit 1
fi

echo ""
echo "========================================"
echo "Container started successfully!"
echo "========================================"
echo ""
echo "Container name: ${CONTAINER_NAME}"
echo "Access URL: http://localhost:${PORT}"
echo ""
echo "Useful commands:"
echo "  View logs:    docker logs -f ${CONTAINER_NAME}"
echo "  Stop:         docker stop ${CONTAINER_NAME}"
echo "  Restart:      docker restart ${CONTAINER_NAME}"
echo "  Remove:       docker rm -f ${CONTAINER_NAME}"
echo ""

# Health check
echo "Performing health check..."
if curl -f http://localhost:${PORT}/health > /dev/null 2>&1; then
    echo "Health check passed! Service is running."
else
    echo "Warning: Health check failed. Check logs for details."
fi
