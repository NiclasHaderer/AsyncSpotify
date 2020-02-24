"""
This file contains the Spotify AuthorisationToken
"""

import time


class SpotifyAuthorisationToken:
    """
    Class that has the Authorisation Token
    """

    def __init__(self, refresh_token: str, activation_time: int, access_token: str = None):
        """
        Generate a new authorisation token
        :param refresh_token: The refresh token that was given to the application
        :param access_token: The token that will be used to make request
        """
        self.activation_time: int = activation_time
        self.refresh_token: str = refresh_token
        self.access_token: str = access_token

    def is_expired(self) -> bool:
        """
        Checks if the api token has expired
        :return: bool
        """
        current_time: int = int(time.time())

        # Check if token is valid (3600 would be correct, but a bit of time padding is always nice)
        if current_time - self.activation_time > 3400:
            return True

        return False
