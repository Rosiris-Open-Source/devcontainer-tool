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
from typing import Any
import argparse

from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonPluginExtension,
)


class GpuDeviceExtension(DevJsonPluginExtension):

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:

        if cliargs.get("gpu_dri", False):
            return {"runArgs": ["--device=/dev/dri", "--group-add", "video"]}

        return {}

    @staticmethod
    def get_name() -> str:
        return "GpuDevice"

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        parser.add_argument(
            "--gpu-dri",
            action="store_true",
            help="Enable direct GPU device access for X11/Wayland",
        )
