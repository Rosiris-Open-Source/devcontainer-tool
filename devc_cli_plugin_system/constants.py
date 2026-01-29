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

from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class PLUGIN_SYSTEM_CONSTANTS:

    PLUGIN_IDENTIFIER: ClassVar[str] = "_plugin"
    COMMAND_IDENTIFIER: ClassVar[str] = "_command"


@dataclass(frozen=True)
class EXTENSION_GROUPS:

    ROOT_GROUP: ClassVar[str] = "devc_cli"
    COMMAND_GROUP: ClassVar[str] = ROOT_GROUP + ".command"
