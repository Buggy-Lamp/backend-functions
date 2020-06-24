from .util import find_color, parse_error
from .. import constants


def single_instance(instance_setting, show_all=False) -> dict or None:
    qualitygate_settings = list(filter(lambda x: x['property_name'] == 'qualitygate',
                                       instance_setting['properties']))

    return None


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
