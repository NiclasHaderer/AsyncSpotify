"""
Preferences for the spotify api
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (preferences.py) is part of AsyncSpotify which is released under MIT.                 #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import os
from os.path import join, abspath
from typing import List


class Preferences:
    """
    A Class with only the application information in it

    Notes:
        __Scopes available:__
        ```
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
        ```
    """

    def __init__(self, application_id: str = None, application_secret: str = None, scopes: List[str] = None,
                 redirect_url: str = None):
        """
        Create a new Spotify Preferences Object

        Args:
            application_id: The id of the application (Has to be set to use the object)
            application_secret: The secret of the application (Has to be set to use the object)
            scopes: The spotify scopes you app will request
            redirect_url: The redirect url spotify will referee the user after authentication
        """
        self.application_id: str = application_id
        self.application_secret: str = application_secret
        self.scopes: List[str] = scopes
        self.redirect_url: str = redirect_url

    def load_from_env(self) -> None:
        """
        Load the Preferences from the environment. The variable names have to be the same as the property name.

        Important:
            Scopes has to be a string separated by ' '
        """

        self.application_id = os.environ.get("application_id", self.application_id)
        self.application_secret = os.environ.get("application_secret", self.application_secret)
        self.redirect_url = os.environ.get("redirect_url", self.redirect_url)

        scopes = os.environ.get("scopes", self.scopes)
        self.scopes = scopes.split(" ") if scopes else self.scopes

    def load_from_docker_secret(self, base_dir: str = join(abspath(os.sep), 'var', 'run', 'secrets')) -> None:
        """
        Loads the Preferences from docker secret.
        The variable names have to be the same as the property name.

        Args:
            base_dir: The docker secrets base dir. Leave empty if you want to use the default

        Important:
            Scopes has to be a string separated by ' '
        """

        self.application_id = self._get_docker_secret('application_id', base_dir, self.application_id)
        self.application_secret = self._get_docker_secret('application_secret', base_dir, self.application_secret)
        self.redirect_url = self._get_docker_secret('redirect_url', base_dir, self.redirect_url)

        scopes = self._get_docker_secret('scopes', base_dir, self.scopes)
        self.scopes = scopes.split(" ") if scopes and not isinstance(scopes, list) else self.scopes

    def save_preferences_to_evn(self, ) -> None:
        """
        Takes the preferences saved in the object and saves them as os environment variables

        Notes:
            This will however not be permanent but only last for one session
        """

        if self.application_id:
            os.environ["application_id"] = self.application_id
        if self.application_secret:
            os.environ["application_secret"] = self.application_secret
        if self.scopes:
            os.environ["scopes"] = " ".join(self.scopes)
        if self.redirect_url:
            os.environ["redirect_url"] = self.redirect_url

    @property
    def valid(self) -> bool:
        """
        Validate if the preferences can be used. This will only check if the values of the preferences are not empty.

        Returns:
            Are the preferences valid
        """
        if self.application_id and self.application_secret and self.scopes and self.redirect_url:
            return True
        return False

    @staticmethod
    def _get_docker_secret(name: str, secrets_dir: str, default=None) -> str:
        """
        Read the docker secret and return it

        Args:
            name: The name of the docker secret
            secrets_dir: The directory where the secrets are stored
            default: The default value if no secret is found

        Returns:
            The docker secret
        """

        # try to read from secret file
        try:
            with open(os.path.join(secrets_dir, name), 'r') as secret_file:
                return secret_file.read().strip()
        except IOError:
            return default

    def __eq__(self, other) -> bool:
        """
        Support for equal assertion

        Args:
            other: The other object the comparison is made to

        Returns:
            Is the content of the objects equal
        """
        return self.__dict__ == other.__dict__
