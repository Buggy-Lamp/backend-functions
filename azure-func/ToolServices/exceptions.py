class InvalidProjectId(Exception):
    """Raised when the project_id is invalid"""
    pass


class ProjectNotFound(Exception):
    """"Raised when a project is not found"""
    pass


class ToolUnavailable(Exception):
    """"Raised when a Tool is unavailable at the time"""
    pass
