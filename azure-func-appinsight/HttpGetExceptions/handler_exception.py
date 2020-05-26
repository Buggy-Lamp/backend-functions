import azure.functions as func
import requests
import json

from .. import constants

EXCEPTIONS_URL = f'{constants.BASE_URL}/events/exceptions'


def get_exception(req: func.HttpRequest, duration) -> json:
    headers = {
        constants.HEADER_AUTH_KEY: constants.API_KEY
    }

    # There is a bug where >= 1 top results to the whole collection
    data = {
        constants.REQ_TOP_KEY: '1',
        constants.REQ_COUNT_KEY: 'true',
        constants.REQ_FILTER_KEY: f'timestamp gt now() sub duration\'PT{duration}M\''
    }

    if req.params.get('all') == 'true':
        data[constants.REQ_TOP_KEY] = '100'

    r = requests.get(EXCEPTIONS_URL, headers=headers, params=data)
    return r.json()
