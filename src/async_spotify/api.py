import base64
import time
import webbrowser
from urllib.parse import urlencode

import aiohttp

from async_spotify.authentification.spotify_authorization_token import SpotifyAuthorisationToken
from async_spotify.authentification.preferences import Preferences
from async_spotify.spotify_errors import SpotifyError
from async_spotify.urls import URLS


class API:
    def __init__(self, preferences: Preferences):
        if not preferences.validate():
            raise SpotifyError("The preferences of your app are not correct")

        self.preferences: Preferences = preferences

    def build_authorization_url(self, show_dialog=True, state: str = None) -> str:
        """
        Builds the URL for the authorisation
        :param state: State of the authorization
        :param show_dialog: Should the spotify auth dialog be shown
        :return: The encoded url
        """

        params = {
            "client_id": self.preferences.application_id,
            "response_type": "code",
            "scope": ' '.join(self.preferences.scopes),
            "show_dialog": f"{show_dialog}",
        }

        url: str = f"{URLS.AUTHORIZE}?redirect_uri={self.preferences.redirect_url}&{urlencode(params)}"

        # Check if a state is required
        url += f"&state={state}" if state else ""
        return url

    def open_oauth_dialog_in_browser(self, show_dialogue: bool = True) -> None:
        """
        Open the url in browser
        Only for testing purposes or the usage of this library in a desktop app
        :param show_dialogue: Should the spotify auth dialog be shown
        :return: None
        """

        # Open url in a new window of the default browser, if possible
        webbrowser.open_new(self.build_authorization_url(show_dialogue))

    async def refresh_token(self, refresh_token: str, reauthorize=True) -> SpotifyAuthorisationToken:
        """
        Refresh the auth token with the refresh token or get a new auth token and refresh token with the code returned
        by the spotify auth flow
        :param refresh_token: The refresh token or the code returned by the spotify auth flow
        :param reauthorize: Should the token be reauthorized with a refresh token, or is this the first time you trie
        to get a oauth_token and refresh token from spotify
        :return: The SpotifyAuthorisationToken
        """

        grant_type = "refresh_token"
        if not reauthorize:
            grant_type = "authorization_code"

        body: dict = {
            "grant_type": grant_type,
        }

        if reauthorize:
            body["refresh_token"] = refresh_token
        else:
            body["code"] = refresh_token
            body["redirect_uri"] = self.preferences.redirect_url

        base_64: base64 = base64.b64encode(
            f"{self.preferences.application_id}:{self.preferences.application_secret}".encode("ascii"))
        header: dict = {'Authorization': f'Basic {base_64.decode("ascii")}'}

        async with aiohttp.ClientSession() as session:
            async with session.post(url=URLS.REFRESH, data=body, headers=header) as response:
                print(response.status)
                print(await response.text())

        return SpotifyAuthorisationToken("", int(time.time()))
