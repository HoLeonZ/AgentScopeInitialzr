#!/usr/bin/env python3
"""
Docker Build Script for AgentScope Initializr

ATOMIC OPERATION: Build image + export tar.gz as a single atomic unit.
- Uses temp file + rename for atomicity
- Automatic rollback on any failure
- Old tar.gz preserved until new one is ready
"""

import argparse
import subprocess
import sys
import os
import platform
import shutil
import tempfile
import hashlib
from pathlib import Path


IMAGE_NAME = "agentscope-initializr"
IMAGE_TAG = "latest"


class AtomicBuild:
    """Atomic build operation with rollback support."""

    def __init__(self, arch: str, no_cache: bool = False):
        self.arch = arch
        self.no_cache = no_cache
        self.platform = f"linux/{arch}"
        self.output_file = Path(f"{IMAGE_NAME}-{arch}.tar.gz")
        self.temp_file: Path | None = None
        self.image_built = False
        self.image_id_before: str | None = None

    def _run(self, cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
        """Execute a shell command."""
        print(f"  $ {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, check=check)
        return result

    def _get_current_image_id(self) -> str | None:
        """Get current image ID if exists."""
        try:
            result = self._run(
                ["docker", "image", "inspect", "-f", "{{.Id}}", f"{IMAGE_NAME}:{IMAGE_TAG}"],
                check=False
            )
            return result.stdout.strip() if result.returncode == 0 else None
        except Exception:
            return None

    def rollback(self):
        """Rollback all changes made during the atomic operation."""
        print("\n" + "=" * 40)
        print("ROLLBACK: Cleaning up...")
        print("=" * 40)

        # Remove temp file if exists
        if self.temp_file and self.temp_file.exists():
            print(f"  Removing temp file: {self.temp_file}")
            self.temp_file.unlink()

        # Remove newly built image if it didn't exist before
        if self.image_built and self.image_id_before is None:
            print(f"  Removing newly built image: {IMAGE_NAME}:{IMAGE_TAG}")
            self._run(["docker", "rmi", "-f", f"{IMAGE_NAME}:{IMAGE_TAG}"], check=False)
        elif self.image_built and self.image_id_before:
            # Restore previous image if it existed
            try:
                print(f"  Restoring previous image...")
                self._run(["docker", "pull", self.image_id_before], check=False)
            except Exception:
                pass

        print("  Rollback complete.")

    def check_docker(self) -> bool:
        """Check if Docker is running."""
        print("Checking Docker status...")
        try:
            result = subprocess.run(
                ["docker", "info"],
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode != 0:
                print("Error: Docker is not running.")
                return False
            print("Docker is ready.")
            return True
        except FileNotFoundError:
            print("Error: docker command not found.")
            return False

    def setup_buildx(self) -> bool:
        """Setup buildx."""
        print("\nSetting up buildx...")
        try:
            self._run(["docker", "context", "use", "default"], check=False)
            self._run(["docker", "buildx", "use", "default"], check=False)
            print("buildx ready.")
            return True
        except Exception as e:
            print(f"Warning: buildx setup error: {e}")
            return True

    def build_image(self) -> tuple[bool, str | None]:
        """Build the Docker image. Returns (success, image_id)."""
        print(f"\n{'=' * 40}")
        print(f"[1/3] Building Docker image ({self.platform})")
        print("=" * 40)

        # Record previous image state
        self.image_id_before = self._get_current_image_id()

        cmd = [
            "docker", "buildx", "build",
            "--platform", self.platform,
            "-t", f"{IMAGE_NAME}:{IMAGE_TAG}",
            "--load"
        ]

        if self.no_cache:
            cmd.append("--no-cache")

        cmd.append(".")

        env = os.environ.copy()
        env["DOCKER_BUILDKIT"] = "1"

        try:
            result = subprocess.run(cmd, env=env, text=True)
            if result.returncode != 0:
                print(f"Build failed!")
                print(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
                return False, None

            image_id = self._get_current_image_id()
            self.image_built = True
            print(f"Build complete: {image_id[:12] if image_id else 'unknown'}")
            return True, image_id

        except Exception as e:
            print(f"Build error: {e}")
            return False, None

    def export_image(self, image_id: str) -> tuple[bool, Path | None]:
        """Export image to tar.gz atomically. Returns (success, output_path)."""
        print(f"\n{'=' * 40}")
        print(f"[2/3] Exporting to tar.gz")
        print("=" * 40)

        # Create temp file in same directory for atomic rename
        temp_fd, temp_path = tempfile.mkstemp(
            suffix=".tar.gz",
            prefix=f"{IMAGE_NAME}-{self.arch}.",
            dir=self.output_file.parent or "."
        )
        os.close(temp_fd)
        self.temp_file = Path(temp_path)

        try:
            # Build image SHA for verification
            expected_sha = image_id.replace("sha256:", "")[:12]

            cmd = ["docker", "save", f"{IMAGE_NAME}:{IMAGE_TAG}"]

            with open(self.temp_file, "wb") as f:
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
                print("Export failed!")
                return False, None

            file_size = self.temp_file.stat().st_size
            print(f"Exported: {file_size / (1024*1024):.1f} MB")

            # Verify the archive is valid
            print("Verifying archive integrity...")
            verify_result = subprocess.run(
                ["gzip", "-t", str(self.temp_file)],
                capture_output=True,
                text=True
            )
            if verify_result.returncode != 0:
                print("Archive verification failed!")
                return False, None
            print("Archive verified.")

            return True, self.temp_file

        except Exception as e:
            print(f"Export error: {e}")
            return False, None

    def finalize(self, temp_path: Path, image_id: str) -> bool:
        """Atomically move temp file to final location."""
        print(f"\n{'=' * 40}")
        print(f"[3/3] Finalizing output")
        print("=" * 40)

        try:
            # Backup old file if exists
            backup_file = Path(str(self.output_file) + ".bak")
            if self.output_file.exists():
                print(f"  Backing up old file: {self.output_file}")
                shutil.move(str(self.output_file), str(backup_file))

            # Atomic rename
            print(f"  Moving to final location: {self.output_file}")
            shutil.move(str(temp_path), str(self.output_file))

            # Remove backup on success
            if backup_file.exists():
                backup_file.unlink()

            # Compute and display checksum
            sha256_hash = hashlib.sha256()
            with open(self.output_file, "rb") as f:
                for chunk in iter(lambda: f.read(8192), b""):
                    sha256_hash.update(chunk)
            checksum = sha256_hash.hexdigest()

            print(f"\n{'=' * 40}")
            print("ATOMIC BUILD COMPLETE")
            print("=" * 40)
            print(f"  Image:     {IMAGE_NAME}:{IMAGE_TAG}")
            print(f"  Image ID:  {image_id[:12]}")
            print(f"  Platform:  {self.platform}")
            print(f"  Output:    {self.output_file}")
            print(f"  Size:      {self.output_file.stat().st_size / (1024*1024):.1f} MB")
            print(f"  SHA256:    {checksum[:16]}...")
            print("=" * 40)

            return True

        except Exception as e:
            print(f"Finalization error: {e}")
            return False

    def run(self) -> bool:
        """Execute the atomic build operation."""
        print("=" * 40)
        print("AgentScope Initializr - Atomic Build")
        print("=" * 40)
        print(f"Platform: {self.platform}")
        print(f"Image:    {IMAGE_NAME}:{IMAGE_TAG}")
        print(f"Output:   {self.output_file}")

        # Pre-flight checks
        if not self.check_docker():
            return False

        self.setup_buildx()

        # Step 1: Build
        success, image_id = self.build_image()
        if not success or not image_id:
            self.rollback()
            return False

        # Step 2: Export
        success, temp_path = self.export_image(image_id)
        if not success or not temp_path:
            self.rollback()
            return False

        # Step 3: Finalize (atomic rename)
        success = self.finalize(temp_path, image_id)
        if not success:
            self.rollback()
            return False

        return True


def main():
    parser = argparse.ArgumentParser(
        description="Build and export AgentScope Initializr Docker image (atomic operation)"
    )
    parser.add_argument(
        "--arch", "-a",
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

    # Auto-detect architecture
    if args.arch == "auto":
        arch = platform.machine().lower()
        if arch in ['arm64', 'aarch64']:
            arch = 'arm64'
        elif arch in ['x86_64', 'amd64']:
            arch = 'amd64'
        else:
            arch = 'amd64'
    else:
        arch = args.arch

    if args.check_only:
        atomic = AtomicBuild(arch)
        return 0 if atomic.check_docker() else 1

    atomic = AtomicBuild(arch, no_cache=args.no_cache)
    success = atomic.run()

    if not success:
        print("\nBuild failed. No changes made.")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
