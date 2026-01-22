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
# devc/plugins/dockerfile_ros2_plugin.py

from pathlib import Path
from typing import override
import argparse
import questionary

from devc_plugins.plugins.dockerfile_plugin_base import DockerfilePluginBase
from devc.core.models.dockerfile_extension_json_scheme import DockerfileHandler
from devc.utils.substitute_placeholders import substitute_placeholders


class Ros2DesktopFullDockerfilePlugin(DockerfilePluginBase):
    """Create a ROS2 desktop-full development container setup."""

    DEFAULT_IMAGE = ""  # use default img from patch
    SUPPORTED_ROS_DISTROS = ("humble", "iron", "jazzy", "kilted", "rolling")

    @override
    def _extend_base_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        parser.add_argument(
            "--ros-distro",
            help="ROS 2 distribution (humble, iron, jazzy, rolling...)",
            choices=self.SUPPORTED_ROS_DISTROS,
            default="rolling",
            nargs="?",
        )

    @override
    def _get_extend_file(self) -> Path:
        return Path(__file__).parent / "ros2_desktop_full_image_patch.json"

    @override
    def _extend_base_interactive_creation_hook(self) -> list[str]:
        ros_distro = questionary.select(
            "ROS 2 Distribution", choices=self.SUPPORTED_ROS_DISTROS
        ).unsafe_ask()

        result: list[str] = []

        if ros_distro:
            result.extend(["--ros-distro", ros_distro])
        return result

    @override
    def _apply_overrides_to_handler_content(
        self, dockerfile_handler: DockerfileHandler, args: argparse.Namespace
    ) -> None:
        env = {"ROS_DISTRO": args.ros_distro}
        # if image is given with args, we override the image given in the patch file
        if args.image:
            dockerfile_handler.override_image(substitute_placeholders(args.image, env))

        substitute_placeholders(dockerfile_handler.content, env)
