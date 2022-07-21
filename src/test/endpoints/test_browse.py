# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (test_browse.py) is part of AsyncSpotify which is released under MIT.                 #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient


class TestArtist:

    @pytest.mark.asyncio
    async def test_releases(self, prepared_api: SpotifyApiClient):
        releases = await prepared_api.browse.get_new_releases()
        assert isinstance(releases, dict)

    @pytest.mark.asyncio
    async def test_featured_playlists(self, prepared_api: SpotifyApiClient):
        releases = await prepared_api.browse.get_featured_playlists()
        assert isinstance(releases, dict)

    @pytest.mark.asyncio
    async def test_categories(self, prepared_api: SpotifyApiClient):
        categories = await prepared_api.browse.get_categories()
        assert isinstance(categories, dict)

    @pytest.mark.asyncio
    async def test_single_categories(self, prepared_api: SpotifyApiClient):
        single_category = await prepared_api.browse.get_single_category('dinner')
        assert isinstance(single_category, dict)

    @pytest.mark.asyncio
    async def test_categories_playlist(self, prepared_api: SpotifyApiClient):
        category_playlist = await prepared_api.browse.get_category_playlists('dinner')
        assert isinstance(category_playlist, dict)

    @pytest.mark.asyncio
    async def test_recommendations(self, prepared_api: SpotifyApiClient):
        recommendations = await prepared_api.browse.get_recommendation_by_seed(seed_artist='7dGJo4pcD2V6oG8kP0tJRR',
                                                                               seed_tracks='7FIWs0pqAYbP91WWM0vlTQ')
        assert isinstance(recommendations, dict)

    @pytest.mark.asyncio
    async def test_genre_seeds(self, prepared_api: SpotifyApiClient):
        genre_seeds = await prepared_api.browse.get_genre_seeds()
        assert isinstance(genre_seeds, dict)
