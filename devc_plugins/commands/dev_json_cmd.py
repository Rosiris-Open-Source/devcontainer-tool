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
import argparse
from typing import override


from devc_cli_plugin_system.command import (
    add_subparsers_on_demand,
    add_plugin_extensions,
)
from devc_cli_plugin_system.command import CommandExtension
from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonExtensionManager,
)
from devc_cli_plugin_system.plugin.plugin_context import PluginContext
from devc_cli_plugin_system.plugin import Plugin


class DevJsonCommand(CommandExtension):
    """Entry point to create dev_json for a development environment."""

    @override
    def add_arguments(
        self, parser: argparse.ArgumentParser, cli_name: str, *, argv: list[str] | None = None
    ) -> None:
        self._subparser = parser
        # get plugins and let them add their arguments
        add_subparsers_on_demand(
            parser,
            cli_name,
            "_plugin",
            "devc_commands.dev_json.plugins",
            required=False,
        )

    @override
    def register_plugin_extensions(self, parser: argparse.ArgumentParser) -> None:
        self._plugin_extensions = add_plugin_extensions(
            "devc_commands.dev_json.plugins.extensions", parser, defaults={}
        )

    @override
    def main(self, *, parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
        if not hasattr(args, "_plugin"):
            # in case no plugin was passed
            self._subparser.print_help()
            return 0

        ext_manager = DevJsonExtensionManager(self._plugin_extensions, args)

        plugin: Plugin = getattr(args, "_plugin")
        context = PluginContext(args=args, parser=parser, ext_manager=ext_manager)
        # call the plugin's main method
        return plugin.main(context)
