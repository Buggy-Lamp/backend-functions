import logging

import azure.functions as func
import requests
import json

from .. import constants


from azure.cosmos import exceptions, CosmosClient, PartitionKey
from .. import family

# Initialize the Cosmos client
endpoint = "https://localhost:8081"
key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='

AVAILABILITY_URL = f'{constants.BASE_URL}/events/availabilityResults'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    headers = {
        constants.HEADER_AUTH_KEY: constants.API_KEY
    }

    data = {
        constants.REQ_TOP_KEY: '5',
        constants.REQ_COUNT_KEY: 'true'
    }

    if req.params.get('all') == 'true':
        data[constants.REQ_TOP_KEY] = '100'

    r = requests.get(AVAILABILITY_URL, headers=headers, params=data)
    rjson = r.json()

    return func.HttpResponse(json.dumps(rjson))
