#!/usr/bin/env python3
"""
Docker Build Script for AgentScope Initializr

Builds a Docker image and exports it as a tar.gz file.
Supports multiple architectures (linux/amd64, linux/arm64).
"""

import argparse
import subprocess
import sys
import os
import platform
from pathlib import Path


IMAGE_NAME = "agentscope-initializr"
IMAGE_TAG = "latest"


def get_current_architecture() -> str:
    """Detect current machine architecture."""
    arch = platform.machine().lower()
    if arch in ['arm64', 'aarch64']:
        return 'arm64'
    elif arch in ['x86_64', 'amd64']:
        return 'amd64'
    return 'amd64'


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


def setup_buildx() -> bool:
    """Setup buildx to use default driver."""
    print("\n" + "=" * 40)
    print("Step 0: Setting up buildx")
    print("=" * 40)

    try:
        run_command(["docker", "context", "use", "default"], check=False)
        run_command(["docker", "buildx", "use", "default"], check=False)
        result = run_command(["docker", "buildx", "inspect", "--bootstrap"], check=False)
        if result.returncode != 0:
            print("Warning: buildx bootstrap failed, continuing anyway...")
        return True
    except Exception as e:
        print(f"Warning: setup_buildx error: {e}")
        return True


def build_image(platform: str, no_cache: bool = False) -> bool:
    """Build the Docker image using buildx."""
    print("\n" + "=" * 40)
    print(f"Step 1: Building Docker image ({platform})")
    print("=" * 40)

    cmd = [
        "docker", "buildx", "build",
        "--platform", platform,
        "-t", f"{IMAGE_NAME}:{IMAGE_TAG}",
        "--load"
    ]

    if no_cache:
        cmd.append("--no-cache")

    cmd.append(".")

    try:
        env = os.environ.copy()
        env["DOCKER_BUILDKIT"] = "1"
        result = subprocess.run(cmd, env=env, text=True)
        if result.returncode != 0:
            print(f"Error: Build failed")
            print(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
            return False
        print("Build completed successfully!")
        return True
    except Exception as e:
        print(f"Error: Build failed: {e}")
        return False


def export_image(arch: str) -> bool:
    """Export the Docker image to tar.gz."""
    output_file = f"{IMAGE_NAME}-{arch}.tar.gz"
    print("\n" + "=" * 40)
    print("Step 2: Exporting image to tar.gz")
    print("=" * 40)

    try:
        cmd = ["docker", "save", f"{IMAGE_NAME}:{IMAGE_TAG}"]
        with open(output_file, "wb") as f:
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

        file_size = Path(output_file).stat().st_size
        file_size_mb = file_size / (1024 * 1024)
        print(f"Export completed successfully!")
        print(f"Output: {output_file} ({file_size_mb:.1f} MB)")
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
        "--arch",
        "-a",
        choices=["amd64", "arm64", "auto"],
        default="auto",
        help="Target architecture (default: auto-detect)"
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

    if args.arch == "auto":
        arch = get_current_architecture()
    else:
        arch = args.arch

    platform_str = f"linux/{arch}"

    output_file = f"{IMAGE_NAME}-{arch}.tar.gz"

    print("=" * 40)
    print("AgentScope Initializr Docker Build")
    print("=" * 40)
    print(f"Platform: {platform_str}")
    print(f"Image: {IMAGE_NAME}:{IMAGE_TAG}")
    print(f"Output: {output_file}")

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

    setup_buildx()

    success = build_image(platform_str, no_cache=args.no_cache)
    if not success:
        return 1

    if not export_image(arch):
        return 1

    info = get_image_info()
    print("\n" + "=" * 40)
    print("Build Summary")
    print("=" * 40)
    print(f"Image: {IMAGE_NAME}:{IMAGE_TAG}")
    if info:
        print(f"Architecture: {info.get('os', 'unknown')}/{info.get('architecture', 'unknown')}")
        print(f"Size: {info.get('size', 0) / (1024*1024):.1f} MB")
    print(f"Output file: {output_file}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
