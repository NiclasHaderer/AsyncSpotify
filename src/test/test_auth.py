"""
Test the authentification
"""
# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_auth.py) is part of AsyncSpotify which is released under MIT.                   #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import os
import time
from urllib.parse import urlencode

import pytest

from async_spotify import SpotifyAuthorisationToken, API, SpotifyError, SpotifyCookies
from async_spotify.api.response_status import ResponseStatus
from async_spotify.preferences import Preferences
from conftest import TestDataTransfer
from helpers import SetupServer


class TestAuth(SetupServer):

    # Test cookie class
    def test_cookie(self):
        cookies = SpotifyCookies("hallo", "welt")
        assert False is cookies.validate()

    # Load preferences
    def test_load_secret_preferences(self):
        preferences = Preferences()
        preferences.load_from_docker_secret()

        assert False is preferences.validate()

    # Load the preferences from os
    def test_load_os_preferences(self):
        preferences = Preferences()
        preferences.load_from_env()

        assert preferences.validate()

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
            API(preferences)

    # Test the generation of the auth url
    def test_auth_url(self, api: API):
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
        api = API(preferences)

        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(TestDataTransfer.cookies, callback_server=True)

    # Get the code from spotify
    @pytest.mark.asyncio
    async def test_code_retrieval(self, api: API):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies, callback_server=True)
        assert code != ""

    # Get the code from spotify with an empty cookie
    @pytest.mark.asyncio
    async def test_code_retrieval_empty_cookie(self, api: API):
        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(SpotifyCookies(), callback_server=True)

    # Get the code from spotify with an invalid cookie
    @pytest.mark.asyncio
    async def test_code_retrieval_invalid_cookie(self, api: API):
        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(SpotifyCookies("1", "2", "3"), callback_server=True)

    # Get the auth token from spotify with an invalid code
    @pytest.mark.asyncio
    async def test_code_retrieval_invalid_code(self, api: API):
        with pytest.raises(SpotifyError):
            await api.get_auth_token_with_code('a_code_which_will_not_work')

    # Get the auth token
    @pytest.mark.asyncio
    async def test_get_auth_code(self, api: API):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies, callback_server=True)
        auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)

        assert auth_token is not None and not auth_token.is_expired()

    # Get refreshed auth token with internal token
    @pytest.mark.asyncio
    async def test_get_refresh_with_internal_auth(self, prepared_api: API):
        auth_token: SpotifyAuthorisationToken = await prepared_api.refresh_token()
        assert auth_token is not None and not auth_token.is_expired()

    # Refresh the auth token
    @pytest.mark.asyncio
    async def test_refresh_auth_code(self, api: API):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies, callback_server=True)
        auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)
        auth_token = await api.refresh_token(auth_token)

        assert auth_token and not auth_token.is_expired()

    # Get the code without server callback
    @pytest.mark.asyncio
    async def test_get_code_without_callback(self, api: API):
        github_action = os.environ.get('github_action', None)
        if github_action:
            with pytest.raises(SpotifyError):
                await api.get_code_with_cookie(TestDataTransfer.cookies)
        else:
            code = await api.get_code_with_cookie(TestDataTransfer.cookies)
            assert code != ""

    # Test different response codes
    def test_response_type(self):
        assert ResponseStatus(200).success
        assert False is ResponseStatus(300).success
        assert False is ResponseStatus(400).success
        assert False is ResponseStatus(500).success
        assert False is ResponseStatus(600).success
