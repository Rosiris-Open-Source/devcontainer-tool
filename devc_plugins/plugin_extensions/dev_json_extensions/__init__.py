
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
from abc import abstractmethod
from typing import Any, Dict

from devc_cli_plugin_system.plugin_extensions.extension_manager import ExtensionManager
from devc_cli_plugin_system.plugin_extensions import PluginExtension, PluginExtensionContext
from devc.utils.merge_dicts import MergeDictsStrategy, AppendListMerge

class DevJsonPluginExtension(PluginExtension):
    """The base class for Rocker extension points"""
    
    @abstractmethod
    def _get_devcontainer_updates(self, cliargs):
        """ Changes to be applied to the devcontainer.json file."""
        raise NotImplementedError

    def get_devcontainer_updates(self, cliargs) -> dict:
        self.precondition_environment(cliargs)
        self.validate_environment(cliargs)
        return self._get_devcontainer_updates(cliargs)


class DevJsonExtensionManager(ExtensionManager):
    """
    Manages plugin extensions for a the dev-json command
    """
    _called: Dict[str, DevJsonPluginExtension]

    def __init__(self, context: PluginExtensionContext, args, merge_updates_strategy: MergeDictsStrategy = AppendListMerge()):
        super().__init__(context, args, merge_updates_strategy)
        self._additional_updates: list[dict[str, Any]] = []

    def get_combined_updates(self) -> Dict[str, Any]:
        """Merge updates from all called extensions."""
        merged = {}
        for _, ext in self.called_extensions.items():
            updates = ext.get_devcontainer_updates(vars(self.args))
            merged = self._merge_updates(merged, updates)
        for update in self._additional_updates:
            merged = self._merge_updates(merged, update)
        return merged
    
    def add_update(self, update:  Dict[str, Any]) -> None:
        self._additional_updates.append(update)

