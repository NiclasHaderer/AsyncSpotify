# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (test_auth_flows.py) is part of AsyncSpotify which is released under MIT.             #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import pytest

from async_spotify import SpotifyApiClient
from async_spotify.authentification.authorization_flows import AuthorizationCodeFlow
from conftest import TestDataTransfer


class TestAuthFlows:

    async def test_authorization_code_flow(self, api: SpotifyApiClient):
        auth_code_flow = AuthorizationCodeFlow()
        auth_code_flow.load_from_env()
        auth_code_flow.scopes = TestDataTransfer.scopes

        api = SpotifyApiClient(auth_code_flow)
        await api.get_auth_token_with_code()

    @pytest.mark.asyncio
    async def test_client_credentials(self):
        api = SpotifyApiClient()
        await api.get_auth_token_with_client_credentials()
        await api.create_new_client()

        resp = await api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')
        assert isinstance(resp, dict)
