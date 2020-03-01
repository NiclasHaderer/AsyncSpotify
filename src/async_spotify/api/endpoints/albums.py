"""
Handle the requests to the albums endpoint
"""

from typing import List

from .decorators import make_request
from .urls import URLS
from ...authentification.spotify_authorization_token import SpotifyAuthorisationToken


class Albums:
    """
    Wraps the spotify album functions
    """

    @staticmethod
    @make_request(URLS.ALBUM.ONE, method="GET")
    async def get_album(album_id: str, auth_token: SpotifyAuthorisationToken = None, **kwargs) -> dict:
        """
        Get the album with the specific spotify album id

        Args:
            auth_token: The auth token if you set the api class not to keep the token in memory
            album_id: The album id of the album you want to get
            kwargs: Optional arguments as keyword args

        Note:
            [https://developer.spotify.com/documentation/web-api/reference/albums/get-album/](https://developer.spotify.com/documentation/web-api/reference/albums/get-album/)

        Returns:
            The album json
        """

        required_args = {"id": album_id}
        return {**required_args, **kwargs}, auth_token

    @staticmethod
    async def get_album_tracks(album_id: str) -> dict:
        """
        Get the tracks of an album

        Args:
            album_id: The id of the album

        Note:
            [https://developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/](https://developer.spotify.com/documentation/web-api/reference/albums/get-albums-tracks/)

        Returns:
            The api response from spotify
        """
        pass

    async def get_multiple_albums(self, album_id_list: List[str]) -> dict:
        """
        Get All the albums specified in the album_id_list

        Args:
            album_id_list: The list of the spotify album ids

        Note:
            [https://developer.spotify.com/documentation/web-api/reference/albums/get-several-albums/](https://developer.spotify.com/documentation/web-api/reference/albums/get-several-albums/)

        Returns:
            The api response from spotify
        """
        pass
