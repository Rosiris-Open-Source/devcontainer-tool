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
from devc.utils.argparse_helpers import get_or_create_group
from devc.constants.plugin_constants import PLUGIN_EXTENSION_ARGUMENT_GROUPS


class UsbExtension(DevJsonPluginExtension):

    name = "usb"

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:
        usb_args = self._parse_cli(cliargs=cliargs)

        if not usb_args:
            return {}

        # Default base config
        run_args = []
        mounts = []

        # Enable USB support
        if usb_args.get("usb_all"):
            run_args.extend(["--device=/dev/bus/usb"])
            mounts.extend(
                [
                    "source=/dev/bus/usb,target=/dev/bus/usb,type=bind",
                    "source=/run/udev,target=/run/udev,type=bind",
                ]
            )

        # Add specific devices (if provided)
        if usb_args.get("usb_devices"):
            for dev_string in usb_args["usb_devices"]:
                # Split by comma, strip whitespace, filter out empty strings
                for dev_path in map(str.strip, dev_string.split(",")):
                    if dev_path:
                        run_args.extend(["--device", dev_path])

        # Add dialout group if requested (default True)
        if usb_args.get("usb_dialout", False):
            run_args.extend(["--group-add", "dialout"])

        # Return devcontainer.json patch
        return {
            **({"runArgs": run_args} if run_args else {}),
            **({"mounts": mounts} if mounts else {}),
        }

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        usb_parser = get_or_create_group(parser, PLUGIN_EXTENSION_ARGUMENT_GROUPS.DEVICES_USB)
        usb_parser.add_argument(
            "--usb-all",
            action="store_true",
            help="Expose all USB devices (/dev/bus/usb) to the container",
        )
        usb_parser.add_argument(
            "--usb-devices",
            nargs="+",
            metavar="PATH",
            help="Specific USB devices to pass,(e.g. --usb-devices=/dev/ttyUSB0,/dev/ttyACM0 )",
        )
        usb_parser.add_argument(
            "--usb-dialout",
            action="store_true",
            help="Do not add the 'dialout' group (use if not dealing with serial devices)",
        )

    def _parse_cli(self, cliargs: argparse.Namespace) -> dict:
        """Convert CLI flags into structured dict."""
        parsed_args = {}
        for arg in self._registered_args:
            parsed_args[arg] = cliargs.get(arg, None)
        return parsed_args
