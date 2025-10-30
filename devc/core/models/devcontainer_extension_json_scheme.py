# Copyright 2025 Manuel Muth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
from dataclasses import dataclass, asdict
from typing import Dict, Any
from typing_extensions import override

from devc.utils.file_handler_interface import FileHandler


@dataclass
class DevJsonPredefinedExtensions:
    name: str = ""
    build_docker_container: bool = True
    dockerfile: str = ""
    image: str = ""
    remote_auto_forward_ports: bool = False
    remote_restore_forwarded_ports: bool = False
    enable_x11: bool = True
    network_mode: str = "host"


@dataclass
class DevJsonConfig:
    pre_defined_extensions: DevJsonPredefinedExtensions


class DevJsonHandler(FileHandler[DevJsonConfig]):

    @override
    def parse_file(self, file) -> DevJsonConfig:
        data: Dict[str, Any] = json.load(file)
        predefs = data.get("pre-defined-extensions", {})

        return DevJsonConfig(
            pre_defined_extensions=DevJsonPredefinedExtensions(
                name=predefs.get("name", ""),
                build_docker_container=predefs.get("build_docker_container", True),
                dockerfile=predefs.get("dockerfile", ""),
                image=predefs.get("image", ""),
                remote_auto_forward_ports=predefs.get("remote_auto_forward_ports", False),
                remote_restore_forwarded_ports=predefs.get("remote_restore_forwarded_ports", False),
                enable_x11=predefs.get("enable_x11", True),
                network_mode=predefs.get("network_mode", "host"),
            )
        )

    @override
    def to_dict(self) -> dict:
        return asdict(self.content)
