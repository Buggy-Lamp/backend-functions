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
    if not lampid:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            lampid = req_body.get('lampid')

    if not lampid:
        return func.HttpResponse(
            "Please pass project on the query string or in the request body",
            status_code=400
        )


    states = list(states_container.query_items(query=f'SELECT c.mac, c.project FROM c WHERE '
                                                     f'c.id = \'{lampid}\'',
                                               enable_cross_partition_query=True))

    if len(states) == 0:
        return func.HttpResponse(
            "Project not found",
            status_code=404
        )
    result = {}
    mac             = states[0]['mac']
    project         = states[0]['project']

    result['url'] = urljoin(req.url,'HttpGetstate?code=hwa8MDSY6Jncf1BJjVLYERuLP1tGHdMejiG4aUA7FogBacdCRuQh1A==&project=' + project)
    result['mac']   = mac

    return func.HttpResponse(json.dumps(result))
