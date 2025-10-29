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
from devc_cli_plugin_system.plugin_extensions import PluginExtension

class DockerfilePluginExtension(PluginExtension):
    """The base class for Rocker extension points"""

    def get_root_docker_snippet(self, cliargs):
        """ Get a dockerfile snippet to be executed as ROOT in the dockerfile."""
        return ''
    
    def get_user_docker_snippet(self, cliargs):
        """ Get a dockerfile snippet to be executed after switching to the expected USER in the dockerfile."""
        return ''