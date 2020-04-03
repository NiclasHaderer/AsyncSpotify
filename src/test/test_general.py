"""
Test the album endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_general.py) is part of AsyncSpotify which is released under MIT.                #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import asyncio

import pytest

from async_spotify import API, SpotifyError
from async_spotify.spotify_errors import RateLimitExceeded
from helpers import SetupServer


class TestGeneral(SetupServer):

    @pytest.mark.asyncio
    async def test_no_session(self, api: API):
        with pytest.raises(SpotifyError):
            await api.albums.get_album('some random string')

    @pytest.mark.asyncio
    async def test_renew_session(self, api: API):
        await api.create_new_client()
        await api.create_new_client()
        assert api.api_request_handler.client_session is not None
        await api.close_client()

    @pytest.mark.asyncio
    async def test_invalid_album_id(self, prepared_api: API):
        with pytest.raises(SpotifyError):
            await prepared_api.albums.get_album('somerandomstring')

    @pytest.mark.asyncio
    async def test_no_auth_token(self, api: API):
        await api.create_new_client()
        with pytest.raises(SpotifyError):
            await api.albums.get_album('somerandomstring')
        await api.close_client()

    @pytest.mark.asyncio
    async def test_rate_limit(self, prepared_api: API):
        await prepared_api.create_new_client(request_timeout=5, request_limit=1000)

        album_id = '03dlqdFWY9gwJxGl3AREVy'
        with pytest.raises(RateLimitExceeded):
            await asyncio.gather(*[prepared_api.albums.get_album(album_id) for _ in range(1000)])
        await asyncio.sleep(5)
