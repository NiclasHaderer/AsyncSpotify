"""
File with all the errors possible
"""


class SpotifyError(Exception):
    """
    Custom error message
    """
    pass


class SpotifyAuthError(Exception):
    """
    Custom auth error message
    """
    pass


class TokenExpired(Exception):
    """
    Custom token expired message
    """
    pass


class RageLimitExceeded(Exception):
    """
    Custom rate limit exceeded exception
    """
    pass
