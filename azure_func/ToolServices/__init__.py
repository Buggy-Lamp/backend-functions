from azure.cosmos import CosmosClient

from . import application_insights, sonarqube, util
from .exceptions import *
from ..Model import Project
from ..constants import DB_ENDPOINT, DB_KEY, DB_DATABASE_ID, DB_CONTAINER_ID

client = CosmosClient(DB_ENDPOINT, DB_KEY)

database = client.get_database_client(DB_DATABASE_ID)
container = database.get_container_client(DB_CONTAINER_ID)


def calc_state(project_id: str) -> Project:
    if not project_id:
        raise InvalidProjectId

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

    sonarqube_settings = list(filter(lambda x: x['tool_name'] == 'sonarqube', project_settings['tools']))
    sonarqube_data = sonarqube.process_sonarqube(sonarqube_settings)

    project = Project(name=project_settings['project'], tools=[appinsights_data, sonarqube_data])
    project.process_project_color()

    return project
