from abc import ABC, abstractmethod
from typing import Dict

class MergeDictsStrategy(ABC):
    @abstractmethod
    def merge_dicts(self, base: Dict, new: Dict) -> Dict:
        pass

class AppendListMerge(MergeDictsStrategy):

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
    