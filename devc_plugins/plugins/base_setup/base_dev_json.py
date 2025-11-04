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
from typing_extensions import override

from devc_plugins.plugins.dev_json_plugin_base import DevJsonPluginBase
from devc.constants.templates import TEMPLATES

class DevJsonPlugin(DevJsonPluginBase):

    @override
    def _get_extend_file(self) -> Path:
        # get the default patch defined in the templates dir
        return TEMPLATES.get_template_path(TEMPLATES.DEVCONTAINER_EXTENSIONS_JSON)
