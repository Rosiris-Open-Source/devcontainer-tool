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
            'devc = devc_cli_plugin_system.cli:main', # Global entry point for devc (devcontainer-tool)
        ],
        'devc_commands.dev_json.plugins.extensions': [
            'nvidia = devc_plugins.plugin_extensions.dev_json_extensions.nvidia_extension:NvidiaExtension',
            'ssh = devc_plugins.plugin_extensions.dev_json_extensions.ssh_extension:SshExtension',
            'privileged = devc_plugins.plugin_extensions.dev_json_extensions.privileged_extension:PrivilegedExtension',
            'usb = devc_plugins.plugin_extensions.dev_json_extensions.usb_extension:UsbExtension',
        ],
        'devc_commands.dev_json.plugins': [
            'base-setup = devc_plugins.plugins.base_setup.base_dev_json:DevJsonPlugin',
        ],
        'devc_commands.dockerfile.plugins': [
            'base-setup = devc_plugins.plugins.base_setup.base_dockerfile:DockerfilePlugin',
            'ros2-desktop-full = devc_plugins.plugins.ros2.ros2_desktop_full:Ros2DesktopFullImagePlugin',
        ],
        'devc_cli.command': [
            'extension_points = devc_cli_plugin_system.command.extension_points:ExtensionPointsCommand',
            'extensions = devc_cli_plugin_system.command.extensions:ExtensionsCommand',
            'dev-json = devc_plugins.commands.dev_json_cmd:DevJsonCommand',
            'dockerfile = devc_plugins.commands.dockerfile_cmd:DockerfileCommand',
        ],
        'devc_cli.extension_point': [
            'devc_cli.command = devc_cli_plugin_system.command:CommandExtension',
            'devc_commands.dev_json.plugins = devc_cli_plugin_system.plugin:Plugin',
            'devc_commands.dockerfile.plugins = devc_cli_plugin_system.plugin:Plugin',
        ],
    },
)
