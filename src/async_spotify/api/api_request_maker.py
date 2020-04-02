"""
The api request handler singleton
"""
from typing import Optional, List, Tuple

from aiohttp import ClientTimeout, TCPConnector, ClientSession

from .response_status import ResponseStatus
from ..authentification.spotify_authorization_token import SpotifyAuthorisationToken
from ..spotify_errors import SpotifyError, TokenExpired, RateLimitExceeded


# TODO multiple sessions for more than 500 requests
# TODO Round robin scheduling ???

class ApiRequestHandler:
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
        self.client_session: Optional[ClientSession] = None

    async def create_new_client(self, request_timeout: int, request_limit: int) -> None:
        """
        Create a new client

        Args:
            request_timeout: The timout which should be used for making requests
            request_limit: The maximal number of requests per session

        Returns:
            None
        """

        if self.client_session:
            await self.client_session.close()

        timeout = ClientTimeout(total=request_timeout)
        connector = TCPConnector(limit=request_limit, enable_cleanup_closed=True)
        self.client_session = ClientSession(connector=connector, timeout=timeout)

    async def close_client(self) -> None:
        """
        Close the current client session. You have to create a new one to connect again to spotify.
        This method should always be called before you end your program

        Returns:
            None
        """

        if self.client_session:
            await self.client_session.close()
            self.client_session = None

    async def make_request(self, method: str, url: str, query_params: dict,
                           auth_token: SpotifyAuthorisationToken) -> dict:
        """
        Make a request to the spotify api

        Args:
            method: The method that should be used (get, post, put, delete)
            url: The url the request is going to
            query_params: URL query params for the request
            auth_token: The auth token (None if the in memory token should be used)

        Returns: The spotify api response
        """

        if not self.client_session:
            raise SpotifyError('You have to create a new client with create_new_client'
                               ' before you can make requests to the spotify api.')

        params: List[Tuple[str, str]] = self.format_params(query_params)
        headers = self.get_headers(auth_token)

        async with self.client_session.request(method, url, params=params, headers=headers) as response:
            response_status = ResponseStatus(response.status)
            response_json: dict = {}
            response_text: str = ""
            if response_status.success:
                response_json = await response.json()
            else:
                response_text = await response.text()

        # Expired
        if response_status.code == 401:
            raise TokenExpired(response_status.message, " ", response_text)

        # Rate limit exceeded
        if response_status.code == 429:
            raise RateLimitExceeded(response_status.message, " ", response_text)

        # TODO check if exception should be thrown if the album id or other things are invalid
        # Check if the response was a success
        if not response_status.success:
            raise SpotifyError(response_status.message, " ", response_text)

        return response_json

    @staticmethod
    def format_params(query_params: dict) -> List[Tuple[str, str]]:
        """
        Converts the query dict into the aiohttp conform Type

        Args:
            query_params: The query params

        Returns: The aiohttp conform object

        """

        return_params: List[Tuple[str, str]] = []

        for key in list(query_params.keys()):
            if isinstance(query_params[key], str):
                query_params[key] = [query_params[key]]

            for value in query_params[key]:
                return_params.append((key, value))

        return return_params

    def get_headers(self, auth_token: SpotifyAuthorisationToken) -> dict:
        """
        Build the spotify header used to authenticate the user for the spotify api

        Args:
            auth_token: The spotify auth token

        Returns: The header as json
        """

        if self.api.hold_authentication and not auth_token:
            auth_token = self.api.spotify_authorisation_token

        if not auth_token:
            raise SpotifyError('You have to provide a valid auth token or set the option hold_authentication to true '
                               'and call the get_auth_token_with_code or refresh_token method at leas once')

        return {
            'Authorization': f'Bearer {auth_token.access_token}',
            'Content-Type': 'application/json'
        }
