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
"""Plugin to create a basic ROS2 devcontainer."""
from typing import override
from typing import Any
import argparse
import questionary

from devc_plugins.plugins.dev_json_plugin_base import DevJsonPluginBase
from devc.constants.plugin_constants import PLUGIN_EXTENSION_ARGUMENT_GROUPS
from devc.utils.argparse_helpers import get_or_create_group
from devc.utils.validators import argparse_validators
from devc.utils.validators import questionary_validators


class Ros2DevJsonPlugin(DevJsonPluginBase):
    """Create a basic ROS2 devcontainer json."""

    SUPPORTED_ROS_DISTROS = ("humble", "iron", "jazzy", "kilted", "rolling")
    SUPPORTED_DISCOVERY_RANGES = ("SUBNET", "LOCALHOST", "OFF", "SYSTEM_DEFAULT")

    @override
    def _extend_base_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        ros2_group = get_or_create_group(parser, PLUGIN_EXTENSION_ARGUMENT_GROUPS.ROS2)
        ros2_group.add_argument(
            "--ros-distro",
            help="ROS 2 distribution (humble, iron, jazzy, rolling...)",
            choices=self.SUPPORTED_ROS_DISTROS,
            default="rolling",
            nargs="?",
        )
        ros2_group.add_argument(
            "--ros-domain-id",
            help="ROS_DOMAIN_ID used in the container.",
            type=argparse_validators.PositiveInt(),
            default=0,
            nargs="?",
        )
        ros2_group.add_argument(
            "--ros-automatic-discovery-range",
            help="ROS_AUTOMATIC_DISCOVERY_RANGE used in the container.",
            choices=self.SUPPORTED_DISCOVERY_RANGES,
            default="SUBNET",
            nargs="?",
        )

    @override
    def _extend_base_interactive_creation_hook(self) -> list[str]:
        ros_distro = questionary.select(
            "ROS 2 Distribution", choices=self.SUPPORTED_ROS_DISTROS
        ).unsafe_ask()

        ros_domain_id = questionary.text(
            "ROS Domain ID",
            default="0",
            validate=questionary_validators.PositiveInt(),
        ).unsafe_ask()

        ros_automatic_discovery_range = questionary.select(
            "ROS Automatic Discovery Range",
            choices=self.SUPPORTED_DISCOVERY_RANGES,
            default="SUBNET",
        ).unsafe_ask()

        result: list[str] = []

        if ros_distro:
            result.extend(["--ros-distro", ros_distro])
        if ros_domain_id:
            result.extend(["--ros-domain-id", ros_domain_id])
        if ros_automatic_discovery_range:
            result.extend(["--ros-automatic-discovery-range", ros_automatic_discovery_range])
        return result

    def _get_direct_json_patch(self, args: argparse.Namespace) -> dict[str, Any]:
        updates: dict[str, Any] = {
            "customizations": {
                "vscode": {
                    "extensions": [
                        "christian-kohler.npm-intellisense",
                        "christian-kohler.path-intellisense",
                        "eamodio.gitlens",
                        "github.vscode-pull-request-github",
                        "ms-python.debugpy",
                        "ms-python.python",
                        "ms-python.vscode-pylance",
                        "ms-python.vscode-python-envs",
                        "ms-vscode.cpptools-extension-pack",
                        "ms-vscode.cpptools-themes",
                        "ranch-hand-robotics.rde-pack",
                        "ranch-hand-robotics.rde-ros-2",
                        "ranch-hand-robotics.urdf-editor",
                        "redhat.vscode-yaml",
                        "streetsidesoftware.code-spell-checker",
                        "vadimcn.vscode-lldb",
                        "visualstudioexptteam.intellicode-api-usage-examples",
                        "visualstudioexptteam.vscodeintellicode",
                        "xaver.clang-format",
                    ]
                }
            }
        }
        if args.ros_distro in ["iron", "jazzy", "kilted", "rolling"]:
            updates["containerEnv"] = {
                "ROS_AUTOMATIC_DISCOVERY_RANGE": args.ros_automatic_discovery_range,
                "ROS_DOMAIN_ID": f"{args.ros_domain_id}",
            }
        else:
            updates["containerEnv"] = {
                "ROS_LOCALHOST_ONLY": self._map_localhost_only(args.ros_automatic_discovery_range),
                "ROS_DOMAIN_ID": f"{args.ros_domain_id}",
            }
        return updates

    def _map_localhost_only(self, automatic_discovery_range: str) -> str:
        if automatic_discovery_range == "LOCALHOST":
            return "1"
        return "0"
