import azure.functions as func
import requests
import json

from .. import constants

AVAILABILITY_URL = f'{constants.BASE_URL}/events/availabilityResults'


def get_availability(req: func.HttpRequest, duration, only_failed=False) -> json:
    headers = {
        constants.HEADER_AUTH_KEY: constants.API_KEY
    }

    data = {
        constants.REQ_TOP_KEY: '5',
        constants.REQ_COUNT_KEY: 'true',
        constants.REQ_FILTER_KEY: f'timestamp gt now() sub duration\'PT{duration}M\''
    }

    if req.params.get('all') == 'true':
        data[constants.REQ_TOP_KEY] = '100'

    if only_failed:
        data[constants.REQ_FILTER_KEY] += ' and availabilityResult/success eq \'0\''

    r = requests.get(AVAILABILITY_URL, headers=headers, params=data)
    return r.json()
