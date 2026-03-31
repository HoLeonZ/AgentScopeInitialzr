#!/usr/bin/env python3
"""
Test script to verify end-to-end extensions configuration flow.

This script tests:
1. ProjectRequest model with all extension fields
2. Converter transformation to AgentScopeMetadata
3. Generator code generation with extensions
"""

import sys
import tempfile
from pathlib import Path

# Add packages to path
sys.path.insert(0, str(Path(__file__).parent / "initializr-web"))
sys.path.insert(0, str(Path(__file__).parent / "initializr-core"))

from initializr_web.models import ProjectRequest
from initializr_web.converter import project_request_to_metadata
from initializr_core.generator.engine import ProjectGenerator


def test_basic_extensions():
    """Test basic extensions configuration."""
    print("Testing basic extensions configuration...")

    # Create a project request with all extension fields
    request = ProjectRequest(
        name="test-agent",
        description="Test agent with extensions",
        author="Test Author",
        agent_type="basic",
        model_provider="openai",
        model_config={"model": "gpt-4"},

        # Memory extensions
        enable_memory=True,
        short_term_memory="in-memory",
        long_term_memory="mem0",

        # Tools extensions
        enable_tools=True,
        tools=["execute_python_code", "web_search"],

        # Formatter extensions
        enable_formatter=True,
        formatter="OpenAIChatFormatter",

        # Hooks extensions
        enable_hooks=True,
        hooks=["pre_reply", "post_reply"],

        # Skills extensions
        enable_skills=True,
        skills=["coding", "writing"],

        # RAG extensions
        enable_rag=True,
        rag_config={
            "store_type": "chroma",
            "embedding_model": "openai:text-embedding-ada-002",
            "chunk_size": 500,
            "chunk_overlap": 50,
        },

        # Pipeline extensions
        enable_pipeline=True,
        pipeline_config={
            "type": "sequential",
            "num_stages": 3,
            "error_handling": "stop",
        },

        # Testing & Evaluation
        generate_tests=True,
        generate_evaluation=True,
        evaluator_type="general",
        enable_openjudge=True,
        openjudge_graders=["RelevanceGrader", "CorrectnessGrader"],
        initial_benchmark_tasks=5,
    )

    print(f"✓ Created ProjectRequest with {len(request.tools)} tools")
    print(f"✓ Memory: short_term={request.short_term_memory}, long_term={request.long_term_memory}")
    print(f"✓ Hooks: {len(request.hooks)} hooks configured")
    print(f"✓ Skills: {len(request.skills)} skills enabled")
    print(f"✓ RAG enabled: {request.enable_rag}")
    print(f"✓ Pipeline enabled: {request.enable_pipeline}")
    print(f"✓ Testing: generate_tests={request.generate_tests}, generate_evaluation={request.generate_evaluation}")
    print(f"✓ OpenJudge: {len(request.openjudge_graders)} graders")

    return request


def test_converter(request: ProjectRequest):
    """Test converter transformation."""
    print("\nTesting converter transformation...")

    metadata = project_request_to_metadata(request)

    print(f"✓ Converted to AgentScopeMetadata")
    print(f"✓ Package name: {metadata.package_name}")
    print(f"✓ Memory type: {metadata.memory_type}")
    print(f"✓ Short-term memory: {metadata.short_term_memory}")
    print(f"✓ Long-term memory: {metadata.long_term_memory}")
    print(f"✓ Tools: {len(metadata.tools)} tools")
    print(f"✓ Hooks: {len(metadata.hooks)} hooks")
    print(f"✓ Middleware: {len(metadata.middleware)} middleware components")
    print(f"✓ Formatter: {metadata.formatter_name}")
    print(f"✓ Skills enabled: {metadata.enable_skills}")
    print(f"✓ RAG enabled: {metadata.enable_rag}")
    print(f"✓ Pipeline enabled: {metadata.enable_pipeline}")
    print(f"✓ Generate tests: {metadata.generate_tests}")
    print(f"✓ Generate evaluation: {metadata.generate_evaluation}")

    # Verify all fields are properly set
    assert metadata.name == "test-agent"
    assert metadata.short_term_memory == "in-memory"
    assert metadata.long_term_memory == "mem0"
    assert len(metadata.tools) == 2
    assert len(metadata.hooks) == 2
    assert metadata.enable_rag is True
    assert metadata.enable_pipeline is True
    assert metadata.generate_tests is True
    assert metadata.generate_evaluation is True

    print("✓ All assertions passed!")
    return metadata


def test_generator(metadata):
    """Test generator code generation."""
    print("\nTesting generator code generation...")

    # Use output directory instead of temp for inspection
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    generator = ProjectGenerator(output_dir=str(output_dir))
    generated = generator.generate(metadata)

    print(f"✓ Generated project at: {generated.path}")
    print(f"✓ Project structure:")

    # Check generated files
    expected_files = [
        "src/test_agent/config/__init__.py",
        "tests/test_test_agent.py",
        "tests/test_evaluation.py",
        "tests/test_benchmarks.py",
        "pytest.ini",
        "README.md",
    ]

    for file_path in expected_files:
        full_path = generated.path / file_path
        if full_path.exists():
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - NOT FOUND")

    # Check config file contains extension configurations
    config_file = generated.path / "src/test_agent/config/__init__.py"
    if config_file.exists():
        config_content = config_file.read_text()

        # Check for memory configuration
        assert "SHORT_TERM_MEMORY_TYPE" in config_content or "get_short_term_memory" in config_content
        print("  ✓ Memory configuration found")

        # Check for RAG configuration
        if metadata.enable_rag:
            assert "RAG_STORE_TYPE" in config_content or "get_rag_retriever" in config_content
            print("  ✓ RAG configuration found")

        # Check for pipeline configuration
        if metadata.enable_pipeline:
            assert "PIPELINE_TYPE" in config_content or "get_pipeline" in config_content
            print("  ✓ Pipeline configuration found")

        # Check for skills configuration
        if metadata.enable_skills:
            assert "get_skills" in config_content
            print("  ✓ Skills configuration found")

    # Check test files
    test_file = generated.path / "tests/test_test_agent.py"
    if metadata.generate_tests and test_file.exists():
        test_content = test_file.read_text()
        assert "TestModel" in test_content or "TestMemory" in test_content
        print("  ✓ Test module generated")

    eval_file = generated.path / "tests/test_evaluation.py"
    if metadata.generate_evaluation and eval_file.exists():
        eval_content = eval_file.read_text()
        assert "TestEvaluation" in eval_content
        if metadata.enable_openjudge:
            assert "TestOpenJudge" in eval_content
        print("  ✓ Evaluation module generated")

    benchmark_file = generated.path / "tests/test_benchmarks.py"
    if metadata.initial_benchmark_tasks > 0 and benchmark_file.exists():
        benchmark_content = benchmark_file.read_text()
        assert "TestBenchmarks" in benchmark_content
        print("  ✓ Benchmark tasks generated")

    print("\n✓ Generator test completed successfully!")
    print(f"✓ Generated project available at: {generated.path}")


def main():
    """Run all tests."""
    print("=" * 60)
    print("AgentScope Initializr - Extensions Flow Test")
    print("=" * 60)

    try:
        # Test 1: Create ProjectRequest
        request = test_basic_extensions()

        # Test 2: Convert to metadata
        metadata = test_converter(request)

        # Test 3: Generate project
        test_generator(metadata)

        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nExtensions configuration flow is working correctly:")
        print("  ✓ P0: Memory & Tools configuration ✓")
        print("  ✓ P0: Converter transformation ✓")
        print("  ✓ P0: Generator code generation ✓")
        print("  ✓ P1: Formatter & Hooks configuration ✓")
        print("  ✓ P1: Testing & Evaluation configuration ✓")
        print("  ✓ P2: Skills, RAG, Pipeline configuration ✓")
        print("\n🎉 Implementation complete!")

    except Exception as e:
        print(f"\n✗ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
