import logging

import azure.functions as func
import requests
import json

from .. import constants

EXCEPTIONS_URL = f'{constants.BASE_URL}/events/exceptions'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    headers = {
        constants.HEADER_AUTH_KEY: constants.API_KEY
    }

    # There is a bug where >= 1 top results to the whole collection
    data = {
        constants.REQ_TOP_KEY: '1',
        constants.REQ_COUNT_KEY: 'true',
        '$filter': 'timestamp gt now() sub duration\'PT10M\''
    }

    if req.params.get('all') == 'true':
        data[constants.REQ_TOP_KEY] = '100'

    r = requests.get(EXCEPTIONS_URL, headers=headers, params=data)
    rjson = r.json()

    return func.HttpResponse(json.dumps(rjson))
