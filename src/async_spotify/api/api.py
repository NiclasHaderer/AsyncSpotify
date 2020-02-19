import asyncio
import base64
import json
import subprocess
import time
import webbrowser
from json import JSONDecodeError
from multiprocessing import Process
from subprocess import CompletedProcess
from urllib.parse import urlencode

import aiohttp

from async_spotify.api.urls import URLS
from async_spotify.authentification import SpotifyAuthorisationToken
from async_spotify.authentification import create_callback_server
from async_spotify.preferences import Preferences
from async_spotify.spotify_errors import SpotifyError


class API:
    def __init__(self, preferences: Preferences, hold_authentication=False):
        """
        Create a new api class
        :param preferences: The preferences object fully filled with information
        :param hold_authentication: Should the api keep the authentication im memory and refresh it automatically
        """

        if not preferences.validate():
            raise SpotifyError("The preferences of your app are not correct")

        self.preferences: Preferences = preferences
        self.hold_authentication: bool = hold_authentication

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
        :param show_dialogue: Should the spotify auth dialog be shown
        :return: None
        """

        # Open url in a new window of the default browser, if possible
        webbrowser.open_new(self.build_authorization_url(show_dialogue))

    async def get_code_with_cookie(self, cookie_file_location: str, callback_server_port: int = 1234,
                                   callback_server_url: str = "/test/api/callback") -> json:
        """
        This function takes care of the user interaction that is normally necessary to get the first code from spotify
        which is necessary to request the refresh_token and the oauth_token.
        The token that is returned by this function has to be passed to API.refresh_token(code, reauthorize=False)
        to get the refresh_token and the oauth_token.
        This will only work if the user has at least once accepted the scopes your app is requesting.
        I would recommend that you take a look at the source code of this function before you use it and that you are
        familiar with the authorization mechanism of spotify.
        This method is intended for automated testing. You have to decide if you want to use it in you production
        environment.
        :param cookie_file_location: The absolute path to the cookie file with all the active cookies in you browser
        when you visit
        https://open.spotify.com. The format is the same one used by curl.
        Take a look at this post if you wat to know the format of the cookies in the file:
        https://stackoverflow.com/questions/7181785/send-cookies-with-curl.
        To download the cookies you can use this extension. I don't know who wrote it and it is not open source so
        download and use it with care.
        https://chrome.google.com/webstore/detail/cookiestxt/njabckikapfpffapmjgojcnbfjonfjfg
        :param callback_server_port: The port the callback server will use to display the callback of the spotify api
        :param callback_server_url: The url the callback server will listen for callbacks for. Don't forget to add the
        url http://localhost:1111/test/api/callback to the allowed urls in the panel of you spotify app
        (developer.spotify.com)

        :return: The spotify code that can be used to get a refresh_token and a oauth_token
        :raises SpotifyError if the command was not successful
        :raises UnicodeDecodeError if the returned string could not be decoded
        :raises JSONDecodeError if the returned and decoded string is not a valid json
        """

        # Build the auth url
        url = self.build_authorization_url(show_dialog=False)

        # Create a webserver that runs in another process
        webserver_process: Process = create_callback_server(callback_server_port, callback_server_url)

        # Give the server some time to start
        await asyncio.sleep(5)

        # Curl the code from spotify
        response: CompletedProcess = subprocess.run(['curl', '-L', '--cookie', f'{cookie_file_location}', f"{url}"],
                                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # Check if the return code is correct (otherwise raise exception)
        if response.returncode != 0:
            raise SpotifyError(response.stderr)

        try:
            return_string: str = response.stdout.decode()
        except UnicodeDecodeError:
            webserver_process.kill()
            raise SpotifyError("The returned code could not be decoded." + response.stderr.decode())
        try:
            # TODO logging
            return_json: dict = json.loads(return_string)
        except JSONDecodeError:
            # TODO logging
            webserver_process.kill()
            raise SpotifyError("The returned code could not be parsed as a json. Is the cookie file the right one?"
                               + response.stderr.decode())

        # Stop the webserver thread
        webserver_process.kill()
        return return_json

    async def refresh_token(self, refresh_token: SpotifyAuthorisationToken = None, reauthorize: bool = True,
                            code: str = None) -> SpotifyAuthorisationToken:
        """
        Refresh the auth token with the refresh token or get a new auth token and refresh token with the code returned
        by the spotify auth flow
        :param refresh_token: The refresh token or the code returned by the spotify auth flow
        :param reauthorize: Do want to reauthorize a expiring SpotifyAuthorisationToken or get a new one with the
        spotify code. Set to false and add the code="your_code_here" if you want to get the SpotifyAuthorisationToken
        for the first time
        :param code: The code returned by spotify and the OAuth
        :return: The SpotifyAuthorisationToken
        """

        grant_type = "refresh_token"
        if not reauthorize:
            grant_type = "authorization_code"

        body: dict = {
            "grant_type": grant_type,
        }

        if reauthorize:
            body["refresh_token"] = refresh_token.refresh_token
        else:
            body["code"] = code
            body["redirect_uri"] = self.preferences.redirect_url

        base_64: base64 = base64.b64encode(
            f"{self.preferences.application_id}:{self.preferences.application_secret}".encode("ascii"))
        header: dict = {'Authorization': f'Basic {base_64.decode("ascii")}'}

        async with aiohttp.ClientSession() as session:
            async with session.post(url=URLS.REFRESH, data=body, headers=header) as response:
                print(response.status)
                print(await response.text())

        return SpotifyAuthorisationToken("", int(time.time()))
