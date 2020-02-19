import pytest

from async_spotify import Preferences, API

scopes = ["ugc-image-upload", "user-read-playback-state", "user-read-email", "playlist-read-collaborative",
          "user-modify-playback-state", "user-read-private", "playlist-modify-public", "user-library-modify",
          "user-top-read", "user-read-currently-playing", "playlist-read-private", "user-follow-read",
          "app-remote-control",
          "user-read-recently-played", "playlist-modify-private", "user-follow-modify", "user-library-read"]


@pytest.fixture(scope='session')
def preferences():
    pref = Preferences()
    pref.load_from_env()
    if not pref.validate():
        raise ValueError("Preferences are not correctly filled in")
    return pref


@pytest.fixture(scope='session')
def api():
    # Get the preferences
    pref = Preferences()
    pref.load_from_env()

    print(pref.redirect_url)

    # Create the api
    api = API(pref)
    return api
