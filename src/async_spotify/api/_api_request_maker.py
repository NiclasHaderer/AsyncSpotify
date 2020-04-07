"""
The api request handler singleton
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (_api_request_maker.py) is part of AsyncSpotify which is released under MIT.          #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import json
import math
from collections import deque
from json import JSONDecodeError
from typing import Optional, List, Tuple, Deque, Union

from aiohttp import ClientTimeout, TCPConnector, ClientSession, DummyCookieJar

from async_spotify.authentification.spotify_authorization_token import SpotifyAuthorisationToken
from async_spotify.spotify_errors import SpotifyError, TokenExpired, RateLimitExceeded, SpotifyAPIError
from ._response_status import ResponseStatus


class ApiRequestHandler:
    """
    The request handler that makes the calls to the spotify api.
    This class is a singleton.
    """

    def __init__(self, spotify_authorisation_token: SpotifyAuthorisationToken):
        """
        Create a new ApiRequestHandler class. The api class should be at least once passed to the constructor of this
        class. Otherwise it will not work.

        Args:
            spotify_authorisation_token: The auth token of the api class
        """

        self.spotify_authorisation_token: SpotifyAuthorisationToken = spotify_authorisation_token
        self.client_session_list: Optional[Deque[ClientSession]] = deque([])

    async def create_new_client(self, request_timeout: int, request_limit: int) -> None:
        """
        Create a new client

        Args:
            request_timeout: The timout which should be used for making requests
            request_limit: The maximal number of requests per session
        """

        if self.client_session_list:
            await self.close_client()

        client_instance_number: int = math.ceil(request_limit / 500)

        for _ in range(client_instance_number):
            timeout = ClientTimeout(total=request_timeout)
            connector = TCPConnector(limit=request_limit, enable_cleanup_closed=True)
            client_session = ClientSession(connector=connector, timeout=timeout, cookie_jar=DummyCookieJar())

            self.client_session_list.append(client_session)

    async def close_client(self) -> None:
        """
        Close the current client session. You have to create a new one to connect again to spotify.
        This method should always be called before you end your program
        """

        for client in self.client_session_list:
            await client.close()

        self.client_session_list: Deque = deque([])

    async def make_request(self, method: str, url: str, query_params: dict,
                           auth_token: SpotifyAuthorisationToken, body: dict = None) -> Union[dict, List[bool], None]:
        """
        Make a request to the spotify api

        Args:
            method: The method that should be used (get, post, put, delete)
            url: The url the request is going to
            query_params: URL query params for the request
            auth_token: The auth token (None if the in memory token should be used)
            body: Add a body to the request

        Returns: The spotify api response
        """

        if not self.client_session_list:
            raise SpotifyError('You have to create a new client with create_new_client'
                               ' before you can make requests to the spotify api.')

        params: List[Tuple[str, str]] = self.format_params(query_params)
        headers = self.get_headers(auth_token)

        # Rotate the list
        self.client_session_list.rotate(1)

        # Get the first of the rotated list
        client: ClientSession = self.client_session_list[0]

        # Make the api response
        async with client.request(method, url, params=params, headers=headers, data=body) as response:
            response_status = ResponseStatus(response.status)

            # Handle the parsing of the rate limit exceeded response which does not work for some reason
            response_text: str = await response.text()
            response_json: dict = {}

            try:
                response_json: dict = json.loads(response_text)
            except JSONDecodeError:
                pass

        # Expired
        if response_status.code == 401:
            raise TokenExpired(response_json)

        # Rate limit exceeded
        if response_status.code == 429:
            raise RateLimitExceeded(response_status.message, " ", response_json)

        # Check if the response was a success
        if not response_status.success:
            raise SpotifyAPIError(response_json)

        if response_json:
            return response_json

        response_text

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
            temp = query_params[key]
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

        if not auth_token:

            if self.spotify_authorisation_token.valid:
                auth_token = self.spotify_authorisation_token
            else:
                raise SpotifyError(
                    'You have to provide a valid auth token or set the option hold_authentication to true '
                    'and call the get_auth_token_with_code or refresh_token method at leas once')

        return {
            'Authorization': f'Bearer {auth_token.access_token}',
            'Content-Type': 'application/json'
        }
