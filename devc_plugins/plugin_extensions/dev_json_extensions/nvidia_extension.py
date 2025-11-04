from packaging.version import Version

from devc_plugins.plugin_extensions.dev_json_extensions import DevJsonPluginExtension
from devc.utils.docker_utils import get_docker_version

class NvidiaExtension(DevJsonPluginExtension):

    def _get_devcontainer_updates(self, cliargs):
        nvidia_flag = self._flag_from_arg(cliargs)
        if nvidia_flag: 
            return {
                "runArgs": [
                    nvidia_flag
                ]
        }
        return {}

    @staticmethod
    def get_name() -> str:
        return "nvidia"

    def _register_arguments(self, parser, defaults):
            parser.add_argument(NvidiaExtension.as_arg_name(),
            choices=['auto', 'runtime', 'gpus'],
            nargs='?',
            const='auto',
            default=defaults.get(NvidiaExtension.get_name(), None),
            help="Enable nvidia. Default behavior is to pick flag based on docker version.")

    def _flag_from_arg(self, cliargs):
        nvidia_mode = cliargs.get(NvidiaExtension.get_name(), None)

        if not nvidia_mode:
            return {}
        
        if nvidia_mode == "runtime":
            return "--runtime=nvidia"
        elif nvidia_mode == "gpus":
            return "--gpus=all"
        return self._auto_detect_flag()


    def _auto_detect_flag(self) -> str:
        try:
            version = get_docker_version()
            if version >= Version("19.03"):
                return "--gpus=all"
            else:
                return "--runtime=nvidia"
        except Exception:
            return "--gpus=all"