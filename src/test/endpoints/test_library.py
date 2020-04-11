# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_library.py) is part of AsyncSpotify which is released under MIT.                #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import pytest

from async_spotify import SpotifyApiClient


class TestLibrary:

    @pytest.mark.asyncio
    async def test_get(self, prepared_api: SpotifyApiClient):
        tracks = await prepared_api.library.get_tracks(limit=10)
        assert isinstance(tracks, dict) and tracks
        albums = await prepared_api.library.get_albums(limit=10)
        assert isinstance(albums, dict) and albums
        shows = await prepared_api.library.get_shows(limit=10)
        assert isinstance(shows, dict) and shows

    @pytest.mark.asyncio
    async def test_contains(self, prepared_api: SpotifyApiClient):
        album = await prepared_api.library.add_album(['07bYtmE3bPsLB6ZbmmFi8d', '48JYNjh7GMie6NjqYHMmtT'])
        assert not album
        c_album = await prepared_api.library.contains_albums(['07bYtmE3bPsLB6ZbmmFi8d', '48JYNjh7GMie6NjqYHMmtT'])
        assert c_album[0]
        album = await prepared_api.library.remove_albums(['07bYtmE3bPsLB6ZbmmFi8d', '48JYNjh7GMie6NjqYHMmtT'])
        assert not album
        c_album = await prepared_api.library.contains_albums(['07bYtmE3bPsLB6ZbmmFi8d', '48JYNjh7GMie6NjqYHMmtT'])
        assert not c_album[0]

        shows = await prepared_api.library.add_shows(['5AvwZVawapvyhJUIx71pdJ', '6ups0LMt1G8n81XLlkbsPo'])
        assert not shows
        c_shows = await prepared_api.library.contains_shows(['5AvwZVawapvyhJUIx71pdJ', '6ups0LMt1G8n81XLlkbsPo'])
        assert c_shows[0]
        shows = await prepared_api.library.remove_shows(['5AvwZVawapvyhJUIx71pdJ', '6ups0LMt1G8n81XLlkbsPo'])
        assert not shows
        c_shows = await prepared_api.library.contains_shows(['5AvwZVawapvyhJUIx71pdJ', '6ups0LMt1G8n81XLlkbsPo'])
        assert not c_shows[0]

        tracks = await prepared_api.library.add_tracks(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ'])
        assert not tracks
        c_tracks = await prepared_api.library.contains_tracks(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ'])
        assert c_tracks[0]
        tracks = await prepared_api.library.remove_tracks(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ'])
        assert not tracks
        c_tracks = await prepared_api.library.contains_tracks(['7ouMYWpwJ422jRcDASZB7P', '4VqPOruhp5EdPBeR92t6lQ'])
        assert not c_tracks[0]
