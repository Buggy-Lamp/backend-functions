import json

from .handler_quality_gate import get_quality_gate as internal_get_quality_gate


def get_quality_gate(api_username: str, api_password: str, project_key: str) -> json:
    return internal_get_quality_gate(api_username=api_username, api_password=api_password, project_key=project_key)
