import requests


def create_post(api, payload):
    post = requests.post(url=api, json=payload)
    return post.status_code


def create_get(api, payload):
    get = requests.get(url=api, params=payload)
    print(get.url)
    return get.status_code
