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
from devc.utils.path_utils import IsEmptyOrNewDir
from devc.utils.string_formatting import can_format_with

console = Console()
class Ros2DesktopFullImagePlugin(Plugin):
    """Create the a basic ROS2 development container setup."""

    def add_arguments(self, parser, cli_name):
        img_group = parser.add_mutually_exclusive_group(required=False)
        img_group.add_argument(
            "--image",
            help=f"Image to use if not use the {DEFAULT_IMAGES.ROS2_DESKTOP_FULL}",
            default=f"{DEFAULT_IMAGES.ROS2_DESKTOP_FULL}", 
            nargs="?"
        )
        img_group.add_argument(
            "--ros-distro",
            help="ROS 2 distribution to use (Humble or newer). Image based on osrf/ros:ros_distro-desktop-full.",
            choices=["humble", "iron", "jazzy", "kilted", "rolling"], 
            default="rolling", 
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
            "--override",
            help="Override the existing Dockerfile if it exists.",
            action="store_true",
            default=False
        )

    def _create_handler_from_args(self, args) -> DockerfileHandler:

        options = DockerfileOptions(
            image="",
            path=args.path,
            extend_with=Path(__file__).parent / "ros2_desktop_full_image_patch.json",
            override=args.override
        )
        dockerfile_handler : DockerfileHandler = DockerfileHandler(options)

        # Apply overrides
        # Override image with osrf/ros:{ros_distro}-desktop-full or user given one
        if args.image and can_format_with(args.image, "ros_distro"):
            if args.ros_distro:
                dockerfile_handler.content.pre_defined_extensions.image = args.image.format(ros_distro=args.ros_distro)
            else:
                raise ValueError("The passed image should be formatted with \"ros_distro\", but no ros_distro passes as argument. Pass ros_distro with --ros-distro=<ros_distro>.")
        elif args.image:
            dockerfile_handler.content.pre_defined_extensions.image = args.image

        return dockerfile_handler

    def main(self, *, args):
        dockerfile_handler: DockerfileHandler = self._create_handler_from_args(args)

        loader = TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR)
        dockerfile_creator = DockerfileCreationService(template_machine=TemplateMachine(), loader=loader)
        try:
            dockerfile_creator.create_dockerfile(template_file=TEMPLATES.BASE_DOCKERFILE, dockerfile_handler=dockerfile_handler)

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