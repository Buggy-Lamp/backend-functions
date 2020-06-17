def find_threshold(thresholds: dict, target: int) -> dict:
    # Sort thresholds
    thresholds = sorted(thresholds, key=lambda k: k['min'])

    target_threshold = thresholds[0]

    weight = 0
    for threshold in thresholds:
        if threshold['min'] > target:
            break

        target_threshold = threshold
        target_threshold['weight'] = weight
        weight += 1

    return target_threshold


def parse_error(data: dict) -> dict:
    if 'error' in data:
        if 'code' in data['error']:
            if data['error']['code'] == 'PathNotFoundError':
                data['description'] = 'The provided api_name can\'t be found in application insights.'
                return data

    return data
