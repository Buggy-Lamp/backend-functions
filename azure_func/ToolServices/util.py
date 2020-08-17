from uuid import UUID, uuid4
from typing import Iterable


def find_threshold(thresholds: dict, target: int, multiplier=1) -> dict:
    # Sort thresholds
    thresholds = sorted(thresholds, key=lambda k: k['min'])

    target_threshold = thresholds[0]

    weight = 0
    for threshold in thresholds:
        if threshold['min'] > target:
            break

        target_threshold = threshold
        target_threshold['color_weight'] = weight
        weight += 1 * multiplier

    return target_threshold


def find_color(properties: dict) -> tuple:
    color = 'gray'
    color_weight = -1

    for property_key in properties:
        prop = properties[property_key]

        if not isinstance(prop, Iterable):
            continue

        if 'color' not in prop or 'color_weight' not in prop:
            continue

        if int(prop['color_weight']) > color_weight:
            color = prop['color']
            color_weight = int(prop['color_weight'])

    return color, color_weight


def parse_error(data: dict) -> dict:
    if 'error' in data and 'code' in data['error'] and data['error']['code'] == 'PathNotFoundError':
        data['description'] = 'The provided api_name can\'t be found in application insights.'
        return data

    return data


def generate_uuid() -> UUID:
    return uuid4()
