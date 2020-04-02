"""
File with all the errors possible
"""


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

