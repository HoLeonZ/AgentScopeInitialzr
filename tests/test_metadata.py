"""Tests for metadata models."""

import pytest
from initializr_core.metadata.models import (
    AgentScopeMetadata,
    AgentType,
    ModelProvider,
    MemoryType,
    Dependency,
)


def test_basic_metadata():
    """Test basic metadata creation."""
    metadata = AgentScopeMetadata(
        name="test-agent",
        description="Test agent",
    )

    assert metadata.name == "test-agent"
    assert metadata.description == "Test agent"
    assert metadata.package_name == "test_agent"
    assert metadata.agent_type == AgentType.BASIC
    assert metadata.model_provider == ModelProvider.OPENAI


def test_metadata_package_name_normalization():
    """Test package name normalization."""
    metadata1 = AgentScopeMetadata(name="my-agent")
    assert metadata1.package_name == "my_agent"

    metadata2 = AgentScopeMetadata(name="My_Agent")
    assert metadata2.package_name == "my_agent"


def test_metadata_to_dict():
    """Test metadata to dictionary conversion."""
    metadata = AgentScopeMetadata(
        name="test-agent",
        agent_type=AgentType.MULTI_AGENT,
        model_provider=ModelProvider.ANTHROPIC,
    )

    data = metadata.to_dict()

    assert data["name"] == "test-agent"
    assert data["agent_type"] == "multi-agent"
    assert data["model_provider"] == "anthropic"


def test_dependency_string():
    """Test dependency string representation."""
    dep1 = Dependency("requests", version="2.31.0")
    assert str(dep1) == "requests==2.31.0"

    dep2 = Dependency("requests")
    assert str(dep2) == "requests"
