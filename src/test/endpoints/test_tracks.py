"""
Test tracks endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (test_tracks.py) is part of AsyncSpotify which is released under MIT.                 #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient


class TestShow:

    @pytest.mark.asyncio
    async def test_analyze(self, prepared_api: SpotifyApiClient):
        track = await prepared_api.track.audio_analyze('7FIWs0pqAYbP91WWM0vlTQ')
        assert isinstance(track, dict)

    @pytest.mark.asyncio
    async def test_features(self, prepared_api: SpotifyApiClient):
        track = await prepared_api.track.audio_features('7FIWs0pqAYbP91WWM0vlTQ')
        assert isinstance(track, dict)

    @pytest.mark.asyncio
    async def test_several_features(self, prepared_api: SpotifyApiClient):
        track = await prepared_api.track.several_audio_features(['7FIWs0pqAYbP91WWM0vlTQ', '7lQ8MOhq6IN2w8EYcFNSUk'])
        assert isinstance(track, dict)

    @pytest.mark.asyncio
    async def test_several(self, prepared_api: SpotifyApiClient):
        track = await prepared_api.track.get_several(['7FIWs0pqAYbP91WWM0vlTQ', '7lQ8MOhq6IN2w8EYcFNSUk'])
        assert isinstance(track, dict)

    @pytest.mark.asyncio
    async def test_one(self, prepared_api: SpotifyApiClient):
        track = await prepared_api.track.get_one('7FIWs0pqAYbP91WWM0vlTQ')
        assert isinstance(track, dict)
