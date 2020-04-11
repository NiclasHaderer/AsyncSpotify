"""
Playlist module
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (playlist.py) is part of AsyncSpotify which is released under MIT.                    #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Playlist(Endpoint):
    """
    Playlist endpoint
    """

    async def add_tracks(self, playlist_id: str, spotify_uris: List[str], auth_token: SpotifyAuthorisationToken = None,
                         **kwargs) -> None:
        """
        Add one or more tracks to a user’s playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/add-tracks-to-playlist/](https://developer.spotify.com/documentation/web-api/reference/playlists/add-tracks-to-playlist/)

        Args:
            spotify_uris: A list of spotify uris
            playlist_id: The id of the playlist
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        args: dict = {'playlist_id': playlist_id, 'uris': spotify_uris, }
        url, args = self._add_url_params(URLS.PLAYLIST.ADD_TRACKS, {**args, **kwargs})
        return await self.api_request_handler.make_request('POST', url, args, auth_token)

    async def change_details(self, playlist_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Change a playlist’s name and public/private state. (The user must, of course, own the playlist.)

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/change-playlist-details/](https://developer.spotify.com/documentation/web-api/reference/playlists/change-playlist-details/)

        Args:
            playlist_id: The id of the playlist
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.ONE, {'playlist_id': playlist_id})
        return await self.api_request_handler.make_request('POST', url, {}, auth_token, body=kwargs)

    async def create_playlist(self, user_id: str, playlist_name: str, auth_token: SpotifyAuthorisationToken = None,
                              **kwargs) -> None:
        """
        Change a playlist’s name and public/private state. (The user must, of course, own the playlist.)

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/create-playlist/](https://developer.spotify.com/documentation/web-api/reference/playlists/create-playlist/)

        Args:
            user_id: The id of the user
            playlist_name: THe name of the playlist
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.CREATE, {'user_id': user_id})
        return await self.api_request_handler.make_request('POST', url, {}, auth_token,
                                                           body={**{'name': playlist_name}, **kwargs})

    async def current_get_all(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get a list of the playlists owned or followed by the current Spotify user.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/get-a-list-of-current-users-playlists/](https://developer.spotify.com/documentation/web-api/reference/playlists/get-a-list-of-current-users-playlists/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            A List of Current User's Playlists
        """

        return await self.api_request_handler.make_request('GET', URLS.PLAYLIST.ME, kwargs, auth_token)

    async def user_get_all(self, user_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get a list of the playlists owned or followed by a Spotify user.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/get-list-users-playlists/](https://developer.spotify.com/documentation/web-api/reference/playlists/get-list-users-playlists/)

        Args:
            user_id: The id of the spotify user
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            A List of a User's Playlists
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.USER, {'user_id': user_id})
        return await self.api_request_handler.make_request('GET', url, kwargs, auth_token)

    async def get_one(self, playlist_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
       Get a playlist owned by a Spotify user.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/](https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist/)

        Args:
            playlist_id: The id of the Playlist
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            A Playlist
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.ONE, {'playlist_id': playlist_id})
        return await self.api_request_handler.make_request('GET', url, kwargs, auth_token)

    async def get_cover(self, playlist_id: str, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get the current image associated with a specific playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist-cover/](https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlist-cover/)

        Args:
            playlist_id: The id of the Playlist
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            The cover image
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.COVER, {'playlist_id': playlist_id})
        return await self.api_request_handler.make_request('GET', url, {}, auth_token)

    async def get_tracks(self, playlist_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get full details of the tracks or episodes of a playlist owned by a Spotify user.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/](https://developer.spotify.com/documentation/web-api/reference/playlists/get-playlists-tracks/)

        Args:
            playlist_id: The id of the Playlist
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            The cover image
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.TRACKS, {'playlist_id': playlist_id})
        return await self.api_request_handler.make_request('GET', url, {}, auth_token)

    # TODO
