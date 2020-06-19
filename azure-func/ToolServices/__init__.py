from azure.cosmos import CosmosClient

from . import application_insights, util
from .exceptions import *
from ..constants import DB_ENDPOINT, DB_KEY, DB_DATABASE_ID, DB_CONTAINER_ID

client = CosmosClient(DB_ENDPOINT, DB_KEY)

database = client.get_database_client(DB_DATABASE_ID)
container = database.get_container_client(DB_CONTAINER_ID)


def calc_state(project_id: str) -> dict:
    # Check if string contains escaping chars
    if '\'' in project_id or '"' in project_id or '\\' in project_id:
        raise InvalidProjectId

    project_settings = list(container.query_items(query=f"SELECT * FROM c WHERE "
                                                        f"c.project = '{project_id}'",
                                                  enable_cross_partition_query=True))

    if len(project_settings) == 0:
        raise ProjectNotFound

    project_settings = project_settings[0]

    appinsights_settings = list(filter(lambda x: x['tool_name'] == 'application_insights', project_settings['tools']))
    appinsights_data = application_insights.process_application_insights(appinsights_settings)

    color, color_weight = util.find_color(appinsights_data)
    state = {
        'project': project_settings['project'],
        'color': color,
        'color_weight': color_weight,
        'tools': {
            'application_insights': appinsights_data
        }
    }

    # return func.HttpResponse(json.dumps(state))
    # return func.HttpResponse(status_code=201)
    return state
