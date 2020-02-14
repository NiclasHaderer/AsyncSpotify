import webbrowser
from urllib.parse import urlencode

from Preferences import Preferences
from SpotifyError import SpotifyError
from URLS import URLS


class API:
    def __init__(self, preferences: Preferences):
        if not preferences.validate():
            raise SpotifyError("The preferences of your app are not correct")

        self.preferences: Preferences = preferences

    def build_authorization_url(self, show_dialog=True, state: str = None) -> str:
        """
        Builds the URL for the authorisation
        :param state: State of the authorization
        :param show_dialog: Is the dialog supposed to be shown
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
        url += "&state={state}" if state else ""
        return url

    def open_url_in_browser(self, show_dialogue=True) -> None:
        """
        Open the url in browser
        Only for testing purposes or the usage of this library in a desktop app
        :return: None
        """

        # Open url in a new window of the default browser, if possible
        webbrowser.open_new(self.build_authorization_url())
