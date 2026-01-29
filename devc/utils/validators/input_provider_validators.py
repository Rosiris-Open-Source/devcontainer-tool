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

from typing import Any
from collections.abc import Generator
from pathlib import Path
from .core import (
    validate_not_empty,
    validate_positive_int,
)


class NotEmpty:
    def __init__(self, *, strip: bool = True) -> None:
        self.strip = strip

    def __call__(self, value: Any) -> bool | str:
        try:
            validate_not_empty(value, strip=self.strip)
            return True
        except ValueError as e:
            return str(e)


class PositiveInt:
    def __call__(self, value: str) -> bool | str:
        try:
            validate_positive_int(value)
            return True
        except ValueError as e:
            return str(e)


class ExistingPaths:
    def __init__(self, *, must_be_device: bool = False, delimiter: str = ",") -> None:
        """
        :param must_be_device: If True, checks that path is a character device (like /dev/ttyUSB0).
        :param delimiter: If passing multiple paths, set the delimiter which separates them.
        """
        self.must_be_device = must_be_device
        self.delimiter = delimiter

    def __call__(self, value: str | Path | list[str | Path]) -> bool | str:
        for p in self.to_paths(value, self.delimiter):
            if not p.exists():
                return f"Path does not exist: {p}"
            if self.must_be_device and not p.is_char_device():
                return f"Path is not a character device: {p}"
        return True

    def to_paths(
        self, value: str | Path | list[str | Path], delimiter: str
    ) -> Generator[Path, None, None]:
        if isinstance(value, (str, Path)):
            value = [value]
        for v in value:
            if isinstance(v, str) and delimiter in v:
                for p in v.split(delimiter):
                    yield Path(p)
            else:
                yield Path(v)
