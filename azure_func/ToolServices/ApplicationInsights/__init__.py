import json

from ... import constants

from .handler_availability import get_availability as internal_get_availability
from .handler_exception import get_exception as internal_get_exception


def get_availability(api_name=constants.APP_INSIGHTS_NAME, api_key=constants.API_KEY,
                     show_all=False, duration=10, only_failed=False) -> json:
    return internal_get_availability(api_name=api_name, api_key=api_key,
                                     show_all=show_all, duration=duration, only_failed=only_failed)


def get_exception(api_name=constants.APP_INSIGHTS_NAME, api_key=constants.API_KEY,
                  show_all=False, duration=10) -> json:
    return internal_get_exception(api_name=api_name, api_key=api_key,
                                  show_all=show_all, duration=duration)
