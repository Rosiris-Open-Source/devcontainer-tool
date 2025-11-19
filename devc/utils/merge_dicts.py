from abc import ABC, abstractmethod


class MergeDictsStrategy(ABC):
    @abstractmethod
    def merge_dicts(self, base: dict, new: dict) -> dict:
        pass


class AppendListMerge(MergeDictsStrategy):

    def merge_dicts(self, base: dict, new: dict) -> dict:
        """Merge dicts by appending list and replacing values."""
        for k, v in new.items():
            if k in base and isinstance(base[k], list) and isinstance(v, list):
                base[k].extend(v)
            elif k in base and isinstance(base[k], dict) and isinstance(v, dict):
                base[k] = self.merge_dicts(base[k], v)
            else:
                base[k] = v
        return base
