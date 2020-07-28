import json
import logging

import azure.functions as func

from ..ToolServices import ApplicationInsights, request_util
from ..constants import BASE_URL, HTTP_JSON_MIMETYPE, APP_INSIGHTS_NAME, API_KEY

EXCEPTIONS_URL = f'{BASE_URL}/events/exceptions'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    api_name = request_util.find_parameter(req, 'api_name', APP_INSIGHTS_NAME)
    api_key = request_util.find_parameter(req, 'api_key', API_KEY)

    rjson = ApplicationInsights.get_exception(
        api_name=api_name,
        api_key=api_key,
        show_all=req.params.get('all') == 'true',
        duration=10
    )

    return func.HttpResponse(json.dumps(rjson), mimetype=HTTP_JSON_MIMETYPE)
