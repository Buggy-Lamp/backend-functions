import json
import logging

import azure.functions as func

from .. import constants
from .. import functions

container = functions.get_container(constants.DB_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    req_body = req.get_json()
    # try:
    result = functions.update(container, req_body)
    # result = container.create_item(body=req_body)
    # except:
    #     result = f"The id is already in use or database error "
    logging.info(result)
    return func.HttpResponse(json.dumps(result), mimetype=constants.HTTP_JSON_MIMETYPE)
