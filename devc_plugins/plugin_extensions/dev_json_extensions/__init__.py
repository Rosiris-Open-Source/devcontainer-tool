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

"""
Extensions for the dev-json command.

This module defines:

- `DevJsonPluginExtension`: base class for plugins that provide extensions for the dev-json command.
- `DevJsonExtensionManager`: orchestrates plugin extensions, merges their updates, and allows
  additional updates to be applied programmatically.

It is intended to extend the dev-json command with common extensions which should then be applied
to the devcontainer.json file. Examples are mounting of devices, graphics access and the like.
"""
from abc import abstractmethod
from typing import Any, override
import argparse


from devc_cli_plugin_system.plugin_extensions.extension_manager import (
    ExtensionManager,
)
from devc_cli_plugin_system.plugin_extensions import (
    PluginExtension,
    PluginExtensionContext,
)
from devc.utils.merge_dicts import MergeDictsStrategy, AppendListMerge


class DevJsonPluginExtension(PluginExtension):
    """
    The base class for extension points.

    This class should be subclassed by all plugins providing updates
    for the devcontainer.json file.
    """

    @abstractmethod
    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:
        """
        Override to return the updates to the devcontainer.json provided by your extension.

        Args
        ----
        cliargs: CLI arguments passed to the plugin.

        Return
        ------
        dict: Updates to apply to devcontainer.json.

        Notes
        -----
        Must be overridden by a dev-json plugin extension.

        """
        raise NotImplementedError

    def get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict:
        """
        Return the updates the extension applies to the devcontainer.json.

        Checks preconditions and validates the environment before returning the updates.

        Args:
        ----
        cliargs: CLI arguments passed to the plugin.

        """
        self.precondition_environment(cliargs)
        self.validate_environment(cliargs)
        return self._get_devcontainer_updates(cliargs)


class DevJsonExtensionManager(ExtensionManager["DevJsonPluginExtension"]):
    """Manages plugin extensions for a the dev-json plugin."""

    def __init__(
        self,
        context: PluginExtensionContext,
        cliargs: argparse.Namespace,
        merge_updates_strategy: MergeDictsStrategy = AppendListMerge(),
    ):
        """
        Initialize the DevJsonExtensionManager.

        Args:
            context (PluginExtensionContext): Holds and manages all available plugin extensions.
            args: Parsed CLI arguments; used to determine which extensions are called.
            merge_updates_strategy (MergeDictsStrategy, optional): Strategy to merge multiple
                update dictionaries returned by extensions. Defaults to AppendListMerge(),
                which appends lists and merges dictionaries.

        Attributes
        ----------
        _additional_updates (list[dict[str, Any]]): Additional updates that can be appended
          programmatically outside of plugin extensions.

        """
        super().__init__(context, cliargs, merge_updates_strategy)
        self._additional_updates: list[dict[str, Any]] = []

    @override
    def get_combined_updates(self) -> dict[str, Any]:
        """Merge updates from all called extensions."""
        merged: dict = {}
        for _, ext in self.called_extensions.items():
            updates = ext.get_devcontainer_updates(vars(self.cliargs))
            merged = self._merge_updates(merged, updates)
        for update in self._additional_updates:
            merged = self._merge_updates(merged, update)
        return merged

    @override
    def add_update(self, update: dict[str, Any]) -> None:
        """Add patches which will be merged with the plugin extension updates."""
        self._additional_updates.append(update)
