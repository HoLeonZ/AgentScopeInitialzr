"""Tests for metadata validator."""

import pytest
from initializr_core.metadata.models import AgentScopeMetadata, AgentType
from initializr_core.validator.validator import MetadataValidator, ValidationError


def test_valid_metadata():
    """Test validation of valid metadata."""
    metadata = AgentScopeMetadata(
        name="valid-agent",
        description="A valid test agent",
        version="1.0.0",
        python_version="3.10",
    )

    errors = MetadataValidator.validate(metadata)
    assert errors == []


def test_invalid_project_name():
    """Test validation fails with invalid project name."""
    metadata = AgentScopeMetadata(name="123invalid")

    with pytest.raises(ValidationError):
        MetadataValidator.validate(metadata)


def test_invalid_python_version():
    """Test validation fails with invalid Python version."""
    metadata = AgentScopeMetadata(
        name="test-agent",
        python_version="3.9",  # Too old
    )

    with pytest.raises(ValidationError):
        MetadataValidator.validate(metadata)


def test_invalid_version_format():
    """Test validation fails with invalid version format."""
    metadata = AgentScopeMetadata(
        name="test-agent",
        version="invalid",
    )

    with pytest.raises(ValidationError):
        MetadataValidator.validate(metadata)
