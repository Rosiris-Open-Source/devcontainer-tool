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
from typing import ClassVar, Dict, List

@dataclass(frozen=True)
class TEMPLATES:
    # Template file names
    DEVCONTAINER_JSON: ClassVar[str] = "devcontainer.json.j2"
    BASE_DOCKERFILE: ClassVar[str] = "Dockerfile.j2"

    _TEMPLATE_FILES: ClassVar[List[ſtr]] = [
        DEVCONTAINER_JSON,
        BASE_DOCKERFILE,
    ]

    # Base directory of templates (relative to this file)
    TEMPLATE_DIR: ClassVar[Path] = Path(__file__).parent.parent.parent / "templates"

    # Mapping template filename -> destination path in devcontainer
    __mapping_to_devcontainer: ClassVar[Dict[str, Path]] = {
        DEVCONTAINER_JSON: Path(".devcontainer/devcontainer.json"),
        BASE_DOCKERFILE: Path(".devcontainer/Dockerfile"),
    }

    @classmethod
    def get_template_path(cls, template_name: str) -> Path:
        """Returns the absolute path to the template file."""
        if template_name not in cls._TEMPLATE_FILES:
            raise ValueError(f"Unknown template: {template_name}")
        template_file = cls._TEMPLATE_DIR / template_name
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")
        return template_file

    @classmethod
    def get_target_path(cls, template_name: str) -> Path:
        """Returns the path inside the devcontainer where the template should be copied."""
        target = cls.__mapping_to_devcontainer.get(template_name)
        if target is None:
            raise ValueError(f"Unknown template: {template_name}")
        return target