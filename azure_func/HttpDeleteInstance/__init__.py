import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from .. import constants
from ..ToolServices import request_util

client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
states_container = database.get_container_client(constants.DB_LAMPCONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    project = request_util.find_parameter(req, 'project')
    lamp_id = request_util.find_parameter(req, 'lampid')

    if not project:
        return func.HttpResponse(
            "Please pass project on the query string or in the request body",
            status_code=400
        )

    if not lamp_id:
        return func.HttpResponse(
            "Please pass lamp_id on the query string or in the request body",
            status_code=400
        )
    # trying to delete it in the database
    try:
        states_container.delete_item(lamp_id, project)
        return func.HttpResponse(
            "Instance is correctly removed",
            status_code=400
        )
    except CosmosResourceNotFoundError:
        return func.HttpResponse(
            "This instance is not found",
            status_code=404
        )



