class DevcontainerJsonError(Exception):
    """Base error for devcontainer json operations."""

class DevJsonTemplateNotFoundError(DevcontainerJsonError):
    pass

class DevJsonExistsError(DevcontainerJsonError):
    pass

class DevJsonTemplateRenderError(DevcontainerJsonError):
    pass