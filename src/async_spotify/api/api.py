"""
The main api class which will be used to authenticate and connect to the spotify api
"""

import base64
import json
import time
import webbrowser
from urllib import parse
from urllib.parse import urlencode

from aiohttp import ClientSession, TCPConnector, ClientTimeout

from .api_request_maker import ApiRequestHandler
from .endpoints.albums import Albums
from .endpoints.artists import Artists
from .endpoints.urls import URLS
from .response_status import ResponseStatus
from ..authentification.spotify_authorization_token import SpotifyAuthorisationToken
from ..authentification.spotify_cookies import SpotifyCookies
from ..preferences import Preferences
from ..spotify_errors import SpotifyError


class API:
    """
    The main api class which will be used to authenticate and connect to the spotify api.
    Use this class to authenticate and connect to the spotify api.
    """

    albums: Albums = Albums()
    artists: Artists = Artists()

    # noinspection PyTypeChecker
    def __init__(self, preferences: Preferences, hold_authentication=False):
        """
        Create a new api class
        Args:
            preferences: The preferences object fully filled with information
            hold_authentication: Should the api keep the authentication im memory and refresh it automatically
        """

        # Check if the preferences are valid
        if not preferences.validate():
            raise SpotifyError("The preferences of your app are not correct")

        # Set the preferences
        self.preferences: Preferences = preferences
        self.session: ClientSession = None

        self.hold_authentication: bool = hold_authentication
        self.spotify_authorisation_token: SpotifyAuthorisationToken = None

        self.api_request_handler: ApiRequestHandler = ApiRequestHandler(self)

    async def create_new_client(self, request_timeout: int = 30, request_limit: int = 500) -> None:
        """
        Create a new session which will be used to connect to the spotify api.
        In general this only has to be called once after you create a new API object.
        You can however call this method if you want ot update the client settings (more requests, ...)
        This will however close all ongoing requests.

        Args:
            request_timeout: How long should be waited for a request (default 30s) (None for no limit)
            request_limit: How many requests should be allowed (default 500)

        Returns:
            None
        """

        if self.session:
            await self.session.close()

        timeout = ClientTimeout(total=request_timeout)
        connector = TCPConnector(limit=request_limit, enable_cleanup_closed=True)
        self.session = ClientSession(connector=connector, timeout=timeout)

    async def close_client(self) -> None:
        """
        Close the current client session. You have to create a new one to connect again to spotify.
        This method should always be called before you end your program

        Returns:
            None
        """

        if self.session:
            await self.session.close()

    def build_authorization_url(self, show_dialog=True, state: str = None) -> str:
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

        Returns:
            None
        """

        # Open url in a new window of the default browser, if possible
        webbrowser.open_new(self.build_authorization_url(show_dialogue))

    async def get_code_with_cookie(self, cookies: SpotifyCookies) -> str:
        """
        This function takes care of the user interaction that is normally necessary to get the first code from spotify
        which is necessary to request the refresh_token and the oauth_token.
        The token that is returned by this function has to be passed to API.refresh_token(code, reauthorize=False)
        to get the refresh_token and the oauth_token.

        Note:
            This will only work if the user has at least once accepted the scopes your app is requesting.
            I would recommend that you take a look at the source code of this function before you use it and that you
            are familiar with the authorization mechanism of spotify.

        Important:
            This method is intended for automated testing. You have to decide if you want to use it in you production
            environment.

        Args:
            cookies: The cookies of the spotify account. Every property of the class has to be filled in.

        Raises:
            SpotifyError: An error occurred during the code retrial

        Returns:
            The spotify code which can be used to get a refresh_token and a oauth_token
        """

        # Build the auth url
        url = self.build_authorization_url(show_dialog=False)

        # Check if the cookie file is valid
        if not cookies.validate():
            raise SpotifyError('The cookies are not complete')

        # Convert the class to a dict
        cookie_dict: dict = cookies.__dict__

        # Make an api request to spotify
        async with ClientSession(cookies=cookie_dict, requote_redirect_url=False) as session:
            async with session.get(url, allow_redirects=False) as resp:
                # Get the headers
                headers = resp.headers

                # Check if the request should have been redirected
                if 'location' not in headers:
                    raise SpotifyError('There was no redirect in in the spotify response. Has the user accepted the '
                                       'scopes once before or has the cookie not the right values?')

                # Get the redirect url
                location: str = headers['location']

                # Parse the url
                local_url = parse.urlparse(location)
                query = parse.parse_qs(local_url.query)

                # Check if code is the redirect url
                if 'code' not in query:
                    raise SpotifyError('There was no code parameter in the redirect url')

                return str(query['code'])

    async def refresh_token(self, passed_auth_token_object: SpotifyAuthorisationToken = None,
                            reauthorize: bool = True, code: str = None) -> SpotifyAuthorisationToken:
        """
        Refresh the auth token with the refresh token or get a new auth token and refresh token with the code returned
        by the spotify auth flow

        Args:
            passed_auth_token_object: The refresh token or the code returned by the spotify auth flow
            reauthorize: Do want to reauthorize a expiring SpotifyAuthorisationToken or get a new one with the
                spotify code. Set to false and add the code="your_code_here" if you want to get the
                SpotifyAuthorisationToken for the first time
            code: The code returned by spotify and the OAuth

        Returns:
            The SpotifyAuthorisationToken
        """

        grant_type: str = "refresh_token"
        if not reauthorize:
            grant_type = "authorization_code"

        body: dict = {
            "grant_type": grant_type,
        }

        if reauthorize:
            body["refresh_token"] = passed_auth_token_object.refresh_token
        else:
            body["code"] = code
            body["redirect_uri"] = self.preferences.redirect_url

        base_64: base64 = base64.b64encode(
            f"{self.preferences.application_id}:{self.preferences.application_secret}".encode("ascii"))
        header: dict = {'Authorization': f'Basic {base_64.decode("ascii")}'}

        if not self.session:
            raise SpotifyError("You have to create a new session with API.create_new_client() to connect to spotify")

        async with self.session.post(url=URLS.REFRESH, data=body, headers=header) as response:
            response_status = ResponseStatus(response.status)
            response_text: str = await response.text()

        response_text: dict = json.loads(response_text)

        # The response was not ok
        if not response_status.success:
            raise SpotifyError(response_status.message + "\n" + str(response_text))

        if "refresh_token" not in response_text:
            refresh_token = passed_auth_token_object.refresh_token
        else:
            refresh_token = response_text["refresh_token"]
        spotify_authorisation_token = SpotifyAuthorisationToken(refresh_token=refresh_token,
                                                                activation_time=int(time.time()),
                                                                access_token=response_text["access_token"])
        # Keep the auth token in memory
        if self.hold_authentication:
            self.spotify_authorisation_token = spotify_authorisation_token

        return spotify_authorisation_token

    def get_header(self, auth_token: SpotifyAuthorisationToken = None) -> json:
        """
        Build the spotify header used to authenticate the user for the spotify api

        Args:
            auth_token: Optional argument. If you store the auth token in memory (api.hold_authentification = True)
                you can skip this.

        Returns: The header as json
        """

        if auth_token:
            return {
                "Authorization": f"Bearer {auth_token.access_token}",
                "Content-Type": "application/json"
            }

        if self.hold_authentication and not self.spotify_authorisation_token:
            raise SpotifyError("You don't have a spotify auth token stored in memory")

        return {
            "Authorization": f"Bearer {self.spotify_authorisation_token.access_token}",
            "Content-Type": "application/json"
        }
