"""
Skill storage manager for AgentScope Initializr.

Manages skill packages uploaded by administrators.
"""

import os
import json
import shutil
import zipfile
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib


class SkillMetadata:
    """Metadata for a skill package."""

    def __init__(
        self,
        skill_id: str,
        name: str,
        description: str,
        version: str,
        license: str,
        author: str = "",
        tags: List[str] = None,
        uploaded_at: str = None,
        file_path: str = None,
        size_bytes: int = 0,
    ):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.version = version
        self.license = license
        self.author = author
        self.tags = tags or []
        self.uploaded_at = uploaded_at or datetime.utcnow().isoformat()
        self.file_path = file_path
        self.size_bytes = size_bytes

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "skill_id": self.skill_id,
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "license": self.license,
            "author": self.author,
            "tags": self.tags,
            "uploaded_at": self.uploaded_at,
            "file_path": self.file_path,
            "size_bytes": self.size_bytes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillMetadata":
        """Create from dictionary."""
        return cls(**data)


class SkillManager:
    """Manager for skill packages."""

    def __init__(self, storage_dir: str = None):
        """
        Initialize skill manager.

        Args:
            storage_dir: Directory to store skill packages
        """
        if storage_dir is None:
            storage_dir = os.getenv("SKILLS_STORAGE_DIR", "./data/skills")

        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        self.skills_file = self.storage_dir / "skills.json"
        self.skills_index = self._load_index()

        # Create skills directory for extracted packages
        self.skills_packages_dir = self.storage_dir / "packages"
        self.skills_packages_dir.mkdir(exist_ok=True)

    def _load_index(self) -> Dict[str, Dict[str, Any]]:
        """Load skills index from JSON file."""
        if self.skills_file.exists():
            with open(self.skills_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_index(self):
        """Save skills index to JSON file."""
        with open(self.skills_file, "w", encoding="utf-8") as f:
            json.dump(self.skills_index, f, indent=2, ensure_ascii=False)

    def _generate_skill_id(self, name: str, version: str) -> str:
        """Generate unique skill ID."""
        content = f"{name}:{version}:{datetime.utcnow().isoformat()}"
        return hashlib.md5(content.encode()).hexdigest()[:12]

    def _validate_skill_structure(self, extract_path: Path) -> tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Validate that the extracted package follows AgentScope skill structure.

        Args:
            extract_path: Path to extracted package

        Returns:
            (is_valid, error_message, skill_metadata)
        """
        # Check for SKILL.md file
        skill_md_files = list(extract_path.glob("SKILL.md")) + list(extract_path.glob("*/SKILL.md"))

        if not skill_md_files:
            return False, "SKILL.md file not found in package", None

        skill_md_path = skill_md_files[0]

        # Parse SKILL.md
        try:
            with open(skill_md_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract YAML frontmatter
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    yaml_content = parts[1]
                    import yaml
                    metadata = yaml.safe_load(yaml_content)

                    if not metadata.get("name"):
                        return False, "SKILL.md missing 'name' field", None

                    if not metadata.get("description"):
                        return False, "SKILL.md missing 'description' field", None

                    # Valid skill structure
                    return True, "", metadata
                else:
                    return False, "Invalid SKILL.md format (missing YAML frontmatter)", None
            else:
                return False, "SKILL.md must start with YAML frontmatter (---)", None

        except yaml.YAMLError as e:
            return False, f"Invalid YAML in SKILL.md: {str(e)}", None
        except Exception as e:
            return False, f"Error reading SKILL.md: {str(e)}", None

    def upload_skill(
        self,
        zip_file_path: str,
        uploaded_by: str = "admin"
    ) -> tuple[bool, str, Optional[SkillMetadata]]:
        """
        Upload and validate a skill package.

        Args:
            zip_file_path: Path to uploaded ZIP file
            uploaded_by: Username of uploader

        Returns:
            (success, message, skill_metadata)
        """
        zip_path = Path(zip_file_path)

        if not zip_path.exists():
            return False, "ZIP file not found", None

        # Create temp directory for extraction
        temp_dir = self.storage_dir / "temp"
        temp_dir.mkdir(exist_ok=True)

        try:
            # Extract ZIP
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

            # Validate skill structure
            is_valid, error_msg, skill_metadata_dict = self._validate_skill_structure(temp_dir)

            if not is_valid:
                shutil.rmtree(temp_dir)
                return False, error_msg, None

            # Generate skill ID
            skill_id = self._generate_skill_id(
                skill_metadata_dict["name"],
                skill_metadata_dict.get("version", "1.0.0")
            )

            # Move to permanent location
            skill_dir = self.skills_packages_dir / skill_id
            if skill_dir.exists():
                shutil.rmtree(skill_dir)
            shutil.move(str(temp_dir), str(skill_dir))

            # Get file size
            file_size = zip_path.stat().st_size

            # Copy ZIP to storage
            zip_storage_path = self.storage_dir / "zips" / f"{skill_id}.zip"
            zip_storage_path.parent.mkdir(exist_ok=True)
            shutil.copy2(zip_path, zip_storage_path)

            # Create metadata
            metadata = SkillMetadata(
                skill_id=skill_id,
                name=skill_metadata_dict["name"],
                description=skill_metadata_dict["description"],
                version=skill_metadata_dict.get("version", "1.0.0"),
                license=skill_metadata_dict.get("license", "MIT"),
                author=skill_metadata_dict.get("author", ""),
                tags=skill_metadata_dict.get("tags", []),
                file_path=str(zip_storage_path),
                size_bytes=file_size,
            )

            # Save to index
            self.skills_index[skill_id] = metadata.to_dict()
            self._save_index()

            return True, "Skill uploaded successfully", metadata

        except zipfile.BadZipFile:
            return False, "Invalid ZIP file", None
        except Exception as e:
            return False, f"Error uploading skill: {str(e)}", None
        finally:
            # Clean up temp directory
            if temp_dir.exists():
                shutil.rmtree(temp_dir)

    def list_skills(self) -> List[SkillMetadata]:
        """List all available skills."""
        skills = []
        for skill_data in self.skills_index.values():
            skills.append(SkillMetadata.from_dict(skill_data))
        return skills

    def get_skill(self, skill_id: str) -> Optional[SkillMetadata]:
        """Get skill by ID."""
        skill_data = self.skills_index.get(skill_id)
        if skill_data:
            return SkillMetadata.from_dict(skill_data)
        return None

    def delete_skill(self, skill_id: str) -> tuple[bool, str]:
        """
        Delete a skill package.

        Args:
            skill_id: Skill ID to delete

        Returns:
            (success, message)
        """
        if skill_id not in self.skills_index:
            return False, "Skill not found"

        try:
            # Delete package directory
            skill_dir = self.skills_packages_dir / skill_id
            if skill_dir.exists():
                shutil.rmtree(skill_dir)

            # Delete ZIP file
            zip_path = self.storage_dir / "zips" / f"{skill_id}.zip"
            if zip_path.exists():
                zip_path.unlink()

            # Remove from index
            del self.skills_index[skill_id]
            self._save_index()

            return True, "Skill deleted successfully"

        except Exception as e:
            return False, f"Error deleting skill: {str(e)}"

    def get_skill_package_path(self, skill_id: str) -> Optional[Path]:
        """Get the path to extracted skill package."""
        skill_dir = self.skills_packages_dir / skill_id
        if skill_dir.exists():
            return skill_dir
        return None

    def search_skills(self, query: str) -> List[SkillMetadata]:
        """Search skills by name, description, or tags."""
        query_lower = query.lower()
        results = []

        for skill_data in self.skills_index.values():
            skill = SkillMetadata.from_dict(skill_data)

            # Search in name, description, tags
            if (
                query_lower in skill.name.lower() or
                query_lower in skill.description.lower() or
                any(query_lower in tag.lower() for tag in skill.tags)
            ):
                results.append(skill)

        return results
