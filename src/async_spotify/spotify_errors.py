"""
File with all the errors possible
"""


# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (spotify_errors.py) is part of AsyncSpotify which is released under MIT.              #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

class SpotifyBaseError(Exception):
    """
    The base Error for all spotify exceptions
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


class SpotifyError(SpotifyBaseError):
    """
    Custom error message
    """


class TokenExpired(SpotifyBaseError):
    """
    Custom token expired message
    """


class RateLimitExceeded(SpotifyBaseError):
    """
    Custom rate limit exceeded exception
    """


class SpotifyAPIError(SpotifyBaseError):
    """
    Custom api error message
    This exception gets throws if the spotify api returns an *non success* return code
    """


