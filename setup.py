# Copyright Manuel Muth
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

from setuptools import find_packages
from setuptools import setup

package_name = "devc"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[],
    install_requires=["argcomplete", "jinja2", "packaging", "typing_extensions", "rich"],
    zip_safe=True,
    author="Manuel Muth",
    author_email="manuel.muth@rosiris.de",
    maintainer="Manuel Muth",
    maintainer_email="manuel.muth@rosiris.de",
    url="https://github.com/Rosiris-Open-Source/devcontainer-tool",
    keywords=[],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    description="Devcontainer tool",
    long_description="""\
    Tool for creating and management of devcontainer development environments.""",
    license="Apache License, Version 2.0",
    extras_require={
        "test": [
            "pytest",
        ],
    },
    entry_points={
        'console_scripts': [
            'devc = devc_cli_plugin_system.cli:main',
        ],
        'devc_commands.container.plugins': [
            'ros2 = devc_plugins.plugins.ros2.ros2_container:Ros2ContainerPlugin',
            'base-setup = devc_plugins.plugins.base_setup.base_container:BaseContainerPlugin',
        ],
        'devc_commands.dev_json.plugins': [
            'ros2 = devc_plugins.plugins.ros2.ros2_dev_json:Ros2DevJsonPlugin',
            'base-setup = devc_plugins.plugins.base_setup.base_dev_json:BaseDevJsonPlugin',
        ],
        'devc_commands.dockerfile.plugins': [
            'ros2 = devc_plugins.plugins.ros2.ros2_image:Ros2ImagePlugin',
            'base-setup = devc_plugins.plugins.base_setup.base_dockerfile:BaseDockerfilePlugin',
        ],
        'devc_cli.command': [
            'extension_points = devc_cli_plugin_system.command.extension_points:ExtensionPointsCommand',
            'extensions = devc_cli_plugin_system.command.extensions:ExtensionsCommand',
            'devcontainer = devc_plugins.commands.container_cmd:ContainerCommand',
            'dev-json = devc_plugins.commands.dev_json_cmd:DevJsonCommand',
            'dockerfile = devc_plugins.commands.dockerfile_cmd:DockerfileCommand',
        ],
        'devc_cli.extension_point': [
            'devc_cli.command = devc_cli_plugin_system.command:CommandExtension',
            'devc_commands.container.plugins = devc_cli_plugin_system.plugin:Plugin',
            'devc_commands.dev_json.plugins = devc_cli_plugin_system.plugin:Plugin',
            'devc_commands.dockerfile.plugins = devc_cli_plugin_system.plugin:Plugin',
        ],
    },
)
