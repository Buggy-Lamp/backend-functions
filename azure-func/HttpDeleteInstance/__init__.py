import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from urllib.parse import urljoin

from .. import constants

client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
states_container = database.get_container_client(constants.DB_LAMPCONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    lampid = req.params.get('lampid')
    project = req.params.get('project')
    if not lampid:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            lampid = req_body.get('lampid')
    if not lampid:
        return func.HttpResponse(
            "Please pass lampid on the query string or in the request body",
            status_code=400
        )

    if not project:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            lampid = req_body.get('project')

    if not project:
        return func.HttpResponse(
            "Please pass project on the query string or in the request body",
            status_code=400
        )

    states_container.delete_item(lampid, project)

    return func.HttpResponse()
