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
    install_requires=["jinja2", "packaging"],
    zip_safe=True,
    author="Manuel Muth",
    author_email="manuel.muth@rosiris.de",
    maintainer="Manuel Muth",
    maintainer_email="manuel.muth@rosiris.de",
    url="https://github.com/Rosiris-Open-Source/ros2-devcontainer",
    keywords=[],
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
    ],
    description="ROS2 devcontainer tool",
    long_description="""\
    Tool for creating and management of ROS2 development containers.""",
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
        ],
        'devc_commands.dev_json.plugins': [
            'ros2 = devc_plugins.plugins.ros2.ros2_dev_json:Ros2DevJsonPlugin',
        ],
        'devc_commands.image.plugins': [
            'ros2 = devc_plugins.plugins.ros2.ros2_image:Ros2ImagePlugin',
        ],
        'devc_cli.command': [
            'extension_points = devc_cli_plugin_system.command.extension_points:ExtensionPointsCommand',
            'extensions = devc_cli_plugin_system.command.extensions:ExtensionsCommand',
            'container = devc_plugins.commands.container_cmd:ContainerCommand',
            'dev_json = devc_plugins.commands.dev_json_cmd:DevJsonCommand',
            'image = devc_plugins.commands.image_cmd:ImageCommand',
        ],
        'devc_cli.extension_point': [
            'devc_cli.command = devc_cli_plugin_system.command:CommandExtension',
            'devc_commands.container.plugins = devc_cli_plugin_system.plugin:Plugin',
            'devc_commands.dev_json.plugins = devc_cli_plugin_system.plugin:Plugin',
            'devc_commands.image.plugins = devc_cli_plugin_system.plugin:Plugin',
        ],
    },
)
