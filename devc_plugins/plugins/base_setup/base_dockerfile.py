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
from devc.constants.defaults import DEFAULTS
from devc.constants.templates import TEMPLATES
from devc.core.error.dockerfile_errors import DockerfileTemplateNotFoundError, DockerfileExistsError, DockerfileTemplateRenderError
from devc.core.models.dockerfile_extension_json_scheme import DockerfileHandler
from devc.core.models.dockerfile_options import DockerfileOptions
from devc.core.template_loader import TemplateLoader
from devc.core.template_machine import TemplateMachine
from devc.dockerfile_creation_service import DockerfileCreationService
from devc.utils.path_utils import IsEmptyOrNewDir, IsExistingFile

console = Console()
class BaseDockerfilePlugin(Plugin):
    """Create the a basic development container setup."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "--image",
            help=f"Image to use. (Default: {DEFAULTS.DEFAULT_UBUNTU_IMG})",
            default=f"{DEFAULTS.DEFAULT_UBUNTU_IMG}", 
            nargs="?"
        )
        parser.add_argument(
            "--path",
            help="Where to create the devcontainer folder and files.",
            type=IsEmptyOrNewDir(must_be_empty=False),
            default=str(TEMPLATES.get_target_default_dir(TEMPLATES.BASE_DOCKERFILE)), 
            nargs="?"
        )
        parser.add_argument(
            "--extend-with",
            help="path to a .json file to extend the Dockerfile.",
            type=IsExistingFile(),
            default=str(TEMPLATES.get_template_path(TEMPLATES.DOCKERFILE_EXTENSIONS_JSON)), 
            nargs="?"
        )
        parser.add_argument(
            "--override",
            help="Override the existing Dockerfile if it exists.",
            action="store_true",
            default=False
        )
        

    def main(self, *, args):
        options = DockerfileOptions(
            image=args.image,
            path=args.path,
            extend_with=args.extend_with,
            override=args.override
        )

        loader = TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR)
        dockerfile_creator = DockerfileCreationService(template_machine=TemplateMachine(), loader=loader)
        try:
            dockerfile_creator.create_dockerfile(options=options, template_file=TEMPLATES.BASE_DOCKERFILE, dockerfile_handler=DockerfileHandler)

        except DockerfileTemplateNotFoundError as e:
            console.print(Panel.fit(
                Text(str(e), style="bold red"),
                title="[red]Template Not Found[/red]",
                border_style="red"
            ))
            return 1

        except DockerfileExistsError as e:
            console.print(Panel.fit(
                Text(str(e), style="bold yellow"),
                title="[yellow]File Already Exists[/yellow]",
                border_style="yellow"
            ))
            return 1

        except DockerfileTemplateRenderError as e:
            console.print(Panel.fit(
                Text(str(e), style="bold red"),
                title="[red]Template Render Error[/red]",
                border_style="red"
            ))
            return 1