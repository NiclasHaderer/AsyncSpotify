"""
Conftest file
"""

# ##################################################################################################
#  Copyright (c) 2020. HuiiBuh                                                                     #
#  This file (conftest.py) is part of AsyncSpotify which is released under MIT.                    #
#  You are not allowed to use this code or this file for another project without                   #
#  linking to the original source.                                                                 #
# ##################################################################################################
import asyncio
import json
import os

import pytest

from async_spotify import Preferences, API, SpotifyCookies


class TestDataTransfer:
    """
    Class which transfers test data
    """
    cookies: SpotifyCookies = None
    preferences: Preferences = None
    api: API = None


@pytest.fixture()
def api():
    """
    Returns: The an api instance
    """

    preferences = Preferences()
    preferences.load_from_env()

    api = API(preferences)
    return api


@pytest.fixture()
@pytest.mark.asyncio
async def prepared_api():
    """
    Returns: A ready to go api client
    """

    preferences = Preferences()
    preferences.load_from_env()

    api = API(preferences, hold_authentication=True)

    code = await api.get_code_with_cookie(TestDataTransfer.cookies, callback_server=True)
    await api.get_auth_token_with_code(code)

    await api.create_new_client()

    yield api

    await api.close_client()


def prepare_test_data():
    """
    Create the test data
    """

    def add_cookie():
        """
        Add the cookie parameter
        """

        cookies = SpotifyCookies()
        cookies.load_from_file(os.environ.get("cookie_file_path",
                                              "/home/niclas/IdeaProjects/AsyncSpotify/examples/private/cookies.json"))
        TestDataTransfer.cookies = cookies

    def add_preferences():
        """
        Add preferences parameter
        """
        preferences = Preferences()
        preferences.load_from_env()
        TestDataTransfer.preferences = preferences

    def add_api():
        """
        Add api parameter
        """
        preferences = Preferences()
        preferences.load_from_env()
        TestDataTransfer.api = API(preferences, hold_authentication=True)

    add_cookie()
    add_preferences()
    add_api()


prepare_test_data()
