"""
Module with the personalization endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (personalization.py) is part of AsyncSpotify which is released under MIT.             #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################


from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Personalization(Endpoint):
    """
    Personalization endpoint
    """

    async def get_top(self, content_type: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get the current user’s top artists or tracks based on calculated affinity.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/](https://developer.spotify.com/documentation/web-api/reference/personalization/get-users-top-artists-and-tracks/)

        Args:
            content_type: Do you want to have the top `artists` or `tracks`
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            The top tracks and artists
        """

        url, _ = self._add_url_params(URLS.PERSONALIZATION.TOP, {'type': content_type})
        return await self.api_request_handler.make_request('GET', url, kwargs, auth_token)
