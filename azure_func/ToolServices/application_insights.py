from .util import find_threshold, find_color, parse_error
from .exceptions import ToolUnavailable
from .. import constants
from .ApplicationInsights import get_availability
from .ApplicationInsights import get_exception


def single_instance(instance_setting, show_all=False) -> dict or None:
    exception_settings = list(filter(lambda x: x['property_name'] == 'exceptions',
                                     instance_setting['properties']))
    availability_settings = list(filter(lambda x: x['property_name'] == 'availability',
                                        instance_setting['properties']))
    instance_data = {
        'color': 'gray',
        'color_weight': -1,
        'properties': {}
    }

    if len(exception_settings) > 0:
        exception_settings = exception_settings[0]
    else:
        exception_settings = None

    if len(availability_settings) > 0:
        availability_settings = availability_settings[0]
    else:
        availability_settings = None

    if exception_settings:
        _process_exceptions(
            instance_setting=instance_setting,
            instance_data=instance_data,
            exception_settings=exception_settings,
            show_all=show_all
        )

    if availability_settings:
        _process_availability(
            instance_setting=instance_setting,
            instance_data=instance_data,
            availability_settings=availability_settings,
            show_all=show_all
        )

    if len(instance_data['properties']) == 0:
        del instance_data['properties']

    if 'properties' in instance_data:
        color, color_weight = find_color(instance_data['properties'])
        instance_data['color'] = color
        instance_data['color_weight'] = color_weight

    return instance_data


def _process_exceptions(instance_setting: dict, instance_data: dict, exception_settings: dict, show_all=False):
    try:
        exception_data = get_exception(
            instance_setting['api_name'], instance_setting['api_key'],
            show_all, 10
        )
    except ToolUnavailable:
        instance_data['external_error'] = 'Tool is unavailable at the moment'
        return

    if 'error' not in exception_data:
        exception_len = exception_data[constants.RESP_COUNT_KEY]
        threshold_target = find_threshold(exception_settings['thresholds'], exception_len)
        threshold_target['found_value'] = exception_len

        instance_data['properties']['exceptions'] = threshold_target
    else:
        instance_data['error'] = parse_error(exception_data)


def _process_availability(instance_setting: dict, instance_data: dict, availability_settings: dict, show_all=False):
    try:
        availability_data = get_exception(
            instance_setting['api_name'], instance_setting['api_key'],
            show_all, 10
        )
    except ToolUnavailable:
        instance_data['error'] = 'Tool is unavailable at the moment'
        return

    if 'error' not in availability_data:
        availability_len = availability_data[constants.RESP_COUNT_KEY]
        threshold_target = find_threshold(availability_settings['thresholds'], availability_len)
        threshold_target['found_value'] = availability_len

        instance_data['properties']['availability'] = threshold_target
    else:
        instance_data['external_error'] = parse_error(availability_data)


def process_application_insights(settings, show_all=False) -> dict or None:
    if len(settings) == 0:
        return None

    settings = settings[0]

    return_data = {}
    for instance in settings['instances']:
        return_data[instance['instance_name']] = single_instance(instance, show_all)

    color, color_weight = find_color(return_data)
    return_data['color'] = color
    return_data['color_weight'] = color_weight

    return return_data
