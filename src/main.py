import asyncio

from async_spotify.api import API
from async_spotify.authentification.preferences import Preferences


async def main():
    preferences = Preferences()
    preferences.load_from_env()
    preferences.load_from_docker_secret()

    spotify_api = API(preferences)
    # spotify_api.open_oauth_dialog_in_browser(show_dialogue=False)
    await spotify_api.refresh_token("token", reauthorize=False)


asyncio.run(main(), debug=True)
