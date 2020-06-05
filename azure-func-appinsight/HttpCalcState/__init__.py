import logging
import os

import azure.functions as func
from azure.cosmos import CosmosClient
from dotenv import load_dotenv

from ..HttpGetExceptions.handler_exception import *
from ..HttpGetAvailability.handler_availability import *

from .. import constants

TRH_COUNT_EXCEPTION = 'count_exception'
TRH_AVAILABILITY_FAILED = 'availability_failed'

load_dotenv()

# client = CosmosClient(os.getenv("DB_ENDPOINT"), os.getenv("DB_KEY"))
#
# database = client.get_database_client(os.getenv("DB_DATABASE_ID"))
# container = database.get_container_client(os.getenv("DB_CONTAINER_ID"))
client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    threshold = {}
    jexception = get_exception(req, 10)
    javailability = get_availability(req, 10, True)

    docs_ex = list(container.query_items(query='SELECT * FROM c WHERE c.tool = \'applicationinsights\' '
                                               'AND c.instantiename = \'exception\'',
                                         enable_cross_partition_query=True))
    docs_avail = list(container.query_items(query='SELECT * FROM c WHERE c.tool = \'applicationinsights\' '
                                                  'AND c.instantiename = \'availability\'',
                                            enable_cross_partition_query=True))

    for doc in (docs_ex, docs_avail):
        logging.info(json.dumps(doc, indent=True))

    count_ex = jexception[constants.RESP_COUNT_KEY]
    count_avail = javailability[constants.RESP_COUNT_KEY]
    count_max_ex = -1
    count_max_avail = -1

    if len(docs_ex) > 0:
        count_max_ex = docs_ex[0]['tresholdAmount']
    if len(docs_avail) > 0:
        count_max_avail = docs_avail[0]['tresholdAmount']

    wanted_keys = ['tresholdAmount', 'tresholdName', 'tool', 'instantiename']

    if count_ex > count_max_ex >= 0:
        # Needs to be removed if not in DB; keeping for tests
        threshold[TRH_COUNT_EXCEPTION] = 'testing'

        # Filter unwanted keys
        if len(docs_ex) > 0:
            threshold[TRH_COUNT_EXCEPTION] = dict((k, docs_ex[0][k]) for k in wanted_keys if k in docs_ex[0])

    if count_avail > count_max_avail >= 0:
        # Needs to be removed if not in DB; keeping for tests
        threshold[TRH_AVAILABILITY_FAILED] = 'testing'

        # Filter unwanted keys
        if len(docs_avail) > 0:
            threshold[TRH_COUNT_EXCEPTION] = dict((k, count_avail[0][k]) for k in wanted_keys if k in count_avail[0])

    logging.info(f'Count exception >{count_max_ex}? {TRH_COUNT_EXCEPTION in threshold}')
    logging.info(f'Count availability >{count_max_avail}? {TRH_AVAILABILITY_FAILED in threshold}')

    color = 'green'

    if len(threshold) >= 1:
        color = 'orange'

    if len(threshold) >= 2:
        color = 'red'

    return func.HttpResponse(json.dumps({
        'color': color,
        'thresholds': threshold
    }))
