from devc_plugins.plugin_extensions.dev_json_extensions import DevJsonPluginExtension

class PrivilegedExtension(DevJsonPluginExtension):

    def get_devcontainer_updates(self, cliargs):
        privileged_flag = cliargs.get(PrivilegedExtension.get_name(), None)
        if privileged_flag: 
            return {
                "runArgs": [
                    "--privileged"
                ]
        }
        return {}

    @staticmethod
    def get_name() -> str:
        return "privileged"

    def register_arguments(self, parser, defaults):
            parser.add_argument(PrivilegedExtension.arg_name(),
            action="store_true",
            default=False,
            help="Make the devcontainer privileged. Disabled by default.")