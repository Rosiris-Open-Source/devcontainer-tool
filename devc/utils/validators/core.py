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

from pathlib import Path
from typing import Any


def validate_not_empty(value: Any, *, strip: bool = True) -> None:
    if value is None:
        raise ValueError("Value is empty.")

    if isinstance(value, str):
        if strip and not value.strip():
            raise ValueError("Value is empty.")
        if not strip and not value:
            raise ValueError("Value is empty.")
    elif not value:
        raise ValueError("Value is empty.")


def validate_positive_int(value: str) -> int:
    try:
        ivalue = int(value)
    except ValueError:
        raise ValueError(f"{value!r} is not a valid integer.")

    if ivalue < 0:
        raise ValueError("Not a positive integer.")

    return ivalue


def validate_empty_or_new_dir(path_str: str, *, must_be_empty: bool = True) -> Path:
    p = Path(path_str).expanduser().resolve()

    if not p.exists():
        return p
    if not p.is_dir():
        raise ValueError(f"{p} exists but is not a directory.")
    if must_be_empty and any(p.iterdir()):
        raise ValueError(f"{p} already exists and is not empty.")

    return p


def validate_existing_file(path: str | Path) -> Path:
    p = Path(path).expanduser().resolve()

    if not p.exists():
        raise ValueError(f"The passed file {p} does not exist.")
    if p.is_dir():
        raise ValueError(f"The passed path {p} is a directory, expected a file.")

    return p


def validate_file_type(path_str: str, valid_file_types: list[str]) -> Path:
    valid_suffixes = [s if s.startswith(".") else f".{s}" for s in valid_file_types]

    p = validate_existing_file(path_str)

    if p.suffix not in valid_suffixes:
        raise ValueError(f"{p} is not a file of type {', '.join(valid_suffixes)}.")

    return p
