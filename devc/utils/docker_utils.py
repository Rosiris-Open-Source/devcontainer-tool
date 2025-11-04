import docker
from packaging.version import Version
from devc.core.exceptions.devc_exceptions import DependencyMissing


def get_docker_client():
    """Return a Docker client connected to the local daemon."""
    try:
        client = docker.from_env().api  # Docker SDK >= 2.0
        client.ping()  # Ensure connection is valid
        return client
    except (docker.errors.DockerException, docker.errors.APIError, ConnectionError) as ex:
        raise DependencyMissing(
            "Docker Client failed to connect to docker daemon. "
            "Verify that Docker is installed, running, and that your user "
            "has permission to access it (usually by being in the 'docker' group). "
            f"\nUnderlying error:\n{ex}"
        )


def get_docker_version() -> Version:
    """
    Return the Docker server version as a packaging.version.Version instance.
    Handles versions like '17.09.0-ce'.
    """
    client = get_docker_client()
    version_raw = client.version().get("Version", "0.0.0")
    return Version(version_raw.split("-")[0])
