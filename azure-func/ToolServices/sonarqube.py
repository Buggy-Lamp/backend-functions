import logging

from .util import find_color, parse_error, find_threshold
from .. import constants
from .Sonarqube import get_quality_gate


def single_instance(instance_setting) -> dict or None:
    quality_gate_settings = list(filter(lambda x: x['property_name'] == 'qualitygate',
                                        instance_setting['properties']))

    instance_data = {
        'color': 'gray',
        'color_weight': -1,
        'properties': {}
    }

    if len(quality_gate_settings) > 0:
        quality_gate_settings = quality_gate_settings[0]
    else:
        quality_gate_settings = None

    if quality_gate_settings:
        quality_gate_data = get_quality_gate(
            instance_setting['api_name'], instance_setting['api_key'],
            instance_setting['api_project_id']
        )

        # 0 = OK; 1 = FAILED
        threshold_status = 0 if quality_gate_data['projectStatus']['status'] == 'OK' else 1

        # An multiplier of 2 is needed because the quality gate has only 2 thresholds instead of 3
        threshold_target = find_threshold(quality_gate_settings['thresholds'], threshold_status, multiplier=2)

        instance_data['properties']['qualitygate'] = threshold_target

    if len(instance_data['properties']) == 0:
        del instance_data['properties']

    if 'properties' in instance_data:
        color, color_weight = find_color(instance_data['properties'])
        instance_data['color'] = color
        instance_data['color_weight'] = color_weight

    return instance_data


def process_sonarqube(settings) -> dict or None:
    if len(settings) == 0:
        return None

    settings = settings[0]

    return_data = {}
    for instance in settings['instances']:
        return_data[instance['instance_name']] = single_instance(instance)

    color, color_weight = find_color(return_data)
    return_data['color'] = color
    return_data['color_weight'] = color_weight

    return return_data
