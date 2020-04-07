"""
pass
"""

import asyncio

from async_spotify import Preferences, SpotifyApiClient, SpotifyCookies


async def make_requests(api: SpotifyApiClient):
    """
    pass
    """




async def main():
    """
    pass
    """

    preferences = Preferences()
    preferences.load_from_env()

    cookies = SpotifyCookies()
    cookies.load_from_file('/home/niclas/IdeaProjects/AsyncSpotify/examples/private/cookies.json')

    api = SpotifyApiClient(preferences, True)

    code = await api.get_code_with_cookie(cookies)
    await api.get_auth_token_with_code(code)
    await api.create_new_client(request_limit=1500)

    await make_requests(api)

    await api.close_client()


if __name__ == '__main__':
    asyncio.run(main())
