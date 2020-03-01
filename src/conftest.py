import pytest

from async_spotify import Preferences, API, SpotifyAuthorisationToken

scopes = ["ugc-image-upload", "user-read-playback-state", "user-read-email", "playlist-read-collaborative",
          "user-modify-playback-state", "user-read-private", "playlist-modify-public", "user-library-modify",
          "user-top-read", "user-read-currently-playing", "playlist-read-private", "user-follow-read",
          "app-remote-control", "user-read-recently-played", "playlist-modify-private", "user-follow-modify",
          "user-library-read"]


class TestDataTransfer:
    preferences: Preferences = None
    api: API = None
    spotify_code: str = None
    auth_token: SpotifyAuthorisationToken = None


@pytest.fixture(scope='session')
def py_api():
    # Get the preferences
    pref = Preferences()
    pref.load_from_env()

    # Create the api
    api = API(pref)
    return api


# Load the preferences in memory and store them
pref = Preferences()
pref.load_from_env()
TestDataTransfer.preferences = pref

# Load the api in memory and store it
api = API(pref)
TestDataTransfer.api = api
