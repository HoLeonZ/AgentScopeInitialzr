#!/usr/bin/env python3
"""
Download all possible packages for Windows x86_64 architecture.
Run this on Windows machine to pre-download packages for offline deployment.
"""

import subprocess
import os
import sys

# All possible packages based on generated requirements
PACKAGES = [
    # Core
    "agentscope>=0.1.0",
    "python-dotenv>=1.0.0",

    # Model providers
    "openai>=1.0.0",
    "anthropic>=0.18.0",
    "dashscope>=1.0.0",
    "google-generativeai>=0.3.0",

    # Memory
    "mem0ai>=0.1.0",
    "redis>=5.0.0",
    "zep>=1.0.0",
    "oceanbase>=1.0.0",

    # Agent types
    "httpx>=0.27.0",
    "playwright>=1.40.0",

    # Knowledge base
    "qdrant-client>=1.7.0",

    # RAGAS evaluation
    "ragas>=0.1.0",
    "langchain>=0.1.0",
    "langchain-openai>=0.0.5",
    "pandas>=2.0.0",
    "datasets>=2.14.0",

    # Additional dependencies
    "aiofiles>=23.0.0",
    "fastapi>=0.100.0",
    "uvicorn>=0.23.0",
    "click>=8.1.0",
    "jinja2>=3.1.0",
    "pydantic>=2.0.0",
    "tavily-python>=0.3.0",
    "python-multipart>=0.0.6",
]


def download_packages(target_dir: str):
    """Download all packages to target directory for Windows x86_64."""
    target_dir = os.path.abspath(target_dir)

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print(f"Downloading packages to: {target_dir}")
    print(f"Platform: Windows x86_64")
    print(f"Total packages: {len(PACKAGES)}")
    print("=" * 60)

    # Create pip download command
    cmd = [
        sys.executable, "-m", "pip", "download",
        "--only-binary=:all:",
        "--platform", "win_amd64",
        "--python-version", "311",
        "--implementation", "cp",
        "-d", target_dir,
    ] + PACKAGES

    print(f"Running: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print("STDERR:", result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
            print()
            print("Some packages don't have Windows wheels, falling back to source download...")

            # Fallback: download without binary restriction
            cmd_fallback = [
                sys.executable, "-m", "pip", "download",
                "-d", target_dir,
            ] + PACKAGES

            result = subprocess.run(cmd_fallback, capture_output=True, text=True)

        if result.returncode != 0:
            print("Warning:", result.stderr[-1000:] if len(result.stderr) > 1000 else result.stderr)
        else:
            print("Download completed!")

    except Exception as e:
        print(f"Error: {e}")
        return False

    # List downloaded files
    print()
    print("=" * 60)
    print("Downloaded files:")
    print("-" * 60)

    files = sorted(os.listdir(target_dir))
    total_size = 0
    for f in files:
        fpath = os.path.join(target_dir, f)
        size = os.path.getsize(fpath)
        total_size += size
        print(f"  {f} ({size / 1024 / 1024:.2f} MB)")

    print("-" * 60)
    print(f"Total: {len(files)} files, {total_size / 1024 / 1024:.2f} MB")

    # Create requirements.txt
    req_file = os.path.join(target_dir, "requirements.txt")
    with open(req_file, "w") as f:
        for pkg in PACKAGES:
            f.write(pkg + "\n")
    print(f"\nCreated: {req_file}")

    return True


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "packages"
    success = download_packages(target)
    sys.exit(0 if success else 1)
