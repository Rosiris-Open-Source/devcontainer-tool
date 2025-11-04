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
from typing_extensions import override
from typing import Any, Dict

from devc_cli_plugin_system.plugin import Plugin
from devc_plugins.plugin_extensions.dev_json_extensions import DevJsonExtensionManager
from devc.constants.templates import TEMPLATES
from devc.core.error.devcontainer_json_errors import DevJsonTemplateNotFoundError, DevJsonTemplateRenderError, DevJsonExistsError
from devc.core.models.devcontainer_extension_json_scheme import DevJsonHandler
from devc.core.models.options import DevContainerJsonOptions
from devc.core.template_loader import TemplateLoader
from devc.core.template_machine import TemplateMachine
from devc.core.devcontainer_json_creation_service import DevcontainerJsonCreationService
from devc.utils.argparse_validators import IsEmptyOrNewDir, IsExistingFile
from devc.utils.console import print_error, print_warning

class DevJsonPluginBase(Plugin):
    """Create a basic devcontainer.json."""

    DEFAULT_TEMPLATE = TEMPLATES.DEVCONTAINER_JSON

    @override
    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "--name",
            help="A name for the dev container displayed in the UI.",
            default="", 
            nargs="?"
        )
        img_build_group = parser.add_mutually_exclusive_group(required=False)
        img_build_group.add_argument(
            "--image",
            help="Image to use if not use a Dockerfile to build a image.",
            default="", 
            nargs="?"
        )
        img_build_group.add_argument(
            "--dockerfile",
            help="Patch to Dockerfile if no existing image is used.",
            default="../.docker/Dockerfile", 
            nargs="?"
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
            help="path to a .json file to extend the .devcontainer.json.",
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
    
    @override
    def main(self, *, ext_manager: DevJsonExtensionManager, parser, args) -> int:
        dev_json_handler: DevJsonHandler = self._create_handler_from_args(args)
        loader = TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR)
        self._add_direct_json_patch(ext_manager, args)
        dev_json_creator = DevcontainerJsonCreationService(template_machine=TemplateMachine(), loader=loader, ext_manager=ext_manager)
        try:
            dev_json_creator.create_devcontainer_json(template_file=self.DEFAULT_TEMPLATE, dev_json=dev_json_handler)

        except DevJsonTemplateNotFoundError as e:
            print_error(title="Template Not Found", message=str(e))
            return 1

        except DevJsonExistsError as e:
            print_warning(title="File Already Exists", message=str(e))
            return 1

        except DevJsonTemplateRenderError as e:
            print_error(title="Template Render Error", message=str(e))
            return 1
    
    def _get_direct_json_patch(self, args) -> Dict[str, Any]:
        """Override to apply a patch direct to devcontainer.json. This is possible since json is a structured format."""
        return {}
    
    def _add_direct_json_patch(self, ext_manager:DevJsonExtensionManager, args):
        patch = self._get_direct_json_patch(args)
        ext_manager.add_update(patch)

    def _add_custom_arguments(self, parser, cli_name) -> None:
        """Override to add extra plugin-specific args."""
        pass

    def _get_extend_file(self) -> Path:
        """Override to apply patch though an extension file (jinja template) to devcontainer.json file."""
        return TEMPLATES.get_template_path(TEMPLATES.DEVCONTAINER_EXTENSIONS_JSON)

    def _apply_args_to_handler(self, dev_json_handler: DevJsonHandler, args) -> None:
        """Override to modify the DevJsonHandler after creation. Don't forget to override the image if set with args."""
        # Apply overrides
        if args.name:
            dev_json_handler.content.pre_defined_extensions.name = args.name
        if args.image:
            dev_json_handler.content.pre_defined_extensions.image = args.image
        if args.dockerfile:
            dev_json_handler.content.pre_defined_extensions.dockerfile = args.dockerfile
        
    def _create_handler_from_args(self, args) -> DevJsonHandler:
        options = DevContainerJsonOptions(
            name=args.name,
            image=args.image,
            dockerfile=args.dockerfile,
            path=args.path,
            extend_with=args.extend_with,
            override=args.override
        )
        
        dev_json_handler : DevJsonHandler = DevJsonHandler(options)
        self._apply_args_to_handler(dev_json_handler, args)

        return dev_json_handler