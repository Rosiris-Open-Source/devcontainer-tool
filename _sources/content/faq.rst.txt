FAQ
===

Argcomplete not working
-------------------------
If argcomplete (argument completion of  ``devc``) is not working when pressing the tab key, please make sure that argcomplete is installed and activated.

Check if its installed:

.. code-block:: bash

    pip list | grep argcomplete
    argcomplete                   <version> # if you see this its installed

Make sure its activated:

.. code-block:: bash

    activate-global-python-argcomplete --user
    eval "$(register-python-argcomplete devc)"

How to debug a  plugin?
------------------------
Example with vscode:
Make sure you have the python extension installed or if for whatever reason you don't want to make sure you have at least ``debugpy`` installed in your env.
Create a ``launch.json`` in you ``.vscode`` folder. Past the following content into the the ``launch.json`` file:

.. code-block:: json

  {
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Debug devc-json",
        "type": "debugpy",
        "request": "launch",
        "module": "devc_cli_plugin_system.cli",
        "args": ["dev-json", "--nvidia=auto", "base-setup", "--name", "test3", "--override"],
        "cwd": "${workspaceFolder}",
        "console": "integratedTerminal",
        "justMyCode": false
      }
    ]
  }

This would be an example on how to debug the  ``devc-json`` plugin. You can change the arguments in the ``args`` field to whatever you want to test.
You can then set breakpoints in the plugin code and start the debugger in vscode.

How to debug a the interactive creation?
-----------------------------------------
Example with vscode:
Make sure you have the python extension installed or if for whatever reason you don't want to make sure you have at least ``debugpy`` installed in your env.
Create a ``launch.json`` in you ``.vscode`` folder. Past the following content into the the ``launch.json`` file:

.. code-block:: json

  {
    "version": "0.2.0",
    "configurations": [
      {
        "name": "Debug devc qustionary",
        "type": "debugpy",
        "request": "launch",
        "module": "devc_cli_plugin_system.cli",
        "args": [],
        "cwd": "${workspaceFolder}",
        "console": "integratedTerminal",
        "justMyCode": false
      }
    ]
  }


This will launch the ``dev`` command in interactive mode. You can then set breakpoints points in the code handling the interactive creation and start the debugger in vscode.

.. toctree::
   :hidden:
