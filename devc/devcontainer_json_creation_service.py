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
import jinja2

from devc.constants.templates import TEMPLATES
from devc.core.error.devcontainer_json_errors import DevJsonTemplateNotFoundError, DevJsonTemplateRenderError, DevJsonExistsError
from devc.core.logging import logger
from devc.core.models.devcontainer_extension_json_scheme import DevcontainerHandler
from devc.core.models.devcontainer_json_options import DevContainerJsonOptions
from devc.core.template_loader import TemplateLoaderABC
from devc.core.template_machine import TemplateMachine

class DevcontainerJsonCreationService:
    def __init__(self, template_machine: TemplateMachine, loader: TemplateLoaderABC):
        self.template_machine = template_machine
        self.loader = loader

    def create_devcontainer_json(
        self,
        options: DevContainerJsonOptions,
        template_file: str,
        dev_json_handler: DevcontainerHandler
    ) -> None:
        try:
            template = self.loader.load_template(template_file)
        except FileNotFoundError:
            logger.error("Template %s not found in %s", 
                         TEMPLATES.get_target_filename(template_file), 
                         TEMPLATES.TEMPLATE_DIR)
            raise DevJsonTemplateNotFoundError(f"Template {template_file} not found")

        path: Path = options.path / TEMPLATES.get_target_filename(template_file)
        if not options.override and path.exists():
            logger.warning("Target file %s already exists", path)
            raise DevJsonExistsError(f"The target file '{path}' already exists.")

        devcontainer_json : DevcontainerHandler = dev_json_handler(options.extend_with)

        # Apply overrides
        if options.name:
            devcontainer_json.content.pre_defined_extensions.name = options.name
        if options.image:
            devcontainer_json.content.pre_defined_extensions.image = options.image
        if options.dockerfile:
            devcontainer_json.content.pre_defined_extensions.dockerfile = options.dockerfile

        try:
            predefs = dict(asdict(devcontainer_json.content.pre_defined_extensions))
            print(predefs)
            self.template_machine.render_to_target(
                template=template, target_path=path, context=predefs
            )
        except jinja2.UndefinedError as e:
            logger.error("Template render error: %s", e.message)
            raise DevJsonTemplateRenderError(
                f"Missing required values to render template {template_file}: {e.message}"
            )

        logger.info("Creation of devcontainer.json successfully at %s", path)
