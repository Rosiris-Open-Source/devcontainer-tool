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
from typing import List, Optional, Union
import argparse

class IsEmptyOrNewDir:
    def __init__(self, must_be_empty=True):
        self.must_be_empty = must_be_empty

    def __call__(self, path_str: str) -> Path:
        p = Path(path_str).expanduser().resolve()

        if not p.exists():
            return p
        elif not p.is_dir():
            raise argparse.ArgumentTypeError(f"{p} exists but is not a directory.")
        elif self.must_be_empty and any(p.iterdir()):
            raise argparse.ArgumentTypeError(f"{p} already exists and is not empty.")

        return p
    
class IsExistingFile:
        
    def __call__(self, path: Optional[Union[str, Path]]) -> Path:
        p = Path(path).expanduser().resolve()

        if not p.exists():
            raise argparse.ArgumentTypeError(f"The passed file {p} does not exist.")
        if p.is_dir():
            raise argparse.ArgumentTypeError(f"The passed path {p} is a directory, expected a file.")

        return p
    
class IsPositiveInt:
    def __call__(self, value: str) -> int:
        try:
            ivalue = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"{value!r} is not a valid integer.")
        if ivalue < 0:
            raise argparse.ArgumentTypeError("Not a positive integer.")
        return ivalue
    
class IsValidFileType:
    def __init__(self, valid_file_types: List[str]):
        self.valid_file_types = [ ending if ending.startswith(".") else f".{ending}" for ending in valid_file_types ]
        
    def __call__(self, path_str: str) -> Path:
        p = Path(path_str).expanduser().resolve()

        if not p.exists():
            raise argparse.ArgumentTypeError(f"The passed file {p} does not exist.")
        elif p.is_dir():
            raise argparse.ArgumentTypeError(f"The passed path {p} is a directory. A file is of type {', '.join(self.valid_file_types)} required.")
        elif p.suffix not in self.valid_file_types:
            raise argparse.ArgumentTypeError(f"{p} is not a file of type {', '.join(self.valid_file_types)}.")

        return p
    