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


class NvidiaExtension(DevJsonPluginExtension):

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:
        nvidia_flag = self._flag_from_arg(cliargs)
        if nvidia_flag:
            return {"runArgs": [nvidia_flag]}
        return {}

    @staticmethod
    def get_name() -> str:
        return "nvidia"

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        parser.add_argument(
            NvidiaExtension.as_arg_name(),
            choices=["auto", "runtime", "gpus"],
            nargs="?",
            const="auto",
            default=defaults.get(NvidiaExtension.get_name(), None),
            help="Enable nvidia. Default behavior is to pick flag based on docker version.",
        )

    def _flag_from_arg(self, cliargs: argparse.Namespace) -> str | None:
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
