from async_spotify.api import API
from async_spotify.preferences import Preferences


class TestAuth:

    def test_load_secret_preferences(self):
        preferences = Preferences()
        preferences.load_from_docker_secret()

        assert None is preferences.save_preferences_to_evn()

    def test_load_os_preferences(self):
        preferences = Preferences()
        preferences.load_from_env()

        print(preferences)
        assert preferences.validate()

    def test_auth_url(self):
        preferences: Preferences = Preferences()
        preferences.load_from_env()

        api = API(preferences)
        url = api.build_authorization_url(show_dialog=False, state="TestState")
        print(url)
        assert ("show_dialog=False" in url and "state=TestState" in url)
