"""
Test the album endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_album.py) is part of AsyncSpotify which is released under MIT.                  #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import pytest

from async_spotify import API
from helpers import SetupServer


class TestAlbum(SetupServer):

    @pytest.mark.asyncio
    async def test_single_album(self, prepared_api: API):
        album_id: str = '03dlqdFWY9gwJxGl3AREVy'
        album = await prepared_api.albums.get_album(album_id)
        assert isinstance(album, dict) and album is not {}

    @pytest.mark.asyncio
    async def test_multiple_albums(self, prepared_api: API):
        album_id_list = ['03dlqdFWY9gwJxGl3AREVy', '3T1SXuvijYFbbsoIXxyhRI', '00LaE2YT3EkPBED8vLyFvp']
        album = await prepared_api.albums.get_multiple_albums(album_id_list)
        assert isinstance(album, dict) and album is not {} and isinstance(album["albums"], list)

    @pytest.mark.asyncio
    async def test_album_tracks(self, prepared_api: API):
        album_id = '03dlqdFWY9gwJxGl3AREVy'
        album = await prepared_api.albums.get_album_tracks(album_id)
        assert isinstance(album, dict) and album is not {}
