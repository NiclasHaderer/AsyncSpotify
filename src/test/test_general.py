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

from async_spotify import API, SpotifyError, SpotifyAuthorisationToken
from async_spotify.spotify_errors import RateLimitExceeded, SpotifyAPIError


class TestGeneral:

    def test_get_hold_authentication(self, api: API):
        api.hold_authentication = False
        assert False is api.hold_authentication

    def test_spotify_api_token(self, api):
        token = SpotifyAuthorisationToken('1', 2, '3')
        api.spotify_authorization_token = token
        assert api.spotify_authorization_token == token

    def test_api_error(self):
        d = {'a': 'b'}
        try:
            raise SpotifyAPIError(d)
        except SpotifyAPIError as e:
            assert d == e.get_json()
            assert str(d) == str(e)

    @pytest.mark.asyncio
    async def test_no_session(self, prepared_api: API):
        await prepared_api.close_client()
        with pytest.raises(SpotifyError):
            await prepared_api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')

    @pytest.mark.asyncio
    async def test_renew_session(self, prepared_api: API):
        await prepared_api.create_new_client()
        await prepared_api.create_new_client()
        assert prepared_api._api_request_handler.client_session_list is not None
        await prepared_api.close_client()

    @pytest.mark.asyncio
    async def test_remove_authentication(self, prepared_api: API):
        prepared_api.hold_authentication = False
        await prepared_api.create_new_client()
        with pytest.raises(SpotifyError):
            await prepared_api.albums.get_one('somerandomstring')
        await prepared_api.close_client()

    @pytest.mark.asyncio
    async def test_unauthenticated_api(self, api: API):
        await api.create_new_client()
        with pytest.raises(SpotifyError):
            await api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')
        await api.close_client()

    @pytest.mark.asyncio
    async def test_invalid_album_id(self, prepared_api: API):
        with pytest.raises(SpotifyAPIError):
            await prepared_api.albums.get_one('somerandomstring')

    @pytest.mark.asyncio
    async def test_rate_limit(self, prepared_api: API):
        await prepared_api.create_new_client(request_timeout=5, request_limit=1000)

        album_id = '03dlqdFWY9gwJxGl3AREVy'
        with pytest.raises(RateLimitExceeded):
            await asyncio.gather(*[prepared_api.albums.get_one(album_id) for _ in range(1000)])
        await asyncio.sleep(5)
