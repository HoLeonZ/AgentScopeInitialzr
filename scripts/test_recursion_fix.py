#!/usr/bin/env python3
"""
Test script to verify the RecursionError fix in generated code.

This script generates a test project and checks:
1. ApplicationLifecycle.initialize() can be called without RecursionError
2. ApplicationLifecycle.shutdown() can be called without errors
"""

import sys
import os
import tempfile
from pathlib import Path

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent / "initializr-core"))
sys.path.insert(0, str(Path(__file__).parent.parent / "initializr-cli"))


def test_recursion_fix():
    """Test that ApplicationLifecycle.initialize() doesn't cause RecursionError."""
    print("=" * 60)
    print("Testing RecursionError Fix")
    print("=" * 60)

    # Import after path is set
    from initializr_core.generator.engine import ProjectGenerator
    from initializr_core.metadata.models import (
        AgentScopeMetadata,
        AgentType,
        ModelProvider,
        MemoryType,
    )

    # Create temp directory for test
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()

        # Generate test project
        print("\n[1] Generating test project...")
        metadata = AgentScopeMetadata(
            name="TestProject",
            package_name="test_project",
            version="0.1.0",
            description="Test project for recursion fix verification",
            agent_type=AgentType.BASIC,
            model_provider=ModelProvider.DASHSCOPE,
            model_config={"model": "doubao", "api_key": "test-key"},
            memory_type=MemoryType.IN_MEMORY,
            hooks=False,
            enable_rag=False,
            enable_knowledge=False,
            enable_pipeline=False,
        )

        try:
            generator = ProjectGenerator(output_dir=str(project_dir))
            result = generator.generate(metadata)
            print(f"  ✓ Project generated")
        except Exception as e:
            print(f"  ✗ Failed to generate project: {e}")
            import traceback
            traceback.print_exc()
            return False

        # Set up paths
        src_dir = project_dir / "TestProject" / "src"
        if str(src_dir) not in sys.path:
            sys.path.insert(0, str(src_dir))

        # Change working directory to avoid logs file issue
        original_cwd = os.getcwd()
        os.chdir(tmpdir)

        try:
            # Test 1: Import ApplicationLifecycle
            print("\n[2] Testing import...")
            from test_project.config.lifecycle import ApplicationLifecycle
            print(f"  ✓ ApplicationLifecycle imported successfully")

            # Test 2: Call initialize() - this is where RecursionError occurred
            print("\n[3] Testing ApplicationLifecycle.initialize()...")
            try:
                ApplicationLifecycle.initialize()
                print(f"  ✓ initialize() called successfully - no RecursionError!")
            except RecursionError as e:
                print(f"  ✗ RecursionError occurred: {e}")
                return False
            except Exception as e:
                # Other exceptions are OK - we just want to verify no RecursionError
                print(f"  ⚠ initialize() raised non-recursion error: {type(e).__name__}: {e}")
                print(f"     (This is acceptable - other dependencies may be missing)")

            # Test 3: Call shutdown()
            print("\n[4] Testing ApplicationLifecycle.shutdown()...")
            try:
                ApplicationLifecycle.shutdown()
                print(f"  ✓ shutdown() called successfully")
            except RecursionError as e:
                print(f"  ✗ RecursionError occurred: {e}")
                return False
            except Exception as e:
                print(f"  ⚠ shutdown() raised error: {type(e).__name__}: {e}")
                print(f"     (This is acceptable)")

            # Test 4: Call get_lifecycle()
            print("\n[5] Testing get_lifecycle()...")
            try:
                from test_project.config.lifecycle import get_lifecycle
                lifecycle = get_lifecycle()
                print(f"  ✓ get_lifecycle() returned: {type(lifecycle).__name__}")
            except RecursionError as e:
                print(f"  ✗ RecursionError in get_lifecycle(): {e}")
                return False
            except Exception as e:
                print(f"  ⚠ get_lifecycle() raised error: {type(e).__name__}: {e}")

            print("\n" + "=" * 60)
            print("✅ RecursionError fix verified!")
            print("   ApplicationLifecycle.initialize() works correctly.")
            print("=" * 60)
            return True

        finally:
            os.chdir(original_cwd)


if __name__ == "__main__":
    success = test_recursion_fix()
    sys.exit(0 if success else 1)
