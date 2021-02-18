from functools import partial
import requests

class GithubGrapqhlClient():
    """
    Use GithubGraphqlClient as context manager, update headers, and reuse same
    url all the time since it's GraphQl
    """

    def __init__(self, url, authorization_token):
        self.url = url
        self.authorization_token = authorization_token
        self.session = None

    def __enter__(self) -> requests.Session():
        self.session = requests.Session()

        self.session.headers.update({
            "Authorization": f"Bearer {self.authorization_token}"
        })
        self.session.get = partial(
            self.session.get,
            url=self.url,
        )
        self.session.post = partial(
            self.session.post,
            url=self.url,
        )
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

