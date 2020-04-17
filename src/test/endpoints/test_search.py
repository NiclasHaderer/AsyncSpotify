"""
Test the search endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_search.py) is part of AsyncSpotify which is released under MIT.                 #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient


class TestSearch:

    @pytest.mark.asyncio
    async def test_search(self, prepared_api: SpotifyApiClient):
        search = await prepared_api.search.start('Hello', ['album'])
        assert isinstance(search, dict)
