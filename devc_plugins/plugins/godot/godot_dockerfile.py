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
from argparse import ArgumentError
from pathlib import Path
from typing import override
import argparse

from devc_plugins.plugins.dockerfile_plugin_base import DockerfilePluginBase
from devc.core.models.dockerfile_extension_json_scheme import DockerfileHandler
from devc.utils.substitute_placeholders import substitute_placeholders


class GodotDockerfilePlugin(DockerfilePluginBase):
    """Create a Dockerfile with the game engine Godot installed."""

    @override
    def _add_custom_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        parser.add_argument(
            "--godot-version",
            help="Version of the Godot engine",
            choices=["4.51-stable"],
            default="4.5.1-stable",
            nargs="?",
        )
        parser.add_argument(
            "--godot-runtime",
            help="Version of the Godot engine",
            choices=["standard", "mono"],
            default="standard",
            nargs="?",
        )

    @override
    def _get_extend_file(self) -> Path:
        return Path(__file__).parent / "godot_image_patch.json"

    @override
    def _apply_overrides_to_handler_content(
        self, dockerfile_handler: DockerfileHandler, args: argparse.Namespace
    ) -> None:
        super()._apply_overrides_to_handler_content(dockerfile_handler, args)
        if not args.godot_version:
            raise ArgumentError(argument=None, message="--godot-version: Version must beset.")

        godot_runtime = ""
        if args.godot_runtime == "mono":
            godot_runtime = "_mono"
            env = {
                "GODOT_VERSION": args.godot_version,
                "GODOT_URL": f"https://github.com/godotengine/godot/releases/download/{args.godot_version}/Godot_v{args.godot_version}{godot_runtime}_linux_x86_64.zip",  # noqa: E501
                "GODOT": f"Godot_v{args.godot_version}{godot_runtime}_linux_x86_64/Godot_v{args.godot_version}{godot_runtime}_linux.x86_64",  # noqa: E501
                "GODOT_ZIP": f"Godot_v{args.godot_version}{godot_runtime}_linux_x86_64.zip",
            }
        else:
            env = {
                "GODOT_VERSION": args.godot_version,
                "GODOT_URL": f"https://github.com/godotengine/godot/releases/download/{args.godot_version}/Godot_v{args.godot_version}{godot_runtime}_linux.x86_64.zip",  # noqa: E501
                "GODOT": f"Godot_v{args.godot_version}{godot_runtime}_linux.x86_64",
                "GODOT_ZIP": f"Godot_v{args.godot_version}{godot_runtime}_linux.x86_64.zip",
            }
        substitute_placeholders(dockerfile_handler.content, env)
