"""
Test the album endpoint
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_general.py) is part of AsyncSpotify which is released under MIT.                #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import os
import time

import pytest

from async_spotify import SpotifyApiClient, SpotifyError, SpotifyAuthorisationToken, Preferences
from async_spotify.spotify_errors import SpotifyAPIError, TokenExpired


class TestGeneral:

    def test_get_hold_authentication(self, api: SpotifyApiClient):
        api.hold_authentication = False
        assert False is api.hold_authentication

        with pytest.raises(SpotifyError):
            api.spotify_authorization_token = SpotifyAuthorisationToken()

        with pytest.raises(SpotifyError):
            token = api.spotify_authorization_token

    def test_spotify_api_token(self, api):
        api.hold_authentication = True
        token = SpotifyAuthorisationToken('1', 2, '3')
        api.spotify_authorization_token = token
        assert api.spotify_authorization_token == token

    def test_api_error(self):
        d = {'a': 'b'}
        try:
            raise SpotifyAPIError(d)
        except SpotifyAPIError as e:
            assert d == e.get_json()
            assert str(d) == str(e)

    @pytest.mark.asyncio
    async def test_no_session(self, prepared_api: SpotifyApiClient):
        await prepared_api.close_client()
        with pytest.raises(SpotifyError):
            await prepared_api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')

    @pytest.mark.asyncio
    async def test_expired_token(self, prepared_api: SpotifyApiClient):
        await prepared_api.create_new_client()
        token = SpotifyAuthorisationToken(access_token='t', refresh_token='i', activation_time=int(time.time()))

        prepared_api.spotify_authorization_token = token

        with pytest.raises(TokenExpired):
            await prepared_api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')

    @pytest.mark.asyncio
    async def test_renew_session(self, prepared_api: SpotifyApiClient):

        a = prepared_api.spotify_authorization_token
        await prepared_api.create_new_client()
        await prepared_api.create_new_client()
        assert prepared_api._api_request_handler.client_session_list is not None
        await prepared_api.close_client()

    @pytest.mark.asyncio
    async def test_remove_authentication(self, prepared_api: SpotifyApiClient):
        prepared_api.hold_authentication = False
        await prepared_api.create_new_client()
        with pytest.raises(SpotifyError):
            await prepared_api.albums.get_one('somerandomstring')
        await prepared_api.close_client()

    @pytest.mark.asyncio
    async def test_unauthenticated_api(self, api: SpotifyApiClient):
        await api.create_new_client()
        with pytest.raises(SpotifyError):
            await api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')
        await api.close_client()

    @pytest.mark.asyncio
    async def test_invalid_album_id(self, prepared_api: SpotifyApiClient):
        with pytest.raises(SpotifyAPIError):
            await prepared_api.albums.get_one('somerandomstring')

    def test_open_browser(self, api: SpotifyApiClient):
        api.open_oauth_dialog_in_browser()
        assert True

    def test_docker_secret(self):

        p = Preferences()

        if os.environ.get('github_action'):
            p.load_from_docker_secret()
            assert p.application_id == 'wrong_id'
        else:
            p.load_from_docker_secret('/home/niclas/IdeaProjects/AsyncSpotify/examples/private/')
            assert p.application_id == 'wrong_id'
