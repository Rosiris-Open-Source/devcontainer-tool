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


import jinja2

from pathlib import Path
from dataclasses import asdict

from devc_cli_plugin_system.plugin import Plugin
from devc.constants.templates import TEMPLATES
from devc.template_loader import TemplateLoader
from devc.template_machine import TemplateMachine
from devc.utils.path_utils import IsEmptyOrNewDir, IsExistingFile
from devc.utils.devcontainer_extension_json_scheme import DevcontainerHandler

class BaseDevJsonPlugin(Plugin):
    def __init__(self) -> None:
        self.template_file = TEMPLATES.DEVCONTAINER_JSON
    """Create the a basic devcontainer json."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "--name",
            help="A name for the dev container displayed in the UI.",
            default="", 
            nargs="?"
        )
        img_build_group = parser.add_mutually_exclusive_group(required=False)
        img_build_group.add_argument(
            "--image",
            help="Image to use if not use a Dockerfile to build a image.",
            default="", 
            nargs="?"
        )
        img_build_group.add_argument(
            "--dockerfile",
            help="Patch to Dockerfile if no existing image is used.",
            default="../.docker/Dockerfile", 
            nargs="?"
        )
        parser.add_argument(
            "--path",
            help="Where to create the devcontainer folder and files.",
            type=IsEmptyOrNewDir(must_be_empty=False),
            default=str(TEMPLATES.get_target_default_dir(self.template_file)), 
            nargs="?"
        )
        parser.add_argument(
            "--extend-with",
            help="path to a .json file to extend the .devcontainer.json.",
            type=IsExistingFile(),
            default=str(TEMPLATES.get_template_path(TEMPLATES.DEVCONTAINER_EXTENSIONS_JSON)), 
            nargs="?"
        )
        parser.add_argument(
            "--override",
            help="Override the existing Dockerfile if it exists.",
            action="store_true",
            default=False
        )
        

    def main(self, *, args):
        template_machine = TemplateMachine()
        loader = TemplateLoader(template_dir=TEMPLATES.TEMPLATE_DIR)

        try:
            template = loader.load_template(self.template_file)
        except FileNotFoundError:
            print(f"Could not find the '{TEMPLATES.get_target_filename(self.template_file)}' template in the template directory '{TEMPLATES.TEMPLATE_DIR}'.")
            return 1

        path : Path = args.path / TEMPLATES.get_target_filename(self.template_file)
        if not args.override and path.exists():
                print(f"The target file '{path}' already exists. Use --override to overwrite it.")
                return 1

        devcontainer_json = DevcontainerHandler(args.extend_with)

        # Override image and tag if provided via CLI
        if args.name:
            devcontainer_json.content.pre_defined_extensions.name = args.name
        if args.image:
            devcontainer_json.content.pre_defined_extensions.image = args.image
        if args.dockerfile:
            devcontainer_json.content.pre_defined_extensions.dockerfile = args.dockerfile

        try:
            predefs = dict(asdict(devcontainer_json.content.pre_defined_extensions))
            template_machine.render_to_target(template=template, target_path=path, context=predefs)
        except jinja2.UndefinedError as e:
            print(f"Not all of the required values to render the '{TEMPLATES.get_target_filename(self.template_file)}' template. ({e.message})")
        return 0