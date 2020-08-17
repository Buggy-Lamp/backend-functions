import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import constants
from ..ToolServices import request_util

client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
states_container = database.get_container_client(constants.DB_STATES_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    project_id = request_util.find_parameter(req, 'project')


    if not project_id:
        return func.HttpResponse(
            "Please pass a project id in the get parameter or in the request body",
            status_code=404
        )
    # Check if string contains escaping chars
    if '\'' in project_id or '"' in project_id or '\\' in project_id:
        return func.HttpResponse(
            "Project is an invalid string",
            status_code=400
        )

    states = list(states_container.query_items(query=f'SELECT * FROM c WHERE '
                                                     f'c.id = \'{project_id}\'',
                                               enable_cross_partition_query=True))

    if len(states) == 0:
        return func.HttpResponse(
            "Project not found",
            status_code=404
        )

    state = states[0]
    return func.HttpResponse(json.dumps(state), mimetype=constants.HTTP_JSON_MIMETYPE)
