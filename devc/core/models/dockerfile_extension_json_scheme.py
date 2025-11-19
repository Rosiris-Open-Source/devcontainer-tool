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

from dataclasses import dataclass, field, asdict
from typing import Any, TextIO
from typing import override
import json

from devc.core.file_handler_interface import FileHandler
from devc.utils.json_parsing import filter_empty_strings


@dataclass
class PredefinedExtensions:
    image: str = ""
    pre_package_install: list[str] = field(default_factory=list)
    additional_apt_packages: list[str] = field(default_factory=list)
    post_package_install: list[str] = field(default_factory=list)
    additional_sudo_commands: list[str] = field(default_factory=list)
    additional_user_commands: list[str] = field(default_factory=list)


@dataclass
class Insertion:
    anchor: str
    position: str
    is_regex: bool
    lines: list[str]


@dataclass
class DockerfileExtension:
    pre_defined_extensions: PredefinedExtensions
    insertions: list[Insertion]


class DockerfileHandler(FileHandler[DockerfileExtension]):

    def override_image(self, image: str) -> None:
        assert self.content is not None
        self.content.pre_defined_extensions.image = image

    @override
    def parse_file(self, file: TextIO) -> DockerfileExtension:
        data: dict[str, Any] = json.load(file)
        predefs = PredefinedExtensions(
            image=data.get("pre-defined-extensions", {}).get("image", None),
            pre_package_install=filter_empty_strings(
                data.get("pre-defined-extensions", {}).get("pre_package_install", [])
            ),
            additional_apt_packages=filter_empty_strings(
                data.get("pre-defined-extensions", {}).get("additional_apt_packages", [])
            ),
            post_package_install=filter_empty_strings(
                data.get("pre-defined-extensions", {}).get("post_package_install", [])
            ),
            additional_sudo_commands=filter_empty_strings(
                data.get("pre-defined-extensions", {}).get("additional_sudo_commands", [])
            ),
            additional_user_commands=filter_empty_strings(
                data.get("pre-defined-extensions", {}).get("additional_user_commands", [])
            ),
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
        assert self.content is not None
        return asdict(self.content)
