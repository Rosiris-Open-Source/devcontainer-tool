# Copyright 2016-2017 Dirk Thomas
# Copyright 2017 Open Source Robotics Foundation, Inc.
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
from abc import ABC, abstractmethod
import argparse
from typing import Any

from devc_cli_plugin_system.plugin_system import instantiate_extensions
from devc_cli_plugin_system.plugin_system import PLUGIN_SYSTEM_VERSION
from devc_cli_plugin_system.plugin_system import satisfies_version
from devc_cli_plugin_system.plugin.plugin_context import PluginContext


class Plugin(ABC):
    """
    The interface for a plugin.

    The following properties must be defined:
    * `NAME` (will be set to the entry point name)

    The following methods must be defined:
    * `main`
    """

    NAME = None
    EXTENSION_POINT_VERSION = "0.1"

    def __init__(self) -> None:
        super().__init__()
        satisfies_version(PLUGIN_SYSTEM_VERSION, "^0.1")

    @abstractmethod
    def add_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
        pass

    @abstractmethod
    def main(self, context: PluginContext) -> int:
        """Entry point for the plugin."""
        pass


def get_plugin(name: str) -> Any:
    extensions = instantiate_extensions(name)
    for name, extension in extensions.items():
        extension.NAME = name
    return extensions


def add_task_arguments(parser: argparse.ArgumentParser, task_name: str) -> None:
    plugins = get_plugin(task_name)
    for plugin_name, plugin in plugins.items():
        group = parser.add_argument_group(title=f"Arguments for '{plugin_name}' packages")
        func = getattr(plugin, "add_%s_arguments" % task_name, None)
        if func:
            func(group)
