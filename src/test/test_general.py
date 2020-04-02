"""
Test the album endpoint
"""
import asyncio

import pytest

from async_spotify import API, SpotifyError
from async_spotify.spotify_errors import RateLimitExceeded


class TestGeneral:

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
        album_id = '03dlqdFWY9gwJxGl3AREVy'
        with pytest.raises(RateLimitExceeded):
            await asyncio.gather(*[prepared_api.albums.get_album(album_id) for _ in range(1000)])
