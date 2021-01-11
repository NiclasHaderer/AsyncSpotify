"""
Test the player endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_player.py) is part of AsyncSpotify which is released under MIT.                 #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient
from async_spotify.spotify_errors import SpotifyAPIError


class TestPlayer:

    @pytest.mark.asyncio
    async def test_get_devices(self, prepared_api: SpotifyApiClient):
        response: dict = await prepared_api.player.get_devices()
        assert isinstance(response, dict)

    @pytest.mark.asyncio
    async def test_get_queue(self, prepared_api: SpotifyApiClient):
        response: dict = await prepared_api.player.get_queue()
        assert isinstance(response, dict)

    @pytest.mark.asyncio
    async def test_recent_tracks(self, prepared_api: SpotifyApiClient):
        response: dict = await prepared_api.player.get_recent_tracks()
        assert isinstance(response, dict)

    @pytest.mark.asyncio
    async def test_add_to_queue(self, prepared_api: SpotifyApiClient):
        try:
            await prepared_api.player.add_to_queue('spotify:track:4iV5W9uYEdYUVa79Axb7Rh')
            response: None = await prepared_api.player.add_to_queue('spotify:track:3RauEVgRgj1IuWdJ9fDs70')
        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404
            return

        assert not response

    @pytest.mark.asyncio
    async def test_add_multiple_to_queue(self, prepared_api: SpotifyApiClient):
        try:
            await prepared_api.player.add_multiple_to_queue(
                ['spotify:track:4iV5W9uYEdYUVa79Axb7Rh',
                 'spotify:track:4iV5W9uYEdYUVa79Axb7Rh',
                 'spotify:track:4iV5W9uYEdYUVa79Axb7Rh',
                 'spotify:track:4iV5W9uYEdYUVa79Axb7Rh'])
            response: None = await prepared_api.player.add_multiple_to_queue(
                ['spotify:track:3RauEVgRgj1IuWdJ9fDs70',
                 'spotify:track:3RauEVgRgj1IuWdJ9fDs70',
                 'spotify:track:3RauEVgRgj1IuWdJ9fDs70'])
        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404
            return

        assert not response

    @pytest.mark.asyncio
    async def test_current_track(self, prepared_api: SpotifyApiClient):
        response: dict = await prepared_api.player.get_current_track()
        assert isinstance(response, dict)

    @pytest.mark.asyncio
    async def test_play_pause(self, prepared_api: SpotifyApiClient):
        try:
            play = await prepared_api.player.play()
            pause = await prepared_api.player.pause()
        except SpotifyAPIError:
            try:
                pause = await prepared_api.player.pause()
                play = await prepared_api.player.play()
            except SpotifyAPIError as e:
                error = e.get_json()
                assert error['error']['status'] == 404 or error['error']['status'] == 500
                return

        assert pause is None and play is None

    @pytest.mark.asyncio
    async def test_seek(self, prepared_api: SpotifyApiClient):
        try:
            seek = await prepared_api.player.seek(5000)
            assert seek is None
        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404

    @pytest.mark.asyncio
    async def test_repeat(self, prepared_api: SpotifyApiClient):
        try:
            t = await prepared_api.player.repeat('track')
            c = await prepared_api.player.repeat('context')
            o = await prepared_api.player.repeat('off')
            assert t is None and c is None and o is None
        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404

    @pytest.mark.asyncio
    async def test_volume(self, prepared_api: SpotifyApiClient):
        try:
            t = await prepared_api.player.volume(50)
            assert t is None

        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404 or error['error']['status'] == 403

    @pytest.mark.asyncio
    async def test_next(self, prepared_api: SpotifyApiClient):
        try:
            t = await prepared_api.player.next()
            assert t is None
        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404

    @pytest.mark.asyncio
    async def test_previous(self, prepared_api: SpotifyApiClient):
        try:
            t = await prepared_api.player.previous()
            assert t is None
        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404

    @pytest.mark.asyncio
    async def test_shuffle(self, prepared_api: SpotifyApiClient):
        try:
            s = await prepared_api.player.shuffle(True)
            n = await prepared_api.player.shuffle(False)
            assert s is None and n is None
        except SpotifyAPIError as e:
            error = e.get_json()
            assert error['error']['status'] == 404

    @pytest.mark.asyncio
    async def test_transfer(self, prepared_api: SpotifyApiClient):
        devices: dict = await prepared_api.player.get_devices()

        try:
            device_id = devices['devices'][0]['id']
        except (KeyError, IndexError):

            try:
                await prepared_api.player.transfer(['invalid_device_id'], True)
            except SpotifyAPIError:
                pass

            assert True
            return

        response = await prepared_api.player.transfer([device_id], True)
        assert response is None
