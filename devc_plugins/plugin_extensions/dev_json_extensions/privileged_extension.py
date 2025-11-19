from typing import Any
import argparse

from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonPluginExtension,
)


class PrivilegedExtension(DevJsonPluginExtension):

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:
        privileged_flag = cliargs.get(PrivilegedExtension.get_name(), None)
        if privileged_flag:
            return {"runArgs": ["--privileged"]}
        return {}

    @staticmethod
    def get_name() -> str:
        return "privileged"

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        parser.add_argument(
            PrivilegedExtension.as_arg_name(),
            action="store_true",
            default=False,
            help="Make the devcontainer privileged. Disabled by default.",
        )
