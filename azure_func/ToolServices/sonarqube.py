from .Sonarqube import get_quality_gate
from .exceptions import ToolUnavailable
from .util import find_threshold
from ..Model import Tool, Instance, Property


def single_instance(instance_setting) -> Instance:
    quality_gate_settings = list(filter(lambda x: x['property_name'] == 'qualitygate',
                                        instance_setting['properties']))

    instance = Instance(name=instance_setting['instance_name'], properties=[])

    if len(quality_gate_settings) > 0:
        quality_gate_settings = quality_gate_settings[0]
    else:
        quality_gate_settings = None

    if quality_gate_settings:
        quality_gate_prop = _process_quality_gate(
            instance_setting=instance_setting,
            quality_gate_settings=quality_gate_settings
        )
        instance.append_prop(quality_gate_prop)

    return instance


def _process_quality_gate(instance_setting: dict, quality_gate_settings: dict) -> Property:
    prop = Property(name=quality_gate_settings['property_name'])

    try:
        quality_gate_data = get_quality_gate(
            instance_setting['api_name'], instance_setting['api_key'],
            instance_setting['api_project_id']
        )
    except ToolUnavailable:
        prop.error = 'Tool is unavailable at the moment'
        return prop

    # 0 means OK; 1 means FAILED
    threshold_status = 0 if quality_gate_data['projectStatus']['status'] == 'OK' else 1

    # An multiplier of 2 is needed because the quality gate has only 2 thresholds instead of 3
    threshold_target = find_threshold(quality_gate_settings['thresholds'], threshold_status, multiplier=2)

    prop.found_value = threshold_status
    prop.min_threshold = threshold_target['min']
    prop.color = threshold_target['color']
    prop.color_weight = threshold_target['color_weight']

    return prop


def process_sonarqube(settings) -> Tool or None:
    if len(settings) == 0:
        return None

    settings = settings[0]

    instances = []
    for instance in settings['instances']:
        instances.append(single_instance(instance_setting=instance))

    return_data = Tool(name='sonarqube', instances=instances)
    return_data.process_tool_color()

    return return_data
