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

# TODO(Manuel) get rid of questionary dependency in this file
import questionary

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata  # type: ignore[no-redef]

from devc_cli_plugin_system.entry_points import get_entry_points
from devc_cli_plugin_system.plugin_system import instantiate_extension
from devc_cli_plugin_system.command import get_first_line_doc
from devc_cli_plugin_system.plugin import Plugin
from devc_cli_plugin_system.command import CommandExtension


# TODO(Manuel) get rid of questionary dependency in this file
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


# TODO(Manuel) we have to clean the user_selected_extension up...
# Split it so it is either for Command Extensions or Plugins.
# TODO(Manuel) get rid of questionary dependency in this file
def user_selected_extension(
    parser: argparse.ArgumentParser,
    subparser: argparse._SubParsersAction | None,
    extension_group: str,
    cli_name: str,
    argv: list[str] | None = None,
) -> tuple[CommandExtension | Plugin | None, list[str]]:
    """Interactive create content that should be parsed. Default print help()."""
    entry_points = get_entry_points(extension_group)
    if not entry_points:
        return (None, [])

    extension_name = questionary.select(
        "Available:", choices=extension_as_choices(entry_points)
    ).unsafe_ask()

    if extension_name is None:
        return (None, [])
    user_argv = [extension_name]

    entry_point = entry_points.get(extension_name)
    if entry_point is None:
        raise ValueError(f"Unknown extension name: {extension_name}")

    extension = instantiate_extension(
        extension_group, extension_name=entry_point.name, extension_class=entry_point.load()
    )

    if subparser is None:
        return (extension, user_argv)

    command_parser = subparser.choices[extension_name]
    command_parser.set_defaults(**{extension_group: extension})
    command_parser.description = get_first_line_doc(extension)

    # add the arguments for the requested extension
    if hasattr(extension, "add_arguments"):
        command_parser._root_parser = parser
        signature = inspect.signature(extension.add_arguments)
        kwargs = {}
        if "argv" in signature.parameters:
            kwargs["argv"] = argv
        extension.add_arguments(command_parser, f"{cli_name} {extension_name}", **kwargs)
        del command_parser._root_parser

    subsubparser = None
    if hasattr(extension, "register_plugin"):
        command_parser._root_parser = parser
        signature = inspect.signature(extension.register_plugin)
        kwargs = {}
        if "argv" in signature.parameters:
            kwargs["argv"] = argv
        subsubparser = extension.register_plugin(
            command_parser, f"{cli_name} {extension_name}", **kwargs
        )
        del command_parser._root_parser

    if hasattr(extension, "register_plugin_extensions"):
        command_parser._root_parser = parser
        extension.register_plugin_extensions(command_parser)
        del command_parser._root_parser

    user_argv = user_argv + extension.interactive_creation_hook(
        parser, subsubparser, f"{cli_name} {extension_name}"
    )
    return (extension, user_argv)
