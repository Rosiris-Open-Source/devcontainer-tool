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

from abc import ABC, abstractmethod
from pathlib import Path
from jinja2 import (
    Environment,
    FileSystemLoader,
    Template,
    StrictUndefined,
    Undefined,
    UndefinedError,
)


class TemplateLoaderABC(ABC):
    @abstractmethod
    def load_template(self, template_name: str) -> Template:
        """Load a Jinja2 template by filename."""
        pass


class TemplateLoader(TemplateLoaderABC):
    def __init__(self, template_dir: Path, undefined: type[Undefined] = StrictUndefined):
        """Initialize the loader with the directory containing Jinja2 templates."""
        if not template_dir.is_dir():
            raise NotADirectoryError(f"Template directory does not exist: {template_dir}")
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            undefined=undefined,
        )
        self.env.filters["required"] = self._required_filter

        self.template_dir = template_dir

    def load_template(self, template_name: str) -> Template:
        """Load a Jinja2 template by filename."""
        try:
            return self.env.get_template(template_name)
        except Exception as e:
            raise FileNotFoundError(f"Template not found: {template_name}") from e

    @staticmethod
    def _required_filter(value: str, field_name: str) -> str:
        """Require non-empty value or raise error."""
        if not value or (isinstance(value, str) and not value.strip()):
            raise UndefinedError(f"Required field '{field_name}' cannot be empty")
        return value
