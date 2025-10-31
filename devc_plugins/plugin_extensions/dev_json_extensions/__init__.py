
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

from devc_cli_plugin_system.plugin_extensions import PluginExtension
from devc_cli_plugin_system.plugin_extensions.extension_manager import ExtensionManager

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

    def get_combined_updates(self) -> Dict[str, Any]:
        """Merge updates from all called extensions."""
        merged = {}
        for _, ext in self.called_extensions.items():
            updates = ext.get_devcontainer_updates(vars(self.args))
            merged = self._merge_updates(merged, updates)
        return merged

