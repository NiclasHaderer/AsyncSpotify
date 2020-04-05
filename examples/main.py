"""
pass
"""

import asyncio
import json

from async_spotify import Preferences, API, SpotifyCookies
from async_spotify.spotify_errors import SpotifyAPIError


async def main():
    """
    pass
    """

    preferences = Preferences()
    preferences.load_from_env()

    cookies = SpotifyCookies()
    cookies.load_from_file('/home/niclas/IdeaProjects/AsyncSpotify/examples/private/cookies.json')

    api = API(preferences, True)

    code = await api.get_code_with_cookie(cookies)
    await api.get_auth_token_with_code(code)
    await api.create_new_client(request_limit=1500)
    album1 = await api.albums.get_album('03dlqdFWY9gwJxGl3AREVy')
    print(album1)

    try:
        await api.albums.get_album('aösldjf')
    except SpotifyAPIError as error:
        print(error.get_json())

    await api.close_client()


if __name__ == '__main__':
    asyncio.run(main())
