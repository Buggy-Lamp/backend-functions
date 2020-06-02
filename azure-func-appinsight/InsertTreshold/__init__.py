import logging

import azure.functions as func

from azure.cosmos import exceptions, CosmosClient, PartitionKey
from .. import family



endpoint = "https://localhost:8081"
key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='
database_id = 'test'
container_id = 'test'
client = CosmosClient(endpoint, key)

database = client.get_database_client(database_id)
container = database.get_container_client(container_id)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    tresholdAmount  = req.params.get('tresholdAmount')
    tresholdName    = req.params.get('tresholdName')
    if not tresholdAmount and not tresholdName:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            tresholdName    = req_body.get('tresholdName')
            tresholdAmount  = req_body.get('tresholdAmount')
    logging.info(tresholdAmount)
    logging.info(tresholdName)
    return func.HttpResponse(tresholdAmount+tresholdName)

