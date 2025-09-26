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

from ros2_devcontainer_cli.verb import VerbExtension

class RebuildVerb(VerbExtension):
    """Rebuild the development container."""

    def add_arguments(self, parser, cli_name):
        arg = parser.add_argument(
            "positional_arg",
            help="Some positional argument for demonstration purposes.",
            nargs="?",
        )

    def main(self, *, args):
        print("Rebuilding the development container...")
        return 0