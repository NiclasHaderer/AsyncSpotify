# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_artist.py) is part of AsyncSpotify which is released under MIT.                 #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import pytest

from async_spotify import SpotifyApiClient


class TestArtist:

    @pytest.mark.asyncio
    async def test_single(self, prepared_api: SpotifyApiClient):
        artist = await prepared_api.artists.get_one('1YEGETLT2p8k97LIo3deHL')
        assert isinstance(artist, dict) and artist

    @pytest.mark.asyncio
    async def test_album(self, prepared_api: SpotifyApiClient):
        artist_a = await prepared_api.artists.get_album_list('1YEGETLT2p8k97LIo3deHL')
        assert isinstance(artist_a, dict) and artist_a

    @pytest.mark.asyncio
    async def test_several(self, prepared_api: SpotifyApiClient):
        artist_several = await prepared_api.artists.get_several(
            ['1YEGETLT2p8k97LIo3deHL', '7dGJo4pcD2V6oG8kP0tJRR'])

        assert isinstance(artist_several, dict) and artist_several

    @pytest.mark.asyncio
    async def test_top_tracks(self, prepared_api: SpotifyApiClient):
        artist_top = await prepared_api.artists.get_top_tracks('1YEGETLT2p8k97LIo3deHL', 'DE')
        assert isinstance(artist_top, dict) and artist_top

    @pytest.mark.asyncio
    async def test_similar(self, prepared_api: SpotifyApiClient):
        artist_similar = await prepared_api.artists.get_similar('1YEGETLT2p8k97LIo3deHL')
        assert isinstance(artist_similar, dict) and artist_similar
