import base64
import webbrowser
from urllib.parse import urlencode

import aiohttp

from async_spotify.spotify_authorization_token import SpotifyAuthorisationToken
from async_spotify.preferences import Preferences
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

    async def refresh_token(self, refresh_token: str, grant_type: str = "refresh_token") -> SpotifyAuthorisationToken:
        """
        Refresh the auth token with the refresh token or get a new auth token and refresh token with the code returned
        by the spotify auth flow
        :param refresh_token: The refresh token or the code returned by the spotify auth flow
        :param grant_type: Default to refresh the token | Has to be "authorization_code" if you only have the code
        returned by spotify
        :return:
        """

        body: dict = {
            "grant_type": grant_type,
        }

        if grant_type == "refresh_token":
            body["refresh_token"] = refresh_token
        elif grant_type == "authorization_code":
            body["code"] = refresh_token
            body["redirect_uri"] = self.preferences.redirect_url

        app_id = self.preferences.application_id
        app_secret = self.preferences.application_secret

        b = str(base64.b64encode(f"{app_id}:{app_secret}".encode("UTF-8")), encoding="UTF-8")
        header: base64 = f' Authorization: Basic {b}'

        async with aiohttp.ClientSession() as session:
            async with session.post(URLS.REFRESH, data=body, headers=header) as resp:
                print(resp.status)
                print(await resp.text())

        return ""
