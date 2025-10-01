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
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from devc_cli_plugin_system.plugin import Plugin
from devc.constants.templates import TEMPLATES
from devc.core.error.devcontainer_json_errors import DevJsonTemplateNotFoundError, DevJsonTemplateRenderError, DevJsonExistsError
from devc.core.models.devcontainer_extension_json_scheme import DevcontainerHandler
from devc.core.models.devcontainer_json_options import DevContainerJsonOptions
from devc.core.template_loader import TemplateLoader
from devc.core.template_machine import TemplateMachine
from devc.devcontainer_json_creation_service import DevcontainerJsonCreationService
from devc.utils.path_utils import IsEmptyOrNewDir, IsExistingFile

console = Console()
class BaseDevJsonPlugin(Plugin):
    def __init__(self) -> None:
        self.template_file = TEMPLATES.DEVCONTAINER_JSON
    """Create the a basic devcontainer json."""

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
            default=str(TEMPLATES.get_target_default_dir(self.template_file)), 
            nargs="?"
        )
        parser.add_argument(
            "--extend-with",
            help="path to a .json file to extend the .devcontainer.json.",
            type=IsExistingFile(),
            default=str(TEMPLATES.get_template_path(TEMPLATES.DEVCONTAINER_EXTENSIONS_JSON)), 
            nargs="?"
        )
        parser.add_argument(
            "--override",
            help="Override the existing Dockerfile if it exists.",
            action="store_true",
            default=False
        )
        

    def main(self, *, args):
        options = DevContainerJsonOptions(
            name=args.name,
            image=args.image,
            dockerfile=args.dockerfile,
            path=args.path,
            extend_with=args.extend_with,
            override=args.override
        )

        loader = TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR)
        dev_json_creator = DevcontainerJsonCreationService(template_machine=TemplateMachine(), loader=loader)
        try:
            dev_json_creator.create_devcontainer_json(options=options, template_file=TEMPLATES.DEVCONTAINER_JSON, dev_json_handler=DevcontainerHandler)

        except DevJsonTemplateNotFoundError as e:
            console.print(Panel.fit(
                Text(str(e), style="bold red"),
                title="[red]Template Not Found[/red]",
                border_style="red"
            ))
            return 1

        except DevJsonExistsError as e:
            console.print(Panel.fit(
                Text(str(e), style="bold yellow"),
                title="[yellow]File Already Exists[/yellow]",
                border_style="yellow"
            ))
            return 1

        except DevJsonTemplateRenderError as e:
            console.print(Panel.fit(
                Text(str(e), style="bold red"),
                title="[red]Template Render Error[/red]",
                border_style="red"
            ))
            return 1