"""
pass
"""

import asyncio
import json

from async_spotify import Preferences, API, SpotifyCookies


async def main():
    """
    pass
    """

    preferences = Preferences()
    preferences.load_from_env()

    with open('private/cookies.json') as file:
        cookie = json.load(file)
        cookies = SpotifyCookies(cookie['sp_t'], cookie['sp_dc'], cookie['sp_key'])

    api = API(preferences, True)
    code = await api.get_code_with_cookie(cookies)
    await api.get_auth_token_with_code(code)
    await api.create_new_client()
    album = await api.albums.get_album('03dlqdFWY9gwJxGl3AREVy')
    print(album)

    await api.close_client()


if __name__ == '__main__':
    asyncio.run(main())
