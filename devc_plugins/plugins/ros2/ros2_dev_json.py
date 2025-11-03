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

from devc_cli_plugin_system.plugin import Plugin
from devc.constants.templates import TEMPLATES
from devc.template_loader import TemplateLoader

class Ros2DevJsonPlugin(Plugin):
    """Create the a basic ROS2 devcontainer json."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "--ros-distro",
            help="ROS 2 distribution to use (Humble or newer).",
            choices=["humble", "iron", "jazzy", "kilted", "rolling"], 
            default="rolling", 
            nargs="?"
        )
        parser.add_argument(
            "--path",
            help="Where to create the devcontainer folder and files.",
            default=".", 
            nargs="?"
        )
        parser.add_argument(
            "--user",
            help="Name of the default user in the container.",
            default="${localEnv:USER}", 
            nargs="?"
        )

    def main(self, *, args):#
        loader = TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR)
        template = loader.load_template(TEMPLATES.BASE_DOCKERFILE)
        return 0