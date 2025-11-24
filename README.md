Information on how to install, use and contribute is described in the [documentation](https://rosiris-open-source.github.io/devcontainer-tool/) 📖.


[Contributions](https://rosiris-open-source.github.io/devcontainer-tool/content/contributing/contributing.html) are warmly welcome if you want to help improve this project, please read the [contributions guide](https://rosiris-open-source.github.io/devcontainer-tool/content/contributing/contributing.html).


# Devcontainer-tool
The devcontainer-tool is a extensible commandline tool (`devc`) to **create Dockerfiles** and  **devcontainer.json** files. It enables you to create isolated, reproducible and sharable development environments based on [Development Containers](https://containers.dev/).

## Installation

#### With pip in a venv:
```bash
python3 -m venv ~/.devc-venv && source ~/.devc-venv/bin/activate &&
pip install git+https://github.com/Rosiris-Open-Source/devcontainer-tool.git
```

## ROS2 example
*You need to have the `ms-vscode-remote.remote-containers` extension for [Visual Studio Code](https://code.visualstudio.com/) installed*

Creating an isolated development environment is as easy as:

```bash
mkdir my_ros2_ws && cd my_ros2_ws
```
Then create a Dockerfile:
```bash
devc dockerfile ros2-desktop-full
```
Create the devcontainer for your workspace
```bash
devc dev-json --nvidia --ssh=mount ros2-desktop-full --name "ros2_rolling_project"
```
After this you can open [Visual Studio Code](https://code.visualstudio.com/) `code .` press `F1 → Dev Containers: Reopen in Container` and start coding!
> **_NOTE:_** This can take a little bit the very first time because the Docker Image needs to be pulled. You can check the progress
