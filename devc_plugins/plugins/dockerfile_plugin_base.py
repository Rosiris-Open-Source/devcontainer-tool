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
from pathlib import Path
from typing import override
import argparse
import questionary

from devc_cli_plugin_system.plugin import Plugin
from devc.constants.defaults import DEFAULT_IMAGES
from devc.constants.templates import TEMPLATES
from devc.core.exceptions.dockerfile_exceptions import (
    DockerfileTemplateNotFoundError,
    DockerfileExistsError,
    DockerfileTemplateRenderError,
)
from devc.core.models.dockerfile_extension_json_scheme import DockerfileHandler
from devc.core.models.options import DockerfileOptions
from devc.core.template_loader import TemplateLoader
from devc.core.template_machine import TemplateMachine
from devc.core.dockerfile_creation_service import DockerfileCreationService
from devc.utils.console import print_error, print_warning
from devc_cli_plugin_system.plugin.plugin_context import PluginContext
from devc.utils.validators.argparse_validators import EmptyOrNewDir, ExistingFile


class DockerfilePluginBase(Plugin):
    """Create a basic Dockerfile."""

    DEFAULT_IMAGE = DEFAULT_IMAGES.UBUNTU
    DEFAULT_TEMPLATE = TEMPLATES.BASE_DOCKERFILE

    @override
    def add_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        parser.add_argument(
            "--image",
            help=f"Base image to use. (Default: {self.DEFAULT_IMAGE})",
            default=self.DEFAULT_IMAGE,
            nargs="?",
        )
        parser.add_argument(
            "--path",
            help="Where to create the devcontainer folder and files.",
            type=EmptyOrNewDir(must_be_empty=False),
            default=str(TEMPLATES.get_target_default_dir(self.DEFAULT_TEMPLATE)),
            nargs="?",
        )
        parser.add_argument(
            "--extend-with",
            help="Path to JSON file to extend the Dockerfile.",
            type=ExistingFile(),
            default=str(self._get_extend_file()),
            nargs="?",
        )
        parser.add_argument(
            "--override",
            help="Override the existing Dockerfile if it exists.",
            action="store_true",
            default=False,
        )
        self._extend_base_arguments(parser, cli_name)

    @override
    def interactive_creation_hook(
        self,
        parser: argparse.ArgumentParser,
        subparser: argparse._SubParsersAction | None,
        cli_name: str,
    ) -> list[str]:

        # Base image
        image = questionary.text(
            "Base image to use:",
            default=self.DEFAULT_IMAGE,
        ).unsafe_ask()

        # Target path
        path = questionary.text(
            "Target path to create Dockerfile:",
            default=str(TEMPLATES.get_target_default_dir(self.DEFAULT_TEMPLATE)),
        ).unsafe_ask()

        # Extend-with
        extend_with = questionary.text(
            "Path to JSON file to extend the Dockerfile:",
            default=str(self._get_extend_file()),
        ).unsafe_ask()

        # Override?
        override = questionary.confirm(
            "Override existing Dockerfile if present?",
            default=False,
        ).unsafe_ask()

        # Build result argv
        result: list[str] = []

        if image:
            result.extend(["--image", image])

        if path:
            result.extend(["--path", path])

        if extend_with:
            result.extend(["--extend-with", extend_with])

        if override:
            result.append("--override")

        # collect interactive selected args from plugins that extend this base plugin
        result.extend(self._extend_base_interactive_creation_hook())
        return result

    def _get_extend_file(self) -> Path:
        """Override to get path to patch file for Dockerfile file."""
        return TEMPLATES.get_template_path(TEMPLATES.DOCKERFILE_EXTENSIONS_JSON)

    def _extend_base_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        """Override to add extra plugin-specific args."""
        pass

    def _extend_base_interactive_creation_hook(self) -> list[str]:
        """Override to add extra interactive questions."""
        return []

    @override
    def main(self, context: PluginContext) -> int:
        dockerfile_handler = self._create_handler_from_args(context.args)
        self._apply_overrides_to_handler_content(dockerfile_handler, context.args)
        options = self._create_options_from_args(context.args)
        creator = DockerfileCreationService(
            template_machine=TemplateMachine(),
            loader=TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR),
        )
        try:
            creator.create_dockerfile(
                template_file=self.DEFAULT_TEMPLATE,
                dockerfile_handler=dockerfile_handler,
                options=options,
            )
        except DockerfileTemplateNotFoundError as e:
            print_error(title="Template Not Found", message=str(e))
            return 1
        except DockerfileExistsError as e:
            print_warning(title="File Already Exists", message=str(e))
            return 1
        except DockerfileTemplateRenderError as e:
            print_error(title="Template Render Error", message=str(e))
            return 1
        return 0

    def _apply_overrides_to_handler_content(
        self,
        dockerfile_handler: DockerfileHandler,
        args: argparse.Namespace,
    ) -> None:
        """
        Override to modify the DockerfileHandler after creation.
        Don't forget to override the image if set with args.
        """
        if args.image:
            dockerfile_handler.override_image(args.image)

    def _create_handler_from_args(
        self,
        args: argparse.Namespace,
    ) -> DockerfileHandler:
        return DockerfileHandler(args.extend_with)

    def _create_options_from_args(
        self,
        args: argparse.Namespace,
    ) -> DockerfileOptions:
        return DockerfileOptions(
            image=args.image,
            path=args.path,
            extend_with=args.extend_with,
            override=args.override,
        )
