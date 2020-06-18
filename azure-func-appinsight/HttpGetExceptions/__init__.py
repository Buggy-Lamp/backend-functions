import json
import logging

import azure.functions as func

from ..ToolServices import ApplicationInsights
from ..constants import BASE_URL

EXCEPTIONS_URL = f'{BASE_URL}/events/exceptions'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rjson = ApplicationInsights.get_exception(req.params.get('all') == 'true', 10)

    return func.HttpResponse(json.dumps(rjson))
