import os
import time

import pytest

from async_spotify import SpotifyAuthorisationToken, API, SpotifyError
from async_spotify.api.response_status import ResponseStatus
from async_spotify.preferences import Preferences
from conftest import TestDataTransfer


class TestAuth:

    @pytest.mark.asyncio
    async def test_setup_test(self):
        spotify_code = await TestDataTransfer.api.get_code_with_cookie(
            os.environ.get("cookie_file_path", "/home/niclas/IdeaProjects/AsyncSpotify/src/private/cookies.txt"))

        TestDataTransfer.spotify_code = spotify_code
        await TestDataTransfer.api.create_new_client()

        auth_token = await TestDataTransfer.api.refresh_token(reauthorize=False, code=spotify_code)
        TestDataTransfer.auth_token = auth_token

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
        p = Preferences()
        with pytest.raises(SpotifyError):
            API(p)

    # Test the generation of the auth url
    def test_auth_url(self, py_api: API):
        url = py_api.build_authorization_url(show_dialog=False, state="TestState")
        assert ("show_dialog=False" in url and "state=TestState" in url)

    # Test the expiration token
    def test_not_expired_token(self):
        token = SpotifyAuthorisationToken("some random string", int(time.time()), "Another random string")
        assert False is token.is_expired()

    # Test the expiration token
    def test_expired_token(self):
        token = SpotifyAuthorisationToken("some random string", int(time.time()) - 3401, "Another random string")
        assert token.is_expired()

    # Test the retrial of the code with wrong params
    @pytest.mark.asyncio
    async def test_wrong_code_url(self):
        preferences = Preferences("test", "test", ["test"], "test")
        api = API(preferences)

        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(
                os.environ.get("cookie_file_path", "/home/niclas/IdeaProjects/AsyncSpotify/src/private/cookies.txt"))

    # Get the code from spotify
    @pytest.mark.asyncio
    async def test_code_retrieval(self, py_api: API):
        spotify_code = await py_api.get_code_with_cookie(
            os.environ.get("cookie_file_path", "/home/niclas/IdeaProjects/AsyncSpotify/src/private/cookies.txt"))

        TestDataTransfer.spotify_code = spotify_code
        assert spotify_code != ""

    # Get the auth token
    @pytest.mark.asyncio
    async def test_get_auth_code(self, py_api: API):
        await py_api.create_new_client()

        auth_token: SpotifyAuthorisationToken = await py_api.refresh_token(code=TestDataTransfer.spotify_code,
                                                                           reauthorize=False)
        assert auth_token is not None and not auth_token.is_expired()

    # Refresh the auth token
    @pytest.mark.asyncio
    async def test_refresh_auth_code(self, py_api):
        await py_api.create_new_client()
        auth_token: SpotifyAuthorisationToken = await py_api.refresh_token(TestDataTransfer.auth_token)

        TestDataTransfer.auth_token = auth_token
        assert auth_token and not auth_token.is_expired()

    # Test different response codes
    def test_response_type(self):
        assert ResponseStatus(200).success
        assert False is ResponseStatus(300).success
        assert False is ResponseStatus(400).success
        assert False is ResponseStatus(500).success
        assert False is ResponseStatus(600).success
