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
from pathlib import Path
from typing import Any, Generic, Optional, TypeVar, Union


T = TypeVar("T")  # content type


class FileHandler(ABC, Generic[T]):
    def __init__(self, path: Optional[Union[str, Path]]) -> None:
        self.path = Path(path)
        self.content: Optional[T] = None
        self.load_file(self.path)

    def load_file(self, path: Path) -> None:
        if not isinstance(path, Path):
            path = Path(path)
        with path.open("r", encoding="utf-8") as f:
            self.content = self.parse_file(f)


    @abstractmethod
    def parse_file(self, file) -> Any:
        pass


    @abstractmethod
    def to_dict(self) -> dict:
        pass