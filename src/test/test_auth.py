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

from async_spotify import SpotifyApiClient
from async_spotify.api._response_status import ResponseStatus
from async_spotify.authentification import SpotifyCookie
from async_spotify.authentification.authorization_flows.authorization_code_flow import AuthorizationCodeFlow
from async_spotify.authentification.spotify_authorization_token import SpotifyAuthorisationToken
from async_spotify.spotify_errors import SpotifyError
from conftest import TestDataTransfer


class TestAuth:

    # Test cookie class
    def test_cookie(self):
        cookies = SpotifyCookie("hallo", "welt")
        assert False is cookies.valid

    def test_pass_authentication(self):
        client = SpotifyApiClient(TestDataTransfer.auth_code_flow, hold_authentication=True,
                                  spotify_authorisation_token=SpotifyAuthorisationToken(refresh_token='1'))

        assert client.spotify_authorization_token.refresh_token is '1'

    # Load auth_code_flow
    def test_load_secret_auth_flow(self):
        auth_flow = AuthorizationCodeFlow()
        auth_flow.load_from_docker_secret()

        assert False is auth_flow.valid

    # Load the auth_code_flow from os
    def test_load_os_auth_flow(self):
        auth_flow = AuthorizationCodeFlow()
        auth_flow.load_from_env()

        assert auth_flow.valid

    # Test auth_flow saving to os env
    def test_save_auth_flow_to_env(self):
        original_data = AuthorizationCodeFlow()
        original_data.load_from_env()

        auth_flow = AuthorizationCodeFlow("save-auth_code_flow", "save-auth_code_flow",
                                          ["save-auth_code_flow", "save-auth_code_flow"],
                                          "save-auth_code_flow")
        auth_flow.save_to_env()

        loaded_auth_flow = AuthorizationCodeFlow()
        loaded_auth_flow.load_from_env()

        original_data.save_to_env()

        assert auth_flow == loaded_auth_flow

    def test_load_wrong_auth_flow(self):
        auth_flow = AuthorizationCodeFlow()
        with pytest.raises(SpotifyError):
            SpotifyApiClient(auth_flow)

    # Test the generation of the auth url
    def test_auth_url(self, api: SpotifyApiClient):
        url = api.build_authorization_url(show_dialog=False, state="TestState")
        assert ("show_dialog=False" in url and
                "state=TestState" in url and
                TestDataTransfer.auth_code_flow.application_id in url and
                urlencode({"redirect_uri": TestDataTransfer.auth_code_flow.redirect_url}) in url)

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
        auth_flow = AuthorizationCodeFlow("test-with-wrong-code", "test-with-wrong-code", ["test-with-wrong-code"],
                                          "test-with-wrong-code")
        api = SpotifyApiClient(auth_flow)

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
