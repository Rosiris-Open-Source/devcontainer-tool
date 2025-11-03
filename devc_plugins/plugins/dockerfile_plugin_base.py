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

from devc_cli_plugin_system.plugin import Plugin
from devc.constants.defaults import DEFAULT_IMAGES
from devc.constants.templates import TEMPLATES
from devc.core.error.dockerfile_errors import DockerfileTemplateNotFoundError, DockerfileExistsError, DockerfileTemplateRenderError
from devc.core.models.dockerfile_extension_json_scheme import DockerfileHandler
from devc.core.models.options import DockerfileOptions
from devc.core.template_loader import TemplateLoader
from devc.core.template_machine import TemplateMachine
from devc.dockerfile_creation_service import DockerfileCreationService
from devc.utils.console import print_error, print_warning
from devc.utils.path_utils import IsEmptyOrNewDir, IsExistingFile

class DockerfilePluginBase(Plugin, ABC):
    """Abstract base for all Dockerfile-creating plugins."""

    DEFAULT_IMAGE = DEFAULT_IMAGES.UBUNTU
    DEFAULT_TEMPLATE = TEMPLATES.BASE_DOCKERFILE

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "--image",
            help=f"Base image to use. (Default: {self.DEFAULT_IMAGE})",
            default=self.DEFAULT_IMAGE, nargs="?"
        )
        parser.add_argument(
            "--path",
            help="Where to create the devcontainer folder and files.",
            type=IsEmptyOrNewDir(must_be_empty=False),
            default=str(TEMPLATES.get_target_default_dir(self.DEFAULT_TEMPLATE)),
            nargs="?"
        )
        parser.add_argument(
            "--extend-with",
            help="Path to JSON file to extend the Dockerfile.",
            type=IsExistingFile(),
            default=str(self._get_extend_file()),
            nargs="?"
        )
        parser.add_argument(
            "--override",
            help="Override the existing Dockerfile if it exists.",
            action="store_true",
            default=False
        )
        self._add_custom_arguments(parser, cli_name)

    def main(self, *, args):
        dockerfile_handler = self._create_handler_from_args(args)
        loader = TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR)
        creator = DockerfileCreationService(template_machine=TemplateMachine(), loader=loader)
        try:
            creator.create_dockerfile(template_file=self.DEFAULT_TEMPLATE, dockerfile_handler=dockerfile_handler)
        except DockerfileTemplateNotFoundError as e:
            print_error("Template Not Found", str(e))
            return 1
        except DockerfileExistsError as e:
            print_warning("File Already Exists", str(e))
            return 1
        except DockerfileTemplateRenderError as e:
            print_error("Template Render Error", str(e))
            return 1

    @abstractmethod
    def _get_extend_file(self) -> Path:
        """Override to apply patch to Dockerfile. Each plugin must define JSON patch file."""
        pass

    def _add_custom_arguments(self, parser, cli_name):
        """Override to add extra plugin-specific args."""
        pass

    def _apply_args_to_handler(self, dockerfile_handler: DockerfileHandler, args):
        """Override to modify the DockerfileHandler after creation. Don't forget to override the image if set with args."""
        if args.image:
            dockerfile_handler.override_image(args.image)

    def _create_handler_from_args(self, args) -> DockerfileHandler:
        options = DockerfileOptions(
            image=args.image,
            path=args.path,
            extend_with=args.extend_with,
            override=args.override
        )

        dockerfile_handler = DockerfileHandler(options)
        self._apply_args_to_handler(dockerfile_handler, args)
        return dockerfile_handler
