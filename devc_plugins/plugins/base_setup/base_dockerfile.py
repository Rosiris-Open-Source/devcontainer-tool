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
from devc.models.dockerfile_extension_json_scheme import DockerfileHandler

class BaseDockerfilePlugin(Plugin):
    """Create the a basic development container setup."""

    def add_arguments(self, parser, cli_name):
        parser.add_argument(
            "--image",
            help="Image to use.",
            default="", 
            nargs="?"
        )
        parser.add_argument(
            "--image-tag",
            help="tag to use",
            default="", 
            nargs="?"
        )
        parser.add_argument(
            "--path",
            help="Where to create the devcontainer folder and files.",
            type=IsEmptyOrNewDir(must_be_empty=False),
            default=str(TEMPLATES.get_target_default_dir(TEMPLATES.BASE_DOCKERFILE)), 
            nargs="?"
        )
        parser.add_argument(
            "--extend-with",
            help="path to a .json file to extend the Dockerfile.",
            type=IsExistingFile(),
            default=str(TEMPLATES.get_template_path(TEMPLATES.DOCKERFILE_EXTENSIONS_JSON)), 
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
        template_file = TEMPLATES.BASE_DOCKERFILE

        try:
            template = loader.load_template(template_file)
        except FileNotFoundError:
            print(f"Could not find the '{TEMPLATES.get_target_filename(template_file)}' template in the template directory '{TEMPLATES.TEMPLATE_DIR}'.")
            return 1

        path : Path = args.path / TEMPLATES.get_target_filename(template_file)
        if not args.override and path.exists():
                print(f"The target file '{path}' already exists. Use --override to overwrite it.")
                return 1

        dockerfile = DockerfileHandler(args.extend_with)

        # Override image and tag if provided via CLI
        if args.image:
            dockerfile.content.pre_defined_extensions.image = args.image
        if args.image_tag:
            dockerfile.content.pre_defined_extensions.image_tag = args.image_tag
        
        try:
            predefs = dict(asdict(dockerfile.content.pre_defined_extensions))
            template_machine.render_to_target(template=template, target_path=path, context=predefs)
        except jinja2.UndefinedError as e:
            print(f"Not all of the required values to render the '{TEMPLATES.get_target_filename(template_file)}' template. ({e.message})")
        return 0