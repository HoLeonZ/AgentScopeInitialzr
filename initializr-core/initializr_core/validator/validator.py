"""
Validator for AgentScope Initializr.

Validates metadata and project configurations.
"""

import re
from typing import List, Optional
from initializr_core.metadata.models import AgentScopeMetadata


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class MetadataValidator:
    """Validator for project metadata."""

    @staticmethod
    def validate(metadata: AgentScopeMetadata) -> List[str]:
        """
        Validate metadata and return list of errors.

        Args:
            metadata: The metadata to validate

        Returns:
            List of error messages (empty if valid)

        Raises:
            ValidationError: If validation fails
        """
        errors = []

        # Validate project name
        if not metadata.name:
            errors.append("Project name is required")
        elif not MetadataValidator._is_valid_project_name(metadata.name):
            errors.append(
                "Project name must contain only letters, numbers, hyphens, and underscores"
            )

        # Validate Python version
        if metadata.python_version:
            if not MetadataValidator._is_valid_python_version(metadata.python_version):
                errors.append(
                    f"Invalid Python version: {metadata.python_version}. "
                    "Must be >= 3.10"
                )

        # Validate package name
        if not MetadataValidator._is_valid_package_name(metadata.package_name):
            errors.append(
                "Package name must be a valid Python identifier "
                "(lowercase, no hyphens or spaces)"
            )

        # Validate version
        if not MetadataValidator._is_valid_version(metadata.version):
            errors.append(
                f"Invalid version format: {metadata.version}. "
                "Expected format: X.Y.Z"
            )

        if errors:
            raise ValidationError("\n".join(errors))

        return []

    @staticmethod
    def _is_valid_project_name(name: str) -> bool:
        """Check if project name is valid."""
        pattern = r'^[a-zA-Z][a-zA-Z0-9_-]*$'
        return re.match(pattern, name) is not None

    @staticmethod
    def _is_valid_package_name(name: str) -> bool:
        """Check if package name is valid Python identifier."""
        return name.isidentifier() and name == name.lower()

    @staticmethod
    def _is_valid_python_version(version: str) -> bool:
        """Check if Python version is >= 3.10."""
        try:
            major, minor = map(int, version.split(".")[:2])
            return major >= 3 and minor >= 10
        except (ValueError, AttributeError):
            return False

    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """Check if version follows semantic versioning."""
        pattern = r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$'
        return re.match(pattern, version) is not None
