"""
Library module
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (library.py) is part of AsyncSpotify which is released under MIT.                     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Library(Endpoint):
    """
    Library endpoint
    """

    async def remove_album(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Remove Albums for Current User

        Args:
            album_id_list: The ids of the albums
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        return await self._remove(album_id_list, auth_token, URLS.LIBRARY.ALBUMS)

    async def remove_shows(self, show_id_list: List[str], auth_token: SpotifyAuthorisationToken = None,
                           **kwargs) -> None:
        """

        Args:
            show_id_list: The ids of the shows
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        return await self._remove(show_id_list, auth_token, URLS.LIBRARY.SHOWS, **kwargs)

    async def remove_tracks(self, track_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """

        Args:
            track_id_list: The ids of the tracks
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        return await self._remove(track_id_list, auth_token, URLS.LIBRARY.TRACKS)

    async def contains_album(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) \
            -> List[bool]:
        """

        Args:
            album_id_list: The ids of the albums
            auth_token: The auth token if you set the api class not to keep the token in memory
        """
        return await self._contains(album_id_list, auth_token, URLS.LIBRARY.CONTAINS_ALBUM)

    async def contains_show(self, show_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> List[bool]:
        """

        Args:
            show_id_list:
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        return await self._contains(show_id_list, auth_token, URLS.LIBRARY.CONTAINS_SHOWS)

    async def contains_track(self, track_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) \
            -> List[bool]:
        """

        Args:
            track_id_list:
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        return await self._contains(track_id_list, auth_token, URLS.LIBRARY.CONTAINS_TRACK)

    async def get_albums(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        return await self._get(auth_token, URLS.LIBRARY.ALBUMS, **kwargs)

    async def get_shows(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        return await self._get(auth_token, URLS.LIBRARY.SHOWS, **kwargs)

    async def get_tracks(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        return await self._get(auth_token, URLS.LIBRARY.TRACKS, **kwargs)

    async def add_album(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """

        Args:
            album_id_list: The ids of the albums
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        return await self._save(album_id_list, auth_token, URLS.LIBRARY.ALBUMS)

    async def add_shows(self, show_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """

        Args:
            show_id_list: The ids of the shows
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        return await self._save(show_id_list, auth_token, URLS.LIBRARY.SHOWS)

    async def add_tracks(self, track_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """

        Args:
            track_id_list: The ids of the tracks
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        return await self._save(track_id_list, auth_token, URLS.LIBRARY.TRACKS)

    async def _remove(self, ids: List[str], auth_token: SpotifyAuthorisationToken, url: str, **kwargs) -> None:
        return await self.api_request_handler.make_request('delete', url, {**{'ids': ids}, **kwargs}, auth_token)

    async def _contains(self, ids: List[str], auth_token: SpotifyAuthorisationToken, url: str) -> List[bool]:
        return await self.api_request_handler.make_request('get', url, {'ids': ids}, auth_token)

    async def _get(self, auth_token: SpotifyAuthorisationToken, url: str, **kwargs) -> dict:
        return await self.api_request_handler.make_request('get', url, {**kwargs}, auth_token)

    async def _save(self, ids: List[str], auth_token: SpotifyAuthorisationToken, url: str) -> None:
        return await self.api_request_handler.make_request('put', url, {**{'ids': ids}}, auth_token)
