"""
Test the authentification
"""
# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_auth.py) is part of AsyncSpotify which is released under MIT.                   #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import time
from urllib.parse import urlencode

import pytest

from async_spotify import SpotifyAuthorisationToken, SpotifyApiClient, SpotifyError, SpotifyCookie
from async_spotify.api._response_status import ResponseStatus
from async_spotify.api.preferences import Preferences
from conftest import TestDataTransfer


class TestAuth:

    # Test cookie class
    def test_cookie(self):
        cookies = SpotifyCookie("hallo", "welt")
        assert False is cookies.valid

    def test_pass_authentication(self):
        client = SpotifyApiClient(TestDataTransfer.preferences, hold_authentication=True,
                                  spotify_authorisation_token=SpotifyAuthorisationToken(refresh_token='1'))

        assert client.spotify_authorization_token.refresh_token is '1'

    # Load preferences
    def test_load_secret_preferences(self):
        preferences = Preferences()
        preferences.load_from_docker_secret()

        assert False is preferences.valid

    # Load the preferences from os
    def test_load_os_preferences(self):
        preferences = Preferences()
        preferences.load_from_env()

        assert preferences.valid

    # Test preference saving to os env
    def test_save_preferences_to_env(self):
        original_data = Preferences()
        original_data.load_from_env()

        preferences = Preferences("save-preferences", "save-preferences", ["save-preferences", "save-preferences"],
                                  "save-preferences")
        preferences.save_preferences_to_evn()

        loaded_preferences = Preferences()
        loaded_preferences.load_from_env()

        original_data.save_preferences_to_evn()

        assert preferences == loaded_preferences

    def test_load_wrong_preferences(self):
        preferences = Preferences()
        with pytest.raises(SpotifyError):
            SpotifyApiClient(preferences)

    # Test the generation of the auth url
    def test_auth_url(self, api: SpotifyApiClient):
        url = api.build_authorization_url(show_dialog=False, state="TestState")
        assert ("show_dialog=False" in url and
                "state=TestState" in url and
                TestDataTransfer.preferences.application_id in url and
                urlencode({"redirect_uri": TestDataTransfer.preferences.redirect_url}) in url)

    # Test the expiration token
    def test_not_expired_token(self):
        token = SpotifyAuthorisationToken("expired token", int(time.time()), "expired token")
        assert False is token.is_expired()

    # Test the expiration token
    def test_expired_token(self):
        token = SpotifyAuthorisationToken("not expired token", int(time.time()) - 3401, "not expired token")
        assert token.is_expired()

    # Test the retrieval of the code with wrong params
    @pytest.mark.asyncio
    async def test_wrong_code_url(self):
        preferences = Preferences("test-with-wrong-code", "test-with-wrong-code", ["test-with-wrong-code"],
                                  "test-with-wrong-code")
        api = SpotifyApiClient(preferences)

        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(TestDataTransfer.cookies)

    # Get the code from spotify
    @pytest.mark.asyncio
    async def test_code_retrieval(self, api: SpotifyApiClient):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        assert code != ""

    # Get the code from spotify with an empty cookie
    @pytest.mark.asyncio
    async def test_code_retrieval_empty_cookie(self, api: SpotifyApiClient):
        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(SpotifyCookie())

    # Get the code from spotify with an invalid cookie
    @pytest.mark.asyncio
    async def test_code_retrieval_invalid_cookie(self, api: SpotifyApiClient):
        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(SpotifyCookie("1", "2", "3"))

    # Get the auth token from spotify with an invalid code
    @pytest.mark.asyncio
    async def test_code_retrieval_invalid_code(self, api: SpotifyApiClient):
        with pytest.raises(SpotifyError):
            await api.get_auth_token_with_code('a_code_which_will_not_work')

    # Get the auth token
    @pytest.mark.asyncio
    async def test_get_auth_code(self, api: SpotifyApiClient):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)

        assert auth_token is not None and not auth_token.is_expired()

    # Get refreshed auth token with internal token
    @pytest.mark.asyncio
    async def test_get_refresh_with_internal_auth(self, prepared_api: SpotifyApiClient):
        auth_token: SpotifyAuthorisationToken = await prepared_api.refresh_token()
        assert auth_token is not None and not auth_token.is_expired()

    # Refresh the auth token
    @pytest.mark.asyncio
    async def test_refresh_auth_code(self, api: SpotifyApiClient):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)
        auth_token = await api.refresh_token(auth_token)

        assert auth_token and not auth_token.is_expired()

    # Get the code without server callback
    @pytest.mark.asyncio
    async def test_get_code_without_callback(self, api: SpotifyApiClient):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        assert code != ""

    # Test different response codes
    def test_response_type(self):
        assert ResponseStatus(200).success
        assert False is ResponseStatus(300).success
        assert False is ResponseStatus(400).success
        assert False is ResponseStatus(500).success
        assert False is ResponseStatus(600).success
