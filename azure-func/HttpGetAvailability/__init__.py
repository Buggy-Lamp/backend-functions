import json
import logging

import azure.functions as func

from ..ToolServices import ApplicationInsights
from ..constants import BASE_URL, HTTP_JSON_MIMETYPE

AVAILABILITY_URL = f'{BASE_URL}/events/availabilityResults'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rjson = ApplicationInsights.get_availability(show_all=req.params.get('all') == 'true', duration=10)

    return func.HttpResponse(json.dumps(rjson), mimetype=HTTP_JSON_MIMETYPE)
