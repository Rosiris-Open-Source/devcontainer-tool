.. _plugin_system:

Plugin System Overview
======================

The ``devc`` tool uses a modular plugin architecture. It is divided into ``commands`` , ``plugins`` and ``plugin-extensions``.

.. code-block:: bash

    devc <command> --plugin-extensions <plugin> --plugin-flag

for example:

.. code-block:: bash

    devc dev-json --nvidia=auto --ssh=mount ros2-dektop-full --name="my_ros2_project" --ros-domain-id=5


**Command**
would be ``dev-json``, which tells ``devc`` we want to create a devcontainer.json. Another example would be the ``dockerfile`` command.

**Plugin**
the plugin would be ``ros2-desktop-full``, which tells exactly what type to create. In this case a devcontainer.json specific for ROS2. This includes additional VS Code extensions and ROS2-specific configurations such as setting the `ROS_DOMAIN_ID <https://docs.ros.org/en/rolling/Concepts/Intermediate/About-Domain-ID.html>`_.

**Plugin Extensions**
are the flags ``--nvidia=auto`` and ``--ssh=mount``. These modify the behavior of the created devcontainer.json by adding NVIDIA GPU support and SSH key mounting, respectively. The special thing about them is, that they are not plugin specific and can be added to any plugin of the ``dev-json`` command not only the ``ros2-desktop-full`` plugin.

**Plugin Flags**
are the flags ``--name="my_ros2_project"`` and ``--ros-domain-id=5`` which are specific to the ``ros2-desktop-full``.

.. toctree::
   :hidden:
   :maxdepth: 2
