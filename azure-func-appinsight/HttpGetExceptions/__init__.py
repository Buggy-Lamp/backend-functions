import logging

from .. import constants
from .handler_exception import *

EXCEPTIONS_URL = f'{constants.BASE_URL}/events/exceptions'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rjson = get_exception(req, 10)

    return func.HttpResponse(json.dumps(rjson))
