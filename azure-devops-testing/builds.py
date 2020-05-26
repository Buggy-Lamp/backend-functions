from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

personal_access_token = "ptqqy6k2tjxa6ldjh5262g66sny4o3kkpjepmgc35c6v4l6ow5ma"
organization_url = "https://dev.azure.com/hu-todss-2020"
project_name = "template-SmartHotel360"

# Create a connection to the org
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

build_client = connection.clients.get_build_client()

# Definitions are pagable? Page 1 is stored in value
# https://github.com/microsoft/azure-devops-python-api/blob/6.0.0b2/azure-devops/azure/devops/released/build/build_client.py#L510
definitions = build_client.get_definitions(project_name).value

selected_def = -1

for definition in definitions:
    print(str(definition.id) + ": " + definition.name)
    selected_def = definition.id


builds = build_client.get_builds(project=project_name, definitions=[selected_def]).value
for build in builds:
    print(build)
