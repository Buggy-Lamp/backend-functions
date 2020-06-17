import json
import logging

import azure.functions as func
from azure.cosmos import CosmosClient

from .application_insights import process_application_insights
from .. import constants

# from dotenv import load_dotenv
# load_dotenv()

# client = CosmosClient(os.getenv("DB_ENDPOINT"), os.getenv("DB_KEY"))
#
# database = client.get_database_client(os.getenv("DB_DATABASE_ID"))
# container = database.get_container_client(os.getenv("DB_CONTAINER_ID"))
client = CosmosClient(constants.DB_ENDPOINT, constants.DB_KEY)

database = client.get_database_client(constants.DB_DATABASE_ID)
container = database.get_container_client(constants.DB_CONTAINER_ID)


# noinspection SqlDialectInspection,SqlNoDataSourceInspection
def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    project_id = req.params.get('project')
    if not project_id:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            project_id = req_body.get('project')

    if not project_id:
        return func.HttpResponse(
            "Please pass project on the query string or in the request body",
            status_code=400
        )

    # Check if string contains escaping chars
    if '\'' in project_id or '"' in project_id or '\\' in project_id:
        return func.HttpResponse(
            "Project is an invalid string",
            status_code=400
        )

    project_settings = list(container.query_items(query=f'SELECT * FROM c WHERE '
                                                        f'c.project = \'{project_id}\'',
                                                  enable_cross_partition_query=True))

    if len(project_settings) == 0:
        return func.HttpResponse(
            "Project not found",
            status_code=404
        )

    project_settings = project_settings[0]

    appinsights_settings = list(filter(lambda x: x['toolname'] == 'application_insights', project_settings['tools']))
    appinsights_data = process_application_insights(appinsights_settings)

    return func.HttpResponse(json.dumps({
        'project': project_settings['project'],
        'tools': {
            'application_insights': appinsights_data
        }
    }))
