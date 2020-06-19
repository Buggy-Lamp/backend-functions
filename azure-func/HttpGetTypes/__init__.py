import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import family
from .. import constants

import json


client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_ToolTypes_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    result = []
    sql = 'SELECT* FROM c'
    queryresult = container.query_items(query=sql, enable_cross_partition_query=True)
    for item in queryresult:
        result.append(item)
    result = json.dumps(result)
    return func.HttpResponse(f"{result}")
    