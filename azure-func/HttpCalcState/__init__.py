import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from ..ToolServices import calc_state, exceptions, request_util
from ..constants import DB_ENDPOINT, DB_KEY, DB_DATABASE_ID, DB_STATES_CONTAINER_ID, HTTP_JSON_MIMETYPE


client = CosmosClient(DB_ENDPOINT, DB_KEY)

database = client.get_database_client(DB_DATABASE_ID)
container = database.get_container_client(DB_STATES_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    project_id = request_util.find_parameter(req, 'project')

    try:
        state = calc_state(project_id)
    except exceptions.InvalidProjectId:
        return func.HttpResponse(
            "Project is an invalid string",
            status_code=400
        )
    except exceptions.ProjectNotFound:
        return func.HttpResponse(
            "Project not found",
            status_code=404
        )

    state['id'] = state['project']

    container.upsert_item(body=state)

    return func.HttpResponse(json.dumps(state), mimetype=HTTP_JSON_MIMETYPE)
