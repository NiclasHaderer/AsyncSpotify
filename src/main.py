import asyncio
import json
import subprocess
from asyncio import sleep
from json import JSONDecodeError
from subprocess import CompletedProcess

from async_spotify.api import API
from async_spotify.authentification.preferences import Preferences


class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


async def main():
    await sleep(1)
    preferences: Preferences = Preferences()
    preferences.load_from_env()
    preferences.load_from_docker_secret()

    spotify_api: API = API(preferences)
    spotify_code = spotify_api.get_code_with_cookie("/home/niclas/Downloads/cookies.txt")
    print(spotify_code)

asyncio.run(main(), debug=True)
