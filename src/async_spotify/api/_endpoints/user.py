"""
Module with the user endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (user.py) is part of AsyncSpotify which is released under MIT.                        #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from async_spotify.api._endpoints.endpoint import Endpoint
from async_spotify.api._endpoints.urls import URLS
from async_spotify.authentification.spotify_authorization_token import SpotifyAuthorisationToken


class User(Endpoint):
    """
    User endpoint
    """

    async def me(self, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get detailed profile information about the current user (including the current user’s username).

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/users-profile/get-current-users-profile/](https://developer.spotify.com/documentation/web-api/reference/users-profile/get-current-users-profile/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            The Current User's Profile
        """

        return await self.api_request_handler.make_request('GET', URLS.USER.ME, {}, auth_token)

    async def get_one(self, user_id: str, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get detailed profile information about a user (including the current user’s username).

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/users-profile/get-users-profile/](https://developer.spotify.com/documentation/web-api/reference/users-profile/get-users-profile/)

        Args:
            user_id: The user’s Spotify user ID.
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            The Current User's Profile
        """

        url, _ = self._add_url_params(URLS.USER.USER, {'user_id': user_id})
        return await self.api_request_handler.make_request('GET', url, {}, auth_token)
