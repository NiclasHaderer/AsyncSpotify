# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_auth_flows.py) is part of AsyncSpotify which is released under MIT.             #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient
from async_spotify.authentification.authorization_flows import AuthorizationCodeFlow
from async_spotify.authentification.authorization_flows.client_credentials_flow import ClientCredentialsFlow
from async_spotify.spotify_errors import SpotifyError
from conftest import TestDataTransfer


class TestAuthFlows:

    @pytest.mark.asyncio
    async def test_authorization_code_flow(self, api: SpotifyApiClient):
        auth_code_flow = AuthorizationCodeFlow()
        auth_code_flow.load_from_env()
        auth_code_flow.scopes = TestDataTransfer.scopes

        api = SpotifyApiClient(auth_code_flow)
        code = await api.get_code_with_cookie(TestDataTransfer.cookies)
        await api.get_auth_token_with_code(code)

    @pytest.mark.asyncio
    async def test_inability_to_get_token_with_client_credentials(self, api: SpotifyApiClient):
        auth_code_flow = AuthorizationCodeFlow()
        auth_code_flow.load_from_env()

        api = SpotifyApiClient(auth_code_flow)
        with pytest.raises(SpotifyError):
            await api.get_auth_token_with_client_credentials()

    @pytest.mark.asyncio
    async def test_client_credentials(self):
        client_credentials = ClientCredentialsFlow()
        client_credentials.load_from_env()
        client_credentials.scopes = TestDataTransfer.scopes

        api = SpotifyApiClient(client_credentials)
        await api.get_auth_token_with_client_credentials()
        await api.create_new_client()

        resp = await api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')
        assert isinstance(resp, dict)

    @pytest.mark.asyncio
    async def test_inability_to_get_token_client_credential(self):
        client_credentials = ClientCredentialsFlow()
        client_credentials.load_from_env()
        client_credentials.scopes = TestDataTransfer.scopes

        api = SpotifyApiClient(client_credentials)
        with pytest.raises(SpotifyError):
            await api.get_code_with_cookie(TestDataTransfer.cookies)

    def test_client_valid(self):
        c = ClientCredentialsFlow()
        c.load_from_env()
        v = c.valid
        assert v
        c.application_secret = None

        v = c.valid
        assert not v

    def test_invalid_access(self):
        c = ClientCredentialsFlow()
        with pytest.raises(KeyError):
            c["will_error"] = "test"

        with pytest.raises(KeyError):
            v = c["will_error"]
