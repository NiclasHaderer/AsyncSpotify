"""
File with all the errors possible
"""


# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (spotify_errors.py) is part of AsyncSpotify which is released under MIT.              #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

class SpotifyError(Exception):
    """
    Custom error message
    """


class TokenExpired(Exception):
    """
    Custom token expired message
    """


class RateLimitExceeded(Exception):
    """
    Custom rate limit exceeded exception
    """


class SpotifyAPIError(Exception):
    """
    Custom api error message
    This exception gets throws if the spotify api returns an *non success* return code
    """

    def __init__(self, message: dict):
        self.message: dict = message

    def __str__(self):
        return str(self.message)

    def get_json(self) -> dict:
        """
        Get the the api response which was an error as dict
        """
        return self.message


try:
    raise SpotifyAPIError({'a': 'b'})
except SpotifyAPIError as e:
    e.get_json()
    str(e)
