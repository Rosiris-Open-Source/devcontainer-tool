from typing import Any
import argparse

from devc_plugins.plugin_extensions.dev_json_extensions import (
    DevJsonPluginExtension,
)


class GpuDeviceExtension(DevJsonPluginExtension):

    def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:

        if cliargs.get("gpu_dri", False):
            return {"runArgs": ["--device=/dev/dri", "--group-add", "video"]}

        return {}

    @staticmethod
    def get_name() -> str:
        return "GpuDevice"

    def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
        parser.add_argument(
            "--gpu-dri",
            action="store_true",
            help="Enable direct GPU device access for X11/Wayland",
        )
