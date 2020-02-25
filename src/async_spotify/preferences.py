"""
Preferences for the spotify api
"""

import os
from typing import List

"""
Scopes available:
ugc-image-upload 
user-read-playback-state 
user-read-email 
playlist-read-collaborative 
user-modify-playback-state 
user-read-private 
playlist-modify-public 
user-library-modify 
user-top-read 
user-read-currently-playing 
playlist-read-private 
user-follow-read app-remote-control 
user-read-recently-played 
playlist-modify-private 
user-follow-modify 
user-library-read
"""


class Preferences:
    """
    A Class with only the application information in it
    """

    def __init__(self, application_id: str = None, application_secret: str = None, scopes: List[str] = None,
                 redirect_url: str = None):
        """
        Create a new Spotify Preferences Object
        :param application_id: The id of the application (Has to be set to use the object)
        :param application_secret: The secret of the application (Has to be set to use the object)
        :param scopes: The spotify scopes you app will request
        :param redirect_url: The redirect url spotify will referee the user after authentication
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
        self.application_id = os.environ.get("application_id", self.application_id)
        self.application_secret = os.environ.get("application_secret", self.application_secret)
        self.redirect_url = os.environ.get("redirect_url", self.redirect_url)

        scopes = os.environ.get("scopes", self.scopes)
        self.scopes = scopes.split(" ") if scopes else self.scopes

    def load_from_docker_secret(self) -> None:
        """
        Loads the Preferences from docker secret.
        The variable names have to be the same as the property name.
        Scopes has to be a string separated by ' '
        :return: None
        """
        self.application_id = self._get_docker_secret('application_id', self.application_id)
        self.application_secret = self._get_docker_secret('application_secret', self.application_secret)
        self.redirect_url = self._get_docker_secret('redirect_url', self.redirect_url)

        scopes = self._get_docker_secret('scopes', self.scopes)
        self.scopes = scopes.split(" ") if scopes and not isinstance(scopes, list) else self.scopes

    def save_preferences_to_evn(self) -> None:
        """
        Takes the preferences saved in the object and saves them as os environment variables
        :return: None
        """
        if self.application_id:
            os.environ["application_id"] = self.application_id
        if self.application_secret:
            os.environ["application_secret"] = self.application_secret
        if self.scopes:
            os.environ["scopes"] = " ".join(self.scopes)
        if self.redirect_url:
            os.environ["redirect_url"] = self.redirect_url

    def validate(self) -> bool:
        """
        Validate if the preferences can be used
        :return: Are the preferences valid
        """
        if self.application_id and self.application_secret and self.scopes and self.redirect_url:
            return True
        return False

    @staticmethod
    def _get_docker_secret(name: str, default=None,
                           secrets_dir=os.path.join(os.path.abspath(os.sep), 'var', 'run', 'secrets')) -> str:
        """
        Read the docker secret and return it
        :param name: The name of the docker secret
        :param default: The default value if no secret is found
        :param secrets_dir: The directory where the secrets are stored
        :returns: The docker secret
        """

        # try to read from secret file
        try:
            with open(os.path.join(secrets_dir, name), 'r') as secret_file:
                return secret_file.read().strip()
        except IOError as _:
            return default

    def __eq__(self, other):
        """
        Support for equal assertion
        :param other: The other object the comparison is made to
        :return: Is the content of the objects equal
        """
        return self.__dict__ == other.__dict__
