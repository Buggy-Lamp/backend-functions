import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import functions
from .. import constants

import json


container = functions.getContainer(constants.DB_ToolTypes_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    result = []
    sql = 'SELECT* FROM c'
    queryresult = container.query_items(query=sql, enable_cross_partition_query=True)
    for item in queryresult:
        result.append(item)
    result = json.dumps(result)
    return func.HttpResponse(result, mimetype=constants.HTTP_JSON_MIMETYPE)
