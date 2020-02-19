import asyncio
from asyncio import sleep

from async_spotify.api import API
from async_spotify.preferences import Preferences


async def main():
    await sleep(1)
    preferences: Preferences = Preferences()
    preferences.load_from_env()
    preferences.load_from_docker_secret()

    spotify_api: API = API(preferences)
    spotify_code = await spotify_api.get_code_with_cookie(
        "/home/niclas/IdeaProjects/AsyncSpotify/src/private/cookies.txt")
    print(spotify_code)


if __name__ == '__main__':
    asyncio.run(main(), debug=False)
