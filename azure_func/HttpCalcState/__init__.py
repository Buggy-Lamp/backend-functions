import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient
from .. import functions
from ..ToolServices import calc_state, exceptions, request_util
from ..constants import DB_STATES_CONTAINER_ID, HTTP_JSON_MIMETYPE




container = functions.get_container(DB_STATES_CONTAINER_ID)


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

    serialized_state = state.serialize()

    container.upsert_item(body=serialized_state)

    return func.HttpResponse(json.dumps(serialized_state), mimetype=HTTP_JSON_MIMETYPE)
