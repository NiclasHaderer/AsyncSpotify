import asyncio

from async_spotify import Preferences, SpotifyApiClient, SpotifyAuthorisationToken


async def main():
    # Create a preferences object and load the preferences from env variables
    preferences = Preferences()
    preferences.load_from_env()

    # Create a new Api client
    api = SpotifyApiClient(preferences, hold_authentication=True)

    # Get the auth token with your code
    code: str = "Your Spotify Code"
    auth_token: SpotifyAuthorisationToken = await api.get_auth_token_with_code(code)

    # Create a new client
    await api.create_new_client(request_limit=1500, request_timeout=30)

    # Start making queries
    album_tracks: dict = await api.albums.get_tracks('03dlqdFWY9gwJxGl3AREVy')


if __name__ == '__main__':
    asyncio.run(main())
