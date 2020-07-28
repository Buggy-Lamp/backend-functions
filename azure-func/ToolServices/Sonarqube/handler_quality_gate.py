import json

import requests

from ... import constants
from ..exceptions import ToolUnavailable


def get_quality_gate(api_username: str, api_password: str, project_key: str) -> json:
    quality_gate_url = f'{constants.SQ_BASE_URL}/api/qualitygates/project_status'

    payload = {
        constants.REQ_PROJECT_KEY: project_key
    }

    try:
        r = requests.get(quality_gate_url, params=payload, auth=(api_username, api_password),
                         timeout=constants.HTTP_TIMEOUT)
    except requests.exceptions.Timeout:
        raise ToolUnavailable

    return r.json()
