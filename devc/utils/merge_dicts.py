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
