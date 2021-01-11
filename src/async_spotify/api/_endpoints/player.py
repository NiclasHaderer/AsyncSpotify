"""
Module with the player endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (player.py) is part of AsyncSpotify which is released under MIT.                      #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
from typing import List

from .endpoint import Endpoint
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Player(Endpoint):
    """
    Player endpoint
    """

    async def get_devices(self, auth_token: SpotifyAuthorisationToken = None) -> dict:
        """
        Get information about a user’s available devices.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/get-a-users-available-devices/](https://developer.spotify.com/documentation/web-api/reference/player/get-a-users-available-devices/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory

        Returns:
            The available devices
        """

        return await self.api_request_handler.make_request('GET', URLS.PLAYER.DEVICES, {}, auth_token)

    async def get_queue(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get information about the user’s current playback state, including track or episode, progress,
        and active device.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/get-information-about-the-users-current-playback/](https://developer.spotify.com/documentation/web-api/reference/player/get-information-about-the-users-current-playback/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            The top tracks and artists
        """

        return await self.api_request_handler.make_request('GET', URLS.PLAYER.PLAYER, kwargs, auth_token)

    async def add_to_queue(self, spotify_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Add an item to the end of the user’s current playback queue

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/add-to-queue/](https://developer.spotify.com/documentation/web-api/reference/player/add-to-queue/)

        Args:
            spotify_id: A spotify id of an item
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        args: dict = {
            'uri': spotify_id,
            **kwargs
        }

        await self.api_request_handler.make_request('POST', URLS.PLAYER.QUEUE, args, auth_token)

    async def add_multiple_to_queue(self, spotify_id_list: List[str],
                                    auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Add items to the end of the user’s current playback queue

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/add-to-queue/](https://developer.spotify.com/documentation/web-api/reference/player/add-to-queue/)

        Args:
            spotify_id_list: A spotify id list of an item
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        for spotify_id in spotify_id_list:
            args: dict = {
                'uri': spotify_id,
                **kwargs
            }

            await self.api_request_handler.make_request('POST', URLS.PLAYER.QUEUE, args, auth_token)

    async def get_recent_tracks(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get the Current User's Recently Played Tracks

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/](https://developer.spotify.com/documentation/web-api/reference/player/get-recently-played/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            The recent tracks
        """

        return await self.api_request_handler.make_request('GET', URLS.PLAYER.RECENTLY, kwargs, auth_token)

    async def get_current_track(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get the User's Currently Playing Track

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/get-the-users-currently-playing-track/](https://developer.spotify.com/documentation/web-api/reference/player/get-the-users-currently-playing-track/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args

        Returns:
            The current track
        """

        return await self.api_request_handler.make_request('GET', URLS.PLAYER.PLAYING, kwargs, auth_token)

    async def pause(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Pause playback on the user’s account

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/pause-a-users-playback/](https://developer.spotify.com/documentation/web-api/reference/player/pause-a-users-playback/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        await self.api_request_handler.make_request('PUT', URLS.PLAYER.PAUSE, kwargs, auth_token)

    async def seek(self, position_ms: int, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Pause playback on the user’s account

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/seek-to-position-in-currently-playing-track/](https://developer.spotify.com/documentation/web-api/reference/player/seek-to-position-in-currently-playing-track/)

        Args:
            position_ms: The position in milliseconds to seek to. Must be a positive number. Passing in a position that
                is greater than the length of the track will cause the player to start playing the next song.
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        args = {**{'position_ms': position_ms}, **kwargs}
        await self.api_request_handler.make_request('PUT', URLS.PLAYER.SEEK, args, auth_token)

    async def repeat(self, state: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Set the repeat mode for the user’s playback. Options are repeat-track, repeat-context, and off.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/set-repeat-mode-on-users-playback/](https://developer.spotify.com/documentation/web-api/reference/player/set-repeat-mode-on-users-playback/)

        Args:
            state: track, context or off.
                track will repeat the current track.
                context will repeat the current context.
                off will turn repeat off.
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        args = {**{'state': state}, **kwargs}
        await self.api_request_handler.make_request('PUT', URLS.PLAYER.REPEAT, args, auth_token)

    async def volume(self, volume_percent: int, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Set the volume for the user’s current playback device.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/set-volume-for-users-playback/](https://developer.spotify.com/documentation/web-api/reference/player/set-volume-for-users-playback/)

        Args:
            volume_percent: Integer. The volume to set. Must be a value from 0 to 100 inclusive.
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        args = {**{'volume_percent': volume_percent}, **kwargs}
        await self.api_request_handler.make_request('PUT', URLS.PLAYER.VOLUME, args, auth_token)

    async def next(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Set the volume for the user’s current playback device.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/skip-users-playback-to-next-track/](https://developer.spotify.com/documentation/web-api/reference/player/skip-users-playback-to-next-track/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        await self.api_request_handler.make_request('POST', URLS.PLAYER.NEXT, kwargs, auth_token)

    async def previous(self, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Skips to previous track in the user’s queue.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/skip-users-playback-to-previous-track/](https://developer.spotify.com/documentation/web-api/reference/player/skip-users-playback-to-previous-track/)

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        await self.api_request_handler.make_request('POST', URLS.PLAYER.PREVIOUS, kwargs, auth_token)

    async def play(self, device_id: str = None, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Start a new context or resume current playback on the user’s active device.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/start-a-users-playback/](https://developer.spotify.com/documentation/web-api/reference/player/start-a-users-playback/)

        Args:
            device_id: A single device ID
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        await self.api_request_handler.make_request('PUT', URLS.PLAYER.PLAY, {'device_id': device_id}, auth_token,
                                                    kwargs)

    async def shuffle(self, shuffle_on: bool, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> None:
        """
        Toggle shuffle on or off for user’s playback.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/toggle-shuffle-for-users-playback/](https://developer.spotify.com/documentation/web-api/reference/player/toggle-shuffle-for-users-playback/)

        Args:
            shuffle_on: The state of the shuffle
            auth_token: The auth token if you set the api class not to keep the token in memory
            kwargs: Optional arguments as keyword args
        """

        args = {**{'state': shuffle_on}, **kwargs}

        await self.api_request_handler.make_request('PUT', URLS.PLAYER.SHUFFLE, args, auth_token)

    async def transfer(self, device_id: List[str], play: bool = False,
                       auth_token: SpotifyAuthorisationToken = None) -> None:
        """
        Transfer playback to a new device and determine if it should start playing.

        Notes:
            [https://developer.spotify.com/documentation/web-api/reference/player/transfer-a-users-playback/](https://developer.spotify.com/documentation/web-api/reference/player/transfer-a-users-playback/)

        Args:
            play: ensure playback happens on new device
            device_id: A SINGLE device ID
            auth_token: The auth token if you set the api class not to keep the token in memory
        """

        body = {
            "device_ids": device_id,
            "state": play
        }

        await self.api_request_handler.make_request('PUT', URLS.PLAYER.PLAYER, {}, auth_token, body=body)
