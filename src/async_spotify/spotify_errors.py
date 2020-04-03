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


class SpotifyAuthError(Exception):
    """
    Custom auth error message
    """


class TokenExpired(Exception):
    """
    Custom token expired message
    """


class RateLimitExceeded(Exception):
    """
    Custom rate limit exceeded exception
    """
