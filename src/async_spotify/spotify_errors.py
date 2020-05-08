"""
File with all the errors possible.
Every Exception inherits from SpotifyBaseError and therefor implements the `get_json` method. Which should be used
to get api response if a SpotifyAPIError is raised or should be used to get the other general error message
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (spotify_errors.py) is part of AsyncSpotify which is released under MIT.              #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import Dict


class SpotifyBaseError(Exception):
    """
    The base Error for all spotify exceptions
    """

    def __init__(self, message: dict):
        self.message: dict = message

    def __str__(self):
        return str(self.message)

    def get_json(self) -> Dict[str, Dict[str, str]]:
        """
        Get the the api response which was an error as dict
        {"error":{"status": 400, "message": "The reason"}}
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
