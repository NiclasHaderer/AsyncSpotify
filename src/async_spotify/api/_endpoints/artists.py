"""
Module with the artists endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (artists.py) is part of AsyncSpotify which is released under MIT.                     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Artists(Endpoint):
    """
    Wraps the spotify artist endpoint
    """

    async def get_one(self, artist_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get an Artist

        Args:
            artist_id: The artist id
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/](https://developer.spotify.com/documentation/web-api/reference/artists/get-artist/)

        Returns:
            The artist
        """

        required_args = {"id": artist_id}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.ARTIST.ONE, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response

    async def get_album_list(self, artist_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Spotify catalog information about an artist’s albums.

        Args:
            artist_id: The artist id
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-albums/](https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-albums/)

        Returns:
            The artists albums
        """

        required_args = {"id": artist_id}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.ARTIST.ALBUM, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response

    async def get_top_tracks(self, artist_id: str, country: str, auth_token: SpotifyAuthorisationToken = None,
                             **kwargs) -> dict:
        """
        Get Spotify catalog information about an artist’s top tracks by country.

        Args:
            artist_id: The artist id
            country: The country of the top tracks
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/](https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/)

        Returns:
            The artists top tracks
        """

        required_args = {"id": artist_id, "country": country}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.ARTIST.TOP_TRACKS, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response

    async def get_similar(self, artist_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Spotify catalog information about artists similar to a given artist. Similarity is based on analysis of the
        Spotify community’s listening history.

        Args:
            artist_id: The artist id
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/](https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/)

        Returns:
            The artists top tracks
        """

        required_args = {"id": artist_id}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.ARTIST.SIMILAR_ARTISTS, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response

    async def get_several(self, artist_id_list: List[str], auth_token: SpotifyAuthorisationToken = None,
                          **kwargs) -> dict:
        """
        Get Spotify catalog information for several artists based on their Spotify IDs.

        Args:
            artist_id_list: The artist ids in a list
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/artists/get-several-artists/](https://developer.spotify.com/documentation/web-api/reference/artists/get-several-artists/)

        Returns:
            Several artists
        """

        required_args = {"ids": artist_id_list}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.ARTIST.SEVERAL, args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)

        return response
