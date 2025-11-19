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


class SshExtension(DevJsonPluginExtension):

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:
        ssh_flag = cliargs.get(SshExtension.get_name(), None)

        if ssh_flag == "forward":
            return {
                "runArgs": [
                    "-e",
                    "SSH_AUTH_SOCK=${env:SSH_AUTH_SOCK}",
                    "-v",
                    "${env:SSH_AUTH_SOCK}:${env:SSH_AUTH_SOCK}",
                ]
            }
        elif ssh_flag == "mount":
            return {
                "mounts": [
                    "source=${env:HOME}/.ssh,target=/home/${localEnv:USER}/.ssh,"
                    + "type=bind,consistency=cached"
                ]
            }
        return {}

    @staticmethod
    def get_name() -> str:
        return "ssh"

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        parser.add_argument(
            SshExtension.as_arg_name(),
            choices=["forward", "mount"],
            nargs="?",
            const="forward",
            default=defaults.get(SshExtension.get_name(), None),
            help="Enable usage of your ssh keys inside the container."
            + "Default behavior is to  provide access by forwarding the ssh agent.",
        )
