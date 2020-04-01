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


@pytest.fixture(scope='session')
def api():
    """
    Returns: The api
    """

    preferences = Preferences()
    preferences.load_from_env()

    api = API(preferences)
    return api


def prepare_test_data():
    """
    Create the test data
    """

    def add_cookie():
        """
        Add the cookie parameter
        """

        location = os.environ.get("cookie_file_path",
                                  "/home/niclas/IdeaProjects/AsyncSpotify/examples/private/cookies.json")
        with open(location) as file:
            print(file.read())
            _cookie = json.load(file)
        TestDataTransfer.cookies = SpotifyCookies(_cookie['sp_t'], _cookie['sp_dc'], _cookie['sp_key'])

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
        TestDataTransfer.api = API(preferences, True)

    add_cookie()
    add_preferences()
    add_api()


prepare_test_data()
