class StatusCodeNotValid(Exception):
    pass


class ResponseContainsErrors(Exception):
    pass


def validate_response(response):
    if response.status_code != 200:
        raise StatusCodeNotValid(response.status_code)
    elif response.json().get("errors"):
        raise ResponseContainsErrors(response.json())
