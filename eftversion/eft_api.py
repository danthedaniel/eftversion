"""EFT Web API Wrapper."""

import json
import requests
import zlib
from urllib.parse import urlencode


class ApiResponse:
    """EFT Web API Response."""

    def __init__(self, response):
        """Initialize an ApiResponse.

        Arguments
        ---------
        response : dict
            The raw decoded JSON.
        """
        self.data = response['data']
        self.errmsg = response['errmsg']
        self.err = response['err']

    def ok(self):
        """Whether the API function executed successfully."""
        return self.err == 0

    def __repr__(self):
        """How to represent in a terminal."""
        return "<ApiResponse [{}]>".format("ok" if self.ok() else self.err)


def get(url):
    """Perform an API GET.

    Arguments
    ---------
    url : str
        The path (with query params)

    Returns
    -------
    Decoded JSON.
    """
    content = requests.get(url).content
    # Interestingly, the API compresses the JSON and sends the compressed bytes
    # instead of using HTTP gzip compression.
    return json.loads(zlib.decompress(content).decode('utf-8'))


def make_api_func(name, params):
    """Create a function for a single endpoint."""
    def _api_func(*args, **kwargs):
        query_params = urlencode(dict(zip(params, args)))
        json_response = get("{}{}?{}".format(BASE_URL, name, query_params))
        return ApiResponse(json_response)
    return _api_func


BASE_URL = "https://launcher.escapefromtarkov.com/launcher/"
ENDPOINTS = {
    "GetLauncherDistrib": [],
    "GetUpdatesFromVersion": ["version"],
    "GetUnpackedDistrib": ["version"],
    "GetDistrib": []
}
API = {
    name: make_api_func(name, params)
    for name, params in ENDPOINTS.items()
}
