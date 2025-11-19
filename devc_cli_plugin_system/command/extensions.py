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
import argparse
from typing import Any, override

from devc_cli_plugin_system.command import CommandExtension
from devc_cli_plugin_system.entry_points import get_all_entry_points
from devc_cli_plugin_system.entry_points import get_first_line_doc


class ExtensionsCommand(CommandExtension):
    """List extensions."""

    @override
    def add_arguments(
        self, parser: argparse.ArgumentParser, cli_name: str, *, argv: list[str] | None = None
    ) -> None:
        parser.add_argument(
            "--all",
            "-a",
            action="store_true",
            default=False,
            help="Also show extensions which failed to load or are "
            "incompatible. (prefixed with `- `)",
        )
        parser.add_argument(
            "--verbose",
            "-v",
            action="store_true",
            default=False,
            help="Show more information for each extension",
        )

    @override
    def main(self, *, parser: argparse.ArgumentParser, args: argparse.Namespace) -> int:
        all_entry_points = get_all_entry_points()
        for group_name in sorted(all_entry_points.keys()):
            print(group_name)
            group = all_entry_points[group_name]
            for entry_point_name in sorted(group.keys()):
                (dist, entry_point) = group[entry_point_name]
                self.print_entry_point(args, dist, entry_point)
        return 0

    def print_entry_point(self, args: argparse.Namespace, dist: Any, entry_point: Any) -> None:
        exception = None
        try:
            plugin = entry_point.load()
        except Exception as e:
            if not args.all:
                # skip entry points which failed to load
                return
            exception = e
            plugin = None
        else:
            try:
                plugin()
            except Exception as e:
                if not args.all:
                    # skip plugins which failed to be instantiated
                    return
                exception = e

        prefix = " " if exception is None else "-"
        print(prefix, entry_point.name + ":", get_first_line_doc(plugin))

        if args.verbose:
            print(prefix, " ", "module_name:", entry_point.module_name)
            if entry_point.attrs:
                print(prefix, " ", "attributes:", ".".join(entry_point.attrs))
            print(prefix, " ", "distribution:", repr(dist))

        if exception:
            print(prefix, " ", "reason:", str(exception))
