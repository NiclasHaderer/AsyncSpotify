import time
from urllib.parse import urlencode

import pytest

from async_spotify import SpotifyAuthorisationToken, API, SpotifyError
from async_spotify.api.response_status import ResponseStatus
from async_spotify.preferences import Preferences
from conftest import TestDataTransfer


class TestAuth:
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

        preferences = Preferences("test", "test", ["test", "test"], "test")
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
        token = SpotifyAuthorisationToken("some random string", int(time.time()), "Another random string")
        assert False is token.is_expired()

    # Test the expiration token
    def test_expired_token(self):
        token = SpotifyAuthorisationToken("some random string", int(time.time()) - 3401, "Another random string")
        assert token.is_expired()

    # Test the retrieval of the code with wrong params
    @pytest.mark.asyncio
    async def test_wrong_code_url(self):
        preferences = Preferences("test", "test", ["test"], "test")
        api = API(preferences)

        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(TestDataTransfer.cookies)

    # Get the code from spotify
    @pytest.mark.asyncio
    async def test_code_retrieval(self, api: API):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        assert code != ""

    # Get the auth token
    @pytest.mark.asyncio
    async def test_get_auth_code(self, api: API):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)

        assert auth_token is not None and not auth_token.is_expired()

    # Refresh the auth token
    @pytest.mark.asyncio
    async def test_refresh_auth_code(self, api: API):
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)
        auth_token = await api.refresh_token(auth_token)

        assert auth_token and not auth_token.is_expired()

    # Test different response codes
    def test_response_type(self):
        assert ResponseStatus(200).success
        assert False is ResponseStatus(300).success
        assert False is ResponseStatus(400).success
        assert False is ResponseStatus(500).success
        assert False is ResponseStatus(600).success
