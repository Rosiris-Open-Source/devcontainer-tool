.. _contributing_plugins_extensions:

Contributing commands, plugins and plugin-extensions
=====================================================

Overview
--------
Adding commands like the ``dev-json`` command, creating new ``dev-json`` generators (plugins), or extending existing behavior is intentionally simple.
Before contributing, it is recommended to read the :ref:`Plugin System overview <plugin_system>`
for a full explanation of how plugins and extensions are discovered and used.

This guide focuses on practical steps for contributors who want to implement
their own:

    - command like the ``dev-json`` command (e.g. ``devc my-command`` ),
    - :ref:`plugin <creating_a_plugin>` for details. to an existing command like the ``ros2`` plugin for the ``dev-json`` command (e.g. ``devc dev-json my-plugin``) :
    - :ref:`plugin-extension <creating_a_plugin_extension>` like the ``--nvidia`` flag for the ``dev-json`` command that can be reused by multiple plugins (e.g. ``devc dev-json --my-extension ros2``).


Contributions should follow the existing directory layout:

* ``devc_plugins/plugins`` for full plugins (e.g. ``ros2``)
* ``devc_plugins/plugin_extensions`` for small reusable extensions (e.g. ``--nvidia``)

.. _creating_a_plugin:

Creating a Plugin
-----------------

.. note::

   The following sections explains how to create a new plugin with the ``dev-json`` command as example

A ``dev-json`` plugin produces a ``devcontainer.json`` file using templates and
optionally activates extensions. The easiest way to start is by subclassing
``DevJsonPluginBase``. Only two methods matter in the beginning:

* ``_extend_base_arguments`` – define your plugin-specific CLI flags
* ``_get_direct_json_patch`` – return JSON patches applied to the final output

Example: A minimal plugin that inserts a custom environment variable::

    # my_package/my_plugin.py
    from typing import Any
    import argparse
    from devc_plugins.plugins.dev_json_plugin_base import DevJsonPluginBase

    class MyDevJsonPlugin(DevJsonPluginBase):
        """Example dev-json plugin adding ENV_FOO."""

        def _extend_base_arguments(self, parser: argparse.ArgumentParser, cli_name: str) -> None:
            parser.add_argument(
                "--foo",
                help="Value injected into container as ENV_FOO.",
                default="bar",
            )

        def _get_direct_json_patch(self, args: argparse.Namespace) -> dict[str, Any]:
            return {
                "containerEnv": {
                    "ENV_FOO": args.foo
                }
            }

To register the plugin, add it to ``pyproject.toml``::

    [project.entry-points."devc_commands.dev_json.plugins"]
    my-example = "my_package.my_plugin:MyDevJsonPlugin"

After installation, it appears automatically:

``devc dev-json my-example --foo hello``

This generates a ``devcontainer.json`` with ``ENV_FOO=hello``. No extra plumbing
is required. The template rendering, extension system, and filesystem handling
are all managed by the plugin base class.

.. _creating_a_plugin_extension:

Creating a Plugin Extension
----------------------------

.. note::

   The following sections explains how to create a new plugin-extension with the ``dev-json`` command as example

Extensions inject optional behavior into existing ``dev-json`` plugins. For
example, SSH handling, GPU flags, or USB passthrough are implemented as
extensions instead of full plugins. Extensions are useful when:

* a feature should work with multiple dev-json plugins,
* the change is small (a few JSON lines),
* the feature should be activated via a simple CLI flag.

Extensions subclass ``DevJsonPluginExtension``. They must implement:

* ``_get_devcontainer_updates`` – return the JSON patch contributed
* ``_register_arguments`` – define flags such as ``--my-extension``

Example: A minimal extension enabling a custom mount::

    # my_package/my_extension.py
    from typing import Any
    import argparse
    from devc_plugins.plugin_extensions.dev_json_extensions import DevJsonPluginExtension

    class MyMountExtension(DevJsonPluginExtension):
        def _register_arguments(self, parser: argparse.ArgumentParser, defaults: dict) -> None:
            parser.add_argument(
                "--my-mount",
                help="Mount ~/data into the container.",
                action="store_true",
            )

        def _get_devcontainer_updates(self, cliargs: argparse.Namespace) -> dict[str, Any]:
            if not cliargs.my_mount:
                return {}
            return {
                "mounts": [
                    "source=${env:HOME}/data,target=/workspace/data,type=bind"
                ]
            }

Register the extension in ``pyproject.toml``::

    [project.entry-points."devc_commands.dev_json.plugins.extensions"]
    my-mount = "my_package.my_extension:MyMountExtension"

Now any dev-json plugin automatically supports the new flag:

``devc dev-json base-setup --my-mount``


When to Use a Plugin vs. an Extension
-------------------------------------

*Use a plugin* when providing a new devcontainer generator
(e.g. ROS 2, language-specific setups).

*Use an extension* when adding optional flags that inject small JSON fragments
(e.g. environment variables, mounts, authentication, GPU settings).

.. toctree::
   :hidden:
