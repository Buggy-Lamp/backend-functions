import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import family
from .. import constants

import json
client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_LAMPCONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    req_body        = family.generateid(req.get_json())
    macadress       = req_body.get('mac')
    
    if macadress:
        result = container.create_item(body=req_body)
       
        result['url'] = '/'.join(req.url.split("/")[:-1]) + '/HttpGetLampData?lampid=' + result['id']
        

        print(dir(req))

    else:
        result = f"Not every condition is provided"
    if result:
        return func.HttpResponse(f"{result}")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
