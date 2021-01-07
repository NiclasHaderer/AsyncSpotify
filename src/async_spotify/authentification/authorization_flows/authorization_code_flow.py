# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (authorization_code_flow.py) is part of AsyncSpotify which is released under MIT.     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import List

from .authorization_flow import AuthorizationFlow


class AuthorizationCodeFlow(AuthorizationFlow):
    """
    A Class which implements the authorization flow

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

    @property
    def valid(self) -> bool:
        """
        Validate if the auth_code_flow can be used. This will only check if the values of the auth_code_flow are not
        empty.

        Returns:
            Are the auth_code_flow valid
        """
        if self.application_id and self.application_secret and self.redirect_url:
            return True
        return False
