"""
Module with the playlists endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (playlist.py) is part of AsyncSpotify which is released under MIT.                    #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import base64
from typing import List, Dict, Any, Union

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Playlists(Endpoint):
    """
    Playlist endpoint
    """

    async def add_tracks(self, playlist_id: str, spotify_uris: List[str], position: int = None,
                         auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Add one or more tracks to a user’s playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/add-tracks-to-playlist/](https://developer.spotify.com/documentation/web-api/reference/playlists/add-tracks-to-playlist/)

        Args:
            position: The position to insert the items, a zero-based index. Appended if omitted
            spotify_uris: A list of spotify uris
            playlist_id: The id of the playlist
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        body = {
            'uris': spotify_uris
        }

        if position is not None:
            body['position'] = position

        url, _ = self._add_url_params(URLS.PLAYLIST.ADD_TRACKS, {'playlist_id': playlist_id})

        await self.api_request_handler.make_request('POST', url, {}, auth_token, body=body)

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
        await self.api_request_handler.make_request('PUT', url, {}, auth_token, body=kwargs)

    async def create_playlist(self, user_id: str, playlist_name: str, auth_token: SpotifyAuthorisationToken = None,
                              **kwargs) -> dict:
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

    async def get_user_all(self, user_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
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

        args = {**{'playlist_id': playlist_id}, **kwargs}
        url, args = self._add_url_params(URLS.PLAYLIST.TRACKS, args)
        return await self.api_request_handler.make_request('GET', url, args, auth_token)

    async def remove_tracks(self, playlist_id: str, spotify_uris: Dict[str, List[Dict[str, Any]]],
                            auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Remove one or more items from a user’s playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/remove-tracks-playlist/](https://developer.spotify.com/documentation/web-api/reference/playlists/remove-tracks-playlist/)

        Args:
            playlist_id: The id of the playlist
            spotify_uris: A dict with a list of spotify uris in the tracks key
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.ADD_TRACKS, {'playlist_id': playlist_id})

        await self.api_request_handler.make_request('DELETE', url, {}, auth_token, body=spotify_uris)

    async def reorder_tracks(self, playlist_id: str, position_dict: Dict[str, Union[int, str]], snapshot_id: str = None,
                             auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Reorder an item or a group of items in a playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/reorder-playlists-tracks/](https://developer.spotify.com/documentation/web-api/reference/playlists/reorder-playlists-tracks/)

        Args:
            playlist_id: The playlist id
            position_dict: The dict which reorders the tracks
            snapshot_id: The playlist’s snapshot ID against which you want to make the changes.
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            A json with the snapshot_id
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.TRACKS, {'playlist_id': playlist_id})

        body = position_dict
        if snapshot_id:
            body['snapshot_id'] = snapshot_id

        return await self.api_request_handler.make_request('PUT', url, {}, auth_token, body=body)

    async def replace_tracks(self, playlist_id: str, spotify_uris: List[str],
                             auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Replace all the items in a playlist, overwriting its existing items. This powerful request can be useful for
        replacing items, re-ordering existing items, or clearing the playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/replace-playlists-tracks/](https://developer.spotify.com/documentation/web-api/reference/playlists/replace-playlists-tracks/)

        Args:
            spotify_uris: A list of spotify uris
            playlist_id: The id of the playlist
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        body = {
            'uris': spotify_uris
        }

        url, _ = self._add_url_params(URLS.PLAYLIST.ADD_TRACKS, {'playlist_id': playlist_id})

        await self.api_request_handler.make_request('PUT', url, {}, auth_token, body=body)

    async def upload_cover(self, playlist_id: str, base_64_image: base64,
                           auth_token: SpotifyAuthorisationToken = None) -> None:

        """
        Replace the image used to represent a specific playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/playlists/upload-custom-playlist-cover/](https://developer.spotify.com/documentation/web-api/reference/playlists/upload-custom-playlist-cover/)

        Args:
            playlist_id: The id of the playlist
            base_64_image: Base64 encoded JPEG image data, maximum payload size is 256 KB
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        url, _ = self._add_url_params(URLS.PLAYLIST.COVER, {'playlist_id': playlist_id})
        await self.api_request_handler.make_request('PUT', url, {}, auth_token, base_64_image)
