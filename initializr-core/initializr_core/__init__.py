"""
AgentScope Initializr - Core Module

A project scaffolding generator for AgentScope applications.
Inspired by Spring Boot Initializr.
"""

__version__ = "0.1.0"

from initializr_core.metadata.models import (
    AgentScopeMetadata,
    AgentType,
    ModelProvider,
    MemoryType,
    FormatterType,
)
from initializr_core.generator.engine import ProjectGenerator

__all__ = [
    "AgentScopeMetadata",
    "AgentType",
    "ModelProvider",
    "MemoryType",
    "FormatterType",
    "ProjectGenerator",
]
