import logging

from .. import constants
from .handler_availability import *


from azure.cosmos import exceptions, CosmosClient, PartitionKey
from .. import family

# Initialize the Cosmos client
endpoint = "https://localhost:8081"
key = 'C2y6yDjf5/R+ob0N8A7Cgv30VRDJIWEHLM+4QDU5DE2nQ9nDuVTqobD4b8mGGyPMbIZnqyMsEcaGQy67XIw/Jw=='

AVAILABILITY_URL = f'{constants.BASE_URL}/events/availabilityResults'


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    rjson = get_availability(req, 10)

    return func.HttpResponse(json.dumps(rjson))
