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
from abc import ABC, abstractmethod
from pprint import pformat
import argparse

from devc_cli_plugin_system.interactive_creation.interaction_provider import InteractionProvider


class PluginExtension(ABC):
    """The base class for plugin extension points of the plugins."""

    name: str = ""

    def precondition_environment(self, cliargs: argparse.Namespace) -> None:
        """Modify the local environment such as setup tempfiles."""
        pass

    def validate_environment(self, cliargs: argparse.Namespace) -> None:
        """
        Check that the environment is something that can be used.
        This will check that we're on the right base OS and that the
        necessary resources are available, like hardware.
        """
        pass

    def interactive_creation_hook(
        self,
        parser: argparse.ArgumentParser,
        subparser: argparse._SubParsersAction,
        cli_name: str,
        interaction_provider: InteractionProvider,
    ) -> list[str]:
        """Override to create the interactive creation hook for a plugin extension."""
        return []

    def get_registered_args(self) -> set:
        """Return argument dest names added by this plugin."""
        return getattr(self, "_registered_args", set())

    @classmethod
    def get_name(cls, name: str = "") -> str:
        if name is None or not name.strip():
            name = cls.name
        if name is None or not name:
            raise NotImplementedError("Plugins must define non empty 'name'.")
        return name.replace("-", "_")

    @classmethod
    def as_arg_name(cls, name: str = "") -> str:
        return "--%s" % cls.get_name(name).replace("_", "-")

    def register_arguments_to_parser(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        """Track which arguments were registered. This is called by the cli infrastructure."""
        # Snapshot parser state before plugin registers
        existing_dests = {a.dest for a in parser._actions}

        # Let plugin adds args
        self._register_arguments(parser=parser, defaults=defaults)

        # Determine newly added arguments
        new_dests = {a.dest for a in parser._actions} - existing_dests
        self._registered_args = new_dests

    @abstractmethod
    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        raise NotImplementedError


class PluginExtensionContext:
    """Holds and manages all available plugin extensions."""

    def __init__(self) -> None:
        # mapping: name -> {"extension": PluginExtension}
        self._available_extensions: dict[str, PluginExtension] = {}

    def add_available_plugin_extension(self, plugin_extension: PluginExtension) -> None:
        """Register a plugin extension and record its argument names."""
        name = plugin_extension.get_name()
        self._available_extensions[name] = plugin_extension

    def get_extension(self, name: str) -> PluginExtension | None:
        """Retrieve a specific extension by name."""
        return self._available_extensions.get(name)

    def list_names(self) -> list[str]:
        """Return all registered extension names."""
        return list(self._available_extensions.keys())

    def get_called_extensions(self, args: argparse.Namespace) -> dict[str, PluginExtension]:
        """Determine which extensions have been triggered by CLI args."""
        called = {}
        for name, plugin in self._available_extensions.items():
            for arg_name in plugin.get_registered_args():
                value = getattr(args, arg_name, None)
                if value is not None:
                    called[name] = plugin
                    break
        return called

    def __repr__(self) -> str:
        return f"PluginExtensionContext({pformat(self._available_extensions)})"

    def __str__(self) -> str:
        """Nicely printable format for debug/log output."""
        lines = ["Registered plugin extensions:"]
        for name, plugin in self._available_extensions.items():
            args = ", ".join(sorted(plugin.get_registered_args())) or "(no args)"
            lines.append(f"  - {name}: {plugin.__class__.__name__} [{args}]")
        return "\n".join(lines)
