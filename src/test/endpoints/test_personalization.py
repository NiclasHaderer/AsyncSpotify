# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (test_personalization.py) is part of AsyncSpotify which is released under MIT.        #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import pytest

from async_spotify import SpotifyApiClient


class TestLibrary:

    @pytest.mark.asyncio
    async def test_get_top(self, prepared_api: SpotifyApiClient):
        response = await prepared_api.personalization.get_top('tracks')

        assert isinstance(response, dict)
