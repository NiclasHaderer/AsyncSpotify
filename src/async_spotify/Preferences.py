import os
from typing import List


class Preferences:
    """
    A Class with only the application information in it
    """

    def __init__(self, application_id: str = None, application_secret: str = None, scopes: List[str] = None,
                 redirect_url: str = None, state: str = None):
        """
        Create a new Spotify Preferences Object
        @param application_id: The id of the application (Has to be set to use the object)
        @param application_secret: The secret of the application (Has to be set to use the object)
        @param scopes: The spotify scopes you app will request
        @param redirect_url: The redirect url spotify will referee the user after authentication
        """
        self.application_id: str = application_id
        self.application_secret: str = application_secret
        self.scopes: List[str] = scopes
        self.redirect_url: str = redirect_url

    def load_from_env(self) -> None:
        """
        Load the Preferences from the environment.
        The variable names have to be the same as the property name.
        Scopes has to be a string separated by ' '
        :return: None
        """
        self.application_id = os.environ.get("application_id")
        self.application_secret = os.environ.get("application_secret")
        self.scopes = os.environ.get("scopes").split(" ")
        self.redirect_url = os.environ.get("redirect_url")

    def validate(self) -> bool:
        """
        Validate if the preferences can be used
        @return: Are the preferences valid
        """
        if self.application_id and self.application_secret and self.scopes and self.redirect_url:
            return True
        return False
