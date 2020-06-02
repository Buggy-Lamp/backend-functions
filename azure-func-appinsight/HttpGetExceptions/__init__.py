import logging

import azure.functions as func
import requests
import json

from .. import constants

from azure.cosmos import exceptions, CosmosClient, PartitionKey
from .. import family

EXCEPTIONS_URL = f'{constants.BASE_URL}/events/exceptions'

endpoint = "https://localhost:8081"
key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='
database_id = 'test'
container_id = 'test'
client = CosmosClient(endpoint, key)

database = client.get_database_client(database_id)
container = database.get_container_client(container_id)

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
    test = container.query_items(query='SELECT * FROM c',enable_cross_partition_query=True)
    
    for item in test:
        logging.info(json.dumps(item, indent=True))
        logging.info("ss")
    
    return func.HttpResponse(json.dumps(rjson))
