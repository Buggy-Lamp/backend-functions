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
    
    thresholdAmount  = req_body.get('thresholdAmount')
    thresholdName    = req_body.get('thresholdName')
    tool            = req_body.get('tool')
    instancename   = req_body.get('instancename')
    try:
        if thresholdAmount and thresholdName and tool and instancename :
            result = container.create_item(body=req_body)
        else:
            result = f"Not every condition is provided"
    except:
        result = f"The id is already in use or the database is not excepting it in a other way"
    logging.info(result)
    if tresholdAmount:
        return func.HttpResponse(f"{result}")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
