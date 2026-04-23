#!/usr/bin/env python3
"""
Verify generated project code can run without errors.

This script generates a test project and checks:
1. All Python files have valid syntax
2. All imports can be resolved
3. Main function can be called
"""

import sys
import os
import tempfile
import shutil
import subprocess
import ast
from pathlib import Path

# Add project paths
sys.path.insert(0, str(Path(__file__).parent.parent / "initializr-core"))
sys.path.insert(0, str(Path(__file__).parent.parent / "initializr-cli"))


def verify_syntax(filepath: Path) -> tuple[bool, str]:
    """Check if a Python file has valid syntax."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            compile(f.read(), filepath, 'exec')
        return True, ""
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Error: {e}"


def verify_imports(src_dir: Path, package_name: str) -> tuple[bool, str]:
    """Try to import all modules in the generated project."""
    errors = []

    # Add src/ to path
    if str(src_dir) not in sys.path:
        sys.path.insert(0, str(src_dir))

    try:
        # Try importing the main package
        import importlib
        pkg = importlib.import_module(package_name)
        print(f"  ✓ Imported {package_name}")

        # Try importing config
        try:
            config = importlib.import_module(f"{package_name}.config")
            print(f"  ✓ Imported {package_name}.config")

            # Check key imports
            if hasattr(config, 'settings'):
                print(f"  ✓ settings loaded")
            if hasattr(config, 'ApplicationLifecycle'):
                print(f"  ✓ ApplicationLifecycle available")
        except ImportError as e:
            errors.append(f"Failed to import config: {e}")

        # Try importing agents
        try:
            agents = importlib.import_module(f"{package_name}.agents")
            print(f"  ✓ Imported {package_name}.agents")
        except ImportError as e:
            errors.append(f"Failed to import agents: {e}")

        # Try importing main module
        try:
            main = importlib.import_module(f"{package_name}.main")
            print(f"  ✓ Imported {package_name}.main")
        except ImportError as e:
            errors.append(f"Failed to import main: {e}")

    except ImportError as e:
        errors.append(f"Failed to import main package: {e}")
    except Exception as e:
        errors.append(f"Unexpected error during import: {e}")

    return len(errors) == 0, "\n".join(errors) if errors else ""


def verify_main_function(main_file: Path) -> tuple[bool, str]:
    """Verify the main function can be called."""
    if not main_file.exists():
        return False, "main.py not found"

    try:
        # Try to parse the main function
        with open(main_file, 'r') as f:
            tree = ast.parse(f.read())

        # Find main function and asyncio.run pattern
        has_main = False
        has_asyncio_run = False

        for node in ast.walk(tree):
            if isinstance(node, ast.AsyncFunctionDef) and node.name == 'main':
                has_main = True
            if isinstance(node, ast.Call):
                func = node.func
                if isinstance(func, ast.Attribute) and func.attr == 'run':
                    if isinstance(func.value, ast.Name) and func.value.id == 'asyncio':
                        has_asyncio_run = True

        if has_main:
            print(f"  ✓ main() function found")
            if has_asyncio_run:
                print(f"  ✓ asyncio.run() pattern found")
            return True, ""
        else:
            return False, "main() function not found"

    except Exception as e:
        return False, f"Error parsing main.py: {e}"


def check_py_files(src_dir: Path, package_name: str) -> tuple[bool, list]:
    """Check syntax of all Python files in the package."""
    errors = []
    package_dir = src_dir / package_name

    if not package_dir.exists():
        return False, [f"Package directory not found: {package_dir}"]

    py_files = list(package_dir.rglob("*.py"))
    print(f"  Found {len(py_files)} Python files")

    for py_file in py_files:
        rel_path = py_file.relative_to(package_dir.parent)
        ok, error = verify_syntax(py_file)
        if ok:
            print(f"  ✓ {rel_path}")
        else:
            print(f"  ✗ {rel_path}: {error}")
            errors.append(f"{rel_path}: {error}")

    return len(errors) == 0, errors


def main():
    """Main entry point."""
    print("="*60)
    print("Generated Code Verification")
    print("="*60)

    # Import after path is set
    try:
        from initializr_core.generator.engine import ProjectGenerator
        from initializr_core.metadata.models import (
            AgentScopeMetadata,
            AgentType,
            ModelProvider,
            MemoryType,
        )
    except ImportError as e:
        print(f"✗ Failed to import generator: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Create temp directory for test
    with tempfile.TemporaryDirectory() as tmpdir:
        project_dir = Path(tmpdir) / "test_project"
        project_dir.mkdir()

        # Generate test project
        print("\n[0] Generating test project...")

        metadata = AgentScopeMetadata(
            name="TestProject",
            package_name="test_project",
            version="0.1.0",
            description="Test project for verification",
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
            return 1

        # The generated project has structure: test_project/TestProject/src/test_project/
        project_name_dir = project_dir / "TestProject"
        src_dir = project_name_dir / "src"
        package_dir = src_dir / "test_project"
        main_file = package_dir / "main.py"

        if not project_name_dir.exists():
            print(f"  ✗ Project directory not found: {project_name_dir}")
            return 1

        all_passed = True

        # 1. Check syntax of all Python files
        print("\n[1] Checking Python syntax...")
        ok, errors = check_py_files(src_dir, "test_project")
        if not ok:
            all_passed = False

        # 2. Check imports
        print("\n[2] Checking imports...")
        ok, error = verify_imports(src_dir, "test_project")
        if not ok:
            print(f"  ✗ Import errors:\n{error}")
            all_passed = False

        # 3. Check main function
        print("\n[3] Checking main function...")
        ok, error = verify_main_function(main_file)
        if not ok:
            print(f"  ✗ {error}")
            all_passed = False

        print("\n" + "="*60)
        if all_passed:
            print("✅ All verification checks passed!")
            print("="*60)
            return 0
        else:
            print("❌ Some verification checks failed!")
            print("="*60)
            return 1


if __name__ == "__main__":
    sys.exit(main())
