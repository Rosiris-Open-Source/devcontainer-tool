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

from devc_plugins.plugins.dockerfile_plugin_base import DockerfilePluginBase
from devc.constants.defaults import DEFAULT_IMAGES
from devc.core.models.dockerfile_extension_json_scheme import DockerfileHandler
from devc.utils.string_formatting import can_format_with

class Ros2DesktopFullImagePlugin(DockerfilePluginBase):
    """Create a ROS2 desktop-full development container setup."""

    DEFAULT_IMAGE = DEFAULT_IMAGES.ROS2_DESKTOP_FULL

    def _add_custom_arguments(self, parser, cli_name):
        parser.add_argument(
            "--ros-distro",
            help="ROS 2 distribution (humble, iron, jazzy, rolling...)",
            choices=["humble", "iron", "jazzy", "kilted", "rolling"],
            default="rolling", nargs="?"
        )

    def _get_extend_file(self) -> Path:
        return Path(__file__).parent / "ros2_desktop_full_image_patch.json"

    def _apply_args_to_handler(self, dockerfile_handler: DockerfileHandler, args):
        if args.image and can_format_with(args.image, "ros_distro"):
            dockerfile_handler.override_image(args.image.format(ros_distro=args.ros_distro))
        elif args.image:
            dockerfile_handler.override_image(args.image)
