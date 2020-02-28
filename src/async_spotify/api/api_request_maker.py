"""
The api request handler singleton
"""
from .response_status import ResponseStatus
from ..authentification.spotify_authorization_token import SpotifyAuthorisationToken
from ..spotify_errors import SpotifyAuthError, SpotifyError


class Singleton(type):
    """
    Singleton class
    """

    _instance = None

    def __call__(cls, api=None):  # :type async_spotify.API
        """
        Create a new ApiRequestHandler singleton

        Args:
            api: The main api object

        Returns: The ApiRequestHandler

        """

        if cls._instance is None:
            cls._instance = super().__call__(api)

        if api:
            cls._instance.api = api

        return cls._instance


class ApiRequestHandler(metaclass=Singleton):
    """
    The request handler that makes the calls to the spotify api.
    This class is a singleton.
    """

    def __init__(self, api=None):  # :type async_spotify.API
        """
        Create a new ApiRequestHandler class. The api class should be at least once passed to the constructor of this
        class. Otherwise it will not work.

        Args:
            api: The main api class
        """
        self.api = api  # :type async_spotify.API

    async def get_request(self, url: str, query_params: dict, auth_token: SpotifyAuthorisationToken) -> dict:
        """
        Make a get request to the spotify api

        Args:
            url: The url the request is going to
            query_params: The query params
            auth_token: The auth token (None if the in memory token should be used)

        Returns: The spotify api response
        """

        header = self.api.get_header(auth_token)

        async with self.api.session.get(url, params=query_params, header=header) as response:
            response_status = ResponseStatus(response.status)
            response_json: dict = await response.json()

        # Check if the auth code has expired
        if response_status.code == 401:
            raise SpotifyAuthError(response_status.message, " ", response_json)

        # Check if the response was a success
        if not response_status.success:
            raise SpotifyError(response_status.message, " ", response_json)

        return response_json

    async def put_request(self, url: str, query_params: dict, auth_token: SpotifyAuthorisationToken) -> dict:
        pass
