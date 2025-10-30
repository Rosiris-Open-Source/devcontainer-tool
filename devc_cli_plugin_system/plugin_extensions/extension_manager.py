from abc import ABC, abstractmethod
from typing import Any, Dict

from devc_cli_plugin_system.plugin_extensions import PluginExtension, PluginExtensionContext
from devc.utils.merge_dicts import MergeDictsStrategy, AppendListMerge

class ExtensionManager(ABC):
    """
    Manages plugin extensions for a given command.
    Handles detection, execution, and aggregation of extension outputs.
    """

    def __init__(self, context: PluginExtensionContext, args, merge_updates_strategy : MergeDictsStrategy = AppendListMerge()):
        """
        Args:
            extensions: The dict returned from `add_plugin_extensions`.
            args: Parsed argparse.Namespace.
        """
        self.context = context
        self.args = args
        self._called: Dict[str, PluginExtension] = context.get_called_extensions(args)
        self._merge_updates_strategy = merge_updates_strategy

    @property
    def called_extensions(self) -> Dict[str, Any]:
        """Return all extensions that were actually invoked."""
        return self._called

    @abstractmethod
    def get_combined_updates(self) -> Dict[str, Any]:
        pass

    def _merge_updates(self, base: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
        return self._merge_updates_strategy.merge_dicts(base, new)