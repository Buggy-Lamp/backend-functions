import json

import requests

from .. import constants


def get_exception(api_name=constants.APP_INSIGHTS_NAME, api_key=constants.API_KEY,
                  show_all=False, duration=10) -> json:
    exceptions_url = f'{constants.BASE_URL}/{api_name}/events/exceptions'

    headers = {
        constants.HEADER_AUTH_KEY: api_key
    }

    # There is a bug where >= 1 top results to the whole collection
    data = {
        constants.REQ_TOP_KEY: '1',
        constants.REQ_COUNT_KEY: 'true',
        constants.REQ_FILTER_KEY: f'timestamp gt now() sub duration\'PT{duration}M\''
    }

    if show_all:
        data[constants.REQ_TOP_KEY] = '100'

    r = requests.get(exceptions_url, headers=headers, params=data)
    return r.json()
