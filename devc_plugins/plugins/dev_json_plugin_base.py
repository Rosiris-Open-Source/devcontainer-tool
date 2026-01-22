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
from typing import Any
import argparse
import questionary

from devc_cli_plugin_system.plugin import Plugin
from devc_cli_plugin_system.plugin_extensions.extension_manager import ExtensionManager
from devc_cli_plugin_system.plugin.plugin_context import PluginContext
from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonExtensionManager,
)
from devc.constants.templates import TEMPLATES
from devc.core.exceptions.devcontainer_json_exception import (
    DevJsonTemplateNotFoundError,
    DevJsonTemplateRenderError,
    DevJsonExistsError,
)
from devc.core.models.devcontainer_extension_json_scheme import DevJsonHandler
from devc.core.models.options import DevContainerJsonOptions
from devc.core.template_loader import TemplateLoader
from devc.core.template_machine import TemplateMachine
from devc.core.devcontainer_json_creation_service import (
    DevcontainerJsonCreationService,
)
from devc.constants.plugin_constants import PLUGIN_EXTENSION_ARGUMENT_GROUPS
from devc.utils.argparse_helpers import get_or_create_group
from devc.utils.console import print_error, print_warning
from devc.utils.validators import argparse_validators
from devc.utils.validators import questionary_validators


class DevJsonPluginBase(Plugin):
    """Create a basic devcontainer.json."""

    DEFAULT_TEMPLATE = TEMPLATES.DEVCONTAINER_JSON
    PLUGIN_EXTENSION_GROUP = "devc_commands.dev_json.plugins.extensions"
    PLUGIN_EXTENSION_MANAGER = DevJsonExtensionManager

    @override
    def add_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        base_group = get_or_create_group(parser, PLUGIN_EXTENSION_ARGUMENT_GROUPS.BASIC)
        base_group.add_argument(
            "--name",
            help="A name for the dev container displayed in the UI.",
            default="",
            type=argparse_validators.NotEmpty(),
            nargs="?",
            required=True,
        )
        img_build_group = base_group.add_mutually_exclusive_group(required=False)
        img_build_group.add_argument(
            "--image",
            help="Image to use if not use a Dockerfile to build a image.",
            default="",
            nargs="?",
        )
        img_build_group.add_argument(
            "--dockerfile",
            help="Patch to Dockerfile if no existing image is used.",
            default="../.docker/Dockerfile",
            nargs="?",
        )
        base_group.add_argument(
            "--path",
            help="Where to create the devcontainer folder and files.",
            type=argparse_validators.EmptyOrNewDir(must_be_empty=False),
            default=str(TEMPLATES.get_target_default_dir(self.DEFAULT_TEMPLATE)),
            nargs="?",
        )
        base_group.add_argument(
            "--extend-with",
            help="path to a .json file to extend the .devcontainer.json.",
            type=argparse_validators.ExistingFile(),
            default=str(self._get_extend_file()),
            nargs="?",
        )
        base_group.add_argument(
            "--override",
            help="Override the existing Dockerfile if it exists.",
            action="store_true",
            default=False,
        )
        self._extend_base_arguments(parser, cli_name)

    def _get_extend_file(self) -> Path:
        """Override to apply patch though an extension file (jinja template) to devcontainer.json file."""  # noqa: E501
        return TEMPLATES.get_template_path(TEMPLATES.DEVCONTAINER_EXTENSIONS_JSON)

    def _extend_base_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        """Override to add extra plugin-specific args."""
        pass

    def _extend_base_interactive_creation_hook(self) -> list[str]:
        """Override to add extra interactive questions."""
        return []

    @override
    def interactive_creation_hook(
        self,
        parser: argparse.ArgumentParser,
        subparser: argparse._SubParsersAction | None,
        cli_name: str,
    ) -> list[str]:

        # Name
        name = questionary.text(
            "Devcontainer name:",
            default="",
            validate=questionary_validators.NotEmpty(),
            instruction="(Visible in UI, cannot be empty)",
        ).unsafe_ask()

        # Choose between image or dockerfile
        img_choice = questionary.select(
            "Select the container base:",
            choices=[
                {"name": "Use an existing image", "value": "image"},
                {"name": "Use a Dockerfile", "value": "dockerfile"},
            ],
        ).unsafe_ask()

        image = ""
        dockerfile = ""

        if img_choice == "image":
            image = questionary.text(
                "Image to use:",
                default="",
                validate=questionary_validators.NotEmpty(),
                instruction="(Cannot be empty)",
            ).unsafe_ask()
        else:
            dockerfile = questionary.text(
                "Path to Dockerfile:",
                default="../.docker/Dockerfile",
            ).unsafe_ask()

        # Path
        path = questionary.text(
            "Target path for creating the devcontainer:",
            default=str(TEMPLATES.get_target_default_dir(self.DEFAULT_TEMPLATE)),
        ).unsafe_ask()

        # Extend-with
        extend_with = questionary.text(
            "Path to .json file extending devcontainer.json:",
            default=str(self._get_extend_file()),
        ).unsafe_ask()

        # Override Dockerfile?
        override = questionary.confirm(
            "Override existing Dockerfile if present?",
            default=False,
        ).unsafe_ask()

        # Start building argv
        result: list[str] = []

        if name:
            result.extend(["--name", name])

        if image:
            result.extend(["--image", image])
        elif dockerfile:
            result.extend(["--dockerfile", dockerfile])

        if path:
            result.extend(["--path", path])

        if extend_with:
            result.extend(["--extend-with", extend_with])

        if override:
            result.append("--override")

        # collect interactive selected args from plugins that extend this base plugin
        result.extend(self._extend_base_interactive_creation_hook())
        return result

    @override
    def main(self, context: PluginContext) -> int:
        if context.ext_manager is None:
            print_error(
                title="Wrong Plugin Context.",
                message="No extension manager given in plugin context.",
            )
            return 1

        self._add_live_json_patch(context.args, context.ext_manager)
        # create the file patch handler and update with given arguments
        dev_json_handler = self._create_handler_from_args(context.args)
        self._apply_overrides_to_handler_content(dev_json_handler, context.args)
        options = self._create_options_from_args(context.args)
        dev_json_creator = DevcontainerJsonCreationService(
            template_machine=TemplateMachine(),
            loader=TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR),
            ext_manager=context.ext_manager,
        )
        try:
            dev_json_creator.create_devcontainer_json(
                template_file=self.DEFAULT_TEMPLATE,
                dev_json=dev_json_handler,
                options=options,
            )

        except DevJsonTemplateNotFoundError as e:
            print_error(title="Template Not Found", message=str(e))
            return 1

        except DevJsonExistsError as e:
            print_warning(title="File Already Exists", message=str(e))
            return 1

        except DevJsonTemplateRenderError as e:
            print_error(title="Template Render Error", message=str(e))
            return 1
        return 0

    def _add_live_json_patch(
        self,
        args: argparse.Namespace,
        ext_manager: ExtensionManager,
    ) -> None:
        patch = self._get_direct_json_patch(args)
        ext_manager.add_update(patch)

    def _get_direct_json_patch(
        self,
        args: argparse.Namespace,
    ) -> dict[str, Any]:
        """Override to apply a patch direct to devcontainer.json. This is possible since json is a structured format."""  # noqa: E501
        return {}

    def _create_handler_from_args(
        self,
        args: argparse.Namespace,
    ) -> DevJsonHandler:
        return DevJsonHandler(args.extend_with)

    def _apply_overrides_to_handler_content(
        self,
        dev_json_handler: DevJsonHandler,
        args: argparse.Namespace,
    ) -> None:
        """Override to modify the DevJsonHandler after creation. Don't forget to override the image if set with args."""  # noqa: E501
        # Apply overrides
        if args.name:
            dev_json_handler.content.pre_defined_extensions.name = args.name
        if args.image:
            dev_json_handler.content.pre_defined_extensions.image = args.image
        if args.dockerfile:
            dev_json_handler.content.pre_defined_extensions.dockerfile = args.dockerfile

    def _create_options_from_args(
        self,
        args: argparse.Namespace,
    ) -> DevContainerJsonOptions:
        return DevContainerJsonOptions(
            name=args.name,
            image=args.image,
            dockerfile=args.dockerfile,
            path=args.path,
            extend_with=args.extend_with,
            override=args.override,
        )
