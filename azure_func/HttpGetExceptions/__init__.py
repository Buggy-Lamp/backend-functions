import json
import logging

import azure.functions as func

from ..ToolServices import ApplicationInsights, exceptions, request_util
from ..constants import BASE_URL, HTTP_JSON_MIMETYPE

EXCEPTIONS_URL = f'{BASE_URL}/events/exceptions'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    api_name = request_util.find_parameter(req, 'api_name')
    api_key = request_util.find_parameter(req, 'api_key')

    if api_name is None or api_key is None:
        return func.HttpResponse(
            "The following parameters are required: `api_name` `api_key`",
            status_code=400
        )

    try:
        rjson = ApplicationInsights.get_exception(
            api_name=api_name,
            api_key=api_key,
            show_all=req.params.get('all') == 'true',
            duration=10
        )
    except exceptions.InvalidCredentials:
        return func.HttpResponse(
            "Invalid credentials; The `api_name` or `api_key` is invalid",
            status_code=403
        )

    return func.HttpResponse(json.dumps(rjson), mimetype=HTTP_JSON_MIMETYPE)
