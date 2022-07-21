"""
Test the search endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
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

    @pytest.mark.asyncio
    async def test_next(self, prepared_api: SpotifyApiClient):
        search = await prepared_api.search.start('Hello', ['track'])

        next_url = search['tracks']['next']
        _next = await prepared_api.next(next_url)

        assert isinstance(_next, dict)

        previous_url = _next['tracks']['previous']
        _previous = await prepared_api.previous(previous_url)
        assert isinstance(_previous, dict)
