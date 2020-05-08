"""
The main api class which will be used to authenticate and connect to the spotify api
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (spotify_api_client.py) is part of AsyncSpotify which is released under MIT.          #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import base64
import json
import time
import webbrowser
from copy import deepcopy
from types import SimpleNamespace
from typing import Optional, List
from urllib import parse
from urllib.parse import urlencode

from aiohttp import ClientSession, TraceConfig, TraceRequestRedirectParams, ClientConnectorError

from ._api_request_maker import ApiRequestHandler
from ._endpoints.albums import Albums
from ._endpoints.artists import Artists
from ._endpoints.browse import Browse
from ._endpoints.episodes import Episodes
from ._endpoints.follow import Follow
from ._endpoints.library import Library
from ._endpoints.personalization import Personalization
from ._endpoints.player import Player
from ._endpoints.playlists import Playlists
from ._endpoints.search import Search
from ._endpoints.shows import Shows
from ._endpoints.tracks import Track
from ._endpoints.urls import URLS
from ._endpoints.user import User
from ._response_status import ResponseStatus
from .preferences import Preferences
from .._error_message import ErrorMessage
from ..authentification.spotify_authorization_token import SpotifyAuthorisationToken
from ..authentification.spotify_cookies import SpotifyCookie
from ..spotify_errors import SpotifyError
from ..token_renew_class import TokenRenewClass


class SpotifyApiClient:
    """
    The main api class which will be used to authenticate and connect to the spotify api.
    Use this class to authenticate and connect to the spotify api.
    """

    def __init__(self, preferences: Preferences,
                 hold_authentication=False,
                 spotify_authorisation_token: SpotifyAuthorisationToken = None,
                 token_renew_instance: TokenRenewClass = None):
        """
        Create a new api class

        Args:
            preferences: The preferences object fully filled with information
            hold_authentication: Should the api keep the authentication im memory and refresh it automatically
            token_renew_instance: An instance of a class which handles the renewing of the token if it should expire
        """

        # Check if the preferences are valid
        if not preferences.valid:
            raise SpotifyError(ErrorMessage(message="The preferences of your app are not correct").__dict__)
        self.preferences: Preferences = preferences

        # Set the SpotifyAuthorisationToken
        if spotify_authorisation_token:
            self._spotify_authorisation_token: SpotifyAuthorisationToken = spotify_authorisation_token
        else:
            self._spotify_authorisation_token: SpotifyAuthorisationToken = SpotifyAuthorisationToken()

        self._token_renew_instance: TokenRenewClass = token_renew_instance
        self._hold_authentication: bool = hold_authentication
        self._api_request_handler: ApiRequestHandler = ApiRequestHandler(self._spotify_authorisation_token,
                                                                         token_renew_instance, self)

        ################################################################################################################
        self.albums: Albums = Albums(self._api_request_handler)
        """ An instance of the [`Albums`][async_spotify.api._endpoints.albums] class. Use this to access the 
         Albums api """

        self.artists: Artists = Artists(self._api_request_handler)
        """ An instance of the [`Artists`][async_spotify.api._endpoints.artists] class. Use this to access the 
         Artists api """

        self.browse: Browse = Browse(self._api_request_handler)
        """ An instance of the [`Browse`][async_spotify.api._endpoints.browse] class. Use this to Browse the 
        Browse api """

        self.episodes: Episodes = Episodes(self._api_request_handler)
        """ An instance of the [`Episodes`][async_spotify.api._endpoints.episodes] class. Use this to access the 
         Episodes api """

        self.follow: Follow = Follow(self._api_request_handler)
        """ An instance of the [`Follow`][async_spotify.api._endpoints.follow] class. Use this to access the 
         Follow api """

        self.library: Library = Library(self._api_request_handler)
        """ An instance of the [`Library`][async_spotify.api._endpoints.library] class. Use this to access the 
         Library api """

        self.personalization: Personalization = Personalization(self._api_request_handler)
        """ An instance of the [`Personalization`][async_spotify.api._endpoints.personalization] class. Use this to 
        access the Personalization api """

        self.player: Player = Player(self._api_request_handler)
        """ An instance of the [`Player`][async_spotify.api._endpoints.player] class. Use this to access the 
         Player api """

        self.playlists: Playlists = Playlists(self._api_request_handler)
        """ An instance of the [`Playlists`][async_spotify.api._endpoints.playlists] class. Use this to access the 
         Playlist api """

        self.search: Search = Search(self._api_request_handler)
        """ An instance of the [`Search`][async_spotify.api._endpoints.search] class. Use this to access the 
         Search api """

        self.shows: Shows = Shows(self._api_request_handler)
        """ An instance of the [`Shows`][async_spotify.api._endpoints.shows] class. Use this to access the 
         Show api """

        self.track: Track = Track(self._api_request_handler)
        """ An instance of the [`Track`][async_spotify.api._endpoints.tracks] class. Use this to access the 
         Track api """

        self.user: User = User(self._api_request_handler)
        """ An instance of the [`User`][async_spotify.api._endpoints.user] class. Use this to access the 
         User api """

    async def create_new_client(self, request_timeout: int = 30, request_limit: int = 500) -> None:
        """
        Create a new session which will be used to connect to the spotify api.
        In general this only has to be called once after you create a new API object.
        You can however call this method if you want ot update the client settings (more requests, ...)
        This will however close all ongoing requests.

        Args:
            request_timeout: How long should be waited for a request (default 30s) (None for no limit)
            request_limit: How many requests should be allowed (default 500)
        """

        await self._api_request_handler.create_new_client(request_timeout, request_limit)

    async def close_client(self) -> None:
        """
        Close the current client session. You have to create a new one to connect again to spotify.
        This method should always be called before you end your program
        """

        await self._api_request_handler.close_client()

    def build_authorization_url(self, show_dialog: bool = True, state: str = None) -> str:
        """
        Builds the URL for the authorisation

        Args:
            state: State of the authorization
            show_dialog: Should the spotify auth dialog be shown

        Returns:
            The encoded url which can be used to authorize a new or existing user
        """

        params = {
            "client_id": self.preferences.application_id,
            "response_type": "code",
            "scope": ' '.join(self.preferences.scopes),
            "show_dialog": f"{show_dialog}",
            "redirect_uri": f"{self.preferences.redirect_url}"
        }

        # Check if a state is required
        if state:
            params["state"] = f"{state}"

        return f"{URLS.AUTHORIZE}?{urlencode(params)}"

    def open_oauth_dialog_in_browser(self, show_dialogue: bool = True) -> None:
        """
        Open the url in browser
        Only for testing purposes or the usage of this library in a desktop app

        Args:
            show_dialogue: Should the spotify auth dialog be shown
        """

        # Open url in a new window of the default browser, if possible
        webbrowser.open_new(self.build_authorization_url(show_dialogue))

    async def get_code_with_cookie(self, cookies: SpotifyCookie) -> str:
        """
        This function takes care of the user interaction that is normally required to get the code from spotify
        which is necessary to request the refresh_token and the oauth_token.
        The token which is returned by this function has to be passed to API.get_auth_token_with_code(code)
        to get the refresh_token and the oauth_token.
        The big advantage is that you don't have to run a callback server to get the code

        Notes:
            This will only work if the user has at least once accepted the scopes your app is requesting.
            I would recommend that you take a look at the source code of this function before you use it and that you
            are familiar with the authorization mechanism of spotify.

        Important:
            This method is intended for automated testing. You have to decide if you want to use it in you production
            environment.

        Args:
            cookies: The cookies of the spotify account. Every property of the class has to be filled in.

        Raises:
            SpotifyError: If the cookie is not valid
            SpotifyError: If there is a redirect between you and spotify
            SpotifyError: If there is an unknown error

        Returns:
            The spotify code which can be used to get a refresh_token and a oauth_token
        """

        # Build the auth url
        url = self.build_authorization_url(show_dialog=False)

        # Check if the cookie file is valid
        if not cookies.valid:
            raise SpotifyError(ErrorMessage(message='The cookies are not complete').__dict__)

        # Convert the class to a dict
        cookie_dict: dict = cookies.__dict__

        return await self._track_request_without_callback(cookie_dict, url)

    @staticmethod
    async def _track_request_without_callback(cookie_dict: dict, url: str) -> str:
        """
        Make a request to the spotify api without redirects. No callback server needed.

        Args:
            cookie_dict: The cookie dict used for authentification
            url: The url of the spotify request

        Raises:
            SpotifyError: If there is a redirect between you and spotify
            SpotifyError: If there is an unknown error

        Returns: The code of spotify
        """

        code: Optional[str] = None

        async def redirect(_: ClientSession, __: SimpleNamespace, trace_request: TraceRequestRedirectParams) -> None:
            """
            Handler the redirect event aiohttp is firing

            Args:
                _: ClientSession
                __: SimpleNamespace
                trace_request: The current redirect request response
            """

            # Get the redirect url
            location: Optional[str] = trace_request.response.headers.get('location')

            # Parse the url
            local_url = parse.urlparse(location)
            query: dict = parse.parse_qs(local_url.query)

            # Check if code is the redirect url
            _code: Optional[List[str]] = query.get('code')

            if _code:
                nonlocal code
                code = _code[0]

        # Create a callback every time there is a redirect
        trace_config = TraceConfig()
        trace_config.on_request_redirect.append(redirect)

        try:
            # Make an api request to spotify
            async with ClientSession(cookies=cookie_dict, trace_configs=[trace_config]) as session:
                async with session.get(url) as resp:
                    response_text = await resp.text()
            await session.close()
        except ClientConnectorError:
            # Ignore the error in case no callback server is running
            pass

        if not code:
            message = f'The collection of the code did not work. Did the user already agree to the scopes' \
                      f' of your app? \n {response_text}'

            raise SpotifyError(ErrorMessage(message=message).__dict__)

        return code

    async def get_auth_token_with_code(self, code: str) -> SpotifyAuthorisationToken:
        """
        Get the auth token with the code returned by the oauth process.

        Args:
            code: The code returned by spotify in the oauth process

        Notes:
            [https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow](https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow)

        Raises:
            SpotifyError: If the request to the refresh api point was not successful

        Returns:
            A valid SpotifyAuthorisationToken
        """

        body: dict = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.preferences.redirect_url
        }

        response_json: dict = await self._make_auth_api_request(body)

        refresh_token: str = response_json['refresh_token']
        access_token: str = response_json['access_token']

        self._spotify_authorisation_token.refresh_token = refresh_token
        self._spotify_authorisation_token.activation_time = int(time.time())
        self._spotify_authorisation_token.access_token = access_token

        return deepcopy(self._spotify_authorisation_token)

    async def refresh_token(self, auth_token: SpotifyAuthorisationToken = None) -> SpotifyAuthorisationToken:
        """
        Refresh the auth token with the refresh token or get a new auth token and refresh token with the code returned
        by the spotify auth flow.

        Args:
            auth_token: The refresh token or the code returned by the spotify auth flow. Leave empty if you enabled
                hold_authentication. Then the internal token will be used.

        Notes:
            https://developer.spotify.com/documentation/general/guides/authorization-guide/#authorization-code-flow

        Returns:
            The SpotifyAuthorisationToken
        """

        # Check if the internal auth token should be used
        if not auth_token and self._hold_authentication:
            auth_token = self._spotify_authorisation_token

        body: dict = {
            'grant_type': 'refresh_token',
            'refresh_token': auth_token.refresh_token
        }

        response_json: dict = await self._make_auth_api_request(body)

        refresh_token = auth_token.refresh_token
        access_token = response_json['access_token']

        # Keep the auth token in memory
        self._spotify_authorisation_token.refresh_token = refresh_token
        self._spotify_authorisation_token.activation_time = int(time.time())
        self._spotify_authorisation_token.access_token = access_token

        return deepcopy(self._spotify_authorisation_token)

    async def _make_auth_api_request(self, body: dict) -> dict:
        """
        Make an api request to the refresh endpoint

        Args:
            body: The body of the request

        Returns:
            The access token and the refresh token if the grant_type was code
        """

        # Build the header of the request
        base_64: base64 = base64.b64encode(
            f'{self.preferences.application_id}:{self.preferences.application_secret}'.encode('ascii'))
        header: dict = {'Authorization': f'Basic {base_64.decode("ascii")}'}

        # Make the request to the api
        async with ClientSession() as session:
            async with session.post(url=URLS.REFRESH, data=body, headers=header) as response:
                response_status = ResponseStatus(response.status)
                response_text: str = await response.text()
            await session.close()

        # The response was not ok
        if not response_status.success:
            raise SpotifyError(ErrorMessage(message=response_text).__dict__)

        return json.loads(response_text)

    async def next(self, url: str, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get the next 'page' of the response

        Args:
            url: The next url
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            The api response
        """

        return await self._api_request_handler.make_request('GET', url, {}, auth_token)

    async def previous(self, url: str, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get the next 'previous' of the response

        Args:
            url: The previous url
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            The api response
        """

        return await self._api_request_handler.make_request('GET', url, {}, auth_token)

    @property
    def spotify_authorization_token(self) -> SpotifyAuthorisationToken:
        """
        Returns:
            The SpotifyAuthorisationToken of the api class
        """
        if not self._hold_authentication:
            raise SpotifyError(ErrorMessage(message='You have to enable hold_authentication').__dict__)

        return self._spotify_authorisation_token

    @spotify_authorization_token.setter
    def spotify_authorization_token(self, spotify_authorization_token: SpotifyAuthorisationToken) -> None:
        """
        Update the spotify auth token

        Args:
            spotify_authorization_token: The spotify auth token
        """

        if not self._hold_authentication:
            raise SpotifyError(ErrorMessage(message='You have to enable hold_authentication').__dict__)

        self._spotify_authorisation_token.refresh_token = spotify_authorization_token.refresh_token
        self._spotify_authorisation_token.access_token = spotify_authorization_token.access_token
        self._spotify_authorisation_token.activation_time = spotify_authorization_token.activation_time

    @property
    def hold_authentication(self) -> bool:
        """
        Returns:
            The hold_authentication property of the spotify api client class
        """

        return self._hold_authentication

    @hold_authentication.setter
    def hold_authentication(self, hold_authentication: bool) -> None:
        """
        Set the hold_authentication param

        Args:
            hold_authentication: Should internal auth token be used for authentication
        """

        self._hold_authentication = hold_authentication

        if not hold_authentication:
            self._spotify_authorisation_token.activation_time = None
            self._spotify_authorisation_token.access_token = None
            self._spotify_authorisation_token.refresh_token = None

    @property
    def token_renew_instance(self) -> TokenRenewClass:
        """
        Returns the token renew class instance

        Returns: The token renew class instance
        """

        return self._token_renew_instance

    @token_renew_instance.setter
    def token_renew_instance(self, value: TokenRenewClass) -> None:
        """
        Set the token renew instance

        Args:
            value: The new token renew instance
        """

        self._token_renew_instance = value
        self._api_request_handler.token_renew_instance = value
