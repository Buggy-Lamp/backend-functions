import logging

from .handler_availability import *

AVAILABILITY_URL = f'{constants.BASE_URL}/events/availabilityResults'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rjson = get_availability(req.params.get('all') == 'true', 10)

    return func.HttpResponse(json.dumps(rjson))
