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


from devc_cli_plugin_system.command import add_subparsers_on_demand
from devc_cli_plugin_system.command import CommandExtension
from devc_cli_plugin_system.plugin import Plugin
from devc_cli_plugin_system.interactive_creation.interactive_creation import user_selected_extension
from devc_cli_plugin_system.constants import PLUGIN_SYSTEM_CONSTANTS
from devc_cli_plugin_system.interactive_creation.interaction_provider import InteractionProvider

PLUGIN_ID = PLUGIN_SYSTEM_CONSTANTS.PLUGIN_IDENTIFIER
DEV_JSON_PLUGINS = "devc_commands.dev_json.plugins"


class DevJsonCommand(CommandExtension):
    """Create a .devcontainer file e.g. for an isolated development environment."""

    @override
    def register_plugin(
        self, parser: argparse.ArgumentParser, cli_name: str, *, argv: list[str] | None = None
    ) -> argparse._SubParsersAction:
        self._subparser = parser
        # get plugins and let them add their arguments
        return add_subparsers_on_demand(
            parser, cli_name, PLUGIN_ID, DEV_JSON_PLUGINS, required=True, argv=argv
        )

    @override
    def interactive_creation_hook(
        self,
        parser: argparse.ArgumentParser,
        subparser: argparse._SubParsersAction | None,
        cli_name: str,
        interaction_provider: InteractionProvider,
    ) -> list[str]:
        """Interactive create content that should be parsed. Default print help()."""
        _, argv = user_selected_extension(
            parser,
            subparser,
            DEV_JSON_PLUGINS,
            cli_name=cli_name,
            interaction_provider=interaction_provider,
        )
        return argv

    @override
    def main(self, *, parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
        if not hasattr(args, PLUGIN_ID):
            # in case no plugin was passed
            self._subparser.print_help()
            return 0

        plugin: Plugin = getattr(args, "_plugin")
        context = self.create_plugin_context(parser=parser, args=args, plugin=plugin)
        # call the plugin's main method
        return plugin.main(context)
