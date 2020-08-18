from .ApplicationInsights import get_availability
from .ApplicationInsights import get_exception
from .exceptions import ToolUnavailable
from .util import find_threshold, parse_error
from ..constants import RESP_COUNT_KEY
from ..Model import Tool, Instance, Property


def single_instance(instance_setting, show_all=False) -> Instance:
    exception_settings = list(filter(lambda x: x['property_name'] == 'exceptions',
                                     instance_setting['properties']))
    availability_settings = list(filter(lambda x: x['property_name'] == 'availability',
                                        instance_setting['properties']))

    instance = Instance(name=instance_setting['instance_name'], properties=[])

    if len(exception_settings) > 0:
        exception_settings = exception_settings[0]
    else:
        exception_settings = None

    if len(availability_settings) > 0:
        availability_settings = availability_settings[0]
    else:
        availability_settings = None

    if exception_settings:
        exceptions_prop = _process_exceptions(
            instance_setting=instance_setting,
            exception_settings=exception_settings,
            show_all=show_all
        )
        instance.append_prop(exceptions_prop)

    if availability_settings:
        availability_prop = _process_availability(
            instance_setting=instance_setting,
            availability_settings=availability_settings,
            show_all=show_all
        )
        instance.append_prop(availability_prop)

    return instance


def _process_exceptions(instance_setting: dict, exception_settings: dict, show_all=False) \
        -> Property:
    prop = Property(name=exception_settings['property_name'])

    try:
        exception_data = get_exception(
            instance_setting['api_name'], instance_setting['api_key'],
            show_all, 10
        )
    except ToolUnavailable:
        prop.error = 'Tool is unavailable at the moment'
        return prop

    _process_prop_data(exception_data, exception_settings, prop)

    return prop


def _process_availability(instance_setting: dict, availability_settings: dict, show_all=False) \
        -> Property:
    prop = Property(name=availability_settings['property_name'])

    try:
        availability_data = get_availability(
            instance_setting['api_name'], instance_setting['api_key'],
            show_all, 10
        )
    except ToolUnavailable:
        prop.error = 'Tool is unavailable at the moment'
        return prop

    _process_prop_data(availability_data, availability_settings, prop)

    return prop


def _process_prop_data(prop_data, prop_settings, prop):
    if 'error' not in prop_data:
        exception_len = prop_data[RESP_COUNT_KEY]

        threshold_target = find_threshold(prop_settings['thresholds'], exception_len)
        prop.found_value = exception_len
        prop.min_threshold = threshold_target['min']
        prop.color = threshold_target['color']
        prop.color_weight = threshold_target['color_weight']
    else:
        prop.error = parse_error(prop_data)


def process_application_insights(settings, show_all=False) -> Tool or None:
    if len(settings) == 0:
        return None

    settings = settings[0]

    instances = []
    for instance in settings['instances']:
        instances.append(single_instance(instance_setting=instance, show_all=show_all))

    return_data = Tool(name='application_insights', instances=instances)
    return_data.process_tool_color()

    return return_data
