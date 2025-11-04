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
from dataclasses import asdict
from pathlib import Path
from pathlib import Path
from typing import Any, Dict
import jinja2 
import json
import re

from devc_plugins.plugin_extensions.dev_json_extensions import DevJsonExtensionManager
from devc.constants.templates import TEMPLATES
from devc.core.error.devcontainer_json_errors import DevJsonTemplateNotFoundError, DevJsonTemplateRenderError, DevJsonExistsError
from devc.core.models.devcontainer_extension_json_scheme import DevJsonHandler
from devc.core.template_loader import TemplateLoaderABC
from devc.core.template_machine import TemplateMachine
from devc.utils.logging import get_logger
from devc.utils.merge_dicts import AppendListMerge

logger = get_logger(__name__)

class DevcontainerJsonCreationService:
    def __init__(self, *, template_machine: TemplateMachine, loader: TemplateLoaderABC, ext_manager: DevJsonExtensionManager):
        self._template_machine : TemplateMachine = template_machine
        self._loader : TemplateLoaderABC = loader
        self._ext_manager : DevJsonExtensionManager = ext_manager
        self._json_update_strategy = AppendListMerge()

    def _load_template(self, template_file: str) -> jinja2.Template:
        try:
            template = self._loader.load_template(template_file)
        except FileNotFoundError:
            logger.error("Template %s not found in %s", 
                         TEMPLATES.get_target_filename(template_file), 
                         TEMPLATES.TEMPLATE_DIR)
            raise DevJsonTemplateNotFoundError(f"Template {template_file} not found")
        return template

    def _update_created_dev_json_with_extensions(self, path: Path) -> None:
        updates = self._ext_manager.get_combined_updates()
        if not updates:
            logger.debug("No devcontainer.json plugin updates to apply.")
            return

        current_data: Dict[str, Any] = json.loads(path.read_text())
        merged = self._json_update_strategy.merge_dicts(current_data, updates)
        path.write_text(json.dumps(merged, indent=4))
        logger.info("Applied following plugin extensions to [bold blue]devcontainer.json[/bold blue] at %s", path)
        for ext_name in self._ext_manager.called_extensions.keys():
            logger.info(f"\t - {ext_name}")
  

    def _postprocess_rendered_json(self, path: Path) -> None:
        """
        Clean up trailing commas and ensure valid JSON formatting.
        """
        text = path.read_text()

        # remove trailing commas before } or ]
        cleaned = re.sub(r',(\s*[}\]])', r'\1', text)

        try:
            # validate and pretty-print the JSON
            parsed = json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error("Postprocessing failed: invalid JSON after cleanup (%s)", e)
            # write cleaned text anyway to aid debugging
            path.write_text(cleaned)
            raise

        # write validated, formatted JSON
        path.write_text(json.dumps(parsed, indent=4))
        logger.debug("Postprocessed and cleaned JSON at %s", path)
    
    def create_devcontainer_json(
        self,
        template_file: str,
        dev_json: DevJsonHandler
    ) -> None:

        template = self._load_template(template_file=template_file)

        logger.info(f"Create a [bold blue]devcontainer.json[/bold blue] with following options:\n{dev_json.options}")
        # check path
        path: Path = dev_json.options.path / TEMPLATES.get_target_filename(template_file)
        if not dev_json.options.override and path.exists():
            logger.warning("Target file %s already exists", path)
            raise DevJsonExistsError(f"The target file '{path}' already exists.")

        # render template with given options
        try:
            predefs = dict(asdict(dev_json.content.pre_defined_extensions))
            self._template_machine.render_to_target(
                template=template, target_path=path, context=predefs
            )
        except jinja2.UndefinedError as e:
            logger.error("Template render error: %s", e.message)
            raise DevJsonTemplateRenderError(
                f"Missing required values to render template {template_file}: {e.message}."
            )

        # make sure no trailing commas and the like
        self._postprocess_rendered_json(path=path)

        # Apply plugin updates
        self._update_created_dev_json_with_extensions(path=path)

        logger.info("Creation of [bold blue]devcontainer.json[/bold blue] successfully at %s", path)
