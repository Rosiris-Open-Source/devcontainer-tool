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
"""Plugin to create a Godot devcontainer.json."""

from typing import Any
import argparse

from devc_plugins.plugins.dev_json_plugin_base import DevJsonPluginBase


class GodotDevJsonPlugin(DevJsonPluginBase):
    """Create a basic Godot devcontainer.json."""

    def _get_direct_json_patch(self, cliargs: argparse.Namespace) -> dict[str, Any]:
        """Add plugins used with Godot development to the extensions."""
        updates = {
            "customizations": {
                "vscode": {
                    "extensions": [
                        "alfish.godot-files",
                        "christian-kohler.npm-intellisense",
                        "christian-kohler.path-intellisense",
                        "eamodio.gitlens",
                        "geequlim.godot-tools",
                        "github.vscode-pull-request-github",
                        "ms-vscode.cpptools-extension-pack",
                        "ms-vscode.cpptools-themes",
                        "streetsidesoftware.code-spell-checker",
                        "xaver.clang-format",
                    ]
                }
            }
        }
        return updates
