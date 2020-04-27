"""
Module with the shows endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (shows.py) is part of AsyncSpotify which is released under MIT.                       #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Shows(Endpoint):
    """
    Shows endpoint
    """

    async def get_one(self, show_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Spotify catalog information for a single show identified by its unique Spotify ID.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/shows/get-a-show/](https://developer.spotify.com/documentation/web-api/reference/shows/get-a-show/)

        Args:
            show_id: The spotify id of the show
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            One show
        """

        url, _ = self._add_url_params(URLS.SHOWS.ONE, {'id': show_id})
        return await self.api_request_handler.make_request('GET', url, {**kwargs}, auth_token)

    async def get_several(self, show_id_list: List[str], auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Spotify catalog information for multiple shows based on their Spotify IDs.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/shows/get-several-shows/](https://developer.spotify.com/documentation/web-api/reference/shows/get-several-shows/)

        Args:
            show_id_list: A list of spotify ids
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            Multiple shows
        """

        return await self.api_request_handler.make_request(
            'GET', URLS.SHOWS.SEVERAL, {**{'ids': show_id_list}, **kwargs}, auth_token)

    async def get_episodes(self, show_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Spotify catalog information about an show’s episodes. Optional parameters can be used to limit the
        number of episodes returned.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/shows/get-shows-episodes/](https://developer.spotify.com/documentation/web-api/reference/shows/get-shows-episodes/9)

        Args:
            show_id: The spotify id of the show
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            A list of episodes
        """

        url, _ = self._add_url_params(URLS.SHOWS.EPISODES, {'id': show_id})

        return await self.api_request_handler.make_request(
            'GET', url, kwargs, auth_token)
