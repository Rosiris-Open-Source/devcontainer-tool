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

from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonExtensionManager,
)


class PluginContext:
    def __init__(
        self,
        *,
        args: argparse.Namespace,
        parser: argparse.ArgumentParser,
        ext_manager: DevJsonExtensionManager | None = None,
    ) -> None:
        self.args = args
        self.parser = parser
        self.ext_manager = ext_manager
