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
from devc.core.error.dockerfile_errors import DockerfileTemplateNotFoundError, DockerfileExistsError, DockerfileTemplateRenderError
from devc.core.models.dockerfile_extension_json_scheme import DockerfileHandler
from devc.core.template_loader import TemplateLoaderABC
from devc.core.template_machine import TemplateMachine
from devc.utils.logging import get_logger

logger = get_logger(__name__)
class DockerfileCreationService:
    def __init__(self, template_machine: TemplateMachine, loader: TemplateLoaderABC):
        self.template_machine = template_machine
        self.loader = loader

    def create_dockerfile(
        self,
        template_file: str,
        dockerfile_handler: DockerfileHandler
    ) -> None:
        try:
            template = self.loader.load_template(template_file)
        except FileNotFoundError:
            logger.error("Template %s not found in %s", 
                         TEMPLATES.get_target_filename(template_file), 
                         TEMPLATES.TEMPLATE_DIR)
            raise DockerfileTemplateNotFoundError(f"Template {template_file} not found")

        path: Path = dockerfile_handler.options.path / TEMPLATES.get_target_filename(template_file)
        if not dockerfile_handler.options.override and path.exists():
            logger.warning("Target file %s already exists", path)
            raise DockerfileExistsError(f"The target file '{path}' already exists.")

        try:
            predefs = dict(asdict(dockerfile_handler.content.pre_defined_extensions))
            self.template_machine.render_to_target(
                template=template, target_path=path, context=predefs
            )
        except jinja2.UndefinedError as e:
            logger.error("Template render error: %s", e.message)
            raise DockerfileTemplateRenderError(
                f"Missing required values to render template {template_file}: {e.message}"
            )

        logger.info("Creation of devcontainer.json successfully at %s", path)
