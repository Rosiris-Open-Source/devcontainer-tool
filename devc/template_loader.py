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

from jinja2 import Environment, FileSystemLoader, Template, StrictUndefined, meta
from pathlib import Path
from typing import Any, Dict

class TemplateLoader:
    def __init__(self, template_dir: Path):
        """
        Initialize the loader with the directory containing Jinja2 templates.
        """
        if not template_dir.is_dir():
            raise NotADirectoryError(f"Template directory does not exist: {template_dir}")
        self.env = Environment(loader=FileSystemLoader(str(template_dir)), undefined=StrictUndefined)
        self.template_dir = template_dir
    
    def get_undeclared_variables(self, template_name: str):
        """
        Return the set of undeclared variables (no default provided in the template).
        """
        source, _, _ = self.env.loader.get_source(self.env, template_name)
        parsed_content = self.env.parse(source)
        return meta.find_undeclared_variables(parsed_content)

    def load_template(self, template_name: str) -> Template:
        """
        Load a Jinja2 template by filename.
        """
        try:
            return self.env.get_template(template_name)
        except Exception as e:
            raise FileNotFoundError(f"Template not found: {template_name}") from e

    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Render the template with the given context dictionary.
        """
        template = self.load_template(template_name)
        return template.render(**context)

    def render_to_target(self, template_name: str, target_path: Path, context: Dict[str, Any]) -> None:
        """
        Render the template and write it to the target path.
        Creates parent directories if needed.
        """
        rendered_content = self.render_template(template_name, context)
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(rendered_content)
