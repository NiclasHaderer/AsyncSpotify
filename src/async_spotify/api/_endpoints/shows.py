"""
Shows module
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (shows.py) is part of AsyncSpotify which is released under MIT.                       #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from async_spotify import SpotifyAuthorisationToken
from async_spotify.api._endpoints.endpoint import Endpoint
from async_spotify.api._endpoints.urls import URLS


class Show(Endpoint):
    """
    Shows endpoint
    """

    async def one(self, show_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs):
        """
        Get Spotify catalog information for a single show identified by its unique Spotify ID.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/upload-custom-playlist-cover/](https://developer.spotify.com/documentation/web-api/reference/playlists/upload-custom-playlist-cover/)

        Args:
            show_id: The spotify id of the show
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        url, _ = self._add_url_params(URLS.SHOWS.ONE, {'id': show_id})
        return await self.api_request_handler.make_request('GET', url, {**kwargs}, auth_token)

    async def several(self):
        pass

    async def episodes(self):
        pass
