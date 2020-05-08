import pytest

from async_spotify import SpotifyApiClient, SpotifyAuthorisationToken, TokenExpired
from async_spotify.token_renew_class import TokenRenewClass


class FalseRenew:

    async def __call__(self, *args, **kwargs):
        return SpotifyAuthorisationToken('asdfasdf', 0, 'asdfasdf')


class TestTokenRenewClass:
    def test_getter_and_setter(self, prepared_api: SpotifyApiClient):
        renew = TokenRenewClass()
        prepared_api.token_renew_instance = renew

        assert prepared_api.token_renew_instance is renew

    @pytest.mark.asyncio
    async def test_renewal(self, prepared_api: SpotifyApiClient):
        invalid_token = prepared_api.spotify_authorization_token
        invalid_token.access_token = 'invalid'
        prepared_api.spotify_authorization_token = invalid_token

        prepared_api.token_renew_instance = TokenRenewClass()

        album = await prepared_api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')
        assert isinstance(album, dict)

    @pytest.mark.asyncio
    async def test_renewal_with_error(self, prepared_api: SpotifyApiClient):
        invalid_token = prepared_api.spotify_authorization_token
        invalid_token.access_token = 'invalid'
        prepared_api.spotify_authorization_token = invalid_token

        prepared_api.token_renew_instance = FalseRenew()

        with pytest.raises(TokenExpired):
            album = await prepared_api.albums.get_one('03dlqdFWY9gwJxGl3AREVy')
