Quickstart
==========

Installation
-------------
Make sure you have docker, python 3.11, venv, and pip installed.

.. code-block:: bash

    python3 -m venv ~/.devc-venv && source ~/.devc-venv/bin/activate &&
    pip install git+https://github.com/Rosiris-Open-Source/devcontainer-tool.git

Usage
------
You can always see available commands by running:

.. code-block:: bash

    devc -h
    or
    devc <command> -h e.g. devc dev-json -h


Create a Dockerfile:
~~~~~~~~~~~~~~~~~~~~~
Create a Dockerfile (optional):

.. code-block:: bash

    devc dockerfile <dockerfile_plugin>

**ROS2 Example:**

For example, to create a Dockerfile with Ubuntu 24.04 and ROS2 Rolling:

.. code-block:: bash

    devc dockerfile ros2-desktop-full

Create a devcontainer.json:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a devcontainer.json using a local ``Dockerfile`` located in ``.docker/Dockerfile``:

.. code-block:: bash

    devc dev-json <dev-json_plugin> --name "test_project"

If you want to use an existing image instead:

.. code-block:: bash

    devc dev-json <dev-json_plugin> --name "test_project" --image="<image_name>"

**ROS2 Example:**

For example, to create a Dockerfile with Ubuntu 24.04 and ROS2 Rolling:

.. code-block:: bash

    devc dev-json --nvidia --ssh=mount ros2-desktop-full --name "ros2_rolling_project"

.. note::

    - The folder in which the ``.devcontainer/devcontainer.json`` is in, is mounted as ``workspace`` into the container.

See :ref:`Plugin System<plugin_system>` for how to create your own dev-json plugins and extensions.

.. toctree::
   :hidden:
