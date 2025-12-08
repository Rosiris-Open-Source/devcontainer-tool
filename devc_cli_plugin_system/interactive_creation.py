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
import inspect
import questionary
from typing import reveal_type

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore[no-redef]

from devc_cli_plugin_system.entry_points import get_entry_points
from devc_cli_plugin_system.plugin_system import instantiate_extension
from devc_cli_plugin_system.command import CommandExtension


def extension_as_choices(
    entry_points: dict[str, importlib_metadata.EntryPoint],
) -> list[questionary.Choice]:
    result = []
    for name, ep in entry_points.items():
        plugin_cls = ep.load()
        doc = plugin_cls.__doc__ or ""
        description = doc.strip().splitlines()[0] if doc else ""
        result.append(
            questionary.Choice(
                title=f"{name:<12} {description}",
                value=name,
            )
        )
    return result


def user_selected_extension(
    command_parser: argparse.ArgumentParser,
    extension_group: str,
    cli_name: str,
    argv: list[str] | None = None,
) -> CommandExtension:
    """Interactive create content that should be parsed. Default print help()."""
    entry_points = get_entry_points(extension_group)
    extension_name = questionary.select(
        "Available:", choices=extension_as_choices(entry_points)
    ).ask()

    entry_point = entry_points.get(extension_name)
    if entry_point is None:
        raise ValueError(f"Unknown extension name: {extension_name}")

    reveal_type(entry_point)

    extension: CommandExtension = instantiate_extension(
        extension_group, extension_name=entry_point.name, extension_class=entry_point.load()
    )
    # add the arguments for the requested extension
    if hasattr(extension, "add_arguments"):
        signature = inspect.signature(extension.add_arguments)
        kwargs = {}
        if "argv" in signature.parameters:
            kwargs["argv"] = argv
        extension.add_arguments(command_parser, f"{cli_name} {extension_name}", **kwargs)

    if hasattr(extension, "register_plugin_extensions"):
        extension.register_plugin_extensions(command_parser)

    return extension
