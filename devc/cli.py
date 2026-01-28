# PYTHON_ARGCOMPLETE_OK

# Copyright 2016-2017 Dirk Thomas
# Copyright 2017 Open Source Robotics Foundation, Inc.
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
"""Entry point for the devc command line tool."""

import argparse
import builtins
import functools
import signal
import sys
from typing import cast

from devc_cli_plugin_system.command import add_subparsers_on_demand
from devc_cli_plugin_system.command import CommandExtension
from devc_cli_plugin_system.interactive_creation.interactive_creation import user_selected_extension
from devc.utils.console import print_error, print_signal
from devc.utils.logging import setup_logging
from devc_cli_plugin_system.constants import PLUGIN_SYSTEM_CONSTANTS, EXTENSION_GROUPS
from devc.utils.interaction_providers.questionary_interaction_provider import (
    QuestionaryInteractionProvider,
)


def main(
    *,
    script_name: str = "devc",
    argv: list[str] | None = None,
    description: str | None = None,
    extension: CommandExtension | None = None,
) -> int:
    """Entry point for the dev-json command line tool."""
    # setup the logger once globally
    logger = setup_logging()
    if description is None:
        description = (
            f"{script_name} is an extensible command-line tool "
            "for creating development containers."
        )

    # top level parser
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--use-python-default-buffering",
        action="store_true",
        default=False,
        help=(
            "Do not force line buffering in stdout and instead use the python default buffering, "
            "which might be affected by PYTHONUNBUFFERED/-u and depends on whatever stdout is "
            "interactive or not"
        ),
    )

    # add arguments for command extension(s)
    if extension:
        extension.add_arguments(parser, script_name)
    else:
        # get command entry points as needed
        subparser = add_subparsers_on_demand(
            parser,
            script_name,
            PLUGIN_SYSTEM_CONSTANTS.COMMAND_IDENTIFIER,
            EXTENSION_GROUPS.COMMAND_GROUP,
            # hide the special commands in the help
            hide_extensions=["extension_points", "extensions"],
            required=False,
            argv=argv,
        )

    # register argcomplete hook if available
    try:
        from argcomplete import autocomplete
    except ImportError as e:
        logger.debug(f"Argcomplete could not be imported. Error when importing: {e}")
        pass
    else:
        autocomplete(parser, exclude=["-h", "--help"])

    # parse the command line arguments
    args = parser.parse_args(args=argv)

    if not args.use_python_default_buffering:
        # Make the output always line buffered.
        # TextIoWrapper has a reconfigure() method, call that if available.
        # https://docs.python.org/3/library/io.html#io.TextIOWrapper.reconfigure
        stdout = sys.stdout
        reconfigure = getattr(stdout, "reconfigure", None)

        if callable(reconfigure):
            reconfigure(line_buffering=True)
        else:
            # if stdout is not a TextIoWrapper instance, or we're using python older than 3.7,
            # force line buffering by patching print
            builtins.print = functools.partial(print, flush=True)  # type: ignore[assignment]
            logger.debug("Forcing line buffering by patching built-in print function.")

    if extension is None:
        # get extension identified by the passed command (if available)
        extension = getattr(args, PLUGIN_SYSTEM_CONSTANTS.COMMAND_IDENTIFIER, None)

    try:
        # handle the case that no command was passed, interactively let the user select commands,
        # plugins, extensions and options
        if extension is None:
            user_extension, argv = user_selected_extension(
                parser,
                subparser,
                EXTENSION_GROUPS.COMMAND_GROUP,
                cli_name=script_name,
                interaction_provider=QuestionaryInteractionProvider(),
                argv=argv,
            )
            if user_extension is None:
                return 0
            args = parser.parse_args(argv)
            # TODO(Manuel) we have to clean the user_selected_extension up...
            extension = cast(CommandExtension, user_extension)

        # call the main method of the extension
        rc = extension.main(parser=parser, args=args)
    except KeyboardInterrupt:
        print_signal(title="Signal Received", message="Execution interrupted by the user.")
        rc = signal.SIGINT
    except RuntimeError as e:
        print_error(title="Runtime Error", message=str(e))
        rc = 1
    return rc


# entrypoint for the debugger
if __name__ == "__main__":
    sys.exit(main(script_name="devc"))
