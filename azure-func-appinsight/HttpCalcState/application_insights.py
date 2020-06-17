from .util import find_threshold, parse_error
from .. import constants
from ..HttpGetAvailability.handler_availability import get_availability
from ..HttpGetExceptions.handler_exception import get_exception


def single_instance(instance_setting, show_all=False) -> dict or None:
    exception_settings = list(filter(lambda x: x['propertyname'] == 'exceptions',
                                     instance_setting['properties']))
    availability_settings = list(filter(lambda x: x['propertyname'] == 'availability',
                                        instance_setting['properties']))

    instance_data = {}

    if len(exception_settings) > 0:
        exception_settings = exception_settings[0]
    else:
        exception_settings = None

    if len(availability_settings) > 0:
        availability_settings = availability_settings[0]
    else:
        availability_settings = None

    if exception_settings:
        exception_data = get_exception(
            instance_setting['api_name'], instance_setting['api_key'],
            show_all, 10
        )

        if 'error' not in exception_data:
            exception_len = exception_data[constants.RESP_COUNT_KEY]
            threshold_target = find_threshold(exception_settings['thresholds'], exception_len)
            threshold_target['foundValue'] = exception_len

            instance_data['exceptions'] = threshold_target
        else:
            instance_data['external_error'] = parse_error(exception_data)

    if availability_settings:
        availability_data = get_availability(
            instance_setting['api_name'], instance_setting['api_key'],
            show_all, 10, True
        )

        if 'error' not in availability_data:
            availability_len = availability_data[constants.RESP_COUNT_KEY]
            threshold_target = find_threshold(availability_settings['thresholds'], availability_len)
            threshold_target['foundValue'] = availability_len

            instance_data['availability'] = threshold_target
        else:
            instance_data['external_error'] = parse_error(availability_data)

    return instance_data


def process_application_insights(settings, show_all=False) -> dict or None:
    if len(settings) == 0:
        return None

    settings = settings[0]

    return_data = {}
    for instance in settings['instances']:
        return_data[instance['instance_name']] = single_instance(instance, show_all)

    return return_data
