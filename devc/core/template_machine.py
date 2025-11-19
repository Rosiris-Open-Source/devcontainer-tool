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

from jinja2 import Template, meta
from pathlib import Path
from typing import Any


class TemplateMachine:

    def get_undeclared_variables(self, template: Template) -> set[str]:
        """Return the set of undeclared variables (no default provided in the template)."""
        res: set[str] = meta.find_undeclared_variables(template)
        return res

    def render_template(self, template: Template, context: dict[str, Any]) -> str:
        """Render the template with the given context dictionary."""
        res: str = template.render(**context)
        return res

    def render_to_target(
        self, template: Template, target_path: Path, context: dict[str, Any]
    ) -> None:
        """
        Render the template and write it to the target path.
        Creates parent directories if needed.
        """
        rendered_content = self.render_template(template, context)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(rendered_content)
