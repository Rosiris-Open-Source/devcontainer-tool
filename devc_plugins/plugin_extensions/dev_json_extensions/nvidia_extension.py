from devc_plugins.plugin_extensions.dev_json_extensions import DevJsonPluginExtension

class NvidiaExtension(DevJsonPluginExtension):

    def _get_devcontainer_updates(self, cliargs):
        nvidia_flag = cliargs.get(NvidiaExtension.get_name(), None)
        if nvidia_flag: 
            return {
                "runArgs": [
                    "--gpus=all"
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