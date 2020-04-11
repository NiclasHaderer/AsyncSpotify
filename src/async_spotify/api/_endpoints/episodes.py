"""
Module with the episodes endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (episodes.py) is part of AsyncSpotify which is released under MIT.                    #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Episodes(Endpoint):
    """
    Class with the episodes endpoint
    """

    async def get_one(self, episode_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get an Episode

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/episodes/get-an-episode/](https://developer.spotify.com/documentation/web-api/reference/episodes/get-an-episode/)

        Args:
            episode_id: The id of the episode
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            A episode
        """

        required_args = {"id": episode_id}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.EPISODES.ONE, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response

    async def get_multiple(self, episode_ids: List[str], auth_token: SpotifyAuthorisationToken = None,
                           **kwargs) -> dict:
        """
        Get Several Episodes

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/episodes/get-several-episodes/](https://developer.spotify.com/documentation/web-api/reference/episodes/get-several-episodes/)

        Args:
            episode_ids: A list of episode ids
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            A list of episodes
        """

        required_args = {"ids": episode_ids}
        args = {**required_args, **kwargs}
        response = await self.api_request_handler.make_request('GET', URLS.EPISODES.MULTIPLE, args, auth_token)

        return response
