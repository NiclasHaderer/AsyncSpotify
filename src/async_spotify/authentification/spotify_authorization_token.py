"""
This file contains the Spotify AuthorisationToken
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (spotify_authorization_token.py) is part of AsyncSpotify which is released under MIT. #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import time


class SpotifyAuthorisationToken:
    """
    Class that has the Authorisation Token
    """

    def __init__(self, refresh_token: str = None, activation_time: int = None, access_token: str = None):
        """
        Generate a new authorisation token

        Args:
            refresh_token: The refresh token that was given to the application
            access_token: The token that will be used to make request
        """

        self.activation_time: int = activation_time
        self.refresh_token: str = refresh_token
        self.access_token: str = access_token

    def is_expired(self) -> bool:
        """
        Checks if the api token has expired

        Returns:
            Is the token expired
        """

        current_time: int = int(time.time())

        # Check if token is valid (3600 would be correct, but a bit of time padding is always nice)
        if current_time - self.activation_time > 3400:
            return True

        return False

    @property
    def valid(self) -> bool:
        """
        Validate that the token is not partially empty

        Returns:
            Is the token valid
        """

        if self.access_token and self.refresh_token and self.activation_time:
            return True
        return False

    def __eq__(self, other) -> bool:
        """
        Support for equal assertion

        Args:
            other: The other object the comparison is made to

        Returns:
            Is the content of the objects equal
        """
        return self.__dict__ == other.__dict__
