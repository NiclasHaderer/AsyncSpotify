"""
Module with the albums endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (tracks.py) is part of AsyncSpotify which is released under MIT.                      #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Track(Endpoint):
    """
    Track endpoint
    """

    async def audio_analyze(self, track_id: str, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get a detailed audio analysis for a single track identified by its unique Spotify ID.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-analysis/)

        Args:
            track_id: The spotify track id
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            Detailed audio analysis for a single track
        """

        url, _ = self._add_url_params(URLS.TRACKS.ANALYZE, {'id': track_id})
        return await self.api_request_handler.make_request('GET', url, {}, auth_token)

    async def audio_features(self, track_id: str, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get audio feature information for a single track identified by its unique Spotify ID.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/](https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)

        Args:
            track_id: The spotify track id
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
             Audio feature information for a single track
        """

        url, _ = self._add_url_params(URLS.TRACKS.FEATURES, {'id': track_id})
        return await self.api_request_handler.make_request('GET', url, {}, auth_token)

    async def several_audio_features(self, track_id_list: List[str],
                                     auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get audio features for multiple tracks based on their Spotify IDs.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/](https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/)

        Args:
            track_id_list: A list of spotify ids
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
             Audio feature information for several track
        """

        return await self.api_request_handler.make_request(
            'GET', URLS.TRACKS.MULTI_FEATURES, {'ids': track_id_list}, auth_token)

    async def get_several(self, track_id_list: List[str], auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Spotify catalog information for multiple tracks based on their Spotify IDs.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/}(https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-tracks/)

        Args:
            track_id_list: A list of spotify ids
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            Information about several tracks
        """

        return await self.api_request_handler.make_request(
            'GET', URLS.TRACKS.SEVERAL, {**{'ids': track_id_list}, **kwargs}, auth_token)

    async def get_one(self, track_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get Spotify catalog information for a single track identified by its unique Spotify ID.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/](https://developer.spotify.com/documentation/web-api/reference/tracks/get-track/)

        Args:
            track_id: The spotify track id
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            Information about one track
        """

        url, _ = self._add_url_params(URLS.TRACKS.ONE, {'id': track_id})

        return await self.api_request_handler.make_request(
            'GET', url, kwargs, auth_token)
