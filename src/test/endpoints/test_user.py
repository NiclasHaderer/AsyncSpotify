"""
Test user endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (test_user.py) is part of AsyncSpotify which is released under MIT.                   #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient


class TestUser:

    @pytest.mark.asyncio
    async def test_user(self, prepared_api: SpotifyApiClient):
        me = await prepared_api.user.me()
        uri = me['id']
        me2 = await prepared_api.user.get_one(uri)

        assert me2['uri'] == me['uri']
