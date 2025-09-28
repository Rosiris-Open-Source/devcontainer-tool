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


from devc_cli_plugin_system.command import add_subparsers_on_demand
from devc_cli_plugin_system.command import CommandExtension


class ImageCommand(CommandExtension):
    """Entry point to create docker image for a development environment."""

    def add_arguments(self, parser, cli_name):
        self._subparser = parser
        # get plugins and let them add their arguments
        add_subparsers_on_demand(parser, cli_name, "_plugin", "devc_commands.image.plugins", required=False)

    def main(self, *, parser, args):
        if not hasattr(args, "_plugin"):
            # in case no plugin was passed
            self._subparser.print_help()
            return 0

        extension = getattr(args, "_plugin")

        # call the plugin's main method
        return extension.main(args=args)