# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_rate_limit.py) is part of AsyncSpotify which is released under MIT.             #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import asyncio

import pytest
from aiohttp import ClientOSError

from async_spotify import SpotifyApiClient
from async_spotify.spotify_errors import RateLimitExceeded


@pytest.mark.asyncio
async def test_rate_limit(prepared_api: SpotifyApiClient):
    await prepared_api.create_new_client(request_timeout=5, request_limit=1000)

    album_id = '03dlqdFWY9gwJxGl3AREVy'
    with pytest.raises(RateLimitExceeded):
        try:
            await asyncio.gather(*[prepared_api.albums.get_one(album_id) for _ in range(1000)])
        except (ClientOSError, TimeoutError):
            pass
    await asyncio.sleep(5)
