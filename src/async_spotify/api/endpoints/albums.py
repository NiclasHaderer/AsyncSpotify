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

from .decorators import make_request
from .objects import DecoratorInformationObject
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Albums:
    """
    Wraps the spotify album functions
    """

    def __init__(self, api):  # :type async_spotify.API
        self.api = api  # :type async_spotify.API

    @make_request(method="GET", url=URLS.ALBUM.ONE)
    async def get_album(self, album_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs):
        """
        Get the album with the specific spotify album id

        Args:
            album_id: The album id of the album you want to get
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Note:
            https://developer.spotify.com/documentation/web-api/reference/albums/get-album/

        Returns:
            The album json
        """

        required_args = {"id": album_id}
        args = {**required_args, **kwargs}
        return DecoratorInformationObject(args, auth_token, self.api.api_request_handler)

    @make_request(method="GET", url=URLS.ALBUM.TRACKS)
    async def get_album_tracks(self, album_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs):
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
        return DecoratorInformationObject(args, auth_token, self.api.api_request_handler)

    @make_request(method="GET", url=URLS.ALBUM.MULTIPLE)
    async def get_multiple_albums(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None,
                                  **kwargs):
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
        return DecoratorInformationObject(args, auth_token, self.api.api_request_handler)
