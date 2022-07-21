# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (test_episodes.py) is part of AsyncSpotify which is released under MIT.               #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient


class TestEpisodes:

    @pytest.mark.asyncio
    async def test_single_episode(self, prepared_api: SpotifyApiClient):
        episode = await prepared_api.episodes.get_one('512ojhOuo1ktJprKbVcKyQ')
        assert isinstance(episode, dict) and episode

    @pytest.mark.asyncio
    async def test_multiple_episode(self, prepared_api: SpotifyApiClient):
        episode_list = await  prepared_api.episodes.get_multiple('512ojhOuo1ktJprKbVcKyQ')
        assert isinstance(episode_list, dict) and episode_list
