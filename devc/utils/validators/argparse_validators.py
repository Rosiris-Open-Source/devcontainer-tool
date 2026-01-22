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


import argparse
from pathlib import Path
from typing import Any

from devc.utils.validators.core import (
    validate_empty_or_new_dir,
    validate_existing_file,
    validate_file_type,
    validate_not_empty,
    validate_positive_int,
)


class EmptyOrNewDir:
    def __init__(self, must_be_empty: bool = True) -> None:
        self.must_be_empty = must_be_empty

    def __call__(self, path_str: str) -> Path:
        try:
            return validate_empty_or_new_dir(path_str, must_be_empty=self.must_be_empty)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))


class ExistingFile:
    def __call__(self, path: str | Path) -> Path:
        try:
            return validate_existing_file(path)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))


class PositiveInt:
    def __call__(self, value: str) -> int:
        try:
            return validate_positive_int(value)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))


class NotEmpty:
    def __init__(self, strip: bool = True) -> None:
        self.strip = strip

    def __call__(self, value: Any) -> Any:
        try:
            validate_not_empty(value, strip=self.strip)
            return value
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))


class ValidFileType:
    def __init__(self, valid_file_types: list[str]) -> None:
        self.valid_file_types = valid_file_types

    def __call__(self, path_str: str) -> Path:
        try:
            return validate_file_type(path_str, self.valid_file_types)
        except ValueError as e:
            raise argparse.ArgumentTypeError(str(e))
