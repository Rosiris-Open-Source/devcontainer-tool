devc – Reproducible Development Environments
============================================
For a quickstart guide, see :doc:`content/quickstart`.

``devc`` is a small CLI tool to create Dockerfiles and devcontainer.json.
It helps to setup reproducible and isolated development environments within seconds that can be shared across teams.


What it gives you
-----------------

* automatic Dockerfile + devcontainer generation
* clean, isolated development environments
* easy sharing — share the image and reuse the devcontainer.json


Quick Example (ROS 2)
---------------------

Using the ROS 2 plugin, ``devc`` creates the entire environment for you:

**Create a ROS 2 my_ros2_ws :**

::

    mkdir my_ros2_ws && cd my_ros2_ws

**Generated ROS 2 Dockerfile :**

::

    devc dockerfile ros2-desktop-full --ros-distro rolling

**Generated ROS 2 devcontainer.json with nvidia support and your ssh keys mounted:**

::

    devc dev-json --nvidia --ssh=mount ros2-desktop-full --ros-distro rolling --name "my_ros2_ws"

That’s all you need. After this you can open the folder in VSCode with: ``code .`` and press F1 → ``Dev Containers: Reopen in Container``.
After this you are all set up with a isolated full ROS 2 development environment.


Typical Project Layout
----------------------

::

    my_ws/
    ├── .devcontainer/
    │   └── devcontainer.json
    └── .docker/
    |    └── Dockerfile
    └── rest of your project files ...

The workspace ``my_ws`` folder is mounted inside the container. This means any code inside this folder is accessible from within the container.

CI Integration
--------------

Pipelines can prebuild the Docker image and push it to a registry.
Your ``devcontainer.json`` can reference that image directly, allowing instant
startup without rebuilding locally.

**Using of a pre-build ros2 image shared with your team:**

::

    devc dev-json base-setup --image="your_registry:your_image" --name "my_ws"


Where to go next
----------------

* :doc:`content/quickstart`
* :doc:`content/plugin_system/plugin_system`
* :doc:`content/contributing/contributing`

.. toctree::

   content/quickstart
   content/plugin_system/plugin_system
   content/contributing/contributing
