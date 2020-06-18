import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import family
from .. import constants

client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    # identifier = {"test" : "sjdfjsadf"}
    # logging.info('Python HTTP trigger function processed a request.')
    # req_body        = family.generateid(req.get_json)
    # container.replace_item(item=identifier,body=req_body)
    return func.HttpResponse(f"{result}")
    