import json
import logging

import azure.functions as func

from .. import functions
from ..ToolServices import request_util
from ..constants import DB_STATES_CONTAINER_ID, \
    HTTP_JSON_MIMETYPE

states_container = functions.get_container(DB_STATES_CONTAINER_ID)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    project_id = request_util.find_parameter(req, 'project')
    instance_name = request_util.find_parameter(req, 'instance_name')

    if not project_id:
        return func.HttpResponse("Project is a required field", status_code=400)

    if '\'' in project_id or '"' in project_id or '\\' in project_id:
        return func.HttpResponse("Project is an invalid string", status_code=400)

    if instance_name:
        if '\'' in instance_name or '"' in instance_name or '\\' in instance_name:
            return func.HttpResponse("Instance name is an invalid string", status_code=400)

    settings = list(states_container.query_items(query=f"SELECT * FROM c WHERE "
                                                       f"c.project = '{project_id}'",
                                                 enable_cross_partition_query=True))

    if len(settings) == 0:
        return func.HttpResponse("Project is not found", status_code=404)

    settings = settings[0]

    state = list(states_container.query_items(query=f"SELECT * FROM c WHERE "
                                                    f"c.id = '{project_id}'",
                                              enable_cross_partition_query=True))
    if len(state) > 0:
        state = state[0]
        attach_state(settings=settings, state=state)

    if instance_name:
        settings = filter_instance_name(settings, instance_name)

    return func.HttpResponse(json.dumps(settings), mimetype=HTTP_JSON_MIMETYPE)


def filter_instance_name(settings: dict, instance_name: str):
    instance_settings = []
    for tool in settings['tools']:
        for instance in tool['instances']:
            if instance['instance_name'] == instance_name:
                instance_settings.append(instance)

    return instance_settings


def attach_state(settings: dict, state: dict):
    settings['state_color'] = state['color']

    for tool in settings['tools']:
        if tool['tool_name'] not in state['tools']:
            tool['color'] = 'gray'
            continue

        tool_state = state['tools'][tool['tool_name']]
        tool['state_color'] = tool_state['color']

        attach_instance_state(tool['instances'], tool_state)


def attach_instance_state(instances: dict, tool_state: dict):
    for instance in instances:
        if instance['instance_name'] not in tool_state:
            continue

        instance_state = tool_state[instance['instance_name']]
        instance['state_color'] = instance_state['color']

        for prop in instance['properties']:
            if 'properties' not in instance_state:
                continue
            if prop['property_name'] not in instance_state['properties']:
                continue

            prop_state = instance_state['properties'][prop['property_name']]
            prop['state_color'] = prop_state['color']
