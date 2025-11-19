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
from typing import Any, TypeVar, Generic, cast
import argparse

from devc_cli_plugin_system.plugin_extensions import (
    PluginExtension,
    PluginExtensionContext,
)
from devc.utils.merge_dicts import MergeDictsStrategy, AppendListMerge


T = TypeVar("T", bound="PluginExtension")


class ExtensionManager(ABC, Generic[T]):
    """
    Manages plugin extensions for a given command.
    Handles detection, execution, and aggregation of extension outputs.
    """

    def __init__(
        self,
        context: PluginExtensionContext,
        cliargs: argparse.Namespace,
        merge_updates_strategy: MergeDictsStrategy = AppendListMerge(),
    ):
        self.context = context
        self.cliargs = cliargs
        self._called: dict[str, T] = cast(dict[str, T], context.get_called_extensions(cliargs))
        self._merge_updates_strategy = merge_updates_strategy

    @property
    def called_extensions(self) -> dict[str, Any]:
        """Return all extensions that were actually invoked."""
        return self._called

    @abstractmethod
    def get_combined_updates(self) -> dict[str, Any]:
        pass

    def _merge_updates(self, base: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
        return self._merge_updates_strategy.merge_dicts(base, new)
