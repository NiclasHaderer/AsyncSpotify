"""
Test show endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_show.py) is part of AsyncSpotify which is released under MIT.                   #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient


class TestShow:

    @pytest.mark.asyncio
    async def test_one(self, prepared_api: SpotifyApiClient):
        show = await prepared_api.show.get_one('38bS44xjbVVZ3No3ByF1dJ')
        assert isinstance(show, dict) and show

    @pytest.mark.asyncio
    async def test_several(self, prepared_api: SpotifyApiClient):
        show = await prepared_api.show.get_several(['5CfCWKI5pZ28U0uOzXkDHe', '5as3aKmN2k11yfDDDSrvaZ'])
        assert isinstance(show, dict) and show

    @pytest.mark.asyncio
    async def test_episodes(self, prepared_api: SpotifyApiClient):
        show = await prepared_api.show.get_episodes('38bS44xjbVVZ3No3ByF1dJ')
        assert isinstance(show, dict) and show
