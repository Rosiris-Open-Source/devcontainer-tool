# Copyright 2025 Manuel Muth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar


@dataclass(frozen=True)
class TEMPLATES:

    # Base directory of templates (relative to this file)
    TEMPLATE_DIR: ClassVar[Path] = Path(__file__).parent / "templates"
    # Template files
    DEVCONTAINER_JSON: ClassVar[str] = "devcontainer.json.j2"
    BASE_DOCKERFILE: ClassVar[str] = "Dockerfile.j2"
    DOCKERFILE_EXTENSIONS_JSON: ClassVar[str] = "dockerfile_extensions.json"
    DEVCONTAINER_EXTENSIONS_JSON: ClassVar[str] = "devcontainer_extensions.json"

    _TEMPLATE_FILES: ClassVar[list[ſtr]] = [
        DEVCONTAINER_JSON,
        BASE_DOCKERFILE,
        DOCKERFILE_EXTENSIONS_JSON,
        DEVCONTAINER_EXTENSIONS_JSON,
    ]

    # Mapping template filename -> destination path in devcontainer
    __mapping_to_default_path: ClassVar[dict[str, Path]] = {
        DEVCONTAINER_JSON: Path(".devcontainer/devcontainer.json"),
        BASE_DOCKERFILE: Path(".docker/Dockerfile"),
    }

    __mapping_to_default_dir: ClassVar[dict[str, Path]] = {
        DEVCONTAINER_JSON: Path(".devcontainer/"),
        BASE_DOCKERFILE: Path(".docker/"),
    }

    __mapping_to_filename: ClassVar[dict[str, Path]] = {
        DEVCONTAINER_JSON: Path("devcontainer.json"),
        BASE_DOCKERFILE: Path("Dockerfile"),
    }

    @classmethod
    def get_template_path(cls, template_name: str) -> Path:
        """Return the absolute path to the template file."""
        if template_name not in cls._TEMPLATE_FILES:
            raise ValueError(f"Unknown template: {template_name}")
        template_file = cls.TEMPLATE_DIR / template_name
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")
        return template_file

    @classmethod
    def get_target_default_path(cls, template_name: str) -> Path:
        """Return the path inside the devcontainer where the template should be copied."""
        target = cls.__mapping_to_default_path.get(template_name)
        if target is None:
            raise ValueError(f"Unknown template: {template_name}")
        return target

    @classmethod
    def get_target_default_dir(cls, template_name: str) -> Path:
        """Return the path inside the devcontainer where the template should be copied."""
        target = cls.__mapping_to_default_dir.get(template_name)
        if target is None:
            raise ValueError(f"Unknown template: {template_name}")
        return target

    @classmethod
    def get_target_filename(cls, template_name: str) -> Path:
        """Return the path inside the devcontainer where the template should be copied."""
        target = cls.__mapping_to_filename.get(template_name)
        if target is None:
            raise ValueError(f"Unknown template: {template_name}")
        return target
