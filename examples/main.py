"""
pass
"""

import asyncio

from async_spotify import Preferences, SpotifyApiClient, SpotifyCookies
from async_spotify.typing import TAlbums, TAritst, TArtistAlbums, TTrackList


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
    album1 = await api.albums.get_one('03dlqdFWY9gwJxGl3AREVy', market='DE')
    album_tracks = await api.albums.get_tracks('03dlqdFWY9gwJxGl3AREVy')
    album2: TAlbums = await api.albums.get_multiple(['03dlqdFWY9gwJxGl3AREVy', '3T1SXuvijYFbbsoIXxyhRI'])

    artist: TAritst = await api.artist.get_one('1YEGETLT2p8k97LIo3deHL')
    artist_a: TArtistAlbums = await api.artist.album_list('1YEGETLT2p8k97LIo3deHL')
    artist_top: TTrackList = await api.artist.top_tracks('1YEGETLT2p8k97LIo3deHL', 'DE')
    artist_several: TTrackList = await api.artist.several(['1YEGETLT2p8k97LIo3deHL', '7dGJo4pcD2V6oG8kP0tJRR'])

    await api.close_client()


if __name__ == '__main__':
    asyncio.run(main())
