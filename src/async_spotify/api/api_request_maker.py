"""
The api request handler singleton
"""
from typing import Optional

from aiohttp import ClientTimeout, TCPConnector, ClientSession

from .response_status import ResponseStatus
from ..authentification.spotify_authorization_token import SpotifyAuthorisationToken
from ..spotify_errors import SpotifyError, TokenExpired, RageLimitExceeded


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

        method = method.lower()

        if not self.client_session:
            raise SpotifyError('You have to create a new client with create_new_client'
                               ' before you can make requests to the spotify api. ')

        header = self.get_header(auth_token)

        async with self.client_session.request(method, url, params=query_params, headers=header) as response:
            response_status = ResponseStatus(response.status)
            response_json: dict = await response.json()

        # Expired
        if response_status.code == 401:
            raise TokenExpired(response_status.message, " ", response_json)

        # Rage limit exceeded
        if response_status.code == 429:
            raise RageLimitExceeded(response_status.message, " ", response_json)

        # Check if the response was a success
        if not response_status.success:
            raise SpotifyError(response_status.message, " ", response_json)

        return response_json

    def get_header(self, auth_token: SpotifyAuthorisationToken) -> dict:
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
