import requests


def send_request_get_cookies(url, headers):
    cookies = []
    response = requests.get(url, headers)
    response
    return cookies
