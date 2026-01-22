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
from packaging.version import Version
from typing import Any
import argparse

from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonPluginExtension,
)
from devc.utils.docker_utils import get_docker_version
from devc.utils.argparse_helpers import get_or_create_group
from devc.constants.plugin_constants import PLUGIN_EXTENSION_ARGUMENT_GROUPS
from devc.core.exceptions.devc_exceptions import EnvironmentValidationError


class NvidiaExtension(DevJsonPluginExtension):

    name: str = "nvidia"
    nvidia_capability = "nvidia_capability"
    nvidia_capability_default = "all"

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:
        nvidia_flag = self._nvidia_flag_from_arg(cliargs)
        if nvidia_flag:
            capability = self._capability_flag_from_arg(cliargs)
            return {"runArgs": [nvidia_flag] + capability}

        return {}

    def validate_environment(self, cliargs: argparse.Namespace) -> None:
        nvidia_mode = cliargs.get(NvidiaExtension.get_name(), None)
        capabilities = cliargs.get(NvidiaExtension.get_name(self.nvidia_capability), None)

        if capabilities and not nvidia_mode:
            raise EnvironmentValidationError(
                "The nvidia capabilities need a runtime selected"
                + f"with the {NvidiaExtension.as_arg_name()} flag"
            )

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        graphics_group = get_or_create_group(parser, PLUGIN_EXTENSION_ARGUMENT_GROUPS.GRAPHICS)
        graphics_group.add_argument(
            NvidiaExtension.as_arg_name(),
            choices=["auto", "runtime", "gpus"],
            nargs="?",
            const="auto",
            default=defaults.get(NvidiaExtension.get_name(), None),
            help="Enable nvidia. Default behavior is to pick flag based"
            + " on docker version. Might need the privileged flag.",
        )
        graphics_group.add_argument(
            NvidiaExtension.as_arg_name(self.nvidia_capability),
            choices=["all", "compute", "utility", "graphics", "video", "display"],
            nargs="?",
            const=self.nvidia_capability_default,
            default=defaults.get(NvidiaExtension.get_name(self.nvidia_capability), None),
            help="Capabilities for nvidia. Might need the privileged flag.",
        )

    def _nvidia_flag_from_arg(self, cliargs: argparse.Namespace) -> str | None:
        nvidia_mode = cliargs.get(NvidiaExtension.get_name(), None)

        if not nvidia_mode:
            return None

        if nvidia_mode == "runtime":
            return "--runtime=nvidia"
        elif nvidia_mode == "gpus":
            return "--gpus=all"
        return self._auto_detect_flag()

    def _auto_detect_flag(self) -> str:
        try:
            version = get_docker_version()
            if version >= Version("19.03"):
                return "--gpus=all"
            else:
                return "--runtime=nvidia"
        except Exception:
            return "--gpus=all"

    def _capability_flag_from_arg(self, cliargs: argparse.Namespace) -> list[str]:
        capability = cliargs.get(NvidiaExtension.get_name(self.nvidia_capability), None)

        if not capability:
            capability = self.nvidia_capability_default
        return ["-e", f"NVIDIA_DRIVER_CAPABILITIES={capability}"]
