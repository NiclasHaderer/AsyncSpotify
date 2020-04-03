"""
File with useful objects
"""
# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (objects.py) is part of AsyncSpotify which is released under MIT.                     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################


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
