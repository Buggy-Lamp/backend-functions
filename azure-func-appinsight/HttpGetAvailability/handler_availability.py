import json

import requests

from .. import constants


def get_availability(api_name=constants.APP_INSIGHTS_NAME, api_key=constants.API_KEY,
                     show_all=False, duration=10, only_failed=False) -> json:
    availability_url = f'{constants.BASE_URL}/{api_name}/events/availabilityResults'

    headers = {
        constants.HEADER_AUTH_KEY: api_key
    }

    data = {
        constants.REQ_TOP_KEY: '5',
        constants.REQ_COUNT_KEY: 'true',
        constants.REQ_FILTER_KEY: f'timestamp gt now() sub duration\'PT{duration}M\''
    }

    if show_all:
        data[constants.REQ_TOP_KEY] = '100'

    if only_failed:
        data[constants.REQ_FILTER_KEY] += ' and availabilityResult/success eq \'0\''

    r = requests.get(availability_url, headers=headers, params=data)
    return r.json()
