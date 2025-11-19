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
