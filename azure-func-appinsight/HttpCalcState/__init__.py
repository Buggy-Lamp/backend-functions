import logging

import azure.functions as func

from .. import constants
from ..HttpGetExceptions.handler_exception import *
from ..HttpGetAvailability.handler_availability import *

TRH_COUNT_EXCEPTION = 'count_exception'
TRH_AVAILABILITY_FAILED = 'availability_failed'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    treshold = []
    jexception = get_exception(req, 10)
    javailability = get_availability(req, 10, True)

    count_ex = jexception[constants.RESP_COUNT_KEY]
    count_avail = javailability[constants.RESP_COUNT_KEY]

    if count_ex > 5:
        treshold.append(TRH_COUNT_EXCEPTION)

    if count_avail > 5:
        treshold.append(TRH_AVAILABILITY_FAILED)

    logging.info(f'Count exception >5? {TRH_COUNT_EXCEPTION in treshold}')
    logging.info(f'Count availability >5? {TRH_AVAILABILITY_FAILED in treshold}')

    color = 'green'

    if len(treshold) >= 1:
        color = 'orange'

    if len(treshold) >= 2:
        color = 'red'

    return func.HttpResponse(json.dumps({
        'color': color,
        'treshold': treshold
    }))