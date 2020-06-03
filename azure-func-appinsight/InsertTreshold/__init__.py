import logging

import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey
from .. import family


endpoint = "https://hu-todss.documents.azure.com:443/"
key = 'K80J9F3LT7suCP8gXtj7wgYqcoFtZsejj2zLv56hyys8PmhAU9YMaSTf2P5s6jCanzfKJ0nG4s1LOINbKbXrng=='
database_id = 'test'
container_id = 'test'
client = CosmosClient(endpoint, key)

database = client.get_database_client(database_id)
container = database.get_container_client(container_id)
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body        = req.get_json()
    tresholdAmount  = req_body.get('tresholdAmount')
    tresholdName    = req_body.get('tresholdName')
    tool            = req_body.get('tool')
    instantiename   = req_body.get('instantiename')
    
    result = container.create_item(body=req_body)
    logging.info(result);
    if tresholdAmount:
        return func.HttpResponse(f"{result}")
    else:
        return func.HttpResponse(
             "Please pass a name on the query string or in the request body",
             status_code=400
        )
