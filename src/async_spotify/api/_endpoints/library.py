"""
Module with the library endpoint
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

    async def contains_albums(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) \
            -> List[bool]:
        """
        Check Current User's Saved Albums

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/check-users-saved-albums/](https://developer.spotify.com/documentation/web-api/reference/library/check-users-saved-albums/)

        Args:
            album_id_list: The ids of the albums
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            Does the user library contain the Album
        """

        return await self.api_request_handler.make_request('GET', URLS.LIBRARY.CONTAINS_ALBUM,
                                                           {'ids': album_id_list}, auth_token)

    async def contains_shows(self, show_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> List[bool]:
        """
        Check Current User's Saved Shows

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/check-users-saved-shows/](https://developer.spotify.com/documentation/web-api/reference/library/check-users-saved-shows/)

        Args:
            show_id_list:
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            Does the user library contain the Show
        """

        return await self.api_request_handler.make_request('GET', URLS.LIBRARY.CONTAINS_SHOWS,
                                                           {'ids': show_id_list}, auth_token)

    async def contains_tracks(self, track_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) \
            -> List[bool]:
        """
        Check Current User's Saved Tracks

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/check-users-saved-tracks/](https://developer.spotify.com/documentation/web-api/reference/library/check-users-saved-tracks/)

        Args:
            track_id_list:
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            Does the user library contain the Track
        """

        return await self.api_request_handler.make_request('GET', URLS.LIBRARY.CONTAINS_TRACK,
                                                           {'ids': track_id_list}, auth_token)

    async def get_albums(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Check User's Saved Albums

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-albums/](https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-albums/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        return await self.api_request_handler.make_request('GET', URLS.LIBRARY.ALBUMS, kwargs, auth_token)

    async def get_shows(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Check User's Saved Shows

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-shows/](https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-shows/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        return await self.api_request_handler.make_request('GET', URLS.LIBRARY.SHOWS, kwargs, auth_token)

    async def get_tracks(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Check User's Saved Tracks

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-tracks/](https://developer.spotify.com/documentation/web-api/reference/library/get-users-saved-tracks/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        return await self.api_request_handler.make_request('GET', URLS.LIBRARY.TRACKS, kwargs, auth_token)

    async def remove_albums(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Remove Albums for Current User

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/remove-albums-user/](https://developer.spotify.com/documentation/web-api/reference/library/remove-albums-user/)

        Args:
            album_id_list: The ids of the albums
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        await self.api_request_handler.make_request('DELETE', URLS.LIBRARY.ALBUMS,
                                                    {'ids': album_id_list}, auth_token)

    async def remove_shows(self, show_id_list: List[str], auth_token: SpotifyAuthorisationToken = None,
                           **kwargs) -> None:
        """
        Remove Shows for Current User

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/remove-shows-user/](https://developer.spotify.com/documentation/web-api/reference/library/remove-shows-user/)

        Args:
            show_id_list: The ids of the shows
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        await self.api_request_handler.make_request('DELETE', URLS.LIBRARY.SHOWS,
                                                    {**{'ids': show_id_list}, **kwargs}, auth_token)

    async def remove_tracks(self, track_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Remove Tracks for Current User

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/remove-tracks-user/](https://developer.spotify.com/documentation/web-api/reference/library/remove-tracks-user/)

        Args:
            track_id_list: The ids of the tracks
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        await self.api_request_handler.make_request('DELETE', URLS.LIBRARY.TRACKS,
                                                    {'ids': track_id_list}, auth_token)

    async def add_album(self, album_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Get User's Saved Albums

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/save-albums-user/](https://developer.spotify.com/documentation/web-api/reference/library/save-albums-user/)

        Args:
            album_id_list: The ids of the albums
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        await self.api_request_handler.make_request('PUT', URLS.LIBRARY.ALBUMS,
                                                    {**{'ids': album_id_list}}, auth_token)

    async def add_shows(self, show_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Get User's Saved Shows

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/save-shows-user/](https://developer.spotify.com/documentation/web-api/reference/library/save-shows-user/)

        Args:
            show_id_list: The ids of the shows
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        await self.api_request_handler.make_request('PUT', URLS.LIBRARY.SHOWS,
                                                    {**{'ids': show_id_list}}, auth_token)

    async def add_tracks(self, track_id_list: List[str], auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Get User's Saved Tracks

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/library/save-tracks-user/](https://developer.spotify.com/documentation/web-api/reference/library/save-tracks-user/)

        Args:
            track_id_list: The ids of the tracks
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        await self.api_request_handler.make_request('PUT', URLS.LIBRARY.TRACKS,
                                                    {**{'ids': track_id_list}}, auth_token)
