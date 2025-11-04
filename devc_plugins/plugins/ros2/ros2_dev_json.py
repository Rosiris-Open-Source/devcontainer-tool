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
from typing_extensions import override
from typing import Any, Dict

from devc.utils.argparse_validators import IsPositiveInt
from devc_plugins.plugins.dev_json_plugin_base import DevJsonPluginBase

class Ros2DevJsonPlugin(DevJsonPluginBase):
    """Create a basic ROS2 devcontainer json."""

    @override
    def _add_custom_arguments(self, parser, cli_name):
        parser.add_argument(
            "--ros-distro",
            help="ROS 2 distribution (humble, iron, jazzy, rolling...)",
            choices=["humble", "iron", "jazzy", "kilted", "rolling"],
            default="rolling", nargs="?"
        )
        parser.add_argument(
            "--ros-domain-id",
            help="ROS_DOMAIN_ID used in the container.",
            type=IsPositiveInt(),
            default=0,
            nargs="?"
        )
        parser.add_argument(
            "--ros-automatic-discovery-range",
            help="ROS_AUTOMATIC_DISCOVERY_RANGE used in the container.",
            choices=["SUBNET", "LOCALHOST", "OFF", "SYSTEM_DEFAULT"],
            default="SUBNET",
            nargs="?"
        )

    def _get_direct_json_patch(self, args) -> Dict[str, Any]:
        updates = {
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
                                "xaver.clang-format"
                            ]
                        }
                    }
                }
        if args.ros_distro in ["iron", "jazzy", "kilted", "rolling"]:
            updates["containerEnv"] = {
                                        "ROS_AUTOMATIC_DISCOVERY_RANGE": args.ros_automatic_discovery_range,
                                        "ROS_DOMAIN_ID": f"{args.ros_domain_id}"
            }
        else:
            updates["containerEnv"] = {
                                        "ROS_LOCALHOST_ONLY": self._map_localhost_only(args.ros_automatic_discovery_range),
                                        "ROS_DOMAIN_ID": f"{args.ros_domain_id}"
                                     }
        return updates
        
            
    def _map_localhost_only(self, automatic_discovery_range: str) -> str:
        if automatic_discovery_range == "LOCALHOST":
            return "1"
        return "0"