"""
AuthorizationCodeFlow for the spotify api
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (authorization_code_flow.py) is part of AsyncSpotify which is released under MIT.     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import os
from os.path import join, abspath
from typing import List

from .authorization_flow import AuthorizationFlow


class AuthorizationCodeFlow(AuthorizationFlow):
    """
    A Class with the necessary information for the Authorization Code Flow in it

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
        Create a new Spotify AuthorizationCodeFlow Object

        Args:
            application_id: The id of the application
            application_secret: The secret of the application
            scopes: The spotify scopes you app will request
            redirect_url: The redirect url spotify will redirect the user after authentication
        """

        self.application_id: str = application_id
        self.application_secret: str = application_secret
        self.scopes: List[str] = scopes
        self.redirect_url: str = redirect_url

    def load_from_env(self) -> None:
        """
        Load the AuthorizationCodeFlow from the environment.
        The variable names have to be the same as the property name.

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
        Loads the AuthorizationCodeFlow from docker secret.
        The variable names have to be the same as the property name.

        Args:
            base_dir: The docker secrets base dir. Leave empty if you want to use the default

        Important:
            Scopes has to be a string separated by ' '
        """

        self.application_id = AuthorizationFlow._get_docker_secret('application_id', base_dir, self.application_id)
        self.application_secret = AuthorizationFlow._get_docker_secret('application_secret', base_dir,
                                                                       self.application_secret)
        self.redirect_url = AuthorizationFlow._get_docker_secret('redirect_url', base_dir, self.redirect_url)

        scopes = AuthorizationFlow._get_docker_secret('scopes', base_dir, self.scopes)
        self.scopes = scopes.split(" ") if scopes and not isinstance(scopes, list) else self.scopes

    def save_to_evn(self) -> None:
        """
        Takes the auth_code_flow saved in the object and saves them as os environment variables

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
        Validate if the auth_code_flow can be used. This will only check if the values of the auth_code_flow are not empty.

        Returns:
            Are the auth_code_flow valid
        """
        if self.application_id and self.application_secret and self.redirect_url and self.scopes:
            return True
        return False
