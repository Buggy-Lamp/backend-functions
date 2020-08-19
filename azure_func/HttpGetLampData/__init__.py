import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient


from urllib.parse import urljoin

from .. import constants
from .. import functions

states_container = functions.get_container(constants.DB_LAMPCONTAINER_ID)


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
            "Please pass a Lamp id in the get parameter or in the request body",
            status_code=404
        )


    states = list(states_container.query_items(query=f'SELECT c.mac, c.project FROM c WHERE '
                                                     f'c.id = \'{lampid}\'',
                                               enable_cross_partition_query=True))

    if len(states) == 0:
        return func.HttpResponse(
            "Lamp not found",
            status_code=404
        )
    result = {}
    mac             = states[0]['mac']
    project         = states[0]['project']

    result['url'] = urljoin(req.url,constants.GetLampDataStatusUrl + project)
    result['mac']   = mac

    return func.HttpResponse(json.dumps(result), mimetype=constants.HTTP_JSON_MIMETYPE,status_code = 200)
