import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .handler_exception import *

EXCEPTIONS_URL = f'{constants.BASE_URL}/events/exceptions'

client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    test = container.query_items(query='SELECT * FROM c', enable_cross_partition_query=True)

    for item in test:
        logging.info(json.dumps(item, indent=True))
        logging.info("ss")

    rjson = get_exception(req.params.get('all') == 'true', 10)

    return func.HttpResponse(json.dumps(rjson))
