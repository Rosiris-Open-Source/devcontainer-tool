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

package_name = "ros2_devcontainer_cli"

setup(
    name=package_name,
    version="0.0.0",
    packages=find_packages(exclude=["test"]),
    data_files=[],
    install_requires=["packaging"],
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
        'ros2_devcontainer_cli.command': [
            'extension_points = ros2_devcontainer_cli.command.extension_points:ExtensionPointsCommand',
            'extensions = ros2_devcontainer_cli.command.extensions:ExtensionsCommand',
            'container = ros2_devcontainer_commands.container.container_cmd:ContainerCommand',
        ],
        'ros2_devcontainer_cli.extension_point': [
            'ros2_devcontainer_cli.command = ros2_devcontainer_cli.command:CommandExtension',
            'ros2_devcontainer_commands.container.verbs = ros2_devcontainer_cli.verb:VerbExtension',
        ],
        'ros2_devcontainer_commands.container.verbs': [
            'rebuild = ros2_devcontainer_commands.container.verbs.rebuild:RebuildVerb',
        ],
        'console_scripts': [
            'ros2-devc = ros2_devcontainer_cli.cli:main',
        ],
    },
)
