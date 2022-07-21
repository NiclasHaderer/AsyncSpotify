"""
Conftest file
"""

# ##################################################################################################
#  Copyright (c) 2020. niclashaderer                                                                     #
#  This file (conftest.py) is part of AsyncSpotify which is released under MIT.                    #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################

import os
from typing import List

import pytest

from async_spotify import SpotifyApiClient
from async_spotify.authentification import SpotifyCookie
from async_spotify.authentification.authorization_flows import AuthorizationCodeFlow


class TestDataTransfer:
    """
    Class which transfers test data
    """
    cookies: SpotifyCookie = None
    auth_code_flow: AuthorizationCodeFlow = None
    api: SpotifyApiClient = None
    scopes: List[str] = None


@pytest.fixture()
def api():
    """
    Returns: The an api instance
    """

    auth_code_flow = AuthorizationCodeFlow()
    auth_code_flow.load_from_env()
    auth_code_flow.scopes = TestDataTransfer.scopes

    api = SpotifyApiClient(auth_code_flow)
    return api


@pytest.fixture()
@pytest.mark.asyncio
async def prepared_api():
    """
    Returns: A ready to go api client
    """

    auth_code_flow = AuthorizationCodeFlow()
    auth_code_flow.load_from_env()
    auth_code_flow.scopes = TestDataTransfer.scopes

    api = SpotifyApiClient(auth_code_flow, hold_authentication=True)
    code = await api.get_code_with_cookie(TestDataTransfer.cookies)
    await api.get_auth_token_with_code(code)

    await api.create_new_client()

    yield api

    await api.close_client()


def prepare_test_data():
    """
    Create the test data
    """

    def add_scopes():
        """
        Add scopes to the TestDataTransfer class
        """

        scopes = ["ugc-image-upload", "user-read-playback-state", "user-read-email", "playlist-read-collaborative",
                  "user-modify-playback-state", "user-read-private", "playlist-modify-public",
                  "user-library-modify", "user-top-read", "user-read-currently-playing", "playlist-read-private",
                  "user-follow-read app-remote-control", "user-read-recently-played", "playlist-modify-private",
                  "user-follow-modify", "user-library-read"]
        TestDataTransfer.scopes = scopes

    def add_cookie():
        """
        Add the cookie parameter
        """

        cookies = SpotifyCookie()
        cookies.load_from_file(os.environ["cookie_file_path"])
        TestDataTransfer.cookies = cookies

    def add_auth_code_flow():
        """
        Add auth_code_flow parameter
        """
        auth_code_flow = AuthorizationCodeFlow()
        auth_code_flow.load_from_env()
        auth_code_flow.scopes = TestDataTransfer.scopes
        TestDataTransfer.auth_code_flow = auth_code_flow

    def add_api():
        """
        Add api parameter
        """
        auth_code_flow = AuthorizationCodeFlow()
        auth_code_flow.load_from_env()
        auth_code_flow.scopes = TestDataTransfer.scopes

        TestDataTransfer.api = SpotifyApiClient(auth_code_flow, hold_authentication=True)

    add_scopes()
    add_cookie()
    add_auth_code_flow()
    add_api()


prepare_test_data()
