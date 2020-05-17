# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_client_credentials.py) is part of AsyncSpotify which is released under MIT.     #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import pytest

from async_spotify import SpotifyApiClient


@pytest.mark.asyncio
async def test_client_credentials(api: SpotifyApiClient):
    auth_token = await api.get_auth_token_with_client_credentials()
    await api.create_new_client()

    resp = await api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')
    assert isinstance(resp, dict)
