import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import family
from .. import constants

client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body        = family.generateid(req.get_json())
    # try:
    result = container.create_item(body=req_body)
    # except:
    #     result = f"The id is already in use or database error "
    logging.info(result)
    return func.HttpResponse(json.dumps(result), mimetype=constants.HTTP_JSON_MIMETYPE)
