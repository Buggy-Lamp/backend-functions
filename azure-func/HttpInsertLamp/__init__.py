import json
import re
from urllib.parse import urljoin

import azure.functions as func
from azure.cosmos import CosmosClient

from .. import functions
from .. import constants
from ..ToolServices import request_util, util

container = functions.get_container(constants.DB_LAMPCONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    uuid = util.generate_uuid()
    project = request_util.find_parameter(req, 'project')
    mac_address = request_util.find_parameter(req, 'mac')

    if project is None or mac_address is None:
        return func.HttpResponse(
            "The following parameters are required: `project` `mac`",
            status_code=400
        )

    if not re.match(r'^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$', mac_address):
        return func.HttpResponse(
            "Your `mac` value is not valid",
            status_code=400
        )

    result = container.create_item(body={'id': str(uuid), 'project': project, 'mac': mac_address})
    result['url'] = urljoin(req.url,
                            'HttpGetLampData?code=53DiyE4/SdwJTN4ZcWFhL9PK4r115XbHBCB4XR8RpWvnvuJPYuxujA=='
                            '&lampid={0}'.format(result['id']))

    return func.HttpResponse(json.dumps(result))
