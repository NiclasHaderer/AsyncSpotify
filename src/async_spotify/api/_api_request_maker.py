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

from ._response_status import ResponseStatus
from .._error_message import ErrorMessage
from ..authentification.spotify_authorization_token import SpotifyAuthorisationToken
from ..spotify_errors import SpotifyError, TokenExpired, RateLimitExceeded, SpotifyAPIError
from ..token_renew_class import TokenRenewClass


class ApiRequestHandler:
    """
    The request handler that makes the calls to the spotify api.
    This class is a singleton.
    """

    def __init__(self, spotify_authorisation_token: SpotifyAuthorisationToken,
                 token_renew_instance: TokenRenewClass,
                 spotify_api_client):
        """
        Create a new ApiRequestHandler class. The api class should be at least once passed to the constructor of this
        class. Otherwise it will not work.

        Args:
            spotify_authorisation_token: The auth token of the api class
            token_renew_instance: An instance of a token renew class
            spotify_api_client: The spotify api client
        """

        self.spotify_authorisation_token: SpotifyAuthorisationToken = spotify_authorisation_token
        self.token_renew_instance: TokenRenewClass = token_renew_instance
        self.__spotify_api_client = spotify_api_client
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

    async def make_request(self,
                           method: str,
                           url: str,
                           query_params: Optional[dict],
                           auth_token: SpotifyAuthorisationToken,
                           body: dict = None,
                           last_try=False) \
            -> Union[dict, List[bool], None, bool]:
        """
        Make a request to the spotify api

        Args:
            method: The method that should be used (get, post, put, delete)
            url: The url the request is going to
            query_params: URL query params for the request
            auth_token: The auth token (None if the in memory token should be used)
            body: Add a body to the request
            last_try: Check if this is the last try (used if you use a token refresh class)

        Returns: The spotify api response
        """

        if not self.client_session_list:
            message = 'You have to create a new client with create_new_client ' \
                      'before you can make requests to the spotify api.'
            raise SpotifyError(ErrorMessage(message=message).__dict__)

        # Prepare the data for the api request
        url_params, headers, updated_body = self._prepare_request_parameters(auth_token, query_params, body)

        # Round robin so you use a different client for every new request
        self.client_session_list.rotate(1)
        client: ClientSession = self.client_session_list[0]

        # Make the api response
        async with client.request(method, url, params=url_params, headers=headers, data=updated_body) as response:
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

            if self.token_renew_instance and not last_try:
                auth_token: SpotifyAuthorisationToken = await self.token_renew_instance(self.__spotify_api_client)

                # Update the auth token if the token should be kept in memory
                if self.spotify_authorisation_token.valid:
                    self.spotify_authorisation_token.access_token = auth_token.access_token
                    self.spotify_authorisation_token.activation_time = auth_token.activation_time
                    self.spotify_authorisation_token.refresh_token = auth_token.refresh_token

                return await self.make_request(method, url, query_params, auth_token, body, last_try=True)
            else:
                raise TokenExpired(response_json)

        # Rate limit exceeded
        if response_status.code == 429:
            raise RateLimitExceeded(response_json)

        # Check if the response was a success
        if not response_status.success:
            raise SpotifyAPIError(response_json)

        return response_json

    def _prepare_request_parameters(self, auth_token: SpotifyAuthorisationToken, query_params: dict, body: dict) \
            -> Tuple[List[Tuple[str, str]], dict, str]:
        """
        Prepare the request parameters for the aiohttp request

        Args:
            auth_token: An auth_token
            query_params: URL params for the request
            body: The request body (either string or dict)

        Returns:
            A tuple with the
                url_params
                headers
                body
            in the right format
        """
        url_params: List[Tuple[str, str]] = self._format_params(query_params)
        headers = self._get_headers(auth_token)

        # Check if the body should be a json or an image
        if body and isinstance(body, dict):
            body = json.dumps(body)
        elif body:
            headers['Content-Type'] = 'image/jpeg'

        return url_params, headers, body

    @staticmethod
    def _format_params(query_params: dict) -> List[Tuple[str, str]]:
        """
        Converts the query dict into the aiohttp conform Type

        Args:
            query_params: The query params

        Returns: The aiohttp conform object
        """

        return_params: List[Tuple[str, str]] = []

        for key in list(query_params.keys()):
            if not isinstance(query_params[key], List):
                query_params[key] = [str(query_params[key])]

            for value in query_params[key]:
                return_params.append((key, str(value)))

        return return_params

    def _get_headers(self, auth_token: SpotifyAuthorisationToken) -> dict:
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
                message = 'You have to provide a valid auth token or set the option hold_authentication to true and ' \
                          'call the get_auth_token_with_code or refresh_token method at leas once'
                raise SpotifyError(ErrorMessage(message=message).__dict__)

        return {
            'Authorization': f'Bearer {auth_token.access_token}',
            'Content-Type': 'application/json'
        }
