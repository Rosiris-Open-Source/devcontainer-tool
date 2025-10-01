class DockerfileError(Exception):
    """Base error for Dockerfile operations."""

class DockerfileTemplateNotFoundError(DockerfileError):
    pass

class DockerfileExistsError(DockerfileError):
    pass

class DockerfileTemplateRenderError(DockerfileError):
    pass