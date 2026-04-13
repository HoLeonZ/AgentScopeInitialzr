#!/usr/bin/env python3
"""
Docker Build Script for AgentScope Initializr

Builds an ARM64 Docker image and exports it as a tar.gz file.
Optimized for caching - only re-downloads dependencies when necessary.
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path


IMAGE_NAME = "agentscope-initializr"
IMAGE_TAG = "latest"
OUTPUT_FILE = f"{IMAGE_NAME}-arm64.tar.gz"
PLATFORM = "linux/arm64"


def run_command(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Execute a shell command and return the result."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, check=check)
    return result


def check_docker() -> bool:
    """Check if Docker is running."""
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def build_image(no_cache: bool = False) -> bool:
    """Build the Docker image."""
    print("\n" + "=" * 40)
    print("Step 1: Building Docker image")
    print("=" * 40)

    if no_cache:
        print("Warning: Building without cache (fresh build)")
        print("This will take longer as all layers will be rebuilt.")
    else:
        print("Note: Docker will use cached layers when possible.")

    cmd = ["docker", "build"]
    if no_cache:
        cmd.append("--no-cache")
    cmd.extend([
        "--platform", PLATFORM,
        "-t", f"{IMAGE_NAME}:{IMAGE_TAG}",
        "."
    ])

    try:
        env = os.environ.copy()
        env["DOCKER_BUILDKIT"] = "1"
        result = subprocess.run(cmd, env=env, text=True)
        if result.returncode != 0:
            print(f"Error: Build failed")
            print(result.stderr)
            return False
        print("Build completed successfully!")
        return True
    except Exception as e:
        print(f"Error: Build failed: {e}")
        return False


def export_image() -> bool:
    """Export the Docker image to tar.gz."""
    print("\n" + "=" * 40)
    print("Step 2: Exporting image to tar.gz")
    print("=" * 40)

    try:
        cmd = ["docker", "save", f"{IMAGE_NAME}:{IMAGE_TAG}"]
        with open(OUTPUT_FILE, "wb") as f:
            gzip_proc = subprocess.Popen(
                ["gzip"],
                stdin=subprocess.PIPE,
                stdout=f
            )
            docker_proc = subprocess.Popen(
                cmd,
                stdout=gzip_proc.stdin
            )
            docker_proc.wait()
            gzip_proc.stdin.close()
            gzip_proc.wait()

        if gzip_proc.returncode != 0:
            print(f"Error: Export failed")
            return False

        file_size = Path(OUTPUT_FILE).stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        print(f"Export completed successfully!")
        print(f"Output: {OUTPUT_FILE} ({file_size_mb:.1f} MB)")
        return True
    except Exception as e:
        print(f"Error: Export failed: {e}")
        return False


def get_image_info() -> dict:
    """Get information about the built image."""
    try:
        result = run_command(
            ["docker", "image", "inspect", f"{IMAGE_NAME}:{IMAGE_TAG}"],
            check=False
        )
        if result.returncode == 0:
            import json
            data = json.loads(result.stdout)
            if data:
                return {
                    "id": data[0].get("Id", ""),
                    "architecture": data[0].get("Architecture", ""),
                    "os": data[0].get("Os", ""),
                    "size": data[0].get("Size", 0)
                }
    except Exception:
        pass
    return {}


def main():
    parser = argparse.ArgumentParser(
        description="Build and export AgentScope Initializr Docker image"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Build without using Docker cache"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="Only check if Docker is running"
    )
    args = parser.parse_args()

    print("=" * 40)
    print("AgentScope Initializr Docker Build")
    print("=" * 40)
    print(f"Platform: {PLATFORM}")
    print(f"Image: {IMAGE_NAME}:{IMAGE_TAG}")
    print(f"Output: {OUTPUT_FILE}")

    if args.check_only:
        if check_docker():
            print("Docker is running.")
            return 0
        else:
            print("Error: Docker is not running.")
            return 1

    if not check_docker():
        print("Error: Docker is not running. Please start Docker first.")
        return 1

    if not build_image(no_cache=args.no_cache):
        return 1

    if not export_image():
        return 1

    info = get_image_info()
    print("\n" + "=" * 40)
    print("Build Summary")
    print("=" * 40)
    print(f"Image: {IMAGE_NAME}:{IMAGE_TAG}")
    if info:
        print(f"Architecture: {info.get('os', 'unknown')}/{info.get('architecture', 'unknown')}")
        print(f"Size: {info.get('size', 0) / (1024*1024):.1f} MB")
    print(f"Output file: {OUTPUT_FILE}")
    print("\nTo verify the image, run:")
    print("  python build_docker.py")
    print("\nTo deploy on target machine:")
    print(f"  1. Copy {OUTPUT_FILE} to the target machine")
    print("  2. Run: docker load < {OUTPUT_FILE}")
    print(f"  3. Run: docker-run.sh")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
