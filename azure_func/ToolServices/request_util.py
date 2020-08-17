import azure.functions as func


def find_parameter(req: func.HttpRequest, parameter_name: str, default=None):
    param = req.params.get(parameter_name)
    if not param:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            # If the supplied body is not a dict
            if not hasattr(req_body, 'get'):
                return default

            param = req_body.get(parameter_name) \
                if req_body.get(parameter_name) is not None else param

    return default if param is None else param
