#!/bin/bash
# Build script for AgentScope Initializr Docker image
# This script builds an ARM64 Docker image and exports it as a tar.gz file
# Optimized for caching - only re-downloads dependencies when necessary

set -e

# Configuration
IMAGE_NAME="agentscope-initializr"
IMAGE_TAG="latest"
OUTPUT_FILE="${IMAGE_NAME}-arm64.tar.gz"
PLATFORM="linux/arm64"

echo "========================================"
echo "AgentScope Initializr Docker Build"
echo "========================================"
echo ""
echo "Platform: ${PLATFORM}"
echo "Image: ${IMAGE_NAME}:${IMAGE_TAG}"
echo "Output: ${OUTPUT_FILE}"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker first."
    exit 1
fi

echo "Step 1: Building Docker image (with cache)..."
echo "----------------------------------------"
echo "Note: Docker will use cached layers when possible."
echo "      Use 'docker build --no-cache' to force fresh build."
echo ""

# Use docker build with cache enabled (default behavior)
DOCKER_BUILDKIT=1 docker build \
    --platform ${PLATFORM} \
    -t ${IMAGE_NAME}:${IMAGE_TAG} \
    .

echo ""
echo "Step 2: Exporting image to tar.gz..."
echo "----------------------------------------"
docker save ${IMAGE_NAME}:${IMAGE_TAG} | gzip > ${OUTPUT_FILE}

# Get file size
FILE_SIZE=$(ls -lh ${OUTPUT_FILE} | awk '{print $5}')
echo ""
echo "========================================"
echo "Build completed successfully!"
echo "========================================"
echo ""
echo "Image file: ${OUTPUT_FILE}"
echo "File size: ${FILE_SIZE}"
echo ""
echo "To verify the image, run:"
echo "  ./docker-verify.sh"
echo ""
echo "To deploy on target machine:"
echo "  1. Copy ${OUTPUT_FILE} to the target machine"
echo "  2. Run: docker load < ${OUTPUT_FILE}"
echo "  3. Run: docker run -d -p 8000:8000 ${IMAGE_NAME}:${IMAGE_TAG}"
echo ""
