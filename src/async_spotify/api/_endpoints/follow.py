"""
Module with the follow endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (follow.py) is part of AsyncSpotify which is released under MIT.                      #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Follow(Endpoint):
    """
    Class with the follow endpoint
    """

    async def check_follow(self, follow_type: str, id_list: List[str],
                           auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Check to see if the current user is following one or more artists or other Spotify users.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/follow/check-current-user-follows/](https://developer.spotify.com/documentation/web-api/reference/follow/check-current-user-follows/)

        Args:
            follow_type: The follow type (user or artist)
            id_list: A comma-separated list of the artist or the user Spotify IDs to check.
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            A bool value
        """

        required_args = {"type": follow_type, "ids": id_list}
        response = await self.api_request_handler.make_request('GET', URLS.FOLLOW.CONTAINS, required_args, auth_token)
        return response

    async def check_follow_playlist(self, playlist_id: str, spotify_user_id_list: List[str],
                                    auth_token: SpotifyAuthorisationToken = None) -> List[bool]:
        """
        Check to see if one or more Spotify users are following a specified playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/follow/check-user-following-playlist/](https://developer.spotify.com/documentation/web-api/reference/follow/check-user-following-playlist/)

        Args:
            playlist_id: The id of the playlist
            spotify_user_id_list: A comma-separated list of the artist or the user Spotify IDs to check.
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            A bool value
        """

        required_args = {"playlist_id": playlist_id, "ids": spotify_user_id_list}
        url, args = self._add_url_params(URLS.FOLLOW.CONTAINS_PLAYLIST, required_args)
        response = await self.api_request_handler.make_request('GET', url, args, auth_token)
        return response

    async def follow_artist_or_user(self, follow_type: str, spotify_user_id_list: List[str],
                                    auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Check to see if the current user is following one or more artists or other Spotify users.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/follow/follow-artists-users/](https://developer.spotify.com/documentation/web-api/reference/follow/follow-artists-users/)

        Args:
            follow_type: The follow type (user or artist)
            spotify_user_id_list: A comma-separated list of the artist or the user Spotify IDs
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            A bool value
        """

        required_args = {"type": follow_type, "ids": spotify_user_id_list}
        await self.api_request_handler.make_request('PUT', URLS.FOLLOW.HUMAN, required_args, auth_token)

    async def follow_playlist(self, playlist_id: str, public=True,
                              auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Add the current user as a follower of a playlist.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/follow/follow-playlist/](https://developer.spotify.com/documentation/web-api/reference/follow/follow-playlist/)

        Args:
            playlist_id: The playlist id
            public: Defaults to true. If true the playlist will be included in user’s public playlists, if false it will
                remain private.
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            A bool value
        """

        required_args = {'playlist_id': playlist_id}
        url, _ = self._add_url_params(URLS.FOLLOW.PLAYLIST, required_args)
        body: dict = {
            "public": public
        }

        await self.api_request_handler.make_request('PUT', url, {}, auth_token, body)

    async def get_followed_artist(self, follow_type: str = 'artist',
                                  auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get the current user’s followed artists.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/follow/get-followed/](https://developer.spotify.com/documentation/web-api/reference/follow/get-followed/)

        Args:
            follow_type: The ID type: currently artist
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            The followed artists
        """

        required_args = {'type': follow_type}
        args = {**required_args, **kwargs}

        url, args = self._add_url_params(URLS.FOLLOW.HUMAN, args)

        response = await self.api_request_handler.make_request('GET', url, args, auth_token)
        return response

    async def unfollow_artist_or_user(self, follow_type: str, spotify_user_id_list: List[str],
                                      auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Unfollow Artists or Users

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/follow/unfollow-artists-users/](https://developer.spotify.com/documentation/web-api/reference/follow/unfollow-artists-users/)

        Args:
            follow_type: The follow type (user or artist)
            spotify_user_id_list: A comma-separated list of the artist or the user Spotify IDs
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            A bool value
        """

        required_args = {"type": follow_type, "ids": spotify_user_id_list}
        await self.api_request_handler.make_request('DELETE', URLS.FOLLOW.HUMAN, required_args, auth_token)

    async def unfollow_playlist(self, playlist_id: str, auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Unfollow a Playlist

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/follow/unfollow-playlist/](https://developer.spotify.com/documentation/web-api/reference/follow/unfollow-playlist/)

        Args:
            playlist_id: The playlist id
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            A bool value
        """

        required_args = {"playlist_id": playlist_id}
        url, _ = self._add_url_params(URLS.FOLLOW.PLAYLIST, required_args)
        await self.api_request_handler.make_request('DELETE', url, required_args,
                                                    auth_token)
