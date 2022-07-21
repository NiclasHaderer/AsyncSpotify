# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (test_follow.py) is part of AsyncSpotify which is released under MIT.                 #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

from typing import List

import pytest

from async_spotify import SpotifyApiClient


class TestFollow:

    @pytest.mark.asyncio
    async def test_follow_status(self, prepared_api: SpotifyApiClient):
        follow_type = await prepared_api.follow.check_follow('artist', ['7dGJo4pcD2V6oG8kP0tJRR'])
        assert isinstance(follow_type, List) and follow_type[0]

    @pytest.mark.asyncio
    async def test_follow_playlist(self, prepared_api: SpotifyApiClient):
        follow = await prepared_api.follow.unfollow_playlist('37i9dQZF1DXbTxeAdrVG2l')
        assert not follow

        follow_playlist = await prepared_api.follow.check_follow_playlist('37i9dQZF1DXbTxeAdrVG2l', ['nhaderer'])
        assert isinstance(follow_playlist, List) and not follow_playlist[0]

        follow = await prepared_api.follow.follow_playlist('37i9dQZF1DXbTxeAdrVG2l')
        assert not follow

        follow_playlist = await prepared_api.follow.check_follow_playlist('37i9dQZF1DXbTxeAdrVG2l', ['nhaderer'])
        assert isinstance(follow_playlist, List) and follow_playlist[0]

        follow = await prepared_api.follow.unfollow_playlist('37i9dQZF1DXbTxeAdrVG2l')
        assert not follow

    @pytest.mark.asyncio
    async def test_follow_artist(self, prepared_api: SpotifyApiClient):
        follow_playlist = await prepared_api.follow.follow_artist_or_user('artist', ['2NjfBq1NflQcKSeiDooVjY'])
        assert not follow_playlist

        follow_playlist = await prepared_api.follow.unfollow_artist_or_user('artist', ['2NjfBq1NflQcKSeiDooVjY'])
        assert not follow_playlist

        follow_type = await prepared_api.follow.check_follow('artist', ['2NjfBq1NflQcKSeiDooVjY'])
        assert isinstance(follow_type, List) and not follow_type[0]

    @pytest.mark.asyncio
    async def test_get_artist(self, prepared_api: SpotifyApiClient):
        follow_artist = await prepared_api.follow.get_followed_artist()
        assert isinstance(follow_artist, dict) and follow_artist
