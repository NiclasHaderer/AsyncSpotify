"""
File with useful objects
"""
from ..api_request_maker import ApiRequestHandler
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class DecoratorInformationObject:
    """
    A object which is used to pass information to the decorator
    """

    def __init__(self, arguments: dict, auth_token: SpotifyAuthorisationToken, request_maker: ApiRequestHandler):
        self.arguments: dict = arguments
        self.auth_token: SpotifyAuthorisationToken = auth_token
        self.request_maker: ApiRequestHandler = request_maker
