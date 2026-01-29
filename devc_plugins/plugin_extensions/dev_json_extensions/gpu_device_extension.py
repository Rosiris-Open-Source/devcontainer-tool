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
from typing import Any, override
import argparse

from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonPluginExtension,
)
from devc.utils.argparse_helpers import get_or_create_group
from devc.constants.plugin_constants import PLUGIN_EXTENSION_ARGUMENT_GROUPS
from devc_cli_plugin_system.interactive_creation.interaction_provider import InteractionProvider


class GpuDeviceExtension(DevJsonPluginExtension):
    name = "gpu-dri"

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:

        if cliargs.get(GpuDeviceExtension.get_name(), False):
            return {"runArgs": ["--device=/dev/dri", "--group-add", "video"]}

        return {}

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        graphics_group = get_or_create_group(parser, PLUGIN_EXTENSION_ARGUMENT_GROUPS.GRAPHICS)
        graphics_group.add_argument(
            GpuDeviceExtension.as_arg_name(),
            action="store_true",
            help="Enable direct GPU device access for X11/Wayland",
        )

    @override
    def interactive_creation_hook(
        self,
        parser: argparse.ArgumentParser,
        subparser: argparse._SubParsersAction,
        cli_name: str,
        interaction_provider: InteractionProvider,
    ) -> list[str]:
        return [GpuDeviceExtension.as_arg_name()]
