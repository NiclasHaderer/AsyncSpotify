"""
Handle the requests to the albums endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (albums.py) is part of AsyncSpotify which is released under MIT.                      #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken
from ...typing import TAlbum, TAlbums, TTracks


class Albums(Endpoint):
    """
    Wraps the spotify album functions
    """

    async def get_one(self, album_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> TAlbum:
        """
        Get the album with the specific spotify album id

        Args:
            album_id: The album id of the album you want to get
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Note:
            [https://developer.spotify.com/documentation/web-api/reference/albums/get-album/](https://developer.spotify.com/documentation/web-api/reference/albums/get-album/)

        Returns:
            The album json
        """

        required_args = {"id": album_id}
        args = {**required_args, **kwargs}

        url, args = self.add_url_params(URLS.ALBUM.ONE, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return TAlbum(**response)

    async def get_tracks(self, album_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> TTracks:
        """
        Get the tracks of an album

        Args:
            album_id: The id of the album
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Note:
            https://developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/

        Returns:
            The tracks of an album
        """

        required_args = {"id": album_id}
        args = {**required_args, **kwargs}

        url, args = self.add_url_params(URLS.ALBUM.TRACKS, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return TTracks(**response)

    async def get_multiple(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None,
                           **kwargs) -> TAlbums:
        """
        Get All the albums specified in the album_id_list

        Args:
            album_id_list: The list of the spotify album ids
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Note:
            https://developer.spotify.com/documentation/web-api/reference/albums/get-several-albums/

        Returns:
            All the albums you queried
        """

        required_args = {"ids": album_id_list}
        args = {**required_args, **kwargs}

        url, args = self.add_url_params(URLS.ALBUM.MULTIPLE, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return TAlbums(**response)
