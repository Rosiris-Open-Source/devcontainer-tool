from abc import ABC, abstractmethod
from typing import Any, Dict

from devc_cli_plugin_system.plugin_extensions import PluginExtension, PluginExtensionContext

class MergeDictsStrategy(ABC):
    @abstractmethod
    def merge_dicts(self, base: Dict, new: Dict) -> Dict:
        pass

class RecursiveDictMerge(MergeDictsStrategy):

    def merge_dicts(self, base: Dict, new: Dict) -> Dict:
        """Simple recursive merge utility."""
        for k, v in new.items():
            if (
                k in base
                and isinstance(base[k], list)
                and isinstance(v, list)
            ):
                base[k].extend(v)
            elif (
                k in base
                and isinstance(base[k], dict)
                and isinstance(v, dict)
            ):
                base[k] = self.merge_dicts(base[k], v)
            else:
                base[k] = v
        return base

class ExtensionManager(ABC):
    """
    Manages plugin extensions for a given command.
    Handles detection, execution, and aggregation of extension outputs.
    """

    def __init__(self, context: PluginExtensionContext, args, merge_strategy : MergeDictsStrategy = RecursiveDictMerge()):
        """
        Args:
            extensions: The dict returned from `add_plugin_extensions`.
            args: Parsed argparse.Namespace.
        """
        self.context = context
        self.args = args
        self._called: Dict[str, PluginExtension] = context.get_called_extensions(args)
        self._merge_strategy = merge_strategy

    @property
    def called_extensions(self) -> Dict[str, Any]:
        """Return all extensions that were actually invoked."""
        return self._called

    @abstractmethod
    def get_combined_updates(self) -> Dict[str, Any]:
        pass

    def _merge_updates(self, base: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
        return self._merge_strategy.merge_dicts(base, new)

