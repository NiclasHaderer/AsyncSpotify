"""
Test the playlist endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (test_playlist.py) is part of AsyncSpotify which is released under MIT.               #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import base64
from typing import List

import pytest
from aiohttp import ClientSession

from async_spotify import SpotifyApiClient


class TestPlaylist:

    @pytest.mark.asyncio
    async def test_create_playlist(self, prepared_api: SpotifyApiClient):
        me = await prepared_api.user.me()
        user_id: str = me['id']

        playlist = await prepared_api.playlists.create_playlist(user_id, 'test_playlist')
        assert isinstance(playlist, dict) and playlist

        playlist_id = playlist['id']

        uris: List[str] = ['spotify:track:7FIWs0pqAYbP91WWM0vlTQ', 'spotify:track:40YbWniIEmqy6s58fYXLUh']
        songs = await prepared_api.playlists.add_tracks(playlist_id, uris, position=0)
        assert songs is None

        details = await prepared_api.playlists.change_details(playlist_id, name='test_playlist_x')
        assert details is None

        playlist_list = await prepared_api.playlists.current_get_all()
        assert isinstance(playlist_list, dict)
        playlist_list_user = await prepared_api.playlists.get_user_all(user_id)
        assert isinstance(playlist_list_user, dict)

        playlist = await prepared_api.playlists.get_one(playlist_id)
        assert isinstance(playlist, dict)

        cover = await prepared_api.playlists.get_cover(playlist_id)
        assert isinstance(cover, List)

        tracks = await prepared_api.playlists.get_tracks(playlist_id)
        assert isinstance(tracks, dict)

        reorder = {
            "range_start": 0,
            "range_length": 1,
            "insert_before": 1
        }

        reorder_return = await prepared_api.playlists.reorder_tracks(playlist_id, reorder)
        assert isinstance(reorder_return, dict)

        snapshot_id = reorder_return['snapshot_id']
        reorder_return = await prepared_api.playlists.reorder_tracks(playlist_id, reorder, snapshot_id)
        assert isinstance(reorder_return, dict)

        replace = await prepared_api.playlists.replace_tracks(playlist_id, ['spotify:track:3kW5Rq9AIL0QQuYTSKNkQw'])
        assert replace is None

        remove = await prepared_api.playlists.remove_tracks(playlist_id,
                                                            {'tracks': [
                                                               {'uri': 'spotify:track:3kW5Rq9AIL0QQuYTSKNkQw'}]})
        assert remove is None

        image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/' \
                'Spotify_logo_vertical_white.jpg/196px-Spotify_logo_vertical_white.jpg'

        async with ClientSession() as session:
            async with session.get(image) as request:
                b_64_image: bytes = await request.read()

        b_64_image = base64.b64encode(b_64_image)

        image = await prepared_api.playlists.upload_cover(playlist_id, b_64_image)
        assert image is None

        await prepared_api.follow.unfollow_playlist(playlist_id)
