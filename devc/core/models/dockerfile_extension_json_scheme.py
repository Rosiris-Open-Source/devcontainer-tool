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

import json
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any
from typing_extensions import override
from typing import Any

from devc.core.file_handler_interface import FileHandler
from devc.core.models.options import DockerfileOptions
from devc.utils.json_parsing import normalize_list

@dataclass
class PredefinedExtensions:
    image: str = ""
    pre_package_install: List[str] = field(default_factory=list)
    additional_apt_packages: List[str] = field(default_factory=list)
    post_package_install: List[str] = field(default_factory=list)
    additional_sudo_commands: List[str] = field(default_factory=list)
    additional_user_commands: List[str] = field(default_factory=list)


@dataclass
class Insertion:
    anchor: str
    position: str
    is_regex: bool
    lines: List[str]


@dataclass
class DockerfileExtension:
    pre_defined_extensions: PredefinedExtensions
    insertions: List[Insertion]


class DockerfileHandler(FileHandler[DockerfileExtension]):
    options: DockerfileOptions

    def override_image(self, image: str) -> None:
        self.content.pre_defined_extensions.image = image

    @override
    def parse_file(self, file) -> DockerfileExtension:
        data: Dict[str, Any] = json.load(file)
        predefs = PredefinedExtensions(
            image=data.get("image", None),
            pre_package_install=normalize_list(data.get("pre-defined-extensions", {}).get("pre_package_install", [])),
            additional_apt_packages=normalize_list(data.get("pre-defined-extensions", {}).get("additional_apt_packages", [])),
            post_package_install=normalize_list(data.get("pre-defined-extensions", {}).get("post_package_install", [])),
            additional_sudo_commands=normalize_list(data.get("pre-defined-extensions", {}).get("additional_sudo_commands", [])),
            additional_user_commands=normalize_list(data.get("pre-defined-extensions", {}).get("additional_user_commands", [])),
        )

        insertions = [
            Insertion(
                anchor=ins.get("anchor", ""),
                position=ins.get("position", ""),
                is_regex=ins.get("is_regex", False),
                lines=ins.get("lines", []),
            )
            for ins in data.get("insertions", [])
            if isinstance(ins, dict)
        ]

        return DockerfileExtension(pre_defined_extensions=predefs, insertions=insertions)


    @override
    def to_dict(self) -> dict:
        return asdict(self.content)