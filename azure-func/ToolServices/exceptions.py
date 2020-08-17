import traceback

class InvalidProjectId(Exception):
    """Raised when the project_id is invalid"""
    message = "Couldn't find any project with the specified id."
    tb = traceback.format_exc()


class ProjectNotFound(Exception):
    """"Raised when a project is not found"""
    message = "Couldn't find the specified project."
    tb = traceback.format_exc()


class ToolUnavailable(Exception):
    """"Raised when a Tool is unavailable at the time"""
    message = "Couldn't reach the tool service."
    tb = traceback.format_exc()


class InvalidCredentials(Exception):
    """"Raised when invalid credentials is provided"""
    message = "Invalid Credentials please try again."
    tb = traceback.format_exc()
